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
# Sidebar: Navigation and Help
# ================================================================
st.sidebar.title('RNA Circuit Modeling Tool')
page = st.sidebar.radio('Navigate', [
    'Simulate',
    'Optimize Ratio',
    'Design Experiment',
    'Protocol Designer',
    'Enter Results',
    'Calibrate Model',
    'Sensitivity Analysis',
    'Experiment History',
])

st.sidebar.markdown('---')

with st.sidebar.expander('How this circuit works'):
    st.markdown('''
**The L7Ae/K-turn AND Gate** is a two-mRNA system:

**Sensor mRNA** encodes L7Ae protein (a translational repressor).
It has a miRNA binding site in its leader sequence.

**Payload mRNA** encodes your gene of interest (sfGFP, DTA, etc).
It has K-turn motifs in its leader sequence that L7Ae binds to.

**In cells WITHOUT the miRNA** (off-target):
- Sensor translates freely, L7Ae protein builds up
- L7Ae binds K-turns on payload, blocks its translation
- Result: payload is OFF

**In cells WITH the miRNA** (target):
- miRNA silences the sensor mRNA
- No L7Ae is made, so payload translates freely
- Result: payload is ON
''')

st.sidebar.markdown('**Current Cell Lines**')
for name, params in history.data['parameters']['cell_lines'].items():
    mirna = params.get('mirna_mean', 0)
    te = params.get('transfection_efficiency', 0)
    st.sidebar.text(f'{name}: miRNA={mirna:,.0f}, TE={te:.0%}')

if not history.data['parameters']['cell_lines']:
    st.sidebar.info('No cell lines configured. Go to Experiment History to add them.')


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
    st.title('Single-Cell Circuit Simulation')
    st.markdown('''
    Simulate what happens inside **one cell** after transfection with the
    AND gate circuit. Adjust the sliders to see how miRNA levels, mRNA doses,
    and repression strength affect sfGFP output in real time.
    ''')

    with st.expander('What do these parameters mean?'):
        st.markdown('''
- **miRNA copies/cell**: How many copies of the cognate miRNA (e.g., miR-122)
  are present. High = sensor gets silenced = payload turns ON.
  Set to 0 for off-target cells.
- **Sensor mRNA copies**: Number of sensor (L7Ae-encoding) mRNA molecules
  delivered to this cell. This is the "brake" on the circuit.
- **Payload mRNA copies**: Number of payload (sfGFP-encoding) mRNA molecules
  delivered. This is what you want to express in target cells.
- **Simulation time**: How many hours to simulate after transfection.
- **L7Ae repression fold**: How strongly L7Ae blocks payload translation when
  bound. 1000 = near-complete block (calibrated value). Lower values = leakier.
        ''')

    col1, col2 = st.columns(2)
    with col1:
        mirna = st.slider('miRNA copies/cell', 0, 200000, 50000, 1000,
                           help='0 = off-target cell; 50,000 = typical target')
        sensor = st.slider('Sensor mRNA copies', 0, 10000, 2000, 100,
                            help='Encodes L7Ae repressor protein')
        payload = st.slider('Payload mRNA copies', 0, 10000, 2000, 100,
                             help='Encodes sfGFP (or therapeutic payload)')
    with col2:
        hours = st.slider('Simulation time (hours)', 6, 72, 24)
        fold = st.slider('L7Ae repression fold', 10, 5000, 1000, 10,
                          help='1000 = near-complete translational block')

    # Run simulation automatically when sliders change (no button needed)
    p = get_params(L7Ae_repression_fold=fold, t_max_hr=hours)
    model = ANDGateModel(p)
    r = model.simulate(mirna, sensor, payload, p)

    k_tr = p['k_translate']; g_m = p['gamma_mRNA']; g_g = p['gamma_GFP']
    t_pk = np.log(g_m / g_g) / (g_m - g_g)
    sfgfp_per_copy = k_tr / (g_g - g_m) * (
        np.exp(-g_m * t_pk) - np.exp(-g_g * t_pk))
    free_peak = payload * sfgfp_per_copy
    eff = r['peak_sfgfp'] / free_peak * 100 if free_peak > 0 else 0

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Peak sfGFP', f'{r["peak_sfgfp"]:,.0f}',
              help='Maximum sfGFP protein molecules in this cell')
    c2.metric('Peak L7Ae', f'{r["peak_l7ae"]:,.0f}',
              help='Maximum L7Ae repressor molecules produced')
    c3.metric('Circuit Efficiency', f'{eff:.1f}%',
              help='sfGFP as % of what free payload would produce')
    kd = p['Kd_L7Ae_molecules']
    state = 'REPRESSED' if r['peak_l7ae'] > kd else 'ACTIVE'
    c4.metric('Payload Status', state,
              help=f'L7Ae {"exceeds" if state == "REPRESSED" else "is below"} '
                   f'the binding threshold (KD = {kd:,.0f} molecules)')

    # Interpretation
    if state == 'REPRESSED':
        st.warning(
            f'**Interpretation:** L7Ae peak ({r["peak_l7ae"]:,.0f}) exceeds the '
            f'K-turn binding threshold (KD = {kd:,.0f}), so the payload is '
            f'**repressed**. Only {eff:.1f}% of maximum sfGFP is produced. '
            f'This is the expected behavior in an **off-target cell** '
            f'(no miRNA to silence the sensor).')
    else:
        st.success(
            f'**Interpretation:** L7Ae peak ({r["peak_l7ae"]:,.0f}) is below the '
            f'K-turn binding threshold (KD = {kd:,.0f}), so the payload is '
            f'**active**. {eff:.1f}% of maximum sfGFP is produced. '
            f'The miRNA successfully silenced the sensor, allowing payload '
            f'expression. This is the expected behavior in a **target cell**.')

    # Time course plots
    t = r['t']
    traj = r['trajectories']

    st.subheader('sfGFP Accumulation Over Time')
    chart_data = pd.DataFrame({
        'Time (h)': t,
        'sfGFP (with circuit)': traj['sfGFP'],
        'sfGFP (free payload, no circuit)': [
            k_tr * payload / (g_g - g_m) * (
                np.exp(-g_m * ti) - np.exp(-g_g * ti))
            for ti in t],
    })
    st.line_chart(chart_data, x='Time (h)')
    st.caption(
        'The dashed-style line shows how much sfGFP the payload mRNA would '
        'produce WITHOUT any circuit (no L7Ae repression). The gap between '
        'the two lines shows how much the circuit is suppressing expression.')

    st.subheader('L7Ae Repressor and Payload mRNA State')
    chart2 = pd.DataFrame({
        'Time (h)': t,
        'L7Ae protein (free)': traj['L7Ae'],
        'Payload mRNA (translatable)': traj['M_payload_free'],
        'Payload mRNA (repressed by L7Ae)': traj['M_payload_repr'],
    })
    st.line_chart(chart2, x='Time (h)')
    st.caption(
        'Shows the competition between L7Ae binding and payload translation. '
        'When L7Ae is high, most payload mRNA is in the "repressed" state. '
        'As L7Ae decays (or is never produced), payload mRNA becomes translatable.')

    # Export trajectory
    with st.expander('Export simulation data'):
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
    st.markdown('''
    Find the best ratio of sensor mRNA to payload mRNA for your experiment.
    The sensor acts as a "brake" on the circuit. Too much sensor wastes payload
    capacity; too little may not fully repress off-target cells.
    ''')

    with st.expander('What do the optimization objectives mean?'):
        st.markdown('''
- **Balanced** (recommended): Maximizes both the number of ON cells AND the
  ON:OFF selectivity ratio. Good general-purpose starting point.
- **Selectivity**: Maximizes the ON:OFF ratio (how many fold more ON cells
  than OFF cells). May sacrifice some ON-cell activation.
- **Activation**: Maximizes the % of ON cells that are positive. Ignores
  OFF-cell leakage. Use when you want the brightest possible signal.
        ''')

    profiles = get_cell_profiles()
    cell_names = list(profiles.keys())

    col1, col2 = st.columns(2)
    with col1:
        total_ng = st.number_input('Total mRNA per well (ng)', 50, 500, 200,
            help='Total sensor + payload mRNA. Split between the two.')
        objective = st.selectbox('Optimization objective', [
            'balanced', 'selectivity', 'activation'])
        cells_per_well = st.number_input(
            'Cells seeded per well', 1000, 200000, 30000, 1000,
            help='More cells = less mRNA per cell. Standard 96-well: 30,000')
    with col2:
        on_cell = st.selectbox(
            'ON cell (target; has the miRNA)', cell_names,
            index=len(cell_names)-1,
            help='Cell type where payload should be expressed')
        off_cell = st.selectbox(
            'OFF cell (off-target; lacks miRNA)', cell_names, index=0,
            help='Cell type where payload should be silenced')

    copies_per_ng_val = 20 * (30000 / cells_per_well)
    st.caption(
        f'At {cells_per_well:,} cells/well, each cell receives about '
        f'{copies_per_ng_val:.0f} mRNA copies per ng of mRNA added '
        f'({total_ng * copies_per_ng_val:,.0f} total copies at {total_ng}ng).')

    if st.button('Run Optimization', type='primary'):
        p = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
        opt = CircuitOptimizer(p)

        use_profiles = {
            off_cell: profiles[off_cell],
            on_cell: profiles[on_cell],
        }

        with st.spinner('Sweeping sensor:payload ratios (about 1 minute)...'):
            result = opt.optimize_ratio(
                total_ng, use_profiles, objective=objective,
                cells_per_well=cells_per_well, n_cells=15000)

        # Results table
        rows = []
        for r in result['sweep']:
            rows.append({
                'SP Ratio': f'{r["sp_ratio"]:.2f}',
                'Sensor (ng)': f'{r["sensor_ng"]:.0f}',
                'Payload (ng)': f'{r["payload_ng"]:.0f}',
                f'{on_cell} sfGFP+ %': f'{r["on_pct"]:.1f}',
                f'{off_cell} sfGFP+ %': f'{r["off_pct"]:.2f}',
                'ON:OFF Ratio': f'{r["ratio"]:.1f}x',
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
        st.caption(
            '**SP Ratio** = sensor ng / payload ng. '
            f'**{on_cell} sfGFP+ %** = predicted fraction of {on_cell} cells '
            f'expressing sfGFP (want this HIGH). '
            f'**{off_cell} sfGFP+ %** = predicted off-target leakage '
            f'(want this LOW). '
            '**ON:OFF Ratio** = selectivity (higher is better).')

        # Highlight best
        b = result['best']
        st.success(
            f'**Recommended: {b["sensor_ng"]:.0f}ng sensor + '
            f'{b["payload_ng"]:.0f}ng payload per well** '
            f'(S:P = {b["sp_ratio"]}:1)')

        # Interpretation
        current_1to1 = next(
            (r for r in result['sweep'] if r['sp_ratio'] == 1.0), None)
        if current_1to1 and b['sp_ratio'] != 1.0:
            improvement = b['ratio'] / max(current_1to1['ratio'], 0.1)
            st.info(
                f'**Compared to the standard 1:1 ratio:** '
                f'Switching to {b["sp_ratio"]}:1 would increase '
                f'{on_cell} activation from {current_1to1["on_pct"]:.0f}% to '
                f'{b["on_pct"]:.0f}% and improve selectivity from '
                f'{current_1to1["ratio"]:.0f}x to {b["ratio"]:.0f}x '
                f'({improvement:.1f}-fold improvement). '
                f'This works because even a small amount of sensor produces '
                f'enough L7Ae to fully repress off-target cells.')

        # Chart
        sp_vals = [r['sp_ratio'] for r in result['sweep']]
        on_vals = [r['on_pct'] for r in result['sweep']]
        off_vals = [r['off_pct'] for r in result['sweep']]

        chart_df = pd.DataFrame({
            'SP Ratio': sp_vals,
            f'{on_cell} % positive': on_vals,
            f'{off_cell} % positive': off_vals,
        })
        st.subheader('Predicted Activation vs Sensor:Payload Ratio')
        st.line_chart(chart_df, x='SP Ratio')
        st.caption(
            'As the sensor:payload ratio increases (more sensor, less payload), '
            f'{on_cell} activation drops because excess sensor creates an L7Ae '
            f'burst that partially represses the payload even when miRNA is present. '
            f'{off_cell} leakage stays low across all ratios because even minimal '
            f'sensor produces enough L7Ae for complete repression.')

        # Export
        with st.expander('Export results'):
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                sweep_csv = pd.DataFrame([{
                    'sp_ratio': r['sp_ratio'],
                    'sensor_ng': r['sensor_ng'],
                    'payload_ng': r['payload_ng'],
                    'on_pct': r['on_pct'],
                    'off_pct': r['off_pct'],
                    'ratio': r['ratio'],
                } for r in result['sweep']])
                st.download_button('Download sweep CSV',
                    sweep_csv.to_csv(index=False),
                    'optimization_sweep.csv', 'text/csv')
            with col_e2:
                from modeling.core.autoprotocol import AutoProtocolExporter
                exporter = AutoProtocolExporter()
                proto = exporter.from_optimization_result(
                    result, use_profiles,
                    cells_per_well=cells_per_well)
                st.download_button('Download AutoProtocol JSON',
                    exporter.to_json(proto),
                    'optimized_protocol.json', 'application/json',
                    help='Load this in the Transfection AutoProtocol tool '
                         'to get plate layout and master mix volumes')


# ================================================================
# PAGE: Design Experiment
# ================================================================
elif page == 'Design Experiment':
    st.title('Design a Validation Experiment')
    st.markdown('''
    Generate a complete experiment plan with plate layout, controls, and
    **quantitative predictions for every condition**. After running the
    experiment, compare your results to the predictions to validate the model.
    ''')

    with st.expander('How to use this page'):
        st.markdown('''
1. Set the **payload mRNA amount** (fixed across all conditions)
2. Enter the **sensor amounts to test** (the model will predict results for each)
3. Choose your **cell lines** and **number of replicates**
4. Click "Generate" to see predictions, controls, and materials needed
5. **Download the AutoProtocol JSON** to auto-populate your transfection protocol
        ''')

    profiles = get_cell_profiles()

    col1, col2 = st.columns(2)
    with col1:
        payload_ng = st.number_input(
            'Payload mRNA per well (ng)', 10, 500, 150,
            help='Amount of payload (sfGFP/DTA) mRNA in every well')
        sensor_input = st.text_input(
            'Sensor amounts to test (ng, comma-separated)',
            '0, 10, 25, 50, 100, 150',
            help='Different sensor doses to test. 0 = payload-only control.')
    with col2:
        replicates = st.number_input('Replicates per condition', 1, 6, 3)
        cell_selection = st.multiselect(
            'Cell lines to test', list(profiles.keys()),
            default=list(profiles.keys()))
        design_cells_per_well = st.number_input(
            'Cells per well', 1000, 200000, 30000, 1000,
            key='design_cpw',
            help='Seeding density. Affects mRNA copies per cell.')

    if st.button('Generate Experiment Plan', type='primary'):
        sensor_list = [float(x.strip()) for x in sensor_input.split(',')]
        use_profiles = {k: v for k, v in profiles.items()
                        if k in cell_selection}

        p = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
        designer = ExperimentDesigner(p)

        with st.spinner('Computing predictions for all conditions...'):
            design = designer.design_titration(
                use_profiles, payload_ng=payload_ng,
                sensor_ng_list=sensor_list, replicates=replicates,
                total_cells_per_well=design_cells_per_well)

        # Predictions
        st.subheader('Model Predictions')
        st.markdown(
            'These are the predicted Live sfGFP+ percentages for each condition. '
            'After running the experiment, compare your flow cytometry results '
            'to these predictions.')
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
        st.markdown(
            'These controls are essential for interpreting your results and '
            'calibrating the model.')
        for ctrl in design['controls']:
            st.markdown(
                f'- **{ctrl["label"]}** - {ctrl["purpose"]}. '
                f'Expected result: {ctrl["expected"]}')

        # Materials
        st.subheader('Materials Summary')
        st.markdown(
            f'- **{design["n_wells"]} wells** needed '
            f'({replicates} replicates per condition)\n'
            f'- Payload mRNA: {payload_ng}ng per well\n'
            f'- Sensor mRNA amounts: {sensor_list} ng per well\n'
            f'- Cells: {design_cells_per_well:,} per well')

        # Export
        st.subheader('Export')
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            plan_text = designer.format_experiment_plan(design)
            st.download_button(
                'Download Experiment Plan (text)', plan_text,
                file_name='experiment_plan.txt', mime='text/plain')
        with col_exp2:
            from modeling.core.autoprotocol import AutoProtocolExporter
            exporter = AutoProtocolExporter()
            protocol_state = exporter.from_experiment_design(
                design, cells_per_well=design_cells_per_well)
            st.download_button(
                'Download AutoProtocol JSON',
                exporter.to_json(protocol_state),
                file_name='autoprotocol_experiment.json',
                mime='application/json',
                help='Open the Transfection AutoProtocol HTML tool, click '
                     '"Load Protocol", and select this file. Plate layout, '
                     'mRNA groups, and volumes will be pre-filled.')


# ================================================================
# PAGE: Protocol Designer
# ================================================================
elif page == 'Protocol Designer':
    from modeling.core.parameters import get_params as get_params_fn
    from modeling.protocol_page import render_protocol_page
    render_protocol_page(history, get_cell_profiles)


# ================================================================
# PAGE: Enter Results
# ================================================================
elif page == 'Enter Results':
    st.title('Enter Experimental Results')
    st.markdown('''
    After running your experiment, enter the flow cytometry results here.
    The data is saved to the experiment database and used to improve
    the model when you run calibration.
    ''')

    exp_name = st.text_input('Experiment name',
                              'ON Switch Titration',
                              help='A descriptive name for this experiment')
    exp_date = st.date_input('Experiment date')

    # File upload
    st.subheader('Option 1: Upload NovoExpress CSV')
    st.markdown(
        'Upload the **Summary Table** CSV exported from NovoExpress. '
        'The tool will automatically extract Live sfGFP+ percentages, '
        'identify cell types and mRNA doses from specimen names, and '
        'compute mean and standard deviation across replicates.')

    uploaded_file = st.file_uploader(
        'Drop your Summary Table CSV here',
        type=['csv'],
        help='The CSV file exported from NovoExpress with specimen statistics. '
             'Must contain columns: Specimen, Live Count, '
             'Live sfGFP Positive Count.')

    if uploaded_file is not None:
        from modeling.core.flow_parser import FlowDataParser
        import tempfile

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
                st.warning(f'Parser warning: {w}')

        st.success(
            f'Successfully parsed {parse_result["n_specimens"]} specimen groups '
            f'into {parse_result["n_observations"]} conditions.')

        summary_rows = []
        for s in parse_result['specimen_summary']:
            summary_rows.append({
                'Cell Type': s['cell_type'],
                'Condition': s['condition'],
                'Sensor (ng)': s['sensor_ng'],
                'Payload (ng)': s['payload_ng'],
                'Mean sfGFP+ %': f'{s["mean_pct"]:.1f}',
                'Std Dev': f'{s["std_pct"]:.1f}',
                'Replicates': s['n'],
            })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)
        st.caption(
            'Verify that cell types and mRNA doses were correctly parsed '
            'from specimen names. If any are wrong, use Option 2 (manual entry) '
            'instead.')

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
                f'with {len(circuit_obs)} conditions. '
                f'Go to **Calibrate Model** to fit the model to this data.')

    st.markdown('---')
    st.subheader('Option 2: Enter data manually')
    st.markdown(
        'Type your results directly. Enter one row per condition. '
        '**cell_type** is the cell line name, **sensor_ng** and **payload_ng** '
        'are the mRNA amounts per well, and **observed_pct** is the '
        'Live sfGFP+ percentage from flow cytometry.')

    profiles = get_cell_profiles()
    cell_names = list(profiles.keys())

    n_rows = st.number_input('Number of conditions', 1, 50, 8)

    default_data = []
    sensor_defaults = [10, 25, 50, 100] * 2
    cell_defaults = ([cell_names[0]] * 4 + [cell_names[-1]] * 4
                     if len(cell_names) >= 2 else [cell_names[0]] * 8)

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
                f'with {len(conditions)} conditions. '
                f'Go to **Calibrate Model** to fit the model to this data.')


# ================================================================
# PAGE: Calibrate Model
# ================================================================
elif page == 'Calibrate Model':
    st.title('Calibrate Model from Experimental Data')
    st.markdown('''
    Adjust the model's internal parameters to match your actual experimental
    results. The model fits against **all selected experiments simultaneously**,
    so it gets more accurate as you add more data.
    ''')

    with st.expander('What parameters can be calibrated?'):
        st.markdown('''
- **mirna_mean**: Average number of functionally active miRNA copies per cell
  in the ON (target) cell type. This is often lower than bulk RNA-seq estimates
  because only RISC-loaded miRNA participates in sensor silencing.
- **mirna_cv**: Cell-to-cell variability in miRNA expression (coefficient of
  variation). Higher CV = more heterogeneous = broader sfGFP distribution.
- **circuit_failure_rate**: Fraction of cells where the circuit fails
  stochastically (sensor never produces enough L7Ae). Accounts for
  translational bursting and endosomal escape variability.
- **expression_ratio**: How much more protein the ON cell produces per mRNA
  compared to the OFF cell. Reflects differences in ribosome availability,
  cell size, and translational machinery.
- **L7Ae_repression_fold**: How strongly L7Ae blocks translation when bound to
  the K-turn. 1000 = near-complete block. Usually does not need fitting.
        ''')

    if not history.data['experiments']:
        st.warning(
            'No experiments recorded yet. Go to **Enter Results** to add '
            'your flow cytometry data first.')
    else:
        st.subheader('Available Experiments')
        for i, exp in enumerate(history.data['experiments']):
            st.markdown(
                f'- **{exp["name"]}** '
                f'({exp["n_conditions"]} conditions, '
                f'{exp.get("metadata", {}).get("date", "no date")})')

        exp_indices = st.multiselect(
            'Experiments to use for calibration',
            range(len(history.data['experiments'])),
            default=list(range(len(history.data['experiments']))),
            format_func=lambda i: history.data['experiments'][i]['name'],
            help='Select all experiments you want the model to fit simultaneously')

        fit_options = {
            'mirna_mean': 'miRNA copies (functional, RISC-loaded)',
            'mirna_cv': 'miRNA cell-to-cell variability',
            'circuit_failure_rate': 'Stochastic circuit failure rate',
            'expression_ratio': 'ON/OFF cell expression efficiency ratio',
            'L7Ae_repression_fold': 'L7Ae translational repression strength',
        }
        fit_params = st.multiselect(
            'Parameters to adjust',
            list(fit_options.keys()),
            default=['mirna_mean', 'mirna_cv'],
            format_func=lambda k: f'{k} ({fit_options[k]})',
            help='Start with mirna_mean and mirna_cv. Add more if the fit is poor.')

        if st.button('Run Calibration', type='primary'):
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
                        f'Fitting model to {len(exp_data)} observations '
                        f'(this may take 1-2 minutes)...'):
                    result = calibrator.calibrate(
                        exp_data, profiles, fit_params=fit_params)

                st.subheader('How Parameters Changed')
                for param, (old, new) in result['changed_params'].items():
                    pct = (new - old) / old * 100 if old != 0 else 0
                    direction = 'increased' if pct > 0 else 'decreased'
                    st.markdown(
                        f'- **{param}** ({fit_options.get(param, "")}): '
                        f'{old:.4g} &rarr; {new:.4g} '
                        f'({direction} {abs(pct):.1f}%)')

                st.subheader('Model Predictions vs Your Data')
                comp_rows = []
                for c in result['comparison']:
                    comp_rows.append({
                        'Condition': c['condition'],
                        'Your Result': f'{c["observed"]:.1f}%',
                        'Model Prediction': f'{c["predicted_after"]:.1f}%',
                        'Difference': f'{c["residual"]:+.1f}%',
                    })
                st.dataframe(pd.DataFrame(comp_rows),
                             use_container_width=True)

                err_before = result['total_error_before']
                err_after = result['total_error_after']
                reduction = ((err_before - err_after) /
                             max(err_before, 0.01) * 100)

                st.metric('Prediction Error (lower is better)',
                          f'{err_after:.1f}',
                          f'{-reduction:.0f}% improvement')

                if err_after < 10:
                    st.success(
                        'Excellent fit. Model predictions match your data '
                        'within a few percent.')
                elif err_after < 50:
                    st.info(
                        'Good fit. Consider adding more calibration parameters '
                        'if you want higher accuracy.')
                else:
                    st.warning(
                        'Moderate fit. Try adding circuit_failure_rate or '
                        'expression_ratio to the fitted parameters.')

                if st.button('Accept and Save Updated Parameters'):
                    fitted = result['fitted_params']
                    on_cell = max(profiles.keys(),
                                  key=lambda c: profiles[c].get('mirna_mean', 0))
                    history.set_cell_line_params(on_cell, {
                        'mirna_mean': fitted.get('mirna_mean',
                            profiles[on_cell]['mirna_mean']),
                        'mirna_cv': fitted.get('mirna_cv',
                            profiles[on_cell]['mirna_cv']),
                    })
                    history.record_calibration(
                        exp_indices, result['initial_params'], fitted,
                        result['comparison'], fit_params,
                        err_before, err_after)
                    st.success(
                        'Parameters saved. Future predictions will use '
                        'the updated values.')
                    st.rerun()


# ================================================================
# PAGE: Sensitivity Analysis
# ================================================================
elif page == 'Sensitivity Analysis':
    st.title('Parameter Sensitivity Analysis')
    st.markdown('''
    Find out which parameters have the biggest impact on circuit performance.
    Each parameter is varied +/- 50% while all others stay constant, and
    the effect on ON:OFF selectivity and circuit efficiency is measured.
    ''')

    with st.expander('How to interpret sensitivity values'):
        st.markdown('''
A **sensitivity index** of 1.0 means a 50% change in the parameter causes
a 50% change in the output (proportional). Values above 1.0 mean the output
is **more sensitive** than the input change (amplified). Values below 1.0
mean the output is **buffered** against changes in that parameter.

The parameters are sorted by their impact on the ON:OFF selectivity ratio,
which is usually the most important metric for circuit design.
        ''')

    col1, col2 = st.columns(2)
    with col1:
        sa_mirna_on = st.number_input(
            'ON cell miRNA copies', 0, 200000, 50000, key='sa_mirna',
            help='miRNA copies in the target cell (where payload should be ON)')
        sa_sensor = st.number_input(
            'Sensor mRNA copies', 100, 10000, 2000, key='sa_sensor',
            help='Sensor (L7Ae) mRNA delivered per cell')
    with col2:
        sa_mirna_off = st.number_input(
            'OFF cell miRNA copies', 0, 200000, 0, key='sa_mirna_off',
            help='miRNA copies in the off-target cell (usually 0)')
        sa_payload = st.number_input(
            'Payload mRNA copies', 100, 10000, 2000, key='sa_payload',
            help='Payload (sfGFP) mRNA delivered per cell')

    if st.button('Run Sensitivity Analysis', type='primary'):
        from modeling.core.sensitivity import SensitivityAnalyzer
        analyzer = SensitivityAnalyzer()

        with st.spinner('Varying each parameter...'):
            results = analyzer.one_at_a_time(
                {}, {},
                mirna_on=sa_mirna_on, mirna_off=sa_mirna_off,
                sensor=sa_sensor, payload=sa_payload)

        rows = []
        for param, data in sorted(results.items(),
                key=lambda x: max(
                    abs(x[1].get('sensitivity_on_off_ratio', 0)),
                    abs(x[1].get('sensitivity_circuit_efficiency', 0))),
                reverse=True):
            rows.append({
                'Parameter': param,
                'Impact on ON:OFF Ratio': f'{data.get("sensitivity_on_off_ratio", 0):.2f}',
                'Impact on Efficiency': f'{data.get("sensitivity_circuit_efficiency", 0):.2f}',
                'Impact on sfGFP': f'{data.get("sensitivity_peak_sfgfp", 0):.2f}',
                'Low Value': f'{data["values"][0]:.4g}',
                'Baseline': f'{data["values"][1]:.4g}',
                'High Value': f'{data["values"][2]:.4g}',
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        # Interpretation
        top_param = rows[0]['Parameter'] if rows else 'unknown'
        top_impact = rows[0]['Impact on ON:OFF Ratio'] if rows else '0'
        st.info(
            f'**Most impactful parameter: {top_param}** '
            f'(sensitivity = {top_impact}). '
            f'This parameter has the strongest effect on ON:OFF selectivity. '
            f'Focus experimental optimization efforts here first.')

        with st.expander('Full text report'):
            st.code(analyzer.format_report(results))


# ================================================================
# PAGE: Experiment History
# ================================================================
elif page == 'Experiment History':
    st.title('Experiment History and Cell Line Settings')
    st.markdown('''
    View all recorded experiments, manage cell line parameters, and track
    how the model has improved over calibration rounds.
    ''')

    st.subheader('Database Summary')
    st.code(history.summary())

    # Cell line editor
    st.subheader('Cell Line Parameters')
    st.markdown('''
    These parameters describe each cell line. They are used by the simulator,
    optimizer, and experiment designer. Calibration updates them automatically,
    but you can also edit them manually.
    ''')

    with st.expander('What do these parameters mean?'):
        st.markdown('''
- **miRNA mean**: Average copies of the cognate miRNA per cell. Determines
  how effectively the sensor mRNA is silenced. Set to 0 for cells that
  lack the miRNA entirely.
- **miRNA CV**: Coefficient of variation (standard deviation / mean) for
  miRNA expression across cells in the population. Higher = more
  heterogeneous. Typical range: 0.3 to 2.0.
- **Transfection Efficiency (TE)**: Fraction of cells that receive any mRNA
  during transfection (0 to 1). Measured from your positive control:
  TE = (sfGFP+ %) / (fraction above threshold among transfected cells).
- **Expression Factor**: Relative protein production per mRNA copy compared
  to the reference cell line. HuH7 makes ~5.5x more sfGFP per mRNA than 4T1.
  Set to 1.0 for the reference cell line.
        ''')

    profiles = get_cell_profiles()
    for name in list(profiles.keys()):
        with st.expander(f'{name}'):
            params = profiles[name]
            col1, col2 = st.columns(2)
            with col1:
                new_mirna = st.number_input(
                    f'miRNA mean (copies/cell)', 0, 500000,
                    int(params['mirna_mean']), key=f'mirna_{name}',
                    help='Functional miRNA copies (RISC-loaded)')
                new_cv = st.number_input(
                    f'miRNA CV (variability)', 0.1, 5.0,
                    float(params['mirna_cv']), 0.1, key=f'cv_{name}',
                    help='Cell-to-cell coefficient of variation')
            with col2:
                new_te = st.number_input(
                    f'Transfection Efficiency', 0.01, 1.0,
                    float(params['transfection_efficiency']), 0.01,
                    key=f'te_{name}',
                    help='Fraction of cells that receive mRNA (0 to 1)')
                new_expr = st.number_input(
                    f'Expression Factor', 0.1, 20.0,
                    float(params['expression_factor']), 0.1,
                    key=f'expr_{name}',
                    help='Protein per mRNA relative to reference (1.0 = reference)')

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
    new_name = st.text_input('Cell line name (e.g., WI-38, IMR-90, HEK293)')
    if new_name and st.button('Add Cell Line'):
        history.set_cell_line_params(new_name, {
            'mirna_mean': 0,
            'mirna_cv': 0.5,
            'transfection_efficiency': 0.5,
            'expression_factor': 1.0,
            'notes': 'New cell line; set parameters above then calibrate',
        })
        st.success(
            f'Added {new_name}. Set its parameters in the expander above, '
            f'then run a calibration experiment to refine them.')
        st.rerun()

    # Calibration history
    if history.data['calibrations']:
        st.subheader('Calibration History')
        st.markdown(
            'Each round shows how the model was adjusted to better match '
            'experimental data.')
        for i, cal in enumerate(history.data['calibrations']):
            with st.expander(
                    f'Round {i+1}: {cal["timestamp"][:10]} '
                    f'(error: {cal["error_before"]:.1f} &rarr; '
                    f'{cal["error_after"]:.1f}, '
                    f'{cal.get("error_reduction", 0):.0f}% better)'):
                st.json(cal['params_after'])

    # Export
    with st.expander('Export data'):
        if st.button('Export all observations as CSV'):
            export_path = os.path.join(
                os.path.dirname(DB_PATH), 'all_observations.csv')
            history.export_observations_csv(export_path)
            st.success(f'Exported to {export_path}')
