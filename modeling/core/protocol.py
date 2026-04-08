"""
Transfection protocol generator.

Computes master mix volumes, generates step-by-step protocol, and
produces plate layout visualizations. Native Python implementation
of the Transfection AutoProtocol calculator.

All volumes in microliters (uL). All concentrations in ng/uL.
All doses in ng per well.

Protocol uses a two-tube system:
  Tube A (Lipo Mix): Opti-MEM + Lipofectamine 2000, shared across all groups
  Tube B (per group): Opti-MEM + mRNA(s), one tube per mRNA group

After incubation, Tube A aliquot is added 1:1 to each Tube B,
then 10 uL of the combined complex is added per well.
"""

import math


# ================================================================
# Volume calculations
# ================================================================

VOLUME_PER_WELL_EACH_TUBE = 5.0   # uL per well for each tube (A and B)
COMPLEX_PER_WELL = 10.0            # uL added to each well (A + B combined)


def compute_master_mixes(groups, plate_mrna, lipo_per_well=0.30,
                          extra_pct=10):
    """Compute all master mix volumes.

    Parameters
    ----------
    groups : list of dict
        Each group: {name, type, mRNAs: [{name, conc, dose}]}
    plate_mrna : list of int
        96-element array, -1 = empty, else group index
    lipo_per_well : float
        Lipofectamine 2000 per well (uL)
    extra_pct : float
        Pipetting overage percentage

    Returns
    -------
    dict with lipo_mix and per_group volumes
    """
    extra_frac = extra_pct / 100.0
    total_assigned = sum(1 for v in plate_mrna if v >= 0)

    if total_assigned == 0:
        return {'lipo_mix': None, 'groups': [], 'total_wells': 0}

    total_n = total_assigned * (1 + extra_frac)

    # Tube A: Shared Lipo Mix
    opti_a_per_well = VOLUME_PER_WELL_EACH_TUBE - lipo_per_well
    lipo_mix = {
        'opti_per_well': opti_a_per_well,
        'opti_total': opti_a_per_well * total_n,
        'lipo_per_well': lipo_per_well,
        'lipo_total': lipo_per_well * total_n,
        'tube_total': VOLUME_PER_WELL_EACH_TUBE * total_n,
        'n_wells': total_assigned,
        'n_with_overage': total_n,
    }

    # Per-group Tube B calculations
    group_mixes = []
    for gi, group in enumerate(groups):
        well_count = sum(1 for v in plate_mrna if v == gi)
        if well_count == 0:
            continue

        n = well_count * (1 + extra_frac)
        tube_b_total = VOLUME_PER_WELL_EACH_TUBE * n

        # Well positions
        wells = get_well_positions(plate_mrna, gi)
        well_str = compress_well_list(wells)

        if group.get('type') == 'negative':
            # Negative control: Opti-MEM only
            group_mixes.append({
                'group_index': gi,
                'group_name': group['name'],
                'group_type': group['type'],
                'well_count': well_count,
                'n_with_overage': n,
                'wells': wells,
                'well_str': well_str,
                'is_negative': True,
                'opti_per_well': VOLUME_PER_WELL_EACH_TUBE,
                'opti_total': tube_b_total,
                'tube_total': tube_b_total,
                'mrna_volumes': [],
                'lipo_aliquot': VOLUME_PER_WELL_EACH_TUBE * n,
            })
            continue

        # Calculate mRNA volumes
        mrna_volumes = []
        total_rna_vol_per_well = 0

        for mrna in group.get('mRNAs', []):
            conc = mrna.get('conc', 500)
            dose = mrna.get('dose', 100)
            vol_per_well = dose / conc if conc > 0 else 0
            vol_total = vol_per_well * n
            total_rna_vol_per_well += vol_per_well

            mrna_volumes.append({
                'name': mrna['name'],
                'conc': conc,
                'dose': dose,
                'vol_per_well': vol_per_well,
                'vol_total': vol_total,
            })

        opti_per_well = VOLUME_PER_WELL_EACH_TUBE - total_rna_vol_per_well
        opti_total = opti_per_well * n

        group_mixes.append({
            'group_index': gi,
            'group_name': group['name'],
            'group_type': group['type'],
            'well_count': well_count,
            'n_with_overage': n,
            'wells': wells,
            'well_str': well_str,
            'is_negative': False,
            'opti_per_well': opti_per_well,
            'opti_total': opti_total,
            'tube_total': tube_b_total,
            'mrna_volumes': mrna_volumes,
            'is_cotransfection': len(mrna_volumes) > 1,
            'lipo_aliquot': VOLUME_PER_WELL_EACH_TUBE * n,
        })

    return {
        'lipo_mix': lipo_mix,
        'groups': group_mixes,
        'total_wells': total_assigned,
        'extra_pct': extra_pct,
        'lipo_per_well': lipo_per_well,
    }


def generate_protocol_steps(master_mix_result, cell_types=None,
                              plate_cells=None):
    """Generate step-by-step transfection protocol.

    Parameters
    ----------
    master_mix_result : dict
        Output from compute_master_mixes()
    cell_types : list of dict, optional
        [{name, density}]
    plate_cells : list of int, optional
        96-element cell type assignment array

    Returns
    -------
    list of dict : protocol steps with text and substeps
    """
    if not master_mix_result.get('lipo_mix'):
        return []

    lipo = master_mix_result['lipo_mix']
    groups = master_mix_result['groups']
    extra = master_mix_result['extra_pct']
    steps = []

    # Step 1: Seed cells
    seed_lines = []
    if cell_types and plate_cells:
        for ci, ct in enumerate(cell_types):
            ct_wells = sum(1 for v in plate_cells
                          if (v == ci) or (isinstance(v, list) and ci in v))
            if ct_wells > 0:
                seed_lines.append(
                    f'Seed {ct["density"]:,} cells/well of {ct["name"]} '
                    f'into {ct_wells} designated wells.')
    if not seed_lines:
        seed_lines.append(
            'Seed cells at appropriate density (typically '
            '1-4 x 10^4 cells/well for 96-well plate). '
            'Target 70-90% confluency at time of transfection.')

    steps.append({
        'title': 'Seed cells (day before transfection)',
        'lines': seed_lines + [
            'Incubate overnight at 37C, 5% CO2.',
            'Verify 70-90% confluency before proceeding.',
        ],
    })

    # Step 2: Prepare Lipo Mix
    steps.append({
        'title': 'Prepare shared Lipofectamine mix (Tube A)',
        'lines': [
            f'Label one tube "Lipo Mix" ({lipo["n_wells"]} wells + '
            f'{extra}% overage).',
            f'Add {_fmt(lipo["opti_total"])} uL Opti-MEM to the tube.',
            f'Add {_fmt(lipo["lipo_total"])} uL Lipofectamine 2000. '
            f'Mix gently by pipetting.',
            f'Total volume: {_fmt(lipo["tube_total"])} uL.',
        ],
    })

    # Step 3: Prepare group tubes
    group_lines = []
    for i, g in enumerate(groups):
        label = f'G{i+1}'
        if g['is_negative']:
            group_lines.append(
                f'{label}: {g["group_name"]} ({g["well_count"]}w, '
                f'{g["well_str"]}): '
                f'Add {_fmt(g["opti_total"])} uL Opti-MEM '
                f'(vehicle control, no mRNA).')
        else:
            parts = []
            for mv in g['mrna_volumes']:
                parts.append(
                    f'Add {_fmt(mv["vol_total"])} uL {mv["name"]} '
                    f'({mv["conc"]} ng/uL, {mv["dose"]} ng/well).')
            parts.append(
                f'Add {_fmt(g["opti_total"])} uL Opti-MEM.')
            cotx = ' [CO-TRANSFECTION]' if g.get('is_cotransfection') else ''
            header = (f'{label}: {g["group_name"]} '
                      f'({g["well_count"]}w, {g["well_str"]}){cotx}:')
            group_lines.append(header + ' ' + ' '.join(parts))

    steps.append({
        'title': 'Prepare mRNA tubes (one per group)',
        'lines': group_lines,
    })

    # Step 4: Combine Lipo Mix with group tubes
    combine_lines = []
    for i, g in enumerate(groups):
        label = f'G{i+1}'
        combine_lines.append(
            f'Add {_fmt(g["lipo_aliquot"])} uL Lipo Mix to '
            f'{label} ({g["group_name"]}). Mix gently.')
    steps.append({
        'title': 'Add Lipo Mix to each group tube (1:1 ratio)',
        'lines': combine_lines,
    })

    # Step 5: Incubate
    steps.append({
        'title': 'Incubate complexes',
        'lines': ['Incubate at room temperature for 5 minutes.'],
    })

    # Step 6: Add to cells
    add_lines = []
    for i, g in enumerate(groups):
        label = f'G{i+1}'
        add_lines.append(
            f'Dispense 10 uL {label} ({g["group_name"]}) into wells: '
            f'{g["well_str"]}.')
    add_lines.append('Gently rock the plate side-to-side after each group.')
    steps.append({
        'title': 'Add transfection complexes to cells',
        'lines': add_lines,
    })

    # Step 7: Final incubation
    steps.append({
        'title': 'Incubate',
        'lines': [
            'Return plate to incubator: 37C, 5% CO2.',
            'Incubate 1-3 days. No medium change required.',
            'Analyze by flow cytometry or microscopy at desired timepoint.',
        ],
    })

    return steps


# ================================================================
# Plate layout utilities
# ================================================================

ROWS = 'ABCDEFGH'


def get_well_name(index):
    """Convert 0-based index to well name (A1, A2, ..., H12)."""
    row = index // 12
    col = index % 12
    return f'{ROWS[row]}{col + 1}'


def get_well_positions(plate_mrna, group_index):
    """Get list of well names assigned to a group."""
    return [get_well_name(i) for i, v in enumerate(plate_mrna)
            if v == group_index]


def compress_well_list(wells):
    """Compress consecutive wells: ['A1','A2','A3'] -> 'A1-A3'."""
    if not wells:
        return ''

    # Group by row
    from itertools import groupby
    rows = {}
    for w in wells:
        row = w[0]
        col = int(w[1:])
        rows.setdefault(row, []).append(col)

    parts = []
    for row in sorted(rows.keys()):
        cols = sorted(rows[row])
        # Find consecutive runs
        ranges = []
        start = cols[0]
        end = cols[0]
        for c in cols[1:]:
            if c == end + 1:
                end = c
            else:
                ranges.append((start, end))
                start = end = c
        ranges.append((start, end))

        for s, e in ranges:
            if s == e:
                parts.append(f'{row}{s}')
            else:
                parts.append(f'{row}{s}-{row}{e}')

    return ', '.join(parts)


def auto_assign_plate(groups, cell_types, replicates=3):
    """Auto-assign wells to groups and cell types.

    Layout: each group gets a column, replicates fill down rows.
    Cell types get separate blocks of columns. When columns are
    exhausted, wraps to the next block of rows.

    Returns
    -------
    plate_mrna, plate_cells : lists of 96 ints
    """
    plate_mrna = [-1] * 96
    plate_cells = [-1] * 96

    col = 0
    row_offset = 0

    for ct_idx in range(len(cell_types)):
        for g_idx in range(len(groups)):
            if col >= 12:
                col = 0
                row_offset += replicates
            for rep in range(replicates):
                row = row_offset + rep
                if row < 8 and col < 12:
                    well_idx = row * 12 + col
                    plate_mrna[well_idx] = g_idx
                    plate_cells[well_idx] = ct_idx
            col += 1

    return plate_mrna, plate_cells


def _fmt(n):
    """Format volume with appropriate precision."""
    if n >= 100:
        return f'{n:.1f}'
    elif n >= 10:
        return f'{n:.1f}'
    elif n >= 1:
        return f'{n:.2f}'
    else:
        return f'{n:.3f}'
