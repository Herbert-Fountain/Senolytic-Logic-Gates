"""
Protocol Designer page for the Streamlit app.

Provides a complete transfection protocol interface integrated with
the circuit modeling tool. Import this and call render_protocol_page()
from the main app.
"""

import streamlit as st
import pandas as pd
import numpy as np


def render_protocol_page(history, get_cell_profiles):
    """Render the full Protocol Designer page."""
    from modeling.core.protocol import (
        compute_master_mixes, generate_protocol_steps,
        auto_assign_plate, get_well_name, ROWS, _fmt
    )

    st.title('Protocol Designer')
    st.markdown('''
    Design your transfection experiment from scratch or auto-populate from
    the optimizer. Generates plate layout, master mix volumes, and a
    step-by-step protocol you can follow at the bench.
    ''')

    # ============================================================
    # Initialize session state
    # ============================================================
    if 'proto_groups' not in st.session_state:
        st.session_state.proto_groups = [
            {'name': 'Positive Control', 'type': 'positive',
             'mRNAs': [{'name': 'sfGFP mRNA', 'conc': 500.0, 'dose': 100.0}]},
            {'name': 'Negative Control', 'type': 'negative', 'mRNAs': []},
            {'name': 'Payload Only (p065)', 'type': 'experimental',
             'mRNAs': [{'name': 'p065 (2xKt-sfGFP)', 'conc': 500.0, 'dose': 150.0}]},
            {'name': 'Circuit S=25ng + P=150ng', 'type': 'experimental',
             'mRNAs': [
                 {'name': 'p069B (L7Ae sensor)', 'conc': 500.0, 'dose': 25.0},
                 {'name': 'p065 (2xKt-sfGFP)', 'conc': 500.0, 'dose': 150.0},
             ]},
        ]
    if 'proto_cell_types' not in st.session_state:
        profiles = get_cell_profiles()
        st.session_state.proto_cell_types = [
            {'name': name, 'density': 30000}
            for name in profiles.keys()
        ]
    if 'proto_plate_mrna' not in st.session_state:
        st.session_state.proto_plate_mrna = [-1] * 96
        st.session_state.proto_plate_cells = [-1] * 96

    groups = st.session_state.proto_groups
    cell_types = st.session_state.proto_cell_types
    plate_mrna = st.session_state.proto_plate_mrna
    plate_cells = st.session_state.proto_plate_cells

    # ============================================================
    # Section 1: Protocol Settings
    # ============================================================
    with st.expander('Protocol Settings', expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            proto_title = st.text_input('Protocol title',
                'Circuit Validation Experiment', key='proto_title')
        with col2:
            lipo_per_well = st.selectbox(
                'Lipofectamine per well (uL)',
                [0.20, 0.30, 0.40, 0.50], index=1,
                help='Volume of Lipofectamine 2000 per well',
                key='proto_lipo')
        with col3:
            extra_pct = st.number_input(
                'Pipetting overage (%)', 0, 50, 10, 5,
                help='Extra volume to account for pipetting loss',
                key='proto_extra')

    # ============================================================
    # Section 2: mRNA Groups
    # ============================================================
    st.subheader('mRNA Groups')
    st.markdown(
        'Define each experimental condition. Each group is a unique '
        'combination of mRNAs at specific doses. Wells assigned to the '
        'same group receive the same transfection mix.')

    # Quick-add from optimizer
    with st.expander('Auto-populate from optimizer result'):
        st.markdown(
            'If you ran the **Optimize Ratio** page, you can generate '
            'groups automatically based on the recommended dosing.')
        profiles = get_cell_profiles()

        ap_payload = st.number_input('Payload dose (ng)', 10, 500, 150,
                                      key='ap_payload')
        ap_sensors = st.text_input('Sensor doses to test (ng, comma-separated)',
                                    '0, 25, 50, 100', key='ap_sensors')
        if st.button('Generate Groups'):
            sensor_list = [float(x.strip())
                           for x in ap_sensors.split(',')]
            new_groups = [
                {'name': 'Negative Control', 'type': 'negative', 'mRNAs': []},
            ]
            for s_ng in sensor_list:
                if s_ng == 0:
                    new_groups.append({
                        'name': f'Payload Only ({ap_payload}ng)',
                        'type': 'positive',
                        'mRNAs': [{'name': 'p065 (2xKt-sfGFP)',
                                   'conc': 500.0, 'dose': ap_payload}],
                    })
                else:
                    new_groups.append({
                        'name': f'S={s_ng:.0f}ng + P={ap_payload}ng',
                        'type': 'experimental',
                        'mRNAs': [
                            {'name': 'p069B (L7Ae sensor)',
                             'conc': 500.0, 'dose': s_ng},
                            {'name': 'p065 (2xKt-sfGFP)',
                             'conc': 500.0, 'dose': ap_payload},
                        ],
                    })
            st.session_state.proto_groups = new_groups
            groups = new_groups
            st.success(f'Generated {len(new_groups)} groups.')
            st.rerun()

    # Display and edit groups
    for gi, group in enumerate(groups):
        type_emoji = {'positive': '(+)', 'negative': '(-)',
                      'experimental': ''}
        label = f'{type_emoji.get(group["type"], "")} {group["name"]}'
        with st.expander(label, expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                new_name = st.text_input('Group name', group['name'],
                                          key=f'gn_{gi}')
                groups[gi]['name'] = new_name
            with col2:
                new_type = st.selectbox(
                    'Type', ['experimental', 'positive', 'negative'],
                    index=['experimental', 'positive', 'negative'].index(
                        group['type']),
                    key=f'gt_{gi}')
                groups[gi]['type'] = new_type

            if new_type != 'negative':
                st.markdown('**mRNAs in this group:**')
                for mi, mrna in enumerate(group.get('mRNAs', [])):
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1:
                        mrna['name'] = st.text_input(
                            'mRNA name', mrna['name'],
                            key=f'mn_{gi}_{mi}')
                    with c2:
                        mrna['conc'] = st.number_input(
                            'Conc (ng/uL)', 1.0, 5000.0, mrna['conc'],
                            key=f'mc_{gi}_{mi}')
                    with c3:
                        mrna['dose'] = st.number_input(
                            'Dose (ng/well)', 1.0, 1000.0, mrna['dose'],
                            key=f'md_{gi}_{mi}')

    # Add/remove groups
    col_add, col_rem = st.columns(2)
    with col_add:
        if st.button('+ Add Group'):
            groups.append({
                'name': f'Group {len(groups) + 1}',
                'type': 'experimental',
                'mRNAs': [{'name': 'mRNA', 'conc': 500.0, 'dose': 100.0}],
            })
            st.rerun()
    with col_rem:
        if len(groups) > 1 and st.button('- Remove Last Group'):
            groups.pop()
            st.rerun()

    # ============================================================
    # Section 3: Cell Types
    # ============================================================
    st.subheader('Cell Types')
    st.markdown(
        'Define the cell lines used in this experiment. Each cell type '
        'can have a different seeding density.')

    ct_cols = st.columns(max(len(cell_types), 1))
    for ci, ct in enumerate(cell_types):
        with ct_cols[ci % len(ct_cols)]:
            ct['name'] = st.text_input('Cell line', ct['name'],
                                        key=f'ct_name_{ci}')
            ct['density'] = st.number_input(
                'Cells/well', 1000, 200000,
                ct['density'], 1000, key=f'ct_dens_{ci}')

    col_ct_add, col_ct_rem = st.columns(2)
    with col_ct_add:
        if st.button('+ Add Cell Type'):
            cell_types.append({'name': 'New Cell Line', 'density': 30000})
            st.rerun()
    with col_ct_rem:
        if len(cell_types) > 1 and st.button('- Remove Last Cell Type'):
            cell_types.pop()
            st.rerun()

    # ============================================================
    # Section 4: Plate Layout
    # ============================================================
    st.subheader('Plate Layout')
    st.markdown(
        'Assign groups and cell types to wells. Use **Auto-assign** for '
        'a standard layout, or manually edit the assignment table.')

    replicates = st.number_input('Replicates per condition', 1, 8, 3,
                                  key='proto_reps')

    if st.button('Auto-assign plate layout', type='primary'):
        plate_mrna, plate_cells = auto_assign_plate(
            groups, cell_types, replicates)
        st.session_state.proto_plate_mrna = plate_mrna
        st.session_state.proto_plate_cells = plate_cells
        st.rerun()

    # Visualize plate as a grid
    n_assigned = sum(1 for v in plate_mrna if v >= 0)
    if n_assigned > 0:
        # Build plate visualization dataframe
        GROUP_COLORS = ['#5b8c78', '#c0884a', '#7b6ea6', '#c26e6e',
                        '#4a8fa8', '#a08c5a', '#8a6d9e', '#5a9a7a',
                        '#b07850', '#6888a8']

        # Create grid display
        grid_data = []
        for row_idx in range(8):
            row_dict = {'Row': ROWS[row_idx]}
            for col_idx in range(12):
                well_idx = row_idx * 12 + col_idx
                gi = plate_mrna[well_idx]
                ci = plate_cells[well_idx]

                if gi >= 0 and gi < len(groups):
                    cell_str = ''
                    if ci >= 0 and ci < len(cell_types):
                        cell_str = f' [{cell_types[ci]["name"]}]'
                    row_dict[str(col_idx + 1)] = f'{groups[gi]["name"][:15]}{cell_str}'
                else:
                    row_dict[str(col_idx + 1)] = ''
            grid_data.append(row_dict)

        plate_df = pd.DataFrame(grid_data)
        st.dataframe(plate_df, use_container_width=True, hide_index=True)

        # Legend
        st.markdown('**Legend:**')
        legend_parts = []
        for gi, g in enumerate(groups):
            well_count = sum(1 for v in plate_mrna if v == gi)
            if well_count > 0:
                legend_parts.append(f'**{g["name"]}** ({well_count} wells)')
        st.markdown(' | '.join(legend_parts))

        st.caption(f'{n_assigned} of 96 wells assigned.')
    else:
        st.info('No wells assigned yet. Click "Auto-assign plate layout" above.')

    # ============================================================
    # Section 5: Master Mix Volumes
    # ============================================================
    if n_assigned > 0:
        st.subheader('Master Mix Volumes')
        st.markdown(
            'Calculated volumes for each tube. Includes '
            f'{extra_pct}% pipetting overage.')

        mm = compute_master_mixes(groups, plate_mrna,
                                   lipo_per_well, extra_pct)

        if mm['lipo_mix']:
            lipo = mm['lipo_mix']

            # Shared Lipo Mix table
            st.markdown('**Shared Lipofectamine Mix (Tube A)**')
            lipo_df = pd.DataFrame([
                {'Component': 'Opti-MEM',
                 'Per Well': f'{_fmt(lipo["opti_per_well"])} uL',
                 'Master Mix': f'{_fmt(lipo["opti_total"])} uL'},
                {'Component': 'Lipofectamine 2000',
                 'Per Well': f'{_fmt(lipo["lipo_per_well"])} uL',
                 'Master Mix': f'{_fmt(lipo["lipo_total"])} uL'},
                {'Component': 'TOTAL',
                 'Per Well': f'{_fmt(5.0)} uL',
                 'Master Mix': f'{_fmt(lipo["tube_total"])} uL'},
            ])
            st.dataframe(lipo_df, use_container_width=True, hide_index=True)
            st.caption(
                f'Covers {lipo["n_wells"]} wells '
                f'(+ {extra_pct}% overage = {lipo["n_with_overage"]:.1f} '
                f'well-equivalents). Aliquot {_fmt(5.0)} uL per group tube '
                f'after combining.')

            # Per-group tables
            for g in mm['groups']:
                cotx = ' (co-transfection)' if g.get('is_cotransfection') else ''
                st.markdown(
                    f'**G{g["group_index"]+1}: {g["group_name"]}** '
                    f'({g["well_count"]} wells: {g["well_str"]}){cotx}')

                rows = []
                if g['is_negative']:
                    rows.append({
                        'Component': 'Opti-MEM (vehicle control, no mRNA)',
                        'Per Well': f'{_fmt(g["opti_per_well"])} uL',
                        'Master Mix': f'{_fmt(g["opti_total"])} uL',
                    })
                else:
                    for mv in g['mrna_volumes']:
                        rows.append({
                            'Component': f'{mv["name"]} ({mv["conc"]} ng/uL)',
                            'Per Well': f'{_fmt(mv["vol_per_well"])} uL '
                                        f'({mv["dose"]} ng)',
                            'Master Mix': f'{_fmt(mv["vol_total"])} uL',
                        })
                    rows.append({
                        'Component': 'Opti-MEM (fill)',
                        'Per Well': f'{_fmt(g["opti_per_well"])} uL',
                        'Master Mix': f'{_fmt(g["opti_total"])} uL',
                    })
                rows.append({
                    'Component': '+ Lipo Mix aliquot',
                    'Per Well': f'{_fmt(5.0)} uL',
                    'Master Mix': f'{_fmt(g["lipo_aliquot"])} uL',
                })
                rows.append({
                    'Component': 'COMPLEX TO ADD PER WELL',
                    'Per Well': '10 uL',
                    'Master Mix': f'{_fmt(10 * g["well_count"])} uL',
                })

                st.dataframe(pd.DataFrame(rows),
                             use_container_width=True, hide_index=True)

        # ============================================================
        # Section 6: Step-by-Step Protocol
        # ============================================================
        st.subheader('Step-by-Step Protocol')
        st.markdown(
            'Follow these steps in order. Check off each step as you '
            'complete it.')

        steps = generate_protocol_steps(mm, cell_types, plate_cells)

        for si, step in enumerate(steps):
            with st.expander(f'Step {si + 1}: {step["title"]}',
                              expanded=(si < 3)):
                for line in step['lines']:
                    st.checkbox(line, key=f'step_{si}_{hash(line)}')

        # ============================================================
        # Section 7: Model Predictions (integration with modeling tool)
        # ============================================================
        st.subheader('Model Predictions for This Protocol')
        st.markdown(
            'The modeling tool predicts the expected sfGFP+ percentage '
            'for each circuit condition in this protocol. Compare these '
            'predictions to your flow cytometry results after the experiment.')

        profiles = get_cell_profiles()
        has_predictions = False

        # Check if any groups look like circuit conditions
        circuit_groups = []
        for gi, g in enumerate(groups):
            sensor_ng = 0
            payload_ng = 0
            for mrna in g.get('mRNAs', []):
                name_lower = mrna['name'].lower()
                if 'sensor' in name_lower or 'l7ae' in name_lower or 'p069' in name_lower:
                    sensor_ng = mrna['dose']
                elif 'payload' in name_lower or 'kt' in name_lower or 'p065' in name_lower or 'sfgfp' in name_lower:
                    payload_ng = mrna['dose']
            if sensor_ng > 0 or payload_ng > 0:
                circuit_groups.append((gi, g['name'], sensor_ng, payload_ng))
                has_predictions = True

        if has_predictions and profiles:
            from modeling.core.optimizer import CircuitOptimizer
            p_model = get_params(L7Ae_repression_fold=1000, t_max_hr=24)
            opt = CircuitOptimizer(p_model)

            pred_rows = []
            for gi, gname, sensor_ng, payload_ng in circuit_groups:
                for cell_name, profile in profiles.items():
                    copies_per_ng = 20 * (30000 / cell_types[0]['density']) if cell_types else 20
                    sensor_c = int(sensor_ng * copies_per_ng)
                    payload_c = int(payload_ng * copies_per_ng)

                    try:
                        pop, thresh = opt._simulate_population(
                            sensor_c, payload_c,
                            {cell_name: profile},
                            n_cells=10000, seed=42)
                        pct = pop[cell_name]['percent_positive']
                    except Exception:
                        pct = 0

                    pred_rows.append({
                        'Group': gname,
                        'Cell Type': cell_name,
                        'Sensor (ng)': sensor_ng,
                        'Payload (ng)': payload_ng,
                        'Predicted sfGFP+ %': f'{pct:.1f}',
                    })

            if pred_rows:
                st.dataframe(pd.DataFrame(pred_rows),
                             use_container_width=True)
                st.caption(
                    'Predictions based on calibrated model parameters. '
                    'After running the experiment, go to **Enter Results** '
                    'to record your flow cytometry data, then '
                    '**Calibrate Model** to improve these predictions.')
        elif not has_predictions:
            st.info(
                'No circuit conditions detected in the groups above. '
                'Predictions are shown for groups containing sensor '
                '(L7Ae/p069B) or payload (2xKt-sfGFP/p065) mRNAs.')

        # ============================================================
        # Section 8: Export
        # ============================================================
        st.subheader('Export Protocol')

        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            # Text protocol
            protocol_text = f'TRANSFECTION PROTOCOL: {proto_title}\n'
            protocol_text += '=' * 60 + '\n\n'

            # Master mix summary
            if mm['lipo_mix']:
                protocol_text += 'MASTER MIX VOLUMES\n'
                protocol_text += '-' * 40 + '\n'
                protocol_text += f'Shared Lipo Mix: {_fmt(mm["lipo_mix"]["tube_total"])} uL total\n'
                for g in mm['groups']:
                    protocol_text += f'  G{g["group_index"]+1} {g["group_name"]}: '
                    protocol_text += f'{g["well_count"]} wells ({g["well_str"]})\n'
                protocol_text += '\n'

            # Steps
            steps = generate_protocol_steps(mm, cell_types, plate_cells)
            for si, step in enumerate(steps):
                protocol_text += f'STEP {si+1}: {step["title"]}\n'
                for line in step['lines']:
                    protocol_text += f'  [ ] {line}\n'
                protocol_text += '\n'

            st.download_button('Download Protocol (text)',
                               protocol_text,
                               f'{proto_title.replace(" ", "_")}_protocol.txt',
                               'text/plain')

        with col_ex2:
            # AutoProtocol JSON
            from modeling.core.autoprotocol import AutoProtocolExporter
            import json
            state = {
                'v': 1,
                'title': proto_title,
                'researcher': '',
                'date': '',
                'lipoPerWell': str(lipo_per_well),
                'extraPct': str(extra_pct),
                'bwMode': False,
                'groups': [
                    {'name': g['name'], 'type': g['type'],
                     'mRNAs': g.get('mRNAs', [])}
                    for g in groups
                ],
                'cellTypes': cell_types,
                'plateMRNA': plate_mrna,
                'plateCells': plate_cells,
                'selectedGroup': 0,
                'selectedCellType': 0,
                'paintMode': 'mrna',
            }
            st.download_button(
                'Download AutoProtocol JSON',
                json.dumps(state, indent=2),
                f'{proto_title.replace(" ", "_")}_autoprotocol.json',
                'application/json',
                help='Load this in the standalone AutoProtocol HTML tool '
                     'for the interactive plate painting interface')
