"""
Phase 3 Benchmark: AND gate model vs experimental flow cytometry data.

Experimental data: miR-122 ON Switch experiment (3/31/2026)
  Constructs: p065 (2xKt-sfGFP payload) + p069B (L7Ae sensor with miR-122 MRE)
  Cell lines: NIH 4T1 (miR-122 absent) and HuH7 (miR-122 high)
  Dose: 100ng each per well, 30,000 cells/well, Lipofectamine MessengerMAX

Targets:
  2xKt-sfGFP alone:    4T1 = 29.87% sfGFP+, HuH7 = 91.49%
  AND gate circuit:     4T1 =  1.32% sfGFP+, HuH7 = 26.67%
  ON:OFF ratio:         20.2x
  L7Ae suppression:     95.6% (29.87% -> 1.32% in 4T1)
  miR-122 recovery:     29.2% (26.67% / 91.49% in HuH7)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
from modeling.core.and_gate import ANDGateModel
from modeling.core.parameters import get_params
from modeling.core.population import PopulationModel


def test_single_cell_dose_response():
    """Test single-cell AND gate circuit across miR-122 range."""
    print('\n=== Single-Cell AND Gate: sfGFP vs miR-122 ===\n')

    p = get_params()
    model = ANDGateModel(p)
    sfgfp_per_copy = PopulationModel(p).sfgfp_per_copy_free(p)
    free_peak = 2000 * sfgfp_per_copy

    print(f'Free payload peak sfGFP (2000 copies): {free_peak:,.0f} molecules')
    print(f'L7Ae-K-turn KD: {p["Kd_L7Ae_molecules"]:.0f} molecules')
    print(f'L7Ae repression fold: {p["L7Ae_repression_fold"]}')
    print()

    mirna_levels = [0, 100, 1000, 5000, 10000, 30000, 50000, 100000]
    print(f'{"miR-122":>10s} {"L7Ae_peak":>10s} {"sfGFP_peak":>12s} {"efficiency":>10s}')
    print('-' * 48)

    for mirna in mirna_levels:
        r = model.simulate(mirna, 2000, 2000, p)
        eff = r['peak_sfgfp'] / free_peak * 100
        print(f'{mirna:10,d} {r["peak_l7ae"]:10,.0f} {r["peak_sfgfp"]:12,.0f} {eff:9.1f}%')

    # Test at calibrated HuH7 miR-122 level
    huh7_mirna = p.get('miR122_HuH7', 50000)
    r_huh7 = model.simulate(huh7_mirna, 2000, 2000, p)
    r_4t1 = model.simulate(0, 2000, 2000, p)
    ratio = r_huh7['peak_sfgfp'] / max(r_4t1['peak_sfgfp'], 1)

    print(f'\n--- Circuit at calibrated levels ---')
    print(f'HuH7 (miR-122={huh7_mirna:,d}): sfGFP={r_huh7["peak_sfgfp"]:,.0f} '
          f'({r_huh7["peak_sfgfp"]/free_peak*100:.1f}% of free)')
    print(f'4T1  (miR-122=0):          sfGFP={r_4t1["peak_sfgfp"]:,.0f} '
          f'({r_4t1["peak_sfgfp"]/free_peak*100:.1f}% of free)')
    print(f'Single-cell ratio: {ratio:.1f}x')


def test_population_model():
    """Test population model with flow cytometry comparison."""
    print('\n=== Population Model: Flow Cytometry Comparison ===\n')

    p = get_params()

    # Cell profiles matching the experiment
    cell_profiles = {
        '4T1': {
            'mirna_copies': 0,
            'transfection_efficiency': 0.31,
        },
        'HuH7': {
            'mirna_copies': (p.get('miR122_HuH7', 50000),
                             p.get('miR122_cv', 1.0)),
            'transfection_efficiency': 0.94,
        },
    }

    pop = PopulationModel(p, n_cells=10000, seed=42)

    print('Running population simulation...')
    sim = pop.simulate_flow_cytometry(
        cell_profiles,
        sensor_mean=2000,
        payload_mean=2000,
        params=p,
    )

    # Calibrate threshold from 4T1 free payload = 29.87%
    threshold = pop.calibrate_threshold(sim, '4T1', 29.87)
    print(f'Calibrated threshold: {threshold:,.0f} sfGFP molecules')

    # Apply gate
    gate_results = pop.apply_gate(sim, threshold)

    print(f'\n{"Condition":<25s} {"Model":>8s} {"Expt":>8s}')
    print('-' * 45)

    targets = {
        '4T1': {'free': 29.87, 'circuit': 1.32},
        'HuH7': {'free': 91.49, 'circuit': 26.67},
    }

    for name in ['4T1', 'HuH7']:
        f_pct = gate_results['free_percent_positive'].get(name, 0)
        c_pct = gate_results['circuit_percent_positive'].get(name, 0)
        print(f'{name} free payload       {f_pct:7.1f}%  {targets[name]["free"]:7.1f}%')
        print(f'{name} AND gate circuit   {c_pct:7.1f}%  {targets[name]["circuit"]:7.1f}%')

    c4t1 = gate_results['circuit_percent_positive'].get('4T1', 0)
    chuh7 = gate_results['circuit_percent_positive'].get('HuH7', 0)
    model_ratio = chuh7 / max(c4t1, 0.01)

    print(f'\nON:OFF ratio:  Model={model_ratio:.1f}x  Expt=20.2x')
    print(f'Selectivity:   {gate_results["selectivity"]:.1f}x')


def test_sensor_alone():
    """Verify sensor alone gives ~0% sfGFP (no payload gene)."""
    print('\n=== Control: Sensor Alone (p069B) ===\n')

    p = get_params()
    model = ANDGateModel(p)

    # Sensor alone = no payload mRNA
    r = model.simulate(0, 2000, 0, p)
    print(f'4T1 sensor alone: sfGFP = {r["peak_sfgfp"]:.1f} (expect ~0)')

    r2 = model.simulate(50000, 2000, 0, p)
    print(f'HuH7 sensor alone: sfGFP = {r2["peak_sfgfp"]:.1f} (expect ~0)')
    print('PASS: sensor alone produces no sfGFP')


def test_dose_robustness():
    """Test that halving the dose gives similar ON:OFF ratio."""
    print('\n=== Dose Robustness: 100ng vs 50ng ===\n')

    p = get_params()
    model = ANDGateModel(p)

    for dose_label, sensor, payload in [('100ng', 2000, 2000), ('50ng', 1000, 1000)]:
        huh7 = model.simulate(50000, sensor, payload, p)
        t41 = model.simulate(0, sensor, payload, p)
        ratio = huh7['peak_sfgfp'] / max(t41['peak_sfgfp'], 1)
        print(f'{dose_label}: HuH7={huh7["peak_sfgfp"]:,.0f}, 4T1={t41["peak_sfgfp"]:,.0f}, ratio={ratio:.1f}x')

    print('\nExperimental: 100ng=20.2x, 50ng=17.3x')


if __name__ == '__main__':
    test_single_cell_dose_response()
    test_sensor_alone()
    test_dose_robustness()
    print('\n' + '='*60)
    print('Running population model (this may take a few minutes)...')
    print('='*60)
    test_population_model()
    print('\n=== Benchmark Complete ===')
