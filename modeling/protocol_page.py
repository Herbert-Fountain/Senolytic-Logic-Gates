"""
Protocol Designer page for the Streamlit app.

Provides a complete transfection protocol interface integrated with
the circuit modeling tool. Import this and call render_protocol_page()
from the main app.
"""

import streamlit as st
import pandas as pd
import numpy as np


# ================================================================
# Plate visualization constants and helpers
# ================================================================

_PLATE_ROWS = 'ABCDEFGH'

_GROUP_COLORS = ['#5b8c78', '#c0884a', '#7b6ea6', '#c26e6e',
                 '#4a8fa8', '#a08c5a', '#8a6d9e', '#5a9a7a',
                 '#b07850', '#6888a8']

_CELL_COLORS = ['#c9b99a', '#d4a88c', '#8cb4d4', '#b4d48c',
                '#d48cb4', '#8cd4b4', '#d4b48c', '#b48cd4']


def _render_plate_html(plate_mrna, plate_cells, groups, cell_types):
    """Render 96-well plate as HTML with colored circles."""
    html = ['<div style="overflow-x: auto;">']
    html.append(
        '<div style="display: inline-grid; '
        'grid-template-columns: 30px repeat(12, 62px); '
        'gap: 5px; align-items: center; justify-items: center; '
        'padding: 8px;">')

    # Column header row
    html.append('<div></div>')
    for c in range(1, 13):
        html.append(
            f'<div style="text-align: center; font-weight: 700; '
            f'font-size: 14px; color: #555;">{c}</div>')

    for ri in range(8):
        # Row label
        html.append(
            f'<div style="text-align: center; font-weight: 700; '
            f'font-size: 14px; color: #555;">{_PLATE_ROWS[ri]}</div>')

        for ci in range(12):
            wi = ri * 12 + ci
            gi = plate_mrna[wi]
            cti = plate_cells[wi]
            name = f'{_PLATE_ROWS[ri]}{ci + 1}'

            if 0 <= gi < len(groups):
                bg = _GROUP_COLORS[gi % len(_GROUP_COLORS)]
                fg = '#fff'
            else:
                bg = '#f5f0e8'
                fg = '#bbb'

            if 0 <= cti < len(cell_types):
                border = f'3px solid {_CELL_COLORS[cti % len(_CELL_COLORS)]}'
            else:
                border = '2px solid #e0dbd2'

            html.append(
                f'<div style="width: 56px; height: 56px; border-radius: 50%; '
                f'background: {bg}; border: {border}; '
                f'display: flex; align-items: center; justify-content: center; '
                f'font-size: 11px; font-weight: 600; color: {fg}; '
                f'font-family: -apple-system, BlinkMacSystemFont, sans-serif; '
                f'box-shadow: 0 1px 3px rgba(0,0,0,0.08);">'
                f'{name}</div>')

    html.append('</div></div>')
    return '\n'.join(html)


def _render_legend_html(groups, plate_mrna, cell_types, plate_cells):
    """Render color-coded legend for groups and cell types."""
    html = ['<div style="font-family: -apple-system, sans-serif; '
            'margin-top: 10px;">']

    # mRNA groups
    items = []
    for gi, g in enumerate(groups):
        wc = sum(1 for v in plate_mrna if v == gi)
        if wc > 0:
            color = _GROUP_COLORS[gi % len(_GROUP_COLORS)]
            gtype = g.get('type', 'experimental')
            type_str = {'positive': 'pos ctrl',
                        'negative': 'neg ctrl'}.get(gtype, 'exp')
            dose_parts = [f'{m["dose"]:.0f}ng'
                          for m in g.get('mRNAs', [])]
            dose_str = '+'.join(dose_parts) if dose_parts else ''
            detail = f' - {dose_str}' if dose_str else ''

            items.append(
                f'<span style="display: inline-flex; align-items: center; '
                f'margin: 4px 16px 4px 0;">'
                f'<span style="width: 18px; height: 18px; border-radius: 50%; '
                f'background: {color}; display: inline-block; '
                f'margin-right: 6px; flex-shrink: 0;"></span>'
                f'<strong>{g["name"]}</strong>'
                f'<span style="color: #777; margin-left: 6px; font-size: 12px;">'
                f'({wc}w - {type_str}{detail})</span></span>')

    html.append(
        '<div style="display: flex; flex-wrap: wrap; margin-bottom: 8px;">')
    html.append(''.join(items))
    html.append('</div>')

    # Cell types
    ct_items = []
    for ci, ct in enumerate(cell_types):
        wc = sum(1 for v in plate_cells if v == ci)
        if wc > 0:
            color = _CELL_COLORS[ci % len(_CELL_COLORS)]
            ct_items.append(
                f'<span style="display: inline-flex; align-items: center; '
                f'margin: 4px 16px 4px 0;">'
                f'<span style="width: 18px; height: 18px; border-radius: 50%; '
                f'border: 3px solid {color}; background: #fff; '
                f'display: inline-block; margin-right: 6px; '
                f'flex-shrink: 0;"></span>'
                f'<strong>{ct["name"]}</strong>'
                f'<span style="color: #777; margin-left: 6px; font-size: 12px;">'
                f'({wc}w - {ct["density"]:,}/well)</span></span>')

    if ct_items:
        html.append(
            '<div style="display: flex; flex-wrap: wrap;">')
        html.append(''.join(ct_items))
        html.append('</div>')

    html.append('</div>')
    return '\n'.join(html)


def _parse_well_input(text):
    """Parse well input like 'A1-A6, B2, C3-D6' into well indices."""
    indices = set()
    for part in text.split(','):
        part = part.strip().upper()
        if not part:
            continue
        if '-' in part:
            try:
                start, end = part.split('-', 1)
                sr = _PLATE_ROWS.index(start[0])
                sc = int(start[1:]) - 1
                er = _PLATE_ROWS.index(end[0])
                ec = int(end[1:]) - 1
                for r in range(sr, er + 1):
                    for c in range(sc, ec + 1):
                        if 0 <= r < 8 and 0 <= c < 12:
                            indices.add(r * 12 + c)
            except (ValueError, IndexError):
                pass
        else:
            try:
                r = _PLATE_ROWS.index(part[0])
                c = int(part[1:]) - 1
                if 0 <= r < 8 and 0 <= c < 12:
                    indices.add(r * 12 + c)
            except (ValueError, IndexError):
                pass
    return indices


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

    # -- Paint mode controls --
    pc1, pc2 = st.columns([1, 1])
    with pc1:
        paint_mode = st.radio(
            'Mode', ['Paint mRNA Groups', 'Paint Cell Types'],
            horizontal=True, key='paint_mode')
    with pc2:
        if paint_mode == 'Paint mRNA Groups':
            group_names = [g['name'] for g in groups]
            active_paint_idx = st.selectbox(
                'Painting', range(len(group_names)),
                format_func=lambda i: group_names[i],
                key='active_group_sel') if group_names else 0
        else:
            ct_names = [ct['name'] for ct in cell_types]
            active_paint_idx = st.selectbox(
                'Painting', range(len(ct_names)),
                format_func=lambda i: ct_names[i],
                key='active_ct_sel') if ct_names else 0

    ec1, ec2, ec3, ec4 = st.columns(4)
    with ec1:
        eraser = st.checkbox('Eraser', key='plate_eraser')
    with ec2:
        if st.button('Clear layer'):
            if paint_mode == 'Paint mRNA Groups':
                st.session_state.proto_plate_mrna = [-1] * 96
                plate_mrna = st.session_state.proto_plate_mrna
            else:
                st.session_state.proto_plate_cells = [-1] * 96
                plate_cells = st.session_state.proto_plate_cells
            st.rerun()
    with ec3:
        replicates = st.number_input('Replicates', 1, 8, 3,
                                      key='proto_reps')
    with ec4:
        if st.button('Auto-assign', type='primary'):
            plate_mrna, plate_cells = auto_assign_plate(
                groups, cell_types, replicates)
            st.session_state.proto_plate_mrna = plate_mrna
            st.session_state.proto_plate_cells = plate_cells
            st.rerun()

    # -- Plate visualization (colored circles) --
    plate_html = _render_plate_html(plate_mrna, plate_cells,
                                     groups, cell_types)
    st.markdown(plate_html, unsafe_allow_html=True)

    # -- Well selection for painting --
    ws1, ws2, ws3 = st.columns([1, 1, 2])
    with ws1:
        sel_rows = st.multiselect(
            'Rows', list(_PLATE_ROWS), key='sel_rows')
    with ws2:
        sel_cols = st.multiselect(
            'Columns', list(range(1, 13)), key='sel_cols')
    with ws3:
        well_text = st.text_input(
            'Or type wells (e.g. A1-A6, B2, C3-D6)',
            key='well_text_input')

    if st.button('Paint selected wells'):
        wells_to_paint = set()
        for r in sel_rows:
            for c in sel_cols:
                wells_to_paint.add(_PLATE_ROWS.index(r) * 12 + (c - 1))
        if well_text.strip():
            wells_to_paint.update(_parse_well_input(well_text))

        for wi in wells_to_paint:
            if 0 <= wi < 96:
                if eraser:
                    if paint_mode == 'Paint mRNA Groups':
                        plate_mrna[wi] = -1
                    else:
                        plate_cells[wi] = -1
                else:
                    if paint_mode == 'Paint mRNA Groups':
                        plate_mrna[wi] = active_paint_idx
                    else:
                        plate_cells[wi] = active_paint_idx

        st.session_state.proto_plate_mrna = plate_mrna
        st.session_state.proto_plate_cells = plate_cells
        st.rerun()

    # -- Legend and summary --
    n_assigned = sum(1 for v in plate_mrna if v >= 0)
    if n_assigned > 0:
        legend_html = _render_legend_html(groups, plate_mrna,
                                           cell_types, plate_cells)
        st.markdown(legend_html, unsafe_allow_html=True)
        st.caption(f'{n_assigned} of 96 wells assigned.')
    else:
        st.info(
            'No wells assigned yet. Click **Auto-assign** or '
            'select wells and click **Paint selected wells**.')

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
