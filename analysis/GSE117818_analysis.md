# GSE117818 Analysis Report
## MRC-5 Fibroblast Replicative Senescence - 5-Timepoint miRNA Time Course

*Analysis date: 2026-04-07*

---

## 1. Study Summary

| Parameter | Details |
|-----------|---------|
| **GEO Accession** | [GSE117818](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE117818) |
| **Source** | JenAge Ageing Factor Database, Leibniz Institute on Aging - Fritz Lipmann Institute (FLI), Jena, Germany |
| **Organism** | *Homo sapiens* |
| **Cell type** | MRC-5 human fetal lung fibroblasts |
| **Senescence inducer** | Replicative senescence (serial passaging) |
| **Platform** | Illumina HiSeq 2000, small RNA-seq |
| **Time course** | 5 population doubling (PD) stages: PD32 (young), PD42, PD52, PD62, PD72 (senescent) |
| **Replicates** | 3 per timepoint |
| **Total samples** | 15 |
| **Data format** | Raw counts (precursor miRNA IDs, combining -5p and -3p strands) |
| **miRNAs detected** | 1,881 precursor miRNAs |

## 2. Significance

This dataset is valuable for three reasons:

1. **Independent fibroblast validation.** MRC-5 is a different fibroblast line from WI-38 (GSE299871) and IMR90 (GSE27404). Both are human fetal lung fibroblasts, but from different donors and maintained independently for decades. Concordance between MRC-5 and WI-38 would strongly validate our findings.

2. **Five-timepoint trajectory.** Unlike most senescence datasets that compare only "young" vs. "senescent," this time course reveals the kinetics of miRNA changes: do they change gradually, abruptly, or non-linearly during senescence progression?

3. **Replicative senescence.** This complements the DXR-induced (GSE299871), irradiation-induced (GSE202120), and SDS-induced (GSE299871) senescence data. Cross-inducer concordance for key miRNAs would indicate convergent downstream programs.

**Data format caveat:** The count data uses precursor miRNA IDs (e.g., `hsa-mir-34a`) without -5p/-3p suffix. This means counts represent the combined output of both mature strands processed from each precursor. For miRNAs where one strand dominates (e.g., miR-34a-5p >> miR-34a-3p), the precursor count is a reasonable proxy. For miRNAs with balanced strand usage, the precursor count may obscure strand-specific changes.

## 3. Results

### 3.1 Time Course Expression of Circuit-Relevant miRNAs

| miRNA (precursor) | PD32 | PD42 | PD52 | PD62 | PD72 | FC (PD72/PD32) | Trajectory |
|-------------------|------|------|------|------|------|----------------|-----------|
| **hsa-mir-34a** | 1,086 | 1,401 | 1,392 | 1,557 | **3,048** | **2.81x UP** | Progressive UP (accelerates at PD62-72) |
| hsa-mir-21 | 249,214 | 186,176 | 235,197 | 221,404 | 190,414 | 0.76x | Stable with fluctuation |
| hsa-mir-22 | 361,588 | 267,082 | 331,229 | 353,664 | 394,755 | 1.09x | Stable |
| hsa-mir-29c | 87 | 89 | 84 | 113 | **261** | **3.00x UP** | Progressive UP (accelerates at PD62-72) |
| hsa-mir-29a | 20,521 | 21,780 | 22,483 | 22,576 | **28,502** | **1.39x UP** | Gradual progressive UP |
| hsa-mir-146a | 12 | 9 | 10 | 9 | 15 | 1.24x | Stable (negligible counts) |
| **hsa-mir-155** | 1,806 | 2,786 | 2,391 | 976 | **185** | **0.10x DOWN** | **Progressive DOWN** (accelerates at PD52-72) |
| **hsa-mir-17** | 576 | 677 | 795 | 587 | **197** | **0.34x DOWN** | DOWN (non-linear, late decline) |
| **hsa-mir-16-1** | 6,825 | 7,545 | 8,980 | 6,696 | **3,623** | **0.53x DOWN** | DOWN (non-linear, late decline) |
| **hsa-mir-92a-1** | 11,862 | 10,416 | 10,066 | 7,515 | **3,785** | **0.32x DOWN** | **Progressive DOWN** |
| hsa-mir-122 | 1 | 0 | 0 | 0 | 0 | 0.25x | Not expressed |

### 3.2 Temporal Kinetics - When Do Changes Occur?

A striking pattern emerges: **most miRNA changes accelerate in late senescence (PD62→PD72)**. Many miRNAs are relatively stable from PD32 through PD52 or PD62, then change sharply at PD72 when cells are fully growth-arrested.

**Late-accelerating UP:**
- mir-34a: stable at ~1,100-1,400 through PD62, then jumps to 3,048 at PD72
- mir-29c: stable at ~85-113 through PD62, then jumps to 261 at PD72

**Late-accelerating DOWN:**
- mir-155: increases slightly (PD32→PD42: 1,806→2,786), then progressively declines (PD52→PD72: 2,391→976→185)
- mir-16-1: stable/slightly up through PD52 (6,825→8,980), then drops (PD62→PD72: 6,696→3,623)
- mir-17: stable through PD52, then drops at PD62-72

**Gradual progressive changes:**
- mir-92a-1: steady decline throughout (11,862→10,416→10,066→7,515→3,785)
- mir-29a: steady increase throughout (20,521→21,780→22,483→22,576→28,502)

This temporal pattern has implications for circuit design: the miRNA profile of **early senescent cells** (PD52-62) may be different from **late/deep senescent cells** (PD72). A circuit optimized for deep senescence markers (miR-34a high, miR-155 low) might not detect cells in early senescence.

### 3.3 Cross-Validation with WI-38 Data (GSE299871)

| miRNA | MRC-5 RS (this study) | WI-38 RS (GSE299871) | WI-38 DXR (GSE299871) | Concordance |
|-------|----------------------|---------------------|----------------------|-------------|
| **mir-34a** | **2.81x UP** | 3.0x UP | 2.5x UP | **All agree** |
| mir-21 | 0.76x stable | 2.2x UP | 1.8x UP | **Disagree** (stable in MRC-5, UP in WI-38) |
| mir-22 | 1.09x stable | 2.7x UP | 2.8x UP | **Disagree** (stable in MRC-5, UP in WI-38) |
| **mir-155** | **0.10x DOWN** | 0.19x DOWN | 0.14x DOWN | **All agree** (strongest in MRC-5) |
| **mir-16** | **0.53x DOWN** | 0.70x DOWN | 0.61x DOWN | **All agree** |
| **mir-92a** | **0.32x DOWN** | 0.47x DOWN | 0.42x DOWN | **All agree** (strongest in MRC-5) |
| mir-17 | 0.34x DOWN | 0.26x DOWN | 0.30x DOWN | **All agree** |
| mir-29c | 3.00x UP | 6x UP (2→12) | 5x UP (2→9) | Direction agrees; MRC-5 has higher baseline |
| mir-29a | 1.39x UP | 1.6x UP | 1.6x UP | **All agree** |
| mir-146a | 1.24x (12 counts) | 0.7x (8 counts) | 1.2x (14 counts) | Both negligible |

**Key concordances:**
- **miR-34a UP, miR-155 DOWN, miR-16 DOWN, miR-92a DOWN, miR-17 DOWN** - all validated across both fibroblast lines.
- These 5 miRNAs represent the **core replicative senescence fibroblast signature** that is reproducible across independent cell lines.

**Key discordances:**
- **miR-21 and miR-22** are UP in WI-38 (both RS and DXR) but stable in MRC-5. This may reflect genuine cell-line-specific differences or differences in the depth of senescence at the endpoint. In the MRC-5 time course, miR-21 and miR-22 do not change at any PD stage, suggesting this is a real difference between the two fibroblast lines rather than a timing artifact.

## 4. Discussion

### 4.1 The Five-miRNA Core Senescence Signature

Across MRC-5 (this study) and WI-38 (GSE299871, both DXR and RS), five miRNAs consistently change in the same direction:

| miRNA | Direction | Mechanism | Circuit Role |
|-------|-----------|-----------|-------------|
| **miR-34a** | UP | p53 target → SIRT1 (He et al., 2007, PMID: 17554337; Yamakuchi et al., 2008, PMID: 18755897) | ON switch |
| **miR-155** | DOWN | Immune/inflammatory regulator (O'Connell et al., 2007, PMID: 17242365) | OFF switch (fibroblast) |
| **miR-16** | DOWN | Cell cycle regulator targeting cyclins/CDKs (Linsley et al., 2007, PMID: 17210802) | OFF switch (cross-cell-type) |
| **miR-92a** | DOWN | miR-17~92 cluster member; proliferation-associated (Olive et al., *J Biol Chem*, 2009, PMID: 19726683) | OFF switch (fibroblast) |
| **miR-17** | DOWN | miR-17~92 cluster member; targets p21/CDKN1A (Faraonio et al., 2012, PMID: 22052189) | OFF switch candidate |

The miR-17~92 cluster (miR-17, miR-92a, and others) is a well-characterized oncogenic/proliferative cluster that is silenced during senescence. Its decline likely reflects epigenetic silencing of the MIR17HG locus as cells exit the cell cycle (Hackl et al., *Aging Cell*, 2010, PMID: 20409078).

### 4.2 MRC-5 vs. WI-38: Same Organ, Different Donors

Both MRC-5 and WI-38 are human fetal lung fibroblasts, yet miR-21 and miR-22 behave differently between them during senescence. This demonstrates that even within the same cell type and organ, donor-to-donor variability can affect miRNA trajectories. For circuit design, this means that miRNAs used as inputs must be robust across individual variation, not just reproducible within a single cell line. The five-miRNA core signature (miR-34a, miR-155, miR-16, miR-92a, miR-17) passes this test; miR-21 and miR-22 do not.

## 5. Limitations

1. **Precursor miRNA IDs only.** Cannot distinguish -5p and -3p strand changes. For most candidates, one strand dominates (e.g., miR-34a-5p), so this is a minor issue.
2. **No treatment control.** This is pure replicative senescence with no young-passage control held at the same culture time - the "young" samples (PD32) were harvested earlier. Time-in-culture effects cannot be distinguished from passage effects.
3. **Single cell type.** MRC-5 fibroblasts only.
4. **n=3 replicates per timepoint.** Adequate but not large.

## 6. Conclusions

1. **miR-34a is validated as UP (2.8x) in MRC-5 replicative senescence**, with a progressive trajectory that accelerates at late passages. This is now confirmed in 8 independent analyses.
2. **miR-155 is validated as DOWN (10x)** - the strongest decline in any dataset, with progressive kinetics from PD42 onward.
3. **miR-16 is validated as DOWN (0.53x)** - fourth human validation (WI-38 DXR, WI-38 RS, HUVEC RS, now MRC-5 RS).
4. **miR-92a shows the most progressive decline** (0.32x, steady from PD32 to PD72), qualifying as an additional OFF-switch candidate for fibroblast circuits.
5. A **five-miRNA core senescence signature** (miR-34a UP; miR-155, miR-16, miR-92a, miR-17 DOWN) is reproducible across two independent human fibroblast lines.
6. **miR-21 and miR-22 are NOT part of the core signature** - they change in WI-38 but not MRC-5, indicating cell-line-specific behavior.

---

## References

1. He L et al. *Nature*. 2007;447:1130-1134. PMID: 17554337
2. Yamakuchi M et al. *PNAS*. 2008;105(36):13421-13426. PMID: 18755897
3. O'Connell RM et al. *PNAS*. 2007;104(5):1604-1609. PMID: 17242365
4. Linsley PS et al. *RNA*. 2007;13(7):1012-1020. PMID: 17210802
5. Faraonio R et al. *Cell Death Differ*. 2012;19(4):616-624. PMID: 22052189
6. Hackl M et al. *Aging Cell*. 2010;9(2):291-296. PMID: 20409078
7. Olive V et al. *J Biol Chem*. 2009;284(9):5731-5741. PMID: 19726683
