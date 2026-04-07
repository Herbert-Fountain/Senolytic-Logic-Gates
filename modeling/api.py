"""
Machine-readable API for AI tool-use.

Provides a JSON-in, JSON-out interface that any AI with code execution
can call. Also serves as a function-calling schema for LLM tool-use
protocols (MCP, OpenAI function calling, etc.).

Usage by an AI:
    import json
    from modeling.api import call

    # Simulate a circuit
    result = call('simulate', {
        'mirna_copies': 50000,
        'sensor_copies': 2000,
        'payload_copies': 2000,
    })
    print(json.dumps(result, indent=2))

    # Get available functions
    schema = call('list_functions', {})

    # Optimize dosing
    result = call('optimize', {
        'total_mRNA_ng': 200,
        'objective': 'balanced',
        'on_cell': {'mirna_mean': 8000, 'transfection_efficiency': 0.94},
        'off_cell': {'mirna_mean': 0, 'transfection_efficiency': 0.31},
    })
"""

import sys
import os
import json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modeling.core import (
    ANDGateModel, CircuitOptimizer, ExperimentDesigner,
    ModelCalibrator, ExperimentHistory, get_params
)
from modeling.core.bridge import CircuitBridge


# ================================================================
# Function Registry
# ================================================================

FUNCTIONS = {}


def register(name, description, parameters, returns):
    """Register a function in the API."""
    def decorator(func):
        FUNCTIONS[name] = {
            'function': func,
            'description': description,
            'parameters': parameters,
            'returns': returns,
        }
        return func
    return decorator


# ================================================================
# API Functions
# ================================================================

@register(
    name='list_functions',
    description='List all available API functions with their schemas.',
    parameters={},
    returns='dict: {function_name: {description, parameters, returns}}'
)
def list_functions(params):
    return {name: {k: v for k, v in info.items() if k != 'function'}
            for name, info in FUNCTIONS.items()}


@register(
    name='simulate',
    description=(
        'Run a single-cell AND gate simulation. Returns peak sfGFP, '
        'L7Ae levels, circuit efficiency, and time-course data.'),
    parameters={
        'mirna_copies': 'float: miR-122 copies per cell (0 for OFF cell)',
        'sensor_copies': 'float: sensor mRNA copies (default: 2000)',
        'payload_copies': 'float: payload mRNA copies (default: 2000)',
        'hours': 'float: simulation duration in hours (default: 24)',
        'repression_fold': 'float: L7Ae repression fold (default: 1000)',
    },
    returns=(
        'dict: {peak_sfgfp, peak_l7ae, circuit_efficiency_pct, '
        'free_payload_peak, l7ae_vs_kd, timepoints (first/last 5)}')
)
def simulate(params):
    mirna = params.get('mirna_copies', 50000)
    sensor = params.get('sensor_copies', 2000)
    payload = params.get('payload_copies', 2000)
    hours = params.get('hours', 24)
    fold = params.get('repression_fold', 1000)

    p = get_params(L7Ae_repression_fold=fold, t_max_hr=hours)
    model = ANDGateModel(p)
    r = model.simulate(mirna, sensor, payload, p)

    k_tr = p['k_translate']; g_m = p['gamma_mRNA']; g_g = p['gamma_GFP']
    t_pk = np.log(g_m / g_g) / (g_m - g_g)
    sfgfp_per_copy = k_tr / (g_g - g_m) * (
        np.exp(-g_m * t_pk) - np.exp(-g_g * t_pk))
    free_peak = payload * sfgfp_per_copy
    eff = r['peak_sfgfp'] / free_peak * 100 if free_peak > 0 else 0

    return {
        'peak_sfgfp': round(r['peak_sfgfp'], 1),
        'peak_l7ae': round(r['peak_l7ae'], 1),
        'circuit_efficiency_pct': round(eff, 2),
        'free_payload_peak': round(free_peak, 1),
        'l7ae_vs_kd': 'ABOVE_repressed' if r['peak_l7ae'] > p['Kd_L7Ae_molecules'] else 'BELOW_active',
        'kd_molecules': round(p['Kd_L7Ae_molecules'], 0),
        'sfgfp_at_endpoint': round(r['trajectories']['sfGFP'][-1], 1),
    }


@register(
    name='optimize',
    description=(
        'Find the optimal sensor:payload mRNA ratio for a given total dose. '
        'Returns a sweep of ratios with predicted ON%, OFF%, and selectivity.'),
    parameters={
        'total_mRNA_ng': 'float: total mRNA per well in ng (default: 200)',
        'objective': 'str: selectivity|activation|balanced (default: balanced)',
        'on_cell': 'dict: {mirna_mean, mirna_cv, transfection_efficiency, expression_factor}',
        'off_cell': 'dict: {mirna_mean, mirna_cv, transfection_efficiency, expression_factor}',
    },
    returns='dict: {best: {sp_ratio, sensor_ng, payload_ng, on_pct, off_pct, ratio}, sweep: [...]}'
)
def optimize(params):
    total = params.get('total_mRNA_ng', 200)
    objective = params.get('objective', 'balanced')

    on_cell = params.get('on_cell', {
        'mirna_mean': 8000, 'mirna_cv': 0.5,
        'transfection_efficiency': 0.94, 'expression_factor': 5.5,
    })
    off_cell = params.get('off_cell', {
        'mirna_mean': 0, 'mirna_cv': 0.5,
        'transfection_efficiency': 0.31, 'expression_factor': 1.0,
    })

    profiles = {'OFF_cell': off_cell, 'ON_cell': on_cell}

    p = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
    opt = CircuitOptimizer(p)
    result = opt.optimize_ratio(total, profiles, objective=objective,
                                 n_cells=10000)

    # Simplify for JSON
    sweep = [{
        'sp_ratio': r['sp_ratio'],
        'sensor_ng': round(r['sensor_ng'], 1),
        'payload_ng': round(r['payload_ng'], 1),
        'on_pct': round(r['on_pct'], 1),
        'off_pct': round(r['off_pct'], 2),
        'ratio': round(r['ratio'], 1),
    } for r in result['sweep']]

    b = result['best']
    return {
        'best': {
            'sp_ratio': b['sp_ratio'],
            'sensor_ng': round(b['sensor_ng'], 1),
            'payload_ng': round(b['payload_ng'], 1),
            'on_pct': round(b['on_pct'], 1),
            'off_pct': round(b['off_pct'], 2),
            'ratio': round(b['ratio'], 1),
        },
        'sweep': sweep,
        'objective': objective,
    }


@register(
    name='evaluate_mirna',
    description=(
        'Evaluate a miRNA as an AND gate circuit input. Takes CPM values '
        'and returns predicted circuit performance with optimal dosing.'),
    parameters={
        'mirna_name': 'str: miRNA name (e.g., miR-34a-5p)',
        'target_cpm': 'float: CPM in target cell type',
        'control_cpm': 'float: CPM in control cell type',
        'switch_type': 'str: ON or OFF (default: ON)',
        'total_mRNA_ng': 'float: total mRNA per well (default: 200)',
        'target_te': 'float: target cell transfection efficiency (default: 0.5)',
        'control_te': 'float: control cell transfection efficiency (default: 0.5)',
    },
    returns='dict: {mirna, selectivity, optimal_dosing, target_pct, control_pct}'
)
def evaluate_mirna(params):
    bridge = CircuitBridge()

    mirna_data = {
        params.get('mirna_name', 'miRNA'): {
            'target_cpm': params.get('target_cpm', 100),
            'control_cpm': params.get('control_cpm', 10),
            'type': params.get('switch_type', 'ON'),
            'fc': params.get('target_cpm', 100) / max(params.get('control_cpm', 10), 1),
        }
    }

    results = bridge.evaluate_mirna_candidates(
        mirna_data,
        target_cell='target',
        control_cell='control',
        target_te=params.get('target_te', 0.5),
        control_te=params.get('control_te', 0.5),
        total_mRNA_ng=params.get('total_mRNA_ng', 200),
    )

    if results:
        r = results[0]
        return {
            'mirna': r['mirna'],
            'switch_type': r['switch_type'],
            'fold_change': round(r['fold_change'], 2),
            'target_copies_per_cell': round(r['target_copies'], 0),
            'control_copies_per_cell': round(r['control_copies'], 0),
            'selectivity_1to1': round(r['model_selectivity_1to1'], 1),
            'selectivity_optimal': round(r['model_selectivity_optimal'], 1),
            'optimal_sensor_ng': round(r['optimal_sensor_ng'], 0),
            'optimal_payload_ng': round(r['optimal_payload_ng'], 0),
            'target_pct': round(r['target_pct_optimal'], 1),
            'control_pct': round(r['control_pct_optimal'], 2),
        }
    return {'error': 'No results'}


@register(
    name='sweep_mirna',
    description=(
        'Sweep miR-122 dose-response: sfGFP output vs miRNA copies. '
        'Useful for understanding the circuit transfer function.'),
    parameters={
        'sensor_copies': 'float: sensor mRNA copies (default: 2000)',
        'payload_copies': 'float: payload mRNA copies (default: 2000)',
        'mirna_range': 'list of float: miRNA values to test (optional)',
    },
    returns='list of {mirna_copies, sfgfp, efficiency_pct, l7ae_peak}'
)
def sweep_mirna(params):
    sensor = params.get('sensor_copies', 2000)
    payload = params.get('payload_copies', 2000)
    mirna_range = params.get('mirna_range', None)

    if mirna_range is None:
        mirna_range = [0] + list(np.logspace(2, 5, 20).astype(int))

    p = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
    model = ANDGateModel(p)

    k_tr = p['k_translate']; g_m = p['gamma_mRNA']; g_g = p['gamma_GFP']
    t_pk = np.log(g_m / g_g) / (g_m - g_g)
    sfgfp_per_copy = k_tr / (g_g - g_m) * (
        np.exp(-g_m * t_pk) - np.exp(-g_g * t_pk))
    free_peak = payload * sfgfp_per_copy

    results = []
    for m in mirna_range:
        r = model.simulate(m, sensor, payload, p)
        sfgfp = r['trajectories']['sfGFP'][-1]
        results.append({
            'mirna_copies': int(m),
            'sfgfp': round(sfgfp, 0),
            'efficiency_pct': round(sfgfp / free_peak * 100, 2),
            'l7ae_peak': round(r['peak_l7ae'], 0),
        })

    return results


@register(
    name='get_parameters',
    description='Get current model parameters with descriptions.',
    parameters={},
    returns='dict: all kinetic parameters with values and units'
)
def get_parameters(params):
    p = get_params()
    return {k: v for k, v in p.items() if isinstance(v, (int, float, str))}


@register(
    name='get_experiment_history',
    description='Get summary of all recorded experiments and calibrations.',
    parameters={},
    returns='str: formatted summary of experiment database'
)
def get_experiment_history(params):
    history = ExperimentHistory()
    return {'summary': history.summary()}


# ================================================================
# Main API Entry Point
# ================================================================

def call(function_name, params=None):
    """Call an API function by name with parameters.

    Parameters
    ----------
    function_name : str
        Name of the function to call (see list_functions)
    params : dict, optional
        Function parameters

    Returns
    -------
    dict : function result (JSON-serializable)
    """
    if function_name not in FUNCTIONS:
        return {
            'error': f'Unknown function: {function_name}',
            'available': list(FUNCTIONS.keys()),
        }

    try:
        result = FUNCTIONS[function_name]['function'](params or {})
        return {'status': 'ok', 'result': result}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}


def get_schema():
    """Get the complete API schema for AI tool-use registration.

    Returns a schema compatible with function-calling protocols.
    """
    schema = {
        'name': 'rna_circuit_modeling_tool',
        'description': (
            'Simulates and optimizes mRNA-based logic gate circuits '
            'using the L7Ae/K-turn translational repression system. '
            'Predicts circuit performance in flow cytometry assays, '
            'finds optimal mRNA dosing ratios, designs validation '
            'experiments, and calibrates from experimental results.'),
        'functions': {},
    }

    for name, info in FUNCTIONS.items():
        schema['functions'][name] = {
            'description': info['description'],
            'parameters': info['parameters'],
            'returns': info['returns'],
        }

    return schema


# ================================================================
# CLI for testing
# ================================================================

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: python api.py <function_name> [json_params]')
        print()
        print('Available functions:')
        for name, info in FUNCTIONS.items():
            print(f'  {name}: {info["description"][:60]}...')
        sys.exit(0)

    func_name = sys.argv[1]
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    result = call(func_name, params)
    print(json.dumps(result, indent=2, default=str))
