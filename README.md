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
├── README.md
├── literature/
│   ├── saito_logic_gates_review.md          # Saito lab mRNA circuit papers (7 papers)
│   ├── senescence_mirna_review.md           # Senescence miRNA profiling studies (12 studies)
│   ├── aging_mirna_datasets.md              # Natural aging miRNA-seq datasets (14 datasets)
│   ├── human_senescence_datasets.md         # Human senescence miRNA-seq catalog
│   ├── human_aging_tissue_mirna_datasets.md # Human aging tissue datasets (incl. GTEx)
│   └── chemotherapy_patient_mirna_datasets.md # Chemo patient miRNA-seq gap analysis
├── data/
│   ├── README.md                            # Data provenance documentation
│   ├── GSE94410/                            # HUVEC replicative senescence (human)
│   ├── GSE299871/                           # WI-38 DXR/SDS/RS senescence (human)
│   ├── GSE202120/                           # HAEC irradiation dose-response (human)
│   ├── GSE117818/                           # MRC-5 replicative senescence (human)
│   ├── GSE200330/                           # Synovial fibroblast EV irradiation (human)
│   ├── GSE217458/                           # Mouse 16-tissue aging (771 samples)
│   ├── GSE55164/                            # Mouse muscle aging
│   ├── GSE172269/                           # Rat 11-organ aging BodyMap (320 samples)
│   ├── GSE136926/                           # Human cardiac aging (ages 38-72)
│   ├── GSE111281/                           # Human skin aging (ages 24-80)
│   ├── GSE111174/                           # Human blood aging (ages 24-80)
│   ├── GSE182598/                           # Human plasma aging (n=103)
│   └── GSE27404/                            # IMR90 replicative senescence (BedGraph)
├── analysis/
│   ├── cross_study_synthesis.md             # Master synthesis (11 datasets, 43 refs)
│   ├── methods_and_statistical_framework.md # Best practices and guidelines
│   ├── normalization_corrections.md         # CPM corrections to raw FC estimates
│   ├── GSE299871_analysis.md                # WI-38 DXR/SDS/RS analysis
│   ├── GSE94410_analysis.md                 # HUVEC analysis
│   ├── GSE202120_analysis.md                # HAEC irradiation analysis
│   ├── GSE117818_analysis.md                # MRC-5 time course analysis
│   ├── GSE217458_analysis.md                # Mouse 16-tissue aging analysis
│   ├── GSE55164_analysis.md                 # Mouse muscle aging analysis
│   ├── GSE200330_analysis.md                # EV miRNA analysis
│   ├── GSE172269_analysis.md                # Rat BodyMap analysis
│   ├── GSE136926_analysis.md                # Human cardiac aging analysis
│   └── GSE111281_GSE111174_analysis.md      # Human skin + blood aging analysis
└── tools/
    └── (circuit design tools - in development)
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

## Data Sources (11 Datasets Analyzed)

| # | Dataset | GEO | Cell/Tissue | Context | Organism | Samples |
|---|---------|-----|------------|---------|----------|---------|
| 1 | RNA Biology 2025 | GSE299871 | WI-38 fibroblasts | DXR, SDS, RS senescence | Human | 36 |
| 2 | Terlecki-Zaniewicz 2018 | GSE94410 | HUVECs | Replicative senescence | Human | 15 |
| 3 | Engel 2022 | GSE202120 | HAECs | Irradiation (0-10 Gy) | Human | 35 |
| 4 | JenAge | GSE117818 | MRC-5 fibroblasts | Replicative senescence | Human | 15 |
| 5 | Peiris 2022 | GSE200330 | Synovial fibroblast EVs | Irradiation | Human | 6 |
| 6 | Wagner 2024 | GSE217458 | 16 mouse tissues | Natural aging | Mouse | 771 |
| 7 | Kim 2014 | GSE55164 | Mouse muscle | Natural aging | Mouse | 12 |
| 8 | Bushel 2022 | GSE172269 | 11 rat organs (incl. liver, kidney) | Natural aging | Rat | 320 |
| 9 | Ma 2019 | GSE136926 | Human right atrium | Natural aging (38-72yr) | Human | 12 |
| 10 | JenAge | GSE111281 | Human skin | Natural aging (24-80yr) | Human | 30 |
| 11 | JenAge | GSE111174 | Human blood | Natural aging (24-80yr) | Human | 30 |

## References

See [literature/](literature/) for detailed reviews with full citations.

## License

This project is for academic research purposes.

## Contact

Herbert Fountain - Cornell University
