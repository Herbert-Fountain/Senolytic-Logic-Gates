# Cross-Study Synthesis: Senescence and Aging miRNA Landscape
## Implications for Logic Gate Circuit Design

*Version 2.0 - Complete rewrite with CPM-corrected values*
*Last updated: 2026-04-07*
*Datasets analyzed: 11 (see Table 1)*

---

## 1. Overview

This document synthesizes findings across eleven analyzed datasets (1,300+ samples across 3 organisms) and the published literature to assess the feasibility of identifying miRNA inputs for senolytic logic gate circuits. We evaluate each candidate miRNA based on four criteria essential for circuit function:

1. **Absolute expression level** - sufficient intracellular copies to engage synthetic mRNA switches
2. **Differential expression** - higher (ON switch) or lower (OFF switch) in senescent/aged cells compared to healthy/young cells
3. **Consistency** - reproducible across cell types, tissues, inducers, and organisms
4. **Conservation** - expressed in both mouse and human for translational path

---

## 2. Analysis Pipeline and Methods

### 2.1 Overall Approach

Our analysis follows this pipeline:

1. **Identify candidate miRNAs** from senescence and aging literature
2. **Download public small RNA-seq datasets** from NCBI GEO with processed count data
3. **Normalize raw counts** using CPM (Counts Per Million) where raw data was provided
4. **Compute fold changes** between senescent/aged and control/young conditions within each dataset
5. **Assess concordance** across datasets by comparing direction and magnitude of changes
6. **Evaluate circuit viability** based on absolute expression, fold change, and cross-dataset consistency

### 2.2 CPM Normalization

**What is CPM?** Counts Per Million is a normalization method that corrects for differences in sequencing depth (library size) between samples:

```
CPM for miRNA X in sample Y = (raw counts of X in Y / total miRNA counts in Y) × 1,000,000
```

**Why it matters:** If one sample was sequenced deeper than another, all its miRNAs will have higher raw counts - this creates the false appearance that miRNAs are upregulated. CPM divides by the total library size, putting all samples on an equal footing.

**Example:** In GSE299871, DXR-treated samples had ~1.6x larger libraries than controls (0.45M vs 0.28M reads). Without CPM correction, every miRNA in the DXR group appeared ~1.6x higher than it actually was. After CPM correction, miR-34a-5p dropped from an apparent 2.5x increase to a true 1.5x increase, and miR-29a-3p dropped from an apparent 1.6x increase to **no change** (0.96x) - its entire upregulation signal was a library size artifact.

CPM is the simplest library-size correction. More sophisticated methods (TMM, DESeq2 median-of-ratios) are recommended for formal differential expression testing (Tam et al., *Brief Bioinform*, 2015, PMID: 25888698) but CPM is adequate for fold change estimation.

### 2.3 Which Datasets Have CPM-Corrected Values

| Dataset | Data Format | CPM Applied? | Notes |
|---------|-----------|-------------|-------|
| GSE299871 | Raw counts | **YES** | Library size bias confirmed (1.6-4.3x between groups) |
| GSE94410 | Raw counts | **YES** | Library size bias confirmed (S3 = 0.53x S0) |
| GSE202120 | Raw counts | Pending | Should be CPM-corrected |
| GSE117818 | Raw counts (precursor) | Pending | Precursor IDs, both strands combined |
| GSE172269 | Raw counts | Pending | |
| GSE111281/174 | Raw counts (precursor) | Pending | |
| GSE217458 | RPMM (pre-normalized) | Not needed | Author-normalized |
| GSE55164 | Log2 (pre-normalized) | Not needed | Author-normalized |
| GSE136926 | Normalized (author) | Not needed | Author-normalized |
| GSE200330 | RPM (per-sample) | Not needed | Author-provided |

**Values labeled "raw" in this document have NOT been CPM-corrected** and may be inflated or deflated by library size differences. Values labeled "CPM" have been corrected. Pre-normalized datasets (RPMM, log2, RPM) do not require additional correction.

### 2.4 Statistical Limitations

- **GSE299871 has n=2 per condition** (below the minimum of 3 recommended by Schurch et al., *RNA*, 2016, PMID: 27022035). Results from this dataset are **hypothesis-generating, not definitive.** No formal p-values can be computed.
- **Cross-dataset fold change comparison** is directional only. Absolute CPM values are not comparable between datasets due to different library preparation protocols, ligation biases, and organisms (Giraldez et al., *Nat Biotechnol*, 2018, PMID: 30010675).
- **Bulk tissue datasets** (GSE217458, GSE172269, GSE136926, GSE111281/174) measure a mixture of cell types. Changes may reflect cell composition shifts (e.g., immune cell infiltration) rather than cell-autonomous miRNA regulation. "Non-cell-autonomous" means changes caused by the surrounding tissue environment - such as macrophages migrating into aging tissue - rather than by the internal biology of the cell being measured.

### 2.5 Senescence Inducers Glossary

| Inducer | Mechanism |
|---------|-----------|
| **Doxorubicin (DXR)** | DNA intercalator and topoisomerase II inhibitor. Generates DNA double-strand breaks, triggering persistent DNA damage response and p53-dependent growth arrest. |
| **SDS (PMD-Sen)** | Sodium dodecyl sulfate damages the plasma membrane at sub-lethal concentrations, triggering a distinct senescence program initiated by membrane stress rather than nuclear DNA damage (RNA Biology, 2025, DOI: 10.1080/15476286.2025.2551299). |
| **Ionizing radiation** | X-ray or gamma irradiation generates DNA double-strand breaks. Doses ≥8 Gy reliably induce senescence in most cell types within 7-14 days. |
| **Replicative senescence (RS)** | Progressive telomere shortening through serial cell division. The most physiologically relevant model. |

---

## 3. Data Sources

**Table 1: Datasets analyzed**

| # | Dataset | Cell/Tissue | Inducer/Context | Organism | Samples | n per group |
|---|---------|------------|----------------|----------|---------|-------------|
| 1 | GSE299871 | WI-38 fibroblasts | DXR, SDS, RS | Human | 36 | **2** (hypothesis-generating) |
| 2 | GSE94410 | HUVECs | Replicative | Human | 15 | 3-4 |
| 3 | GSE202120 | HAECs | X-ray 0-10 Gy, 24+72h | Human | 35 | 3 |
| 4 | GSE117818 | MRC-5 fibroblasts | Replicative (5 PD stages) | Human | 15 | 3 |
| 5 | GSE200330 | Synovial fibroblast **EVs** | 10 Gy irradiation | Human | 6 | 3 |
| 6 | GSE217458 | 16 mouse tissues | Natural aging (1-27mo) | Mouse | 771 | Up to 6 |
| 7 | GSE55164 | Mouse muscle | Natural aging (6 vs 24mo) | Mouse | 12 | 6 |
| 8 | GSE172269 | 11 rat organs | Natural aging (6wk-104wk) | Rat | 320 | 8 |
| 9 | GSE136926 | Human right atrium | Natural aging (38-72yr) | Human | 12 | 3 |
| 10 | GSE111281 | Human skin | Natural aging (24-80yr) | Human | 30 | 6-9 |
| 11 | GSE111174 | Human blood | Natural aging (24-80yr) | Human | 30 | 7 |

Note: GSE202120 captures early growth arrest (72h post-irradiation), not established senescence (which requires 7-14 days). Results are flagged accordingly.

---

## 4. ON-Switch Candidates (Upregulated in Senescence)

### 4.1 miR-34a-5p - The Only Consistent ON-Switch Candidate

**Table 2: miR-34a-5p evidence across all datasets**

| Dataset | Context | FC | Counts/Level | Data Type |
|---------|---------|-----|-------------|-----------|
| GSE299871 | WI-38 DXR (n=2) | **1.50x UP** | 371→558 CPM | CPM-corrected |
| GSE299871 | WI-38 SDS (n=2) | **1.66x UP** | 371→615 CPM | CPM-corrected |
| GSE299871 | WI-38 RS (n=2) | **1.50x UP** | 371→558 CPM | CPM-corrected |
| GSE94410 | HUVEC RS | **11.5x UP** | 8→90 CPM | CPM-corrected |
| GSE202120 | HAEC irr. 10Gy 72h | **1.6x UP** | 1,599→2,629 | Raw (pre-normalized pending) |
| GSE117818 | MRC-5 RS (precursor) | **2.8x UP** | 1,086→3,048 | Raw (precursor IDs) |
| GSE217458 | Mouse heart aging | 1.36x UP | 1,167→1,587 RPMM | Pre-normalized |
| GSE217458 | Mouse kidney aging | 1.51x UP | 2,535→3,829 RPMM | Pre-normalized |
| GSE217458 | Mouse liver aging | 1.25x UP | 843→1,056 RPMM | Pre-normalized |
| GSE217458 | Mouse lung aging | **1.68x UP** | 1,548→2,597 RPMM | Pre-normalized |
| GSE217458 | Mouse spleen aging | 1.55x UP | 488→756 RPMM | Pre-normalized |
| GSE217458 | Mouse skin aging | 1.17x (stable) | 1,112→1,305 RPMM | Pre-normalized |
| GSE55164 | Mouse muscle aging | **2.5x UP** | ~1,500 est. | Log2 normalized |
| GSE172269 | Rat liver aging | **4.1x UP** | 30→120 | Raw (pending CPM) |
| GSE172269 | Rat kidney aging | 1.5x UP | 219→319 | Raw (pending CPM) |
| GSE172269 | Rat spleen aging | **2.1x UP** | 294→602 | Raw (pending CPM) |
| GSE172269 | Rat lung aging | 1.5x UP | 1,732→2,546 | Raw (pending CPM) |
| GSE172269 | Rat heart aging | **0.84x (stable)** | 754→630 | Raw (pending CPM) |
| GSE136926 | **Human heart aging** | **2.54x UP** | 771→1,959 | Pre-normalized |
| GSE111281 | **Human skin aging** | 1.25x UP | 828→1,035 | Raw (precursor, pending CPM) |
| GSE111174 | Human blood aging | Not expressed | 2 counts | Raw |

**Summary: UP in 18/21 analyses.** Exceptions: mouse skin (1.17x, borderline), rat heart (0.84x, borderline decline), human blood (not expressed). miR-34a-5p is the most consistently upregulated miRNA across 4 senescence inducers, 4 human cell types (WI-38, MRC-5, HUVEC, HAEC), 2 human tissues in vivo (heart, skin), 3 organisms (human, mouse, rat), and both in vitro and in vivo contexts. It is notably absent from blood (<2 counts).

**Mechanistic basis:** miR-34a is a direct transcriptional target of p53 (He et al., *Nature*, 2007, PMID: 17554337), which targets SIRT1 (Yamakuchi et al., *PNAS*, 2008, PMID: 18755897). Since p53 activation is the convergent node of all senescence pathways, miR-34a upregulation is mechanistically expected across inducers.

**Circuit viability concern:** After CPM correction, the fold change in WI-38 fibroblasts is only 1.5x, and the estimated intracellular copy number is ~45 per cell (based on calibration against published absolute quantification data; Bissels et al., *RNA*, 2009, PMID: 19850911). Whether this is sufficient for switch activation is unknown - the Saito lab has not published a quantitative transfer function for the L7Ae system, and this remains the single most important empirical question (see Section 6.2).

### 4.2 miR-22-3p - Fibroblast-Specific, Not Universal

miR-22-3p is UP 1.74x (CPM) in DXR-senescent WI-38 fibroblasts (8,920→15,543 CPM) with high absolute expression. However, it is DOWN 0.65x (CPM) in replicatively senescent HUVECs and stable in aged mouse tissues (0.90-1.55x across 6 tissues). The response is **cell-type-dependent**: UP in fibroblasts regardless of inducer, DOWN or stable elsewhere. Not suitable for a universal circuit.

### 4.3 Eliminated ON-Switch Candidates

| Candidate | Raw FC | CPM FC | Reason Eliminated |
|-----------|--------|--------|------------------|
| **miR-29a-3p** | 1.56x UP (DXR) | **0.96x (stable)** | Entire raw signal was library size artifact |
| **miR-21-5p** | 1.79x UP (DXR) | **1.09x (stable)** | Entire raw signal was library size artifact |
| miR-29c-3p | 5.0x UP (DXR) | 3.2x UP | Direction holds but only 6→21 CPM - negligible expression |
| miR-146a-5p | 1.2x | 1.2x | No change in DXR-senescent fibroblasts |
| miR-184 | - | - | Not expressed (<10 counts in all human cells) |
| miR-96-5p | - | - | Not expressed |
| miR-215-5p | - | - | Not expressed |

---

## 5. OFF-Switch Candidates (Downregulated in Senescence)

For an OFF switch, the miRNA must be HIGH in healthy cells (producing L7Ae to repress the payload) and LOW in senescent cells (no L7Ae, payload expressed).

### 5.1 miR-155-5p - Strongest Fibroblast OFF-Switch

| Dataset | Cell/Tissue | FC | CPM | Data Type |
|---------|------------|-----|-----|-----------|
| GSE299871 | WI-38 DXR (n=2) | **0.09x** | 9,887→889 | CPM-corrected |
| GSE299871 | WI-38 RS (n=2) | **0.11x** | 9,887→1,108 | CPM-corrected |
| GSE117818 | MRC-5 RS (precursor) | **0.10x** | 1,806→185 | Raw |
| GSE94410 | HUVEC RS | **1.81x UP** | 2,809→5,087 | CPM-corrected |
| GSE202120 | HAEC irr. 72h | 0.92x stable | 14,815→13,597 | Raw |
| GSE217458 | Mouse tissues (all 6) | UP 1.24-4.20x | 21-1,219 RPMM | Pre-normalized (inflammaging) |

**Verdict:** 9-11x decline in fibroblasts - strongest OFF-switch signal. But **UP in senescent HUVECs** (CPM 1.81x) and **UP in aged tissues** (inflammaging artifact - macrophage infiltration drives bulk signal). Fibroblast-specific only.

**Inflammaging explanation:** miR-155 is >100-fold enriched in activated macrophages (Mann et al., *PLoS One*, 2017, PMID: 27447824). Macrophages accumulate in aged tissues (Tabula Muris Consortium, *Nature*, 2020, PMID: 32669714). When bulk tissue is sequenced, the macrophage-derived miR-155 overwhelms the parenchymal cell signal. In vivo, macrophage-derived exosomes can deliver miR-155 to neighboring cells (Yin et al., *Cell Commun Signal*, 2024, PMID: 38987851; He et al., *Hum Mutat*, 2025, PMID: 40486266), potentially confounding an OFF switch by introducing miR-155 into senescent cells near inflammatory foci.

---

### 5.2 miR-92a-3p - Most Cross-Tissue OFF-Switch

| Dataset | Cell/Tissue | FC | Level | Data Type |
|---------|------------|-----|-------|-----------|
| GSE299871 | WI-38 DXR (n=2) | **0.26x** | 23,101→6,053 CPM | CPM-corrected |
| GSE117818 | MRC-5 RS (precursor) | **0.32x** | 11,862→3,785 | Raw |
| GSE136926 | Human heart aging | **0.76x** | 1,294→980 | Pre-normalized |
| GSE111281 | Human skin aging | **0.75x** | 107,107→80,310 | Raw (precursor) |
| GSE111174 | Human blood aging | **0.71x** | 1.48M→1.05M | Raw (precursor) |
| GSE94410 | HUVEC RS | **5.14x UP** | 3,200→16,459 CPM | CPM-corrected |

**Verdict:** DOWN in fibroblasts (0.26-0.32x), human heart (0.76x), skin (0.75x), and blood (0.71x). The only OFF candidate declining across multiple human tissues in vivo. However, **UP in senescent HUVECs** (CPM 5.14x). No inflammaging confound (miR-92a is not immune-enriched; it is part of the miR-17~92 proliferative cluster silenced during senescence; Hackl et al., *Aging Cell*, 2010, PMID: 20409078).

---

### 5.3 miR-16-5p - Cross-Cell-Type OFF-Switch (Fibroblasts + Rat Kidney)

| Dataset | Cell/Tissue | FC | Level | Data Type |
|---------|------------|-----|-------|-----------|
| GSE299871 | WI-38 DXR (n=2) | **0.37x** | 3,172→1,183 CPM | CPM-corrected |
| GSE299871 | WI-38 RS (n=2) | **0.37x** | 3,172→1,169 CPM | CPM-corrected |
| GSE117818 | MRC-5 RS (precursor) | **0.53x** | 6,825→3,623 | Raw |
| GSE94410 | HUVEC RS | **0.89x (stable)** | 574→513 CPM | CPM-corrected |
| GSE172269 | Rat kidney aging | **0.58x** | 38,321→22,357 | Raw (pending CPM) |
| GSE111174 | Human blood aging | **0.61x** | 68,945→41,870 | Raw (precursor) |

**Verdict:** DOWN in fibroblasts (0.37-0.53x), rat kidney (0.58x), and human blood (0.61x). After CPM correction, the HUVEC decline is **no longer significant** (0.89x, effectively stable). This weakens the "cross-cell-type" claim - miR-16 is primarily a fibroblast + kidney OFF switch, not fibroblast + endothelial. Mechanistically linked to cell cycle arrest (targets cyclins/CDKs; Linsley et al., *RNA*, 2007, PMID: 17210802).

---

### 5.4 miR-17-5p - Strong Fibroblast OFF-Switch

| Dataset | Cell/Tissue | FC | Level | Data Type |
|---------|------------|-----|-------|-----------|
| GSE299871 | WI-38 DXR (n=2) | **0.19x** | 472→88 CPM | CPM-corrected |
| GSE299871 | WI-38 RS (n=2) | **0.15x** | 472→69 CPM | CPM-corrected |
| GSE117818 | MRC-5 RS (precursor) | **0.34x** | 576→197 | Raw |
| GSE202120 | HAEC irr. 72h | **0.68x** | 5,156→3,481 | Raw |
| GSE111174 | Human blood aging | **0.59x** | 3,017→1,775 | Raw (precursor) |
| GSE94410 | HUVEC RS | **11.0x UP** | 266→2,924 CPM | CPM-corrected |

**Verdict:** Strong decline in fibroblasts (0.15-0.34x) and HAECs (0.68x). **Dramatically UP in HUVECs** (CPM 11x) - opposite direction. Part of the miR-17~92 cluster (Faraonio et al., *Cell Death Differ*, 2012, PMID: 22052189).

---

### 5.5 Five-miRNA Core Senescence Signature (Fibroblasts)

Validated across both WI-38 (GSE299871) and MRC-5 (GSE117818):

| miRNA | Direction | WI-38 DXR (CPM) | MRC-5 RS (raw) |
|-------|-----------|-----------------|----------------|
| miR-34a-5p | **UP** | 1.50x | 2.81x |
| miR-155-5p | **DOWN** | 0.09x | 0.10x |
| miR-16-5p | **DOWN** | 0.37x | 0.53x |
| miR-92a-3p | **DOWN** | 0.26x | 0.32x |
| miR-17-5p | **DOWN** | 0.19x | 0.34x |

**Not part of core signature:** miR-21-5p (CPM 1.09x in WI-38 DXR - no change) and miR-22-3p (UP in WI-38 but stable in MRC-5). These were excluded because they do not replicate across independent fibroblast lines.

---

## 6. Cross-Context Concordance

### 6.1 Do Different Inducers Produce the Same miRNA Profile?

GSE299871 compares three inducers in the same cell type (WI-38, n=2 per group - hypothesis-generating):

| miRNA | DXR (CPM FC) | SDS (CPM FC) | RS (CPM FC) | Shared? |
|-------|-------------|-------------|------------|---------|
| miR-34a-5p | 1.50x UP | 1.66x UP | 1.50x UP | **Yes** |
| miR-22-3p | 1.74x UP | 1.41x UP | 1.34x UP | **Yes** |
| miR-155-5p | 0.09x DOWN | 0.23x DOWN | 0.11x DOWN | **Yes** (all DOWN) |
| miR-92a-3p | 0.26x DOWN | 0.40x DOWN | 0.26x DOWN | **Yes** |
| miR-17-5p | 0.19x DOWN | 0.32x DOWN | 0.15x DOWN | **Yes** |
| miR-29a-3p | 0.96x stable | 1.32x UP | 0.81x DOWN | **No** (variable) |
| miR-21-5p | 1.09x stable | 1.19x stable | 1.09x stable | Stable in all |

After CPM correction, the three inducers converge on a shared program of **two miRNAs UP** (miR-34a, miR-22) and **three DOWN** (miR-155, miR-92a, miR-17). miR-29a and miR-21 are **not part of the shared program** - their apparent upregulation in raw data was a library size artifact.

Note: SDS had 4.3x larger libraries than controls. The raw SDS fold changes reported in earlier analyses (e.g., "miR-34a 7.2x UP") were heavily inflated. CPM-corrected SDS fold changes (1.66x for miR-34a) are comparable to DXR (1.50x), not dramatically higher.

### 6.2 In Vitro Senescence vs. In Vivo Aging

| miRNA | In vitro DXR (CPM) | In vivo aging (mouse, per tissue) | Match? |
|-------|-------------------|----------------------------------|--------|
| miR-34a-5p | 1.50x UP | UP in 5/6 tissues (1.25-1.68x) | **Yes** |
| miR-22-3p | 1.74x UP | Stable in 4/6 tissues | **Partial** |
| miR-155-5p | 0.09x DOWN | UP in all 6 tissues (1.24-4.20x) | **No** - inflammaging |
| miR-92a-3p | 0.26x DOWN | Stable in most tissues | **Partial** |

In vivo aging fold changes (1.2-1.7x) are consistently smaller than in vitro senescence fold changes. This is expected: aged tissues are a mixture of senescent and non-senescent cells. If senescent cells comprise ~15% of tissue (Baker et al., *Nature*, 2011, PMID: 22012258), a miRNA 2x higher in senescent cells appears only ~1.15x higher in bulk tissue.

The miR-155-5p discrepancy (DOWN in vitro, UP in vivo) is a clear example of **non-cell-autonomous effects**. This means changes caused by the surrounding tissue environment rather than the internal biology of the measured cell - in this case, macrophage infiltration into aging tissues brings high miR-155 that dominates the bulk tissue signal, masking the cell-autonomous decline in resident fibroblasts and epithelial cells.

### 6.3 Blood vs. Tissue Divergence

Most miRNAs **decline** in aged human blood (GSE111174) but are **stable or UP** in aged tissues (GSE111281 skin, GSE136926 heart). This reflects immunosenescence - aged blood has fewer proliferative lymphocytes due to thymic involution (Goronzy & Weyand, *Nat Immunol*, 2013, PMID: 24048120). Blood miRNA aging studies cannot be used to infer tissue-level changes.

---

## 7. Circuit Architectures

### 7.1 Design Goal and Constraints

**Goal:** Express a cytotoxic payload (Gasdermin or DTA) only in senescent cells while sparing healthy cells.

**Hardware:** L7Ae/K-turn repressor only (no MS2CP). Multiple L7Ae mRNAs with different MREs achieve AND-gate logic:

```
L7Ae-mRNA-1: [MREs for miRNA-A] - L7Ae CDS
L7Ae-mRNA-2: [MREs for miRNA-B] - L7Ae CDS  
Payload-mRNA: [K-turn in 5'UTR] - Gasdermin or DTA CDS
```

Both miRNA-A AND miRNA-B must be active to silence both L7Ae sources and permit payload expression.

### 7.2 Performance Benchmarks

- **L7Ae K-turn repression: ~10-fold** - payload at 1/10th level when L7Ae present (Saito et al., *Nat Chem Biol*, 2010)
- **Single miRNA switch: resolves 1.3-1.5x differences** between cell populations (Endo et al., *Sci Rep*, 2016, PMID: 26902536) - but "resolves" means visually separable on FACS, not necessarily binary kill/no-kill. No quantitative transfer function published.
- **Hybrid ON+OFF switch: up to 16-fold** (Saito lab, *Mol Ther Nucleic Acids*, 2025)
- **miRNA-mediated silencing is sigmoidal**, not linear (Mukherji et al., *Nature*, 2011, PMID: 21753848). Small fold changes could produce either no response or near-binary switching depending on threshold position.

### 7.3 Selectivity Estimation Method

We estimate selectivity as the product of individual discriminations. This is an **order-of-magnitude approximation** - the actual relationship is nonlinear, and the estimates are useful for ranking architectures relative to each other but not for predicting performance. See [methods_and_statistical_framework.md](methods_and_statistical_framework.md) for detailed assumptions and caveats.

### 7.4 Approach 1 - Universal Senolytic

**Design U3: miR-34a + miR-16 + miR-92a (Dual OFF coverage)**

Using both miR-16 and miR-92a simultaneously as OFF switches provides complementary coverage - each compensates for the other's cell-type gaps.

| Cell type | miR-16 declines? | miR-92a declines? | Coverage |
|-----------|-----------------|------------------|----------|
| Fibroblasts | YES (0.37x CPM) | YES (0.26x CPM) | Both |
| Aged human heart | Stable | YES (0.76x) | miR-92a |
| Aged human skin | Stable | YES (0.75x) | miR-92a |
| Aged human blood | YES (0.61x) | YES (0.71x) | Both |
| HUVECs (senescent) | Stable (0.89x CPM) | UP (5.14x CPM) | **Neither** |

**Estimated selectivity:** ~15x in fibroblasts (both OFF switches active), ~4-6x in heart/skin (one OFF active), **~1.5x in endothelial** (neither OFF active - fails for senescent endothelial cells).

**Verdict:** Best available universal design but cannot target senescent endothelial cells. Cost: 4 mRNAs.

### 7.5 Approach 2 - Fibroblast-Specific

**Design F1: miR-34a ON + miR-155 OFF (~16x selectivity)**

| miRNA | Healthy fibroblast | Senescent fibroblast | Discrimination |
|-------|-------------------|---------------------|---------------|
| miR-34a-5p | 371 CPM → L7Ae-1 ON | 558 CPM → L7Ae-1 OFF | 1.5x |
| miR-155-5p | 9,887 CPM → L7Ae-2 ON | 889 CPM → L7Ae-2 OFF | 11x |
| **Combined** | **Payload OFF** | **Payload ON** | **~16x** |

Best in vitro proof-of-concept. Inflammaging risk in vivo.

**Design F4: miR-34a ON + miR-155 OFF + miR-92a OFF (~63x)**

Three-input AND gate for maximum safety. Cost: 4 mRNAs.

### 7.6 Comparison

| Design | Inputs | Selectivity | Applicability |
|--------|--------|------------|---------------|
| U3 | miR-34a + miR-16 + miR-92a | ~4-15x (tissue-dependent) | Broad (except endothelial) |
| **F1** | **miR-34a + miR-155** | **~16x** | Fibroblasts only |
| **F4** | **miR-34a + miR-155 + miR-92a** | **~63x** | Fibroblasts (maximum safety) |

### 7.7 Recommendations

1. **First experiment:** Test miR-34a-5p ON switch alone in senescent vs. healthy WI-38 cells. Determines if ~45 copies/cell activates the switch.
2. **Proof-of-concept:** Design F1 (miR-34a + miR-155) in DXR-senescent WI-38 fibroblasts.
3. **If F1 works:** Progress to F4 (triple input) for safety margin before in vivo.
4. **If miR-34a threshold too low:** The planned doxorubicin small RNA-seq becomes urgent.

---

## 8. The Human In Vivo Gap

No publicly deposited small RNA-seq dataset exists with paired pre/post-chemotherapy blood samples from patients. The closest study (Mikulski/Fendler 2024, PMID: 38650024 - serum miRNA-seq at 4 timepoints during myeloablative ASCT, 10 patients) did not deposit data publicly. The planned experiments fill a field-wide gap.

---

## 9. Conclusions

1. **miR-34a-5p is the only consistent ON-switch candidate**, UP in 18/21 analyses across 4 inducers, 4 human cell types, 3 organisms. After CPM correction, the DXR fold change is 1.5x (~45 estimated copies/cell). Whether this is sufficient for switch activation is the critical empirical question.

2. **miR-155-5p is the strongest OFF-switch** (11x decline, CPM-corrected) but fibroblast-specific. UP in senescent HUVECs (CPM 1.81x) and aged tissues (inflammaging).

3. **miR-92a-3p is the broadest OFF-switch**, declining in fibroblasts AND human heart, skin, and blood. No inflammaging confound. But UP in senescent HUVECs.

4. **CPM normalization eliminated two previously reported candidates** (miR-29a-3p and miR-21-5p). Their apparent upregulation was entirely a library size artifact. This underscores the importance of proper normalization.

5. **The core fibroblast senescence signature** (miR-34a UP; miR-155, miR-16, miR-92a, miR-17 DOWN) replicates across WI-38 and MRC-5 fibroblast lines.

6. **A truly universal circuit is not achievable** - no OFF-switch declines in senescent endothelial cells after CPM correction. Tissue-specific panels may be more realistic.

7. **Blood and tissue miRNA aging patterns diverge** due to immunosenescence. Blood studies cannot inform tissue-level circuit design.

8. **The recommended first experiment** is testing miR-34a-5p switch activation at endogenous senescent cell levels. All circuit architectures depend on this.

---

## References

1. RNA Biology 2025. DOI: 10.1080/15476286.2025.2551299 (GSE299871)
2. Terlecki-Zaniewicz L et al. *Redox Biology*. 2018;18:77-83. PMC: PMC6037909 (GSE94410)
3. Wagner V et al. *Nat Biotechnol*. 2024;42:109-118. PMID: 37106037 (GSE217458)
4. Kim JY et al. *Aging*. 2014;6(7):524-544. PMID: 25063768 (GSE55164)
5. Peiris HN et al. *Front Mol Biosci*. 2022. PMID: 36213127 (GSE200330)
6. He L et al. *Nature*. 2007;447:1130-1134. PMID: 17554337 (miR-34a/p53)
7. Yamakuchi M et al. *PNAS*. 2008;105(36):13421-13426. PMID: 18755897 (miR-34a/SIRT1)
8. O'Connell RM et al. *PNAS*. 2007;104(5):1604-1609. PMID: 17242365 (miR-155 in macrophages)
9. Baker DJ et al. *Nature*. 2011;479:232-236. PMID: 22012258 (senescent cell burden)
10. Faraonio R et al. *Cell Death Differ*. 2012;19(4):616-624. PMID: 22052189 (miR-17 family)
11. Linsley PS et al. *RNA*. 2007;13(7):1012-1020. PMID: 17210802 (miR-16/cell cycle)
12. Hackl M et al. *Aging Cell*. 2010;9(2):291-296. PMID: 20409078 (miR-17~92 in senescence)
13. Mann M et al. *PLoS One*. 2017;12(7):e0159724. PMID: 27447824 (miR-155 in M1 macrophages)
14. Tabula Muris Consortium. *Nature*. 2020;583:590-595. PMID: 32669714 (immune cells in aging)
15. Yin Q et al. *Cell Commun Signal*. 2024;22:386. PMID: 38987851 (exosomal miR-155)
16. He J et al. *Hum Mutat*. 2025;2025:6771390. PMID: 40486266 (exosomal miR-155)
17. Goronzy JJ, Weyand CM. *Nat Immunol*. 2013;14(5):428-436. PMID: 24048120 (immunosenescence)
18. Tam S et al. *Brief Bioinform*. 2015;16(6):950-963. PMID: 25888698 (normalization)
19. Schurch NJ et al. *RNA*. 2016;22(6):839-851. PMID: 27022035 (replicate requirements)
20. Giraldez MD et al. *Nat Biotechnol*. 2018;36:746-757. PMID: 30010675 (small RNA-seq biases)
21. Mukherji S et al. *Nature*. 2011;473:382-386. PMID: 21753848 (miRNA threshold model)
22. Bissels U et al. *RNA*. 2009;15(12):2375-2384. PMID: 19850911 (absolute miRNA quantification)
23. Engel et al. *Sci Rep*. 2022. PMID: 36402833 (GSE202120)
24. Bushel PR et al. *Sci Data*. 2022;9:252. PMID: 35551205 (GSE172269)
25. Ma Z et al. *Front Physiol*. 2019;10:1226. PMID: 31607954 (GSE136926)
26. Mikulski M, Fendler W et al. 2024. PMID: 38650024 (ASCT serum miRNA-seq)
27. Endo K et al. *Sci Rep*. 2016;6:21991. PMID: 26902536 (switch resolution)
28. Saito H et al. *Nat Chem Biol*. 2010;6:71-78 (L7Ae/K-turn)
29. Fujita Y et al. *Sci Adv*. 2022;8(1):eabj1793 (ON/OFF switch)
30. Franceschi C et al. *Ann N Y Acad Sci*. 2000;908:244-254. PMID: 10911963 (inflammaging)
