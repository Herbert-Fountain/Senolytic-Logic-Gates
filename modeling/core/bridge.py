"""
Bridge between the Circuit Designer and the Modeling Tool.

The circuit designer (tools/circuit_designer.py) identifies candidate miRNAs
and proposes circuit architectures. This bridge takes those designs and runs
them through the modeling tool to produce quantitative performance predictions.

Workflow:
  1. Circuit designer outputs: candidate miRNAs with fold changes and
     proposed circuit architectures with estimated selectivity
  2. This bridge converts those into modeling tool inputs:
     cell profiles with miRNA copy numbers, circuit configurations
  3. The modeling tool simulates each circuit and returns:
     predicted % positive, ON:OFF ratio, optimal dosing

Usage:
    from modeling.core.bridge import CircuitBridge

    bridge = CircuitBridge()

    # From circuit designer output
    results = bridge.evaluate_circuit_design(circuit_design, cell_profiles)

    # Or directly from miRNA names and fold changes
    results = bridge.evaluate_mirna_candidates(
        mirna_data={'miR-34a-5p': {'fc': 3.5, 'target_cpm': 558}},
        target_cell='senescent_WI38',
        control_cell='quiescent_WI38',
    )
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modeling.core.optimizer import CircuitOptimizer
from modeling.core.parameters import get_params
from modeling.core.history import ExperimentHistory


# Approximate CPM-to-copies calibration
# Based on miR-122 in HuH7: ~8000 functional copies at high CPM
# This is a rough estimate; calibration from experimental data improves it
DEFAULT_CPM_TO_COPIES = 15  # copies per cell per CPM unit


class CircuitBridge:
    """Connect circuit designer output to the modeling tool."""

    def __init__(self, params=None, history_path=None):
        self.params = params or get_params(
            L7Ae_repression_fold=1000, t_max_hr=24)
        self.optimizer = CircuitOptimizer(self.params)

        if history_path:
            self.history = ExperimentHistory(history_path)
        else:
            self.history = None

    def mirna_cpm_to_copies(self, cpm, calibration_factor=None):
        """Convert CPM (counts per million) to estimated copies per cell.

        Parameters
        ----------
        cpm : float
            miRNA expression in CPM
        calibration_factor : float, optional
            Copies per CPM. Default: 15 (rough estimate).
            Improves with calibration data.

        Returns
        -------
        float : estimated copies per cell
        """
        factor = calibration_factor or DEFAULT_CPM_TO_COPIES
        return cpm * factor

    def evaluate_circuit_design(self, circuit, target_profile,
                                 control_profile, total_mRNA_ng=200,
                                 cpm_to_copies=None):
        """Evaluate a circuit design from the circuit designer.

        Parameters
        ----------
        circuit : dict
            From CircuitDesigner.design_circuits(). Expected keys:
            - inputs: list of {miRNA, type, target_cpm, control_cpm, fc}
            - estimated_selectivity: float
        target_profile : dict
            {transfection_efficiency, expression_factor}
        control_profile : dict
            {transfection_efficiency, expression_factor}
        total_mRNA_ng : float
            Total mRNA budget per well
        cpm_to_copies : float, optional
            CPM to copies conversion factor

        Returns
        -------
        dict with simulation results, optimal dosing, and comparison
        """
        factor = cpm_to_copies or DEFAULT_CPM_TO_COPIES

        # For the simplest AND gate (single miRNA input):
        # The circuit has one sensor mRNA responsive to one miRNA
        # All other inputs are additional L7Ae mRNAs with different MREs

        # For now, model the DOMINANT input (highest discrimination)
        inputs = circuit.get('inputs', [])
        if not inputs:
            return {'error': 'No inputs in circuit design'}

        # Find the primary input (highest fold change)
        primary = max(inputs, key=lambda x: abs(
            np.log2(x.get('fc', x.get('discrimination', 1)))))

        mirna_name = primary.get('miRNA', 'unknown')
        switch_type = primary.get('type', 'ON')
        target_cpm = primary.get('target_cpm', 0)
        control_cpm = primary.get('control_cpm', 0)

        # Convert CPM to copies
        target_copies = self.mirna_cpm_to_copies(target_cpm, factor)
        control_copies = self.mirna_cpm_to_copies(control_cpm, factor)

        # Build cell profiles for the optimizer
        if switch_type == 'ON':
            # miRNA is UP in target -> target cell has high miRNA
            cell_profiles = {
                'target': {
                    'mirna_mean': target_copies,
                    'mirna_cv': 0.5,
                    'transfection_efficiency': target_profile.get(
                        'transfection_efficiency', 0.5),
                    'expression_factor': target_profile.get(
                        'expression_factor', 1.0),
                },
                'control': {
                    'mirna_mean': control_copies,
                    'mirna_cv': 0.5,
                    'transfection_efficiency': control_profile.get(
                        'transfection_efficiency', 0.5),
                    'expression_factor': control_profile.get(
                        'expression_factor', 1.0),
                },
            }
        else:
            # OFF switch: miRNA is DOWN in target
            # In OFF switch, miRNA REPRESSES the payload
            # High miRNA = payload OFF, low miRNA = payload ON
            cell_profiles = {
                'target': {
                    'mirna_mean': control_copies,  # Swap: target has LOW miRNA
                    'mirna_cv': 0.5,
                    'transfection_efficiency': target_profile.get(
                        'transfection_efficiency', 0.5),
                    'expression_factor': target_profile.get(
                        'expression_factor', 1.0),
                },
                'control': {
                    'mirna_mean': target_copies,  # Control has HIGH miRNA
                    'mirna_cv': 0.5,
                    'transfection_efficiency': control_profile.get(
                        'transfection_efficiency', 0.5),
                    'expression_factor': control_profile.get(
                        'expression_factor', 1.0),
                },
            }

        # Run optimization
        opt_result = self.optimizer.optimize_ratio(
            total_mRNA_ng, cell_profiles,
            objective='balanced', n_cells=15000)

        # Also run at 1:1 for comparison
        result_1to1 = self.optimizer.optimize_ratio(
            total_mRNA_ng, cell_profiles,
            objective='balanced',
            sp_ratios=[1.0], n_cells=15000)

        best = opt_result['best']
        baseline = result_1to1['sweep'][0] if result_1to1['sweep'] else None

        return {
            'mirna': mirna_name,
            'switch_type': switch_type,
            'target_copies': target_copies,
            'control_copies': control_copies,
            'fold_change': target_cpm / max(control_cpm, 1),
            'designer_selectivity': circuit.get('estimated_selectivity', 0),
            'model_selectivity_1to1': baseline['ratio'] if baseline else 0,
            'model_selectivity_optimal': best['ratio'],
            'optimal_sensor_ng': best['sensor_ng'],
            'optimal_payload_ng': best['payload_ng'],
            'optimal_sp_ratio': best['sp_ratio'],
            'target_pct_optimal': best['on_pct'],
            'control_pct_optimal': best['off_pct'],
            'target_pct_1to1': baseline['on_pct'] if baseline else 0,
            'control_pct_1to1': baseline['off_pct'] if baseline else 0,
            'full_sweep': opt_result['sweep'],
            'cell_profiles': cell_profiles,
        }

    def evaluate_mirna_candidates(self, mirna_data, target_cell,
                                   control_cell, target_te=0.5,
                                   control_te=0.5, total_mRNA_ng=200):
        """Evaluate individual miRNA candidates as circuit inputs.

        Parameters
        ----------
        mirna_data : dict
            {mirna_name: {fc, target_cpm, control_cpm, type}}
        target_cell : str
            Name of target cell type
        control_cell : str
            Name of control cell type
        target_te : float
            Target cell transfection efficiency
        control_te : float
            Control cell transfection efficiency
        total_mRNA_ng : float

        Returns
        -------
        list of dict : ranked candidates with modeling predictions
        """
        results = []

        for mirna_name, data in mirna_data.items():
            circuit = {
                'inputs': [{
                    'miRNA': mirna_name,
                    'type': data.get('type', 'ON'),
                    'target_cpm': data.get('target_cpm', 0),
                    'control_cpm': data.get('control_cpm', 0),
                    'fc': data.get('fc', 1),
                }],
                'estimated_selectivity': data.get('fc', 1),
            }

            target_profile = {
                'transfection_efficiency': target_te,
                'expression_factor': 1.0,
            }
            control_profile = {
                'transfection_efficiency': control_te,
                'expression_factor': 1.0,
            }

            result = self.evaluate_circuit_design(
                circuit, target_profile, control_profile, total_mRNA_ng)

            results.append(result)

        # Sort by model selectivity
        results.sort(key=lambda r: r.get('model_selectivity_optimal', 0),
                     reverse=True)

        return results

    def format_evaluation_report(self, results):
        """Format evaluation results as readable text."""
        if isinstance(results, dict):
            results = [results]

        lines = []
        lines.append('=' * 75)
        lines.append('CIRCUIT DESIGN EVALUATION REPORT')
        lines.append('=' * 75)
        lines.append('')

        lines.append(f'{"miRNA":<20s} {"Type":>5s} {"FC":>6s} '
                      f'{"Designer":>10s} {"Model(1:1)":>11s} '
                      f'{"Model(opt)":>11s} {"Opt S:P":>8s}')
        lines.append('-' * 75)

        for r in results:
            lines.append(
                f'{r["mirna"]:<20s} {r["switch_type"]:>5s} '
                f'{r["fold_change"]:5.1f}x '
                f'{r["designer_selectivity"]:9.1f}x '
                f'{r["model_selectivity_1to1"]:10.1f}x '
                f'{r["model_selectivity_optimal"]:10.1f}x '
                f'{r["optimal_sp_ratio"]:7.2f}:1')

        if results:
            best = results[0]
            lines.append('')
            lines.append(f'TOP CANDIDATE: {best["mirna"]}')
            lines.append(f'  Optimal dosing: {best["optimal_sensor_ng"]:.0f}ng '
                          f'sensor + {best["optimal_payload_ng"]:.0f}ng payload')
            lines.append(f'  Predicted selectivity: {best["model_selectivity_optimal"]:.1f}x')
            lines.append(f'  Target cells: {best["target_pct_optimal"]:.1f}% positive')
            lines.append(f'  Control cells: {best["control_pct_optimal"]:.2f}% positive')

        return '\n'.join(lines)
