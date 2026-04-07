"""
Population layer for RNA logic gate circuit simulation.

Converts single-cell ODE results into flow cytometry-like readouts
by simulating cell-to-cell variability in mRNA delivery, miRNA levels,
and applying a fluorescence detection threshold.

Key insights from experimental calibration (3/31/2026 ON switch data):
  - Flow cytometry reports % positive cells (above a gate), not mean protein
  - The threshold effect dramatically sharpens ON:OFF ratios
  - Cell-to-cell variability in sensor:payload ratio creates circuit output spread
  - miR-122 variability within HuH7 contributes to the sfGFP+ distribution
  - HuH7 has ~3.5x higher autofluorescence than 4T1

Calibration targets (p065 + p069B AND gate, 100ng dose):
  4T1:  1.32% sfGFP+ (miR-122 absent, L7Ae represses payload)
  HuH7: 26.67% sfGFP+ (miR-122 silences L7Ae sensor, partial derepression)
  ON:OFF ratio: 20.2x
"""

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from .and_gate import ANDGateModel
from .parameters import get_params


class PopulationModel:
    """Simulate a population of cells with delivery and miRNA variability."""

    def __init__(self, params=None, n_cells=10000, seed=42):
        self.params = params or get_params()
        self.gate_model = ANDGateModel(self.params)
        self.n_cells = n_cells
        self.rng = np.random.default_rng(seed)
        self._lookup_cache = {}

    def _sample_lognormal(self, mean, cv, n):
        """Sample from lognormal distribution with given mean and CV."""
        if mean <= 0:
            return np.zeros(n)
        sigma = np.sqrt(np.log(1 + cv**2))
        mu = np.log(mean) - sigma**2 / 2
        return self.rng.lognormal(mu, sigma, n)

    def _sample_correlated_delivery(self, sensor_mean, payload_mean, cv,
                                     correlation, n):
        """Sample correlated sensor and payload delivery per cell.

        Uses shared + independent noise to generate correlated lognormals.
        """
        sigma = np.sqrt(np.log(1 + cv**2))

        z_shared = self.rng.standard_normal(n)
        z_sensor = correlation * z_shared + np.sqrt(1 - correlation**2) * self.rng.standard_normal(n)
        z_payload = correlation * z_shared + np.sqrt(1 - correlation**2) * self.rng.standard_normal(n)

        mu_s = np.log(sensor_mean) - sigma**2 / 2
        mu_p = np.log(payload_mean) - sigma**2 / 2

        sensor = np.exp(mu_s + sigma * z_sensor)
        payload = np.exp(mu_p + sigma * z_payload)

        return sensor, payload

    def build_lookup_table(self, mirna_values, sensor_range=None,
                           payload_range=None, grid_size=20, params=None):
        """Build interpolation lookup for sfGFP(sensor, payload, mirna).

        Parameters
        ----------
        mirna_values : array-like or float
            miRNA levels to include in the lookup. If scalar, builds 2D lookup.
        sensor_range : tuple (min, max), optional
            Range of sensor copies. Default: (30, 10000)
        payload_range : tuple (min, max), optional
            Range of payload copies. Default: (30, 10000)
        grid_size : int
            Points per dimension
        params : dict, optional

        Returns
        -------
        interpolator function
        """
        p = params or self.params
        s_min, s_max = sensor_range or (30, 10000)
        p_min, p_max = payload_range or (30, 10000)

        sensor_grid = np.logspace(np.log10(s_min), np.log10(s_max), grid_size)
        payload_grid = np.logspace(np.log10(p_min), np.log10(p_max), grid_size)

        mirna_arr = np.atleast_1d(mirna_values)

        if len(mirna_arr) == 1:
            # 2D lookup (fixed miRNA)
            grid = np.zeros((grid_size, grid_size))
            for i, s in enumerate(sensor_grid):
                for j, pl in enumerate(payload_grid):
                    grid[i, j] = self.gate_model.simulate(
                        mirna_arr[0], s, pl, p)['peak_sfgfp']

            return RegularGridInterpolator(
                (np.log10(sensor_grid), np.log10(payload_grid)),
                grid, bounds_error=False, fill_value=0
            )
        else:
            # 3D lookup (variable miRNA)
            mirna_grid = np.logspace(
                np.log10(max(mirna_arr.min() * 0.1, 10)),
                np.log10(mirna_arr.max() * 2),
                grid_size
            )
            grid = np.zeros((grid_size, grid_size, grid_size))
            for i, s in enumerate(sensor_grid):
                for j, pl in enumerate(payload_grid):
                    for k, m in enumerate(mirna_grid):
                        grid[i, j, k] = self.gate_model.simulate(
                            m, s, pl, p)['peak_sfgfp']

            return RegularGridInterpolator(
                (np.log10(sensor_grid), np.log10(payload_grid),
                 np.log10(mirna_grid)),
                grid, bounds_error=False, fill_value=0
            )

    def sfgfp_per_copy_free(self, params=None):
        """Compute peak sfGFP molecules per copy of freely translating mRNA."""
        p = params or self.params
        k_tr = p['k_translate']
        g_m = p['gamma_mRNA']
        g_g = p['gamma_GFP']
        if abs(g_m - g_g) > 1e-10:
            t_peak = np.log(g_m / g_g) / (g_m - g_g)
        else:
            t_peak = 1.0 / g_m
        return k_tr / (g_g - g_m) * (np.exp(-g_m * t_peak) - np.exp(-g_g * t_peak))

    def simulate_flow_cytometry(self, cell_profiles, sensor_mean, payload_mean,
                                 params=None):
        """Full population simulation mimicking flow cytometry readout.

        Parameters
        ----------
        cell_profiles : dict
            {cell_name: {
                'mirna_copies': float or (mean, cv) tuple,
                'transfection_efficiency': float,
            }}
        sensor_mean : float
            Mean sensor mRNA copies per transfected cell
        payload_mean : float
            Mean payload mRNA copies per transfected cell
        params : dict, optional

        Returns
        -------
        dict with per-cell results, threshold, and selectivity metrics
        """
        p = params or self.params
        n = self.n_cells
        cv = p.get('delivery_cv', 0.5)
        corr = p.get('delivery_correlation', 0.7)
        sfgfp_per_copy = self.sfgfp_per_copy_free(p)

        # Sample delivery (same for all cell types - same transfection mix)
        sensor_copies, payload_copies = self._sample_correlated_delivery(
            sensor_mean, payload_mean, cv, corr, n
        )

        # Free payload sfGFP (for threshold calibration)
        sfgfp_free = payload_copies * sfgfp_per_copy

        results = {}
        for cell_name, profile in cell_profiles.items():
            te = profile.get('transfection_efficiency', 0.85)
            transfected = self.rng.random(n) < te

            # miRNA per cell
            mirna_spec = profile.get('mirna_copies', 0)
            if isinstance(mirna_spec, (tuple, list)):
                # (mean, cv) -> variable miRNA
                mirna_mean, mirna_cv = mirna_spec
                mirna_cells = self._sample_lognormal(mirna_mean, mirna_cv, n)
            else:
                mirna_cells = np.full(n, float(mirna_spec))

            # Compute circuit sfGFP per cell using ODE lookup
            # For efficiency, use a 1D lookup if miRNA is constant,
            # or precompute on a grid
            circuit_sfgfp = np.zeros(n)
            n_trans = np.sum(transfected)

            if n_trans > 0:
                trans_idx = np.where(transfected)[0]
                s_trans = sensor_copies[trans_idx]
                p_trans = payload_copies[trans_idx]
                m_trans = mirna_cells[trans_idx]

                # Use grid-based interpolation for speed
                # Build lookup for this cell type's miRNA range
                unique_mirna = np.unique(m_trans)
                if len(unique_mirna) == 1:
                    # Constant miRNA - 2D lookup
                    interp = self.build_lookup_table(
                        unique_mirna[0], grid_size=15, params=p)
                    pts = np.column_stack([
                        np.log10(np.clip(s_trans, 30, 10000)),
                        np.log10(np.clip(p_trans, 30, 10000)),
                    ])
                else:
                    # Variable miRNA - 3D lookup
                    interp = self.build_lookup_table(
                        m_trans, grid_size=12, params=p)
                    pts = np.column_stack([
                        np.log10(np.clip(s_trans, 30, 10000)),
                        np.log10(np.clip(p_trans, 30, 10000)),
                        np.log10(np.clip(m_trans, 10, 200000)),
                    ])

                circuit_sfgfp[trans_idx] = interp(pts)

            # Free payload for this cell type
            free_sfgfp = np.zeros(n)
            free_sfgfp[transfected] = sfgfp_free[transfected]

            results[cell_name] = {
                'circuit_sfgfp': circuit_sfgfp,
                'free_sfgfp': free_sfgfp,
                'transfected': transfected,
                'mirna_cells': mirna_cells,
                'sensor_copies': sensor_copies,
                'payload_copies': payload_copies,
            }

        return {
            'cell_results': results,
            'sfgfp_per_copy': sfgfp_per_copy,
            'n_cells': n,
        }

    def apply_gate(self, sim_results, threshold):
        """Apply sfGFP detection threshold to simulation results.

        Parameters
        ----------
        sim_results : dict from simulate_flow_cytometry
        threshold : float
            sfGFP molecule threshold for gate

        Returns
        -------
        dict with per-cell-type % positive and selectivity
        """
        pcts = {}
        free_pcts = {}

        for name, data in sim_results['cell_results'].items():
            pcts[name] = np.mean(data['circuit_sfgfp'] > threshold) * 100
            free_pcts[name] = np.mean(data['free_sfgfp'] > threshold) * 100

        # Selectivity
        if pcts:
            target = max(pcts, key=pcts.get)
            offtarget = min(pcts, key=pcts.get)
            selectivity = pcts[target] / max(pcts[offtarget], 0.01)
        else:
            target = offtarget = None
            selectivity = 0

        return {
            'circuit_percent_positive': pcts,
            'free_percent_positive': free_pcts,
            'target_cell': target,
            'offtarget_cell': offtarget,
            'selectivity': selectivity,
            'threshold': threshold,
        }

    def calibrate_threshold(self, sim_results, cell_name,
                            target_free_percent):
        """Find threshold that gives target % positive for free payload.

        Parameters
        ----------
        sim_results : dict from simulate_flow_cytometry
        cell_name : str
            Cell type to calibrate from (e.g., '4T1')
        target_free_percent : float
            Target % sfGFP+ for free payload (e.g., 29.87 for 4T1)

        Returns
        -------
        threshold : float
        """
        free_sfgfp = sim_results['cell_results'][cell_name]['free_sfgfp']
        n = len(free_sfgfp)
        target_frac = target_free_percent / 100.0
        sorted_vals = np.sort(free_sfgfp)[::-1]
        idx = int(target_frac * n)
        return sorted_vals[min(idx, n - 1)]
