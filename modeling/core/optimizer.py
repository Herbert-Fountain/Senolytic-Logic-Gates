"""
Circuit dosing optimizer for RNA logic gate circuits.

Given a circuit architecture, cell-type profiles, and experimental constraints,
finds the optimal mRNA component ratios to maximize selectivity, ON-cell
activation, or a custom objective.

Supports:
  - Sensor:payload ratio optimization (fixed total mRNA)
  - Independent dose optimization (variable total mRNA)
  - Multi-objective optimization (selectivity vs activation tradeoff)
  - Dose robustness analysis (performance across dose range)

Calibrated against miR-122 ON switch flow cytometry data (3/31/2026).
"""

import numpy as np
from .and_gate import ANDGateModel
from .parameters import get_params


class CircuitOptimizer:
    """Optimize mRNA component ratios for RNA logic gate circuits."""

    def __init__(self, params=None):
        self.params = params or get_params()
        self.model = ANDGateModel(self.params)

        # Derived constants
        p = self.params
        k_tr = p['k_translate']
        g_m = p['gamma_mRNA']
        g_g = p['gamma_GFP']
        if abs(g_m - g_g) > 1e-10:
            t_peak = np.log(g_m / g_g) / (g_m - g_g)
        else:
            t_peak = 1.0 / g_m
        self.sfgfp_per_copy = k_tr / (g_g - g_m) * (
            np.exp(-g_m * t_peak) - np.exp(-g_g * t_peak))

        # Calibrated population parameters
        self.base_failure_rate = p.get('circuit_failure_rate', 0.044)
        self.ref_copies = 2000  # Reference dose for failure rate scaling
        self.expression_ratio = p.get('expression_ratio_HuH7', 5.5)
        self.delivery_cv = p.get('delivery_cv', 0.5)

    def _build_efficiency_lookup(self, sensor_copies, payload_copies,
                                  mirna_grid=None):
        """Build miR-122 -> circuit efficiency lookup for a specific ratio."""
        p = self.params
        if mirna_grid is None:
            mirna_grid = np.concatenate([[0], np.logspace(2, 5, 40)])

        t_max = p.get('t_max_hr', 24)
        eff = np.zeros(len(mirna_grid))
        free_sfgfp = payload_copies * self.sfgfp_per_copy

        for i, m in enumerate(mirna_grid):
            if sensor_copies > 0:
                r = self.model.simulate(m, sensor_copies, payload_copies, p)
                eff[i] = r['trajectories']['sfGFP'][-1] / max(free_sfgfp, 1)
            else:
                eff[i] = 1.0
        return mirna_grid, eff

    def _simulate_population(self, sensor_copies, payload_copies,
                              cell_profiles, n_cells=20000, seed=42):
        """Run population simulation for given component amounts.

        Parameters
        ----------
        sensor_copies : float
            Mean sensor mRNA copies per transfected cell
        payload_copies : float
            Mean payload mRNA copies per transfected cell
        cell_profiles : dict
            {cell_name: {
                'mirna_mean': float,
                'mirna_cv': float,
                'transfection_efficiency': float,
                'expression_factor': float (relative to reference cell type),
            }}
        n_cells : int
        seed : int

        Returns
        -------
        dict with per-cell-type % positive and metrics
        """
        p = self.params
        mirna_grid, eff_lookup = self._build_efficiency_lookup(
            sensor_copies, payload_copies)

        rng = np.random.default_rng(seed)
        n = n_cells
        sigma_d = np.sqrt(np.log(1 + self.delivery_cv**2))

        # Payload delivery distribution
        mu_p = np.log(max(payload_copies, 1)) - sigma_d**2 / 2
        payload_del = rng.lognormal(mu_p, sigma_d, n)
        sfgfp_free = payload_del * self.sfgfp_per_copy

        # Fixed threshold (calibrated from reference condition)
        mu_ref = np.log(self.ref_copies) - sigma_d**2 / 2
        del_ref = rng.lognormal(mu_ref, sigma_d, n)
        # Reference: 4T1 at 2000 copies, TE=0.31, 29.87% positive
        mask_ref = rng.random(n) < 0.31
        free_ref = np.zeros(n)
        free_ref[mask_ref] = del_ref[mask_ref] * self.sfgfp_per_copy
        thresh = np.sort(free_ref)[::-1][int(0.2987 * n)]

        # Dose-dependent failure rate
        avg_copies = max((sensor_copies + payload_copies) / 2, 10)
        failure_rate = self.base_failure_rate * np.sqrt(
            self.ref_copies / avg_copies)

        results = {}
        for cell_name, profile in cell_profiles.items():
            te = profile.get('transfection_efficiency', 0.85)
            expr_factor = profile.get('expression_factor', 1.0)
            mirna_mean = profile.get('mirna_mean', 0)
            mirna_cv = profile.get('mirna_cv', 0.5)

            mask = rng.random(n) < te

            # miRNA distribution
            if mirna_mean > 0:
                sigma_m = np.sqrt(np.log(1 + mirna_cv**2))
                mu_m = np.log(mirna_mean) - sigma_m**2 / 2
                mirna_cells = rng.lognormal(mu_m, sigma_m, np.sum(mask))
            else:
                mirna_cells = np.zeros(np.sum(mask))

            # Circuit efficiency per cell
            eff_cells = np.interp(mirna_cells, mirna_grid, eff_lookup)

            # Circuit sfGFP
            sfgfp_circuit = (payload_del[mask] * eff_cells *
                             expr_factor * self.sfgfp_per_copy)

            # Circuit failures (full expression)
            fails = rng.random(np.sum(mask)) < failure_rate
            sfgfp_fail = (payload_del[mask] * self.sfgfp_per_copy *
                          expr_factor)
            sfgfp_combined = np.where(fails, sfgfp_fail, sfgfp_circuit)

            out = np.zeros(n)
            out[mask] = sfgfp_combined
            pct = np.mean(out > thresh) * 100

            # Free payload
            out_free = np.zeros(n)
            out_free[mask] = sfgfp_free[mask] * expr_factor
            pct_free = np.mean(out_free > thresh) * 100

            results[cell_name] = {
                'percent_positive': pct,
                'percent_free': pct_free,
                'n_positive': int(pct / 100 * n),
            }

        return results, thresh

    def optimize_ratio(self, total_mRNA_ng, cell_profiles,
                       copies_per_ng=20, objective='selectivity',
                       sp_ratios=None, n_cells=20000, seed=42):
        """Find optimal sensor:payload ratio for a given total mRNA dose.

        Parameters
        ----------
        total_mRNA_ng : float
            Total mRNA per well (ng). Split between sensor and payload.
        cell_profiles : dict
            Cell type definitions (see _simulate_population)
        copies_per_ng : float
            mRNA copies delivered per ng per cell (default: 20 at 30K cells/well)
        objective : str
            'selectivity': maximize ON:OFF ratio
            'activation': maximize ON-cell % positive
            'balanced': maximize ON% * log(ratio)
        sp_ratios : array-like, optional
            Custom S:P ratios to test. Default: logarithmic sweep.
        n_cells : int
        seed : int

        Returns
        -------
        dict with optimization results and recommendations
        """
        total_copies = total_mRNA_ng * copies_per_ng

        if sp_ratios is None:
            sp_ratios = [0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5,
                         0.7, 1.0, 1.5, 2.0, 3.0, 5.0]

        # Identify ON and OFF cell types
        cell_names = list(cell_profiles.keys())
        on_cell = max(cell_names,
                      key=lambda c: cell_profiles[c].get('mirna_mean', 0))
        off_cell = min(cell_names,
                       key=lambda c: cell_profiles[c].get('mirna_mean', 0))

        sweep_results = []
        for sp in sp_ratios:
            sensor_c = int(total_copies * sp / (1 + sp))
            payload_c = total_copies - sensor_c
            sensor_ng = sensor_c / copies_per_ng
            payload_ng = payload_c / copies_per_ng

            pop_results, thresh = self._simulate_population(
                sensor_c, payload_c, cell_profiles, n_cells, seed)

            on_pct = pop_results[on_cell]['percent_positive']
            off_pct = pop_results[off_cell]['percent_positive']
            ratio = on_pct / max(off_pct, 0.01)

            if objective == 'selectivity':
                score = ratio
            elif objective == 'activation':
                score = on_pct
            elif objective == 'balanced':
                score = on_pct * np.log10(max(ratio, 1))
            else:
                score = ratio

            sweep_results.append({
                'sp_ratio': sp,
                'sensor_copies': sensor_c,
                'payload_copies': payload_c,
                'sensor_ng': sensor_ng,
                'payload_ng': payload_ng,
                'on_pct': on_pct,
                'off_pct': off_pct,
                'ratio': ratio,
                'score': score,
                'pop_results': pop_results,
            })

        # Find optimal
        best = max(sweep_results, key=lambda r: r['score'])

        return {
            'sweep': sweep_results,
            'best': best,
            'objective': objective,
            'total_mRNA_ng': total_mRNA_ng,
            'on_cell': on_cell,
            'off_cell': off_cell,
        }

    def dose_sweep(self, cell_profiles, sensor_ng_range, payload_ng,
                   copies_per_ng=20, n_cells=20000, seed=42):
        """Sweep sensor dose at fixed payload dose.

        Parameters
        ----------
        cell_profiles : dict
        sensor_ng_range : array-like
            Range of sensor mRNA amounts (ng) to test
        payload_ng : float
            Fixed payload amount (ng)
        copies_per_ng : float
        n_cells : int
        seed : int

        Returns
        -------
        dict with sweep results
        """
        cell_names = list(cell_profiles.keys())
        on_cell = max(cell_names,
                      key=lambda c: cell_profiles[c].get('mirna_mean', 0))
        off_cell = min(cell_names,
                       key=lambda c: cell_profiles[c].get('mirna_mean', 0))

        payload_c = int(payload_ng * copies_per_ng)
        results = []

        for sensor_ng in sensor_ng_range:
            sensor_c = int(sensor_ng * copies_per_ng)
            pop, thresh = self._simulate_population(
                sensor_c, payload_c, cell_profiles, n_cells, seed)

            on_pct = pop[on_cell]['percent_positive']
            off_pct = pop[off_cell]['percent_positive']

            results.append({
                'sensor_ng': sensor_ng,
                'payload_ng': payload_ng,
                'sensor_copies': sensor_c,
                'payload_copies': payload_c,
                'on_pct': on_pct,
                'off_pct': off_pct,
                'ratio': on_pct / max(off_pct, 0.01),
            })

        return {
            'sweep': results,
            'on_cell': on_cell,
            'off_cell': off_cell,
        }

    def format_report(self, opt_result):
        """Format optimization results as a readable report.

        Parameters
        ----------
        opt_result : dict from optimize_ratio

        Returns
        -------
        str : formatted report
        """
        lines = []
        lines.append('=' * 75)
        lines.append(f'CIRCUIT DOSING OPTIMIZATION REPORT')
        lines.append(f'Objective: {opt_result["objective"]}')
        lines.append(f'Total mRNA: {opt_result["total_mRNA_ng"]}ng per well')
        lines.append(f'ON cell: {opt_result["on_cell"]}, '
                      f'OFF cell: {opt_result["off_cell"]}')
        lines.append('=' * 75)
        lines.append('')
        lines.append(f'{"S:P":>6s} {"sensor":>8s} {"payload":>8s} '
                      f'{"ON%":>7s} {"OFF%":>7s} {"ratio":>7s} {"score":>8s}')
        lines.append('-' * 60)

        best_sp = opt_result['best']['sp_ratio']
        for r in opt_result['sweep']:
            marker = ' <--' if r['sp_ratio'] == best_sp else ''
            lines.append(
                f'{r["sp_ratio"]:6.2f} {r["sensor_ng"]:7.1f}ng '
                f'{r["payload_ng"]:7.1f}ng {r["on_pct"]:6.1f}% '
                f'{r["off_pct"]:6.2f}% {r["ratio"]:6.1f}x '
                f'{r["score"]:7.1f}{marker}')

        lines.append('')
        b = opt_result['best']
        lines.append(f'OPTIMAL: {b["sensor_ng"]:.0f}ng sensor + '
                      f'{b["payload_ng"]:.0f}ng payload '
                      f'(S:P = {b["sp_ratio"]}:1)')
        lines.append(f'  {opt_result["on_cell"]}: {b["on_pct"]:.1f}% positive')
        lines.append(f'  {opt_result["off_cell"]}: {b["off_pct"]:.2f}% positive')
        lines.append(f'  Selectivity: {b["ratio"]:.1f}x')

        return '\n'.join(lines)
