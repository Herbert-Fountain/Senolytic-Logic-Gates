# GSE200330 Analysis Report
## Irradiation-Induced Senescence — Synovial Fibroblast Extracellular Vesicle miRNAs

*Analysis date: 2026-04-06*

---

## 1. Study Summary

| Parameter | Details |
|-----------|---------|
| **GEO Accession** | [GSE200330](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200330) |
| **Publication** | Peiris HN et al. Comparative analysis of extracellular vesicle cargo in senescence and non-senescence induced human synovial fibroblasts. *Front Mol Biosci*. 2022. PMID: [36213127](https://pubmed.ncbi.nlm.nih.gov/36213127/) |
| **Organism** | *Homo sapiens* |
| **Cell type** | Primary synovial fibroblasts (from osteoarthritis patients undergoing joint replacement) |
| **Senescence inducer** | Ionizing radiation (10 Gy gamma irradiation), 18 days post-irradiation |
| **What was sequenced** | **Extracellular vesicle (EV) small RNA** — NOT intracellular |
| **Platform** | Illumina NovaSeq 6000, 100bp SE |
| **Total miRNAs** | 2,659 |
| **Data format** | Per-sample CSV with raw reads and RPM |

## 2. Experimental Design

| Group | Samples | Treatment |
|-------|---------|-----------|
| **Senescent** | GSM6031388 (N2), GSM6031391 (N4), GSM6031392 (N7) | 10 Gy irradiation, 18 days culture |
| **Control** | GSM6031389 (N6), GSM6031390 (N3), GSM6031393 (N5) | No irradiation, same culture period |

**Critical caveat:** This dataset profiles miRNAs in **extracellular vesicles** (EVs) secreted by the cells, not the intracellular miRNA pool. For circuit design, we need intracellular levels. However, this data is valuable for understanding which miRNAs are actively exported vs. retained during senescence. A miRNA that is depleted from EVs may be accumulating intracellularly, and vice versa.

## 3. Results

| miRNA | Control (reads) | Senescent (reads) | FC | EV Level | Interpretation |
|-------|----------------|-------------------|-----|----------|---------------|
| hsa-miR-21-5p | 596 | 570 | 1.0x | HIGH | Abundant in EVs regardless of senescence |
| hsa-miR-22-3p | 459 | 294 | **0.6x DOWN** | HIGH | Less exported in senescent EVs — retained intracellularly? |
| hsa-miR-122-5p | 34 | 36 | 1.1x | MED | Stable |
| hsa-miR-29a-3p | 29 | 28 | 1.0x | MED | No change in EV export |
| hsa-miR-155-5p | 28 | 7 | **0.2x DOWN** | LOW | Strongly reduced in senescent EVs |
| hsa-miR-34a-5p | 10 | 11 | 1.1x | MED | No change |
| hsa-miR-146a-5p | 7 | 7 | 1.0x | LOW | No change |
| hsa-miR-21-3p | 6 | 8 | 1.4x | LOW | Low in EVs (consistent with intracellular retention) |
| hsa-miR-29c-3p | 5 | 8 | 1.5x | LOW | Low in EVs |
| hsa-miR-215-5p | 4 | 0 | DOWN | LOW | Nearly absent |
| hsa-miR-184 | 0 | 1 | — | NEGLIGIBLE | Not in EVs |
| hsa-miR-96-5p | 0 | 0 | — | NEGLIGIBLE | Not in EVs |
| hsa-miR-17-5p | 0 | 0 | — | NEGLIGIBLE | Not in EVs |

## 4. Discussion

### 4.1 Most Candidate miRNAs Show No Change in EV Cargo

Of 13 candidates tested, only 2 showed meaningful changes in senescent cell EVs:
- **miR-22-3p**: 40% reduction in senescent EVs. In our GSE94410 analysis, miR-22-3p was also DOWN intracellularly in senescent HUVECs (3-fold). If it's both reduced intracellularly and exported less via EVs, the total cellular pool may be genuinely declining in senescence, contradicting some literature reports of upregulation.
- **miR-155-5p**: 80% reduction in senescent EVs. This is striking — if less is being exported, more may be retained intracellularly, which would be consistent with the in vivo aging increase we observed in GSE217458 (4.2x UP in aged liver).

### 4.2 Cross-Reference with Intracellular Retention Data

The Terlecki-Zaniewicz 2019 study (PMID: 29779019) found that miR-21-3p and miR-17-3p are selectively retained intracellularly in senescent fibroblasts (not packaged into EVs). Our GSE200330 data is partially consistent: miR-21-3p has low EV counts (6-8 reads) in both conditions, suggesting it's generally not an EV-exported miRNA regardless of senescence state.

### 4.3 Limitations

1. **EV miRNAs ≠ intracellular miRNAs.** This data tells us about export, not about what's available inside the cell for circuit sensing.
2. **Very low read counts** for most candidates (<30 reads). Statistical power is limited.
3. **n=3 per group.** Adequate for trends but underpowered for small effect sizes.
4. **Irradiation-induced senescence** may produce different EV cargo than doxorubicin or replicative senescence.
5. **Osteoarthritis patient-derived cells** may have baseline inflammatory/senescence features.

## 5. Conclusions

1. The EV miRNA landscape during senescence is largely unchanged for our candidate miRNAs — most show no significant export difference.
2. The reduction of miR-155-5p in senescent EVs is interesting and warrants further investigation — it may indicate intracellular accumulation.
3. This dataset's primary value is as negative evidence: miRNAs that are absent or unchanged in EVs (like miR-34a, miR-29c, miR-146a) are likely intracellularly retained, which is favorable for circuit sensing.

---

## References

1. Peiris HN et al. *Front Mol Biosci*. 2022. PMID: 36213127
2. Terlecki-Zaniewicz L et al. *Aging*. 2018;10(5):1103-1132. PMID: 29779019
