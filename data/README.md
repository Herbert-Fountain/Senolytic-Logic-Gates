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
