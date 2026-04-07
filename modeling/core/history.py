"""
Experiment history and persistent data storage.

Stores all experimental observations, model predictions, fitted parameters,
and calibration history in a structured JSON database. Supports:

  - Recording experiments with conditions, observations, and metadata
  - Tracking parameter evolution across calibration rounds
  - Cumulative calibration: fitting against ALL historical data
  - Splitting parameters into universal (shared across experiments)
    and experiment-specific (per cell line, per construct)
  - Exporting history for analysis and publication

Data architecture:
  experiments/         One entry per physical experiment
    conditions[]       Each well/condition with observed results
    metadata           Date, constructs, cell lines, cytometer
  calibrations/        One entry per model fitting round
    parameters_before  Parameters at start of calibration
    parameters_after   Fitted parameters
    residuals[]        Per-condition prediction errors
  parameters/          Current best parameter estimates
    universal          Shared across all experiments (kinetics, binding)
    cell_lines/        Per-cell-line parameters (TE, miRNA, expression)
    constructs/        Per-construct parameters (if applicable)
"""

import json
import os
from datetime import datetime
from copy import deepcopy


class ExperimentHistory:
    """Persistent storage for experiments, calibrations, and parameters."""

    def __init__(self, db_path=None):
        """Initialize or load experiment history.

        Parameters
        ----------
        db_path : str, optional
            Path to JSON database file. Default: modeling/data/history.json
        """
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'data', 'history.json')

        self.db_path = db_path
        self.data = self._load_or_create()

    def _load_or_create(self):
        """Load existing database or create a new one."""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {
            'version': '1.0',
            'created': datetime.now().isoformat(),
            'experiments': [],
            'calibrations': [],
            'parameters': {
                'universal': {
                    'mRNA_halflife_hr': 12.0,
                    'k_translate': 100.0,
                    'kon_RISC': 0.003,
                    'k_slice': 18.0,
                    'Kd_L7Ae_nM': 0.9,
                    'L7Ae_repression_fold': 1000.0,
                    'GFP_halflife_hr': 26.0,
                    'L7Ae_halflife_hr': 20.0,
                    'delivery_cv': 0.5,
                    'delivery_correlation': 0.7,
                },
                'cell_lines': {},
                'constructs': {},
            },
        }

    def save(self):
        """Save database to disk."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.data['last_modified'] = datetime.now().isoformat()
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)

    # ================================================================
    # Experiment Recording
    # ================================================================

    def add_experiment(self, name, conditions, metadata=None):
        """Record a new experiment with observed results.

        Parameters
        ----------
        name : str
            Experiment identifier (e.g., 'ON Switch Titration 4/15/2026')
        conditions : list of dict
            Each condition: {
                'cell_type': str,
                'sensor_ng': float,
                'payload_ng': float,
                'observed_pct': float,      # Live sfGFP+ %
                'observed_mfi': float,       # optional: median FITC-A
                'replicate_values': list,    # optional: per-replicate %
                'condition_label': str,      # optional
            }
        metadata : dict, optional
            {
                'date': str,
                'constructs': {'sensor': str, 'payload': str},
                'cytometer': str,
                'cells_per_well': int,
                'transfection_reagent': str,
                'notes': str,
            }

        Returns
        -------
        int : experiment index
        """
        experiment = {
            'name': name,
            'timestamp': datetime.now().isoformat(),
            'conditions': conditions,
            'metadata': metadata or {},
            'n_conditions': len(conditions),
        }

        # Register any new cell lines
        for cond in conditions:
            cell = cond.get('cell_type', '')
            if cell and cell not in self.data['parameters']['cell_lines']:
                self.data['parameters']['cell_lines'][cell] = {
                    'mirna_mean': 0,
                    'mirna_cv': 0.5,
                    'transfection_efficiency': 0.5,
                    'expression_factor': 1.0,
                    'notes': 'Auto-created; needs calibration',
                }

        self.data['experiments'].append(experiment)
        self.save()
        return len(self.data['experiments']) - 1

    def get_all_observations(self, cell_type=None, experiment_idx=None):
        """Get all recorded observations, optionally filtered.

        Parameters
        ----------
        cell_type : str, optional
            Filter by cell type
        experiment_idx : int or list, optional
            Filter by experiment index(es)

        Returns
        -------
        list of dict : observations with experiment context
        """
        observations = []
        indices = range(len(self.data['experiments']))
        if experiment_idx is not None:
            if isinstance(experiment_idx, int):
                indices = [experiment_idx]
            else:
                indices = experiment_idx

        for idx in indices:
            if idx >= len(self.data['experiments']):
                continue
            exp = self.data['experiments'][idx]
            for cond in exp['conditions']:
                if cell_type and cond.get('cell_type') != cell_type:
                    continue
                obs = cond.copy()
                obs['experiment_name'] = exp['name']
                obs['experiment_idx'] = idx
                obs['experiment_date'] = exp.get('metadata', {}).get(
                    'date', exp['timestamp'])
                observations.append(obs)

        return observations

    # ================================================================
    # Cell Line Management
    # ================================================================

    def set_cell_line_params(self, cell_type, params):
        """Set or update parameters for a cell line.

        Parameters
        ----------
        cell_type : str
        params : dict
            Any of: mirna_mean, mirna_cv, transfection_efficiency,
                    expression_factor, notes
        """
        if cell_type not in self.data['parameters']['cell_lines']:
            self.data['parameters']['cell_lines'][cell_type] = {}
        self.data['parameters']['cell_lines'][cell_type].update(params)
        self.save()

    def get_cell_profiles(self):
        """Get cell line parameters formatted for the optimizer/simulator.

        Returns
        -------
        dict : {cell_name: {mirna_mean, mirna_cv, transfection_efficiency,
                            expression_factor}}
        """
        profiles = {}
        for name, params in self.data['parameters']['cell_lines'].items():
            profiles[name] = {
                'mirna_mean': params.get('mirna_mean', 0),
                'mirna_cv': params.get('mirna_cv', 0.5),
                'transfection_efficiency': params.get(
                    'transfection_efficiency', 0.5),
                'expression_factor': params.get('expression_factor', 1.0),
            }
        return profiles

    # ================================================================
    # Calibration History
    # ================================================================

    def record_calibration(self, experiment_indices, params_before,
                           params_after, comparison, fit_params, error_before,
                           error_after):
        """Record a calibration round.

        Parameters
        ----------
        experiment_indices : list of int
            Which experiments were used for fitting
        params_before : dict
        params_after : dict
        comparison : list of dict
            Per-condition observed vs predicted
        fit_params : list of str
            Which parameters were fitted
        error_before : float
        error_after : float
        """
        cal = {
            'timestamp': datetime.now().isoformat(),
            'experiment_indices': experiment_indices,
            'n_observations': sum(
                len(self.data['experiments'][i]['conditions'])
                for i in experiment_indices
                if i < len(self.data['experiments'])),
            'fit_params': fit_params,
            'params_before': params_before,
            'params_after': params_after,
            'error_before': error_before,
            'error_after': error_after,
            'error_reduction': (
                (error_before - error_after) / max(error_before, 0.01) * 100),
            'comparison': comparison,
        }

        self.data['calibrations'].append(cal)

        # Update current parameters
        for param, value in params_after.items():
            if param in ('mirna_mean', 'mirna_cv', 'transfection_efficiency',
                         'expression_factor'):
                # These are cell-line-specific; update the ON cell
                # (caller should specify which cell line)
                pass
            elif param in self.data['parameters']['universal']:
                self.data['parameters']['universal'][param] = value

        self.save()
        return len(self.data['calibrations']) - 1

    def get_parameter_history(self, param_name):
        """Track how a parameter evolved across calibration rounds.

        Returns
        -------
        list of (timestamp, before_value, after_value)
        """
        history = []
        for cal in self.data['calibrations']:
            if param_name in cal.get('params_after', {}):
                history.append({
                    'timestamp': cal['timestamp'],
                    'before': cal['params_before'].get(param_name),
                    'after': cal['params_after'].get(param_name),
                    'n_observations': cal['n_observations'],
                    'error_after': cal['error_after'],
                })
        return history

    # ================================================================
    # Summary and Reporting
    # ================================================================

    def summary(self):
        """Return a text summary of the database contents."""
        lines = []
        lines.append(f'Experiment History Database')
        lines.append(f'  Location: {self.db_path}')
        lines.append(f'  Created: {self.data.get("created", "unknown")}')
        lines.append(f'  Last modified: {self.data.get("last_modified", "never")}')
        lines.append(f'')
        lines.append(f'  Experiments: {len(self.data["experiments"])}')

        total_obs = sum(len(e['conditions'])
                        for e in self.data['experiments'])
        lines.append(f'  Total observations: {total_obs}')
        lines.append(f'  Calibration rounds: {len(self.data["calibrations"])}')
        lines.append(f'')

        cell_lines = list(self.data['parameters']['cell_lines'].keys())
        lines.append(f'  Cell lines: {", ".join(cell_lines) if cell_lines else "none"}')

        for name, params in self.data['parameters']['cell_lines'].items():
            mirna = params.get('mirna_mean', 0)
            te = params.get('transfection_efficiency', 0)
            lines.append(f'    {name}: miRNA={mirna:,.0f}, TE={te:.0%}, '
                          f'expr={params.get("expression_factor", 1):.1f}x')

        if self.data['experiments']:
            lines.append(f'')
            lines.append(f'  Experiment log:')
            for i, exp in enumerate(self.data['experiments']):
                lines.append(f'    [{i}] {exp["name"]} '
                              f'({exp["n_conditions"]} conditions)')

        if self.data['calibrations']:
            lines.append(f'')
            lines.append(f'  Calibration log:')
            for i, cal in enumerate(self.data['calibrations']):
                lines.append(
                    f'    [{i}] {cal["timestamp"][:10]}: '
                    f'error {cal["error_before"]:.1f} -> '
                    f'{cal["error_after"]:.1f} '
                    f'({cal["error_reduction"]:.0f}% reduction, '
                    f'{cal["n_observations"]} obs)')

        return '\n'.join(lines)

    def export_observations_csv(self, filepath):
        """Export all observations as CSV for external analysis."""
        import csv
        obs = self.get_all_observations()
        if not obs:
            return

        fields = ['experiment_name', 'experiment_date', 'cell_type',
                  'sensor_ng', 'payload_ng', 'observed_pct']
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields,
                                     extrasaction='ignore')
            writer.writeheader()
            writer.writerows(obs)
