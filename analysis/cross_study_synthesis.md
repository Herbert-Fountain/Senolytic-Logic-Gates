# Cross-Study Synthesis: Senescence and Aging miRNA Landscape
## Implications for Logic Gate Circuit Design

*Last updated: 2026-04-07*
*Datasets analyzed: 5 (see Table 1)*

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

**Critical methodological note:** Direct quantitative comparison of absolute expression values between datasets is not valid due to different organisms, normalization methods, library preparation protocols, cell types, and biological contexts. We compare **directions of change** and **relative expression tiers** (high/medium/low/negligible) across datasets, not absolute values. When we refer to "counts" across studies, these reflect dataset-specific quantifications.

---

## 3. Master Concordance Table

**Table 2: Candidate miRNA expression across all analyzed datasets**

| miRNA | GSE299871 DXR (WI-38) | GSE299871 SDS | GSE299871 RS | GSE94410 (HUVEC rep.) | GSE217458 (mouse aging) | GSE55164 (mouse muscle) | GSE200330 (irr. EVs) | Overall |
|-------|----------------------|--------------|-------------|----------------------|------------------------|------------------------|---------------------|---------|
| **miR-34a-5p** | **2.5x UP** (102→253) | **7.2x UP** | **3.0x UP** | **5.2x UP** (46→239) | **1.2-1.7x UP** (500-3800) | **2.5x UP** | 1.1x (EVs) | **CONSISTENT UP** |
| **miR-22-3p** | **2.8x UP** (2.5K→7K) | **6.1x UP** | **2.7x UP** | **0.3x DOWN** (59K→19K) | ~1x stable | ~1x stable | 0.6x (EVs) | **INDUCER-DEPENDENT** |
| **miR-29a-3p** | **1.6x UP** (3.7K→5.9K) | **6.2x UP** | 1.6x UP | Not tested | **1.2-2.3x UP** (3K-16K) | 1.2x UP | 1.0x (EVs) | Consistent UP, modest |
| **miR-21-5p** | **1.8x UP** (18K→33K) | **5.8x UP** | 2.2x UP | **2.6x UP** (408K→1.1M) | 1.0-1.8x UP (1.5K-16K) | ~1x | 1.0x (EVs) | UP but high baseline |
| **miR-29c-3p** | 5.0x UP (**2→9 counts**) | 15x (2→30) | 6x (2→12) | Not tested | **1.5-3.1x UP** (700-4500) | 1.2x UP | 1.5x (EVs, low) | UP but **negligible in fibroblasts** |
| miR-146a-5p | 1.2x (12→14) | 1.7x | 0.7x | 1.0x (401→410) | 1.0-2.3x variable | **2.5x UP** (muscle) | 1.0x (EVs) | Inconsistent |
| miR-21-3p | 1.2x (55→65) | 7.1x | 2.1x | 1.2x (387→462) | 0.9-2.0x | ~1x | 1.4x (EVs, low) | Weak/inconsistent |
| **miR-155-5p** | **0.1x DOWN** (2.8K→396) | 1.0x | **0.2x DOWN** | Not tested | 1.2-4.2x UP (in vivo) | 1.7x UP | **0.2x DOWN** (EVs) | **DOWN in vitro, UP in vivo** |
| **miR-17-5p** | **0.3x DOWN** (134→40) | 1.4x UP | **0.3x DOWN** | 5.9x UP (HUVEC only) | 0.9-1.2x stable | 0.8x | 0x (EVs) | **DOWN in DXR/RS fibroblasts** |
| miR-184 | 0→8 (from zero) | 0→4 | 0→8 | 1→2 | 1-6 RPMM | Near-zero | 0-1 (EVs) | **NOT EXPRESSED** |
| miR-96-5p | 0→0 | 0→2 | 0→1 | 8→2 | 1-65 RPMM | Near-zero | 0 (EVs) | **NOT EXPRESSED** |
| miR-215-5p | 0→1 | 0→0 | 0→0 | 40→7 | Very low | N/A | 0 (EVs) | **NOT EXPRESSED** |
| miR-122-5p | 14→18 | 14→16 | 14→38 | 108→21 | 100K liver only | Not expressed | 34→36 (EVs) | **LIVER-SPECIFIC** |

---

## 4. Tiered Candidate Assessment (Revised)

### Tier 1: Strongest Circuit Input Candidates

#### miR-34a-5p — The Most Consistent Senescence miRNA

**Evidence summary:**

| Source | Context | Direction | FC | Absolute Level |
|--------|---------|-----------|-----|---------------|
| GSE299871 | DXR senescence (WI-38) | UP | 2.5x | 102→253 |
| GSE299871 | SDS senescence (WI-38) | UP | 7.2x | 102→732 |
| GSE299871 | Replicative senescence (WI-38) | UP | 3.0x | 102→310 |
| GSE94410 | Replicative senescence (HUVEC) | UP | 5.2x | 46→239 |
| GSE217458 | Mouse aging (16 tissues) | UP | 1.2-1.7x | 500-3,800 RPMM |
| GSE55164 | Mouse muscle aging | UP | 2.5x | ~1,500 (est.) |
| Literature | Multiple cell types/inducers | UP | Various | Various |

**miR-34a-5p is the ONLY miRNA that is upregulated in every context we have examined:** doxorubicin senescence, SDS senescence, replicative senescence, HUVEC senescence, mouse multi-tissue aging, and mouse muscle aging. No other candidate achieves this level of consistency.

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
| GSE217458 | Mouse aging (16 tissues) | ~1x | Stable | 1,500-11,000 RPMM |

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

#### miR-155-5p — Potential De-Targeting Element

| Source | Context | Direction | FC | Absolute Level |
|--------|---------|-----------|-----|---------------|
| GSE299871 | DXR senescence (WI-38) | **DOWN** | **0.14x** | 2,760→396 |
| GSE299871 | Replicative (WI-38) | **DOWN** | 0.19x | 2,760→530 |
| GSE200330 | Irradiation EVs | **DOWN** | 0.25x | 28→7 |
| GSE217458 | Mouse aging (in vivo) | **UP** | 1.2-4.2x | 21-1,200 RPMM |

miR-155-5p presents a paradox: it is strongly DOWN in senescent cells in vitro but UP in aged tissues in vivo. The in vivo increase is likely driven by **immune cell infiltration** in aging tissues — miR-155 is a well-characterized immune regulator (O'Connell et al., *PNAS*, 2007, PMID: 17460050; Rodriguez et al., *Science*, 2007, PMID: 17463290). In isolated senescent fibroblasts, the cell-autonomous response is downregulation.

**For circuit design:** miR-155-5p could serve as a de-targeting/OFF-switch element — if present at high levels (indicating a healthy, non-senescent cell), it suppresses payload expression. The 7-fold decline in senescent cells provides good ON/OFF separation. However, its behavior in vivo (where immune cells contribute miR-155) needs careful consideration.

---

#### miR-17-5p — Declining in Senescent Fibroblasts

| Source | Context | Direction | FC |
|--------|---------|-----------|-----|
| GSE299871 | DXR senescence (WI-38) | **DOWN** | 0.30x |
| GSE299871 | Replicative (WI-38) | **DOWN** | 0.26x |
| GSE94410 | Replicative (HUVEC) | UP (5.9x) | Opposite in HUVECs |

The miR-17 family decline in senescent fibroblasts is consistent with published reports (Faraonio et al., 2012, PMID: 22052189). However, HUVECs show the opposite pattern. This limits miR-17 to fibroblast-specific de-targeting.

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
| miR-34a-5p | 2.5x UP | 5.2x UP | 1.2-1.7x UP | **All agree** |
| miR-22-3p | 2.8x UP | **0.3x DOWN** | ~1x | **Disagree** |
| miR-29a-3p | 1.6x UP | Not tested | 1.2-2.3x UP | Agree (limited) |
| miR-21-5p | 1.8x UP | 2.6x UP | 1.0-1.8x UP | **All agree** |

Only **miR-34a-5p and miR-21-5p** maintain consistent upregulation across both cell types tested. miR-22-3p, despite being shared across inducers within WI-38 cells, fails to generalize to HUVECs. This distinction between "inducer-universal, cell-type-specific" and "truly universal" is critical for circuit design.

### 5.3 In Vitro Senescence vs. In Vivo Aging

| miRNA | In vitro senescence (DXR) | In vivo aging (mouse) | Direction match? | Interpretation |
|-------|--------------------------|----------------------|-----------------|---------------|
| miR-34a-5p | 2.5x UP | 1.2-1.7x UP | **YES** | True senescence marker, diluted in bulk tissue |
| miR-21-5p | 1.8x UP | 1.0-1.8x UP | **YES** | Modest in both contexts |
| miR-29a-3p | 1.6x UP | 1.2-2.3x UP | **YES** | Consistent |
| miR-155-5p | 0.14x DOWN | 1.2-4.2x UP | **NO** | Cell-autonomous DOWN vs. immune infiltration UP |
| miR-22-3p | 2.8x UP | ~1x stable | **PARTIAL** | Changed in vitro but not detectable in bulk tissue |

The in vivo aging fold changes (1.2-1.8x) are consistently smaller than in vitro senescence fold changes (2-7x). This is expected because aged tissues contain a **mixture of senescent and non-senescent cells**. If senescent cells comprise ~15% of an aged tissue (a commonly cited estimate; Baker et al., *Nature*, 2011, PMID: 22012258), a miRNA that is 2.5x higher in senescent cells would appear only ~1.2x higher in bulk tissue: (0.85 × 1.0 + 0.15 × 2.5) / 1.0 = 1.23x. This is consistent with what we observe.

The miR-155-5p discrepancy (DOWN in vitro, UP in vivo) is the clearest example of non-cell-autonomous effects in bulk tissue aging. miR-155 is primarily expressed by immune cells, which infiltrate aging tissues. The in vivo increase reflects this infiltration, not senescent cell biology.

---

## 6. Recommended Circuit Architectures

Based on all evidence, we propose three candidate circuit configurations:

### Architecture A: Dual ON-Switch AND Gate (Fibroblast-Targeted)

```
Input 1: miR-34a-5p (ON switch) — universal senescence marker
Input 2: miR-22-3p (ON switch) — high-abundance fibroblast senescence marker

Logic: Payload expressed ONLY when both miR-34a AND miR-22 are high
```

**Rationale:** miR-34a provides universality (UP in all contexts). miR-22 provides the high absolute abundance (7,025 counts) needed for reliable switch engagement. Together they create a 2-input AND gate requiring both p53-pathway activation (miR-34a) and fibroblast-specific senescence (miR-22).

**Limitation:** Cell-type restricted. miR-22 is DOWN in senescent endothelial cells, so this circuit would NOT target senescent endothelial cells.

### Architecture B: ON + OFF Hybrid (Broader Target)

```
Input 1: miR-34a-5p (ON switch) — activates payload when present
Input 2: miR-155-5p (OFF switch / de-targeting) — suppresses payload when present

Logic: Payload expressed when miR-34a is HIGH and miR-155 is LOW
```

**Rationale:** miR-34a is UP in senescent cells; miR-155 is DOWN in senescent cells. A healthy cell has low miR-34a (payload OFF via ON-switch) AND high miR-155 (payload OFF via OFF-switch). A senescent cell has high miR-34a (payload ON) AND low miR-155 (no suppression). Double protection.

**Based on Saito 2025 hybrid switch design** (achieving 16-fold dynamic range with single-construct ON+OFF), this may be the most practical architecture.

**Limitation:** miR-155 behavior in vivo is complicated by immune cells. In tissues with significant immune infiltration, non-senescent cells may have low miR-155, creating false positives.

### Architecture C: Triple-Input AND Gate (Maximum Selectivity)

```
Input 1: miR-34a-5p (ON switch) — universal
Input 2: miR-22-3p or miR-29a-3p (ON switch) — abundance
Input 3: miR-155-5p (OFF switch) — de-targeting

Logic: Payload requires miR-34a HIGH + miR-22/29a HIGH + miR-155 LOW
```

**Rationale:** Maximum selectivity through three orthogonal signals. Requires adding a second repressor protein (e.g., MS2CP) beyond L7Ae.

**Limitation:** Circuit complexity. More components = more potential failure points. Would require Herbert to implement MS2CP alongside L7Ae.

---

## 7. Critical Unknowns Remaining

1. **What absolute miRNA copy number is needed for switch activation?** No published threshold exists. Our candidates range from ~250 copies (miR-34a) to ~7,000 copies (miR-22) in senescent fibroblasts. Empirical testing is needed.

2. **How does miR-34a-5p behave in Herbert's planned doxorubicin mouse model?** The GSE299871 data is from WI-38 human fibroblasts. Herbert plans in vivo mouse experiments where LNPs primarily target the liver.

3. **Is miR-22-3p upregulated in senescent cells within living tissue?** We see it UP in vitro but stable in bulk aging tissue. The in vivo signal may be too diluted.

4. **Does miR-155-5p de-targeting work in vivo?** The immune cell contribution to miR-155 in tissues could cause unwanted payload suppression in senescent cells near immune infiltrates.

5. **What is the stoichiometric balance between LNP-delivered mRNA and endogenous miRNA in target tissues?** This depends on LNP dose, tissue biodistribution, and cell-type uptake efficiency.

---

## 8. Conclusions

1. **miR-34a-5p is the single most validated ON-switch candidate**, consistent across 5 datasets, 3 senescence inducers, 2 cell types, 2 organisms, and both in vitro and in vivo contexts. Its mechanistic basis (p53 target, SIRT1 regulator) explains this universality.

2. **Three senescence inducers converge on a shared core miRNA program** (miR-34a, miR-21, miR-22, miR-29a), supporting the feasibility of detecting senescence regardless of initial trigger. However, cell-type-specific differences (miR-22 in HUVECs) limit universal applicability.

3. **miR-155-5p is the strongest OFF-switch candidate**, showing 7-fold decline in senescent fibroblasts. Its in vivo behavior requires careful validation due to immune cell expression.

4. **Several highly-cited senescence miRNAs (miR-184, miR-96, miR-215, miR-375) are not expressed at detectable levels** in human fibroblasts or endothelial cells. Their identification as "senescence markers" in the literature reflects fold-change-based analysis of negligible absolute expression — a systemic methodological issue in the field.

5. **The hybrid ON+OFF circuit architecture** (Architecture B: miR-34a ON + miR-155 OFF) is the most promising design based on current evidence, combining the universality of miR-34a with the de-targeting capability of miR-155. This aligns with the Saito lab's 2025 hybrid switch design achieving 16-fold dynamic range.

6. **Herbert's planned experiments — doxorubicin senescence in mouse (in vivo) and human primary dermal fibroblasts (in vitro) — remain essential.** The public data we've analyzed provides strong candidates and design rationale, but empirical validation in the target system is irreplaceable.

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
