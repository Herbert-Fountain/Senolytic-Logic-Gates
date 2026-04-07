# Cross-Study Synthesis: Senescence and Aging miRNA Landscape
## Implications for Logic Gate Circuit Design

*Last updated: 2026-04-06*
*Datasets analyzed: GSE94410 (HUVEC senescence), GSE217458 (mouse aging 16 tissues)*
*Additional datasets pending: GSE27404 (IMR90 senescence), human senescence datasets*

---

## 1. Overview

This document synthesizes findings across multiple datasets and the published literature to assess the feasibility of identifying miRNA inputs for senolytic logic gate circuits. We evaluate each candidate miRNA based on four criteria essential for circuit function:

1. **Absolute expression level** — sufficient intracellular copies to engage synthetic mRNA switches
2. **Differential expression** — higher in senescent/aged cells than in healthy/young cells
3. **Consistency** — reproducible across cell types, tissues, and experimental contexts
4. **Conservation** — expressed in both mouse and human for translational path

## 2. Data Sources Analyzed

| Dataset | Context | Cell/Tissue | Inducer | Organism | Data Type |
|---------|---------|------------|---------|----------|-----------|
| GSE94410 | In vitro senescence | HUVECs | Replicative | Human | Raw counts |
| GSE217458 | In vivo natural aging | 16 tissues | Natural | Mouse | RPMM |
| Literature | Various | Multiple | Various | Multiple | Fold changes (mostly) |

**Critical methodological note:** Direct quantitative comparison between GSE94410 (human HUVEC raw counts) and GSE217458 (mouse tissue RPMM) is not statistically valid due to different organisms, normalization methods, library preparation protocols, and biological contexts. We compare **directions of change** and **relative expression levels** (high/medium/low/negligible) across datasets, not absolute values.

## 3. Consolidated Candidate Assessment

### Tier 1: Strongest Candidates (supported by multiple lines of evidence)

#### miR-29c-3p / miR-29a-3p (miR-29 family)

| Evidence | Source | Finding |
|----------|--------|---------|
| Natural aging | GSE217458 (Wagner 2024) | UP 1.5-3.1x across ALL 16 mouse tissues; strongest pan-tissue aging correlation |
| Rejuvenation | Wagner 2024 | Restored to young levels by heterochronic parabiosis |
| Absolute expression | GSE217458 | HIGH (700-16,000 RPMM depending on tissue) |
| In vitro senescence | Not prominently reported | Gap in knowledge |
| Functional targets | Wagner 2024 | ECM and secretion pathways (consistent with SASP) |
| Conservation | miRBase | miR-29c-3p: 100% identical between mmu and hsa |
| Circuit viability | Assessment | HIGH — abundant, consistent, conserved |

**Strengths:** Most consistent aging signal across all tissues. High absolute expression sufficient for switch engagement. Reversed by rejuvenation, suggesting true aging/senescence biology rather than developmental artifact. 100% conserved with human ortholog.

**Weaknesses:** Not confirmed in pure senescent cell populations (in vitro data lacking). Already moderately expressed in young tissue (700-6,000 RPMM), so ON/OFF ratio may be limited. The in vivo signal could be driven by cell composition changes (e.g., fibrosis) rather than cell-autonomous senescence.

**What would resolve this:** Testing miR-29c-3p expression in Herbert's planned doxorubicin-induced senescent vs. non-senescent cells in vitro.

---

#### miR-34a-5p

| Evidence | Source | Finding |
|----------|--------|---------|
| In vitro senescence (HUVEC) | GSE94410 | UP 5.2x (46→239 counts) |
| Natural aging (mouse) | GSE217458 | UP 1.2-1.7x across 6 tissues (500-3,800 RPMM) |
| Literature | Multiple studies | Established senescence marker; targets SIRT1 (Terlecki-Zaniewicz 2018, Faraonio 2012, reviews) |
| Conservation | miRBase | 100% identical mmu↔hsa |
| Circuit viability | Assessment | MODERATE — consistent direction but moderate absolute levels in HUVEC data |

**Strengths:** Most consistently reported senescence miRNA in the literature across multiple cell types and inducers. Confirmed UP in both our in vitro (GSE94410) and in vivo (GSE217458) analyses. Well-characterized mechanistically (SIRT1 targeting). 100% conserved.

**Weaknesses:** Absolute counts in senescent HUVECs are low (239 raw counts). The in vivo fold change is modest (1.2-1.7x). Functional significance of the reported fold changes for circuit applications is unclear — 239 copies may or may not be enough for reliable switch activation.

---

#### miR-21a-5p (hsa-miR-21-5p)

| Evidence | Source | Finding |
|----------|--------|---------|
| In vitro senescence (HUVEC) | GSE94410 | UP 2.6x (407,800→1,070,778 counts) |
| Natural aging (mouse) | GSE217458 | UP 1.0-1.8x (1,500-16,000 RPMM) |
| Intracellular retention | Terlecki-Zaniewicz 2019 | miR-21-3p (not -5p) selectively retained intracellularly in senescent cells |
| Conservation | miRBase | 100% identical mmu↔hsa |
| Circuit viability | Assessment | HIGH abundance but LOW selectivity — already very high in young/healthy cells |

**Strengths:** Extremely abundant (highest expressed miRNA in most cells). Would provide the most reliable switch engagement from a stoichiometric perspective.

**Weaknesses:** The high baseline expression (407,800 in young HUVECs) means the circuit would partially activate in healthy cells. The 2.6x fold change, while statistically significant, provides poor ON/OFF selectivity for a kill switch.

**Note on miR-21-3p vs. -5p:** The -3p strand was reported as selectively retained intracellularly in senescent cells (Terlecki-Zaniewicz et al., *Aging*, 2018, PMID: 29779019). However, in GSE94410 it shows only 1.2x change (387→462 counts), and in GSE217458 it has low expression (3-72 RPMM). The intracellular retention finding is from a different study using SIPS, not replicative senescence, and may not generalize.

---

### Tier 2: Promising but Insufficient Evidence

#### miR-155-5p

| Evidence | Source | Finding |
|----------|--------|---------|
| Natural aging (mouse) | GSE217458 | UP 1.2-4.2x; largest in liver (21→89) and lung (122→457) |
| Pan-tissue aging marker | Wagner 2024 | One of 8 broadly deregulated miRNAs |
| Known function | O'Connell et al. 2007 (PMID: 17460050) | Inflammatory signaling regulator |
| In vitro senescence | Not tested in our analyses | Gap |
| Conservation | miRBase | 100% identical mmu↔hsa |

**Assessment:** Tissue-variable expression. The large fold changes in liver and lung are interesting for tissue-specific circuit applications but the low absolute levels (21 RPMM in young liver) may limit utility. Needs in vitro validation.

---

#### miR-146a-5p

| Evidence | Source | Finding |
|----------|--------|---------|
| In vitro senescence (HUVEC) | GSE94410 | NO CHANGE (401→410 counts) |
| Natural aging (mouse) | GSE217458 | UP 1.0-2.3x (variable by tissue; best in kidney 2.3x) |
| Literature | Bonifacio 2010 (PMID: 20824140) | Regulates SASP via IRAK1 (IL-6, IL-8 axis) |
| Conservation | miRBase | 100% identical mmu↔hsa |

**Assessment:** Established SASP regulator mechanistically, but inconsistent expression changes across our two datasets. The lack of change in senescent HUVECs despite being reported as a senescence marker elsewhere underscores the cell-type specificity problem.

---

### Tier 3: Unlikely Candidates (insufficient expression or inconsistent)

#### miR-184-3p

| Evidence | Source | Finding |
|----------|--------|---------|
| Pan-tissue aging marker | Wagner 2024 | One of 8 broadly deregulated miRNAs (UP) |
| Natural aging (mouse) | GSE217458 | UP 1.1-2.7x but expression is **1-6 RPMM** |
| In vitro senescence (HUVEC) | GSE94410 | **1-2 raw counts** — essentially not expressed |
| Doxorubicin senescence | Weigl 2024 (preprint) | Reported UP across 5 cell types |

**Assessment:** **Not viable for circuit applications.** Despite being identified as a pan-tissue aging marker, the absolute expression is negligible in both our datasets. This exemplifies the biomarker-vs-circuit disconnect: a statistically significant change at very low abundance is informative as a biomarker but useless as a switch input.

---

#### miR-22-3p, miR-96-5p, miR-375, miR-215-5p

These candidates showed either opposite-direction changes from literature reports, negligible expression, or both. See individual dataset analyses for details.

---

## 4. Key Cross-Study Observations

### 4.1 Cell-Type and Context Specificity is the Dominant Challenge

Across our analyses, the most consistent finding is **inconsistency**. The same miRNA can be upregulated in one cell type, downregulated in another, and unchanged in a third. This is supported by:

- Our GSE94410 analysis: only 25% concordance with literature reports
- Weigl/Grillari 2024 (preprint): most senescence miRNAs are cell-type specific
- Wagner 2024: molecular aging trajectories are largely tissue-specific

**Implication for circuit design:** A universal senolytic circuit using a single miRNA input is unlikely to work across all tissue types. Either:
1. Use multiple inputs (AND gate) to increase specificity
2. Design tissue-specific circuit panels
3. Identify the rare miRNAs that ARE consistent (miR-29 family, miR-34a are the best candidates)

### 4.2 Fold Change ≠ Circuit Utility

Multiple miRNAs with dramatic fold changes in the literature turned out to have negligible absolute expression in our quantitative analyses (miR-184, miR-96-5p, miR-375). This is a systemic problem in the senescence miRNA field: most studies report only fold changes without absolute levels, making it impossible to assess circuit viability from published data alone.

**Implication:** All future analyses in this project must prioritize absolute expression levels alongside fold changes. The minimum threshold for circuit viability is unknown (Saito lab has not defined one), but our working assumption is that miRNAs below ~100 RPMM (or equivalent) are too low for reliable switch engagement.

### 4.3 The miR-29 Family Deserves Priority Investigation

The miR-29 family (miR-29a-3p, miR-29c-3p) was not a prominent candidate in the classical senescence literature but emerged as the strongest signal from our quantitative analysis of the Wagner aging dataset:

- Most consistent cross-tissue aging signal
- Highest absolute expression among consistently upregulated candidates
- Reversed by rejuvenation
- 100% human conservation
- Known ECM/secretion pathway targets (SASP-relevant)

**Gap:** No published data on miR-29 family expression in pure senescent cell populations. This is the single most important question to address in Herbert's planned experiment.

### 4.4 In Vivo vs. In Vitro Signal Differences

In vivo aging shows more modest fold changes (1.2-3x) than in vitro senescence (2-10x). This is expected due to dilution of senescent cells within bulk tissue. However, the directions of change are partially concordant for some miRNAs (miR-34a, miR-21) and discordant for others (miR-22, miR-17). The discordant cases likely reflect genuine differences between replicative senescence and natural aging, or between HUVECs and mouse tissues, or both.

## 5. Current Assessment: Feasibility of Senolytic Circuit Design

### What We Know
1. No single miRNA provides a clean ON/OFF signal for senescence across cell types
2. Several miRNAs (miR-29c, miR-34a, miR-21) show consistent upward trends with sufficient absolute expression
3. The hybrid ON+OFF circuit architecture (Saito 2025) achieving 16-fold dynamic range may compensate for imperfect individual switch performance

### What We Don't Know (Critical Gaps)
1. **Whether miR-29 family is upregulated in chemotherapy-induced senescent cells** — the single most important unanswered question
2. **What absolute expression threshold is needed for reliable switch activation** — Saito lab has not defined this
3. **Whether combining 2-3 modestly selective miRNAs in an AND gate provides sufficient overall selectivity** — needs computational modeling and experimental validation
4. **How LNP delivery dose interacts with miRNA abundance** — stoichiometric balance is critical but tissue-dependent

### Recommended Next Steps
1. Generate doxorubicin-induced senescence small RNA-seq data (Herbert's planned experiment)
2. Specifically measure miR-29 family alongside classical candidates
3. Build the circuit design tool to evaluate candidate combinations computationally
4. Consider whether tissue-specific circuit panels are more realistic than a universal design

---

## References

1. Wagner V et al. *Nat Biotechnol*. 2024;42:109-118. DOI: 10.1038/s41587-023-01751-6
2. Terlecki-Zaniewicz L et al. *Redox Biology*. 2018;18:77-83. PMC: PMC6037909
3. Terlecki-Zaniewicz L et al. *Aging*. 2018;10(5):1103-1132. PMID: 29779019
4. Weigl M et al. *bioRxiv*. 2024. DOI: 10.1101/2024.04.10.588794
5. Yang MY et al. *PLoS ONE*. 2012;7(5):e37205. PMID: 22606351
6. Faraonio R et al. *Cell Death Differ*. 2012;19(4):616-624. PMID: 22052189
7. Bonifacio LN, Jarstfer MB. *PLoS ONE*. 2010;5(9):e12519. PMID: 20824140
8. Santiago FE et al. *PNAS*. 2024;121(40):e2321182121
9. Fujita Y et al. *Sci Adv*. 2022;8(1):eabj1793. DOI: 10.1126/sciadv.abj1793
10. O'Connell RM et al. *PNAS*. 2007;104(5):1604-1609. PMID: 17460050
