# Circuit Designer Tool

Recommends L7Ae-based miRNA-sensing logic gate circuit designs from miRNA expression data.

## Quick Start

```bash
# Cancer targeting: kill 4T1 cells, spare normal tissues
python circuit_designer.py --target 4T1_counts.csv --control tissue_counts.csv --mode cancer

# Senolytic: kill senescent cells, spare healthy
python circuit_designer.py --target senescent_counts.csv --control healthy_counts.csv --mode senolytic
```

## Input Format

Two CSV/TSV files with miRNA counts:
- Rows = miRNAs (first column = miRNA names)
- Columns = replicate samples
- Values = raw read counts (CPM normalization applied automatically) or pre-normalized values (use `--no-normalize`)

## What It Does

1. CPM-normalizes raw counts (corrects for library size differences)
2. Computes fold changes between target and control conditions
3. Identifies ON-switch candidates (miRNAs UP in target cells)
4. Identifies OFF-switch candidates (miRNAs DOWN in target cells, HIGH in control)
5. Generates all 1-3 input circuit combinations using L7Ae AND-gate architecture
6. Ranks circuits by estimated selectivity
7. Outputs a Markdown report with tables, caveats, and recommendations

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--min-expression` | 50 CPM | Minimum expression in target cells for ON switch |
| `--min-healthy-expr` | 100 CPM | Minimum expression in control cells for OFF switch |
| `--min-fc` | 1.3x | Minimum fold change to consider as ON candidate |
| `--min-off-fc` | 0.7x | Maximum fold change for OFF candidate (must be below) |
| `--no-normalize` | False | Skip CPM normalization if data is pre-normalized |

## Circuit Architecture

All designs use L7Ae/K-turn repression with multiple L7Ae mRNAs:

```
L7Ae-mRNA-1: [MREs for miRNA-A] - L7Ae CDS
L7Ae-mRNA-2: [MREs for miRNA-B] - L7Ae CDS  
Payload-mRNA: [K-turn in 5'UTR] - Gasdermin or DTA CDS
```

Both miRNA inputs must be active to silence all L7Ae and permit payload expression.

## Caveats

- Selectivity estimates are multiplicative approximations (actual response is sigmoidal)
- CPM corrects library size but not composition bias
- Sequencing counts are not copies per cell
- Empirical validation with fluorescent reporter is required before cytotoxic payload
