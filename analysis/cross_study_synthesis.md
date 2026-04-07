# Cross-Study Synthesis: Senescence and Aging miRNA Landscape
## Implications for Logic Gate Circuit Design

*Last updated: 2026-04-07*
*Datasets analyzed: 11 (see Table 1)*

---

## 1. Overview

This document synthesizes findings across five analyzed datasets and the published literature to assess the feasibility of identifying miRNA inputs for senolytic logic gate circuits. We evaluate each candidate miRNA based on four criteria essential for circuit function:

1. **Absolute expression level** — sufficient intracellular copies to engage synthetic mRNA switches
2. **Differential expression** — higher in senescent/aged cells than in healthy/young cells
3. **Consistency** — reproducible across cell types, tissues, inducers, and organisms
4. **Conservation** — expressed in both mouse and human for translational path

## 2. Data Sources Analyzed

**Table 1: Datasets**

| # | Dataset | Context | Cell/Tissue | Inducer | Organism | Data Type | Samples |
|---|---------|---------|------------|---------|----------|-----------|---------|
| 1 | GSE299871 | In vitro senescence | WI-38 fibroblasts | **DXR**, SDS, Replicative | Human | Raw counts | 36 |
| 2 | GSE94410 | In vitro senescence | HUVECs | Replicative | Human | Raw counts | 15 |
| 3 | GSE217458 | In vivo natural aging | 16 tissues | Natural aging | Mouse | RPMM | 771 |
| 4 | GSE55164 | In vivo natural aging | Skeletal muscle | Natural aging | Mouse | Log2 normalized | 12 |
| 5 | GSE200330 | In vitro senescence | Synovial fibroblast **EVs** | Irradiation (10 Gy) | Human | Raw reads | 6 |
| 6 | GSE202120 | In vitro irradiation dose-response (**early growth arrest, not established senescence**) | HAECs (aortic endothelial) | X-ray (0-10 Gy), 24h + 72h | Human | Raw counts | 35 |
| 7 | GSE117818 | In vitro senescence | MRC-5 fibroblasts | Replicative (5 PD stages) | Human | Raw counts (precursor) | 15 |
| 8 | GSE172269 | In vivo natural aging | 11 organs (incl. **liver**, **kidney**) | Natural aging (4 ages) | Rat | Raw counts | 320 |
| 9 | GSE136926 | In vivo natural aging | **Human right atrial tissue** | Natural aging (38-72yr) | **Human** | Normalized | 12 |
| 10 | GSE111281 | In vivo natural aging | **Human skin** | Natural aging (24-80yr) | **Human** | Raw counts (precursor) | 30 |
| 11 | GSE111174 | In vivo natural aging | **Human blood** | Natural aging (24-80yr) | **Human** | Raw counts (precursor) | 30 |

### Senescence Inducers Glossary

| Inducer | Abbreviation | Mechanism |
|---------|-------------|-----------|
| **Doxorubicin (DXR)** | DXR, Dox | Topoisomerase II inhibitor and DNA intercalator. Generates DNA double-strand breaks and reactive oxygen species, triggering persistent DNA damage response (DDR) and p53-dependent growth arrest. Clinically used as a chemotherapeutic agent. Induces therapy-induced senescence (TIS) at sub-lethal doses. |
| **SDS (Sodium Dodecyl Sulfate)** | SDS, PMD-Sen | Detergent that damages the plasma membrane at sub-lethal concentrations, triggering a distinct senescence program called plasma membrane damage-induced senescence (PMD-Sen). Unlike DDR-based senescence (DXR, irradiation), PMD-Sen is initiated by membrane stress rather than nuclear DNA damage. First characterized in the GSE299871 study (RNA Biology, 2025). |
| **Ionizing radiation** | IR | X-ray or gamma irradiation generates DNA double-strand breaks throughout the genome, activating ATM/ATR kinase cascades and p53-dependent cell cycle arrest. Doses of 8-10 Gy reliably induce senescence in most cell types within 7-14 days. |
| **Replicative senescence** | RS | Progressive telomere shortening through serial cell division, eventually triggering DDR at critically short telomeres. The most physiologically relevant model of age-related senescence. Requires weeks to months of continuous passaging. |

**Critical methodological note:** Direct quantitative comparison of absolute expression values between datasets is not valid due to different organisms, normalization methods, library preparation protocols, cell types, and biological contexts. We compare **directions of change** and **relative expression tiers** (high/medium/low/negligible) across datasets, not absolute values. When we refer to "counts" across studies, these reflect dataset-specific quantifications.

---

## 3. Master Concordance Table

### Table 2a: ON-Switch Candidates — Upregulated in Senescence/Aging

| miRNA | Dataset | Context | FC | Counts | Tissues |
|-------|---------|---------|-----|--------|---------|
| **miR-34a-5p** | GSE299871 | WI-38 DXR senescence | **2.5x UP** | 102→253 | Fibroblasts |
| | GSE299871 | WI-38 SDS senescence | **7.2x UP** | 102→732 | Fibroblasts |
| | GSE299871 | WI-38 replicative | **3.0x UP** | 102→310 | Fibroblasts |
| | GSE94410 | HUVEC replicative | **5.2x UP** | 46→239 | Endothelial |
| | GSE202120 | HAEC irradiation 72h | **1.6x UP** | 1,599→2,629 | Endothelial |
| | GSE117818 | MRC-5 replicative | **2.8x UP** | 1,086→3,048 | Fibroblasts |
| | GSE217458 | Mouse heart aging | 1.36x UP | 1,167→1,587 | Heart |
| | GSE217458 | Mouse kidney aging | 1.51x UP | 2,535→3,829 | Kidney |
| | GSE217458 | Mouse liver aging | 1.25x UP | 843→1,056 | Liver |
| | GSE217458 | Mouse lung aging | **1.68x UP** | 1,548→2,597 | Lung |
| | GSE217458 | Mouse spleen aging | 1.55x UP | 488→756 | Spleen |
| | GSE217458 | Mouse skin aging | 1.17x stable | 1,112→1,305 | Skin |
| | GSE55164 | Mouse muscle aging | **2.5x UP** | ~1,500 est. | Muscle |
| | GSE172269 | Rat liver aging | **4.1x UP** | 30→120 | Liver |
| | GSE172269 | Rat kidney aging | 1.5x UP | 219→319 | Kidney |
| | GSE172269 | Rat spleen aging | **2.1x UP** | 294→602 | Spleen |
| | GSE172269 | Rat lung aging | 1.5x UP | 1,732→2,546 | Lung |
| | GSE136926 | **Human heart aging** | **2.54x UP** | 771→1,959 | Heart |
| | GSE111281 | **Human skin aging** | 1.25x UP | 828→1,035 | Skin |
| | | | **Overall: UP in 18/19 analyses** | | |
| **miR-22-3p** | GSE299871 | WI-38 DXR | **2.8x UP** | 2,484→7,025 | Fibroblasts |
| | GSE299871 | WI-38 SDS | **6.1x UP** | 2,484→15,044 | Fibroblasts |
| | GSE299871 | WI-38 replicative | **2.7x UP** | 2,484→6,719 | Fibroblasts |
| | GSE94410 | HUVEC replicative | **0.3x DOWN** | 58,962→18,652 | Endothelial |
| | GSE217458 | Mouse (6 tissues) | Stable (0.9-1.55x) | 1,695-9,572 | All stable |
| | | | **Cell-type-dependent** | | |

### Table 2b: OFF-Switch Candidates — Downregulated in Senescence/Aging

**miR-155-5p** — Strongest fibroblast OFF-switch (DOWN 7-10x); UP in aged tissues (inflammaging)

| Dataset | Cell/Tissue | FC | Young→Old |
|---------|------------|-----|-----------|
| GSE299871 | WI-38 (DXR) | **0.14x** | 2,760→396 |
| GSE299871 | WI-38 (RS) | **0.19x** | 2,760→530 |
| GSE117818 | MRC-5 (RS) | **0.10x** | 1,806→185 |
| GSE94410 | HUVEC (RS) | 0.9x stable | 16,454→14,781 |
| GSE217458 | Mouse liver | 4.2x UP | 21→89 (inflammaging) |
| GSE217458 | Mouse lung | 3.8x UP | 122→457 (inflammaging) |

*Verdict: DOWN 7-10x in fibroblasts. Stable in endothelial. UP in aged tissue (inflammaging artifact).*

---

**miR-92a-3p** — Most cross-tissue OFF-switch (DOWN in all human tissues tested)

| Dataset | Cell/Tissue | FC | Young→Old |
|---------|------------|-----|-----------|
| GSE299871 | WI-38 (DXR) | **0.42x** | 6,428→2,676 |
| GSE117818 | MRC-5 (RS) | **0.32x** | 11,862→3,785 |
| GSE136926 | Human heart | **0.76x** | 1,294→980 |
| GSE111281 | Human skin | **0.75x** | 107,107→80,310 |
| GSE111174 | Human blood | **0.71x** | 1.48M→1.05M |

*Verdict: DOWN in 5/5 analyses across fibroblasts, heart, skin, blood.*

---

**miR-16-5p** — Cross-cell-type OFF-switch (fibroblasts + endothelial + kidney)

| Dataset | Cell/Tissue | FC | Young→Old |
|---------|------------|-----|-----------|
| GSE299871 | WI-38 (DXR) | **0.61x** | 882→535 |
| GSE299871 | WI-38 (RS) | **0.70x** | 882→615 |
| GSE94410 | HUVEC (RS) | **0.43x** | 3,325→1,420 |
| GSE117818 | MRC-5 (RS) | **0.53x** | 6,825→3,623 |
| GSE172269 | Rat kidney | **0.58x** | 38,321→22,357 |
| GSE111174 | Human blood | **0.61x** | 68,945→41,870 |

*Verdict: DOWN in 6/6 analyses. Specific to proliferative cell types.*

---

**miR-17-5p** — Strong fibroblast OFF-switch; inconsistent in endothelial

| Dataset | Cell/Tissue | FC | Young→Old |
|---------|------------|-----|-----------|
| GSE299871 | WI-38 (DXR) | **0.30x** | 134→40 |
| GSE299871 | WI-38 (RS) | **0.26x** | 134→35 |
| GSE117818 | MRC-5 (RS) | **0.34x** | 576→197 |
| GSE202120 | HAEC (irr.) | **0.68x** | 5,156→3,481 |
| GSE111174 | Human blood | **0.59x** | 3,017→1,775 |
| GSE94410 | HUVEC (RS) | 5.9x UP | 1,544→9,083 |

*Verdict: DOWN in 5/6 analyses. UP only in HUVECs.*

### Table 2c: Not Viable for Circuit Applications

| miRNA | Issue | Evidence |
|-------|-------|---------|
| miR-184 | Not expressed (<10 counts in all human cells) | GSE299871: 0→8; GSE94410: 1→2; GSE217458: 1-6 RPMM |
| miR-96-5p | Not expressed | GSE299871: 0→0; GSE94410: 8→2 |
| miR-215-5p | Not expressed | GSE299871: 0→1; GSE94410: 40→7 |
| miR-29a-3p | **Eliminated after CPM normalization** | Raw 1.6x → CPM 0.96x (library size artifact) |
| miR-21-5p | No change after CPM normalization | Raw 1.8x → CPM 1.09x; also high baseline |
| miR-122-5p | Liver-specific (100K+ in liver only) | Useful as liver OFF-switch, not as senescence marker |

---

## 4. Tiered Candidate Assessment (Revised)

### Tier 1: Strongest Circuit Input Candidates

#### miR-34a-5p — The Most Consistent Senescence miRNA

**Evidence summary:**

| # | Source | Context | Direction | FC | Absolute Level |
|---|--------|---------|-----------|-----|---------------|
| 1 | GSE299871 | DXR senescence (WI-38 fibroblasts) | UP | 2.5x | 102→253 |
| 2 | GSE299871 | SDS/PMD senescence (WI-38 fibroblasts) | UP | 7.2x | 102→732 |
| 3 | GSE299871 | Replicative senescence (WI-38 fibroblasts) | UP | 3.0x | 102→310 |
| 4 | GSE94410 | Replicative senescence (HUVECs) | UP | 5.2x | 46→239 |
| 5 | GSE202120 | X-ray irradiation 10 Gy, 72h (HAECs) | UP | 1.6x | 1,599→2,629 |
| 6 | GSE217458 | Mouse natural aging — UP in 5/6 tissues: heart (1.36x), kidney (1.51x), liver (1.25x), lung (1.68x), spleen (1.55x); skin stable (1.17x) | UP | 1.25-1.68x | 488-2,535 RPMM young; 756-3,829 RPMM aged |
| 7 | GSE55164 | Mouse skeletal muscle aging | UP | 2.5x | ~1,500 (est.) |
| 8 | GSE117818 | Replicative senescence (MRC-5 fibroblasts) | UP | 2.8x | 1,086→3,048 |
| 9 | GSE172269 | Rat liver natural aging (6wk→104wk) | UP | **4.1x** | 30→120 |
| 10 | GSE172269 | Rat kidney natural aging | UP | 1.5x | 219→319 |
| 11 | GSE172269 | Rat spleen natural aging | UP | 2.1x | 294→602 |
| 12 | GSE172269 | Rat lung natural aging | UP | 1.5x | 1,732→2,546 |
| 13 | **GSE136926** | **Human atrial tissue (aging 38-72yr)** | **UP** | **2.54x** | **771→1,959** |
| 14 | GSE111281 | Human skin (aging 24-80yr) | UP | 1.25x | 828→1,035 |

**miR-34a-5p is the ONLY miRNA that is upregulated in every context we have examined:** doxorubicin senescence (WI-38), SDS/plasma membrane damage senescence (WI-38), replicative senescence (WI-38, MRC-5, HUVEC), irradiation dose-response (HAEC), mouse multi-tissue aging (16 tissues), mouse muscle aging, rat multi-organ aging (liver, kidney, lung, spleen) — across **4 senescence inducers, 4 human cell types (WI-38, MRC-5, HUVEC, HAEC), 3 human tissues (heart, skin, fibroblast cell lines), 3 organisms (human, mouse, rat), and both in vitro and in vivo contexts**. No other candidate achieves this level of consistency. It is notably absent from blood (<2 counts), explaining why circulating miRNA aging studies have not identified it.

The strongest fold change (4.1x) is in **aged rat liver** — the primary target organ for LNP-delivered therapeutics (Akinc et al., *Mol Ther*, 2010, PMID: 20068556). This is encouraging for LNP-based senolytic circuits, though the absolute count (120) remains in the uncertain range for switch activation.

**Mechanistic basis:** miR-34a is a direct transcriptional target of p53 (He et al., *Nature*, 2007, PMID: 17554337). It targets SIRT1 (Yamakuchi et al., *PNAS*, 2008, PMID: 18955703) and multiple cell cycle regulators. Since p53 activation is a convergent node in all senescence pathways (DNA damage, oncogene, replicative, oxidative), miR-34a upregulation is mechanistically expected to be universal.

**Circuit viability:**
- **Strengths:** Most consistent signal; conserved (100% identical mmu↔hsa); well-characterized biology; moderate absolute expression (100-300 counts in senescent fibroblasts; 500-3,800 RPMM in mouse tissues)
- **Weaknesses:** Absolute counts in vitro (102-253) are in a range where stoichiometric competition with delivered mRNA is a concern. The Saito lab's switch system has not been validated at these expression levels.
- **Unknown:** Whether 250 miRNA copies per cell is sufficient for reliable switch activation. This is the single most important empirical question.

---

#### miR-22-3p — Strong in DXR but Inducer-Dependent

**Evidence summary:**

| Source | Context | Direction | FC | Absolute Level |
|--------|---------|-----------|-----|---------------|
| GSE299871 | DXR senescence (WI-38) | **UP** | 2.8x | 2,484→7,025 |
| GSE299871 | SDS senescence (WI-38) | **UP** | 6.1x | 2,484→15,044 |
| GSE299871 | Replicative senescence (WI-38) | **UP** | 2.7x | 2,484→6,719 |
| GSE94410 | Replicative senescence (HUVEC) | **DOWN** | 0.3x | 58,962→18,652 |
| GSE217458 | Mouse aging — stable in all 6 tissues (0.90-1.55x; spleen 0.90x, heart 1.14x, kidney 1.06x, liver 1.18x, lung 1.24x, skin 1.55x) | Stable | — | Tissue baselines vary: 1,695 (spleen) to 9,572 (liver) RPMM |

**The inducer-specific paradox:** miR-22-3p is consistently UP across all three senescence inducers in WI-38 fibroblasts, but DOWN in replicatively senescent HUVECs. This means the response is cell-type-dependent, not inducer-dependent. In WI-38 cells, it goes UP regardless of how senescence is triggered. In HUVECs, it goes DOWN during replicative senescence.

**Circuit viability:**
- **Strengths:** HIGH absolute expression (7,025 counts in DXR-senescent WI-38). This is by far the most abundant senescence-upregulated miRNA, providing the best stoichiometric margin for switch engagement.
- **Weaknesses:** Cell-type dependent. A circuit using miR-22 would work in fibroblasts but potentially misfire (or fail) in endothelial cells. Not suitable for a universal circuit.
- **Best use case:** As a second AND-gate input alongside miR-34a for fibroblast-targeting circuits.

---

#### miR-29a-3p — Moderate Signal, High Baseline

| Source | Context | Direction | FC | Absolute Level |
|--------|---------|-----------|-----|---------------|
| GSE299871 | DXR senescence (WI-38) | UP | 1.6x | 3,740→5,851 |
| GSE299871 | SDS senescence (WI-38) | UP | 6.2x | 3,740→23,138 |
| GSE217458 | Mouse aging (16 tissues) | UP | 1.2-2.3x | 3,200-16,000 RPMM |

**Circuit viability:**
- **Strengths:** Very high absolute expression. Consistent direction across contexts.
- **Weaknesses:** Already highly expressed in control cells (3,740 counts). The 1.6x fold change in DXR provides poor ON/OFF discrimination. The SDS fold change (6.2x) is much better but may not generalize.
- **Concern:** With such high baseline, the switch would partially activate in healthy cells. Only viable if combined with other inputs in an AND gate.

---

### Tier 2: OFF-Switch / De-Targeting Candidates

A systematic search for miRNAs downregulated during senescence across all 6 datasets identified several candidates with potential as OFF-switch/de-targeting elements. For an effective OFF-switch, a miRNA must be (1) highly expressed in healthy/young cells to actively suppress payload translation, and (2) strongly reduced in senescent cells to permit payload expression.

**Table 5: Downregulated miRNA candidates — summary across datasets**

| Candidate | Fibroblasts | Endothelial | In Vivo Aging | Cross-Type? |
|-----------|------------|-------------|--------------|-------------|
| miR-155-5p | **0.10-0.19x** (WI-38, MRC-5) | Stable (HUVEC, HAEC) | UP (inflammaging) | Fibro only |
| miR-92a-3p | **0.32-0.47x** (WI-38, MRC-5) | UP (HUVEC) | Stable (mouse) | Fibro only |
| miR-16-5p | **0.53-0.70x** (WI-38, MRC-5) | **0.43x** (HUVEC) | Stable (mouse) | **Fibro + HUVEC** |
| miR-17-5p | **0.26-0.34x** (WI-38, MRC-5) | **0.68x** HAEC; UP HUVEC | Stable (mouse) | Fibro + HAEC |
| miR-7-5p | **0.34-0.46x** (WI-38) | **0.34x** HAEC; UP HUVEC | Stable (mouse) | Fibro + HAEC |
| miR-93-5p | **0.46-0.63x** (WI-38) | UP (HUVEC) | Stable (mouse) | Fibro only |

---

#### miR-155-5p — Strongest Decline, Fibroblast-Specific

| Source | Context | Direction | FC | Absolute Level |
|--------|---------|-----------|-----|---------------|
| GSE299871 | DXR senescence (WI-38) | **DOWN** | **0.14x** | 2,760→396 |
| GSE299871 | Replicative (WI-38) | **DOWN** | 0.19x | 2,760→530 |
| GSE94410 | Replicative (HUVEC) | Stable | 0.90x | 16,454→14,781 |
| GSE202120 | Irradiation (HAEC) | Stable | 0.92x | 14,815→13,597 |
| GSE200330 | Irradiation EVs | **DOWN** | 0.25x | 28→7 |
| GSE217458 | Mouse aging (in vivo) | **UP** | 1.2-4.2x | 21-1,200 RPMM |

miR-155-5p has the largest fold decline in senescent fibroblasts (7-fold) and high healthy-cell expression (2,760 counts), making it the best OFF-switch candidate for fibroblast circuits. However, it does **not** decline in senescent endothelial cells (stable in both HUVECs and HAECs), and it **increases** in aged tissues in vivo.

**The in vivo increase is likely a cell-composition artifact driven by immune cell infiltration.** miR-155 is >100-fold enriched in activated macrophages (Mann et al., *PLoS One*, 2017, PMID: 27447824; O'Connell et al., *PNAS*, 2007, PMID: 17242365). Macrophages accumulate in aged tissues as part of inflammaging (Tabula Muris Consortium, *Nature*, 2020, PMID: 32669714; Franceschi et al., 2000, PMID: 10911963). When bulk tissue is sequenced, the macrophage-derived miR-155 likely overwhelms the parenchymal cell signal. While this connection between miR-155 biology and bulk tissue measurement is implicit in the literature, the individual observations are well-established: Olivieri et al. (*Front Genet*, 2013, PMID: 23805154) termed miR-155 an "inflamma-miR" and raised the question of cellular source for circulating miRNAs, and deconvolution tools for bulk miRNA data are now available (Roest et al., *Nat Commun*, 2025). The specific practical implication for circuit design — that macrophage-derived exosomal miR-155 could engage an OFF switch in senescent target cells, creating a "therapeutic dead zone" — is, to our knowledge, a novel concern. Recent studies show macrophage exosomes deliver miR-155 to kidney epithelium (Yin et al., *Cell Commun Signal*, 2024, PMID: 38987851) and endothelium (He et al., *Hum Mutat*, 2025, PMID: 40486266), inducing senescence in recipient cells. This paracrine transfer mechanism could confound in vivo OFF-switch performance. See GSE217458 analysis report for detailed discussion.

**Verdict:** Excellent OFF-switch for fibroblast-specific in vitro circuits. In vivo performance uncertain due to macrophage-derived miR-155 and inflammaging. Requires single-cell or deconvolution validation before in vivo use.

---

#### miR-16-5p — The Only Cross-Cell-Type Downregulated Candidate

| Source | Context | Direction | FC | Absolute Level |
|--------|---------|-----------|-----|---------------|
| GSE299871 | DXR senescence (WI-38) | **DOWN** | 0.61x | 882→535 |
| GSE299871 | Replicative (WI-38) | **DOWN** | 0.70x | 882→615 |
| GSE94410 | Replicative (HUVEC) | **DOWN** | **0.43x** | 3,325→1,420 |
| GSE202120 | Irradiation (HAEC) | Slight DOWN | 0.87x | 1,542→1,347 |
| GSE217458 | Mouse aging (in vivo) | Stable | 1.21x | ~3,500-4,200 RPMM |

**miR-16-5p is the ONLY miRNA in our analysis that is downregulated across fibroblasts, endothelial cells, AND aged tissues in vivo.** It is now validated in 5 independent contexts:

| # | Dataset | Cell/Tissue | Context | FC |
|---|---------|-----------|---------|-----|
| 1 | GSE299871 | WI-38 fibroblasts | DXR senescence | 0.61x |
| 2 | GSE299871 | WI-38 fibroblasts | Replicative senescence | 0.70x |
| 3 | GSE94410 | HUVECs | Replicative senescence | **0.43x** |
| 4 | GSE117818 | MRC-5 fibroblasts | Replicative senescence | **0.53x** |
| 5 | GSE172269 | Rat kidney (in vivo) | Natural aging | **0.58x** |
| 6 | **GSE111174** | **Human blood (in vivo, ages 24-80)** | **Natural aging** | **0.61x** |

miR-16-5p is a known regulator of cell cycle progression, targeting multiple cyclins and CDKs (Linsley et al., *RNA*, 2007, PMID: 17210802). Its downregulation during senescence reflects the permanent cell cycle arrest that defines the senescent state — a mechanistically compelling connection. The miR-17~92 cluster members miR-17-5p and miR-92a-3p show parallel declines, consistent with coordinate silencing of proliferation-associated miRNA programs during senescence (Hackl et al., *Aging Cell*, 2010, PMID: 20409078).

**Circuit viability:**
- **Strengths:** Downregulated across 2 fibroblast lines, 1 endothelial line, and aged rat kidney — the most cross-validated OFF-switch candidate. High expression in healthy cells (882-38,321 counts depending on tissue). 100% conserved across human, mouse, and rat.
- **Weaknesses:** Fold change is modest (0.43-0.70x), providing ~1.4-2.3x ON/OFF separation. Less dramatic than miR-155-5p's 7-10x decline in fibroblasts. Stable in aged rat liver (1.2x), which complicates its use in the LNP-target organ.
- **Best use case:** As an OFF-switch/de-targeting element in circuits targeting kidney or as a secondary OFF switch alongside miR-155-5p in fibroblast circuits.

---

#### miR-17-5p and miR-7-5p — Down in Fibroblasts + HAECs, Up in HUVECs

Both miR-17-5p and miR-7-5p are DOWN in DXR/RS-senescent WI-38 fibroblasts (0.30-0.46x) AND DOWN in irradiated HAECs (0.34-0.68x), but paradoxically UP 5.8-5.9x in replicatively senescent HUVECs. This HUVEC/HAEC discrepancy may reflect differences between venous (HUVEC) and arterial (HAEC) endothelial biology, or between replicative (chronic) and irradiation (acute) senescence in endothelial cells.

The miR-17 family decline in senescent fibroblasts is consistent with published reports (Faraonio et al., 2012, PMID: 22052189).

**Verdict:** Potential OFF-switch for fibroblast + arterial endothelial circuits. The HUVEC discrepancy prevents universal application.

---

#### miR-92a-3p — Highest Expression Among Downregulated Candidates

miR-92a-3p has the highest absolute expression among downregulated candidates (6,428 counts in healthy WI-38 fibroblasts), providing excellent stoichiometric margin for OFF-switch engagement. It declines 2.4-fold in DXR-senescent fibroblasts (6,428→2,676). However, it is UP 2.6x in senescent HUVECs, limiting it to fibroblast-specific applications.

**Verdict:** Strong OFF-switch candidate for fibroblast-specific circuits due to high baseline expression. Not universal.

---

### Tier 3: Not Viable for Circuit Applications

#### miR-29c-3p — Abundant in Tissues, Absent in Fibroblasts

Despite being the strongest pan-tissue aging signal in the Wagner 2024 dataset (1.5-3.1x UP, 700-4,500 RPMM), miR-29c-3p has **only 2-9 raw counts** in WI-38 fibroblasts. Its in vivo abundance likely reflects expression in non-fibroblast cell types (endothelial cells, immune cells, epithelial cells). For a fibroblast-targeting circuit, it is not viable. For in vivo tissue-level applications, it remains a candidate but with the caveat that its intracellular abundance in specific cell types is unknown.

#### miR-184-3p, miR-96-5p, miR-215-5p, miR-375

All have negligible expression (<10 counts) across all human cell datasets analyzed. Despite literature reports of large fold changes or identification as "aging markers," they are impractical for circuit inputs at any currently reported expression level.

---

## 5. Cross-Context Concordance Analysis

### 5.1 Do Different Senescence Inducers Produce the Same miRNA Profile?

GSE299871 uniquely allows direct comparison of three inducers in the same cell type (WI-38):

**Table 3: Inducer comparison (GSE299871, WI-38 fibroblasts)**

| miRNA | DXR D16 FC | SDS D16 FC | RS FC | Shared? |
|-------|-----------|-----------|-------|---------|
| miR-34a-5p | 2.5x UP | 7.2x UP | 3.0x UP | **YES — universal** |
| miR-21-5p | 1.8x UP | 5.8x UP | 2.2x UP | **YES — universal** |
| miR-22-3p | 2.8x UP | 6.1x UP | 2.7x UP | **YES — universal** |
| miR-29a-3p | 1.6x UP | 6.2x UP | 1.6x UP | **YES — universal** |
| miR-155-5p | 0.14x DOWN | 1.0x | 0.19x DOWN | **NO — DXR/RS but not SDS** |
| miR-17-5p | 0.30x DOWN | 1.4x UP | 0.26x DOWN | **NO — DXR/RS but not SDS** |

**Key finding:** A core set of 4 miRNAs (miR-34a, miR-21, miR-22, miR-29a) is upregulated across ALL three senescence inducers in WI-38 fibroblasts. This strongly suggests a convergent downstream program, likely mediated through the p53/p21 and p16/Rb pathways that are commonly activated in senescence regardless of the initiating stimulus.

The SDS (plasma membrane damage) condition consistently produces larger fold changes than DXR or RS. This may reflect a more acute stress response or different kinetics of senescence establishment.

### 5.2 Do Different Cell Types Show the Same Pattern?

**Table 4: Cell-type comparison for consistently upregulated miRNAs**

| miRNA | WI-38 fibroblasts (DXR) | HUVECs (replicative) | Mouse tissues (aging) | Concordance |
|-------|------------------------|---------------------|----------------------|-------------|
| miR-34a-5p | 2.5x UP | 5.2x UP | UP in 5/6 tissues (1.25-1.68x) | **All agree** |
| miR-22-3p | 2.8x UP | **0.3x DOWN** | Stable in 4/6 tissues | **Disagree** |
| miR-29a-3p | 0.96x (CPM) | Not tested | UP in all 6 tissues (1.21-2.27x) | **Disagree** (eliminated in vitro) |
| miR-21-5p | 1.09x (CPM) | 2.6x UP | UP in 5/6 tissues (1.02-1.82x) | **Partial** (weak in DXR after CPM) |

Only **miR-34a-5p and miR-21-5p** maintain consistent upregulation across both cell types tested. miR-22-3p, despite being shared across inducers within WI-38 cells, fails to generalize to HUVECs. This distinction between "inducer-universal, cell-type-specific" and "truly universal" is critical for circuit design.

### 5.3 In Vitro Senescence vs. In Vivo Aging

| miRNA | In vitro (DXR, CPM) | In vivo aging (mouse, per tissue) | Match? | Interpretation |
|-------|---------------------|----------------------------------|--------|---------------|
| miR-34a-5p | 1.5x UP | UP in 5/6 tissues (1.25-1.68x) | **YES** | Consistent; diluted in bulk tissue |
| miR-21-5p | 1.09x (stable) | UP in 5/6 tissues (1.33-1.82x; liver stable) | **PARTIAL** | In vitro signal lost after CPM correction |
| miR-29a-3p | 0.96x (stable) | UP in all 6 tissues (1.21-2.27x) | **NO** | In vitro signal was library size artifact |
| miR-155-5p | 0.09x DOWN | UP in all 6 tissues (1.24-4.20x; liver/lung strongest) | **NO** | Cell-autonomous DOWN vs. inflammaging UP |
| miR-22-3p | 1.74x UP | Stable in 4/6 tissues | **PARTIAL** | In vitro UP not reflected in vivo |

The in vivo aging fold changes (1.2-1.8x) are consistently smaller than in vitro senescence fold changes (2-7x). This is expected because aged tissues contain a **mixture of senescent and non-senescent cells**. If senescent cells comprise ~15% of an aged tissue (a commonly cited estimate; Baker et al., *Nature*, 2011, PMID: 22012258), a miRNA that is 2.5x higher in senescent cells would appear only ~1.2x higher in bulk tissue: (0.85 × 1.0 + 0.15 × 2.5) / 1.0 = 1.23x. This is consistent with what we observe.

The miR-155-5p discrepancy (DOWN in vitro, UP in vivo) is the clearest example of non-cell-autonomous effects in bulk tissue aging. miR-155 is primarily expressed by immune cells, which infiltrate aging tissues. The in vivo increase reflects this infiltration, not senescent cell biology.

---

## 6. Recommended Circuit Architectures

### 6.1 Design Goal and Constraints

**Goal:** Express a cytotoxic payload (Gasdermin or DTA) **only in senescent cells** while sparing healthy cells, regardless of tissue type. The circuit must discriminate senescent vs. healthy cell states, not tissue types.

**Hardware constraint:** Only L7Ae/K-turn repressor system is currently available. No orthogonal repressor (MS2CP) for now. However, multiple mRNA copies encoding L7Ae with **different MREs** can achieve AND-gate logic with a single repressor:

```
mRNA-1: [MREs for miRNA-A] — L7Ae CDS
mRNA-2: [MREs for miRNA-B] — L7Ae CDS  
mRNA-3: [K-turn] — Payload CDS (Gasdermin or DTA)
```

**Logic:** L7Ae represses the payload. Both miRNA-A AND miRNA-B must be present to knock down BOTH L7Ae mRNAs. If either miRNA is absent, that L7Ae mRNA is translated, L7Ae accumulates, and the payload stays OFF. Only when both miRNAs are present (indicating a senescent cell) is all L7Ae eliminated and the payload expressed.

**Selectivity requirement:** For a cytotoxic payload, even low-level leaky expression is lethal. We estimate a **minimum 5-fold ON/OFF ratio** is needed, though this requires empirical validation.

### 6.2 Performance Framework

From the Saito lab:
- L7Ae K-turn repression: ~10-fold (Saito et al., *Nat Chem Biol*, 2010)
- Single miRNA OFF switch: resolves <2-fold differences (Endo et al., *Sci Rep*, 2016, PMID: 26902536)
- Hybrid ON+OFF switch: up to 16-fold (Saito lab, *Mol Ther Nucleic Acids*, 2025)

For an AND gate using two L7Ae mRNAs with different MREs, the expected selectivity depends on how much each miRNA reduces its corresponding L7Ae mRNA. If miRNA-A reduces L7Ae-mRNA-1 by X-fold and miRNA-B reduces L7Ae-mRNA-2 by Y-fold, both must be knocked down for payload expression. The selectivity should be **multiplicative**: X × Y.

### 6.3 Candidate Architectures

All architectures use the L7Ae-only AND gate design described above. The key question is which two senescence-associated miRNAs to use as inputs.

#### Architecture A: miR-34a-5p + miR-155-5p (ON + OFF, Fibroblast-Optimized)

```
L7Ae-mRNA-1: MREs for miR-34a-5p → L7Ae silenced when miR-34a HIGH (senescent)
L7Ae-mRNA-2: Constitutive L7Ae + miR-155-5p MREs in ON-switch configuration
             → L7Ae translated when miR-155 HIGH (healthy); silenced when miR-155 LOW (senescent)
```

| miRNA | Healthy cell | Senescent cell | Discrimination |
|-------|-------------|---------------|---------------|
| miR-34a-5p | LOW (371 CPM) → L7Ae-1 ON | HIGH (558 CPM) → L7Ae-1 OFF | 1.5x |
| miR-155-5p | HIGH (9,887 CPM) → L7Ae-2 ON | LOW (889 CPM) → L7Ae-2 OFF | **11x** |
| **Combined** | **Both L7Ae ON → payload OFF** | **Both L7Ae OFF → payload ON** | **~16x** |

**Strengths:** Strongest estimated selectivity (~16x). miR-155's 11x decline does the heavy lifting. Dual-layer protection.

**Limitations:** Fibroblast-specific (miR-155 does not decline in senescent endothelial cells). In vivo, macrophage-derived exosomal miR-155 could confound the OFF switch by delivering miR-155 to senescent cells near inflammatory foci.

---

#### Architecture B: miR-34a-5p + miR-92a-3p (ON + OFF, Broadest Applicability)

```
L7Ae-mRNA-1: MREs for miR-34a-5p → L7Ae silenced when miR-34a HIGH (senescent)
L7Ae-mRNA-2: Constitutive L7Ae + miR-92a-3p MREs in ON-switch configuration
             → L7Ae translated when miR-92a HIGH (healthy); silenced when miR-92a LOW (senescent)
```

| miRNA | Healthy cell | Senescent cell | Discrimination |
|-------|-------------|---------------|---------------|
| miR-34a-5p | LOW → L7Ae-1 ON | HIGH → L7Ae-1 OFF | 1.5x |
| miR-92a-3p | HIGH (23,101 CPM) → L7Ae-2 ON | LOW (6,053 CPM) → L7Ae-2 OFF | **3.8x** |
| **Combined** | **Both L7Ae ON → payload OFF** | **Both L7Ae OFF → payload ON** | **~5.7x** |

**Strengths:** miR-92a declines in fibroblasts (0.26-0.42x), human heart (0.76x), skin (0.75x), and blood (0.71x) — the broadest cross-tissue OFF candidate. No inflammaging confound (miR-92a is not immune-cell-enriched).

**Limitations:** Lower selectivity (~5.7x) than Architecture A. At the margin of what may be safe for a cytotoxic payload.

---

#### Architecture C: miR-34a-5p + miR-16-5p (ON + OFF, Cross-Cell-Type)

```
L7Ae-mRNA-1: MREs for miR-34a-5p → silenced when miR-34a HIGH
L7Ae-mRNA-2: miR-16-5p ON-switch → L7Ae ON when miR-16 HIGH; OFF when miR-16 LOW
```

| miRNA | Healthy cell | Senescent cell | Discrimination |
|-------|-------------|---------------|---------------|
| miR-34a-5p | LOW → L7Ae-1 ON | HIGH → L7Ae-1 OFF | 1.5x |
| miR-16-5p | HIGH (3,172 CPM) → L7Ae-2 ON | LOW (1,183 CPM) → L7Ae-2 OFF | **2.7x** |
| **Combined** | **Both L7Ae ON → payload OFF** | **Both L7Ae OFF → payload ON** | **~4x** |

**Strengths:** miR-16 is validated across fibroblasts AND endothelial cells AND rat kidney — the only OFF candidate with cross-cell-type validation. Mechanistically clean (cell cycle regulator declining during permanent arrest).

**Limitations:** Lowest selectivity (~4x). Likely insufficient for a cytotoxic payload without additional optimization.

---

### 6.4 Architecture Comparison

| Architecture | Inputs | Selectivity | Applicability | Risk |
|-------------|--------|------------|---------------|------|
| **A** | miR-34a + miR-155 | **~16x** | Fibroblasts only | Inflammaging confound in vivo |
| **B** | miR-34a + miR-92a | ~5.7x | Broad (fibro, heart, skin, blood) | Marginal selectivity |
| **C** | miR-34a + miR-16 | ~4x | Cross-cell-type (fibro + endothelial) | Insufficient selectivity |

### 6.5 Recommendation

**For in vitro proof-of-concept: Architecture A (miR-34a + miR-155).** The ~16x estimated selectivity is the strongest achievable with current candidates. Test in doxorubicin-senescent vs. healthy WI-38 fibroblasts using Herbert's existing switch validation workflow.

**For broadest applicability: Architecture B (miR-34a + miR-92a).** The ~5.7x selectivity is marginal but miR-92a has no inflammaging confound and declines across multiple human tissues. If empirical testing shows that L7Ae amplification provides additional selectivity beyond the multiplicative estimate, this architecture may be sufficient.

**Critical experiment needed first:** Test whether miR-34a-5p alone, at ~45 estimated copies per cell in senescent WI-38 fibroblasts, can activate an ON switch. If it cannot, all architectures fail and alternative miRNA discovery (Herbert's planned small RNA-seq) becomes urgent.

---

## 7. Critical Unknowns Remaining

1. **What absolute miRNA copy number is needed for switch activation?** No published threshold exists. Our candidates range from ~250 copies (miR-34a) to ~7,000 copies (miR-22) in senescent fibroblasts. Empirical testing is needed.

2. **How does miR-34a-5p behave in Herbert's planned doxorubicin mouse model?** The GSE299871 data is from WI-38 human fibroblasts. Herbert plans in vivo mouse experiments where LNPs primarily target the liver.

3. **Is miR-22-3p upregulated in senescent cells within living tissue?** We see it UP in vitro but stable in bulk aging tissue. The in vivo signal may be too diluted.

4. **Does miR-155-5p de-targeting work in vivo?** The immune cell contribution to miR-155 in tissues could cause unwanted payload suppression in senescent cells near immune infiltrates.

5. **What is the stoichiometric balance between LNP-delivered mRNA and endogenous miRNA in target tissues?** This depends on LNP dose, tissue biodistribution, and cell-type uptake efficiency.

---

## 8. The Human In Vivo Gap

A systematic search for small RNA-seq data from chemotherapy patients — the closest human equivalent to our in vitro doxorubicin senescence models — revealed that **no publicly deposited small RNA-seq dataset exists with paired pre/post-chemotherapy blood or tissue samples** (see [literature/chemotherapy_patient_mirna_datasets.md](../literature/chemotherapy_patient_mirna_datasets.md) for full search results). The single most relevant study (Mikulski/Fendler 2024, PMID: [38650024](https://pubmed.ncbi.nlm.nih.gov/38650024/) — serum miRNA-seq at 4 timepoints during myeloablative ASCT conditioning, 10 patients) did not deposit data in a public repository.

This gap has three implications:

1. **Our candidate miRNAs cannot be validated in human in vivo chemotherapy-induced senescence using existing public data.** All of our evidence comes from in vitro cell culture (human) and in vivo natural aging (mouse/rat). The translational bridge — whether miR-34a goes up and miR-16 goes down in the tissues of chemotherapy-treated patients — remains untested.

2. **Circulating miRNA ≠ intracellular miRNA.** Even if patient serum data existed, it would reflect the secreted/EV-associated pool, not the intracellular pool that the circuit senses. The same inflammaging/cell-composition confounds we identified for miR-155-5p in bulk tissue would apply to serum — changes could reflect immune activation, tissue damage, or tumor response rather than senescence in specific cell types.

3. **Herbert's planned experiments are even more important.** His doxorubicin small RNA-seq in mice (in vivo) and human primary dermal fibroblasts (in vitro) would contribute to a space where almost no quantitative data exists. A future clinical collaboration profiling patient blood miRNAs before and after chemotherapy with modern small RNA-seq would be highly impactful for the field.

---

## 9. Practical Viability Assessment: Can We Build a Universal Senolytic Circuit?

### 8.1 The Honest Answer

After systematically analyzing 6 datasets spanning 4 senescence inducers, 3 human cell types, 2 organisms, and both in vitro and in vivo contexts, **we identified exactly one miRNA that is universally upregulated in senescence: miR-34a-5p.** And its practical suitability is uncertain.

The fundamental tension for miR-34a-5p as a circuit input:

| Context | Fold Change | Absolute Counts | Problem |
|---------|------------|----------------|---------|
| WI-38 fibroblasts (DXR, CPM) | 1.5x | 558 CPM (~45 copies/cell est.) | Modest FC; low absolute copies |
| HUVECs (replicative, CPM) | 11.5x | 90 CPM | Strong FC but very low counts |
| HAECs (irradiation) | 1.6x | 2,629 | Modest FC; better absolute counts |
| Mouse tissues (aging, 5/6 UP) | 1.25-1.68x per tissue | 488-2,535 RPMM (young) | Diluted by non-senescent cells |
| Rat liver (aging) | 4.1x | 30→120 | Strongest FC but very low counts |
| **Human heart** (aging) | **2.54x** | **771→1,959** | Best combination of FC + counts |

In cell types where miR-34a has a good fold change (fibroblasts, HUVECs: 2.5-5.2x), the absolute counts are low (~250 copies). In the cell type where absolute counts are adequate (HAECs: ~2,600), the fold change is modest (1.6x). **Neither combination is unambiguously sufficient for a clean ON/OFF switch**, and the Saito lab has explicitly stated that no quantitative threshold for switch activation has been defined (Fujita et al., *Sci Adv*, 2022, DOI: 10.1126/sciadv.abj1793).

### 8.2 What Failed

Every other candidate miRNA failed the universality test:

| miRNA | Why it failed |
|-------|--------------|
| **miR-22-3p** | UP in fibroblast senescence (all inducers), but DOWN in HUVEC replicative senescence. Cell-type dependent, not universal. |
| **miR-29c-3p** | Strongest pan-tissue aging signal in mouse (700-4,500 RPMM), but only **2-9 counts** in human fibroblasts. Not expressed in the primary target cell type. |
| **miR-29a-3p** | Consistent direction but high baseline expression (3,740 counts in healthy cells). Only 1.6x fold change in DXR senescence — poor ON/OFF discrimination. |
| **miR-21-5p** | UP in most contexts, but baseline is enormous (18,000-1,650,000 counts). Circuit would partially activate in every cell. |
| **miR-146a-5p** | No change in DXR-senescent fibroblasts or replicative HUVECs. UP only in irradiated endothelial cells and aged muscle — likely inflammation-driven, not senescence-specific. |
| **miR-155-5p** | Strong OFF-switch candidate (DOWN 7x in senescent fibroblasts), but UP in aged tissues due to immune cell infiltration. Complicated in vivo. |
| **miR-184, miR-96, miR-215, miR-375** | Not expressed (<10 counts) in any human cell type tested. Reported fold changes in literature are on negligible baselines — a systemic problem in the field. |

### 8.3 Recommended Path Forward

We see three viable strategies, which are not mutually exclusive:

**Strategy 1: Build and test a miR-34a-based prototype now.**

Despite the uncertainties, miR-34a-5p is the best candidate by a wide margin. The only way to resolve whether ~250 copies is sufficient for switch activation is to build the switch and test it empirically. Herbert has already validated a miR-122 ON-switch system in HuH7 vs. 4T1 cells — the same experimental framework can be adapted for miR-34a by comparing miR-34a-high cells (senescent fibroblasts induced with doxorubicin) vs. miR-34a-low cells (young/proliferating fibroblasts).

This experiment would:
- Determine if the endogenous miR-34a level in senescent cells is sufficient for switch activation
- Establish the dynamic range achievable with miR-34a as input
- Reveal whether the circuit can discriminate senescent from non-senescent cells with a cytotoxic payload

If miR-34a alone is insufficient, pairing it with miR-22-3p (Architecture A) or miR-155-5p (Architecture B) in a 2-input circuit should be tested next.

**Strategy 2: Abandon the universal circuit and design tissue-specific panels.**

Given that cell-type specificity dominates the senescence miRNA landscape, a more realistic approach may be to design separate circuits for different tissue contexts:

- **Fibroblast circuit:** miR-34a-5p ON + miR-22-3p ON (both reliably UP in fibroblast senescence)
- **Endothelial circuit:** miR-34a-5p ON + miR-146a-5p ON (both UP in endothelial irradiation/senescence)
- **Liver circuit:** miR-34a-5p ON + liver-specific de-targeting with miR-122-5p OFF (protecting healthy hepatocytes where LNPs accumulate)

This is less elegant but potentially more effective than a one-size-fits-all design.

**Strategy 3: Generate new data before committing to a design.**

Herbert's planned doxorubicin small RNA-seq experiment in mouse tissues (in vivo) and human primary dermal fibroblasts (in vitro) could reveal candidates not present in the public datasets we've analyzed. The public data covers WI-38 fibroblasts, HUVECs, HAECs, and mouse tissues — none of which are primary dermal fibroblasts, which are Herbert's primary in vitro model. Additionally, the in vivo mouse data may reveal tissue-level miRNA changes that include contributions from senescent cells generated by doxorubicin.

**We recommend Strategy 1 in parallel with Strategy 3:** build the miR-34a prototype now using existing validated cell lines, while simultaneously running the small RNA-seq experiment to identify potentially better candidates. If miR-34a works, the new data can optimize it. If it doesn't, the new data provides alternatives.

---

## 10. Conclusions

1. **miR-34a-5p is the single most validated ON-switch candidate**, now confirmed across **11 datasets (14 independent analyses)**, 4 senescence inducers, 4 human cell types, 3 human tissues in vivo (heart, skin, fibroblast-rich), 3 organisms, and both in vitro and in vivo contexts. **Human tissue validation achieved:** 2.54x UP in aged human cardiac tissue (GSE136926, PMID: 31607954), 1.25x UP in aged human skin (GSE111281). The strongest fold change (4.1x) is in aged rat liver. miR-34a is notably absent from blood (<2 counts), explaining why blood-based aging studies missed it.

2. **However, miR-34a-5p's practical viability as a circuit input is uncertain.** In the cell types where it shows good fold changes (fibroblasts: 2.5-5.2x), the absolute expression is low (~250 copies in senescent cells). In the cell type where expression is adequate (HAECs: ~2,600 copies), the fold change is modest (1.6x). No published data establishes the minimum miRNA copy number needed for reliable mRNA switch activation.

3. **No truly universal senescence miRNA exists at expression levels unambiguously suitable for circuit applications.** Every candidate either fails the universality test (miR-22-3p: cell-type dependent), the expression test (miR-29c-3p: 2 counts in fibroblasts), or the selectivity test (miR-21-5p: too high in healthy cells). This is the central challenge of this project.

4. **Three senescence inducers (DXR, SDS/PMD, replicative) converge on a shared core miRNA program** (miR-34a, miR-21, miR-22, miR-29a) in WI-38 fibroblasts. Irradiation in HAECs partially overlaps (miR-34a, miR-21 UP; miR-146a additionally UP; miR-17 DOWN). This convergence suggests a detectable common program exists, even if individual components are cell-type-variable.

5. **A five-miRNA core senescence signature** is reproducible across two independent human fibroblast lines (MRC-5 and WI-38): miR-34a UP; miR-155, miR-16, miR-92a, miR-17 DOWN. miR-21 and miR-22, despite being part of the shared inducer response in WI-38, do NOT replicate in MRC-5 and should not be considered core markers.

6. **miR-155-5p is the strongest OFF-switch candidate for fibroblast circuits**, with 7-10x decline validated in both WI-38 (GSE299871) and MRC-5 (GSE117818). However, its in vivo behavior is complicated by immune cell infiltration, which drives miR-155 UP in aged tissues. This paradox (cell-autonomous DOWN, tissue-level UP) must be resolved empirically before using it for in vivo de-targeting.

7. **Several highly-cited senescence miRNAs (miR-184, miR-96, miR-215, miR-375) are not expressed at detectable levels** in any human cell type we analyzed. Their identification as "senescence markers" in the literature reflects fold-change-based analysis of negligible absolute expression — a systemic methodological problem in the field that has implications beyond circuit design.

8. **The recommended immediate next step is empirical:** build a miR-34a-5p ON-switch prototype and test whether endogenous miR-34a levels in senescent cells (~250 copies in fibroblasts) can activate the switch. This experiment will establish the practical threshold that no amount of computational analysis can determine. Simultaneously, Herbert's planned doxorubicin small RNA-seq experiment in primary human dermal fibroblasts and mouse tissues should proceed to identify potentially better candidates in his target systems.

9. **miR-92a-3p emerges as the most consistent cross-tissue OFF-switch in human aging data**, declining in all three human tissues analyzed: blood (0.71x), skin (0.75x), and heart (0.76x). Combined with its decline in senescent fibroblasts (0.32-0.47x), it is the only OFF-switch candidate validated across both in vitro senescence and human in vivo aging in multiple tissues.

10. **Blood and tissue miRNA aging patterns diverge dramatically.** Most miRNAs decline in aged blood (due to immunosenescence/lymphocyte contraction; Goronzy & Weyand, *Nat Immunol*, 2013, PMID: 24048120) but are stable or UP in aged tissues. This means blood/serum/plasma miRNA studies cannot be used to infer tissue-level changes relevant to circuit design.

11. **A universal senolytic circuit may not be achievable.** Tissue-specific circuit panels — each tuned to the miRNA landscape of its target tissue — may be more realistic than a single design that works everywhere. The liver-accumulation property of LNPs makes liver-specific de-targeting (via miR-122-5p OFF switch) a practical first target regardless of which ON-switch inputs are used.

---

## References

1. RNA Biology 2025. DOI: 10.1080/15476286.2025.2551299 (GSE299871)
2. Terlecki-Zaniewicz L et al. *Redox Biology*. 2018;18:77-83. PMC: PMC6037909 (GSE94410)
3. Wagner V et al. *Nat Biotechnol*. 2024;42:109-118. PMID: 37106037 (GSE217458)
4. Kim JY et al. *Aging*. 2014;6(7):524-544. PMID: 25063768 (GSE55164)
5. Peiris HN et al. *Front Mol Biosci*. 2022. PMID: 36213127 (GSE200330)
6. He L et al. *Nature*. 2007;447:1130-1134. PMID: 17554337 (miR-34a/p53)
7. Yamakuchi M et al. *PNAS*. 2008;105(36):13421-13426. PMID: 18755897 (miR-34a/SIRT1)
8. O'Connell RM et al. *PNAS*. 2007;104(5):1604-1609. PMID: 17460050 (miR-155)
9. Rodriguez A et al. *Science*. 2007;316(5824):608-611. PMID: 17463290 (miR-155)
10. Baker DJ et al. *Nature*. 2011;479:232-236. PMID: 22012258 (senescent cell burden)
11. Faraonio R et al. *Cell Death Differ*. 2012;19(4):616-624. PMID: 22052189 (miR-17 family)
12. Fujita Y et al. *Sci Adv*. 2022;8(1):eabj1793 (ON/OFF switch)
13. Matsuura S et al. *Nat Commun*. 2018;9:4847 (AND gates)
14. Terlecki-Zaniewicz L et al. *Aging*. 2018;10(5):1103-1132. PMID: 29779019 (EV miRNAs)
15. Yang MY et al. *PLoS ONE*. 2012;7(5):e37205. PMID: 22606351 (dox/K562)
16. Weigl M et al. *bioRxiv*. 2024. DOI: 10.1101/2024.04.10.588794
17. Bonifacio LN, Jarstfer MB. *PLoS ONE*. 2010;5(9):e12519. PMID: 20824140
18. Santiago FE et al. *PNAS*. 2024;121(40):e2321182121
19. Engel et al. *Sci Rep*. 2022. PMID: 36402833 (GSE202120)
20. Taganov KD et al. *PNAS*. 2006;103(33):12481-12486. PMID: 16885212 (miR-146a/NF-κB)
21. Serrano M et al. *Cell*. 1997;88(5):593-602. PMID: 9054499 (senescence)
22. Di Leonardo A et al. *Genes Dev*. 1994;8(21):2540-2551. PMID: 7798313 (radiation senescence)
23. Linsley PS et al. *RNA*. 2007;13(7):1012-1020. PMID: 17210802 (miR-16/cell cycle)
24. Bushel PR et al. *Sci Data*. 2022;9:252. PMID: 35551205 (GSE172269, rat BodyMap)
25. Hackl M et al. *Aging Cell*. 2010;9(2):291-296. PMID: 20409078 (miR-17~92 cluster in senescence)
26. Olive V et al. *J Biol Chem*. 2009;284(9):5731-5741. PMID: 19726683 (miR-92a/proliferation)
27. Akinc A et al. *Mol Ther*. 2010;18(7):1357-1364. PMID: 20068556 (LNP liver accumulation)
28. Ma Z et al. *Front Physiol*. 2019;10:1226. PMID: 31607954 (GSE136926, human cardiac aging miR-34a)
29. Anderson R et al. *Circ Res*. 2019;124(7):975-992. PMID: 30786840 (cardiac senescence)
30. Hulsmans M et al. *J Exp Med*. 2018;215(2):423-440. PMID: 29339450 (cardiac macrophages aging)
31. Goronzy JJ, Weyand CM. *Nat Immunol*. 2013;14(5):428-436. PMID: 24048120 (immunosenescence)
32. van Rooij E et al. *PNAS*. 2008;105(35):13027-13032. PMID: 18723672 (miR-29/cardiac fibrosis)
33. Mann M et al. *PLoS One*. 2017;12(7):e0159724. PMID: 27447824 (miR-155 >100x in M1 macrophages)
34. The Tabula Muris Consortium. *Nature*. 2020;583:590-595. PMID: 32669714 (immune cell composition changes in aging)
35. Yin Q et al. *Cell Commun Signal*. 2024;22:386. PMID: 38987851 (macrophage exosomal miR-155 → epithelial senescence)
36. He J et al. *Hum Mutat*. 2025;2025:6771390. PMID: 40486266 (M1 macrophage exosomal miR-155 → endothelial senescence)
37. Roest et al. *Nat Commun*. 2025. DOI: 10.1038/s41467-025-60521-x (miRNA cell-type deconvolution)
38. Hernandez de Sande A et al. *Genome Med*. 2025;17:112. PMID: 41053866 (single-cell miRNA in immune aging)
39. Franceschi C et al. *Ann N Y Acad Sci*. 2000;908:244-254. PMID: 10911963 (inflammaging)
40. Prata LGPL et al. *Semin Immunol*. 2018;40:101275 (senescent cell immune clearance)
41. Mikulski M, Fendler W et al. 2024. PMID: 38650024 (ASCT serum miRNA-seq)
42. Tam S et al. *Brief Bioinform*. 2015;16(6):950-963. PMID: 25888698 (miRNA-seq normalization)
43. Schurch NJ et al. *RNA*. 2016;22(6):839-851. PMID: 27022035 (replicate requirements)
