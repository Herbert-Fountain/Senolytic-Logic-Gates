# GSE217458 Analysis Report
## Natural Mouse Aging — miRNA Expression Across 16 Tissues

*Analysis date: 2026-04-06*
*Dataset: GSE217458 (Wagner et al., Nature Biotechnology, 2024)*

---

## 1. Study Summary

| Parameter | Details |
|-----------|---------|
| **GEO Accessions** | [GSE217458](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE217458), [GSE222857](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE222857) |
| **Publication** | Wagner V, Kern F, Hahn O et al. Characterizing expression changes in noncoding RNAs during aging and heterochronic parabiosis across mouse tissues. *Nature Biotechnology*. 2024;42:109-118. PMID: [37106037](https://pubmed.ncbi.nlm.nih.gov/37106037/). DOI: [10.1038/s41587-023-01751-6](https://doi.org/10.1038/s41587-023-01751-6) |
| **Organism** | *Mus musculus* (C57BL/6JN) |
| **Cohort** | Tabula Muris Senis (TMS) |
| **Tissues** | 16: bone, brain, BAT, GAT, heart, kidney, limb muscle, liver, lung, bone marrow, MAT, pancreas, skin, small intestine, spleen, SCAT |
| **Ages** | 10 timepoints: 1, 3, 6, 9, 12, 15, 18, 21, 24, 27 months |
| **Method** | Small RNA-seq |
| **Samples** | 771 total (up to 6 replicates per tissue per timepoint) |
| **Data format** | RPMM (reads per million mapped) — normalized expression |
| **Total ncRNAs** | 7,883 (including 1,076 miRBase-annotated miRNAs) |
| **Additional data** | Plasma, plasma-derived EVs, heterochronic parabiosis rejuvenation |

## 2. Data Files Used

Downloaded from GEO supplementary files on 2026-04-06:

| File | Description | Size |
|------|-------------|------|
| `GSE217458_TMS_rpmm_Complete_Filtered_global_GEO_18012023.csv` | RPMM-normalized expression matrix (7,883 ncRNAs × 771 samples) | 48 MB |
| `GSE217458_annotation_TMS.csv` | Sample annotation (organ, age, sex, sample IDs) | 151 KB |

**Download URLs:**
```
https://ftp.ncbi.nlm.nih.gov/geo/series/GSE217nnn/GSE217458/suppl/GSE217458_TMS_rpmm_Complete_Filtered_global_GEO_18012023.csv.gz
https://ftp.ncbi.nlm.nih.gov/geo/series/GSE217nnn/GSE217458/suppl/GSE217458_annotation_TMS.csv.gz
```

## 3. Methods

### 3.1 Analysis Approach
We extracted expression values for senescence candidate miRNAs across 6 tissues of interest (heart, kidney, liver, lung, spleen, skin) that overlap with our pilot small RNA-seq data. Mean RPMM was calculated for young (1, 3, 6 months) and old (21, 24, 27 months) age groups. Fold change was computed as mean(old) / mean(young).

### 3.2 Important Context
This is **natural aging** data from intact tissues, NOT pure senescent cell populations. Aged tissues contain a mixture of senescent and non-senescent cells. Therefore:
- miRNA changes likely underestimate the true senescent-cell-specific signal (diluted by non-senescent cells)
- Some changes may reflect cell composition shifts (e.g., immune cell infiltration) rather than cell-autonomous senescence
- Direct comparison with in vitro senescence data (where 100% of cells are senescent) requires accounting for this dilution

## 4. Results

### 4.1 Candidate miRNA Expression Across Tissues

Values are mean RPMM for young (1-6 months, n varies) vs. old (21-27 months, n varies) animals.

| miRNA | Tissue | Young RPMM | Old RPMM | FC | Notes |
|-------|--------|-----------|---------|-----|-------|
| **mmu-miR-29c-3p** | Heart | 3,049 | 4,574 | 1.5x | Strongest pan-tissue aging signal (Wagner 2024) |
| | Kidney | 2,638 | 4,561 | 1.7x | |
| | Liver | 2,020 | 3,550 | 1.8x | |
| | Lung | 2,795 | 4,555 | 1.6x | |
| | Spleen | 699 | 1,285 | 1.8x | |
| | Skin | 439 | 1,356 | **3.1x** | Largest change |
| **mmu-miR-29a-3p** | Heart | 6,894 | 10,192 | 1.5x | Same family as miR-29c |
| | Kidney | 6,312 | 11,221 | 1.8x | |
| | Liver | 5,111 | 8,616 | 1.7x | |
| | Lung | 10,028 | 16,278 | 1.6x | |
| | Spleen | 5,923 | 7,180 | 1.2x | |
| | Skin | 3,207 | 7,273 | **2.3x** | |
| **mmu-miR-21a-5p** | Heart | 1,575 | 2,220 | 1.4x | Very abundant |
| | Kidney | 5,163 | 7,999 | 1.5x | |
| | Liver | 14,180 | 14,519 | 1.0x | No change in liver |
| | Lung | 7,559 | 12,676 | 1.7x | |
| | Spleen | 8,640 | 15,707 | **1.8x** | |
| | Skin | 4,330 | 5,763 | 1.3x | |
| **mmu-miR-34a-5p** | Heart | 1,167 | 1,587 | 1.4x | Classic senescence marker |
| | Kidney | 2,535 | 3,829 | 1.5x | |
| | Liver | 843 | 1,056 | 1.3x | |
| | Lung | 1,548 | 2,597 | 1.7x | |
| | Spleen | 488 | 756 | 1.5x | |
| | Skin | 1,113 | 1,305 | 1.2x | |
| **mmu-miR-155-5p** | Heart | 343 | 423 | 1.2x | Immune/inflammatory miRNA |
| | Kidney | 108 | 217 | 2.0x | |
| | Liver | 21 | 89 | **4.2x** | Largest FC; low baseline |
| | Lung | 122 | 457 | **3.8x** | |
| | Spleen | 703 | 1,219 | 1.7x | |
| | Skin | 74 | 96 | 1.3x | |
| **mmu-miR-146a-5p** | Heart | 207 | 322 | 1.6x | SASP regulator |
| | Kidney | 237 | 537 | **2.3x** | |
| | Liver | 244 | 313 | 1.3x | |
| | Lung | 1,434 | 2,085 | 1.5x | |
| | Spleen | 1,711 | 1,734 | 1.0x | |
| | Skin | 432 | 490 | 1.1x | |
| **mmu-miR-184-3p** | Heart | 2.8 | 2.9 | 1.1x | Pan-tissue aging UP (Wagner 2024) |
| | Kidney | 1.3 | 1.8 | 1.4x | |
| | Liver | 2.2 | 5.9 | 2.7x | |
| | Lung | 2.1 | 4.9 | 2.4x | |
| | Spleen | 1.7 | 4.2 | 2.5x | |
| | Skin | 3.2 | 4.1 | 1.3x | |
| **mmu-miR-22-3p** | Heart | 9,397 | 10,706 | 1.1x | Reported UP in dox-K562 |
| | Kidney | 7,553 | 7,975 | 1.1x | |
| | Liver | 9,572 | 11,291 | 1.2x | |
| | Lung | 4,635 | 5,730 | 1.2x | |
| | Spleen | 1,695 | 1,521 | 0.9x | |
| | Skin | 2,600 | 4,029 | 1.5x | |
| **mmu-miR-96-5p** | Heart | 0.6 | 0.7 | 1.2x | Induces senescence (Santiago 2024) |
| | Kidney | 13.0 | 15.2 | 1.2x | |
| | Liver | 6.9 | 10.5 | 1.5x | |
| | Lung | 48.1 | 47.0 | 1.0x | |
| | Spleen | 2.5 | 4.0 | 1.6x | |
| | Skin | 42.6 | 65.3 | 1.5x | |
| **mmu-miR-122-5p** | Heart | 35.1 | 42.9 | 1.2x | Liver-specific |
| | Kidney | 32.9 | 32.7 | 1.0x | |
| | Liver | 99,551 | 115,487 | 1.2x | |
| | Lung | 33.4 | 49.6 | 1.5x | |
| | Spleen | 27.9 | 17.9 | 0.6x | |
| | Skin | 21.7 | 10,194 | **470x** | Likely contamination or outlier |
| **mmu-miR-17-5p** | Heart | 229 | 279 | 1.2x | miR-17 family |
| | Kidney | 570 | 589 | 1.0x | |
| | Liver | 385 | 401 | 1.0x | |
| | Lung | 460 | 549 | 1.2x | |
| | Spleen | 1,101 | 956 | 0.9x | |
| | Skin | 537 | 526 | 1.0x | |

### 4.2 Data Quality Note

The mmu-miR-122-5p value in old skin (10,194 RPMM vs. 21.7 in young) is a **470-fold outlier** and almost certainly reflects either sample contamination (e.g., liver tissue co-isolated with skin) or a data processing artifact. miR-122-5p is canonically liver-specific, with expression in our pilot data at ~100,000 counts in liver and <150 in all other tissues. This data point should be flagged and excluded from downstream analysis.

## 5. Discussion

### 5.1 Comparison with In Vitro Senescence Data (GSE94410)

| miRNA | GSE94410 (HUVEC in vitro) | GSE217458 (Mouse in vivo) | Concordance |
|-------|--------------------------|--------------------------|-------------|
| miR-34a-5p | 5.2x UP (46→239) | 1.2-1.7x UP (500-3800 RPMM) | **YES** — same direction, higher absolute levels in vivo |
| miR-21-5p | 2.6x UP (408K→1.1M) | 1.0-1.8x UP (1.5K-16K RPMM) | **YES** — same direction |
| miR-22-3p | 0.3x DOWN (59K→19K) | 0.9-1.5x (~stable) | **PARTIAL** — down in vitro, stable in vivo |
| miR-146a-5p | 1.0x (no change) | 1.0-2.3x (variable) | **PARTIAL** — no change in HUVEC, modest UP in some mouse tissues |
| miR-17-5p | 5.9x UP (1.5K→9K) | 0.9-1.2x (~stable) | **NO** — up in HUVEC, stable in mouse |
| miR-181a-5p | 0.2x DOWN (30K→5K) | Not shown here | N/A |

**Interpretation:** The modest in vivo aging changes (1.2-1.8x) compared to larger in vitro senescence changes (2-6x) are expected. Aged tissue is a mixture of senescent and non-senescent cells; if senescent cells comprise 10-20% of an aged tissue, a miRNA that's 10x higher in senescent cells would appear only 1.9-2.8x higher in bulk tissue. The direction of change is more informative than the magnitude when comparing these two data types.

### 5.2 miR-29 Family as Novel Circuit Candidates

The miR-29 family (miR-29a-3p, miR-29c-3p) emerged from this dataset as strong candidates that were NOT prominently featured in the in vitro senescence literature:

- **Consistently UP across all 6 tissues** (1.2-3.1x), the most uniform aging signal
- **High absolute expression** (700-16,000 RPMM), sufficient for circuit engagement
- **Reversed by heterochronic parabiosis** (Wagner et al., 2024), suggesting the change is driven by aging biology, not just developmental shifts
- **Targets ECM and secretion pathways** (Wagner et al., 2024), consistent with SASP biology

However, we cannot confirm from this data alone that miR-29 upregulation is driven by senescent cells specifically. It could reflect:
- Age-related changes in cell composition (e.g., increased fibrosis = more fibroblasts expressing miR-29)
- Systemic signaling changes
- Cell-autonomous aging in multiple cell types

**This must be tested in Herbert's planned doxorubicin senescence experiment.**

### 5.3 miR-184-3p: Pan-Tissue Aging Marker but Impractical for Circuits

Wagner et al. (2024) identified miR-184-3p as one of 8 broadly deregulated aging miRNAs. Our analysis confirms it increases with age in most tissues (1.1-2.7x). However, the absolute expression is **1-6 RPMM** — far too low for circuit applications. This illustrates a fundamental disconnect between biomarker discovery (where any detectable change is informative) and circuit engineering (where absolute molecule count determines function).

### 5.4 miR-155-5p: The Inflammaging Paradox — A Novel Synthesis

miR-155-5p shows the largest fold changes in aged liver (4.2x, 21→89 RPMM) and lung (3.8x, 122→457 RPMM). This is **paradoxical** because in pure senescent cell populations in vitro, miR-155-5p is strongly DOWN: 0.14x in DXR-senescent WI-38 fibroblasts (GSE299871), 0.19x in replicatively senescent WI-38 fibroblasts, and confirmed downregulated in senescent IMR90 fibroblasts (Faraonio et al., *Cell Death Differ*, 2012, PMID: 22052189).

We propose that this apparent contradiction is explained by **immune cell infiltration into aged tissues**, a phenomenon central to the concept of "inflammaging" — the chronic, low-grade inflammation that accompanies aging (Franceschi et al., *Ann N Y Acad Sci*, 2000, PMID: 10911963). The evidence supporting this explanation comes from multiple independent lines:

1. **miR-155 is one of the most enriched miRNAs in activated macrophages.** It is induced >100-fold in M1-polarized macrophages (Mann et al., *PLoS One*, 2017, PMID: 27447824) and is the primary miRNA induced by TLR ligands and IFN-β in the macrophage inflammatory response (O'Connell et al., *PNAS*, 2007, PMID: 17242365). It is essential for normal immune function, as demonstrated by miR-155 knockout mice (Rodriguez et al., *Science*, 2007, PMID: 17463290).

2. **Macrophages accumulate in aged tissues.** Single-cell transcriptomic profiling of aged mouse tissues (Tabula Muris Senis; The Tabula Muris Consortium, *Nature*, 2020, PMID: 32669714) has documented expansion of M1-like macrophage populations in multiple organs with aging, including kidney. Senescent cells actively chemoattract macrophages through SASP-mediated immune surveillance (Prata et al., *Semin Immunol*, 2018), and impaired clearance in aging leads to macrophage accumulation.

3. **Macrophage-derived exosomal miR-155 can transfer to and affect neighboring cells.** Recent studies have shown that macrophage-derived exosomes deliver miR-155 to kidney tubular epithelial cells, driving senescence via TRF1 targeting and telomere dysfunction (Yin et al., *Cell Commun Signal*, 2024, PMID: 38987851). Similarly, M1 macrophage-derived exosomal miR-155 induces endothelial senescence via SOCS1/JAK2/STAT3 signaling in aged aortas (He et al., *Hum Mutat*, 2025, PMID: 40486266).

4. **Bulk tissue miRNA measurements are confounded by cell-type composition.** Recent work has explicitly demonstrated that cellular heterogeneity is an important confounding factor in bulk miRNA profiling, and cell-type deconvolution tools have been developed to address this (Roest et al., *Nat Commun*, 2025, DOI: 10.1038/s41467-025-60521-x). Single-cell miRNA profiling confirms that miR-155 expression varies dramatically across immune cell subpopulations (Hernandez de Sande et al., *Genome Med*, 2025, PMID: 41053866).

**To our knowledge, no published paper has explicitly synthesized these observations into the unified explanation we propose:** that the apparent upregulation of miR-155 in aged tissues measured by bulk sequencing is substantially or entirely a cell-composition artifact driven by increased macrophage/immune cell representation, and that the cell-autonomous response in parenchymal cells (fibroblasts, epithelial cells) is actually downregulation. The individual pieces are well-established across the literature, but the connection between in vitro senescence data and in vivo aging data for miR-155 has not been framed as a measurement artifact.

**Implications for circuit design are significant:**

1. **In vitro**, miR-155-5p's 7-fold decline in senescent fibroblasts makes it an excellent OFF-switch candidate for protecting non-senescent cells. The circuit logic is clean: healthy cells have high miR-155 (payload suppressed), senescent cells have low miR-155 (payload expressed).

2. **In vivo**, the picture is complicated. Macrophage-derived exosomal miR-155 can be delivered to neighboring cells (Yin 2024, He 2025). If senescent cells near macrophage-rich zones receive exosomal miR-155, the OFF switch could be inadvertently engaged, suppressing the cytotoxic payload in exactly the cells it should be killing. This paracrine transfer of miR-155 from macrophages to senescent cells could create a **therapeutic dead zone** around inflammatory foci.

3. This paradox could be resolved by **single-cell miRNA profiling of aged tissues** to determine the actual intracellular miR-155 levels within senescent cells in vivo, accounting for both endogenous expression and exosomal delivery. Alternatively, **cell-type deconvolution** of existing bulk tissue miRNA-seq data (using tools like those described by Roest et al., 2025) could estimate parenchymal cell miR-155 levels independently of immune cell contributions.

This analysis illustrates a broader challenge: **miRNA profiles measured in isolated cell cultures may not reflect the intracellular miRNA landscape within intact tissues**, where intercellular communication via EVs, direct cell contact, and local immune microenvironments contribute additional complexity. Future senolytic circuit design studies should validate miRNA input candidates using single-cell or spatially resolved approaches rather than relying solely on bulk tissue or isolated cell culture data.

### 5.5 Downregulated miRNAs in Natural Aging

Most candidate miRNAs that decline in in vitro senescence (miR-155-5p, miR-17-5p, miR-92a-3p, miR-16-5p) show **no decline** or **slight increases** in aged mouse tissues. This is consistent with two non-exclusive explanations:
1. The cell-autonomous decline is diluted by non-senescent cells in bulk tissue
2. Age-related changes in cell composition (immune infiltration, fibrosis) produce miRNAs that mask the senescent-cell signal

The exception is that no miRNA in this dataset shows a clear pan-tissue decline with aging, reinforcing the finding from Wagner et al. (2024) that aging trajectories are largely tissue-specific.

## 6. Limitations

1. **Natural aging ≠ induced senescence.** Aged tissues contain mixed cell populations. The miRNA signal is diluted.
2. **Mouse, not human.** While most miRNAs are conserved, expression levels and aging trajectories may differ in human tissues.
3. **RPMM normalization** was applied by the original authors. We did not re-normalize from raw data.
4. **Young vs. old comparison** groups extreme ages (1-6 mo vs. 21-27 mo). Intermediate timepoints could reveal non-linear dynamics.
5. **No senescence markers measured.** We cannot correlate miRNA changes with SA-β-gal, p16, p21, or other senescence markers in these tissues.

## 7. Conclusions

1. The miR-29 family (miR-29a-3p, miR-29c-3p) warrants investigation as potential circuit inputs based on high expression, consistent cross-tissue upregulation with age, and reversibility by rejuvenation.
2. miR-184-3p, despite being a pan-tissue aging marker, is impractical for circuit applications due to negligible absolute expression levels.
3. In vivo aging data shows more modest fold changes than in vitro senescence, as expected from the dilution of senescent cells within bulk tissue.
4. Direct comparison between in vitro senescence and in vivo aging datasets reveals partial concordance for some miRNAs (miR-34a, miR-21) but not others (miR-22, miR-17), highlighting the importance of context-specific validation.

---

## Appendix: Reproduction Code

```python
import pandas as pd
import numpy as np

counts = pd.read_csv('data/GSE217458/TMS_counts.csv')
annot = pd.read_csv('data/GSE217458/TMS_annotation.csv')

# Filter for miRBase-annotated miRNAs
mirnas = counts[counts['ncRNA'].str.contains('mmu-miR|mmu-let', case=False)]

# Define age groups
young_ages = [1, 3, 6]
old_ages = [21, 24, 27]
tissues = ['Heart', 'Kidney', 'Liver', 'Lung', 'Spleen', 'Skin']

for tissue in tissues:
    young_ids = annot[(annot['organ'] == tissue) & (annot['age'].isin(young_ages))]['sample_id']
    old_ids = annot[(annot['organ'] == tissue) & (annot['age'].isin(old_ages))]['sample_id']
    # ... compute means and fold changes
```
