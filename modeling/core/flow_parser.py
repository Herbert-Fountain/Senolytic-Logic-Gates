"""
Flow cytometry data parser.

Reads raw flow cytometry export files and converts them into the
format needed by the model calibrator. Supports:

  - NovoExpress summary CSV (NovoCyte Quanteon)
  - Generic CSV with % positive columns
  - Manual entry format (cell_type, sensor_ng, payload_ng, observed_pct)

The parser extracts Live sfGFP+ % and MFI data, maps specimen names
to cell types and mRNA doses, and outputs a standardized observation
table ready for calibration.
"""

import csv
import re
import os
from collections import defaultdict


class FlowDataParser:
    """Parse flow cytometry exports into model-compatible format."""

    def __init__(self):
        # Known specimen name patterns -> (cell_type, sensor_ng, payload_ng)
        self.specimen_patterns = [
            # ON switch experiment patterns
            (r'(?i)(\w+)\s+positive\s+control\s+(\d+)\s*ng',
             lambda m: (m.group(1), 0, float(m.group(2)),
                        'positive_control')),
            (r'(?i)(\w+)\s+negative\s+control',
             lambda m: (m.group(1), 0, 0, 'negative_control')),
            (r'(?i)(\w+)\s+2xKt-sfGFP\s+(\d+)\s*ng',
             lambda m: (m.group(1), 0, float(m.group(2)),
                        'payload_only')),
            (r'(?i)(\w+)\s+p069B\s+(\d+)\s*ng',
             lambda m: (m.group(1), float(m.group(2)), 0,
                        'sensor_only')),
            (r'(?i)(\w+)\s+p065\s*\+\s*p069B\s+(\d+):(\d+)\s*ng',
             lambda m: (m.group(1), float(m.group(3)), float(m.group(2)),
                        'and_gate')),
            (r'(?i)(\w+)\s+No\s+Transfection',
             lambda m: (m.group(1), 0, 0, 'no_transfection')),
        ]

    def parse_novoexpress_csv(self, filepath, encoding='utf-8-sig'):
        """Parse a NovoExpress summary table CSV.

        Expected columns (from NovoCyte Quanteon export):
            Specimen No., Specimen, Well ID, Sample, Run Time,
            All Count, Cells Count, Live Count,
            Live sfGFP Negative Count, Live sfGFP Positive Count,
            Dead Count, etc.

        Parameters
        ----------
        filepath : str
            Path to the NovoExpress summary CSV

        Returns
        -------
        dict with:
            observations: list of standardized observation dicts
            raw_data: list of raw rows
            specimen_summary: per-specimen averaged data
            warnings: list of parsing issues
        """
        raw_rows = []
        warnings = []

        with open(filepath, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_rows.append(row)

        if not raw_rows:
            return {'observations': [], 'raw_data': [], 'warnings': ['Empty file']}

        # Group by specimen
        specimens = defaultdict(list)
        for row in raw_rows:
            spec_name = row.get('Specimen', '').strip()
            if spec_name:
                specimens[spec_name].append(row)

        # Process each specimen
        observations = []
        specimen_summary = []

        for spec_name, rows in specimens.items():
            # Parse specimen name to get cell type and doses
            cell_type, sensor_ng, payload_ng, condition_type = \
                self._parse_specimen_name(spec_name)

            if cell_type is None:
                warnings.append(f'Could not parse specimen: "{spec_name}"')
                continue

            # Compute Live sfGFP+ % for each replicate
            replicate_pcts = []
            replicate_mfis = []

            for row in rows:
                live_count = self._safe_int(row.get('Live Count', 0))
                live_pos = self._safe_int(
                    row.get('Live sfGFP Positive Count', 0))

                if live_count > 0:
                    pct = 100.0 * live_pos / live_count
                    replicate_pcts.append(pct)

                    # MFI if available (from the Median X column for sfGFP+)
                    # NovoExpress doesn't always include MFI in summary CSV
                    # but we can compute it from count * median if present

            if not replicate_pcts:
                warnings.append(
                    f'No valid replicates for "{spec_name}"')
                continue

            mean_pct = sum(replicate_pcts) / len(replicate_pcts)
            std_pct = (sum((x - mean_pct)**2 for x in replicate_pcts)
                       / max(len(replicate_pcts) - 1, 1)) ** 0.5

            obs = {
                'cell_type': cell_type,
                'sensor_ng': sensor_ng,
                'payload_ng': payload_ng,
                'observed_pct': round(mean_pct, 2),
                'std_pct': round(std_pct, 2),
                'n_replicates': len(replicate_pcts),
                'replicate_values': [round(p, 2) for p in replicate_pcts],
                'condition_type': condition_type,
                'specimen_name': spec_name,
            }

            observations.append(obs)

            specimen_summary.append({
                'specimen': spec_name,
                'cell_type': cell_type,
                'condition': condition_type,
                'sensor_ng': sensor_ng,
                'payload_ng': payload_ng,
                'mean_pct': round(mean_pct, 2),
                'std_pct': round(std_pct, 2),
                'n': len(replicate_pcts),
                'replicates': [round(p, 1) for p in replicate_pcts],
            })

        return {
            'observations': observations,
            'raw_data': raw_rows,
            'specimen_summary': specimen_summary,
            'warnings': warnings,
            'n_specimens': len(specimens),
            'n_observations': len(observations),
        }

    def _parse_specimen_name(self, name):
        """Parse a specimen name into (cell_type, sensor_ng, payload_ng, type).

        Returns (None, 0, 0, None) if unrecognized.
        """
        name = name.strip().rstrip(',')

        for pattern, extractor in self.specimen_patterns:
            m = re.search(pattern, name)
            if m:
                cell_type, sensor, payload, cond_type = extractor(m)
                # Normalize cell type names
                cell_type = cell_type.strip()
                if cell_type.upper() == 'NIH':
                    # "NIH 4T1" -> "4T1"
                    rest = name[m.end():].strip()
                    cell_match = re.match(r'(\w+)', rest)
                    if cell_match:
                        cell_type = cell_match.group(1)
                    else:
                        cell_type = '4T1'  # Default for NIH prefix

                # Handle "NIH 4T1" as a compound name
                if 'NIH' in name and '4T1' in name:
                    cell_type = '4T1'
                elif 'HuH7' in name or 'HuH-7' in name:
                    cell_type = 'HuH7'

                return cell_type, sensor, payload, cond_type

        return None, 0, 0, None

    def _safe_int(self, val):
        """Safely convert to int, returning 0 on failure."""
        try:
            return int(str(val).strip().replace(',', ''))
        except (ValueError, TypeError):
            return 0

    def to_calibration_csv(self, observations, filepath):
        """Export observations in the format expected by the calibrator.

        Output columns: cell_type, sensor_ng, payload_ng, observed_pct
        """
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(
                f, fieldnames=['cell_type', 'sensor_ng', 'payload_ng',
                               'observed_pct'])
            writer.writeheader()
            for obs in observations:
                writer.writerow({
                    'cell_type': obs['cell_type'],
                    'sensor_ng': obs['sensor_ng'],
                    'payload_ng': obs['payload_ng'],
                    'observed_pct': obs['observed_pct'],
                })

    def format_summary(self, parse_result):
        """Format parsed flow data as readable text."""
        lines = []
        lines.append(f'Parsed {parse_result["n_specimens"]} specimens, '
                      f'{parse_result["n_observations"]} conditions')

        if parse_result['warnings']:
            lines.append(f'\nWarnings:')
            for w in parse_result['warnings']:
                lines.append(f'  - {w}')

        lines.append(f'\n{"Specimen":<45s} {"Cell":>6s} {"Type":>15s} '
                      f'{"S(ng)":>6s} {"P(ng)":>6s} {"Mean%":>7s} '
                      f'{"SD":>5s} {"n":>3s}')
        lines.append('-' * 100)

        for s in parse_result['specimen_summary']:
            lines.append(
                f'{s["specimen"]:<45s} {s["cell_type"]:>6s} '
                f'{s["condition"]:>15s} {s["sensor_ng"]:6.0f} '
                f'{s["payload_ng"]:6.0f} {s["mean_pct"]:6.1f}% '
                f'{s["std_pct"]:4.1f} {s["n"]:3d}')

        return '\n'.join(lines)
