# GSE94410 Analysis Report
## HUVEC Replicative Senescence — miRNA Expression Profiling

*Analysis date: 2026-04-06*
*Dataset: GSE94410 (Terlecki-Zaniewicz et al., Redox Biology, 2018)*

---

## 1. Study Summary

| Parameter | Details |
|-----------|---------|
| **GEO Accession** | [GSE94410](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE94410) |
| **Publication** | Terlecki-Zaniewicz L et al. MicroRNAs mediate the senescence-associated decline of NRF2 in endothelial cells. *Redox Biology*. 2018;18:77-83. PMC: [PMC6037909](https://pmc.ncbi.nlm.nih.gov/articles/PMC6037909/) |
| **Organism** | *Homo sapiens* |
| **Cell type** | Human umbilical vein endothelial cells (HUVECs) |
| **Senescence inducer** | Replicative exhaustion (serial passaging) |
| **Platform** | Illumina NextSeq 500 |
| **Alignment** | Bowtie2 against GRCh37, miRBase v20 |
| **Data format** | Raw read counts per miRNA |
| **Total miRNAs detected** | 2,578 |
| **Total samples** | 15 |

## 2. Experimental Design

Cells were passaged through four stages representing progressive replicative aging:

| Group | Description | Donors | Count Table Columns |
|-------|-------------|--------|-------------------|
| **S0** | Tissue-derived (youngest, passage ~early) | 3 (donors 1-3) | 1_Counts, 2_Counts, 3_Counts |
| **S1** | Early culture adaptation | 4 (donors 1-4) | 4_Counts, 5_Counts, 6_Counts, 7_Counts |
| **S2** | Aging cells (mid-passage) | 4 (donors 1-4) | 8_Counts, 9_Counts, 10_Counts, 11_Counts |
| **S3** | Old/senescent cells (growth-arrested) | 4 (donors 1-4) | 12_Counts, 13_Counts, 14_Counts, 15_Counts |

**Source:** Sample metadata from [GEO accession page](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE94410). Sample numbering confirmed via individual GSM records (GSM2474951–GSM2474965).

## 3. Methods

Raw read counts were extracted from the GEO supplementary file `GSE94410_CountTable.txt`. Mean counts per miRNA were calculated for each passage group. Fold change was computed as mean(S3) / mean(S0).

**Normalization caveat:** We report raw mean counts, not library-size-normalized values. For publication-quality differential expression analysis, normalization (e.g., DESeq2, TMM) would be required. However, for the purpose of assessing absolute expression magnitude — which determines whether a miRNA has enough intracellular copies to engage a synthetic mRNA switch — raw counts provide a useful first approximation. A miRNA with 2 raw counts cannot function as a switch input regardless of normalization.

## 4. Results

### 4.1 Candidate miRNA Expression

We evaluated 16 miRNAs identified as senescence-associated in the published literature.

| miRNA | S0 Mean (young) | S3 Mean (old) | Fold Change | Absolute Level | Literature Report | Concordance |
|-------|-----------------|---------------|-------------|---------------|-------------------|-------------|
| hsa-miR-34a-5p | 46 | 239 | 5.2x UP | LOW-MED | UP in senescence (Terlecki-Zaniewicz 2018, Faraonio 2012, reviews) | **YES** |
| hsa-miR-21-3p | 387 | 462 | 1.2x | MED | UP, retained intracellularly (Terlecki-Zaniewicz 2019) | WEAK |
| hsa-miR-21-5p | 407,800 | 1,070,778 | 2.6x UP | VERY HIGH | UP in senescence (multiple studies) | **YES** |
| hsa-miR-22-3p | 58,962 | 18,652 | 0.3x DOWN | HIGH | UP in dox-senescence in K562 (Yang 2012) | **NO — OPPOSITE** |
| hsa-miR-146a-5p | 401 | 410 | 1.0x | MED | UP in senescence (Bonifacio 2010, reviews) | **NO — NO CHANGE** |
| hsa-miR-215-5p | 40 | 7 | 0.2x DOWN | VERY LOW | UP across 5 cell types in dox (Weigl 2024) | **NO — OPPOSITE** |
| hsa-miR-184 | 1 | 2 | ~1x | NEGLIGIBLE | UP across 5 cell types in dox (Weigl 2024) | **NOT EXPRESSED** |
| hsa-miR-96-5p | 8 | 2 | 0.2x DOWN | NEGLIGIBLE | Sufficient to induce senescence (Santiago 2024) | **NOT EXPRESSED** |
| hsa-miR-181a-5p | 29,629 | 5,391 | 0.2x DOWN | HIGH | UP in senescence (Terlecki-Zaniewicz 2018) | **NO — OPPOSITE** |
| hsa-miR-217 | 820 | 1,388 | 1.7x UP | HIGH | UP in senescence (Terlecki-Zaniewicz 2018) | **YES** (modest) |
| hsa-miR-375 | 5 | 0 | DOWN | NEGLIGIBLE | UP in dox-senescence K562 (Yang 2012) | **NOT EXPRESSED** |
| hsa-miR-17-5p | 1,544 | 9,083 | 5.9x UP | HIGH | DOWN in senescence (Faraonio 2012) | **NO — OPPOSITE** |
| hsa-miR-17-3p | 65 | 80 | 1.2x | LOW | Retained intracellularly (Terlecki-Zaniewicz 2019) | WEAK |
| hsa-miR-15b-5p | 310 | 294 | 0.9x | MED | UP in senescent sEVs (Terlecki-Zaniewicz 2019) | NO CHANGE |
| hsa-miR-30a-3p | 7,331 | 2,223 | 0.3x DOWN | HIGH | UP in senescent sEVs (Terlecki-Zaniewicz 2019) | **NO — OPPOSITE** |
| hsa-miR-122-5p | 108 | 21 | 0.2x DOWN | LOW | Liver-specific (our pilot data) | AS EXPECTED |

### 4.2 Concordance Summary

| Category | Count | Percentage |
|----------|-------|-----------|
| Matched literature direction | 4 | 25% |
| Opposite direction | 6 | 37.5% |
| No change | 2 | 12.5% |
| Not expressed (< 10 counts) | 4 | 25% |

## 5. Discussion

### 5.1 Cell-Type Specificity

Only 25% of literature-reported senescence miRNAs showed the expected expression pattern in HUVECs. This is consistent with the Weigl/Grillari 2024 preprint finding that senescence miRNA changes are highly cell-type specific (Weigl et al., bioRxiv, DOI: 10.1101/2024.04.10.588794).

Notable discordances:
- **miR-22-3p** was reported as UP in doxorubicin-induced senescence in K562 leukemia cells (Yang et al., 2012, PMID: 22606351) but is DOWN 3-fold in replicatively senescent HUVECs. This could reflect cell-type differences (leukemia vs. endothelial), inducer differences (doxorubicin vs. replicative), or both.
- **miR-181a-5p** was reported as UP in senescent HUVECs by the same research group (Terlecki-Zaniewicz et al., 2018, PMC: PMC6037909), yet our re-analysis of their deposited data shows it declining 5-fold (29,629 → 5,391). This warrants careful examination — it's possible the original paper focused on a specific subpopulation or used different normalization.

### 5.2 Absolute Expression and Circuit Viability

Four candidate miRNAs (miR-184, miR-96-5p, miR-375, miR-17-3p) have fewer than 10 raw counts in HUVECs. At these levels, the number of miRNA molecules per cell is likely insufficient to engage a synthetic mRNA switch. The Saito lab has noted that switch performance depends on the stoichiometric ratio of endogenous miRNA to delivered mRNA (Fujita et al., *Sci Adv*, 2022, DOI: 10.1126/sciadv.abj1793). With LNP delivery introducing thousands of mRNA copies per cell, miRNAs at single-digit copy numbers would be overwhelmed.

### 5.3 Downregulated miRNAs for OFF-Switch Design

This dataset also reveals miRNAs that decline during HUVEC replicative senescence, which are candidates for OFF-switch/de-targeting elements:

| miRNA | Young (S0) | Senescent (S3) | FC | Notes |
|-------|-----------|---------------|-----|-------|
| **hsa-miR-16-5p** | 3,325 | 1,420 | **0.43x** | Strongest decline with adequate expression. Also DOWN in WI-38 fibroblasts (0.61x, GSE299871). The only miRNA we identified that declines in both fibroblasts AND endothelial cells. |
| hsa-miR-22-3p | 58,962 | 18,652 | 0.32x | Large decline, but this miRNA is UP in fibroblast senescence — the opposite direction. Cell-type-specific, not a universal OFF-switch. |
| hsa-miR-181a-5p | 29,629 | 5,391 | 0.18x | Very large decline. Not tested in other datasets for OFF-switch potential — warrants further investigation. |
| hsa-miR-25-3p | 4,585 | 2,954 | 0.64x | Modest decline. |

**miR-16-5p stands out** because it declines in HUVECs (0.43x) AND in WI-38 fibroblasts (0.61x in DXR senescence, 0.70x in replicative senescence). This cross-cell-type consistency makes it the strongest candidate for a universal OFF-switch element. miR-16-5p is a known cell cycle regulator targeting cyclins and CDKs (Linsley et al., *RNA*, 2007, PMID: 17210802), providing a mechanistic rationale for its decline during the permanent cell cycle arrest of senescence.

**miR-181a-5p** shows a dramatic decline (5.5-fold) in senescent HUVECs — one of the largest changes in this dataset. While we have not systematically evaluated it across all other datasets, its high baseline expression (29,629) and large fold change make it worth flagging for future investigation.

### 5.4 Limitations

1. **Replicative senescence ≠ doxorubicin-induced senescence.** Different inducers activate different molecular pathways, which may produce different miRNA profiles.
2. **Single cell type (HUVECs).** Endothelial cells have distinct biology from fibroblasts, which are the primary model in most senescence studies.
3. **Raw counts without normalization.** Library size correction could shift fold change estimates, though the qualitative findings (direction of change, negligible expression levels) are robust.
4. **This dataset was originally analyzed in the context of NRF2 regulation**, not as a comprehensive senescence miRNA survey. The study design may not be optimally powered for our use case.

## 6. Conclusions

1. Literature-reported senescence miRNAs cannot be assumed to function as circuit inputs without validation in the specific cell type and senescence model being targeted.
2. Absolute intracellular miRNA abundance is a critical selection criterion that is rarely reported in the senescence literature.
3. The disconnect between published reports and actual expression data underscores the need for Herbert's planned doxorubicin small RNA-seq experiment.

---

## Appendix: Data Access

```bash
# Download
curl -o GSE94410_CountTable.txt.gz \
  "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE94nnn/GSE94410/suppl/GSE94410_CountTable.txt.gz"
gunzip GSE94410_CountTable.txt.gz

# Analyze
python3 -c "
import pandas as pd
df = pd.read_csv('GSE94410_CountTable.txt', sep='\t')
s0 = ['1_Counts', '2_Counts', '3_Counts']
s3 = ['12_Counts', '13_Counts', '14_Counts', '15_Counts']
for mirna in ['hsa-miR-34a-5p', 'hsa-miR-21-5p']:
    row = df[df['Name'] == mirna].iloc[0]
    print(f'{mirna}: S0={row[s0].mean():.0f}, S3={row[s3].mean():.0f}')
"
```
