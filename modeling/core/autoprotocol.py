"""
Transfection AutoProtocol integration.

Generates protocol JSON files compatible with the Transfection AutoProtocol
HTML tool. Takes an experiment design from the ExperimentDesigner and converts
it into a plate layout with mRNA groups, cell types, and well assignments
that the AutoProtocol can load directly.

The AutoProtocol state format:
{
    "v": 1,
    "title": str,
    "researcher": str,
    "date": str,
    "lipoPerWell": str,
    "extraPct": str,
    "groups": [
        {
            "name": str,
            "type": "positive"|"negative"|"experimental",
            "mRNAs": [{"name": str, "conc": float, "dose": float}]
        }
    ],
    "cellTypes": [{"name": str, "density": int}],
    "plateMRNA": [int * 96],   // -1 = empty, index into groups
    "plateCells": [int * 96],  // -1 = empty, index into cellTypes
    "selectedGroup": 0,
    "selectedCellType": 0,
    "paintMode": "mrna"
}
"""

import json


class AutoProtocolExporter:
    """Export experiment designs as AutoProtocol-compatible JSON."""

    def __init__(self, sensor_name='p069B (L7Ae sensor)',
                 payload_name='p065 (2xKt-sfGFP)',
                 sensor_conc=500, payload_conc=500,
                 lipo_per_well='0.30', extra_pct='10'):
        self.sensor_name = sensor_name
        self.payload_name = payload_name
        self.sensor_conc = sensor_conc  # ng/uL stock concentration
        self.payload_conc = payload_conc
        self.lipo_per_well = lipo_per_well
        self.extra_pct = extra_pct

    def from_experiment_design(self, design, title=None, researcher='',
                                date='', cells_per_well=30000):
        """Convert an ExperimentDesigner output to AutoProtocol JSON.

        Parameters
        ----------
        design : dict
            Output from ExperimentDesigner.design_titration()
        title : str, optional
        researcher : str
        date : str (YYYY-MM-DD)
        cells_per_well : int

        Returns
        -------
        dict : AutoProtocol state object (JSON-serializable)
        """
        # Build mRNA groups from the unique (sensor_ng, payload_ng) combinations
        conditions = design.get('conditions', [])
        controls = design.get('controls', [])
        cell_types_in_design = sorted(design.get('cell_profiles', {}).keys())
        replicates = design.get('replicates', 3)

        # Collect unique dose combinations
        dose_combos = []
        seen = set()

        # Controls first
        # Negative/Mock control
        dose_combos.append({
            'name': 'Mock Transfection',
            'type': 'negative',
            'mRNAs': [],
            'sensor_ng': 0,
            'payload_ng': 0,
        })
        seen.add((0, 0, 'mock'))

        # Payload-only control
        payload_ng = design.get('payload_ng', 150)
        dose_combos.append({
            'name': f'Payload Only ({payload_ng}ng)',
            'type': 'positive',
            'mRNAs': [{'name': self.payload_name,
                       'conc': self.payload_conc,
                       'dose': payload_ng}],
            'sensor_ng': 0,
            'payload_ng': payload_ng,
        })
        seen.add((0, payload_ng))

        # Sensor-only control
        dose_combos.append({
            'name': 'Sensor Only (100ng)',
            'type': 'experimental',
            'mRNAs': [{'name': self.sensor_name,
                       'conc': self.sensor_conc,
                       'dose': 100}],
            'sensor_ng': 100,
            'payload_ng': 0,
        })
        seen.add((100, 0))

        # Experimental conditions
        sensor_list = sorted(set(
            c['sensor_ng'] for c in conditions if c['sensor_ng'] > 0))

        for sensor_ng in sensor_list:
            key = (sensor_ng, payload_ng)
            if key in seen:
                continue
            seen.add(key)

            mRNAs = []
            if sensor_ng > 0:
                mRNAs.append({'name': self.sensor_name,
                              'conc': self.sensor_conc,
                              'dose': sensor_ng})
            if payload_ng > 0:
                mRNAs.append({'name': self.payload_name,
                              'conc': self.payload_conc,
                              'dose': payload_ng})

            dose_combos.append({
                'name': f'S={sensor_ng}ng + P={payload_ng}ng',
                'type': 'experimental',
                'mRNAs': mRNAs,
                'sensor_ng': sensor_ng,
                'payload_ng': payload_ng,
            })

        # Build groups array for autoprotocol
        groups = []
        for combo in dose_combos:
            groups.append({
                'name': combo['name'],
                'type': combo['type'],
                'mRNAs': combo['mRNAs'],
            })

        # Build cell types
        cell_type_list = []
        for ct_name in cell_types_in_design:
            cell_type_list.append({
                'name': ct_name,
                'density': cells_per_well,
            })

        # Build plate layout (96 wells)
        # Layout: each group gets a column, replicates fill down rows.
        # Cell types get separate blocks of columns.
        plateMRNA = [-1] * 96
        plateCells = [-1] * 96

        col = 0
        row_offset = 0

        for ct_idx, ct_name in enumerate(cell_types_in_design):
            for g_idx, group in enumerate(groups):
                if col >= 12:
                    col = 0
                    row_offset += replicates
                for rep in range(replicates):
                    row = row_offset + rep
                    if row < 8 and col < 12:
                        well_idx = row * 12 + col
                        plateMRNA[well_idx] = g_idx
                        plateCells[well_idx] = ct_idx
                col += 1

        state = {
            'v': 1,
            'title': title or f'Circuit Validation: {", ".join(cell_types_in_design)}',
            'researcher': researcher,
            'date': date,
            'lipoPerWell': self.lipo_per_well,
            'extraPct': self.extra_pct,
            'bwMode': False,
            'groups': groups,
            'cellTypes': cell_type_list,
            'plateMRNA': plateMRNA,
            'plateCells': plateCells,
            'selectedGroup': 0,
            'selectedCellType': 0,
            'paintMode': 'mrna',
        }

        return state

    def from_optimization_result(self, opt_result, cell_profiles,
                                  replicates=3, title=None, researcher='',
                                  date='', cells_per_well=30000):
        """Generate a protocol from an optimizer result.

        Creates groups for the optimal ratio plus comparison ratios.

        Parameters
        ----------
        opt_result : dict
            Output from CircuitOptimizer.optimize_ratio()
        cell_profiles : dict
        replicates : int
        title, researcher, date, cells_per_well : see above

        Returns
        -------
        dict : AutoProtocol state
        """
        cell_names = sorted(cell_profiles.keys())
        best = opt_result['best']

        # Select key ratios to test: optimal + a few comparison points
        sweep = opt_result.get('sweep', [])
        key_ratios = [best]

        # Add 1:1 baseline if different from optimal
        for r in sweep:
            if r['sp_ratio'] == 1.0 and r != best:
                key_ratios.append(r)

        # Add one point on each side of optimal
        best_idx = sweep.index(best) if best in sweep else 0
        if best_idx > 0:
            key_ratios.append(sweep[best_idx - 1])
        if best_idx < len(sweep) - 1:
            key_ratios.append(sweep[best_idx + 1])

        # Deduplicate and sort
        seen_sp = set()
        unique_ratios = []
        for r in key_ratios:
            if r['sp_ratio'] not in seen_sp:
                seen_sp.add(r['sp_ratio'])
                unique_ratios.append(r)
        unique_ratios.sort(key=lambda r: r['sp_ratio'])

        # Build groups
        groups = [
            {'name': 'Mock Transfection', 'type': 'negative', 'mRNAs': []},
        ]

        # Add payload-only control
        payload_ng = best['payload_ng']
        groups.append({
            'name': f'Payload Only ({payload_ng:.0f}ng)',
            'type': 'positive',
            'mRNAs': [{'name': self.payload_name,
                       'conc': self.payload_conc,
                       'dose': round(payload_ng)}],
        })

        # Add each ratio as a group
        for r in unique_ratios:
            label = f'S={r["sensor_ng"]:.0f}ng + P={r["payload_ng"]:.0f}ng'
            if r == best:
                label += ' [OPTIMAL]'
            elif r['sp_ratio'] == 1.0:
                label += ' [1:1 baseline]'

            mRNAs = []
            if r['sensor_ng'] > 0:
                mRNAs.append({'name': self.sensor_name,
                              'conc': self.sensor_conc,
                              'dose': round(r['sensor_ng'])})
            if r['payload_ng'] > 0:
                mRNAs.append({'name': self.payload_name,
                              'conc': self.payload_conc,
                              'dose': round(r['payload_ng'])})

            groups.append({
                'name': label,
                'type': 'experimental',
                'mRNAs': mRNAs,
            })

        # Cell types
        cell_type_list = [{'name': n, 'density': cells_per_well}
                          for n in cell_names]

        # Plate layout: groups in columns, replicates down rows
        plateMRNA = [-1] * 96
        plateCells = [-1] * 96

        col = 0
        row_offset = 0

        for ct_idx in range(len(cell_names)):
            for g_idx in range(len(groups)):
                if col >= 12:
                    col = 0
                    row_offset += replicates
                for rep in range(replicates):
                    row = row_offset + rep
                    if row < 8 and col < 12:
                        well_idx = row * 12 + col
                        plateMRNA[well_idx] = g_idx
                        plateCells[well_idx] = ct_idx
                col += 1

        return {
            'v': 1,
            'title': title or 'Optimized Circuit Validation',
            'researcher': researcher,
            'date': date,
            'lipoPerWell': self.lipo_per_well,
            'extraPct': self.extra_pct,
            'bwMode': False,
            'groups': groups,
            'cellTypes': cell_type_list,
            'plateMRNA': plateMRNA,
            'plateCells': plateCells,
            'selectedGroup': 0,
            'selectedCellType': 0,
            'paintMode': 'mrna',
        }

    def to_json(self, state, filepath=None):
        """Serialize state to JSON string or file.

        Parameters
        ----------
        state : dict
        filepath : str, optional
            If provided, write to file. Otherwise return string.

        Returns
        -------
        str : JSON string (if no filepath)
        """
        json_str = json.dumps(state, indent=2)
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_str)
        return json_str
