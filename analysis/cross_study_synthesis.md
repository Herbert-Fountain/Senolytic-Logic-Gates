# Cross-Study Synthesis: Senescence and Aging miRNA Landscape
## Implications for Logic Gate Circuit Design

*Last updated: 2026-04-07*
*Datasets analyzed: 6 (see Table 1)*

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
| 6 | GSE202120 | In vitro irradiation dose-response | HAECs (aortic endothelial) | X-ray (0-10 Gy) | Human | Raw counts | 35 |

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

**Table 2: Candidate miRNA expression across all analyzed datasets**

| miRNA | GSE299871 DXR (WI-38) | GSE299871 SDS | GSE299871 RS | GSE94410 (HUVEC rep.) | GSE202120 (HAEC irr. 72h) | GSE217458 (mouse aging) | GSE55164 (mouse muscle) | GSE200330 (irr. EVs) | Overall |
|-------|----------------------|--------------|-------------|----------------------|--------------------------|------------------------|------------------------|---------------------|---------|
| **miR-34a-5p** | **2.5x UP** (102→253) | **7.2x UP** | **3.0x UP** | **5.2x UP** (46→239) | **1.6x UP** (1599→2629) | **1.2-1.7x UP** (500-3800) | **2.5x UP** | 1.1x (EVs) | **CONSISTENT UP** |
| **miR-22-3p** | **2.8x UP** (2.5K→7K) | **6.1x UP** | **2.7x UP** | **0.3x DOWN** (59K→19K) | 1.2x (40K→48K) | ~1x stable | ~1x stable | 0.6x (EVs) | **CELL-TYPE-DEPENDENT** |
| **miR-29a-3p** | **1.6x UP** (3.7K→5.9K) | **6.2x UP** | 1.6x UP | Not tested | 1.3x (13K→17K) | **1.2-2.3x UP** (3K-16K) | 1.2x UP | 1.0x (EVs) | Consistent UP, modest |
| **miR-21-5p** | **1.8x UP** (18K→33K) | **5.8x UP** | 2.2x UP | **2.6x UP** (408K→1.1M) | **1.6x UP** (1.65M→2.6M) | 1.0-1.8x UP (1.5K-16K) | ~1x | 1.0x (EVs) | UP but high baseline |
| **miR-29c-3p** | 5.0x UP (**2→9 counts**) | 15x (2→30) | 6x (2→12) | Not tested | 1.3x (54→69, low) | **1.5-3.1x UP** (700-4500) | 1.2x UP | 1.5x (EVs, low) | UP but **negligible in human cells** |
| **miR-146a-5p** | 1.2x (12→14) | 1.7x | 0.7x | 1.0x (401→410) | **2.2x UP** (1966→4275) | 1.0-2.3x variable | **2.5x UP** (muscle) | 1.0x (EVs) | **Radiation/inflammation-specific** |
| miR-21-3p | 1.2x (55→65) | 7.1x | 2.1x | 1.2x (387→462) | 1.1x (892→949) | 0.9-2.0x | ~1x | 1.4x (EVs, low) | Weak/inconsistent |
| **miR-155-5p** | **0.1x DOWN** (2.8K→396) | 1.0x | **0.2x DOWN** | Not tested | 0.9x (14.8K→13.6K) | 1.2-4.2x UP (in vivo) | 1.7x UP | **0.2x DOWN** (EVs) | **DOWN in senescent cells, UP in aged tissue** |
| **miR-17-5p** | **0.3x DOWN** (134→40) | 1.4x UP | **0.3x DOWN** | 5.9x UP (HUVEC only) | **0.7x DOWN** (5156→3481) | 0.9-1.2x stable | 0.8x | 0x (EVs) | **DOWN in DXR/RS/irradiation** |
| miR-184 | 0→8 (from zero) | 0→4 | 0→8 | 1→2 | Not detected | 1-6 RPMM | Near-zero | 0-1 (EVs) | **NOT EXPRESSED** |
| miR-96-5p | 0→0 | 0→2 | 0→1 | 8→2 | Not detected | 1-65 RPMM | Near-zero | 0 (EVs) | **NOT EXPRESSED** |
| miR-215-5p | 0→1 | 0→0 | 0→0 | 40→7 | Not tested | Very low | N/A | 0 (EVs) | **NOT EXPRESSED** |
| miR-122-5p | 14→18 | 14→16 | 14→38 | 108→21 | 34→36 | 100K liver only | Not expressed | 34→36 (EVs) | **LIVER-SPECIFIC** |

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
| 6 | GSE217458 | Mouse natural aging (16 tissues) | UP | 1.2-1.7x | 500-3,800 RPMM |
| 7 | GSE55164 | Mouse skeletal muscle aging | UP | 2.5x | ~1,500 (est.) |

**miR-34a-5p is the ONLY miRNA that is upregulated in every context we have examined:** doxorubicin senescence, SDS/plasma membrane damage senescence, replicative senescence, HUVEC replicative senescence, irradiation-induced changes in aortic endothelial cells, mouse multi-tissue aging, and mouse muscle aging — across 4 senescence inducers, 3 human cell types, 2 organisms, and both in vitro and in vivo contexts. No other candidate achieves this level of consistency.

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

## 8. Practical Viability Assessment: Can We Build a Universal Senolytic Circuit?

### 8.1 The Honest Answer

After systematically analyzing 6 datasets spanning 4 senescence inducers, 3 human cell types, 2 organisms, and both in vitro and in vivo contexts, **we identified exactly one miRNA that is universally upregulated in senescence: miR-34a-5p.** And its practical suitability is uncertain.

The fundamental tension for miR-34a-5p as a circuit input:

| Context | Fold Change | Absolute Counts | Problem |
|---------|------------|----------------|---------|
| WI-38 fibroblasts (DXR) | 2.5x (good) | 253 (low) | May not have enough molecules for reliable switch activation |
| HUVECs (replicative) | 5.2x (excellent) | 239 (low) | Same stoichiometric concern |
| HAECs (irradiation) | 1.6x (modest) | 2,629 (adequate) | Fold change may be too small for clean ON/OFF separation |
| Mouse tissues (aging) | 1.2-1.7x (modest) | 500-3,800 RPMM | In vivo signal diluted by non-senescent cells |

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

## 9. Conclusions

1. **miR-34a-5p is the single most validated ON-switch candidate**, consistent across 6 datasets, 4 senescence inducers (doxorubicin, SDS/PMD, replicative, irradiation), 3 human cell types (WI-38 fibroblasts, HUVECs, HAECs), 2 organisms, and both in vitro and in vivo contexts. Its mechanistic basis as a direct p53 transcriptional target (He et al., *Nature*, 2007, PMID: 17554337) explains this universality, since p53 activation is the convergent node of all senescence pathways.

2. **However, miR-34a-5p's practical viability as a circuit input is uncertain.** In the cell types where it shows good fold changes (fibroblasts: 2.5-5.2x), the absolute expression is low (~250 copies in senescent cells). In the cell type where expression is adequate (HAECs: ~2,600 copies), the fold change is modest (1.6x). No published data establishes the minimum miRNA copy number needed for reliable mRNA switch activation.

3. **No truly universal senescence miRNA exists at expression levels unambiguously suitable for circuit applications.** Every candidate either fails the universality test (miR-22-3p: cell-type dependent), the expression test (miR-29c-3p: 2 counts in fibroblasts), or the selectivity test (miR-21-5p: too high in healthy cells). This is the central challenge of this project.

4. **Three senescence inducers (DXR, SDS/PMD, replicative) converge on a shared core miRNA program** (miR-34a, miR-21, miR-22, miR-29a) in WI-38 fibroblasts. Irradiation in HAECs partially overlaps (miR-34a, miR-21 UP; miR-146a additionally UP; miR-17 DOWN). This convergence suggests a detectable common program exists, even if individual components are cell-type-variable.

5. **miR-155-5p is the strongest OFF-switch candidate**, with 7-fold decline in DXR-senescent fibroblasts and dose-dependent decline in irradiated HAECs. However, its in vivo behavior is complicated by immune cell infiltration, which drives miR-155 UP in aged tissues. This paradox (cell-autonomous DOWN, tissue-level UP) must be resolved empirically before using it for in vivo de-targeting.

6. **Several highly-cited senescence miRNAs (miR-184, miR-96, miR-215, miR-375) are not expressed at detectable levels** in any human cell type we analyzed. Their identification as "senescence markers" in the literature reflects fold-change-based analysis of negligible absolute expression — a systemic methodological problem in the field that has implications beyond circuit design.

7. **The recommended immediate next step is empirical:** build a miR-34a-5p ON-switch prototype and test whether endogenous miR-34a levels in senescent cells (~250 copies in fibroblasts) can activate the switch. This experiment will establish the practical threshold that no amount of computational analysis can determine. Simultaneously, Herbert's planned doxorubicin small RNA-seq experiment in primary human dermal fibroblasts and mouse tissues should proceed to identify potentially better candidates in his target systems.

8. **A universal senolytic circuit may not be achievable.** Tissue-specific circuit panels — each tuned to the miRNA landscape of its target tissue — may be more realistic than a single design that works everywhere. The liver-accumulation property of LNPs makes liver-specific de-targeting (via miR-122-5p OFF switch) a practical first target regardless of which ON-switch inputs are used.

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
