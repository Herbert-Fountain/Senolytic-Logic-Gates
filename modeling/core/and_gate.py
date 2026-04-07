"""
L7Ae AND Gate intracellular model.

Models the actual circuit architecture used in the miR-122 ON switch experiment:
  mRNA-1: 5'MRE-L7Ae sensor (L7Ae CDS with miR-122-5p MRE in 5'UTR)
  mRNA-2: 2xKt-sfGFP (sfGFP CDS with 2 K-turn motifs in 5'UTR)

When miR-122 is ABSENT (4T1):
  -> L7Ae sensor mRNA translates freely -> L7Ae protein accumulates
  -> L7Ae binds K-turns on sfGFP mRNA -> sfGFP repressed
  -> Result: sfGFP OFF

When miR-122 is PRESENT (HuH7):
  -> miR-122 silences L7Ae sensor mRNA via 5'UTR AGO2 cleavage
  -> Less L7Ae protein produced -> L7Ae decays
  -> K-turn sites on sfGFP mRNA become unoccupied
  -> sfGFP translated
  -> Result: sfGFP ON (partially, depending on stoichiometry)

Species tracked (8 state variables):
  [0] M_sensor_free    - Free L7Ae sensor mRNA (translatable)
  [1] M_sensor_bound   - L7Ae sensor mRNA bound to RISC-miR-122 (silenced)
  [2] RISC             - Free RISC-miR-122 complexes
  [3] L7Ae             - Free L7Ae protein
  [4] M_payload_free   - Free 2xKt-sfGFP mRNA (translatable)
  [5] M_payload_repr   - 2xKt-sfGFP mRNA with L7Ae bound (repressed)
  [6] sfGFP            - sfGFP protein
  [7] L7Ae_on_payload  - L7Ae molecules bound to payload K-turns
"""

import numpy as np
from scipy.integrate import solve_ivp
from .parameters import get_params, halflife_to_rate, nM_to_molecules


class ANDGateModel:
    """ODE model of the L7Ae/K-turn miRNA-responsive AND gate circuit."""

    def __init__(self, params=None):
        self.params = params or get_params()

    def ode_system(self, t, y, p):
        """Compute derivatives for the AND gate system.

        Parameters
        ----------
        t : float
            Time (hours)
        y : array
            State vector [M_sens, M_sens_b, RISC, L7Ae, M_pay, M_pay_r, sfGFP, L7Ae_bound]
        p : dict
            Parameters

        Returns
        -------
        dydt : list
            Derivatives
        """
        M_s, M_sb, R, L, M_p, M_pr, G, Lb = y

        # Ensure non-negative
        M_s = max(M_s, 0)
        M_sb = max(M_sb, 0)
        R = max(R, 0)
        L = max(L, 0)
        M_p = max(M_p, 0)
        M_pr = max(M_pr, 0)
        G = max(G, 0)
        Lb = max(Lb, 0)

        # ============================================================
        # Layer 1: miRNA silencing of L7Ae sensor mRNA
        # ============================================================
        # 5'UTR MRE: AGO2 cleavage (catalytic, RISC recycled)
        n_mre_sensor = p.get('n_mre_sensor', 1)
        sensor_binding = p['kon_RISC'] * n_mre_sensor * M_s * R
        sensor_unbinding = p['koff_RISC'] * M_sb
        sensor_cleavage = p['k_slice'] * M_sb  # AGO2 cleavage destroys mRNA

        # Sensor mRNA decay
        sensor_decay_free = p['gamma_mRNA'] * M_s
        sensor_decay_bound = p['gamma_mRNA'] * M_sb

        # L7Ae translation (only from free sensor mRNA)
        l7ae_translation = p['k_translate'] * M_s

        # L7Ae protein decay
        l7ae_decay = p['gamma_L7Ae'] * L

        # ============================================================
        # Layer 2: L7Ae repression of payload mRNA
        # ============================================================
        # L7Ae binds K-turn motifs on payload mRNA
        n_kturn = p.get('n_kturn', 2)  # 2xKt in the actual construct

        # L7Ae-K-turn binding/unbinding
        # Each K-turn can independently bind L7Ae
        # Simplified: treat payload as either free or fully repressed
        # A payload with 2 K-turns needs both occupied for full repression
        # Model: use effective binding that accounts for multiple sites
        payload_binding = p['kon_L7Ae'] * n_kturn * L * M_p
        payload_unbinding = p['koff_L7Ae'] * M_pr

        # Payload mRNA decay
        payload_decay_free = p['gamma_mRNA'] * M_p
        payload_decay_repr = p['gamma_mRNA'] * M_pr

        # sfGFP translation
        # Free payload translates normally; repressed payload is reduced
        repression_factor = 1.0 / p['L7Ae_repression_fold']
        sfgfp_translation = p['k_translate'] * (M_p + repression_factor * M_pr)

        # sfGFP decay
        sfgfp_decay = p['gamma_GFP'] * G

        # ============================================================
        # ODEs
        # ============================================================
        dM_s = -sensor_binding + sensor_unbinding - sensor_decay_free
        dM_sb = sensor_binding - sensor_unbinding - sensor_cleavage - sensor_decay_bound
        dR = -sensor_binding + sensor_unbinding + sensor_cleavage  # RISC recycled
        dL = l7ae_translation - l7ae_decay - payload_binding + payload_unbinding
        dM_p = -payload_binding + payload_unbinding - payload_decay_free
        dM_pr = payload_binding - payload_unbinding - payload_decay_repr
        dG = sfgfp_translation - sfgfp_decay
        dLb = payload_binding - payload_unbinding  # Track bound L7Ae separately

        return [dM_s, dM_sb, dR, dL, dM_p, dM_pr, dG, dLb]

    def simulate(self, mirna_copies, sensor_copies, payload_copies, params=None):
        """Run a single-cell simulation of the AND gate circuit.

        Parameters
        ----------
        mirna_copies : float
            Copies of the cognate miRNA per cell
        sensor_copies : float
            Copies of L7Ae sensor mRNA delivered per cell
        payload_copies : float
            Copies of 2xKt-sfGFP mRNA delivered per cell
        params : dict, optional
            Parameter overrides

        Returns
        -------
        dict with time course and key metrics
        """
        p = params or self.params

        # Initial conditions
        y0 = [
            sensor_copies,   # M_sensor_free
            0,               # M_sensor_bound
            mirna_copies,    # RISC
            0,               # L7Ae
            payload_copies,  # M_payload_free
            0,               # M_payload_repr
            0,               # sfGFP
            0,               # L7Ae_bound
        ]

        t_span = (0, p['t_max_hr'])
        t_eval = np.linspace(0, p['t_max_hr'], p['n_timepoints'])

        sol = solve_ivp(
            lambda t, y: self.ode_system(t, y, p),
            t_span, y0, t_eval=t_eval,
            method='LSODA', rtol=1e-8, atol=1e-10,
            max_step=0.5
        )

        if not sol.success:
            raise RuntimeError(f'ODE solver failed: {sol.message}')

        names = ['M_sensor_free', 'M_sensor_bound', 'RISC', 'L7Ae',
                 'M_payload_free', 'M_payload_repr', 'sfGFP', 'L7Ae_bound']

        trajectories = {name: sol.y[i] for i, name in enumerate(names)}

        # Key metrics
        peak_sfgfp = np.max(trajectories['sfGFP'])
        final_sfgfp = trajectories['sfGFP'][-1]
        peak_l7ae = np.max(trajectories['L7Ae'])
        sensor_remaining = trajectories['M_sensor_free'][-1]

        return {
            't': sol.t,
            'trajectories': trajectories,
            'species_names': names,
            'peak_sfgfp': peak_sfgfp,
            'final_sfgfp': final_sfgfp,
            'peak_l7ae': peak_l7ae,
            'sensor_remaining_72h': sensor_remaining,
            'mirna_copies': mirna_copies,
            'sensor_copies': sensor_copies,
            'payload_copies': payload_copies,
        }

    def compare_cell_types(self, cell_profiles, sensor_copies, payload_copies,
                           params=None):
        """Compare circuit behavior across cell types.

        Parameters
        ----------
        cell_profiles : dict
            {cell_name: mirna_copies}
        sensor_copies : float
            L7Ae sensor mRNA copies per cell
        payload_copies : float
            2xKt-sfGFP mRNA copies per cell

        Returns
        -------
        dict with per-cell results and selectivity
        """
        results = {}
        for name, mirna in cell_profiles.items():
            results[name] = self.simulate(mirna, sensor_copies, payload_copies, params)

        peaks = {name: r['peak_sfgfp'] for name, r in results.items()}
        target = max(peaks, key=peaks.get)
        offtarget = min(peaks, key=peaks.get)
        selectivity = peaks[target] / max(peaks[offtarget], 1e-10)

        return {
            'cell_results': results,
            'peak_sfgfp': peaks,
            'target_cell': target,
            'offtarget_cell': offtarget,
            'selectivity': selectivity,
        }

    def dose_response(self, mirna_range, sensor_copies, payload_copies, params=None):
        """Sweep miRNA concentration and record sfGFP output."""
        responses = []
        for mirna in mirna_range:
            r = self.simulate(mirna, sensor_copies, payload_copies, params)
            responses.append(r['peak_sfgfp'])
        return {
            'mirna_copies': np.array(mirna_range),
            'peak_sfgfp': np.array(responses),
        }

    def molar_ratio_sweep(self, mirna_copies, sensor_range, payload_copies,
                          params=None):
        """Sweep sensor:payload ratio and record sfGFP."""
        responses = []
        for sensor in sensor_range:
            r = self.simulate(mirna_copies, sensor, payload_copies, params)
            responses.append(r['peak_sfgfp'])
        return {
            'sensor_copies': np.array(sensor_range),
            'peak_sfgfp': np.array(responses),
            'ratio': np.array(sensor_range) / payload_copies,
        }
