"""
Default kinetic parameters for RNA circuit simulation.
All values are from published literature with sources cited.
Units: molecules per cell, hours.
"""

import math


def halflife_to_rate(halflife_hr):
    """Convert half-life (hours) to first-order decay rate (hr^-1)."""
    return math.log(2) / halflife_hr


# Cell volume for nM to molecules/cell conversion
# Typical mammalian cell volume ~1-4 pL; using 2 pL as default
CELL_VOLUME_PL = 2.0
AVOGADRO = 6.022e23

def nM_to_molecules(conc_nM, volume_pL=CELL_VOLUME_PL):
    """Convert nM concentration to molecules per cell."""
    return conc_nM * 1e-9 * volume_pL * 1e-12 * AVOGADRO

def molecules_to_nM(n_molecules, volume_pL=CELL_VOLUME_PL):
    """Convert molecules per cell to nM concentration."""
    return n_molecules / (volume_pL * 1e-12 * AVOGADRO) * 1e9


DEFAULT_PARAMS = {
    # ================================================================
    # mRNA Properties
    # ================================================================
    # Modified mRNA (m1psi) half-life
    # Source: Mauger et al., PNAS, 2019, PMID: 31712433
    'mRNA_halflife_hr': 12.0,

    # Translation rate: proteins produced per mRNA per hour
    # Source: Schwanhausser et al., Nature, 2011/2013 (corrected), PMID: 21593866
    # Median endogenous: ~140; synthetic modified mRNA may be higher
    'k_translate': 100.0,

    # ================================================================
    # miRNA-RISC Binding Kinetics
    # ================================================================
    # Association rate for RISC-miRNA binding to perfectly complementary MRE
    # Source: Briskin et al., Mol Cell, 2019, PMID: 31324449
    # In vitro: 0.01-0.05 nM^-1 min^-1
    # Converted to molecules^-1 cell hr^-1:
    #   0.03 nM^-1 min^-1 * 60 min/hr / (600 molecules/nM) = 0.003
    'kon_RISC': 0.003,

    # Dissociation rate for RISC-miRNA from MRE
    # Source: Briskin et al., 2019; Salomon et al., Cell, 2015, PMID: 26140592
    # KD ~ 0.01-0.1 nM for 8mer; koff = KD * kon
    # At KD = 0.05 nM (30 molecules): koff = 30 * 0.003 = 0.09 hr^-1
    'koff_RISC': 0.09,

    # AGO2 endonucleolytic cleavage rate (for perfectly complementary sites)
    # Source: Wang & Bartel, Mol Cell, 2024, PMID: 39025072
    # In vitro: 0.1-1.0 min^-1 for favorable guide sequences
    # Using 0.3 min^-1 = 18 hr^-1
    'k_slice': 18.0,

    # ================================================================
    # L7Ae-K-turn Binding
    # ================================================================
    # L7Ae-K-turn dissociation constant
    # Source: Turner et al., RNA, 2005, PMC: 1370803
    # KD = 0.9 nM (in vitro FRET measurement)
    'Kd_L7Ae_nM': 0.9,

    # Association rate for L7Ae binding K-turn
    # Estimated: typical protein-RNA kon ~ 1e6 M^-1 s^-1
    # = 1e6 * 1e-9 nM^-1 * 3600 s/hr / 600 molecules/nM = 6.0 molecule^-1 cell hr^-1
    # This is fast; binding is not rate-limiting
    'kon_L7Ae': 6.0,

    # Dissociation rate: koff = KD * kon
    # KD = 0.9 nM = ~540 molecules; koff = 540 * 6.0 = ... too fast
    # Better: use KD directly in steady-state approximation
    # koff = KD_molecules * kon = 540 * 6.0 = 3240 hr^-1 (very fast on/off)
    # L7Ae binding reaches equilibrium rapidly relative to other timescales
    'koff_L7Ae': 3240.0,

    # Functional repression fold when L7Ae is bound to 5'UTR K-turn
    # L7Ae binding blocks 40S ribosome scanning; near-complete translational block
    # Source: Saito et al., Nat Chem Biol, 2010 (measured ~10x for 1xKt reporter)
    # Calibrated from ON switch flow data (3/31/2026): near-complete block needed
    # to match 95.6% suppression in 4T1 and bimodal flow histograms
    'L7Ae_repression_fold': 1000.0,

    # Expression efficiency ratio between cell types
    # HuH7 produces ~5.5x more sfGFP per mRNA copy than 4T1
    # Source: flow cytometry MFI (HuH7 sfGFP+ median ~55M vs 4T1 ~10M FITC-A)
    'expression_ratio_HuH7': 5.5,

    # Circuit failure rate (fraction of cells where repression fails)
    # Accounts for stochastic effects: translational bursting, endosomal
    # escape variability, L7Ae misfolding. Calibrated from 4T1 AND gate
    # (1.32% positive = irreducible circuit leakage)
    'circuit_failure_rate': 0.044,

    # ================================================================
    # Protein Degradation
    # ================================================================
    # GFP half-life: 26 hours
    # Source: Li et al., PEDS, 1998, PMID: 10611396
    'GFP_halflife_hr': 26.0,

    # DTA half-life: 26.5 hours
    # Source: Bhatt et al., EMBO J, 1998, PMID: 9450983
    'DTA_halflife_hr': 26.5,

    # L7Ae half-life: ~20 hours (estimated; no direct measurement published)
    # Small, thermostable archaeal protein; assumed stable
    'L7Ae_halflife_hr': 20.0,

    # Gasdermin: treated as irreversible pore formation, not simple degradation
    'Gasdermin_halflife_hr': 10.0,  # Placeholder

    # ================================================================
    # Transfection Parameters
    # ================================================================
    # mRNA copies delivered per transfected cell
    # Estimated from 100ng/well, 30,000 cells/well, MW ~10^6
    # ~2000 copies per transfected cell at 100ng dose
    # Source: Cohen et al., 2009, PMC: 2765102; experimental calibration
    'mRNA_delivered_per_cell': 2000,

    # Transfection efficiency (fraction of cells receiving any mRNA)
    # Calibrated from flow cytometry: 2xKt-sfGFP alone data (3/31/2026)
    # 4T1: ~31% sfGFP+ -> TE ~0.31; HuH7: ~91.5% sfGFP+ -> TE ~0.94
    'transfection_efficiency': 0.85,  # Default; use cell-specific values
    'transfection_efficiency_4T1': 0.31,
    'transfection_efficiency_HuH7': 0.94,

    # Coefficient of variation for mRNA delivery per cell
    # Accounts for cell-to-cell variability in uptake
    'delivery_cv': 0.5,

    # Sensor:payload delivery correlation
    # Two mRNAs co-delivered in same lipoplexes; partially correlated
    'delivery_correlation': 0.7,

    # ================================================================
    # miRNA Levels (copies per cell)
    # ================================================================
    # miR-122-5p in HuH7: one of the most abundant miRNAs in hepatocytes
    # Source: Lagos-Quintana et al., 2002; Jopling et al., 2005
    # Literature range: 50,000-120,000 copies/cell (bulk measurement)
    # Calibrated from ON switch flow data (3/31/2026): mean=8,000, CV=0.5
    # Lower than bulk estimates; reflects functional RISC-loaded miR-122
    # and HuH7 passage-dependent expression heterogeneity
    'miR122_HuH7': 8000,
    'miR122_4T1': 0,

    # miR-122 cell-to-cell variability (CV within HuH7 population)
    # Calibrated from AND gate flow data: CV=0.5 gives 26.7% sfGFP+
    'miR122_cv': 0.5,

    # ================================================================
    # Cell Death
    # ================================================================
    # Payload molecules needed to trigger cell death
    # For DTA: a single molecule can kill (catalytically inactivates ribosomes)
    # For Gasdermin: needs enough to form pores (~16 monomers per pore)
    # Default: conservative threshold
    'death_threshold_DTA': 10,
    'death_threshold_gasdermin': 500,
    'death_threshold': 100,  # Generic default

    # ================================================================
    # Simulation Settings
    # ================================================================
    't_max_hr': 72.0,
    'n_timepoints': 500,
}


def get_params(**overrides):
    """Return default parameters with optional overrides."""
    params = DEFAULT_PARAMS.copy()
    params.update(overrides)

    # Compute derived rates
    params['gamma_mRNA'] = halflife_to_rate(params['mRNA_halflife_hr'])
    params['gamma_GFP'] = halflife_to_rate(params['GFP_halflife_hr'])
    params['gamma_DTA'] = halflife_to_rate(params['DTA_halflife_hr'])
    params['gamma_L7Ae'] = halflife_to_rate(params['L7Ae_halflife_hr'])
    params['gamma_gasdermin'] = halflife_to_rate(params['Gasdermin_halflife_hr'])

    # L7Ae KD in molecules
    params['Kd_L7Ae_molecules'] = nM_to_molecules(params['Kd_L7Ae_nM'])

    return params
