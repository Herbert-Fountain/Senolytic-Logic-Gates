# Senolytic RNA Logic Gate Technology

Computational tools and literature analysis for designing miRNA-sensing mRNA logic gate circuits that selectively kill senescent cells while sparing healthy tissue.

## Project Overview

This project develops tools to support the design of synthetic mRNA-based Boolean logic circuits delivered via lipid nanoparticles (LNPs). These circuits sense endogenous microRNA (miRNA) profiles within cells and conditionally express cytotoxic payloads (Gasdermin or Diphtheria Toxin A) only in senescent cells. The approach is based on the miRNA-responsive mRNA switch framework developed by [Hirohide Saito's laboratory](https://www.cira.kyoto-u.ac.jp/e/research/saito_summary.html) at Kyoto University.

### How It Works

1. **OFF switch**: An mRNA encoding a repressor protein (L7Ae) contains miRNA response elements (MREs). If the cognate miRNA is present, L7Ae is NOT translated.
2. **Output mRNA**: Encodes the cytotoxic payload with a K-turn motif in its 5' UTR. L7Ae protein blocks translation of this mRNA.
3. **AND gate logic**: When both input miRNAs are present (indicating a senescent cell), both repressors are knocked down, and the payload is expressed. In healthy cells lacking these miRNAs, the repressors remain active and the payload stays OFF.

### Current Status

- **Validated**: miR-122-5p ON switch system in miR-122-positive (HuH7) vs. miR-122-negative (NIH 4T1) cell lines
- **In progress**: Identifying optimal miRNA inputs for senescence-specific circuit design
- **Planned**: Doxorubicin-induced senescence small RNA-seq in mice and human primary dermal fibroblasts

## Repository Structure

```
Senolytic-Logic-Gates/
├── README.md                          # This file
├── literature/
│   ├── saito_logic_gates_review.md    # Review of Saito lab's mRNA circuit papers
│   └── senescence_mirna_review.md     # Review of senescence miRNA profiling studies
├── data/
│   ├── README.md                      # Data sources, provenance, and access details
│   ├── GSE94410/                      # HUVEC replicative senescence (Terlecki-Zaniewicz 2018)
│   │   ├── GSE94410_CountTable.txt    # Raw miRNA counts (2,578 miRNAs × 15 samples)
│   │   └── analysis_notes.md          # Analysis of candidate miRNAs in this dataset
│   └── GSE27404/                      # IMR90 replicative senescence (Dhahbi 2011)
│       └── (to be downloaded)
├── analysis/
│   ├── GSE94410_candidate_analysis.md # Detailed writeup of GSE94410 findings
│   └── (future analyses)
├── docs/
│   └── (project documentation)
└── tools/
    └── (circuit design tools — in development)
```

## Key Findings So Far

### 1. Senescence miRNA signatures are highly cell-type specific
The Weigl/Grillari 2024 study profiled 5 human cell types under doxorubicin-induced senescence and found that most regulated miRNAs were unique to individual cell types. Our re-analysis of GSE94410 (HUVEC data) confirms this: many literature-reported "senescence miRNAs" show the **opposite** pattern or are not expressed at all in endothelial cells.

### 2. Fold change ≠ functional utility for circuit design
Several miRNAs reported as senescence biomarkers with large fold changes have extremely low absolute counts (< 10 reads). A miRNA at 2 counts going to 20 counts is a "10-fold increase" but utterly useless as a switch input because there aren't enough molecules to reliably engage the mRNA circuit. Absolute intracellular abundance matters more than relative change.

### 3. Intracellular vs. secreted miRNA distinction is critical
Senescent cells secrete 4x more extracellular vesicles than healthy cells, and >80% of miRNA species are enriched in these vesicles. For circuit design, we need miRNAs that are **retained intracellularly** in senescent cells (e.g., miR-21-3p, miR-17-3p), not those that are packaged and exported.

### 4. No hard miRNA expression threshold exists for switch activation
The Saito lab explicitly states that the system depends on the ratio of endogenous miRNA to delivered switch mRNA, and no quantitative copies-per-cell threshold has been defined. This means empirical optimization is required for each miRNA input.

## Data Sources

| Dataset | GEO Accession | Cell Type | Senescence Inducer | Method | Status |
|---------|--------------|-----------|-------------------|--------|--------|
| Terlecki-Zaniewicz 2018 | [GSE94410](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE94410) | HUVEC | Replicative | small RNA-seq | Downloaded, analyzed |
| Dhahbi 2011 | [GSE27404](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE27404) | IMR90 | Replicative | small RNA-seq | To download |
| Weigl/Grillari 2024 | TBD | 5 human primary types | Doxorubicin | small RNA-seq | Preprint, data TBD |
| Casella 2019 | [GSE130727](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE130727) | WI-38, IMR-90, HUVEC | Multiple (incl. dox) | mRNA-seq | Reference |

## References

See [literature/](literature/) for detailed reviews with full citations.

## License

This project is for academic research purposes.

## Contact

Herbert Fountain — Cornell University
