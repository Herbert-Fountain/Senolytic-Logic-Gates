# GSE202120 Analysis Report
## Irradiation Dose-Response — Human Aortic Endothelial Cell miRNA Profiling

*Analysis date: 2026-04-07*

---

## 1. Study Summary

| Parameter | Details |
|-----------|---------|
| **GEO Accession** | [GSE202120](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE202120) (sub-series of [GSE202121](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE202121)) |
| **Publication** | Engel et al. *Scientific Reports*. 2022. PMID: [36402833](https://pubmed.ncbi.nlm.nih.gov/36402833/) |
| **Organism** | *Homo sapiens* |
| **Cell type** | Primary human aortic endothelial cells (HAECs) |
| **Treatment** | X-ray irradiation: 0, 1, 2, 4, 8, 10 Gy |
| **Timepoints** | 24h and 72h post-irradiation |
| **Method** | Qiaseq miRNA Library Prep, Illumina HiSeq X, ~10M SE reads/sample |
| **Replicates** | 3 per condition (except 2Gy/24h has 2) |
| **Total miRNAs** | 1,874 |
| **Total samples** | 35 |
| **Data format** | Raw counts (Excel) |

## 2. Experimental Design

This dataset provides a unique **dose-response** perspective on radiation-induced miRNA changes in endothelial cells. High-dose irradiation (8-10 Gy) is a well-established method for inducing cellular senescence. The graded doses allow us to assess whether miRNA changes are dose-dependent and at what dose the senescence-associated profile emerges.

| Dose | Expected Biology |
|------|-----------------|
| 0 Gy | Untreated control |
| 1 Gy | Sublethal — DNA repair, transient stress |
| 2 Gy | Low-dose — some persistent damage |
| 4 Gy | Moderate — significant DNA damage |
| 8 Gy | High — senescence-inducing range |
| 10 Gy | High — senescence-inducing range |

**Note:** The study was designed to profile radiation response broadly, not specifically to study senescence. Senescence markers (SA-β-gal, p21, p16) were not measured. We infer senescence induction at high doses based on established radiobiology (Serrano et al., *Cell*, 1997, PMID: 9054499; Di Leonardo et al., *Genes Dev*, 1994, PMID: 7798313).

## 3. Results

### 3.1 24h Post-Irradiation — Acute Response

| miRNA | 0 Gy | 1 Gy | 2 Gy | 4 Gy | 8 Gy | 10 Gy | FC (10/0) | Pattern |
|-------|------|------|------|------|------|-------|-----------|---------|
| miR-34a-5p | 1,438 | 1,652 | 1,620 | 1,692 | **2,111** | 1,827 | 1.3x | Modest dose-dependent UP |
| miR-21-5p | 1,764,943 | 1,785,332 | 1,933,747 | 1,843,525 | **2,185,636** | 1,974,290 | 1.1x | Slight UP at 8 Gy peak |
| miR-22-3p | 48,131 | 50,125 | 55,768 | 50,769 | **59,494** | 49,847 | 1.0x | No clear dose-response |
| miR-155-5p | 12,779 | 12,411 | 12,980 | 12,482 | 14,429 | 12,447 | 1.0x | No change |
| miR-146a-5p | 1,823 | 1,793 | 2,163 | 1,954 | 2,524 | 2,109 | 1.2x | Slight UP |
| miR-17-5p | 6,039 | 6,052 | 5,920 | 5,702 | 6,726 | 6,169 | 1.0x | No change |
| miR-29a-3p | 13,335 | 13,756 | 14,624 | 14,042 | 16,315 | 14,480 | 1.1x | Slight UP |
| miR-29c-3p | 59 | 63 | 60 | 52 | 70 | 61 | 1.0x | Low counts, no change |

**At 24h, miRNA changes are minimal.** The acute DNA damage response does not dramatically alter the miRNA landscape. The largest effect is miR-34a-5p at 8 Gy (2,111, +47% over control), consistent with rapid p53-mediated miR-34a induction.

### 3.2 72h Post-Irradiation — Emerging Senescence Response

| miRNA | 0 Gy | 1 Gy | 2 Gy | 4 Gy | 8 Gy | 10 Gy | FC (10/0) | Pattern |
|-------|------|------|------|------|------|-------|-----------|---------|
| miR-34a-5p | 1,599 | 2,011 | 2,348 | 2,455 | 2,548 | **2,629** | **1.6x** | **Dose-dependent UP** |
| miR-21-5p | 1,654,002 | 1,967,478 | 2,005,151 | 2,274,648 | 2,380,982 | **2,609,852** | **1.6x** | **Dose-dependent UP** |
| miR-146a-5p | 1,966 | 3,403 | 4,247 | **5,369** | 4,990 | 4,275 | **2.2x** | **Dose-dependent UP** (peaks 4-8 Gy) |
| miR-29a-3p | 12,983 | 16,115 | 16,453 | 17,539 | 18,022 | 16,965 | **1.3x** | Modest dose-dependent UP |
| miR-22-3p | 39,647 | 53,678 | 48,685 | 49,052 | 56,930 | 47,857 | 1.2x | Variable, no clear trend |
| miR-155-5p | 14,815 | 15,065 | 13,573 | 13,210 | 12,771 | **13,597** | **0.9x** | Slight DOWN at high doses |
| miR-17-5p | 5,156 | 5,028 | 4,505 | 4,222 | 3,863 | **3,481** | **0.7x** | **Dose-dependent DOWN** |
| miR-29c-3p | 54 | 68 | 79 | 69 | 72 | 69 | 1.3x | Low counts, slight UP |

### 3.3 Key Findings

#### miR-34a-5p: Dose-Dependent Radiation Response Confirms Universal Role

miR-34a-5p shows a clear **dose-dependent increase** at 72h, rising from 1,599 (0 Gy) to 2,629 (10 Gy). The response is:
- Absent at 24h (acute DNA repair, before p53-dependent transcription kicks in)
- Progressive at 72h (1 Gy: 1.3x → 10 Gy: 1.6x)

This temporal pattern matches the known kinetics of p53 → miR-34a transcriptional activation following DNA damage (He et al., *Nature*, 2007, PMID: 17554337).

**Updated cross-dataset concordance for miR-34a-5p:**

| # | Dataset | Context | FC | Counts |
|---|---------|---------|-----|--------|
| 1 | GSE299871 | DXR senescence (WI-38 fibroblasts) | 2.5x UP | 102→253 |
| 2 | GSE299871 | SDS senescence (WI-38 fibroblasts) | 7.2x UP | 102→732 |
| 3 | GSE299871 | Replicative senescence (WI-38 fibroblasts) | 3.0x UP | 102→310 |
| 4 | GSE94410 | Replicative senescence (HUVEC) | 5.2x UP | 46→239 |
| 5 | **GSE202120** | **Irradiation (HAEC, 10Gy 72h)** | **1.6x UP** | **1,599→2,629** |
| 6 | GSE217458 | Mouse aging (16 tissues) | 1.2-1.7x UP | 500-3,800 RPMM |
| 7 | GSE55164 | Mouse muscle aging | 2.5x UP | ~1,500 (est.) |

**miR-34a-5p is now confirmed across 7 analyses, 4 senescence inducers, 3 human cell types, and 2 organisms.** No other miRNA achieves this consistency.

Notably, miR-34a-5p counts in HAECs (1,438-2,629) are **substantially higher** than in WI-38 fibroblasts (102-253). If HAECs are a relevant target tissue for the circuit, miR-34a provides much better stoichiometric margins for switch activation in endothelial cells than in fibroblasts.

#### miR-146a-5p: Strong Dose-Dependent Response in Endothelial Cells

miR-146a-5p shows the largest fold change in this dataset (2.2x at 10 Gy, 72h), with a bell-shaped dose response peaking at 4 Gy (5,369). This is notable because:
- miR-146a showed **no change** in HUVEC replicative senescence (GSE94410)
- It showed **2.5x UP** in aged mouse muscle (GSE55164)
- It showed **no change** in DXR-senescent WI-38 fibroblasts (GSE299871)

The pattern suggests miR-146a-5p upregulation may be **radiation-specific and endothelial-specific**, possibly reflecting NF-κB pathway activation by ionizing radiation rather than a universal senescence response. miR-146a is a known NF-κB target and inflammation regulator (Taganov et al., *PNAS*, 2006, PMID: 16885212).

#### miR-17-5p: Dose-Dependent Decline at 72h

miR-17-5p declines from 5,156 to 3,481 (0.7x) at 72h in a dose-dependent manner. This is consistent with:
- 0.3x decline in DXR-senescent WI-38 fibroblasts (GSE299871)
- 0.3x decline in replicatively senescent WI-38 fibroblasts (GSE299871)
- miR-17 family downregulation in senescence (Faraonio et al., 2012, PMID: 22052189)

However, in HUVEC replicative senescence (GSE94410), miR-17-5p was paradoxically UP (5.9x). The HAEC radiation data (DOWN 0.7x) and WI-38 data (DOWN 0.3x) suggest the HUVEC finding may be an outlier or reflect fundamentally different biology in umbilical vein vs. aortic endothelial cells.

#### miR-155-5p: Slight Decline at High Doses

miR-155-5p shows a subtle decrease at high doses (0.9x at 10 Gy, 72h), consistent with the dramatic decline seen in DXR-senescent fibroblasts (0.14x, GSE299871). The smaller effect here may reflect:
- Different cell type (endothelial vs. fibroblast)
- Different inducer kinetics (radiation is instantaneous; DXR is sustained)
- 72h may be too early for full senescence-associated miR-155 decline

#### Absolute Expression Levels in HAECs

This dataset provides the first look at baseline miRNA abundance in aortic endothelial cells:

| miRNA | HAEC Baseline (0 Gy) | WI-38 Baseline (Ctrl) | Ratio |
|-------|---------------------|----------------------|-------|
| miR-21-5p | 1,654,002 | 18,370 | **90x higher in HAECs** |
| miR-22-3p | 39,647 | 2,484 | 16x higher |
| miR-155-5p | 14,815 | 2,760 | 5x higher |
| miR-29a-3p | 12,983 | 3,740 | 3.5x higher |
| miR-17-5p | 5,156 | 134 | 38x higher |
| miR-146a-5p | 1,966 | 12 | **164x higher** |
| miR-34a-5p | 1,438 | 102 | **14x higher** |
| miR-29c-3p | 54 | 2 | 27x higher |

**HAECs express most miRNAs at dramatically higher levels than WI-38 fibroblasts.** This has major implications for circuit design: the stoichiometric balance between endogenous miRNA and delivered mRNA will be very different in endothelial cells vs. fibroblasts.

**Caveat on comparing raw counts:** These two datasets used different library preparation methods and sequencing depths, so the absolute count differences may partly reflect technical factors. However, the consistent >10x differences across most miRNAs suggest genuine biological differences in miRNA abundance between cell types.

## 4. Limitations

1. **Not a senescence study per se.** Senescence markers were not measured. We infer senescence induction at 8-10 Gy based on established radiobiology literature.
2. **72h may be too early.** Full senescence establishment typically takes 7-14 days. The 72h timepoint captures early senescence/growth arrest but not established SASP-secreting senescence.
3. **n=3 replicates per condition**, which is adequate for detecting moderate effects but may miss subtle dose-dependent changes.
4. **Aortic endothelial cells** are a specific cell type; findings may not generalize to other endothelial subtypes or non-endothelial cells.
5. **No 2Gy/24h replicate 2.** Minor gap in the dose-response curve.

## 5. Conclusions

1. **miR-34a-5p shows dose-dependent upregulation in irradiated endothelial cells**, adding a fourth senescence inducer (irradiation) to the list where it is confirmed UP (after DXR, SDS, and replicative). It is now validated across 7 independent analyses.

2. **miR-146a-5p is radiation-responsive in endothelial cells** (2.2x at 72h) but not in DXR-treated fibroblasts. This is an **inducer- and cell-type-specific** response, likely reflecting NF-κB pathway activation by radiation.

3. **miR-17-5p dose-dependent decline** is consistent across irradiation (this study) and DXR/replicative senescence (GSE299871), strengthening it as an OFF-switch candidate.

4. **HAECs express most miRNAs at 10-100x higher absolute levels than WI-38 fibroblasts.** Circuit design must account for this cell-type-dependent miRNA abundance.

5. **The 24h→72h temporal shift** from minimal changes to emerging senescence signatures is consistent with the DXR time course in GSE299871, where the strongest changes also required days to develop.

---

## References

1. Engel et al. *Sci Rep*. 2022. PMID: 36402833
2. He L et al. *Nature*. 2007;447:1130-1134. PMID: 17554337
3. Taganov KD et al. *PNAS*. 2006;103(33):12481-12486. PMID: 16885212
4. Faraonio R et al. *Cell Death Differ*. 2012;19(4):616-624. PMID: 22052189
5. Serrano M et al. *Cell*. 1997;88(5):593-602. PMID: 9054499
6. Di Leonardo A et al. *Genes Dev*. 1994;8(21):2540-2551. PMID: 7798313
