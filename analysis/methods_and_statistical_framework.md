# Methods and Statistical Framework
## Best Practices for Small RNA-Seq Re-Analysis Across Public Datasets

*Date: 2026-04-07*
*Addressing Peer Review Concerns #1 (normalization) and #2 (statistics)*

---

## 1. Purpose

This document establishes the methodological framework for our cross-dataset analysis of senescence and aging miRNA expression. It defines what comparisons are appropriate, what normalization and statistical methods are used, and what limitations apply. All methodological decisions are supported by published benchmarking studies and field guidelines.

## 2. Analysis Scope and Limitations

### 2.1 What We Are Doing

We are performing a **secondary analysis of published, processed small RNA-seq data** from public repositories (GEO). We did NOT generate any sequencing data, perform alignment, or run primary quantification pipelines. For each dataset, we start from the count tables or normalized expression matrices deposited by the original authors.

Our analysis has two goals:
1. **Within-dataset:** Identify miRNAs that change between senescent/aged and control/young conditions
2. **Cross-dataset:** Assess whether candidates show consistent directional changes across datasets, cell types, and organisms

### 2.2 What We Cannot Do

- **Cross-dataset quantitative comparison of absolute expression levels.** Different datasets used different library preparation kits, sequencing platforms, read depths, alignment tools, and normalization methods. Absolute miRNA counts are not comparable across datasets. We compare **directions of change** and **relative expression tiers** (high/medium/low/negligible), not absolute values.

- **Formal meta-analysis.** True meta-analysis requires either combining p-values (Fisher's method) or effect sizes (random-effects model) with study as a covariate. This requires consistent effect size estimates, which our heterogeneous dataset collection does not support. Our approach is a systematic **concordance analysis** — testing whether each candidate changes in the same direction across independent experiments.

These limitations are inherent to secondary analysis of published data and are standard in the field (Rossi et al., *PLoS Comput Biol*, 2021, DOI: 10.1371/journal.pcbi.1008608).

### 2.3 Sequencing Counts vs. Intracellular Copy Number

A critical assumption throughout this analysis is that sequencing counts correlate with intracellular miRNA copy number, which determines circuit activation potential. This relationship is complex and depends on RNA extraction efficiency, library prep biases, cell number input, and sequencing depth.

Published absolute quantification studies provide calibration points:
- miR-21 has been estimated at **2,000-10,000 copies per cell** in various cell lines (Bissels et al., *RNA*, 2009, PMID: 19850911; Leshkowitz et al., *RNA*, 2013, PMID: 23697550)
- miR-16 has been estimated at **~10,000-50,000 copies per cell** in lymphocytes (Lim et al., *Nucleic Acids Res*, 2011)
- Total miRNA content is estimated at **~100,000-200,000 copies per cell** in most cell types

In GSE299871 (WI-38 fibroblasts), miR-21-5p has ~66,000 CPM in controls. If this represents ~5,000 copies per cell (midpoint of published estimates), then 1 CPM ≈ 0.08 copies per cell. Under this rough calibration, miR-34a-5p at 558 CPM in DXR-senescent WI-38 cells would correspond to **~45 copies per cell** — substantially lower than the ~250 raw counts originally reported and potentially too few for reliable switch activation.

**This calibration is approximate** and varies by cell type, RNA extraction method, and library prep. It should not be treated as precise. However, it underscores that the absolute copy number question is even more challenging than raw count analysis suggests.

### 2.4 Ligation Bias Caveat

Small RNA-seq suffers from **ligation bias**: T4 RNA ligases ligate adapters with sequence-dependent efficiency, causing orders-of-magnitude variation in absolute quantification of individual miRNAs (Fuchs et al., *PLoS One*, 2015, PMID: 25942504; Jayaprakash et al., *Nucleic Acids Res*, 2011, PMC: PMC3241666; Giraldez et al., *Nat Biotechnol*, 2018, PMID: 30010675). This bias is **largely consistent within the same library preparation protocol**, so within-experiment fold changes remain valid. However, it means that:

- Absolute expression comparisons between miRNAs (e.g., "miR-34a has 250 counts while miR-22 has 7,000 counts") may reflect ligation efficiency differences rather than true abundance differences
- Cross-dataset comparisons of absolute levels are confounded by protocol-specific biases
- Our assessment of "sufficient expression for circuit activation" is approximate

## 3. Normalization

### 3.1 Recommended Methods

The benchmarking study by Tam et al. (*Briefings in Bioinformatics*, 2015, PMID: 25888698) evaluated eight normalization methods using spike-in dilution data and found that **TMM (Trimmed Mean of M-values)** and **Upper Quartile (UQ)** normalization produced the most accurate differential expression results. CPM (counts per million) showed increased variance, especially for low-abundance miRNAs. DESeq2's **median-of-ratios (RLE)** normalization performs comparably to TMM for balanced designs (Zhou et al., *RNA*, 2013, PMID: 23616640).

### 3.2 What We Applied

| Dataset | Data As Received | Our Normalization | Status |
|---------|-----------------|-------------------|--------|
| GSE299871 | Raw counts | CPM applied; DESeq2 recommended | **CPM corrections documented** |
| GSE94410 | Raw counts | CPM applied; DESeq2 recommended | **CPM corrections documented** |
| GSE202120 | Raw counts (Excel) | CPM recommended | Pending |
| GSE117818 | Raw counts (precursor IDs) | CPM recommended | Pending |
| GSE172269 | Raw counts | CPM recommended | Pending |
| GSE111281 | Raw counts (precursor IDs) | CPM recommended | Pending |
| GSE111174 | Raw counts (precursor IDs) | CPM recommended | Pending |
| GSE200330 | Raw reads + RPM (per-sample) | RPM provided by authors | Adequate |
| GSE217458 | RPMM (author-normalized) | None needed | Pre-normalized |
| GSE55164 | Log2 normalized (author) | None needed | Pre-normalized |
| GSE136926 | Normalized (author) | None needed | Pre-normalized |

### 3.3 Impact of Normalization

Our CPM analysis (see [normalization_corrections.md](normalization_corrections.md)) revealed that library size differences between conditions were substantial in some datasets:

- **GSE299871:** DXR samples had 1.6x larger libraries than controls, inflating all raw upregulation fold changes by ~1.6x and deflating all downregulation
- **GSE94410:** Senescent HUVEC samples had 0.53x the library size of young, inflating apparent downregulation and suppressing apparent upregulation

Key corrections:
- miR-29a-3p: **eliminated** as ON-switch candidate (raw 1.6x → CPM 0.96x)
- miR-21-5p: **eliminated** as ON-switch candidate (raw 1.8x → CPM 1.1x)
- miR-34a-5p: direction confirmed (raw 2.5x → CPM 1.5x)
- OFF-switch candidates **strengthened** after normalization

## 4. Statistical Testing

### 4.1 Field Guidelines

Schurch et al. (*RNA*, 2016, PMID: 27022035) established that:
- **Minimum 3 biological replicates** per condition are needed for DE analysis
- **6+ replicates** are recommended for robust detection of moderate fold changes
- With <12 replicates, **DESeq2 and edgeR** outperform other DE tools due to empirical Bayes shrinkage of dispersion estimates
- With n=2 per group, only genes with the **largest effect sizes** are reliably detectable

### 4.2 Applicability to Our Datasets

| Dataset | Replicates per Group | Formal DE Feasible? | Notes |
|---------|---------------------|--------------------|----|
| GSE299871 | n=2 | **Marginal** — DESeq2 can run but severely underpowered. Only largest effects detectable. | n=2 is below the Schurch et al. minimum of 3 |
| GSE94410 | n=3-4 | **Yes** — meets minimum threshold | S0 has 3, S1-S3 have 4 donors |
| GSE202120 | n=3 | **Yes** — meets minimum threshold | 3 replicates per dose/timepoint |
| GSE117818 | n=3 | **Yes** — meets minimum threshold | 3 replicates per PD stage |
| GSE172269 | n=8 (4M+4F) | **Yes** — well-powered | Could model sex as covariate |
| GSE111281 | n=6-9 | **Yes** — adequately powered | 4 age groups |
| GSE111174 | n=7 | **Yes** — adequately powered | 4 age groups |
| GSE136926 | n=3 | **Yes** — meets minimum threshold | 4 age groups |
| GSE217458 | n=up to 6/tissue/age | **Yes** — well-powered | 771 samples total |
| GSE200330 | n=3 | **Yes** — meets minimum threshold | 3 senescent + 3 control |
| GSE55164 | n=6 | **Yes** — adequately powered | 6 young + 6 aged |

### 4.3 What We Will Report

For datasets meeting the minimum replicate threshold (n≥3):
- **DESeq2** differential expression analysis with default settings (median-of-ratios normalization, Wald test, Benjamini-Hochberg FDR correction)
- Adjusted p-values (padj) with FDR < 0.05 significance threshold
- Log2 fold change estimates with shrinkage (apeglm method)

For datasets with n=2 (GSE299871):
- **Descriptive fold changes only** (CPM-normalized)
- No formal p-values reported
- Results labeled as "hypothesis-generating" in all reports
- The n=2 limitation is stated explicitly

### 4.4 Multiple Testing

For within-dataset DE analysis, DESeq2 applies **Benjamini-Hochberg** FDR correction internally.

For the cross-dataset concordance analysis (testing whether a miRNA is consistently UP or DOWN across datasets), we do NOT apply formal multiple testing correction because:
1. This is a hypothesis-generating analysis, not a hypothesis-testing one
2. Each dataset is independent, so the concordance pattern itself provides replication
3. A miRNA that is UP in 14/14 independent analyses does not require a p-value to be considered robust — the consistency IS the evidence

## 5. Cross-Dataset Concordance Analysis

### 5.1 Approach

For each candidate miRNA, we assess:
1. **Direction of change** in each dataset (UP / DOWN / STABLE, using CPM-normalized fold change where available)
2. **Consistency across datasets** — what fraction of analyses show the same direction?
3. **Absolute expression tier** — categorized as HIGH (>1,000 CPM), MEDIUM (100-1,000 CPM), LOW (10-100 CPM), or NEGLIGIBLE (<10 CPM)

We explicitly do NOT:
- Average fold changes across datasets
- Perform formal meta-analysis
- Compare absolute CPM values between datasets

### 5.2 Concordance Criteria

A candidate is classified as:
- **Consistent:** Same direction in ≥80% of applicable analyses
- **Partial:** Same direction in 50-80% of analyses
- **Inconsistent:** Same direction in <50% of analyses
- **Cell-type-dependent:** Consistent within a cell type but different between cell types

### 5.3 Handling Multi-Tissue Datasets

For datasets covering multiple tissues (GSE217458, GSE172269), we report **per-tissue fold changes individually** rather than averaging across tissues. The concordance assessment counts each tissue separately. When summarizing in tables, we indicate the range across tissues and note which tissues agree/disagree.

## 6. Data Provenance Standards

For each dataset, we document:
1. GEO accession and publication citation (PMID/DOI)
2. Download date and source URL
3. File names and formats
4. Sample-to-condition mapping with accession numbers
5. Original normalization method (if pre-normalized)
6. Our analysis code (Python, reproducible)

## 7. Quality Control

We apply the following QC checks where data permits:
- **Minimum expression filter:** Retain miRNAs with ≥10 counts in at least 2 samples (consistent with DESeq2 default independent filtering)
- **Library size assessment:** Report total mapped reads per sample and flag datasets with >2-fold library size differences between groups
- **Replicate consistency:** Note where within-group variance is high relative to between-group differences

## 8. Software and Versions

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.14 | Data manipulation and CPM normalization |
| pandas | 3.0.2 | Data frames |
| numpy | 2.4.4 | Numerical computation |
| openpyxl | 3.1.5 | Excel file reading |
| DESeq2 | (pending) | Formal DE analysis |

---

## References

1. Tam S et al. Optimization of miRNA-seq data preprocessing. *Brief Bioinform*. 2015;16(6):950-963. PMID: 25888698
2. Schurch NJ et al. How many biological replicates are needed in an RNA-seq experiment? *RNA*. 2016;22(6):839-851. PMID: 27022035
3. Love MI et al. Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biology*. 2014;15:550. PMID: 25516281
4. Zhou X et al. miRNA-Seq normalization comparisons need improvement. *RNA*. 2013;19(6):733-734. PMID: 23616640
5. Fuchs RT et al. Bias in ligation-based small RNA sequencing library construction. *PLoS One*. 2015;10(5):e0126049. PMID: 25942504
6. Jayaprakash AD et al. Identification and remediation of biases in RNA ligases in small-RNA deep sequencing. *Nucleic Acids Res*. 2011;39(21):e141
7. Giraldez MD et al. Comprehensive multi-center assessment of small RNA-seq methods. *Nat Biotechnol*. 2018;36:746-757. PMID: 30010675
8. Wright C et al. Comprehensive assessment of multiple biases in small RNA sequencing. *BMC Genomics*. 2019;20:513. PMID: 31226924
9. Benesova S et al. Small RNA-Sequencing: Approaches and Considerations for miRNA Analysis. *Diagnostics*. 2021;11(6):964. PMID: 34071824
10. Rossi D et al. miRNA normalization enables joint analysis of several datasets. *PLoS Comput Biol*. 2021;17(2):e1008608
11. Qin L-X et al. Statistical Assessment of Depth Normalization for Small RNA Sequencing. *JCO Clin Cancer Inform*. 2020;4:567-582
12. Zou J et al. PRECISION.seq: An R Package for Benchmarking Depth Normalization. *Front Genet*. 2022;12:823431
13. ENCODE Small RNA-seq Data Standards. encodeproject.org/data-standards/rna-seq/small-rnas/
