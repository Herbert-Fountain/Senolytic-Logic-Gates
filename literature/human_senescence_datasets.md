# Human Senescence and Aging miRNA-Seq Datasets
## Systematic Search Results

*Search date: 2026-04-06*

---

## Key Finding

**True small RNA-seq datasets from induced human cellular senescence are rare.** Most senescence miRNA studies used microarrays or qPCR panels. No public small RNA-seq dataset was found specifically for doxorubicin-induced senescence in human cells.

---

## Confirmed Small RNA-Seq Datasets

### GSE94410 — HUVEC Replicative Senescence *(Already analyzed)*

| Parameter | Details |
|-----------|---------|
| Cell type | HUVECs |
| Inducer | Replicative |
| Samples | 15 (4 passage stages) |
| Count data | YES — raw counts available |
| Status | **Downloaded and analyzed** |

See: [analysis/GSE94410_analysis.md](../analysis/GSE94410_analysis.md)

---

### GSE27404 — IMR90 Replicative Senescence

| Parameter | Details |
|-----------|---------|
| Cell type | IMR90 human lung fibroblasts |
| Inducer | Replicative (passage 14 vs 34) |
| Samples | 2 (young vs senescent) — **n=1 per condition** |
| Count data | Only BedGraph genomic coordinates; miRNA counts in paper supplementary tables (DOC format, behind PMC paywall) |
| Citation | Dhahbi et al. *PLoS ONE*. 2011;6(5):e20509. PMID: [21637828](https://pubmed.ncbi.nlm.nih.gov/21637828/) |
| Status | **Downloaded but count table not extracted** — BedGraph files need re-processing or supplementary DOC needs manual extraction |

**Limitation:** n=1 per condition. No biological replicates.

---

### GSE189209 — Prostate Epithelial Cell Replicative Senescence

| Parameter | Details |
|-----------|---------|
| Cell type | Primary human prostate epithelial cells (PrECs) |
| Inducer | Replicative (passage 1 proliferative vs passage 7 senescent) |
| Samples | 4 miRNA-seq (2 active + 2 senescent) + 4 mRNA-seq |
| Method | TruSeq Small RNA Library, HiSeq2500, SE50 |
| Count data | **NO processed count files on GEO** — only raw SRA reads. Would need FASTQ → alignment → counting pipeline |
| Citation | Protopopov et al. *Genes*. 2022;13(2):208. PMID: [35205253](https://pubmed.ncbi.nlm.nih.gov/35205253/). PMC: [PMC8872619](https://pmc.ncbi.nlm.nih.gov/articles/PMC8872619/) |
| Key findings | 97 differentially expressed miRNAs |
| Status | **Not downloaded** — requires re-processing from raw FASTQ |

**Note:** This is one of the few datasets from epithelial cells (not fibroblasts or endothelial). Epithelial senescence may have different miRNA profiles.

---

### GSE200330 — Irradiation-Induced Senescence in Synovial Fibroblasts (EV miRNAs)

| Parameter | Details |
|-----------|---------|
| Cell type | Human synovial fibroblasts (from OA patients) |
| Inducer | Irradiation (10 Gy) |
| What was sequenced | **Extracellular vesicle (EV) small RNA**, NOT intracellular |
| Samples | Non-senescent vs senescent EV cargo |
| Citation | Peiris et al. *Front Mol Biosci*. 2022. PMID: [36213127](https://pubmed.ncbi.nlm.nih.gov/36213127/) |
| Key findings | 17 DE miRNAs in EVs |
| Status | **Not downloaded** |

**Important caveat:** This dataset profiles EV-associated miRNAs, not intracellular miRNAs. For circuit design, we need intracellular levels. However, this is relevant for understanding which miRNAs are secreted vs retained (cf. Terlecki-Zaniewicz 2019 finding that miR-21-3p is retained intracellularly).

---

## Confirmed mRNA-Seq Datasets (NOT miRNA-seq, but relevant context)

### GSE130727 — Multi-Model Senescence Transcriptome

| Parameter | Details |
|-----------|---------|
| Cell types | WI-38, IMR-90 fibroblasts; HUVECs, HAECs |
| Inducers | Replicative, ionizing radiation, **doxorubicin**, oncogene (HRAS-G12V) |
| Method | Total RNA-seq (rRNA-depleted) — **NOT small RNA-seq** |
| GEO | [GSE130727](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE130727) |
| Citation | Casella et al. *Nucleic Acids Res*. 2019;47(14):7294-7305. PMID: [31251810](https://pubmed.ncbi.nlm.nih.gov/31251810/) |

**Why this matters:** Includes doxorubicin-induced senescence in fibroblasts — the same conditions Herbert plans. While it's mRNA-seq (not miRNA), the transcriptome data could validate predicted miRNA targets.

### GSE280381 — Doxorubicin Therapy-Induced Senescence in Breast Cancer

| Parameter | Details |
|-----------|---------|
| Cell types | MCF7, T47D, MDA-MB-231, Hs578T |
| Inducer | High-dose doxorubicin |
| Method | Bulk RNA-seq + scRNA-seq — **NOT small RNA-seq** |
| GEO | [GSE280381](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE280381) |

---

## Human Aging Tissue miRNA-Seq Datasets

### GSE55164 — Human Skeletal Muscle Aging

| Parameter | Details |
|-----------|---------|
| Tissue | Gastrocnemius skeletal muscle |
| Ages | Young vs aged human donors |
| Method | Small RNA-seq |
| Samples | n=6 per group (12 total) |
| Key findings | 15 up, 19 down-regulated miRNAs |
| Citation | Kim et al. *Aging*. 2014;6(7):524-544. PMID: [25063768](https://pubmed.ncbi.nlm.nih.gov/25063768/) |

### Human Skin Aging miRNA (Multiple GSEs)

| GEO Accessions | GSE31037, GSE72193, GSE84193, GSE142582 |
|----------------|----------------------------------------|
| Tissue | Human skin biopsies |
| Ages | 18-83 years across studies |
| Method | Small RNA-seq |
| Samples | ~72 subjects total |
| Citation | Sola-Garcia et al. *Arch Dermatol Res*. 2024. PMID: [38822910](https://pubmed.ncbi.nlm.nih.gov/38822910/) |

---

## Datasets Previously Misidentified as Small RNA-Seq

### GSE64553 — HFF/MRC5 Replicative Senescence Time Course

**This was initially identified as small RNA-seq but is actually mRNA-seq.** Contains protein-coding gene expression from HFF fibroblasts at 6 population doublings and MRC5 fibroblasts at 4 population doublings, with/without rotenone treatment. Despite being mRNA-seq, the time course design (PD22→PD74 for HFF) with 3 replicates per condition is valuable for understanding gene expression trajectories during senescence.

| Parameter | Details |
|-----------|---------|
| GEO | [GSE64553](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE64553) |
| Cell types | HFF (human foreskin fibroblasts), MRC5 (human lung fibroblasts) |
| Method | **mRNA-seq** (HiSeq2000, 50bp SE) — NOT small RNA-seq |
| Citation | Marthandan et al. *PLoS ONE*. 2016. PMID: [27128674](https://pubmed.ncbi.nlm.nih.gov/27128674/) |

---

## Summary: Usable Small RNA-Seq Datasets for Our Project

| Priority | Dataset | Cell Type | Inducer | Count Data Available | Status |
|----------|---------|-----------|---------|---------------------|--------|
| **1** | GSE94410 | HUVEC | Replicative | YES | **Analyzed** |
| **2** | GSE189209 | Prostate epithelial | Replicative | Raw FASTQ only | Needs processing |
| **3** | GSE27404 | IMR90 fibroblast | Replicative | BedGraph only (n=1) | Needs processing |
| **4** | GSE200330 | Synovial fibroblast EVs | Irradiation | On GEO | Not downloaded |
| — | **None** | **Any** | **Doxorubicin** | — | **DOES NOT EXIST** |

**The critical gap remains: there is no public small RNA-seq dataset for doxorubicin-induced senescence in any human cell type.** Herbert's planned experiment will be the first.

---

## References

1. Terlecki-Zaniewicz L et al. *Redox Biology*. 2018;18:77-83. PMC: PMC6037909
2. Dhahbi JM et al. *PLoS ONE*. 2011;6(5):e20509. PMID: 21637828
3. Protopopov AI et al. *Genes*. 2022;13(2):208. PMID: 35205253
4. Peiris HN et al. *Front Mol Biosci*. 2022. PMID: 36213127
5. Casella G et al. *Nucleic Acids Res*. 2019;47(14):7294-7305. PMID: 31251810
6. Marthandan S et al. *PLoS ONE*. 2016. PMID: 27128674
7. Kim JY et al. *Aging*. 2014;6(7):524-544. PMID: 25063768
8. Sola-Garcia A et al. *Arch Dermatol Res*. 2024. PMID: 38822910
