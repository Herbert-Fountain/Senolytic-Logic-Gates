# Publicly Available Small RNA-seq Datasets: Aging miRNA Profiling
## Compiled for Natural Aging vs. Chemo-Induced Senescence Comparison

*Last updated: 2026-04-06*

---

## Purpose

To compare miRNA expression changes during natural aging (in vivo, mixed cell populations) with chemotherapy-induced senescence (in vitro, pure senescent populations). This comparison helps distinguish:
- **Universal aging/senescence miRNAs** — changed in both contexts
- **Senescence-specific miRNAs** — changed only in pure senescent cells, diluted in bulk tissue
- **Tissue aging miRNAs** — changed in aging tissue but driven by non-senescent cell composition shifts

---

## Tier 1: Highest Priority

### GSE217458 / GSE222857 — Body-Wide ncRNA Aging Atlas (16 Mouse Tissues)

**Citation:** Wagner V, Kern F, Hahn O, Schaum N, Ludwig N, Fehlmann T, Engel A, Henn D, Rishik S, Isakova A, Tan M, Sit R, Neff N, Hart M, Meese E, Quake S, Wyss-Coray T, Keller A. Characterizing expression changes in noncoding RNAs during aging and heterochronic parabiosis across mouse tissues. *Nature Biotechnology*. 2024;42:109-118.

**PMID:** [37106037](https://pubmed.ncbi.nlm.nih.gov/37106037/)
**DOI:** [10.1038/s41587-023-01751-6](https://doi.org/10.1038/s41587-023-01751-6)

| Parameter | Details |
|-----------|---------|
| Organism | *Mus musculus* (C57BL/6JN) |
| Tissues | 16: bone, brain, BAT, GAT, heart, kidney, limb muscle, liver, lung, bone marrow, MAT, pancreas, skin, small intestine, spleen, SCAT |
| Ages | 10 timepoints: 1, 3, 6, 9, 12, 15, 18, 21, 24, 27 months |
| Method | Small RNA-seq |
| Samples | 771 total (up to 6 replicates per tissue per timepoint) |
| Also includes | Plasma, plasma-derived EVs, heterochronic parabiosis rejuvenation |
| GEO | GSE217458, GSE222857 |
| Cohort | Tabula Muris Senis (TMS) |

**8 Broadly Deregulated miRNAs Across Tissues:**

| miRNA | Direction with Age | Notes |
|-------|-------------------|-------|
| miR-29a-3p | UP | ECM/secretion targets |
| miR-29c-3p | UP | Strongest pan-tissue aging correlation; reversed by parabiosis |
| miR-155-5p | UP | Immune/inflammatory |
| miR-184-3p | UP | Also reported UP in dox-induced senescence (Weigl 2024) |
| miR-1895 | UP | Mouse-specific, no human ortholog |
| miR-300-3p | DOWN | |
| miR-487b-3p | DOWN | |
| miR-541-5p | DOWN | |

**Why this matters:** Most comprehensive natural aging miRNA dataset. Overlaps our tissue panel (heart, kidney, liver, lung, spleen). The finding that aging trajectories are tissue-specific mirrors the senescence finding from Weigl 2024.

---

### GSE119661 — Mouse Tissue Atlas of Small Noncoding RNA (11 Tissues, Baseline)

**Citation:** Isakova A et al. A mouse tissue atlas of small noncoding RNA. *PNAS*. 2020;117(41):25634-25645.

| Parameter | Details |
|-----------|---------|
| Organism | *Mus musculus* (C57BL/6J) |
| Tissues | 11: brain, lung, heart, muscle, kidney, pancreas, liver, small intestine, spleen, bone marrow, testes |
| Ages | Adult only (not an aging comparison) |
| Method | Small RNA-seq |
| Samples | 140 libraries from 14 biological replicates (10 female, 4 male) |
| GEO | GSE119661 |

**Why this matters:** Establishes tissue-specific miRNA baseline expression. ~30% of small ncRNAs are tissue-specific. Essential reference for knowing what's "normal" in each tissue.

---

## Tier 2: Tissue-Specific Mouse Aging

### GSE55164 — Skeletal Muscle Aging miRNA-seq

**Citation:** Kim JY et al. Genome-wide profiling of the microRNA-mRNA regulatory network in skeletal muscle with aging. *Aging*. 2014;6(7):524-544.

| Parameter | Details |
|-----------|---------|
| Organism | Mouse (C57BL/6) |
| Tissue | Gastrocnemius muscle |
| Ages | 6 months vs 24 months |
| Method | miRNA-seq |
| Samples | n=5 per age group |
| Companion | GSE55163 (mRNA-seq) |
| GEO | GSE55164 |

**Key findings:** 34 DE miRNAs (15 up, 19 down). miR-206 and miR-434 confirmed. 8 miRNAs in the Dlk1-Dio3 locus coordinately downregulated.

---

### GSE124087 — Mouse Heart Aging RNA-seq

**Citation:** Hasanpourghadi M et al. Dichotomy between the transcriptomic landscape of naturally versus accelerated aged murine hearts. *Scientific Reports*. 2020.

| Parameter | Details |
|-----------|---------|
| Organism | Mouse |
| Tissue | Heart |
| Ages | 12, 52, 104 weeks (natural aging); plus Ercc1 KO, Tert KO, Hq models |
| Method | Total RNA-seq (includes ncRNA) |
| GEO | GSE124087 |

**Key finding:** No dramatic transcriptome changes in naturally aged hearts until 2 years, in contrast to accelerated aging models.

---

## Tier 3: Circulating miRNA Aging

### Mouse Serum miRNA Aging + Calorie Restriction

**Citation:** Dhahbi JM et al. Deep sequencing identifies circulating mouse miRNAs that are functionally implicated in manifestations of aging and responsive to calorie restriction. *Aging*. 2013;5(2):130-141.

| Parameter | Details |
|-----------|---------|
| Organism | Mouse |
| Source | Serum (circulating miRNAs) |
| Ages | 7 months (young) vs 27 months (old) vs 27 months + CR |
| Method | Small RNA-seq (Illumina, 50 nt reads) |
| Samples | n=3 per group (9 total) |

**Key finding:** Many circulating miRNAs increase with age; calorie restriction antagonizes these increases.

---

## Tier 4: Human Aging

### EGAS00001008117 — Rotterdam Study Plasma miRNA Aging

**Citation:** Plasma microRNA signatures of aging and their links to health outcomes and mortality. *Genome Medicine*. 2025.

| Parameter | Details |
|-----------|---------|
| Organism | Human |
| Source | Plasma |
| Ages | Continuous (median 53.5-70.6 years) |
| Method | Targeted RNA-seq (2,083 miRNAs) |
| Samples | n=2,684 participants |
| Repository | EGA: EGAS00001008117 |

**Key finding:** 591 well-expressed plasma miRNAs. Composite miRNA aging biomarkers predict health outcomes and mortality.

---

### GSE32493 — Human Centenarian B-Cell miRNA-seq

**Citation:** Serna E et al. Comprehensive microRNA profiling in B-cells of human centenarians by massively parallel sequencing. *BMC Genomics*. 2012;13:353.

| Parameter | Details |
|-----------|---------|
| Organism | Human |
| Source | B-cells (peripheral blood) |
| Ages | Ashkenazi Jewish centenarians vs younger controls |
| Method | miRNA-seq (26.7 million reads) |
| Samples | n=3 centenarians + n=3 controls |
| GEO | GSE32493 |

**Key finding:** 22 miRNAs upregulated in centenarians. miR-363 declines with age but maintained in centenarians.

---

## Tier 5: Cross-Species Reference

### GSE172269 — Rat miRNA-seq BodyMap (11 Organs, 4 Ages, 2 Sexes)

**Citation:** Bushel PR et al. Comprehensive microRNA-seq transcriptomic profiling across 11 organs, 4 ages, and 2 sexes of Fischer 344 rats. *Scientific Data*. 2022;9:252.

| Parameter | Details |
|-----------|---------|
| Organism | Rat (Fischer 344) |
| Tissues | 11: adrenal, brain, heart, kidney, liver, lung, muscle, spleen, testis, thymus, uterus |
| Ages | 4 groups: juvenile, adolescent, adult, aged |
| Method | Small RNA-seq (Illumina TruSeq, 50bp SE) |
| Samples | 320 (4 replicates per group); 1.6 billion total reads |
| GEO | GSE172269 |

**Key finding:** 604 of 764 annotated rat miRNAs quantified. 12 novel organ-enriched miRNA candidates.

---

## Cross-Dataset miRNA Comparison

miRNAs recurring across multiple aging datasets — candidates for comparison with chemo-induced senescence:

| miRNA | Natural Aging | In Vitro Senescence | In Vivo Dox Senescence | EV/Circulating |
|-------|--------------|--------------------|-----------------------|---------------|
| miR-29c-3p | UP (strongest pan-tissue) | Not reported | Unknown | UP in plasma/EVs |
| miR-29a-3p | UP (pan-tissue) | Not reported | Unknown | UP |
| miR-34a-5p | Mixed | UP (multiple studies) | Unknown | UP |
| miR-21-5p | UP (skin) | UP (HUVECs, 2.6x) | Unknown | UP |
| miR-155-5p | UP (pan-tissue) | Not reported | Unknown | Mixed |
| miR-184-3p | UP (pan-tissue) | Not reported | UP (Weigl 2024, dox) | Unknown |
| miR-206 | DOWN (muscle) | Not reported | Unknown | Changed in EVs |
| miR-143-3p | Unknown | Unknown | Unknown | UP in aging EVs |
| miR-122-5p | Liver-specific | DOWN in kidney (our data) | Unknown | UP in aging EVs |
| miR-146a | Mixed | UP (fibroblasts) | Unknown | Unknown |

**Key observation:** miR-184-3p appears in both the natural aging pan-tissue signature (Wagner 2024) AND doxorubicin-induced senescence (Weigl 2024). This makes it a high-priority candidate for further investigation, despite having very low counts in HUVECs. It may be expressed at higher levels in other cell types.

---

## Recommended Analysis Plan

1. **Download GSE217458/GSE222857** count data for heart, kidney, liver, lung, spleen, skin (overlapping with our tissue pilot data)
2. **Extract expression of senescence candidate miRNAs** across ages — do they change with natural aging in the same direction as in vitro senescence?
3. **Identify miRNAs that are UP in aging across tissues** but have LOW baseline expression in young tissue — these would be ideal ON-switch candidates
4. **Compare with Herbert's future dox small RNA-seq data** when available
5. **Cross-reference with rat BodyMap** (GSE172269) for conservation validation

---

## References

1. Wagner V et al. *Nat Biotechnol*. 2024;42:109-118. DOI: 10.1038/s41587-023-01751-6
2. Isakova A et al. *PNAS*. 2020;117(41):25634-25645
3. Kim JY et al. *Aging*. 2014;6(7):524-544
4. Hasanpourghadi M et al. *Sci Rep*. 2020
5. Dhahbi JM et al. *Aging*. 2013;5(2):130-141
6. Bushel PR et al. *Sci Data*. 2022;9:252
7. Serna E et al. *BMC Genomics*. 2012;13:353
8. Plasma miRNA signatures of aging. *Genome Med*. 2025
