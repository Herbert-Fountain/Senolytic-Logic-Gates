"""
Data export utilities for simulation results.

Exports ODE trajectories, optimization sweeps, and population
distributions as CSV files for external analysis or plotting.
"""

import csv
import os
import numpy as np


def export_trajectory(sim_result, filepath):
    """Export ODE time-course trajectories as CSV.

    Parameters
    ----------
    sim_result : dict
        Output from ANDGateModel.simulate()
    filepath : str
        Output CSV path

    Writes CSV with columns: time_hr, M_sensor_free, M_sensor_bound,
    RISC, L7Ae, M_payload_free, M_payload_repr, sfGFP, L7Ae_bound
    """
    t = sim_result['t']
    traj = sim_result['trajectories']
    names = sim_result['species_names']

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time_hr'] + names)
        for i in range(len(t)):
            row = [f'{t[i]:.4f}'] + [f'{traj[n][i]:.2f}' for n in names]
            writer.writerow(row)


def export_optimization_sweep(opt_result, filepath):
    """Export optimization sweep results as CSV.

    Parameters
    ----------
    opt_result : dict
        Output from CircuitOptimizer.optimize_ratio()
    filepath : str
    """
    sweep = opt_result['sweep']
    if not sweep:
        return

    fields = ['sp_ratio', 'sensor_ng', 'payload_ng', 'on_pct',
              'off_pct', 'ratio', 'score']

    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for r in sweep:
            writer.writerow({k: f'{v:.4f}' if isinstance(v, float) else v
                             for k, v in r.items() if k in fields})


def export_dose_response(sweep_data, filepath):
    """Export miR-122 dose-response sweep as CSV.

    Parameters
    ----------
    sweep_data : list of dict
        Output from api.sweep_mirna()
    filepath : str
    """
    if not sweep_data:
        return

    fields = list(sweep_data[0].keys())
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sweep_data)


def export_population_distribution(sfgfp_values, filepath,
                                     label='sfGFP_molecules'):
    """Export population sfGFP distribution as CSV.

    Parameters
    ----------
    sfgfp_values : array
        sfGFP per cell for all cells in population
    filepath : str
    label : str
        Column header
    """
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['cell_index', label])
        for i, v in enumerate(sfgfp_values):
            writer.writerow([i, f'{v:.2f}'])
