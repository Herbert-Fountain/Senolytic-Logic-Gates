"""
RNA Logic Gate Circuit Modeling Tool - Interactive Web Interface

Launch with:
    streamlit run modeling/app.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import os
import sys
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modeling.core import (
    ANDGateModel, CircuitOptimizer, ExperimentDesigner,
    ModelCalibrator, get_params
)
from modeling.core.history import ExperimentHistory

# ================================================================
# Page Configuration
# ================================================================
st.set_page_config(
    page_title='RNA Circuit Modeling Tool',
    page_icon='🧬',
    layout='wide',
)

# ================================================================
# Initialize persistent state
# ================================================================
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'data', 'history.json')

@st.cache_resource
def get_history():
    return ExperimentHistory(DB_PATH)

history = get_history()

# ================================================================
# Sidebar: Navigation
# ================================================================
st.sidebar.title('RNA Circuit Modeling Tool')
page = st.sidebar.radio('Navigate', [
    'Simulate',
    'Optimize Ratio',
    'Design Experiment',
    'Enter Results',
    'Calibrate Model',
    'Sensitivity Analysis',
    'Experiment History',
])

st.sidebar.markdown('---')
st.sidebar.markdown('**Current Cell Lines**')
for name, params in history.data['parameters']['cell_lines'].items():
    mirna = params.get('mirna_mean', 0)
    te = params.get('transfection_efficiency', 0)
    st.sidebar.text(f'{name}: miRNA={mirna:,.0f}, TE={te:.0%}')

if not history.data['parameters']['cell_lines']:
    st.sidebar.info('No cell lines configured. Add them below.')


# ================================================================
# Helper: get or create cell profiles
# ================================================================
def get_cell_profiles():
    """Get cell profiles from history, or use defaults."""
    profiles = history.get_cell_profiles()
    if not profiles:
        profiles = {
            '4T1': {
                'mirna_mean': 0, 'mirna_cv': 0.5,
                'transfection_efficiency': 0.31,
                'expression_factor': 1.0,
            },
            'HuH7': {
                'mirna_mean': 8000, 'mirna_cv': 0.5,
                'transfection_efficiency': 0.94,
                'expression_factor': 5.5,
            },
        }
        for name, params in profiles.items():
            history.set_cell_line_params(name, params)
    return profiles


# ================================================================
# PAGE: Simulate
# ================================================================
if page == 'Simulate':
    st.title('AND Gate Circuit Simulation')
    st.markdown('Simulate the L7Ae/K-turn AND gate for a single cell.')

    col1, col2 = st.columns(2)
    with col1:
        mirna = st.slider('miR-122 copies/cell', 0, 200000, 50000, 1000)
        sensor = st.slider('Sensor mRNA copies', 0, 10000, 2000, 100)
        payload = st.slider('Payload mRNA copies', 0, 10000, 2000, 100)
    with col2:
        hours = st.slider('Simulation time (hours)', 6, 72, 24)
        fold = st.slider('L7Ae repression fold', 10, 5000, 1000, 10)

    if st.button('Run Simulation', type='primary'):
        p = get_params(L7Ae_repression_fold=fold, t_max_hr=hours)
        model = ANDGateModel(p)

        with st.spinner('Running ODE solver...'):
            r = model.simulate(mirna, sensor, payload, p)

        k_tr = p['k_translate']; g_m = p['gamma_mRNA']; g_g = p['gamma_GFP']
        t_pk = np.log(g_m / g_g) / (g_m - g_g)
        sfgfp_per_copy = k_tr / (g_g - g_m) * (
            np.exp(-g_m * t_pk) - np.exp(-g_g * t_pk))
        free_peak = payload * sfgfp_per_copy
        eff = r['peak_sfgfp'] / free_peak * 100 if free_peak > 0 else 0

        # Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric('Peak sfGFP', f'{r["peak_sfgfp"]:,.0f}')
        c2.metric('Peak L7Ae', f'{r["peak_l7ae"]:,.0f}')
        c3.metric('Circuit Efficiency', f'{eff:.1f}%')
        kd = p['Kd_L7Ae_molecules']
        c4.metric('L7Ae vs KD',
                   'REPRESSED' if r['peak_l7ae'] > kd else 'ACTIVE')

        # Time course plots
        t = r['t']
        traj = r['trajectories']

        # sfGFP trajectory
        st.subheader('sfGFP Accumulation')
        chart_data = pd.DataFrame({
            'Time (h)': t,
            'sfGFP (circuit)': traj['sfGFP'],
            'sfGFP (free payload)': [
                k_tr * payload / (g_g - g_m) * (
                    np.exp(-g_m * ti) - np.exp(-g_g * ti))
                for ti in t],
        })
        st.line_chart(chart_data, x='Time (h)')

        # L7Ae and payload state
        st.subheader('L7Ae Protein and Payload mRNA State')
        chart2 = pd.DataFrame({
            'Time (h)': t,
            'L7Ae (free)': traj['L7Ae'],
            'Payload (free)': traj['M_payload_free'],
            'Payload (repressed)': traj['M_payload_repr'],
        })
        st.line_chart(chart2, x='Time (h)')

        # Export trajectory
        st.subheader('Export Data')
        traj_df = pd.DataFrame({'time_hr': t})
        for name in r['species_names']:
            traj_df[name] = traj[name]
        st.download_button(
            'Download trajectory CSV',
            traj_df.to_csv(index=False),
            file_name='trajectory.csv',
            mime='text/csv')


# ================================================================
# PAGE: Optimize Ratio
# ================================================================
elif page == 'Optimize Ratio':
    st.title('Sensor:Payload Ratio Optimization')
    st.markdown('Find the optimal mRNA ratio to maximize circuit performance.')

    profiles = get_cell_profiles()
    cell_names = list(profiles.keys())

    col1, col2 = st.columns(2)
    with col1:
        total_ng = st.number_input('Total mRNA per well (ng)', 50, 500, 200)
        objective = st.selectbox('Optimization objective', [
            'balanced', 'selectivity', 'activation'])
        cells_per_well = st.number_input(
            'Cells seeded per well', 1000, 200000, 30000, 1000,
            help='Affects mRNA copies per cell. Standard: 30,000 (96-well)')
    with col2:
        on_cell = st.selectbox('ON cell (has miRNA)', cell_names,
                                index=len(cell_names)-1)
        off_cell = st.selectbox('OFF cell (lacks miRNA)', cell_names,
                                 index=0)

    copies_per_ng_val = 20 * (30000 / cells_per_well)
    st.caption(f'At {cells_per_well:,} cells/well: {copies_per_ng_val:.1f} '
               f'copies/ng/cell ({total_ng * copies_per_ng_val:.0f} total '
               f'copies at {total_ng}ng)')

    if st.button('Run Optimization', type='primary'):
        p = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
        opt = CircuitOptimizer(p)

        use_profiles = {
            off_cell: profiles[off_cell],
            on_cell: profiles[on_cell],
        }

        with st.spinner('Running optimization sweep (this takes ~1 min)...'):
            result = opt.optimize_ratio(
                total_ng, use_profiles, objective=objective,
                cells_per_well=cells_per_well, n_cells=15000)

        # Results table
        rows = []
        for r in result['sweep']:
            rows.append({
                'S:P Ratio': f'{r["sp_ratio"]:.2f}',
                'Sensor (ng)': f'{r["sensor_ng"]:.0f}',
                'Payload (ng)': f'{r["payload_ng"]:.0f}',
                f'{on_cell} %': f'{r["on_pct"]:.1f}',
                f'{off_cell} %': f'{r["off_pct"]:.2f}',
                'ON:OFF': f'{r["ratio"]:.1f}x',
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)

        # Highlight best
        b = result['best']
        st.success(
            f'**Optimal: {b["sensor_ng"]:.0f}ng sensor + '
            f'{b["payload_ng"]:.0f}ng payload** '
            f'(S:P = {b["sp_ratio"]}:1) | '
            f'{on_cell}: {b["on_pct"]:.1f}% | '
            f'{off_cell}: {b["off_pct"]:.2f}% | '
            f'Ratio: {b["ratio"]:.1f}x')

        # Chart
        sp_vals = [r['sp_ratio'] for r in result['sweep']]
        on_vals = [r['on_pct'] for r in result['sweep']]
        off_vals = [r['off_pct'] for r in result['sweep']]
        ratio_vals = [r['ratio'] for r in result['sweep']]

        chart_df = pd.DataFrame({
            'S:P Ratio': sp_vals,
            f'{on_cell} % positive': on_vals,
            f'{off_cell} % positive': off_vals,
        })
        st.subheader('Activation vs Sensor:Payload Ratio')
        st.line_chart(chart_df, x='S:P Ratio')

        # Export
        st.subheader('Export')
        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            sweep_csv = pd.DataFrame([{
                'sp_ratio': r['sp_ratio'],
                'sensor_ng': r['sensor_ng'],
                'payload_ng': r['payload_ng'],
                'on_pct': r['on_pct'],
                'off_pct': r['off_pct'],
                'ratio': r['ratio'],
            } for r in result['sweep']])
            st.download_button('Download sweep CSV', sweep_csv.to_csv(index=False),
                               'optimization_sweep.csv', 'text/csv')
        with col_e2:
            from modeling.core.autoprotocol import AutoProtocolExporter
            exporter = AutoProtocolExporter()
            proto = exporter.from_optimization_result(
                result, use_profiles,
                cells_per_well=cells_per_well)
            st.download_button('Download AutoProtocol JSON',
                               exporter.to_json(proto),
                               'optimized_protocol.json',
                               'application/json',
                               help='Load in Transfection AutoProtocol')


# ================================================================
# PAGE: Design Experiment
# ================================================================
elif page == 'Design Experiment':
    st.title('Design Validation Experiment')
    st.markdown(
        'Generate a plate layout with controls and predictions. '
        'The model tells you what to expect before you run the experiment.')

    profiles = get_cell_profiles()

    col1, col2 = st.columns(2)
    with col1:
        payload_ng = st.number_input('Payload mRNA per well (ng)',
                                      10, 500, 150)
        sensor_input = st.text_input(
            'Sensor amounts to test (ng, comma-separated)',
            '0, 10, 25, 50, 100, 150')
    with col2:
        replicates = st.number_input('Replicates', 1, 6, 3)
        cell_selection = st.multiselect(
            'Cell lines', list(profiles.keys()),
            default=list(profiles.keys()))
        design_cells_per_well = st.number_input(
            'Cells per well', 1000, 200000, 30000, 1000,
            key='design_cpw')

    if st.button('Generate Experiment Plan', type='primary'):
        sensor_list = [float(x.strip()) for x in sensor_input.split(',')]

        use_profiles = {k: v for k, v in profiles.items()
                        if k in cell_selection}

        p = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
        designer = ExperimentDesigner(p)

        with st.spinner('Computing predictions...'):
            design = designer.design_titration(
                use_profiles, payload_ng=payload_ng,
                sensor_ng_list=sensor_list, replicates=replicates,
                total_cells_per_well=design_cells_per_well)

        # Show predictions
        st.subheader('Predicted Results')
        rows = []
        for cond in design['conditions']:
            if cond['sensor_ng'] > 0:
                pred = cond['predicted_pct']
                tol = max(pred * 0.3, 2.0)
                rows.append({
                    'Cell Type': cond['cell_type'],
                    'Sensor (ng)': cond['sensor_ng'],
                    'Payload (ng)': cond['payload_ng'],
                    'Predicted sfGFP+ %': f'{pred:.1f}',
                    'Expected Range': f'{max(pred-tol,0):.1f} - {min(pred+tol,100):.1f}%',
                })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        # Controls
        st.subheader('Required Controls')
        for ctrl in design['controls']:
            st.markdown(f'- **{ctrl["label"]}**: {ctrl["purpose"]}')

        # Materials summary
        st.subheader('Materials')
        n_wells = design['n_wells']
        st.markdown(f'- **{n_wells} wells** total ({replicates} replicates)')
        st.markdown(f'- Payload: {payload_ng}ng/well')
        st.markdown(f'- Sensor: {sensor_list} ng/well')

        # Export buttons
        st.subheader('Export')
        col_exp1, col_exp2 = st.columns(2)

        with col_exp1:
            # Experiment plan text
            plan_text = designer.format_experiment_plan(design)
            st.download_button(
                'Download Experiment Plan (text)',
                plan_text,
                file_name='experiment_plan.txt',
                mime='text/plain')

        with col_exp2:
            # AutoProtocol JSON export
            from modeling.core.autoprotocol import AutoProtocolExporter
            exporter = AutoProtocolExporter()
            protocol_state = exporter.from_experiment_design(
                design, cells_per_well=design_cells_per_well)
            protocol_json = exporter.to_json(protocol_state)
            st.download_button(
                'Download AutoProtocol JSON',
                protocol_json,
                file_name='autoprotocol_experiment.json',
                mime='application/json',
                help='Load this file in the Transfection AutoProtocol tool')

        with st.expander('Full Experiment Plan (text)'):
            st.code(plan_text)


# ================================================================
# PAGE: Enter Results
# ================================================================
elif page == 'Enter Results':
    st.title('Enter Experimental Results')
    st.markdown(
        'Record flow cytometry results. Upload your NovoExpress CSV '
        'directly or enter data manually. Saved for model calibration.')

    exp_name = st.text_input('Experiment name',
                              'ON Switch Titration')
    exp_date = st.date_input('Experiment date')

    # File upload option
    st.subheader('Option 1: Upload NovoExpress CSV')
    uploaded_file = st.file_uploader(
        'Upload your Summary Table CSV from NovoExpress',
        type=['csv'],
        help='The CSV exported from NovoExpress with specimen statistics.')

    if uploaded_file is not None:
        from modeling.core.flow_parser import FlowDataParser
        import tempfile

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv',
                                          delete=False, encoding='utf-8') as tmp:
            content = uploaded_file.read().decode('utf-8-sig')
            tmp.write(content)
            tmp_path = tmp.name

        parser = FlowDataParser()
        parse_result = parser.parse_novoexpress_csv(tmp_path)
        os.unlink(tmp_path)

        if parse_result['warnings']:
            for w in parse_result['warnings']:
                st.warning(w)

        st.success(
            f'Parsed {parse_result["n_specimens"]} specimens, '
            f'{parse_result["n_observations"]} conditions')

        # Show parsed data
        summary_rows = []
        for s in parse_result['specimen_summary']:
            summary_rows.append({
                'Cell Type': s['cell_type'],
                'Condition': s['condition'],
                'Sensor (ng)': s['sensor_ng'],
                'Payload (ng)': s['payload_ng'],
                'Mean sfGFP+ %': f'{s["mean_pct"]:.1f}',
                'SD': f'{s["std_pct"]:.1f}',
                'n': s['n'],
            })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)

        # Filter to circuit conditions for calibration
        circuit_obs = [o for o in parse_result['observations']
                       if o['observed_pct'] is not None]

        col1, col2 = st.columns(2)
        with col1:
            constructs = st.text_input('Constructs used',
                'p065 (2xKt-sfGFP) + p069B (5\'MRE-L7Ae)',
                key='upload_constructs')
        with col2:
            cytometer = st.text_input('Cytometer', 'NovoCyte Quanteon',
                key='upload_cytometer')

        if st.button('Save Uploaded Results', type='primary'):
            metadata = {
                'date': str(exp_date),
                'constructs': constructs,
                'cytometer': cytometer,
                'source_file': uploaded_file.name,
            }
            idx = history.add_experiment(exp_name, circuit_obs, metadata)
            st.success(
                f'Saved as experiment #{idx}: "{exp_name}" '
                f'with {len(circuit_obs)} conditions.')

    st.markdown('---')
    st.subheader('Option 2: Enter data manually')
    st.markdown('Add one row per condition (cell type + dose combination).')

    profiles = get_cell_profiles()
    cell_names = list(profiles.keys())

    # Editable dataframe for entering results
    n_rows = st.number_input('Number of conditions', 1, 50, 8)

    default_data = []
    sensor_defaults = [10, 25, 50, 100] * 2
    cell_defaults = [cell_names[0]] * 4 + [cell_names[-1]] * 4 if len(cell_names) >= 2 else [cell_names[0]] * 8

    for i in range(n_rows):
        default_data.append({
            'cell_type': cell_defaults[i] if i < len(cell_defaults) else cell_names[0],
            'sensor_ng': sensor_defaults[i] if i < len(sensor_defaults) else 50,
            'payload_ng': 150,
            'observed_pct': 0.0,
        })

    df = pd.DataFrame(default_data)
    edited_df = st.data_editor(df, num_rows='dynamic',
                                use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        constructs = st.text_input('Constructs used',
                                    'p065 (2xKt-sfGFP) + p069B (5\'MRE-L7Ae)')
    with col2:
        cytometer = st.text_input('Cytometer', 'NovoCyte Quanteon')

    if st.button('Save Experiment', type='primary'):
        conditions = edited_df.to_dict('records')

        # Validate
        valid = all(c.get('observed_pct', 0) >= 0 for c in conditions)
        if not valid:
            st.error('All observed_pct values must be >= 0')
        else:
            metadata = {
                'date': str(exp_date),
                'constructs': constructs,
                'cytometer': cytometer,
            }
            idx = history.add_experiment(exp_name, conditions, metadata)
            st.success(
                f'Experiment saved as #{idx}: "{exp_name}" '
                f'with {len(conditions)} conditions.')
            st.info('Go to "Calibrate Model" to fit the model to this data.')


# ================================================================
# PAGE: Calibrate Model
# ================================================================
elif page == 'Calibrate Model':
    st.title('Calibrate Model from Experimental Data')
    st.markdown(
        'Fit model parameters to your experimental results. '
        'Uses all saved experiments (cumulative learning).')

    if not history.data['experiments']:
        st.warning('No experiments recorded yet. Go to "Enter Results" first.')
    else:
        st.subheader('Available Experiments')
        for i, exp in enumerate(history.data['experiments']):
            st.markdown(
                f'- **[{i}] {exp["name"]}** '
                f'({exp["n_conditions"]} conditions, '
                f'{exp.get("metadata", {}).get("date", "no date")})')

        # Select which experiments to use
        exp_indices = st.multiselect(
            'Experiments to include in calibration',
            range(len(history.data['experiments'])),
            default=list(range(len(history.data['experiments']))),
            format_func=lambda i: f'[{i}] {history.data["experiments"][i]["name"]}')

        # Parameters to fit
        fit_options = ['mirna_mean', 'mirna_cv', 'circuit_failure_rate',
                       'expression_ratio', 'L7Ae_repression_fold']
        fit_params = st.multiselect(
            'Parameters to fit',
            fit_options,
            default=['mirna_mean', 'mirna_cv'])

        if st.button('Run Calibration', type='primary'):
            # Gather all observations from selected experiments
            all_obs = history.get_all_observations(experiment_idx=exp_indices)

            if not all_obs:
                st.error('No observations found in selected experiments.')
            else:
                profiles = get_cell_profiles()
                p = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
                calibrator = ModelCalibrator(p)

                exp_data = [{
                    'cell_type': obs['cell_type'],
                    'sensor_ng': obs['sensor_ng'],
                    'payload_ng': obs['payload_ng'],
                    'observed_pct': obs['observed_pct'],
                } for obs in all_obs]

                with st.spinner(
                        f'Calibrating against {len(exp_data)} observations '
                        f'from {len(exp_indices)} experiment(s)...'):
                    result = calibrator.calibrate(
                        exp_data, profiles, fit_params=fit_params)

                # Show results
                st.subheader('Parameter Changes')
                for param, (old, new) in result['changed_params'].items():
                    pct = (new - old) / old * 100 if old != 0 else 0
                    st.markdown(f'- **{param}**: {old:.4g} -> {new:.4g} '
                                f'({pct:+.1f}%)')

                st.subheader('Prediction vs Observation')
                comp_rows = []
                for c in result['comparison']:
                    comp_rows.append({
                        'Condition': c['condition'],
                        'Observed': f'{c["observed"]:.1f}%',
                        'Predicted (after)': f'{c["predicted_after"]:.1f}%',
                        'Residual': f'{c["residual"]:+.1f}%',
                    })
                st.dataframe(pd.DataFrame(comp_rows),
                             use_container_width=True)

                err_before = result['total_error_before']
                err_after = result['total_error_after']
                reduction = (err_before - err_after) / max(err_before, 0.01) * 100

                st.metric('Total Squared Error',
                          f'{err_after:.1f}',
                          f'{-reduction:.0f}% from {err_before:.1f}')

                # Save calibration
                if st.button('Accept and Save Updated Parameters'):
                    fitted = result['fitted_params']

                    # Update cell line parameters
                    on_cell = max(profiles.keys(),
                                  key=lambda c: profiles[c].get('mirna_mean', 0))
                    history.set_cell_line_params(on_cell, {
                        'mirna_mean': fitted.get('mirna_mean',
                            profiles[on_cell]['mirna_mean']),
                        'mirna_cv': fitted.get('mirna_cv',
                            profiles[on_cell]['mirna_cv']),
                    })

                    history.record_calibration(
                        exp_indices,
                        result['initial_params'],
                        fitted,
                        result['comparison'],
                        fit_params,
                        err_before, err_after)

                    st.success('Parameters updated and calibration recorded.')
                    st.rerun()


# ================================================================
# PAGE: Sensitivity Analysis
# ================================================================
elif page == 'Sensitivity Analysis':
    st.title('Parameter Sensitivity Analysis')
    st.markdown(
        'See which parameters have the most impact on circuit performance. '
        'Each parameter is varied +/- 50% while others are held constant.')

    col1, col2 = st.columns(2)
    with col1:
        sa_mirna_on = st.number_input('ON cell miR-122 copies', 0, 200000, 50000,
                                       key='sa_mirna')
        sa_sensor = st.number_input('Sensor copies', 100, 10000, 2000,
                                     key='sa_sensor')
    with col2:
        sa_mirna_off = st.number_input('OFF cell miR-122 copies', 0, 200000, 0,
                                        key='sa_mirna_off')
        sa_payload = st.number_input('Payload copies', 100, 10000, 2000,
                                      key='sa_payload')

    if st.button('Run Sensitivity Analysis', type='primary'):
        from modeling.core.sensitivity import SensitivityAnalyzer
        analyzer = SensitivityAnalyzer()

        with st.spinner('Running sensitivity sweep...'):
            results = analyzer.one_at_a_time(
                {}, {},
                mirna_on=sa_mirna_on, mirna_off=sa_mirna_off,
                sensor=sa_sensor, payload=sa_payload)

        # Display as table
        rows = []
        for param, data in sorted(results.items(),
                key=lambda x: max(abs(x[1].get('sensitivity_on_off_ratio', 0)),
                                  abs(x[1].get('sensitivity_circuit_efficiency', 0))),
                reverse=True):
            rows.append({
                'Parameter': param,
                'Sensitivity (ON:OFF)': f'{data.get("sensitivity_on_off_ratio", 0):.2f}',
                'Sensitivity (efficiency)': f'{data.get("sensitivity_circuit_efficiency", 0):.2f}',
                'Sensitivity (sfGFP)': f'{data.get("sensitivity_peak_sfgfp", 0):.2f}',
                'Low value': f'{data["values"][0]:.4g}',
                'Baseline': f'{data["values"][1]:.4g}',
                'High value': f'{data["values"][2]:.4g}',
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        st.info(
            'Sensitivity index = (% change in output) / (% change in input). '
            'Values > 1 mean the output is MORE sensitive than the input change. '
            'Sorted by impact on ON:OFF ratio.')

        with st.expander('Full report (text)'):
            st.code(analyzer.format_report(results))


# ================================================================
# PAGE: Experiment History
# ================================================================
elif page == 'Experiment History':
    st.title('Experiment History and Model Evolution')

    st.subheader('Database Summary')
    st.code(history.summary())

    # Cell line editor
    st.subheader('Cell Line Parameters')
    st.markdown('Edit cell line parameters directly.')

    profiles = get_cell_profiles()
    for name in list(profiles.keys()):
        with st.expander(f'{name}'):
            params = profiles[name]
            col1, col2 = st.columns(2)
            with col1:
                new_mirna = st.number_input(
                    f'{name} miRNA mean', 0, 500000,
                    int(params['mirna_mean']), key=f'mirna_{name}')
                new_cv = st.number_input(
                    f'{name} miRNA CV', 0.1, 5.0,
                    float(params['mirna_cv']), 0.1, key=f'cv_{name}')
            with col2:
                new_te = st.number_input(
                    f'{name} Transfection Eff', 0.01, 1.0,
                    float(params['transfection_efficiency']), 0.01,
                    key=f'te_{name}')
                new_expr = st.number_input(
                    f'{name} Expression Factor', 0.1, 20.0,
                    float(params['expression_factor']), 0.1,
                    key=f'expr_{name}')

            if st.button(f'Update {name}', key=f'update_{name}'):
                history.set_cell_line_params(name, {
                    'mirna_mean': new_mirna,
                    'mirna_cv': new_cv,
                    'transfection_efficiency': new_te,
                    'expression_factor': new_expr,
                })
                st.success(f'{name} parameters updated.')
                st.rerun()

    # Add new cell line
    st.subheader('Add New Cell Line')
    new_name = st.text_input('Cell line name')
    if new_name and st.button('Add Cell Line'):
        history.set_cell_line_params(new_name, {
            'mirna_mean': 0,
            'mirna_cv': 0.5,
            'transfection_efficiency': 0.5,
            'expression_factor': 1.0,
            'notes': 'Needs calibration',
        })
        st.success(f'Added {new_name}. Set parameters above.')
        st.rerun()

    # Calibration history
    if history.data['calibrations']:
        st.subheader('Calibration History')
        for i, cal in enumerate(history.data['calibrations']):
            with st.expander(
                    f'Round {i}: {cal["timestamp"][:10]} '
                    f'(error: {cal["error_before"]:.1f} -> '
                    f'{cal["error_after"]:.1f})'):
                st.json(cal['params_after'])

    # Export
    st.subheader('Export')
    if st.button('Export All Observations as CSV'):
        export_path = os.path.join(
            os.path.dirname(DB_PATH), 'all_observations.csv')
        history.export_observations_csv(export_path)
        st.success(f'Exported to {export_path}')
