# Human Aging Tissue miRNA-Seq Datasets
## Systematic Search for In Vivo Human Aging miRNA Data

*Search date: 2026-04-07*

---

## Key Finding

While large human miRNA-seq resources exist, **there is no large-scale human TISSUE small RNA-seq study specifically designed for aging** (i.e., young vs. old biopsies from the same organ with dedicated small RNA library prep). The closest resources are GTEx V10 (which includes small RNA-seq across ages 21-70 but was not designed as an aging study) and organ-specific small-N studies.

**No human liver or kidney aging miRNA-seq dataset exists** — a critical gap given that LNPs accumulate in liver.

---

## Tier 1: Large-Scale Resources

### GTEx V10 — Small RNA-seq Across 54 Human Tissues

| Parameter | Details |
|-----------|---------|
| **Repository** | dbGaP phs000424.v10.p1; [GTEx Portal](https://gtexportal.org/) |
| **Tissues** | ~54 tissue types (post-mortem) |
| **Age range** | 21-70 years (does NOT include very elderly >70) |
| **Method** | Small RNA-seq |
| **Samples** | **~16,760** small RNA-seq samples from ~1,000 donors |
| **Data access** | Open access expression matrices on GTEx Portal; controlled access individual-level data via AnVIL/dbGaP |
| **Citation** | GTEx Consortium, GTEx V10 release (2024) |

This is the single largest human small RNA-seq resource. Age-stratified analysis (e.g., 20-40 vs. 50-70) across tissues would provide the first comprehensive view of human tissue miRNA aging. However, the upper age limit of 70 means the most relevant aging biology (senescent cell accumulation, which accelerates after 70) is not captured.

**Priority for our project: VERY HIGH.** GTEx open-access expression matrices could be downloaded and analyzed immediately for our candidate miRNAs across human tissues and ages.

---

### miRNATissueAtlas 2025

| Parameter | Details |
|-----------|---------|
| **Repository** | [ccb.uni-saarland.de/tissueatlas2025](https://www.ccb.uni-saarland.de/tissueatlas2025) |
| **Coverage** | 74 organs, 373 tissues (human and mouse), 799 billion reads, 61,593 samples |
| **Method** | Uniformly reprocessed small RNA-seq meta-resource |
| **Citation** | *Nucleic Acids Research*. 2025;53(D1):D129 |

A comprehensive meta-resource rather than a primary dataset. Could be valuable for cross-referencing our candidates across tissues.

---

## Tier 2: Organ-Specific Human Aging miRNA-Seq

### GSE136930 — Human Right Atrial Tissue Aging

| Parameter | Details |
|-----------|---------|
| **GEO** | [GSE136930](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE136930) |
| **Tissue** | Right atrial appendage (cardiac surgery patients, sinus rhythm) |
| **Age groups** | 4 groups: 38-42, 48-52, 58-62, 68-72 years |
| **Method** | NEBNext Small RNA Library Prep, Illumina HiSeq2500, ~10M reads/sample |
| **Samples** | 12 (3 per age group) |
| **Key finding** | **miR-34a-5p upregulated with age** — validates our top ON-switch candidate in human cardiac tissue |
| **Citation** | Ma et al. *Front Physiol*. 2019. PMID: [31607954](https://pubmed.ncbi.nlm.nih.gov/31607954/) |

**This is the only human tissue aging small RNA-seq study that directly validates miR-34a-5p as age-upregulated.** The finding of miR-34a-5p increasing with age in human atrial tissue is consistent with all of our other datasets (WI-38, MRC-5, HUVEC, HAEC, mouse 16-tissue, mouse muscle, rat liver/kidney/lung/spleen).

---

### de Vries et al. (2019) — Human Bronchial Biopsy Aging

| Parameter | Details |
|-----------|---------|
| **Publication** | de Vries M et al. *Sci Rep*. 2019;9:3891. PMID: [30842487](https://pubmed.ncbi.nlm.nih.gov/30842487/) |
| **Tissue** | Bronchial biopsies |
| **Age range** | 18-73 years (86 healthy individuals) |
| **Method** | Small RNA-seq |
| **Data availability** | **NOT confirmed as publicly deposited.** GEO accession not found in publication. |
| **Key finding** | 27 age-related miRNAs. miR-146a-5p, miR-146b-5p, miR-142-5p LOWER with increasing age. |

Relevant finding: miR-146a-5p declines with age in human bronchial tissue — **opposite** of what we see in mouse aging tissues (UP 1.3-2.5x in GSE217458, GSE172269). This may reflect tissue-specific biology (airway vs. other organs) or species differences.

---

## Tier 3: Human Blood/Serum/Plasma Aging miRNA-Seq

### GSE53439 — HANDLS Study Serum miRNA-Seq

| Parameter | Details |
|-----------|---------|
| **GEO** | [GSE53439](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE53439) |
| **Sample type** | Serum |
| **Ages** | Young (~30 years) vs Old (~64 years) |
| **Samples** | 22 (11 young + 11 old) |
| **Method** | Illumina small RNA-seq |
| **Key findings** | miR-151a-5p, miR-181a-5p, miR-1248 significantly DECREASED with age |
| **Citation** | Noren Hooten et al. *Aging*. 2013. PMID: [24088671](https://pubmed.ncbi.nlm.nih.gov/24088671/) |

### Rotterdam Study — Plasma miRNA-Seq (Largest Human Cohort)

| Parameter | Details |
|-----------|---------|
| **Samples** | **2,684 participants** (median age 70.6 in main cohort) |
| **Method** | HTG EdgeSeq miRNA WTA, Illumina NextSeq 500 (targeted RNA-seq, 2,083 miRNAs) |
| **Data access** | Controlled access via Erasmus MC (not in public repositories) |
| **Key findings** | Composite miRNA aging biomarkers predict health outcomes and mortality |
| **Citation** | *Genome Medicine*. 2025 |

### Framingham Heart Study — Plasma exRNA

| Parameter | Details |
|-----------|---------|
| **Repository** | dbGaP phs000363; exRNA Atlas |
| **Samples** | 40 (small RNA-seq discovery) + 2,763 (qPCR validation) |
| **Key finding** | 159 miRNAs significantly decreased with age |
| **Citation** | Huan et al. *Nat Commun*. 2016 |

---

## Tier 4: Centenarian/Longevity Studies

### GSE32493 — Centenarian B-Cell miRNA-Seq

| Parameter | Details |
|-----------|---------|
| **GEO** | [GSE32493](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE32493) |
| **Sample type** | Purified B-cells from blood |
| **Ages** | **Centenarians (100+ years)** vs younger controls (Ashkenazi Jewish) |
| **Samples** | 6 (3 centenarians + 3 controls) |
| **Method** | Illumina massively parallel sequencing (26.7M total reads) |
| **Key findings** | 276 known miRNAs; 22 upregulated in centenarians; miR-363* declines with age but maintained in centenarians |
| **Citation** | Noren Hooten et al. *BMC Genomics*. 2012. PMID: [22838459](https://pubmed.ncbi.nlm.nih.gov/22838459/) |

Small dataset (n=3 per group) but the only small RNA-seq data from centenarians.

---

## Tier 5: Notable Datasets Using Microarray (Not Sequencing)

These are not usable for our count-based analyses but are referenced for completeness:

| Dataset | Tissue | Ages | N | Method | Key Finding |
|---------|--------|------|---|--------|-------------|
| Ludwig et al. 2020 | Whole blood | Wide | 4,393 | Microarray | Age > sex effect on miRNA; nonlinear changes |
| Drummond et al. 2011 | Muscle | 31 vs 73 yr | 36 | Microarray | miRNA aging in vastus lateralis |
| GSE72264 | Skin | <10 vs >60 yr | 12 | Microarray | Dermal tissue aging |
| Centenarian vs octogenarian | PBMCs | 80+ vs 100+ | Multiple | Microarray | Centenarian profile resembles young |

---

## Critical Gaps in Human Aging miRNA-Seq Data

1. **No human liver aging miRNA-seq dataset exists.** This is the most critical gap for LNP-based senolytic circuit design.
2. **No human kidney aging miRNA-seq dataset exists.**
3. **No human skin aging miRNA-seq dataset exists** (all published skin aging miRNA studies used microarrays).
4. **GTEx V10 caps at age 70** — the most relevant age range for senescent cell accumulation (>70) is not represented.
5. **Centenarian data is limited to 3 B-cell samples** (GSE32493). No centenarian tissue miRNA-seq exists.
6. **Most large cohort studies** (Rotterdam, Framingham) used controlled-access data that requires institutional agreements.

---

## Recommendations

1. **Download and analyze GTEx V10 open-access small RNA expression data** for our candidate miRNAs across human tissues stratified by age (21-40 vs 50-70). This is feasible immediately and would provide the first systematic view of our candidates in human tissue aging.
2. **GSE136930** (human cardiac aging) directly validates miR-34a-5p — should be cited in our synthesis as the only human tissue confirmation.
3. **GSE32493** (centenarian B-cells) is small but novel — worth analyzing to see if our candidates show patterns in extreme aging.

---

## References

1. GTEx Consortium. GTEx V10 release. 2024. [gtexportal.org](https://gtexportal.org/)
2. Ma et al. *Front Physiol*. 2019. PMID: 31607954
3. de Vries M et al. *Sci Rep*. 2019;9:3891. PMID: 30842487
4. Noren Hooten N et al. *Aging*. 2013. PMID: 24088671
5. Noren Hooten N et al. *BMC Genomics*. 2012. PMID: 22838459
6. Ludwig N et al. *Nat Commun*. 2020. (miRNA blood aging)
7. Huan T et al. *Nat Commun*. 2016. (Framingham exRNA)
