# Data Sources and Provenance

This directory contains publicly available datasets used for senescence miRNA analysis. All data was obtained from NCBI GEO under their standard data use policies.

---

## GSE94410 — HUVEC Replicative Senescence miRNA-seq

**Publication:** Terlecki-Zaniewicz L et al. MicroRNAs mediate the senescence-associated decline of NRF2 in endothelial cells. *Redox Biology*. 2018;18:77-83. PMC: [PMC6037909](https://pmc.ncbi.nlm.nih.gov/articles/PMC6037909/)

**GEO URL:** https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE94410

**Downloaded:** 2026-04-06

**Source file:** `GSE94410_CountTable.txt.gz` from https://ftp.ncbi.nlm.nih.gov/geo/series/GSE94nnn/GSE94410/suppl/

### Experimental Design

| Parameter | Details |
|-----------|---------|
| Organism | *Homo sapiens* |
| Cell type | Human umbilical vein endothelial cells (HUVECs) |
| Senescence inducer | Replicative exhaustion (serial passaging) |
| Platform | Illumina NextSeq 500 |
| Alignment | Bowtie2 against GRCh37 + miRBase v20 |
| Quantification | Raw read counts per miRNA |

### Sample Groups

| Group | Description | Samples | Donors | Column IDs in count table |
|-------|-------------|---------|--------|--------------------------|
| S0 | Tissue-derived cells (youngest) | 3 | Donors 1-3 | 1_Counts, 2_Counts, 3_Counts |
| S1 | Early culture passage | 4 | Donors 1-4 | 4_Counts, 5_Counts, 6_Counts, 7_Counts |
| S2 | Aging cells (mid-passage) | 4 | Donors 1-4 | 8_Counts, 9_Counts, 10_Counts, 11_Counts |
| S3 | Old/senescent cells (late passage) | 4 | Donors 1-4 | 12_Counts, 13_Counts, 14_Counts, 15_Counts |

### GEO Sample Accession Mapping

| GSM Accession | Sample | Group | Donor | Count Table Column |
|--------------|--------|-------|-------|-------------------|
| GSM2474951 | Sample 1 | S0 | Donor 1 | 1_Counts |
| GSM2474952 | Sample 2 | S0 | Donor 2 | 2_Counts |
| GSM2474953 | Sample 3 | S0 | Donor 3 | 3_Counts |
| GSM2474954 | Sample 4 | S1 | Donor 1 | 4_Counts |
| GSM2474955 | Sample 5 | S1 | Donor 2 | 5_Counts |
| GSM2474956 | Sample 6 | S1 | Donor 3 | 6_Counts |
| GSM2474957 | Sample 7 | S1 | Donor 4 | 7_Counts |
| GSM2474958 | Sample 8 | S2 | Donor 1 | 8_Counts |
| GSM2474959 | Sample 9 | S2 | Donor 2 | 9_Counts |
| GSM2474960 | Sample 10 | S2 | Donor 3 | 10_Counts |
| GSM2474961 | Sample 11 | S2 | Donor 4 | 11_Counts |
| GSM2474962 | Sample 12 | S3 | Donor 1 | 12_Counts |
| GSM2474963 | Sample 13 | S3 | Donor 2 | 13_Counts |
| GSM2474964 | Sample 14 | S3 | Donor 3 | 14_Counts |
| GSM2474965 | Sample 15 | S3 | Donor 4 | 15_Counts |

### Data Format

Tab-delimited text file with columns:
- `Name`: miRNA identifier (miRBase nomenclature, e.g., `hsa-miR-21-5p`)
- `Sequence`: Mature miRNA nucleotide sequence
- `Name count`: Number of unique sequences mapping to this miRNA
- `Identical miRNAs`: miRNAs with identical mature sequences
- `{N}_Counts`: Raw read counts for sample N

**Total miRNAs:** 2,578
**Total samples:** 15

### How to Reproduce

```bash
# Download
curl -o GSE94410_CountTable.txt.gz \
  "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE94nnn/GSE94410/suppl/GSE94410_CountTable.txt.gz"
gunzip GSE94410_CountTable.txt.gz
```

### Limitations

1. **Replicative senescence, NOT doxorubicin-induced.** The miRNA changes may differ from chemotherapy-induced senescence.
2. **Single cell type (HUVECs).** Findings may not generalize to fibroblasts, epithelial cells, or other tissue types.
3. **Raw counts, not normalized.** Library size differences between samples must be accounted for in any differential expression analysis. We report raw mean counts in our analysis for transparency; formal DE analysis should use DESeq2 or similar.

---

## GSE27404 — IMR90 Replicative Senescence miRNA Deep Sequencing

**Publication:** Dhahbi JM et al. Deep Sequencing Reveals Novel MicroRNAs and Regulation of MicroRNA Expression during Cell Senescence. *PLoS ONE*. 2011;6(5):e20509. PMID: [21637828](https://pubmed.ncbi.nlm.nih.gov/21637828/)

**GEO URL:** https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE27404

**Status:** To be downloaded and analyzed.

### Experimental Design

| Parameter | Details |
|-----------|---------|
| Organism | *Homo sapiens* |
| Cell type | IMR90 fetal lung fibroblasts |
| Senescence inducer | Replicative exhaustion |
| Platform | Illumina Genome Analyzer IIx |
| Read depth | 11.4M reads (young), 9.1M reads (senescent) |

### Critical Limitation

**n = 1 per condition** (one young sample, one senescent sample). No biological replicates. This limits statistical inference but provides a reference for absolute miRNA expression levels in fibroblasts.

---

## Planned Datasets

### Herbert Fountain Lab — Doxorubicin-Induced Senescence in Mice
- **Organism:** *Mus musculus*
- **Inducer:** Doxorubicin (in vivo injection)
- **Tissues:** Multiple organs
- **Method:** Small RNA-seq
- **Status:** Planned, not yet performed

### Herbert Fountain Lab — Doxorubicin-Induced Senescence in Human pHDFs
- **Organism:** *Homo sapiens*
- **Cell type:** Primary human dermal fibroblasts
- **Inducer:** Doxorubicin (in vitro)
- **Method:** Small RNA-seq
- **Status:** Planned, not yet performed

## Additional Datasets — Provenance Summary

All datasets below were downloaded from NCBI GEO between 2026-04-06 and 2026-04-07.

| Dataset | GEO | Downloaded File | Source URL | Download Date |
|---------|-----|----------------|-----------|---------------|
| GSE299871 | [Link](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299871) | `raw_counts.txt` | GEO suppl: `GSE299871_raw_counts_All.txt.gz` | 2026-04-06 |
| GSE202120 | [Link](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE202120) | `Counts_miRNA.xlsx` | GEO download gateway | 2026-04-07 |
| GSE117818 | [Link](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE117818) | `counts.xls` | GEO suppl: `GSE117818_sample_counts.xls.gz` | 2026-04-07 |
| GSE200330 | [Link](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200330) | Per-sample CSVs | GEO suppl: `GSE200330_RAW.tar` | 2026-04-06 |
| GSE217458 | [Link](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE217458) | `TMS_counts.csv`, `TMS_annotation.csv` | GEO suppl (RPMM-normalized) | 2026-04-06 |
| GSE55164 | [Link](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE55164) | `normalized.txt` | GEO suppl: `GSE55164_small_RNA_Seq_normalized.txt.gz` | 2026-04-06 |
| GSE172269 | [Link](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE172269) | `exprmat.csv` | GEO suppl: `GSE172269_exprmat_forPublish.csv.gz` | 2026-04-07 |
| GSE136926 | [Link](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE136926) | `mirna_norm.txt` | GEO suppl: `GSE136926_miRNA_seq_SR12_norm.txt.gz` | 2026-04-07 |
| GSE111281 | [Link](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE111281) | `counts.txt` | GEO suppl: `GSE111281_sample_counts.txt.gz` | 2026-04-07 |
| GSE111174 | [Link](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE111174) | `counts.txt` | GEO suppl: `GSE111174_sample_counts.txt.gz` | 2026-04-07 |
| GSE182598 | [Link](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE182598) | `normalized_counts.xlsx`, `age_association.xlsx` | GEO suppl | 2026-04-07 |

### Data Formats

| Format | Datasets | Notes |
|--------|----------|-------|
| Raw counts | GSE299871, GSE94410, GSE172269, GSE111281, GSE111174 | Require CPM or DESeq2 normalization |
| Author-normalized | GSE217458 (RPMM), GSE55164 (log2), GSE136926 (normalized) | No additional normalization needed |
| Raw counts (precursor miRNA IDs) | GSE117818, GSE111281, GSE111174 | Combine -5p and -3p strands |
| Per-sample RPM | GSE200330 | RPM provided per sample |
| Excel | GSE202120, GSE182598 | Requires openpyxl for reading |

### Citations for All Datasets

| Dataset | PMID | Citation |
|---------|------|---------|
| GSE299871 | — | RNA Biology 2025. DOI: 10.1080/15476286.2025.2551299 |
| GSE94410 | 29980056 | Terlecki-Zaniewicz et al. Redox Biology. 2018;18:77-83 |
| GSE202120 | 36402833 | Engel et al. Scientific Reports. 2022 |
| GSE117818 | — | JenAge Consortium, Leibniz Institute on Aging |
| GSE200330 | 36213127 | Peiris et al. Front Mol Biosci. 2022 |
| GSE217458 | 37106037 | Wagner et al. Nature Biotechnology. 2024;42:109-118 |
| GSE55164 | 25063768 | Kim et al. Aging. 2014;6(7):524-544 |
| GSE172269 | 35551205 | Bushel et al. Scientific Data. 2022;9:252 |
| GSE136926 | 31607954 | Ma et al. Front Physiol. 2019;10:1226 |
| GSE111281 | — | JenAge Consortium, Leibniz Institute on Aging |
| GSE111174 | — | JenAge Consortium, Leibniz Institute on Aging |
| GSE182598 | — | To be confirmed |
| GSE27404 | 21637828 | Dhahbi et al. PLoS ONE. 2011;6(5):e20509 |
