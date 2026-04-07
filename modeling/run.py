#!/usr/bin/env python3
"""
RNA Logic Gate Circuit Modeling Tool - Command Line Interface

Usage:
    python run.py simulate    -- Run AND gate simulation for HuH7 vs 4T1
    python run.py optimize    -- Find optimal sensor:payload ratio
    python run.py design      -- Generate a validation experiment plan
    python run.py calibrate   -- Fit model to experimental results (CSV)
    python run.py benchmark   -- Run benchmark against experimental data
    python run.py sweep       -- Sweep miR-122 dose-response curve

Examples:
    python run.py simulate --mirna 50000 --sensor 2000 --payload 2000
    python run.py optimize --total-ng 200 --objective balanced
    python run.py design --payload-ng 150 --sensor-range 10,25,50,100,150
    python run.py calibrate --csv results.csv
"""

import argparse
import sys
import os
import csv
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modeling.core import (
    ANDGateModel, PopulationModel, CircuitOptimizer,
    ExperimentDesigner, ModelCalibrator, get_params
)


# Default cell profiles (calibrated from 3/31/2026 ON switch experiment)
DEFAULT_CELL_PROFILES = {
    '4T1': {
        'mirna_mean': 0,
        'mirna_cv': 0.5,
        'transfection_efficiency': 0.31,
        'expression_factor': 1.0,
    },
    'HuH7': {
        'mirna_mean': 8000,
        'mirna_cv': 0.5,
        'transfection_efficiency': 0.94,
        'expression_factor': 5.5,
    },
}


def cmd_simulate(args):
    """Run a single AND gate simulation."""
    p = get_params(L7Ae_repression_fold=1000, t_max_hr=args.hours)
    model = ANDGateModel(p)

    print(f'Simulating AND gate circuit ({args.hours}h)')
    print(f'  Sensor mRNA: {args.sensor} copies')
    print(f'  Payload mRNA: {args.payload} copies')
    print(f'  miR-122: {args.mirna} copies')
    print()

    r = model.simulate(args.mirna, args.sensor, args.payload, p)

    k_tr = p['k_translate']; g_m = p['gamma_mRNA']; g_g = p['gamma_GFP']
    t_pk = np.log(g_m / g_g) / (g_m - g_g)
    free_peak = args.payload * k_tr / (g_g - g_m) * (
        np.exp(-g_m * t_pk) - np.exp(-g_g * t_pk))

    eff = r['peak_sfgfp'] / free_peak * 100 if free_peak > 0 else 0

    print(f'Results:')
    print(f'  Peak sfGFP:      {r["peak_sfgfp"]:,.0f} molecules')
    print(f'  Peak L7Ae:       {r["peak_l7ae"]:,.0f} molecules')
    print(f'  Free payload:    {free_peak:,.0f} molecules (reference)')
    print(f'  Circuit efficiency: {eff:.1f}% of free payload')
    print(f'  KD (L7Ae-Kturn): {p["Kd_L7Ae_molecules"]:.0f} molecules')
    print(f'  L7Ae vs KD:      {"ABOVE (repressed)" if r["peak_l7ae"] > p["Kd_L7Ae_molecules"] else "BELOW (derepressed)"}')


def cmd_optimize(args):
    """Find optimal sensor:payload ratio."""
    p = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
    opt = CircuitOptimizer(p)

    profiles = DEFAULT_CELL_PROFILES.copy()

    print(f'Optimizing sensor:payload ratio')
    print(f'  Total mRNA: {args.total_ng}ng')
    print(f'  Objective: {args.objective}')
    print(f'  Cell lines: {", ".join(profiles.keys())}')
    print()

    result = opt.optimize_ratio(
        args.total_ng, profiles,
        objective=args.objective,
        n_cells=args.n_cells,
    )

    print(opt.format_report(result))

    # Practical recommendation
    b = result['best']
    print()
    print('EXPERIMENTAL RECOMMENDATION:')
    print(f'  Mix {b["sensor_ng"]:.0f}ng sensor (p069B) + '
          f'{b["payload_ng"]:.0f}ng payload (p065) per well')
    print(f'  Expected: {b["on_pct"]:.1f}% ON, '
          f'{b["off_pct"]:.2f}% OFF, {b["ratio"]:.1f}x selectivity')


def cmd_design(args):
    """Generate a validation experiment plan."""
    p = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
    designer = ExperimentDesigner(p)

    profiles = DEFAULT_CELL_PROFILES.copy()

    sensor_list = [float(x) for x in args.sensor_range.split(',')]

    design = designer.design_titration(
        profiles,
        payload_ng=args.payload_ng,
        sensor_ng_list=sensor_list,
        replicates=args.replicates,
    )

    print(designer.format_experiment_plan(design))

    if args.output:
        # Save plate map as CSV
        with open(args.output, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['well', 'condition',
                                                     'replicate', 'type'])
            writer.writeheader()
            for row in design['plate_map']:
                writer.writerow(row)
        print(f'\nPlate map saved to: {args.output}')


def cmd_calibrate(args):
    """Calibrate model from experimental CSV."""
    p = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
    calibrator = ModelCalibrator(p)

    profiles = DEFAULT_CELL_PROFILES.copy()

    # Read CSV
    data = []
    with open(args.csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'cell_type': row['cell_type'],
                'sensor_ng': float(row['sensor_ng']),
                'payload_ng': float(row['payload_ng']),
                'observed_pct': float(row['observed_pct']),
            })

    print(f'Loaded {len(data)} observations from {args.csv}')
    print('Running calibration...')

    fit_params = args.fit_params.split(',')
    result = calibrator.calibrate(data, profiles, fit_params=fit_params)

    print(calibrator.format_calibration_report(result))

    if args.save_params:
        calibrator.save_params(result['fitted_params'], args.save_params)
        print(f'\nFitted parameters saved to: {args.save_params}')


def cmd_benchmark(args):
    """Run benchmark against experimental data."""
    # Import and run the benchmark test
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))
    from test_benchmark import (test_single_cell_dose_response,
                                 test_sensor_alone, test_dose_robustness)

    test_single_cell_dose_response()
    test_sensor_alone()
    test_dose_robustness()
    print('\nBenchmark complete.')


def cmd_sweep(args):
    """Sweep miR-122 dose-response curve."""
    p = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
    model = ANDGateModel(p)

    k_tr = p['k_translate']; g_m = p['gamma_mRNA']; g_g = p['gamma_GFP']
    t_pk = np.log(g_m / g_g) / (g_m - g_g)
    sfgfp_per_copy = k_tr / (g_g - g_m) * (
        np.exp(-g_m * t_pk) - np.exp(-g_g * t_pk))
    free_peak = args.payload * sfgfp_per_copy

    mirna_range = np.logspace(2, 5, 30)
    if args.include_zero:
        mirna_range = np.concatenate([[0], mirna_range])

    print(f'miR-122 dose-response (sensor={args.sensor}, payload={args.payload})')
    print()
    print(f'{"miR-122":>10s} {"sfGFP":>12s} {"efficiency":>10s} {"L7Ae_peak":>10s}')
    print('-' * 46)

    for m in mirna_range:
        r = model.simulate(m, args.sensor, args.payload, p)
        sfgfp = r['trajectories']['sfGFP'][-1]
        eff = sfgfp / free_peak * 100
        print(f'{m:10,.0f} {sfgfp:12,.0f} {eff:9.1f}% {r["peak_l7ae"]:10,.0f}')


def main():
    parser = argparse.ArgumentParser(
        description='RNA Logic Gate Circuit Modeling Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest='command', help='Command to run')

    # simulate
    p_sim = sub.add_parser('simulate', help='Run AND gate simulation')
    p_sim.add_argument('--mirna', type=float, default=50000,
                       help='miR-122 copies per cell (default: 50000)')
    p_sim.add_argument('--sensor', type=float, default=2000,
                       help='Sensor mRNA copies (default: 2000)')
    p_sim.add_argument('--payload', type=float, default=2000,
                       help='Payload mRNA copies (default: 2000)')
    p_sim.add_argument('--hours', type=float, default=24,
                       help='Simulation time in hours (default: 24)')

    # optimize
    p_opt = sub.add_parser('optimize', help='Optimize sensor:payload ratio')
    p_opt.add_argument('--total-ng', type=float, default=200,
                       help='Total mRNA per well in ng (default: 200)')
    p_opt.add_argument('--objective', choices=['selectivity', 'activation',
                       'balanced'], default='balanced',
                       help='Optimization objective (default: balanced)')
    p_opt.add_argument('--n-cells', type=int, default=20000,
                       help='Simulated cells per condition (default: 20000)')

    # design
    p_des = sub.add_parser('design', help='Design validation experiment')
    p_des.add_argument('--payload-ng', type=float, default=150,
                       help='Fixed payload mRNA per well (default: 150)')
    p_des.add_argument('--sensor-range', type=str, default='0,10,25,50,100,150',
                       help='Sensor amounts to test, comma-separated (ng)')
    p_des.add_argument('--replicates', type=int, default=3,
                       help='Replicates per condition (default: 3)')
    p_des.add_argument('--output', type=str, default=None,
                       help='Save plate map to CSV file')

    # calibrate
    p_cal = sub.add_parser('calibrate', help='Calibrate model from CSV')
    p_cal.add_argument('--csv', type=str, required=True,
                       help='CSV with columns: cell_type, sensor_ng, '
                            'payload_ng, observed_pct')
    p_cal.add_argument('--fit-params', type=str, default='mirna_mean,mirna_cv',
                       help='Parameters to fit, comma-separated')
    p_cal.add_argument('--save-params', type=str, default=None,
                       help='Save fitted parameters to JSON file')

    # benchmark
    p_bench = sub.add_parser('benchmark', help='Run benchmark tests')

    # sweep
    p_sweep = sub.add_parser('sweep', help='miR-122 dose-response sweep')
    p_sweep.add_argument('--sensor', type=float, default=2000)
    p_sweep.add_argument('--payload', type=float, default=2000)
    p_sweep.add_argument('--include-zero', action='store_true',
                         help='Include miR-122=0 in sweep')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        print('\nQuick start:')
        print('  python run.py simulate              # Basic AND gate simulation')
        print('  python run.py optimize               # Find best S:P ratio')
        print('  python run.py design                 # Generate experiment plan')
        print('  python run.py sweep --include-zero   # miR-122 dose-response')
        return

    commands = {
        'simulate': cmd_simulate,
        'optimize': cmd_optimize,
        'design': cmd_design,
        'calibrate': cmd_calibrate,
        'benchmark': cmd_benchmark,
        'sweep': cmd_sweep,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
