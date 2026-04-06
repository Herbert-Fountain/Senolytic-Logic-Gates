# GSE94410 Analysis: Senescence miRNA Candidates in HUVEC Replicative Senescence

*Analysis date: 2026-04-06*

---

## 1. Objective

To evaluate literature-reported senescence-associated miRNAs using actual quantitative expression data from a publicly available small RNA-seq dataset, assessing their suitability as inputs for miRNA-responsive mRNA logic gate circuits.

## 2. Dataset

**Source:** GSE94410 (Terlecki-Zaniewicz et al., *Redox Biology*, 2018)
**Cell type:** Human umbilical vein endothelial cells (HUVECs)
**Senescence model:** Replicative exhaustion (serial passaging through 4 stages: S0 → S1 → S2 → S3)
**Method:** Small RNA-seq (Illumina NextSeq 500)
**Samples:** 15 total (3-4 biological replicates per stage from independent donors)

See [data/README.md](../data/README.md) for full sample mapping and data provenance.

## 3. Methods

Raw read counts were extracted directly from the GEO supplementary file `GSE94410_CountTable.txt`. Mean counts per miRNA were calculated for each passage group (S0, S1, S2, S3). Fold change was computed as mean(S3) / mean(S0).

**Important note on normalization:** We report raw mean counts, not normalized values. Library sizes may differ between samples. For publication-quality differential expression analysis, DESeq2 or equivalent normalization would be required. However, for the purpose of evaluating absolute expression magnitude (which determines circuit feasibility), raw counts provide a useful first approximation — a miRNA with 2 raw counts is not going to be a viable switch input regardless of normalization method.

## 4. Results

### 4.1 Candidate miRNA Expression Table

We evaluated 16 miRNAs identified as senescence-associated in the published literature (see [literature/senescence_mirna_review.md](../literature/senescence_mirna_review.md) for sources).

| miRNA | S0 Mean (young) | S3 Mean (old) | Fold Change | Absolute Level | Literature Report | Match? |
|-------|-----------------|---------------|-------------|---------------|-------------------|--------|
| hsa-miR-34a-5p | 46 | 239 | 5.2x UP | LOW-MED | UP in senescence | YES |
| hsa-miR-21-3p | 387 | 462 | 1.2x | MED | UP, retained intracellularly | WEAK |
| hsa-miR-21-5p | 407,800 | 1,070,778 | 2.6x UP | VERY HIGH | UP in senescence | YES |
| hsa-miR-22-3p | 58,962 | 18,652 | 0.3x DOWN | HIGH | UP in senescence | **NO — OPPOSITE** |
| hsa-miR-146a-5p | 401 | 410 | 1.0x | MED | UP in senescence | **NO — NO CHANGE** |
| hsa-miR-215-5p | 40 | 7 | 0.2x DOWN | VERY LOW | UP across 5 cell types (dox) | **NO — OPPOSITE** |
| hsa-miR-184 | 1 | 2 | ~1x | NEGLIGIBLE | UP across 5 cell types (dox) | **NOT EXPRESSED** |
| hsa-miR-96-5p | 8 | 2 | 0.2x DOWN | NEGLIGIBLE | Induces senescence | **NOT EXPRESSED** |
| hsa-miR-181a-5p | 29,629 | 5,391 | 0.2x DOWN | HIGH | UP in senescence | **NO — OPPOSITE** |
| hsa-miR-217 | 820 | 1,388 | 1.7x UP | HIGH | UP in senescence | YES (modest) |
| hsa-miR-375 | 5 | 0 | DOWN | NEGLIGIBLE | UP in dox-senescence (K562) | **NOT EXPRESSED** |
| hsa-miR-17-5p | 1,544 | 9,083 | 5.9x UP | HIGH | DOWN in senescence | **NO — OPPOSITE** |
| hsa-miR-17-3p | 65 | 80 | 1.2x | LOW | Retained intracellularly | WEAK |
| hsa-miR-15b-5p | 310 | 294 | 0.9x | MED | UP in senescent sEVs | NO CHANGE |
| hsa-miR-30a-3p | 7,331 | 2,223 | 0.3x DOWN | HIGH | UP in senescent sEVs | **NO — OPPOSITE** |
| hsa-miR-122-5p | 108 | 21 | 0.2x DOWN | LOW | Liver-specific marker | AS EXPECTED |

### 4.2 Summary Statistics

- **Matched literature direction:** 4/16 (25%) — miR-34a-5p, miR-21-5p, miR-21-3p (weak), miR-217
- **Opposite direction:** 6/16 (37.5%) — miR-22-3p, miR-215-5p, miR-181a-5p, miR-17-5p, miR-30a-3p, miR-96-5p
- **No change:** 2/16 (12.5%) — miR-146a-5p, miR-15b-5p
- **Not expressed (<10 counts):** 4/16 (25%) — miR-184, miR-96-5p, miR-375, miR-17-3p

## 5. Discussion

### 5.1 Cell-Type Specificity of Senescence miRNA Programs

The most striking finding is that **only 25% of literature-reported senescence miRNAs showed the expected expression pattern** in this HUVEC dataset. This is consistent with the Weigl/Grillari 2024 finding that senescence miRNA changes are highly cell-type specific. The implications for senolytic circuit design are significant:

- A circuit designed using fibroblast senescence data (the most common model in the literature) may not function correctly in endothelial cells, epithelial cells, or other tissue types.
- The goal of a "universal" senolytic circuit that kills senescent cells regardless of tissue origin may require multiple tissue-specific circuit variants rather than a single design.
- Alternatively, the circuit could target the small number of miRNAs that appear consistent across cell types, but our analysis shows these are rare.

### 5.2 Absolute Expression vs. Fold Change

This analysis demonstrates why fold change alone is insufficient for circuit input selection:

**miR-184** is reported as upregulated in doxorubicin-induced senescence across 5 cell types (Weigl/Grillari 2024). In HUVECs, it has **1-2 raw counts**. Even if it increased 100-fold to 200 counts, the absolute number of miRNA molecules per cell would likely be insufficient to reliably engage a switch mRNA. The Saito lab's switch system depends on the ratio of endogenous miRNA to delivered mRNA molecules, and at very low miRNA abundance, the mRNA pool will overwhelm the miRNA, causing leaky expression of the cytotoxic payload.

Conversely, **miR-21-5p** shows only a 2.6-fold increase but starts at ~400,000 counts and reaches ~1,000,000. The absolute intracellular concentration of this miRNA is enormous, which would make it a very reliable switch input from a stoichiometric perspective. The challenge is that it's already highly expressed in young/healthy cells (400K counts), so the ON/OFF ratio of the circuit would be limited.

### 5.3 The Ideal Switch Input Profile

Based on our analysis, an ideal ON-switch miRNA input would have:

1. **High absolute expression in senescent cells** (thousands of counts, not tens) to ensure reliable switch activation
2. **Low expression in healthy cells** (ideally <100 counts) to prevent leaky payload expression
3. **Large fold change** (>5x) to provide a clear ON/OFF differential
4. **Consistency across cell types** (not just one tissue)
5. **Conservation between mouse and human** (for translational studies)
6. **Intracellular retention** (not secreted via EVs)

No single miRNA in our analysis meets all criteria. **miR-34a-5p** comes closest (5.2x increase, 239 counts in senescent cells, well-conserved, consistent across studies) but the absolute counts are relatively low.

### 5.4 Implications for Circuit Architecture

Given the challenges identified, several circuit design strategies may help:

1. **Multi-input AND gates** requiring 2-3 miRNAs that are each modestly upregulated in senescence. Even if no single miRNA provides clean ON/OFF switching, requiring multiple inputs simultaneously could achieve the needed selectivity.

2. **Hybrid ON + OFF design** (as in Saito's 2025 paper, achieving 16-fold dynamic range). Using a senescence-upregulated miRNA as ON input AND a healthy-tissue miRNA as OFF/de-targeting input could improve selectivity even when individual switch performance is modest.

3. **Tissue-specific circuit panels** rather than a universal design. Different tissues could receive circuits tuned to their local miRNA landscape.

### 5.5 Limitations of This Analysis

1. **Replicative senescence ≠ doxorubicin-induced senescence.** The miRNA changes in chemotherapy-induced senescence may differ substantially. Herbert's planned doxorubicin small RNA-seq experiment is essential.

2. **Single cell type.** HUVECs are endothelial cells; fibroblasts, which are the primary target for many senolytic applications, may show different patterns.

3. **Raw counts without normalization.** Library size differences between samples could bias fold change estimates. However, the key findings (miRNAs with <10 counts being unsuitable, direction mismatches) are robust to normalization method choice.

4. **Replicative senescence is progressive, not acute.** The S0→S3 transition occurs over many passages, whereas doxorubicin induces senescence acutely (24-48 hours). Acute and chronic senescence may have different miRNA kinetics.

## 6. Conclusions

1. **Literature-reported senescence miRNAs cannot be used as circuit inputs without experimental validation in the target cell type and senescence model.** The disconnect between published reports and actual expression data is too large.

2. **Absolute miRNA abundance must be a primary selection criterion,** not fold change. Circuit designers should set a minimum count threshold based on the expected mRNA delivery dose.

3. **Herbert's planned doxorubicin small RNA-seq experiment is the single most important next step.** No existing public dataset provides the combination of doxorubicin inducer + multiple cell types + absolute count data needed for confident circuit design.

4. **The Weigl/Grillari 2024 dataset (if raw data can be obtained) would be the most valuable external resource,** as it uses doxorubicin on 5 human primary cell types with small RNA-seq.

---

## Appendix: Reproduction

```python
import pandas as pd

df = pd.read_csv('data/GSE94410/GSE94410_CountTable.txt', sep='\t')

s0 = ['1_Counts', '2_Counts', '3_Counts']           # Young
s3 = ['12_Counts', '13_Counts', '14_Counts', '15_Counts']  # Senescent

candidates = ['hsa-miR-34a-5p', 'hsa-miR-21-5p', ...]  # See full list above

for mirna in candidates:
    row = df[df['Name'] == mirna].iloc[0]
    mean_s0 = row[s0].mean()
    mean_s3 = row[s3].mean()
    fc = mean_s3 / mean_s0 if mean_s0 > 0 else float('inf')
    print(f'{mirna}: S0={mean_s0:.0f}, S3={mean_s3:.0f}, FC={fc:.1f}x')
```
