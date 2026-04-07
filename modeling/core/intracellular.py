"""
Intracellular model for RNA logic gate circuit simulation.

Implements ODE-based simulation of miRNA-responsive mRNA switches
within a single cell. Tracks all molecular species over time.

Phase 2: Simple ON/OFF switch with single miRNA input.
Phase 4 will extend to multi-construct AND gates.
"""

import numpy as np
from scipy.integrate import solve_ivp
from .parameters import get_params, halflife_to_rate


class MRNAConstruct:
    """Defines a single mRNA construct in the circuit."""

    def __init__(self, name, product, mre_mirnas=None, n_mres_5utr=0,
                 n_mres_3utr=0, has_kturn=False, copies_per_cell=1000,
                 switch_type='OFF'):
        """
        Parameters
        ----------
        name : str
            Construct identifier (e.g., 'L7Ae_mRNA', 'payload_mRNA')
        product : str
            Protein product name (e.g., 'GFP', 'L7Ae', 'DTA')
        mre_mirnas : list of str
            Which miRNAs the MREs respond to (e.g., ['miR-122-5p'])
        n_mres_5utr : int
            Number of MRE sites in the 5' UTR (AGO2 cleavage sites)
        n_mres_3utr : int
            Number of MRE sites in the 3' UTR (translational repression)
        has_kturn : bool
            Whether this construct has a K-turn in the 5' UTR (L7Ae target)
        copies_per_cell : int
            Number of copies delivered per cell
        switch_type : str
            'OFF' (miRNA represses), 'ON' (miRNA activates), or 'constitutive'
        """
        self.name = name
        self.product = product
        self.mre_mirnas = mre_mirnas or []
        self.n_mres_5utr = n_mres_5utr
        self.n_mres_3utr = n_mres_3utr
        self.has_kturn = has_kturn
        self.copies_per_cell = copies_per_cell
        self.switch_type = switch_type

    def total_mres(self):
        return self.n_mres_5utr + self.n_mres_3utr


class CircuitConfig:
    """Defines a complete circuit configuration."""

    def __init__(self, name='circuit'):
        self.name = name
        self.constructs = []
        self.mirna_profiles = {}  # {mirna_name: copies_per_cell}

    def add_construct(self, construct):
        self.constructs.append(construct)

    def set_mirna_profile(self, profile_dict):
        """Set miRNA concentrations. profile_dict: {mirna_name: copies_per_cell}"""
        self.mirna_profiles = profile_dict

    def get_mirna_copies(self, mirna_name):
        return self.mirna_profiles.get(mirna_name, 0)


class IntracellularModel:
    """ODE-based intracellular simulation of an mRNA circuit."""

    def __init__(self, params=None):
        self.params = params or get_params()
        self.results = None

    def _build_simple_off_switch(self, construct, mirna_copies):
        """Build ODE system for a simple OFF switch.

        Species: [M_free, M_bound, RISC, Protein]
        M_free: unbound mRNA (translating)
        M_bound: mRNA bound to RISC-miRNA (silenced)
        RISC: free RISC-miRNA complexes
        Protein: accumulated reporter/payload
        """
        p = self.params

        def ode(t, y):
            M, Mb, R, P = y

            # Effective binding rate scales with number of MRE sites
            n_sites = construct.total_mres()
            kon_eff = p['kon_RISC'] * n_sites

            # Reactions
            binding = kon_eff * M * R
            unbinding = p['koff_RISC'] * Mb
            cleavage = p['k_slice'] * Mb * (construct.n_mres_5utr / max(n_sites, 1))
            repression_3utr = Mb  # 3'UTR-bound mRNA does not translate
            mRNA_decay_free = p['gamma_mRNA'] * M
            mRNA_decay_bound = p['gamma_mRNA'] * Mb
            translation = p['k_translate'] * M  # Only free mRNA translates
            protein_decay = p.get('gamma_' + construct.product,
                                  p.get('gamma_GFP', 0.027)) * P

            dM = -binding + unbinding - mRNA_decay_free
            dMb = binding - unbinding - cleavage - mRNA_decay_bound
            dR = -binding + unbinding + cleavage  # RISC recycled after cleavage
            dP = translation - protein_decay

            return [dM, dMb, dR, dP]

        y0 = [construct.copies_per_cell, 0, mirna_copies, 0]
        return ode, y0, ['mRNA_free', 'mRNA_bound', 'RISC', construct.product]

    def _build_on_switch(self, construct, mirna_copies):
        """Build ODE system for an ON switch.

        The ON switch has an inhibitory extra sequence after the poly(A) tail.
        When the cognate miRNA is present, AGO2 cleaves the mRNA at the MRE
        after the poly(A), removing the inhibitory sequence and activating
        translation.

        Species: [M_silent, M_active, RISC, Protein]
        """
        p = self.params

        def ode(t, y):
            Ms, Ma, R, P = y

            # miRNA-mediated activation (cleavage of inhibitory sequence)
            activation = p['k_slice'] * Ms * R * 0.1  # Slower than standard cleavage
            mRNA_decay_silent = p['gamma_mRNA'] * Ms
            mRNA_decay_active = p['gamma_mRNA'] * Ma
            translation = p['k_translate'] * Ma  # Only activated mRNA translates
            protein_decay = p.get('gamma_' + construct.product,
                                  p.get('gamma_GFP', 0.027)) * P

            dMs = -activation - mRNA_decay_silent
            dMa = activation - mRNA_decay_active
            dR = 0  # RISC is catalytic, not consumed
            dP = translation - protein_decay

            return [dMs, dMa, dR, dP]

        y0 = [construct.copies_per_cell, 0, mirna_copies, 0]
        return ode, y0, ['mRNA_silent', 'mRNA_active', 'RISC', construct.product]

    def simulate_single_construct(self, construct, mirna_copies):
        """Simulate a single mRNA construct in one cell.

        Parameters
        ----------
        construct : MRNAConstruct
            The mRNA construct to simulate
        mirna_copies : float
            Copies of the cognate miRNA per cell

        Returns
        -------
        dict with keys: t, species_names, trajectories, steady_state
        """
        p = self.params
        t_span = (0, p['t_max_hr'])
        t_eval = np.linspace(0, p['t_max_hr'], p['n_timepoints'])

        if construct.switch_type == 'OFF':
            ode_func, y0, names = self._build_simple_off_switch(construct, mirna_copies)
        elif construct.switch_type == 'ON':
            ode_func, y0, names = self._build_on_switch(construct, mirna_copies)
        else:
            raise ValueError(f'Unknown switch type: {construct.switch_type}')

        # Solve ODE
        sol = solve_ivp(ode_func, t_span, y0, t_eval=t_eval,
                        method='LSODA', rtol=1e-8, atol=1e-10,
                        max_step=0.5)

        if not sol.success:
            raise RuntimeError(f'ODE solver failed: {sol.message}')

        # Extract results
        trajectories = {name: sol.y[i] for i, name in enumerate(names)}
        steady_state = {name: sol.y[i][-1] for i, name in enumerate(names)}

        self.results = {
            't': sol.t,
            'species_names': names,
            'trajectories': trajectories,
            'steady_state': steady_state,
            'construct': construct.name,
            'mirna_copies': mirna_copies,
        }

        return self.results

    def dose_response(self, construct, mirna_range, metric='peak_protein'):
        """Compute dose-response: payload expression vs miRNA concentration.

        Parameters
        ----------
        construct : MRNAConstruct
            The mRNA construct
        mirna_range : array-like
            Range of miRNA copy numbers to sweep
        metric : str
            'peak_protein' or 'steady_state_protein'

        Returns
        -------
        dict with keys: mirna_copies, response, metric
        """
        responses = []

        for mirna in mirna_range:
            result = self.simulate_single_construct(construct, mirna)
            protein_name = construct.product
            trajectory = result['trajectories'][protein_name]

            if metric == 'peak_protein':
                responses.append(np.max(trajectory))
            elif metric == 'steady_state_protein':
                responses.append(trajectory[-1])
            else:
                raise ValueError(f'Unknown metric: {metric}')

        return {
            'mirna_copies': np.array(mirna_range),
            'response': np.array(responses),
            'metric': metric,
            'construct': construct.name,
        }

    def compare_cell_types(self, construct, cell_profiles):
        """Run simulation for multiple cell types and compare.

        Parameters
        ----------
        construct : MRNAConstruct
            The circuit construct
        cell_profiles : dict
            {cell_name: mirna_copies} for each cell type

        Returns
        -------
        dict with per-cell-type results and selectivity metrics
        """
        results = {}
        for cell_name, mirna_copies in cell_profiles.items():
            results[cell_name] = self.simulate_single_construct(construct, mirna_copies)

        # Compute selectivity
        protein_name = construct.product
        peaks = {name: np.max(r['trajectories'][protein_name])
                 for name, r in results.items()}

        # Find target (highest expression) and off-target (lowest)
        target = max(peaks, key=peaks.get)
        offtarget = min(peaks, key=peaks.get)
        selectivity = peaks[target] / max(peaks[offtarget], 1e-10)

        return {
            'cell_results': results,
            'peak_protein': peaks,
            'target_cell': target,
            'offtarget_cell': offtarget,
            'selectivity': selectivity,
        }


def create_off_switch(name='OFF_switch', product='GFP', mirna='miR-122-5p',
                      copies=1000, n_5utr=1, n_3utr=4):
    """Convenience: create a standard OFF-switch construct (Saito design)."""
    return MRNAConstruct(
        name=name, product=product, mre_mirnas=[mirna],
        n_mres_5utr=n_5utr, n_mres_3utr=n_3utr,
        copies_per_cell=copies, switch_type='OFF'
    )


def create_on_switch(name='ON_switch', product='GFP', mirna='miR-122-5p',
                     copies=1000):
    """Convenience: create a standard ON-switch construct."""
    return MRNAConstruct(
        name=name, product=product, mre_mirnas=[mirna],
        n_mres_5utr=0, n_mres_3utr=0,
        copies_per_cell=copies, switch_type='ON'
    )
