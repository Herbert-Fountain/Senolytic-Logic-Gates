# Chemotherapy Patient miRNA-Seq Datasets
## Systematic Search for Human In Vivo Therapy-Induced Senescence miRNA Data

*Search date: 2026-04-07*

---

## Key Finding

**Genuine small RNA-seq datasets with paired pre/post-chemotherapy blood samples from patients are extremely rare in public repositories.** Most chemotherapy-miRNA studies used microarrays or qPCR panels, not sequencing. Among those that used small RNA-seq, most did not deposit data publicly. This represents a significant gap in the field - there is effectively no publicly available small RNA-seq dataset capturing therapy-induced senescence in human patients in vivo.

---

## Tier 1: Small RNA-Seq with Longitudinal Pre/Post-Chemotherapy Design

### Mikulski, Fendler et al. (2024) - Autologous Stem Cell Transplantation Serum miRNA-seq

| Parameter | Details |
|-----------|---------|
| **Publication** | PMID: [38650024](https://pubmed.ncbi.nlm.nih.gov/38650024/) (2024). Earlier abstract: Blood 2021;138(Suppl 1):4789 |
| **Cancer types** | Multiple myeloma (n=4), Hodgkin lymphoma (n=3), non-Hodgkin lymphoma (n=3) |
| **Conditioning regimens** | Melphalan-200 (50.6%), reduced melphalan (20.8%), BeEAM (22.1%), BEAM (6.5%) |
| **Sample type** | Serum |
| **Method** | Illumina NextSeq 550, 75nt SE, ~10M reads/sample |
| **Timepoints** | 4: (T1) before conditioning, (T2) day of transplant, (T3) day +7, (T4) day +14 |
| **Sample sizes** | Discovery: 10 patients × 4 timepoints = 40 samples; Validation (qPCR): 67 patients |
| **Data availability** | **NOT in GEO.** Supplementary files only. |

**This is the single most relevant dataset for our project.** The conditioning regimens are extremely cytotoxic (myeloablative doses), which would induce massive therapy-induced senescence in surviving normal tissues. The 4-timepoint longitudinal design captures the kinetic response. However, the data is not publicly deposited - it would need to be requested from the corresponding author (Wojciech Fendler, Medical University of Lodz, Poland).

**Related findings from the same research group:**
- miR-122-5p and miR-125a-5p predict **hepatotoxicity** in ASCT patients (PMID: [38556255](https://pubmed.ncbi.nlm.nih.gov/38556255/)) - directly relevant to LNP liver tropism concern
- miR-223-3p predicts complete response in MM after ASCT (PMID: [37829335](https://pubmed.ncbi.nlm.nih.gov/37829335/))

---

### Ju, Jang et al. (2024) - FOLFOX Chemotherapy Neuropathy miRNA-seq

| Parameter | Details |
|-----------|---------|
| **Publication** | PMID: [38701955](https://pubmed.ncbi.nlm.nih.gov/38701955/) (Biochim Biophys Acta Mol Basis Dis, 2024) |
| **Cancer type** | Colorectal cancer |
| **Chemotherapy** | FOLFOX (5-FU/leucovorin/oxaliplatin) |
| **Sample type** | Plasma |
| **Design** | ≤3 cycles vs ≥6 cycles FOLFOX (cumulative exposure, not paired pre/post) |
| **Sample sizes** | 8 patients (sequencing), 27 patients (qPCR validation) |
| **Data availability** | Not confirmed as publicly deposited |
| **Key finding** | miR-3184-5p identified as biomarker for peripheral neuropathy |

---

## Tier 2: Chemotherapy-Induced Organ Damage miRNA-seq

### Anthracycline-Induced Liver Injury - Exosomal miRNA-seq

| Parameter | Details |
|-----------|---------|
| **Publication** | PMID: [32355577](https://pubmed.ncbi.nlm.nih.gov/32355577/) (PeerJ, 2020) |
| **Cancer type** | Postoperative breast cancer |
| **Chemotherapy** | Anthracycline-based adjuvant chemotherapy |
| **Sample type** | Serum exosomes |
| **Design** | Liver injury group vs non-liver injury group AFTER chemotherapy |
| **Key finding** | miR-1-3p identified as critical exosomal miRNA biomarker for anthracycline-induced liver injury |
| **Data availability** | NOT publicly deposited |

**Relevance:** Directly studies chemotherapy-induced hepatotoxicity (the LNP target organ) via exosomal miRNA. Senescence is implicated in anthracycline hepatotoxicity.

---

## Tier 3: Microarray/qPCR (NOT sequencing) But Highly Relevant Design

### GSE70754 - Breast Cancer NAC with 4-Timepoint Serum Design

| Parameter | Details |
|-----------|---------|
| **GEO Accession** | [GSE70754](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE70754) |
| **Method** | **Affymetrix Multispecies miRNA-2 Array** (microarray, NOT sequencing) |
| **Cancer type** | Locally advanced breast cancer |
| **Chemotherapy** | **Doxorubicin/cyclophosphamide** followed by docetaxel |
| **Sample type** | Tissue biopsies AND serum |
| **Timepoints** | 4: diagnosis, after 1st cycle AC, after 4th cycle AC, after 4th cycle docetaxel |
| **Citation** | PMID: [27064979](https://pubmed.ncbi.nlm.nih.gov/27064979/) |
| **Data availability** | YES - 35.5 MB XLSX on GEO |

**Although this is microarray data (not sequencing), the experimental design is exactly what we need:** paired serum samples from the same patients before and during doxorubicin/cyclophosphamide treatment. This is the closest thing to a human equivalent of our WI-38 doxorubicin senescence model. The microarray data cannot provide absolute counts but can identify miRNAs that change with chemotherapy, which we can cross-reference with our sequencing-based count data from in vitro studies.

---

## Tier 4: Reference Datasets (Cross-Sectional, No Treatment)

| GEO | Description | Relevance |
|-----|-------------|-----------|
| [GSE113994](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE113994) | Healthy plasma/serum small RNA reference (312 samples, 12 timepoints) | Normal temporal variation baseline |
| [GSE94533](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE94533) | Ovarian cancer serum miRNA-seq (179 samples) | Cancer patient serum reference |
| [GSE71008](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE71008) | Pan-cancer plasma exRNA (192 samples) | Cancer patient circulating miRNA reference |
| [GSE270497](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE270497) | Breast cancer screening plasma EV small RNA-seq (180 samples) | Plasma EV miRNA reference |

---

## Gaps Identified

**No publicly deposited small RNA-seq datasets exist for:**

1. **Childhood cancer survivors with accelerated aging** - Despite extensive epigenetic aging (DNA methylation clock) data from the CCSS and St. Jude LIFE cohorts, no small RNA-seq has been published.
2. **Chemotherapy-induced cardiotoxicity** - Only qPCR panel studies (miR-1, let-7f, miR-126)
3. **Cisplatin nephrotoxicity in patients** - Animal models exist but no human small RNA-seq
4. **Any therapy-induced senescence study with paired pre/post miRNA-seq and public data deposition**

---

## Implications

The absence of public small RNA-seq data from chemotherapy patients is both a gap and an opportunity:

1. **For our project:** We cannot directly validate our candidate miRNAs (miR-34a, miR-16, miR-155, etc.) in human in vivo chemotherapy-induced senescence using existing public data. The GSE70754 microarray data is the best available proxy for doxorubicin-treated patients.

2. **For the field:** The planned doxorubicin small RNA-seq experiment in mice and human primary fibroblasts would contribute important data. A future clinical study profiling serum miRNAs before and after chemotherapy (with modern small RNA-seq) would be highly impactful.

3. **Circulating miRNA ≠ intracellular miRNA:** Even if we had patient serum miRNA-seq data, it would reflect the circulating pool (secreted + EV-associated), not the intracellular pool that the circuit senses. The same inflammaging/cell-composition confounds we identified for bulk tissue would apply to serum - circulating miRNAs come from all cell types, and changes could reflect immune activation, tissue damage, or tumor response rather than senescence per se.

---

## References

1. Mikulski M, Fendler W et al. 2024. PMID: 38650024
2. Ju H, Jang Y et al. 2024. PMID: 38701955
3. Anthracycline liver injury exosomal miRNA. PeerJ. 2020. PMID: 32355577
4. NAC miRNA serum/tissue microarray. PMID: 27064979
5. ASCT hepatotoxicity miRNA prediction. PMID: 38556255
