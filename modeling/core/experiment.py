"""
Experiment design and model calibration module.

Two-phase workflow:
  1. DESIGN: Generate a validation experiment with plate layout,
     controls, predictions, and pass/fail criteria.
  2. CALIBRATE: Ingest experimental results and refine model parameters
     using least-squares fitting. Outputs updated parameters and a
     report comparing old vs new predictions.

The design phase outputs a structured experiment plan including:
  - Plate map with well assignments
  - Required mRNA amounts per well
  - Model predictions for each condition (with confidence intervals)
  - Essential controls and what they constrain
  - Specific quantitative predictions to test

The calibration phase accepts:
  - CSV of flow cytometry results (% sfGFP+ per condition)
  - Updates model parameters to minimize prediction error
  - Reports which parameters shifted and by how much
  - Generates improved predictions for the next experiment
"""

import numpy as np
from scipy.optimize import minimize
from .optimizer import CircuitOptimizer
from .parameters import get_params
import json
import os


class ExperimentDesigner:
    """Design validation experiments and generate predictions."""

    def __init__(self, params=None):
        self.params = params or get_params()
        self.optimizer = CircuitOptimizer(self.params)

    def design_titration(self, cell_profiles, payload_ng=150,
                          sensor_ng_list=None, total_cells_per_well=30000,
                          replicates=3, plate_format=96):
        """Design a sensor titration experiment.

        Parameters
        ----------
        cell_profiles : dict
            {cell_name: {mirna_mean, mirna_cv, transfection_efficiency,
                         expression_factor}}
        payload_ng : float
            Fixed payload mRNA per well (ng)
        sensor_ng_list : list of float, optional
            Sensor amounts to test. Default: [0, 10, 25, 50, 75, 100, 150]
        total_cells_per_well : int
        replicates : int
        plate_format : int (96 or 384)

        Returns
        -------
        dict with experiment plan, plate map, and predictions
        """
        if sensor_ng_list is None:
            sensor_ng_list = [0, 10, 25, 50, 75, 100, 150]

        copies_per_ng = total_cells_per_well / 30000 * 20  # Scale with cell count

        cell_names = sorted(cell_profiles.keys())
        n_conditions = len(sensor_ng_list) * len(cell_names)
        n_controls = len(cell_names) * 4  # neg, payload-only, sensor-only, pos
        n_wells = (n_conditions + n_controls) * replicates

        # Generate predictions for each condition
        conditions = []
        for sensor_ng in sensor_ng_list:
            sensor_c = int(sensor_ng * copies_per_ng)
            payload_c = int(payload_ng * copies_per_ng)

            pop_results, thresh = self.optimizer._simulate_population(
                sensor_c, payload_c, cell_profiles,
                n_cells=20000, seed=42)

            for cell_name in cell_names:
                sp_ratio = sensor_ng / payload_ng if payload_ng > 0 else 0
                conditions.append({
                    'cell_type': cell_name,
                    'sensor_ng': sensor_ng,
                    'payload_ng': payload_ng,
                    'sp_ratio': sp_ratio,
                    'predicted_pct': pop_results[cell_name]['percent_positive'],
                    'predicted_free': pop_results[cell_name]['percent_free'],
                    'condition_label': (f'{cell_name} '
                                       f'p069B={sensor_ng}ng + '
                                       f'p065={payload_ng}ng'),
                })

        # Generate controls
        controls = []
        for cell_name in cell_names:
            # Negative (mock transfection)
            controls.append({
                'cell_type': cell_name,
                'label': f'{cell_name} Mock Transfection',
                'sensor_ng': 0, 'payload_ng': 0,
                'purpose': 'Set sfGFP gate; autofluorescence baseline',
                'expected': '0% sfGFP+',
            })
            # Payload only (no sensor)
            pop_free, _ = self.optimizer._simulate_population(
                0, int(payload_ng * copies_per_ng), cell_profiles,
                n_cells=20000, seed=42)
            controls.append({
                'cell_type': cell_name,
                'label': f'{cell_name} Payload Only ({payload_ng}ng p065)',
                'sensor_ng': 0, 'payload_ng': payload_ng,
                'purpose': 'Baseline transfection; constrains TE and expression',
                'expected': f'{pop_free[cell_name]["percent_free"]:.1f}% sfGFP+',
            })
            # Sensor only
            controls.append({
                'cell_type': cell_name,
                'label': f'{cell_name} Sensor Only (100ng p069B)',
                'sensor_ng': 100, 'payload_ng': 0,
                'purpose': 'Verify sensor produces no sfGFP',
                'expected': '~0% sfGFP+',
            })
            # No transfection
            controls.append({
                'cell_type': cell_name,
                'label': f'{cell_name} No Transfection',
                'sensor_ng': 0, 'payload_ng': 0,
                'purpose': 'Cell viability; autofluorescence',
                'expected': '~0% sfGFP+',
            })

        # Plate layout
        rows = 'ABCDEFGH'
        cols = list(range(1, 13)) if plate_format == 96 else list(range(1, 25))
        plate_map = []
        well_idx = 0

        for cond in controls:
            for rep in range(replicates):
                if well_idx < len(rows) * len(cols):
                    row = rows[well_idx // len(cols)]
                    col = cols[well_idx % len(cols)]
                    plate_map.append({
                        'well': f'{row}{col}',
                        'condition': cond['label'],
                        'replicate': rep + 1,
                        'type': 'control',
                    })
                    well_idx += 1

        for cond in conditions:
            for rep in range(replicates):
                if well_idx < len(rows) * len(cols):
                    row = rows[well_idx // len(cols)]
                    col = cols[well_idx % len(cols)]
                    plate_map.append({
                        'well': f'{row}{col}',
                        'condition': cond['condition_label'],
                        'replicate': rep + 1,
                        'type': 'experimental',
                    })
                    well_idx += 1

        # Key predictions to test
        predictions = []
        for cond in conditions:
            if cond['sensor_ng'] > 0:
                predictions.append({
                    'condition': cond['condition_label'],
                    'metric': 'Live sfGFP+ %',
                    'predicted': cond['predicted_pct'],
                    'tolerance': max(cond['predicted_pct'] * 0.3, 2.0),
                })

        return {
            'conditions': conditions,
            'controls': controls,
            'plate_map': plate_map,
            'predictions': predictions,
            'n_wells': n_wells,
            'replicates': replicates,
            'cell_profiles': cell_profiles,
            'payload_ng': payload_ng,
            'sensor_ng_list': sensor_ng_list,
        }

    def format_experiment_plan(self, design):
        """Format experiment design as readable text."""
        lines = []
        lines.append('=' * 75)
        lines.append('VALIDATION EXPERIMENT PLAN')
        lines.append('=' * 75)
        lines.append('')

        # Materials
        lines.append('MATERIALS')
        lines.append('-' * 40)
        lines.append(f'  Payload mRNA (p065, 2xKt-sfGFP): {design["payload_ng"]}ng/well')
        sensor_amounts = sorted(set(design['sensor_ng_list']))
        lines.append(f'  Sensor mRNA (p069B, 5\'MRE-L7Ae): {sensor_amounts} ng/well')
        cell_types = sorted(design['cell_profiles'].keys())
        lines.append(f'  Cell lines: {", ".join(cell_types)}')
        lines.append(f'  Replicates: n={design["replicates"]}')
        lines.append(f'  Total wells: {design["n_wells"]}')
        lines.append('')

        # Controls
        lines.append('CONTROLS')
        lines.append('-' * 40)
        for ctrl in design['controls']:
            lines.append(f'  {ctrl["label"]}')
            lines.append(f'    Purpose: {ctrl["purpose"]}')
            lines.append(f'    Expected: {ctrl["expected"]}')
        lines.append('')

        # Experimental conditions with predictions
        lines.append('EXPERIMENTAL CONDITIONS AND PREDICTIONS')
        lines.append('-' * 75)
        lines.append(f'{"Condition":<45s} {"Predicted":>10s} {"Range":>15s}')
        lines.append('-' * 75)

        for cond in design['conditions']:
            if cond['sensor_ng'] > 0:
                pred = cond['predicted_pct']
                tol = max(pred * 0.3, 2.0)
                lo = max(pred - tol, 0)
                hi = min(pred + tol, 100)
                lines.append(
                    f'{cond["condition_label"]:<45s} {pred:9.1f}% '
                    f'{lo:6.1f}-{hi:.1f}%')

        lines.append('')

        # Key testable predictions
        lines.append('KEY TESTABLE PREDICTIONS')
        lines.append('-' * 75)
        lines.append('')

        # Find conditions to compare
        for cell in cell_types:
            cell_conds = [c for c in design['conditions']
                          if c['cell_type'] == cell and c['sensor_ng'] > 0]
            if len(cell_conds) >= 2:
                low_s = min(cell_conds, key=lambda c: c['sensor_ng'])
                high_s = max(cell_conds, key=lambda c: c['sensor_ng'])
                lines.append(
                    f'  {cell}: reducing sensor from {high_s["sensor_ng"]}ng '
                    f'to {low_s["sensor_ng"]}ng should {"increase" if cell == max(cell_types, key=lambda c: design["cell_profiles"][c].get("mirna_mean", 0)) else "not change"} '
                    f'sfGFP+ %')
                lines.append(
                    f'    ({high_s["predicted_pct"]:.1f}% -> '
                    f'{low_s["predicted_pct"]:.1f}%)')

        lines.append('')
        lines.append('  If model is correct:')
        lines.append('  - Payload-only control should match free payload baseline')
        lines.append('  - Sensor-only control should show 0% sfGFP+')
        lines.append('  - Low sensor doses should show HIGHER HuH7 sfGFP+ than 1:1')
        lines.append('  - 4T1 should remain ~1-2% across all sensor doses')

        return '\n'.join(lines)


class ModelCalibrator:
    """Calibrate model parameters from experimental results."""

    # Parameters that can be fitted and their bounds
    FITTABLE_PARAMS = {
        'mirna_mean': (1000, 200000, 'miR-122 functional copies in ON cell'),
        'mirna_cv': (0.1, 3.0, 'miR-122 cell-to-cell CV'),
        'circuit_failure_rate': (0.001, 0.20, 'Stochastic circuit failure rate'),
        'expression_ratio': (1.0, 20.0, 'ON/OFF cell expression ratio'),
        'L7Ae_repression_fold': (10, 10000, 'L7Ae translational repression fold'),
    }

    def __init__(self, params=None):
        self.params = params or get_params()
        self.fit_history = []

    def calibrate(self, experimental_data, cell_profiles,
                  fit_params=None, copies_per_ng=20):
        """Fit model parameters to experimental flow cytometry data.

        Parameters
        ----------
        experimental_data : list of dict
            Each entry: {
                'cell_type': str,
                'sensor_ng': float,
                'payload_ng': float,
                'observed_pct': float,  # Live sfGFP+ %
                'weight': float (optional, default 1.0)
            }
        cell_profiles : dict
            Cell type definitions (template; mirna_mean etc will be fitted)
        fit_params : list of str, optional
            Which parameters to fit. Default: ['mirna_mean', 'mirna_cv']
        copies_per_ng : float

        Returns
        -------
        dict with fitted parameters, residuals, and comparison
        """
        if fit_params is None:
            fit_params = ['mirna_mean', 'mirna_cv']

        # Current parameter values as starting point
        current = {
            'mirna_mean': cell_profiles[max(cell_profiles.keys(),
                key=lambda c: cell_profiles[c].get('mirna_mean', 0))].get('mirna_mean', 8000),
            'mirna_cv': cell_profiles[max(cell_profiles.keys(),
                key=lambda c: cell_profiles[c].get('mirna_mean', 0))].get('mirna_cv', 0.5),
            'circuit_failure_rate': self.params.get('circuit_failure_rate', 0.044),
            'expression_ratio': self.params.get('expression_ratio_HuH7', 5.5),
            'L7Ae_repression_fold': self.params.get('L7Ae_repression_fold', 1000),
        }

        # Extract initial values and bounds for fitted params
        x0 = []
        bounds = []
        for param in fit_params:
            info = self.FITTABLE_PARAMS[param]
            x0.append(current[param])
            bounds.append((info[0], info[1]))

        # ON cell name
        on_cell = max(cell_profiles.keys(),
                      key=lambda c: cell_profiles[c].get('mirna_mean', 0))

        def objective(x):
            """Compute sum of squared residuals."""
            # Update parameters
            trial = current.copy()
            for i, param in enumerate(fit_params):
                trial[param] = x[i]

            # Build modified cell profiles
            mod_profiles = {}
            for name, prof in cell_profiles.items():
                mod_profiles[name] = prof.copy()
                if name == on_cell:
                    mod_profiles[name]['mirna_mean'] = trial['mirna_mean']
                    mod_profiles[name]['mirna_cv'] = trial['mirna_cv']
                    mod_profiles[name]['expression_factor'] = trial['expression_ratio']

            # Build optimizer with modified params
            p = get_params(
                L7Ae_repression_fold=trial['L7Ae_repression_fold'],
                circuit_failure_rate=trial['circuit_failure_rate'],
                expression_ratio_HuH7=trial['expression_ratio'],
                t_max_hr=24,
            )
            opt = CircuitOptimizer(p)
            opt.base_failure_rate = trial['circuit_failure_rate']
            opt.expression_ratio = trial['expression_ratio']

            # Compute predictions
            total_err = 0
            for obs in experimental_data:
                sensor_c = int(obs['sensor_ng'] * copies_per_ng)
                payload_c = int(obs['payload_ng'] * copies_per_ng)
                weight = obs.get('weight', 1.0)

                try:
                    pop, thresh = opt._simulate_population(
                        sensor_c, payload_c, mod_profiles,
                        n_cells=10000, seed=42)
                    predicted = pop[obs['cell_type']]['percent_positive']
                except Exception:
                    predicted = 0

                residual = predicted - obs['observed_pct']
                total_err += weight * residual**2

            return total_err

        # Use Nelder-Mead (gradient-free) since population model is stochastic
        # Scale parameters to similar magnitudes for optimizer
        scales = np.array([b[1] - b[0] for b in bounds])
        x0_scaled = [(x - b[0]) / s for x, b, s in zip(x0, bounds, scales)]

        def objective_scaled(x_s):
            x_real = [x_s[i] * scales[i] + bounds[i][0] for i in range(len(x_s))]
            # Clip to bounds
            x_real = [max(bounds[i][0], min(bounds[i][1], x_real[i]))
                       for i in range(len(x_real))]
            return objective(x_real)

        result_scaled = minimize(objective_scaled, x0_scaled,
                                  method='Nelder-Mead',
                                  options={'maxiter': 200, 'xatol': 0.01,
                                           'fatol': 1.0, 'adaptive': True})

        # Convert back to real scale
        class Result:
            pass
        result = Result()
        result.x = np.array([result_scaled.x[i] * scales[i] + bounds[i][0]
                              for i in range(len(bounds))])
        # Clip to bounds
        result.x = np.array([max(bounds[i][0], min(bounds[i][1], result.x[i]))
                              for i in range(len(bounds))])
        result.success = result_scaled.success
        result.fun = result_scaled.fun
        result.nit = result_scaled.nit

        # Extract fitted values
        fitted = current.copy()
        for i, param in enumerate(fit_params):
            fitted[param] = result.x[i]

        # Compute final predictions with fitted parameters
        mod_profiles = {}
        for name, prof in cell_profiles.items():
            mod_profiles[name] = prof.copy()
            if name == on_cell:
                mod_profiles[name]['mirna_mean'] = fitted['mirna_mean']
                mod_profiles[name]['mirna_cv'] = fitted['mirna_cv']
                mod_profiles[name]['expression_factor'] = fitted['expression_ratio']

        p_fitted = get_params(
            L7Ae_repression_fold=fitted['L7Ae_repression_fold'],
            circuit_failure_rate=fitted['circuit_failure_rate'],
            expression_ratio_HuH7=fitted['expression_ratio'],
            t_max_hr=24,
        )
        opt_fitted = CircuitOptimizer(p_fitted)
        opt_fitted.base_failure_rate = fitted['circuit_failure_rate']
        opt_fitted.expression_ratio = fitted['expression_ratio']

        comparison = []
        for obs in experimental_data:
            sensor_c = int(obs['sensor_ng'] * copies_per_ng)
            payload_c = int(obs['payload_ng'] * copies_per_ng)

            try:
                pop, thresh = opt_fitted._simulate_population(
                    sensor_c, payload_c, mod_profiles,
                    n_cells=15000, seed=42)
                predicted = pop[obs['cell_type']]['percent_positive']
            except Exception:
                predicted = 0

            comparison.append({
                'condition': (f'{obs["cell_type"]} '
                              f'S={obs["sensor_ng"]}ng P={obs["payload_ng"]}ng'),
                'observed': obs['observed_pct'],
                'predicted_before': obs.get('predicted_before', None),
                'predicted_after': predicted,
                'residual': predicted - obs['observed_pct'],
            })

        # Record in history
        self.fit_history.append({
            'fitted_params': fitted,
            'initial_params': current,
            'fit_params': fit_params,
            'comparison': comparison,
            'optimizer_result': {
                'success': result.success,
                'fun': result.fun,
                'nit': result.nit,
            },
        })

        return {
            'fitted_params': fitted,
            'initial_params': current,
            'changed_params': {p: (current[p], fitted[p]) for p in fit_params},
            'comparison': comparison,
            'fit_success': result.success,
            'total_error_before': sum(
                (c['observed'] - (c['predicted_before'] or c['observed']))**2
                for c in comparison),
            'total_error_after': result.fun,
        }

    def format_calibration_report(self, cal_result):
        """Format calibration results as readable text."""
        lines = []
        lines.append('=' * 75)
        lines.append('MODEL CALIBRATION REPORT')
        lines.append('=' * 75)
        lines.append('')

        lines.append('PARAMETER CHANGES')
        lines.append('-' * 50)
        for param, (old, new) in cal_result['changed_params'].items():
            desc = self.FITTABLE_PARAMS[param][2]
            pct_change = (new - old) / old * 100 if old != 0 else 0
            lines.append(f'  {desc}:')
            lines.append(f'    Before: {old:.4g}  ->  After: {new:.4g}'
                          f'  ({pct_change:+.1f}%)')
        lines.append('')

        lines.append('PREDICTION vs OBSERVATION')
        lines.append('-' * 75)
        lines.append(f'{"Condition":<40s} {"Observed":>9s} {"Before":>9s} '
                      f'{"After":>9s} {"Resid":>7s}')
        lines.append('-' * 75)

        for c in cal_result['comparison']:
            before = f'{c["predicted_before"]:.1f}%' if c['predicted_before'] is not None else 'N/A'
            lines.append(
                f'{c["condition"]:<40s} {c["observed"]:8.1f}% '
                f'{before:>9s} {c["predicted_after"]:8.1f}% '
                f'{c["residual"]:+6.1f}%')

        lines.append('')
        lines.append(f'Total squared error: '
                      f'{cal_result["total_error_before"]:.1f} -> '
                      f'{cal_result["total_error_after"]:.1f}')

        return '\n'.join(lines)

    def save_params(self, fitted_params, filepath):
        """Save fitted parameters to JSON for future sessions."""
        with open(filepath, 'w') as f:
            json.dump(fitted_params, f, indent=2)

    def load_params(self, filepath):
        """Load previously fitted parameters from JSON."""
        with open(filepath, 'r') as f:
            return json.load(f)
