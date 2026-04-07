#!/usr/bin/env python3
"""
miRNA Logic Gate Circuit Designer
===================================
Takes miRNA expression data from two conditions (e.g., target vs. non-target,
senescent vs. healthy) and recommends L7Ae-based AND-gate circuit designs.

Supports two use cases:
  1. Senolytic: Kill senescent cells, spare healthy (same cell type, different state)
  2. Cancer-targeting: Kill cancer cells, spare normal tissues

Usage:
  python circuit_designer.py --target target_counts.csv --control control_counts.csv --mode [senolytic|cancer]

Or use as a library:
  from circuit_designer import CircuitDesigner
  designer = CircuitDesigner()
  results = designer.analyze(target_df, control_df, mode='cancer')
"""

import pandas as pd
import numpy as np
import argparse
import os
import sys
import json
from datetime import datetime


class CircuitDesigner:
    """Designs L7Ae-based miRNA-sensing logic gate circuits."""

    # Known senescence-associated miRNAs from our cross-study analysis
    KNOWN_SENESCENCE_UP = {
        'miR-34a-5p': {'confidence': 'high', 'note': 'UP in 18/21 analyses across 4 inducers, 3 organisms'},
        'miR-22-3p': {'confidence': 'moderate', 'note': 'UP in fibroblasts only; DOWN in HUVECs'},
    }

    KNOWN_SENESCENCE_DOWN = {
        'miR-155-5p': {'confidence': 'high', 'note': '9-11x decline in fibroblasts; inflammaging confound in vivo'},
        'miR-92a-3p': {'confidence': 'high', 'note': 'DOWN in fibroblasts + human heart/skin/blood'},
        'miR-16-5p': {'confidence': 'moderate', 'note': 'DOWN in fibroblasts + rat kidney; uncertain in endothelial'},
        'miR-17-5p': {'confidence': 'moderate', 'note': 'DOWN in fibroblasts + HAECs; UP in HUVECs'},
    }

    # Default thresholds
    DEFAULT_MIN_EXPRESSION = 50        # Minimum CPM in target cells for ON switch
    DEFAULT_MIN_HEALTHY_EXPR = 100     # Minimum CPM in healthy cells for OFF switch
    DEFAULT_MIN_FC = 1.3               # Minimum fold change to consider meaningful
    DEFAULT_MIN_OFF_FC = 0.7           # Maximum fold change for OFF switch (must be below this)

    def __init__(self, min_expression=None, min_healthy_expr=None, min_fc=None, min_off_fc=None):
        self.min_expression = min_expression or self.DEFAULT_MIN_EXPRESSION
        self.min_healthy_expr = min_healthy_expr or self.DEFAULT_MIN_HEALTHY_EXPR
        self.min_fc = min_fc or self.DEFAULT_MIN_FC
        self.min_off_fc = min_off_fc or self.DEFAULT_MIN_OFF_FC

    def normalize_cpm(self, df):
        """Apply CPM normalization to a counts dataframe.
        Rows = miRNAs, columns = samples. Returns CPM-normalized dataframe."""
        lib_sizes = df.sum(axis=0)
        cpm = df.divide(lib_sizes, axis=1) * 1e6
        return cpm

    def compute_fold_changes(self, target_df, control_df, normalize=True):
        """Compute fold changes between target and control conditions.

        Parameters
        ----------
        target_df : DataFrame
            miRNA counts for target cells (rows=miRNAs, cols=replicates)
        control_df : DataFrame
            miRNA counts for control cells
        normalize : bool
            If True, apply CPM normalization before computing FC

        Returns
        -------
        DataFrame with columns: miRNA, target_mean, control_mean, fc, log2fc, direction
        """
        if normalize:
            target_cpm = self.normalize_cpm(target_df)
            control_cpm = self.normalize_cpm(control_df)
        else:
            target_cpm = target_df
            control_cpm = control_df

        # Compute means
        target_mean = target_cpm.mean(axis=1)
        control_mean = control_cpm.mean(axis=1)

        # Compute fold change (target / control)
        fc = target_mean / control_mean.replace(0, np.nan)
        log2fc = np.log2(fc)

        results = pd.DataFrame({
            'miRNA': target_mean.index,
            'target_mean_cpm': target_mean.values,
            'control_mean_cpm': control_mean.values,
            'fc': fc.values,
            'log2fc': log2fc.values,
        })

        # Classify direction
        results['direction'] = 'stable'
        results.loc[results['fc'] >= self.min_fc, 'direction'] = 'UP_in_target'
        results.loc[results['fc'] <= self.min_off_fc, 'direction'] = 'DOWN_in_target'

        return results.dropna(subset=['fc']).sort_values('fc', ascending=False)

    def find_on_candidates(self, fc_results, mode='senolytic'):
        """Find ON-switch candidates (miRNAs high in target, low in control).

        For senolytic mode: miRNAs UP in senescent cells
        For cancer mode: miRNAs UP in cancer cells
        """
        candidates = fc_results[
            (fc_results['direction'] == 'UP_in_target') &
            (fc_results['target_mean_cpm'] >= self.min_expression)
        ].copy()

        candidates['discrimination'] = candidates['fc']
        candidates['switch_type'] = 'ON'
        candidates['role'] = 'Activates payload when this miRNA is present (high in target cells)'

        # Flag known senescence miRNAs
        if mode == 'senolytic':
            candidates['known_senescence'] = candidates['miRNA'].apply(
                lambda x: self._match_known(x, self.KNOWN_SENESCENCE_UP)
            )
        else:
            candidates['known_senescence'] = 'N/A (cancer mode)'

        return candidates.sort_values('discrimination', ascending=False)

    def find_off_candidates(self, fc_results, mode='senolytic'):
        """Find OFF-switch candidates (miRNAs high in control, low in target).

        These protect non-target cells: L7Ae is produced when the miRNA is present,
        repressing the payload. In target cells where the miRNA is low, L7Ae is
        not produced and the payload is expressed.
        """
        candidates = fc_results[
            (fc_results['direction'] == 'DOWN_in_target') &
            (fc_results['control_mean_cpm'] >= self.min_healthy_expr)
        ].copy()

        # Discrimination = how much more L7Ae is produced in control vs target
        candidates['discrimination'] = 1.0 / candidates['fc']
        candidates['switch_type'] = 'OFF'
        candidates['role'] = 'Protects non-target cells; L7Ae produced when this miRNA is high'

        # Flag known senescence miRNAs
        if mode == 'senolytic':
            candidates['known_senescence'] = candidates['miRNA'].apply(
                lambda x: self._match_known(x, self.KNOWN_SENESCENCE_DOWN)
            )
        else:
            candidates['known_senescence'] = 'N/A (cancer mode)'

        return candidates.sort_values('discrimination', ascending=False)

    def find_cancer_detarget_candidates(self, fc_results, tissue_profiles=None):
        """For cancer mode: find tissue-specific miRNAs for de-targeting.

        These are miRNAs that are HIGH in specific normal tissues but LOW in cancer.
        They protect that tissue from off-target killing.

        Parameters
        ----------
        fc_results : DataFrame
            FC results from cancer vs. each tissue
        tissue_profiles : dict
            {tissue_name: DataFrame} of miRNA expression in each tissue
        """
        if tissue_profiles is None:
            return self.find_off_candidates(fc_results, mode='cancer')

        detarget = []
        for tissue_name, tissue_df in tissue_profiles.items():
            tissue_mean = tissue_df.mean(axis=1) if isinstance(tissue_df, pd.DataFrame) else tissue_df

            for mirna in fc_results['miRNA']:
                if mirna in tissue_mean.index:
                    tissue_expr = tissue_mean[mirna]
                    cancer_row = fc_results[fc_results['miRNA'] == mirna]
                    if len(cancer_row) > 0:
                        cancer_expr = cancer_row.iloc[0]['target_mean_cpm']
                        if tissue_expr > self.min_healthy_expr and cancer_expr < tissue_expr * self.min_off_fc:
                            detarget.append({
                                'miRNA': mirna,
                                'tissue': tissue_name,
                                'tissue_cpm': tissue_expr,
                                'cancer_cpm': cancer_expr,
                                'fc_tissue_over_cancer': tissue_expr / max(cancer_expr, 0.1),
                                'switch_type': 'OFF (de-target)',
                                'role': f'Protects {tissue_name}; L7Ae produced when present',
                            })

        return pd.DataFrame(detarget).sort_values('fc_tissue_over_cancer', ascending=False) if detarget else pd.DataFrame()

    def design_circuits(self, on_candidates, off_candidates, max_on=3, max_off=3, max_total_inputs=3):
        """Generate and rank circuit designs from candidate lists.

        Each circuit uses the L7Ae-only AND gate:
        - Multiple L7Ae mRNAs, each controlled by a different miRNA
        - One payload mRNA with K-turn in 5'UTR

        Parameters
        ----------
        on_candidates : DataFrame
            ON-switch candidates (sorted by discrimination)
        off_candidates : DataFrame
            OFF-switch candidates (sorted by discrimination)
        max_on : int
            Maximum ON-switch inputs to consider
        max_off : int
            Maximum OFF-switch inputs to consider
        max_total_inputs : int
            Maximum total inputs per circuit

        Returns
        -------
        List of circuit design dicts, sorted by estimated selectivity
        """
        circuits = []

        top_on = on_candidates.head(max_on)
        top_off = off_candidates.head(max_off)

        # Generate all combinations up to max_total_inputs
        from itertools import combinations

        all_inputs = []
        for _, row in top_on.iterrows():
            all_inputs.append({
                'miRNA': row['miRNA'],
                'type': 'ON',
                'discrimination': row['discrimination'],
                'target_cpm': row['target_mean_cpm'],
                'control_cpm': row['control_mean_cpm'],
            })
        for _, row in top_off.iterrows():
            all_inputs.append({
                'miRNA': row['miRNA'],
                'type': 'OFF',
                'discrimination': row['discrimination'],
                'target_cpm': row.get('target_mean_cpm', 0),
                'control_cpm': row.get('control_mean_cpm', 0),
            })

        # Generate circuits with 1 to max_total_inputs inputs
        for n_inputs in range(1, min(max_total_inputs + 1, len(all_inputs) + 1)):
            for combo in combinations(range(len(all_inputs)), n_inputs):
                inputs = [all_inputs[i] for i in combo]

                # Must have at least one ON switch
                n_on = sum(1 for inp in inputs if inp['type'] == 'ON')
                if n_on == 0:
                    continue

                # Compute estimated selectivity (multiplicative)
                selectivity = 1.0
                for inp in inputs:
                    selectivity *= inp['discrimination']

                # Count mRNAs needed (one L7Ae per input + one payload)
                n_mrnas = len(inputs) + 1

                circuit = {
                    'inputs': inputs,
                    'n_on': n_on,
                    'n_off': len(inputs) - n_on,
                    'n_mrnas': n_mrnas,
                    'estimated_selectivity': selectivity,
                    'mirnas': [inp['miRNA'] for inp in inputs],
                    'input_types': [inp['type'] for inp in inputs],
                }
                circuits.append(circuit)

        # Sort by selectivity
        circuits.sort(key=lambda x: x['estimated_selectivity'], reverse=True)
        return circuits

    def generate_report(self, fc_results, on_candidates, off_candidates, circuits,
                        mode='senolytic', output_path=None):
        """Generate a Markdown report of the analysis and recommendations."""
        lines = []
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

        lines.append(f'# Circuit Design Report\n')
        lines.append(f'*Generated: {timestamp}*\n')
        lines.append(f'*Mode: {mode}*\n\n')
        lines.append('---\n\n')

        # Summary stats
        n_up = (fc_results['direction'] == 'UP_in_target').sum()
        n_down = (fc_results['direction'] == 'DOWN_in_target').sum()
        n_stable = (fc_results['direction'] == 'stable').sum()
        lines.append(f'## 1. Data Summary\n\n')
        lines.append(f'- Total miRNAs analyzed: {len(fc_results)}\n')
        lines.append(f'- Upregulated in target: {n_up}\n')
        lines.append(f'- Downregulated in target: {n_down}\n')
        lines.append(f'- Stable: {n_stable}\n\n')

        # Thresholds
        lines.append(f'## 2. Thresholds Used\n\n')
        lines.append(f'| Parameter | Value |\n')
        lines.append(f'|-----------|-------|\n')
        lines.append(f'| Minimum target expression (ON switch) | {self.min_expression} CPM |\n')
        lines.append(f'| Minimum control expression (OFF switch) | {self.min_healthy_expr} CPM |\n')
        lines.append(f'| Minimum fold change (ON) | {self.min_fc}x |\n')
        lines.append(f'| Maximum fold change (OFF) | {self.min_off_fc}x |\n\n')

        # ON candidates
        lines.append(f'## 3. ON-Switch Candidates (Upregulated in Target)\n\n')
        if len(on_candidates) > 0:
            lines.append(f'| Rank | miRNA | Target CPM | Control CPM | FC | Discrimination |\n')
            lines.append(f'|------|-------|-----------|------------|-----|---------------|\n')
            for i, (_, row) in enumerate(on_candidates.head(10).iterrows(), 1):
                lines.append(f'| {i} | {row["miRNA"]} | {row["target_mean_cpm"]:.0f} | '
                            f'{row["control_mean_cpm"]:.0f} | {row["fc"]:.2f}x | {row["discrimination"]:.2f}x |\n')
        else:
            lines.append('No ON-switch candidates found meeting thresholds.\n')
        lines.append('\n')

        # OFF candidates
        lines.append(f'## 4. OFF-Switch Candidates (Downregulated in Target)\n\n')
        if len(off_candidates) > 0:
            lines.append(f'| Rank | miRNA | Target CPM | Control CPM | FC | Discrimination |\n')
            lines.append(f'|------|-------|-----------|------------|-----|---------------|\n')
            for i, (_, row) in enumerate(off_candidates.head(10).iterrows(), 1):
                lines.append(f'| {i} | {row["miRNA"]} | {row["target_mean_cpm"]:.0f} | '
                            f'{row["control_mean_cpm"]:.0f} | {row["fc"]:.2f}x | {row["discrimination"]:.2f}x |\n')
        else:
            lines.append('No OFF-switch candidates found meeting thresholds.\n')
        lines.append('\n')

        # Circuit designs
        lines.append(f'## 5. Recommended Circuit Designs\n\n')
        lines.append('All designs use the L7Ae-only AND gate architecture:\n')
        lines.append('each input miRNA controls a separate L7Ae mRNA. The payload\n')
        lines.append('mRNA has a K-turn in its 5\'UTR. All L7Ae sources must be\n')
        lines.append('eliminated for payload expression.\n\n')

        lines.append('**Selectivity estimates are approximate** (multiplicative model;\n')
        lines.append('actual response is nonlinear/sigmoidal). Use for ranking, not prediction.\n\n')

        for i, circuit in enumerate(circuits[:10], 1):
            on_names = [inp['miRNA'] for inp in circuit['inputs'] if inp['type'] == 'ON']
            off_names = [inp['miRNA'] for inp in circuit['inputs'] if inp['type'] == 'OFF']

            lines.append(f'### Design {i}: {" + ".join(circuit["mirnas"])}\n\n')
            lines.append(f'| Property | Value |\n')
            lines.append(f'|----------|-------|\n')
            lines.append(f'| ON inputs | {", ".join(on_names) if on_names else "None"} |\n')
            lines.append(f'| OFF inputs | {", ".join(off_names) if off_names else "None"} |\n')
            lines.append(f'| Total mRNAs | {circuit["n_mrnas"]} ({circuit["n_on"]} ON + {circuit["n_off"]} OFF + 1 payload) |\n')
            lines.append(f'| Estimated selectivity | ~{circuit["estimated_selectivity"]:.1f}x |\n\n')

            lines.append('| miRNA | Type | Target CPM | Control CPM | Discrimination |\n')
            lines.append('|-------|------|-----------|------------|---------------|\n')
            for inp in circuit['inputs']:
                lines.append(f'| {inp["miRNA"]} | {inp["type"]} | {inp["target_cpm"]:.0f} | '
                            f'{inp["control_cpm"]:.0f} | {inp["discrimination"]:.2f}x |\n')
            lines.append('\n---\n\n')

        # Caveats
        lines.append('## 6. Important Caveats\n\n')
        lines.append('1. **Selectivity estimates are order-of-magnitude approximations.** The actual\n')
        lines.append('   miRNA-to-switch response is sigmoidal, not linear (Mukherji et al., Nature, 2011).\n')
        lines.append('   Small fold changes may produce binary or no response depending on threshold position.\n\n')
        lines.append('2. **CPM normalization corrects for library size but not composition bias.** TMM or\n')
        lines.append('   DESeq2 normalization is recommended for formal analysis.\n\n')
        lines.append('3. **Sequencing counts are not copies per cell.** Absolute intracellular abundance\n')
        lines.append('   depends on ligation bias, extraction efficiency, and cell number input.\n\n')
        lines.append('4. **Empirical validation is required.** Test with fluorescent reporter before\n')
        lines.append('   switching to cytotoxic payload.\n\n')

        report = ''.join(lines)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)

        return report

    def analyze(self, target_df, control_df, mode='senolytic', normalize=True,
                tissue_profiles=None, output_path=None):
        """Run the full analysis pipeline.

        Parameters
        ----------
        target_df : DataFrame
            miRNA counts for target cells (rows=miRNAs, cols=replicates)
        control_df : DataFrame
            miRNA counts for control/healthy cells
        mode : str
            'senolytic' or 'cancer'
        normalize : bool
            If True, apply CPM normalization
        tissue_profiles : dict, optional
            For cancer mode: {tissue_name: DataFrame} for de-targeting analysis
        output_path : str, optional
            Path to save the report

        Returns
        -------
        dict with keys: fc_results, on_candidates, off_candidates, circuits, report
        """
        print(f'Circuit Designer - Mode: {mode}')
        print(f'Target samples: {target_df.shape[1]}, Control samples: {control_df.shape[1]}')
        print(f'miRNAs: {target_df.shape[0]}')

        # Step 1: Compute fold changes
        print('\n[1/4] Computing fold changes...')
        fc_results = self.compute_fold_changes(target_df, control_df, normalize=normalize)
        n_up = (fc_results['direction'] == 'UP_in_target').sum()
        n_down = (fc_results['direction'] == 'DOWN_in_target').sum()
        print(f'  {n_up} UP in target, {n_down} DOWN in target')

        # Step 2: Find candidates
        print('[2/4] Identifying candidates...')
        on_candidates = self.find_on_candidates(fc_results, mode=mode)
        off_candidates = self.find_off_candidates(fc_results, mode=mode)
        print(f'  {len(on_candidates)} ON-switch candidates')
        print(f'  {len(off_candidates)} OFF-switch candidates')

        # Step 3: Design circuits
        print('[3/4] Designing circuits...')
        circuits = self.design_circuits(on_candidates, off_candidates)
        print(f'  {len(circuits)} circuit designs generated')

        # Step 4: Generate report
        print('[4/4] Generating report...')
        report = self.generate_report(fc_results, on_candidates, off_candidates,
                                       circuits, mode=mode, output_path=output_path)

        if output_path:
            print(f'\nReport saved to: {output_path}')

        # Print top designs
        print(f'\nTop 3 circuit designs:')
        for i, circuit in enumerate(circuits[:3], 1):
            names = " + ".join(circuit['mirnas'])
            print(f'  {i}. {names} (~{circuit["estimated_selectivity"]:.1f}x selectivity, '
                  f'{circuit["n_mrnas"]} mRNAs)')

        return {
            'fc_results': fc_results,
            'on_candidates': on_candidates,
            'off_candidates': off_candidates,
            'circuits': circuits,
            'report': report,
        }

    def _match_known(self, mirna_name, known_dict):
        """Check if a miRNA matches any in the known senescence dict."""
        clean = mirna_name.replace('hsa-', '').replace('mmu-', '').replace('rno-', '')
        for known, info in known_dict.items():
            if clean == known or known in clean:
                return f'{info["confidence"]}: {info["note"]}'
        return ''


def load_count_matrix(filepath, mirna_col=None):
    """Load a miRNA count matrix from CSV/TSV/Excel.

    Expects rows = miRNAs, columns = samples.
    First column (or mirna_col) is used as index.
    """
    if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
        df = pd.read_excel(filepath, engine='openpyxl')
    elif filepath.endswith('.tsv') or '\t' in open(filepath).readline():
        df = pd.read_csv(filepath, sep='\t')
    else:
        df = pd.read_csv(filepath)

    if mirna_col:
        df = df.set_index(mirna_col)
    else:
        df = df.set_index(df.columns[0])

    # Ensure numeric
    df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all')
    return df


def main():
    parser = argparse.ArgumentParser(
        description='miRNA Logic Gate Circuit Designer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Senolytic mode: senescent vs healthy fibroblasts
  python circuit_designer.py --target senescent_counts.csv --control healthy_counts.csv --mode senolytic

  # Cancer mode: 4T1 cells vs normal tissues
  python circuit_designer.py --target 4T1_counts.csv --control tissue_counts.csv --mode cancer

  # With custom thresholds
  python circuit_designer.py --target target.csv --control ctrl.csv --min-expression 100 --min-fc 1.5
        """
    )
    parser.add_argument('--target', required=True, help='CSV/TSV of target cell miRNA counts')
    parser.add_argument('--control', required=True, help='CSV/TSV of control cell miRNA counts')
    parser.add_argument('--mode', choices=['senolytic', 'cancer'], default='senolytic',
                        help='Analysis mode (default: senolytic)')
    parser.add_argument('--output', default='circuit_design_report.md', help='Output report path')
    parser.add_argument('--min-expression', type=float, default=50, help='Min CPM in target for ON switch')
    parser.add_argument('--min-healthy-expr', type=float, default=100, help='Min CPM in control for OFF switch')
    parser.add_argument('--min-fc', type=float, default=1.3, help='Min fold change for ON switch')
    parser.add_argument('--min-off-fc', type=float, default=0.7, help='Max fold change for OFF switch')
    parser.add_argument('--no-normalize', action='store_true', help='Skip CPM normalization (data is pre-normalized)')
    parser.add_argument('--mirna-col', default=None, help='Column name containing miRNA IDs')

    args = parser.parse_args()

    # Load data
    print(f'Loading target data: {args.target}')
    target_df = load_count_matrix(args.target, mirna_col=args.mirna_col)
    print(f'Loading control data: {args.control}')
    control_df = load_count_matrix(args.control, mirna_col=args.mirna_col)

    # Align miRNAs
    common = target_df.index.intersection(control_df.index)
    print(f'Common miRNAs: {len(common)}')
    target_df = target_df.loc[common]
    control_df = control_df.loc[common]

    # Run analysis
    designer = CircuitDesigner(
        min_expression=args.min_expression,
        min_healthy_expr=args.min_healthy_expr,
        min_fc=args.min_fc,
        min_off_fc=args.min_off_fc,
    )

    results = designer.analyze(
        target_df, control_df,
        mode=args.mode,
        normalize=not args.no_normalize,
        output_path=args.output,
    )

    print(f'\nDone. Report saved to {args.output}')


if __name__ == '__main__':
    main()
