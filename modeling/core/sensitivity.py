"""
Parameter sensitivity analysis for the RNA logic gate circuit model.

Performs one-at-a-time (OAT) sensitivity analysis by varying each parameter
+/- 50% from its baseline while holding all others constant, then computing
a normalized sensitivity index for key circuit outputs.
"""

import numpy as np
from .and_gate import ANDGateModel
from .parameters import get_params


# Default outputs to track from each simulation
_OUTPUT_KEYS = ('peak_sfgfp', 'circuit_efficiency', 'on_off_ratio')


def _circuit_efficiency(on_result, off_result):
    """Fraction of payload expressed in ON state relative to unrepressed level.

    Efficiency = peak_sfGFP(ON) / (payload_copies * theoretical_max).
    Approximated here as the ratio of ON-state peak sfGFP to payload copies
    delivered, normalized so a perfectly translated payload gives 1.0.
    """
    payload = on_result['payload_copies']
    if payload <= 0:
        return 0.0
    # Normalize to payload copies (rough proxy; exact max depends on kinetics)
    return on_result['peak_sfgfp'] / payload


def _on_off_ratio(on_result, off_result):
    """ON:OFF selectivity ratio based on peak sfGFP."""
    off_peak = off_result['peak_sfgfp']
    if off_peak < 1e-10:
        return float('inf')
    return on_result['peak_sfgfp'] / off_peak


class SensitivityAnalyzer:
    """One-at-a-time parameter sensitivity analysis for the AND gate circuit.

    Parameters
    ----------
    L7Ae_repression_fold : float
        Translational repression fold for L7Ae-bound payload (default 1000).
    t_max_hr : float
        Simulation duration in hours (default 24).
    """

    def __init__(self, L7Ae_repression_fold=1000, t_max_hr=24):
        self.L7Ae_repression_fold = L7Ae_repression_fold
        self.t_max_hr = t_max_hr

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def one_at_a_time(self, base_params, param_ranges, mirna_on, mirna_off,
                      sensor, payload):
        """Run one-at-a-time sensitivity analysis.

        Each parameter in *param_ranges* is varied while all others are held
        at their baseline values.  For every variation the AND gate is
        simulated in both the ON (high miRNA) and OFF (low miRNA) states so
        that selectivity metrics can be computed.

        Parameters
        ----------
        base_params : dict
            Baseline parameter dictionary (e.g. from ``get_params()``).  The
            analyzer will override ``L7Ae_repression_fold`` and ``t_max_hr``
            with instance defaults unless they are already present in
            *param_ranges*.
        param_ranges : dict
            ``{param_name: [low, baseline, high]}`` specifying the values to
            test.  If only a parameter name is given (value is ``None``), the
            analyzer auto-generates low/high as baseline +/- 50%.
        mirna_on : float
            miRNA copies per cell for the ON state (e.g. HuH7 miR-122).
        mirna_off : float
            miRNA copies per cell for the OFF state (e.g. 4T1, typically 0).
        sensor : float
            Sensor mRNA copies delivered per cell.
        payload : float
            Payload mRNA copies delivered per cell.

        Returns
        -------
        dict
            Keyed by parameter name.  Each value is a dict with:
            - ``values``: list of tested parameter values [low, base, high]
            - ``outputs``: dict of output name -> list of output values
            - ``sensitivity``: dict of output name -> sensitivity index
              (mean of |% change output / % change input| for low and high)
        """
        # Ensure instance defaults are applied to the base params
        bp = base_params.copy()
        bp.setdefault('L7Ae_repression_fold', self.L7Ae_repression_fold)
        bp.setdefault('t_max_hr', self.t_max_hr)

        # Resolve param_ranges: fill in auto ranges where needed
        resolved = {}
        for pname, vals in param_ranges.items():
            if vals is None:
                baseline_val = bp.get(pname)
                if baseline_val is None:
                    raise KeyError(
                        f"Parameter '{pname}' not found in base_params"
                    )
                resolved[pname] = [
                    baseline_val * 0.5,
                    baseline_val,
                    baseline_val * 1.5,
                ]
            else:
                resolved[pname] = list(vals)

        # Compute baseline outputs once
        baseline_on, baseline_off = self._run_pair(bp, mirna_on, mirna_off,
                                                   sensor, payload)
        baseline_outputs = self._extract_outputs(baseline_on, baseline_off)

        results = {}
        for pname, values in resolved.items():
            param_outputs = {k: [] for k in _OUTPUT_KEYS}

            for val in values:
                p = bp.copy()
                # Handle non-parameter inputs that live outside the params dict
                s_copies = sensor
                p_copies = payload
                m_on = mirna_on
                m_off = mirna_off

                if pname == 'sensor_copies':
                    s_copies = val
                elif pname == 'payload_copies':
                    p_copies = val
                elif pname == 'mirna_on_copies':
                    m_on = val
                else:
                    p[pname] = val
                    # Recompute derived rates if a half-life was changed
                    p = get_params(**{k: v for k, v in p.items()})

                on_res, off_res = self._run_pair(p, m_on, m_off,
                                                 s_copies, p_copies)
                outs = self._extract_outputs(on_res, off_res)
                for k in _OUTPUT_KEYS:
                    param_outputs[k].append(outs[k])

            # Compute sensitivity indices
            sensitivity = {}
            base_idx = 1  # middle element is baseline
            base_val = values[base_idx]
            for k in _OUTPUT_KEYS:
                si_values = []
                for i in [0, 2]:  # low and high perturbations
                    delta_input = (values[i] - base_val)
                    if abs(base_val) < 1e-30:
                        continue
                    frac_input = delta_input / base_val

                    base_output = baseline_outputs[k]
                    delta_output = param_outputs[k][i] - base_output
                    if abs(base_output) < 1e-30:
                        # Use absolute change when baseline is near zero
                        si_values.append(abs(delta_output))
                        continue
                    frac_output = delta_output / base_output

                    if abs(frac_input) < 1e-30:
                        continue
                    si_values.append(abs(frac_output / frac_input))

                sensitivity[k] = (
                    float(np.mean(si_values)) if si_values else 0.0
                )

            results[pname] = {
                'values': values,
                'outputs': param_outputs,
                'sensitivity': sensitivity,
            }

        return results

    def format_report(self, results):
        """Format sensitivity analysis results as a readable text table.

        Parameters
        ----------
        results : dict
            Output from :meth:`one_at_a_time`.

        Returns
        -------
        str
            Multi-line string with a formatted table showing sensitivity
            indices for each parameter and output metric.
        """
        # Header
        col_param = 'Parameter'
        col_heads = ['peak_sfgfp', 'circuit_eff', 'ON:OFF ratio']
        col_w = 16
        param_w = max(len(col_param), max(len(p) for p in results) + 1)

        header = f"{'Parameter':<{param_w}}  "
        header += '  '.join(f'{h:>{col_w}}' for h in col_heads)
        sep = '-' * len(header)

        lines = [
            'Sensitivity Analysis (OAT, +/- 50%)',
            '=' * 38,
            '',
            'Sensitivity Index = |% change output / % change input|',
            'Values > 1.0 indicate amplified sensitivity.',
            '',
            header,
            sep,
        ]

        # Sort by max sensitivity across outputs (most sensitive first)
        sorted_params = sorted(
            results.keys(),
            key=lambda p: max(results[p]['sensitivity'].values()),
            reverse=True,
        )

        for pname in sorted_params:
            entry = results[pname]
            sens = entry['sensitivity']
            vals_str = [
                f'{sens.get("peak_sfgfp", 0.0):>{col_w}.4f}',
                f'{sens.get("circuit_efficiency", 0.0):>{col_w}.4f}',
                f'{sens.get("on_off_ratio", 0.0):>{col_w}.4f}',
            ]
            lines.append(f'{pname:<{param_w}}  ' + '  '.join(vals_str))

        lines.append(sep)
        lines.append('')

        # Append baseline and perturbed values for reference
        lines.append('Parameter sweep values and outputs:')
        lines.append('')
        for pname in sorted_params:
            entry = results[pname]
            vals = entry['values']
            lines.append(f'  {pname}:')
            lines.append(f'    values tested: {vals}')
            for out_key in _OUTPUT_KEYS:
                out_vals = entry['outputs'][out_key]
                formatted = [f'{v:.4g}' for v in out_vals]
                lines.append(f'    {out_key}: {formatted}')
            lines.append('')

        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _run_pair(self, params, mirna_on, mirna_off, sensor, payload):
        """Simulate the AND gate in both ON and OFF miRNA conditions."""
        model = ANDGateModel(params=params)
        on_result = model.simulate(mirna_on, sensor, payload, params=params)
        off_result = model.simulate(mirna_off, sensor, payload, params=params)
        return on_result, off_result

    def _extract_outputs(self, on_result, off_result):
        """Compute the three tracked output metrics from a simulation pair."""
        return {
            'peak_sfgfp': on_result['peak_sfgfp'],
            'circuit_efficiency': _circuit_efficiency(on_result, off_result),
            'on_off_ratio': _on_off_ratio(on_result, off_result),
        }
