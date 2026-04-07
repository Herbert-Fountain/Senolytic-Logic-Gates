# Normalization Corrections
## Impact of Library Size Normalization on All Reported Fold Changes

*Date: 2026-04-07*
*Addressing Peer Review Concern #1 (MAJOR)*

---

## 1. The Problem

All fold changes in our initial analyses were computed from **raw read counts** without correcting for library size differences between samples. Library size (total mapped miRNA reads) can vary substantially between samples due to differences in sequencing depth, RNA input, and library prep efficiency. If senescent/aged samples have systematically larger or smaller libraries than control/young samples, all fold changes will be biased in the same direction.

## 2. Correction Method

We applied **Counts Per Million (CPM)** normalization, the simplest library-size correction:

```
CPM = (raw counts for miRNA X / total miRNA counts in sample) × 1,000,000
```

This corrects for differences in sequencing depth while preserving the compositional relationships between miRNAs within each sample. More sophisticated methods (DESeq2, TMM) are recommended for formal differential expression testing but CPM is adequate for fold change estimation.

## 3. Library Size Analysis

### GSE299871 (WI-38 fibroblasts)

| Sample Group | Mean Library Size | Ratio to Ctrl |
|-------------|------------------|---------------|
| Ctrl | 0.28M | 1.0x |
| DXR D16 | 0.45M | **1.6x** |
| SDS D16 | 1.19M | **4.3x** |
| RS | 0.53M | **1.9x** |

**The DXR/SDS/RS samples have 1.6-4.3x larger libraries than controls.** This means every raw fold change for upregulated miRNAs was inflated by approximately this factor, and every raw fold change for downregulated miRNAs was deflated.

### GSE94410 (HUVECs)

| Sample Group | Mean Library Size | Ratio to S0 |
|-------------|------------------|-------------|
| S0 (young) | 5.8M | 1.0x |
| S3 (senescent) | 3.0M | **0.53x** |

**The senescent HUVEC samples have ~half the library size of young samples.** This means every raw fold change for upregulated miRNAs was underestimated, and every downregulated miRNA was overestimated.

## 4. Corrected Fold Changes

### GSE299871: DXR Senescence (WI-38)

| miRNA | Raw FC | CPM FC | Impact | Status |
|-------|--------|--------|--------|--------|
| **miR-34a-5p** | 2.47x UP | **1.50x UP** | Reduced but direction holds | **Still valid ON-switch** |
| miR-22-3p | 2.83x UP | **1.74x UP** | Reduced but direction holds | Still valid |
| **miR-29a-3p** | 1.56x UP | **0.96x STABLE** | **DIRECTION LOST** | **Eliminated as ON-switch** |
| miR-21-5p | 1.79x UP | **1.09x STABLE** | Nearly 1x | **No longer meaningful** |
| miR-155-5p | 0.14x DOWN | **0.09x DOWN** | Even stronger decline | **Strengthened OFF-switch** |
| miR-16-5p | 0.61x DOWN | **0.37x DOWN** | Even stronger decline | **Strengthened OFF-switch** |
| miR-92a-3p | 0.42x DOWN | **0.26x DOWN** | Even stronger decline | **Strengthened OFF-switch** |
| miR-17-5p | 0.30x DOWN | **0.19x DOWN** | Even stronger decline | **Strengthened OFF-switch** |

### GSE299871: SDS Senescence (WI-38)

| miRNA | Raw FC | CPM FC | Impact |
|-------|--------|--------|--------|
| miR-34a-5p | 7.18x UP | **1.66x UP** | Dramatically reduced (SDS had 4.3x library bias) |
| miR-22-3p | 6.06x UP | **1.41x UP** | Reduced |
| miR-29a-3p | 6.19x UP | **1.32x UP** | Reduced (marginally UP, not dramatic) |
| miR-155-5p | 0.99x | **0.23x DOWN** | Now clearly DOWN (was hidden by library bias) |

### GSE299871: Replicative Senescence (WI-38)

| miRNA | Raw FC | CPM FC | Impact |
|-------|--------|--------|--------|
| miR-34a-5p | 3.02x UP | **1.50x UP** | Reduced but holds |
| miR-29a-3p | 1.59x UP | **0.81x DOWN** | **Direction reverses** |
| miR-155-5p | 0.19x DOWN | **0.11x DOWN** | Strengthened |

### GSE94410: HUVEC Replicative Senescence

| miRNA | Raw FC | CPM FC | Impact | Status |
|-------|--------|--------|--------|--------|
| miR-34a-5p | 5.24x UP | **11.49x UP** | Enhanced (library bias was hiding signal) | Strengthened |
| miR-22-3p | 0.32x DOWN | **0.65x DOWN** | Less dramatic but still DOWN | Holds |
| **miR-155-5p** | 0.90x STABLE | **1.81x UP** | **DIRECTION REVERSED** | **No longer a valid OFF-switch in HUVECs** |
| miR-16-5p | 0.43x DOWN | **0.89x STABLE** | **Direction weakened** | **Uncertain in HUVECs** |
| miR-92a-3p | 2.61x UP | **5.14x UP** | Enhanced | - |
| miR-17-5p | 5.88x UP | **10.99x UP** | Enhanced | - |

## 5. Impact on Key Conclusions

### What Still Holds After Normalization

1. **miR-34a-5p is still consistently UP across all contexts.** The magnitude is reduced in GSE299871 (2.5x → 1.5x) but enhanced in GSE94410 (5.2x → 11.5x). Direction is consistent across all datasets.

2. **miR-155-5p, miR-92a-3p, miR-17-5p are even MORE strongly downregulated** in senescent fibroblasts after normalization. The OFF-switch candidates are strengthened.

3. **The five-miRNA core senescence signature** (miR-34a UP; miR-155, miR-16, miR-92a, miR-17 DOWN) holds in WI-38 fibroblasts.

### What Changes

1. **miR-29a-3p is NO LONGER upregulated in DXR senescence** (CPM FC = 0.96x). Its apparent 1.6x increase was entirely a library size artifact. miR-29a-3p should be **removed from the ON-switch candidate list** for fibroblast circuits. The strong increases seen in SDS (1.32x CPM) and in vivo aging data (mouse/rat) may still be real but need verification.

2. **miR-21-5p is effectively stable** in DXR senescence (CPM FC = 1.09x). Its raw 1.8x increase was inflated. miR-21-5p should not be considered a senescence-upregulated miRNA in WI-38 fibroblasts.

3. **miR-155-5p is UP (1.81x) in senescent HUVECs after normalization** - the raw data suggested stability (0.90x). This changes the inflammaging interpretation: miR-155-5p may genuinely increase in some senescent cell types (endothelial), not just through immune cell infiltration. The OFF-switch recommendation for miR-155-5p now applies only to fibroblasts, not endothelial cells.

4. **miR-16-5p decline in HUVECs is less certain** (CPM FC = 0.89x vs raw 0.43x). The dramatic raw decline was largely a library size artifact. miR-16-5p may not be a reliable OFF-switch in endothelial cells.

5. **The SDS fold changes were the most inflated** (4.3x library bias). The "SDS consistently produces larger fold changes than DXR" statement in the synthesis was an artifact of larger SDS libraries, not a biological difference. After normalization, SDS and DXR produce similar fold changes.

## 6. Revised Candidate Rankings

### ON-Switch Candidates (CPM-corrected)

| Rank | miRNA | CPM FC (DXR) | CPM Level (senescent) | Assessment |
|------|-------|-------------|----------------------|------------|
| **1** | **miR-34a-5p** | 1.50x | 558 CPM | Only consistent ON candidate; modest FC |
| 2 | miR-22-3p | 1.74x | 15,543 CPM | Higher FC, high counts, fibroblast-specific |
| ~~3~~ | ~~miR-29a-3p~~ | ~~0.96x~~ | - | **ELIMINATED - no change after normalization** |
| ~~4~~ | ~~miR-21-5p~~ | ~~1.09x~~ | - | **ELIMINATED - no change after normalization** |

### OFF-Switch Candidates (CPM-corrected, STRENGTHENED)

| Rank | miRNA | CPM FC (DXR) | CPM Level (healthy) | Assessment |
|------|-------|-------------|---------------------|------------|
| **1** | **miR-155-5p** | **0.09x** | 9,887 CPM | 11x decline - strongest OFF-switch |
| **2** | **miR-92a-3p** | **0.26x** | 23,101 CPM | 3.8x decline, highest expression |
| **3** | **miR-16-5p** | **0.37x** | 3,172 CPM | 2.7x decline |
| **4** | **miR-17-5p** | **0.19x** | 472 CPM | 5.3x decline, lower expression |

## 7. Note on Other Datasets

The following datasets provided pre-normalized data and are NOT affected by this correction:
- **GSE217458** (RPMM-normalized by original authors)
- **GSE55164** (log2 normalized by original authors)
- **GSE136926** (normalized by original authors)

The following datasets use raw counts and SHOULD be CPM-corrected:
- **GSE172269** (rat BodyMap) - correction pending
- **GSE111281/GSE111174** (JenAge skin/blood) - precursor IDs, correction pending
- **GSE117818** (MRC-5) - precursor IDs, correction pending
- **GSE200330** (EV miRNAs) - per-sample RPM already provided

## 8. Lessons Learned

1. **Always normalize before computing fold changes.** This is standard practice in RNA-seq analysis but was not applied in our initial exploratory analyses. The raw count comparisons were useful for identifying candidate directions but the magnitudes were unreliable.

2. **Library size biases can be systematic.** In GSE299871, all treated groups had larger libraries than controls - possibly because senescent cells produce more total miRNA, or because more RNA was extracted from those samples. This creates a consistent bias that inflates all apparent upregulation and hides all downregulation.

3. **The direction of change is more robust than the magnitude.** After CPM correction, most directional conclusions held (7/9 miRNAs kept the same direction in DXR). But magnitudes changed substantially, and two miRNAs lost their signal entirely.

---

## References

- Fuchs RT et al. Bias in ligation-based small RNA sequencing library construction is determined by adaptor and RNA structure. *PLoS One*. 2015;10(5):e0126049. PMID: 25942504
- Dillies MA et al. A comprehensive evaluation of normalization methods for Illumina high-throughput RNA sequencing data analysis. *Brief Bioinform*. 2013;14(6):671-683. PMID: 22988256
