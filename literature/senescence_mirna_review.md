# Senescence-Associated miRNA Expression Studies
## Literature Review for Senolytic Circuit miRNA Input Selection

*Compiled for the Senolytic RNA Logic Gate Project*
*Last updated: 2026-04-06*

---

## 1. Overview

This review surveys the literature on miRNA expression changes during cellular senescence, with emphasis on:
- Studies using **doxorubicin** as the senescence inducer (matching our planned experiments)
- Studies employing **small RNA-seq** (providing genome-wide, quantitative miRNA profiling)
- Studies with **raw data deposited** in public repositories (GEO/SRA) enabling independent re-analysis
- Studies reporting **absolute expression levels** (counts, TPM, RPM) rather than only fold changes

The goal is to identify candidate miRNAs for use as ON-switch inputs (upregulated in senescence) and OFF-switch/de-targeting elements (downregulated in senescence / high in healthy tissue) in synthetic mRNA logic gate circuits for selective senolytic therapy.

**Critical note on data quality:** For circuit design, absolute intracellular miRNA abundance matters more than fold change. A miRNA that increases 100-fold from 1 to 100 copies per cell may be less useful as a switch input than one that increases 3-fold from 10,000 to 30,000 copies. Most published studies report only fold changes, which is insufficient for our purposes. Studies with deposited raw data are prioritized because we can re-analyze them to extract absolute count information.

---

## 2. Tier 1: Highest Priority Studies

### 2.1 Weigl, Grillari et al. (2024) — Doxorubicin-Induced Senescence Across 5 Human Cell Types

**Citation:** Weigl M, Krammer TL, Pultar M, Wieser M, Chaib S, Suda M, Diendorfer A, Khamina-Kotisch K, Giorgadze N, Pirtskhalava T, Johnson KO, Inman CL, Xue A, Lammermann I, Meixner B, Wang L, Xu M, Grillari R, Ogrodnik M, Tchkonia T, Hackl M, Kirkland JL, Grillari J. Profiling microRNA expression during senescence and aging: mining for a diagnostic tool of senescent-cell burden. *bioRxiv*. 2024.

**DOI:** [10.1101/2024.04.10.588794](https://doi.org/10.1101/2024.04.10.588794)

**Status:** Preprint (bioRxiv), version 2 available.

**Senescence Inducer:** Doxorubicin

**Cell Types (all human primary):**
1. Skin fibroblasts (dermal fibroblasts)
2. Microvascular endothelial cells (HMVEC)
3. Umbilical vein endothelial cells (HUVEC)
4. Renal proximal tubular epithelial cells
5. Adipose-derived mesenchymal stem cells

**In Vivo Component:**
- Mouse tissues (7 tissues) from young vs. 25-month-old mice
- Plasma and plasma-derived extracellular vesicles (EVs) from aged mice
- Transgenic p21-high senescent cell clearance model on high-fat diet (HFD)

**Method:** Small RNA-seq and mRNA-seq (both transcriptomics layers)

**Raw Data:** GEO accession not confirmed from preprint search — **must check data availability section of full preprint**. The Grillari/Hackl laboratory (TAmiRNA GmbH) has a strong track record of data deposition.

**Expression Data Format:** Likely normalized counts from small RNA-seq pipeline (to be confirmed).

**Key miRNAs Identified:**
- **Commonly upregulated across multiple cell types:** miR-215-5p, miR-184
- **22 candidate "senomiRs"** identified as potential circulating biomarkers of senescent cell burden

**Critical Finding for Our Project:** miRNA expression changes during senescence are **highly cell-type specific**. The majority of regulated miRNAs were unique to individual cell types, with very few showing consistent changes across all 5 types. This has profound implications for the goal of building a tissue-agnostic senolytic circuit — it may not be possible to identify a single miRNA input that reliably distinguishes senescent from non-senescent cells across all tissue contexts.

**Sample Sizes:** 5 cell types × 2 conditions (senescent vs. control); exact replicate numbers to be confirmed from full paper.

**Priority:** **HIGHEST.** This is the single most relevant study for our project — doxorubicin inducer, small RNA-seq, multiple human primary cell types, systematic approach. Should attempt to obtain raw data or contact authors.

---

### 2.2 Devrukhkar et al. (2024/2025) — Doxorubicin-Induced Senescence in Human Ovary

**Citation:** Devrukhkar A et al. A Comprehensive Multiomics Signature of Doxorubicin-Induced Cellular Senescence in the Postmenopausal Human Ovary. *Aging Cell*. 2025.

**DOI (preprint):** [10.1101/2024.10.02.616143](https://doi.org/10.1101/2024.10.02.616143)
**DOI (published):** [10.1111/acel.70111](https://doi.org/10.1111/acel.70111)

**Senescence Inducer:** Doxorubicin (24h treatment)

**Cell/Tissue Type:** Human postmenopausal ovarian cortex and medulla explants, cultured up to 10 days in doxorubicin-free medium post-treatment.

**Method:** Multi-omics (transcriptomics + proteomics). Whether small RNA-seq was specifically included is unclear.

**Raw Data:** Not confirmed from search results. Check published paper.

**Key Findings:**
- Distinct senescence profiles for cortex vs. medulla
- 120 common SASP proteins identified
- 26 shared transcriptomic/proteomic markers defining a "senotype"

**Priority:** MEDIUM. Tissue-level (not pure cell populations) and may not include miRNA-specific profiling. However, the doxorubicin inducer and human tissue context are relevant.

---

## 3. Tier 2: Important Studies with Deposited Small RNA-Seq Data

### 3.1 Dhahbi et al. (2011) — Replicative Senescence, IMR90 Fibroblasts

**Citation:** Dhahbi JM, Atamna H, Boffelli D, Magis W, Spindler SR, Martin DIK. Deep Sequencing Reveals Novel MicroRNAs and Regulation of MicroRNA Expression during Cell Senescence. *PLoS ONE*. 2011;6(5):e20509.

**PMID:** [21637828](https://pubmed.ncbi.nlm.nih.gov/21637828/)
**PMC:** [PMC3102725](https://pmc.ncbi.nlm.nih.gov/articles/PMC3102725/)

**Senescence Inducer:** Replicative exhaustion (passaging to growth arrest)

**Cell Type:** IMR90 human fetal lung fibroblasts (diploid, non-transformed)

**Method:** Illumina small RNA deep sequencing (Genome Analyzer IIx). miRDeep2 pipeline for analysis.

**Raw Data:** **GEO accession: GSE27404** ✓ CONFIRMED

**Expression Data Format:** Absolute read counts. 11.4 million reads (young, passage ~30) and 9.1 million reads (senescent, passage ~55). 452 known miRNAs detected; 272 differentially expressed.

**Key miRNAs:** Detailed lists in Supplementary Tables S2 (known miRNAs with read counts) and S4 (novel miRNAs). Specific names not fully extracted — need to download supplementary data.

**Sample Sizes:** n=1 per condition (young vs. senescent). **This is a major limitation** — no biological replicates for statistical analysis.

**Priority:** HIGH for data availability (confirmed GEO deposit with raw counts), LOW for statistical rigor (n=1). Useful as a reference but insufficient alone for circuit design decisions.

---

### 3.2 Terlecki-Zaniewicz et al. (2018) — Replicative Senescence, HUVECs

**Citation:** Terlecki-Zaniewicz L et al. MicroRNAs mediate the senescence-associated decline of NRF2 in endothelial cells. *Redox Biology*. 2018;18:77-83.

**PMC:** [PMC6037909](https://pmc.ncbi.nlm.nih.gov/articles/PMC6037909/)

**Senescence Inducer:** Replicative senescence (young vs. old passage)

**Cell Type:** Human umbilical vein endothelial cells (HUVECs)

**Method:** Small RNA-seq (miRNA-seq)

**Raw Data:** **GEO accession: GSE94410** ✓ CONFIRMED

**Expression Data Format:** Sequencing counts-based (specific normalization to be confirmed from data).

**Key miRNAs:**
- **Upregulated with senescence:** miR-34a-5p (used as senescence marker), miR-21, miR-217, miR-34a, miR-181a
- These miRNAs **directly target NRF2 mRNA**, linking senescence-associated miRNA changes to oxidative stress response decline.

**Sample Sizes:** To be confirmed from GEO.

**Priority:** HIGH. Same lab group as the Weigl 2024 study. Raw data confirmed deposited. Endothelial cell focus relevant for vascular senescence context.

---

### 3.3 Terlecki-Zaniewicz et al. (2018/2019) — SASP Extracellular Vesicle miRNA Cargo

**Citation:** Terlecki-Zaniewicz L, Lammermann I, Latreille J, Bobbili MR, Pils V, Schosserer M, Weinmullner R, Dellago H, Skalicky S, Pum D, Higareda Almaraz JC, Scheideler M, Morizot F, Hackl M, Gruber F, Grillari J. Small extracellular vesicles and their miRNA cargo are anti-apoptotic members of the senescence-associated secretory phenotype. *Aging*. 2018;10(5):1103-1132.

**PMID:** [29779019](https://pubmed.ncbi.nlm.nih.gov/29779019/)
**PMC:** [PMC5990398](https://pmc.ncbi.nlm.nih.gov/articles/PMC5990398/)

**Senescence Inducer:** Stress-induced premature senescence (SIPS) — UVB irradiation and mitomycin C; also quiescence controls

**Cell Type:** Human dermal fibroblasts (HDF), three different donor strains

**Method:** Small RNA-NGS (next-generation sequencing). Average 17.6 million reads per sample; 432 miRNAs detected at ≥5 TPM in at least one donor. 752 miRNAs screened, 375 selected for analysis.

**Raw Data:** GEO accession not confirmed. Check published paper supplementary materials.

**Expression Data Format:** **Tags per million (TPM)** — this is absolute quantification and directly usable for expression level comparisons.

**Key Findings — Intracellular vs. Extracellular:**
This study is **uniquely valuable** because it separately profiled intracellular and small extracellular vesicle (sEV) miRNA pools:

- **Four-fold increase** in sEV secretion from senescent cells compared to quiescent controls.
- **>80%** of miRNA cargo species were increased in senescent cell sEVs.
- **Selectively RETAINED intracellularly** in senescent cells (NOT packaged into sEVs):
  - **miR-21-3p**
  - **miR-17-3p**
- **Selectively PACKAGED into senescent sEVs** (depleted intracellularly):
  - **miR-15b-5p**
  - **miR-30a-3p**

**Why This Matters for Circuit Design:** Our therapeutic circuit senses **intracellular** miRNA levels, not extracellular/secreted levels. A miRNA that is upregulated in total cellular extracts but actively secreted via EVs may have lower intracellular concentration than expected. Conversely, miRNAs that are selectively retained (miR-21-3p, miR-17-3p) accumulate at high intracellular levels in senescent cells, making them strong ON-switch candidates.

**Sample Sizes:** 3 HDF strains, 2 conditions (SIPS, quiescence), 2 timepoints (D7, D21).

**Priority:** **VERY HIGH** for the intracellular vs. secreted miRNA distinction, which is critical for circuit design. The TPM data format is ideal. Limitation: SIPS inducer (not doxorubicin).

---

## 4. Tier 3: Supporting Studies (Microarray/qPCR, Important for Candidate Lists)

### 4.1 Yang et al. (2012) — Doxorubicin-Induced Senescence, K562

**Citation:** Yang MY, Lin PM, Liu YC, Hsiao HH, Yang WC, Hsu JF, et al. Induction of Cellular Senescence by Doxorubicin Is Associated with Upregulated miR-375 and Induction of Autophagy in K562 Cells. *PLoS ONE*. 2012;7(5):e37205.

**PMID:** [22606351](https://pubmed.ncbi.nlm.nih.gov/22606351/)
**PMC:** [PMC3350486](https://pmc.ncbi.nlm.nih.gov/articles/PMC3350486/)

**Senescence Inducer:** Doxorubicin (50 nM, 4 days)

**Cell Type:** K562 human chronic myelogenous leukemia cells (p53-null, p16-null)

**Method:** TaqMan MicroRNA microarray (667 human miRNAs). Validation by qRT-PCR.

**Raw Data:** Not deposited (microarray data likely in supplementary tables only).

**Key miRNAs Upregulated (≥4-fold in doxorubicin-treated vs. untreated):**
- **miR-375** (strongest upregulation)
- **miR-652**
- **miR-22**
- **miR-139-5p**
- 10 total upregulated miRNAs (≥4-fold)

**Key miRNAs Downregulated:** Not specifically listed in search results.

**Functional Validation:** miR-375 overexpression induced autophagy in K562 cells. Knockdown of miR-375 partially rescued doxorubicin-induced senescence.

**Sample Sizes:** 3 independent experiments.

**Limitations:**
- Cancer cell line (K562), not primary cells — p53 and p16 are null, so the senescence pathway is atypical
- Microarray, not sequencing — limited dynamic range and no novel miRNA discovery
- No raw data deposited
- Fold changes only, no absolute expression levels

**Priority:** LOW for data quality, MODERATE for being one of the few doxorubicin-specific studies with miRNA profiling.

---

### 4.2 Faraonio et al. (2012) — Multiple Senescence Inducers, IMR90

**Citation:** Faraonio R, Salerno P, Passaro F, Sedia C, Iaccio A, Nassa G, et al. A set of miRNAs participates in the cellular senescence program in human diploid fibroblasts. *Cell Death & Differentiation*. 2012;19(4):616-624.

**PMID:** [22052189](https://pubmed.ncbi.nlm.nih.gov/22052189/)
**PMC:** [PMC3307984](https://pmc.ncbi.nlm.nih.gov/articles/PMC3307984/)

**Senescence Inducers (compared):**
1. Replicative exhaustion
2. Etoposide (DNA damage)
3. Diethylmaleate (oxidative stress)

**Cell Type:** IMR90 human diploid fibroblasts

**Method:** Microarray + qRT-PCR validation

**Key Findings:**
- 14 miRNAs upregulated (>2-fold) and 10 downregulated (>2-fold) in senescent vs. young cells.
- **4 downregulated miRNAs were from the miR-17 family** — consistent with the Terlecki-Zaniewicz finding of miR-17-3p being retained intracellularly in senescent cells (the -3p strand accumulates because the -5p strand processing/activity changes).
- **7 upregulated miRNAs were functionally validated**: their overexpression was sufficient to induce SA-β-gal activity and senescence-associated heterochromatin foci (SAHF).
- Importantly, some miRNAs were specific to certain inducers, while others were shared — providing evidence for both universal and inducer-specific components of the senescence miRNA program.

**Sample Sizes:** Not confirmed.

**Priority:** MODERATE. The cross-inducer comparison is valuable for identifying universal senescence miRNAs. Limitation: microarray data, no raw sequencing.

---

### 4.3 Bonifacio & Jarstfer (2010) — Replicative Senescence, BJ Fibroblasts

**Citation:** Bonifacio LN, Jarstfer MB. MiRNA Profile Associated with Replicative Senescence, Extended Cell Culture, and Ectopic Telomerase Expression in Human Foreskin Fibroblasts. *PLoS ONE*. 2010;5(9):e12519.

**PMID:** [20824140](https://pubmed.ncbi.nlm.nih.gov/20824140/)

**Senescence Inducer:** Replicative senescence

**Cell Type:** BJ human foreskin fibroblasts (wild type and BJ-hTERT)

**Method:** Microarray (83 miRNAs changed by >1 SD)

**Key miRNAs:**
- **miR-143** functionally validated (induces growth arrest)
- **miR-146a** confirmed role in SASP regulation (targets IRAK1, modulating IL-6 and IL-8 secretion)

**Priority:** LOW. Early microarray study, useful for cross-referencing candidate lists.

---

### 4.4 Santiago et al. (2024) — miR-96-5p Sufficient to Induce Senescence

**Citation:** Santiago FE, Adige T, Mahmud S, Dong X, Niedernhofer LJ, Robbins PD. miR-96-5p expression is sufficient to induce and maintain the senescent cell fate in the absence of stress. *Proceedings of the National Academy of Sciences*. 2024;121(40):e2321182121.

**DOI:** [10.1073/pnas.2321182121](https://doi.org/10.1073/pnas.2321182121)

**Cell Type:** IMR-90 human fibroblasts

**Method:** Lentiviral overexpression of miR-96-5p; likely RNA-seq for transcriptomic analysis. Source data deposited on Mendeley Data.

**Key Finding:** **miR-96-5p overexpression alone is sufficient to induce and maintain senescence**, producing all hallmarks including:
- SA-β-gal activity
- Genome-wide heterochromatin changes
- Epigenetic activation of p16INK4a, p21CIP1, and SASP genes

**Why This Matters:** If a single miRNA can drive the entire senescence program, it may be a reliable sensor for detecting the senescent state. However, causality ≠ biomarker — miR-96-5p being sufficient to induce senescence doesn't guarantee it's always upregulated in all forms of senescence. Need to check its expression levels in doxorubicin-induced and other senescence models.

**Priority:** MODERATE-HIGH. Important mechanistic finding, but need quantitative expression data from senescence models (not just overexpression).

---

### 4.5 Henriques et al. (2023) — Therapy-Induced Senescence in Melanoma

**Citation:** Henriques V et al. A multi-omics integrative approach unravels novel genes and pathways associated with senescence escape after targeted therapy in NRAS mutant melanoma. *Cancer Gene Therapy*. 2023.

**PMC:** [PMC10581906](https://pmc.ncbi.nlm.nih.gov/articles/PMC10581906/)

**Senescence Inducer:** CDK4/6 + MEK inhibitor combination (therapy-induced senescence), 33-day treatment course

**Cell Type:** Three NRAS-mutant human melanoma cell lines (SKMEL30, IPC298, others)

**Method:** Total RNA-seq, small RNA-seq, qCLASH (crosslinking and sequencing of hybrids), kinome profiling — comprehensive multi-omics.

**Raw Data:** Not confirmed. Check paper.

**Key miRNAs:**
- **miR-211-5p** upregulated in resistant/proliferative cells (not in senescent cells)
- The qCLASH method identifies **direct miRNA-mRNA interactions** experimentally, which is valuable for validating circuit target predictions.

**Priority:** MODERATE. Therapy-induced senescence is relevant, but the inducer (CDK4/6i + MEKi) differs from doxorubicin. The qCLASH methodology is noteworthy.

---

## 5. Tier 4: Reference Datasets (mRNA-seq, Not miRNA-Specific)

### 5.1 Casella et al. (2019) — Transcriptome Signature of Cellular Senescence

**Citation:** Casella G, Munk R, Kim KM, Piao Y, De S, Abdelmohsen K, Gorospe M. Transcriptome signature of cellular senescence. *Nucleic Acids Research*. 2019;47(14):7294-7305.

**PMID:** [31251810](https://pubmed.ncbi.nlm.nih.gov/31251810/)
**PMC:** [PMC6698740](https://pmc.ncbi.nlm.nih.gov/articles/PMC6698740/)

**Senescence Inducers (8 models):**
1. Replicative exhaustion (WI-38, IMR-90)
2. Ionizing radiation (WI-38, IMR-90)
3. **Doxorubicin** (2 μg/mL, 24h) (WI-38, IMR-90)
4. Oncogene-induced (HRAS-G12V) (WI-38, IMR-90)
5. Replicative (HUVEC, HAEC)

**Cell Types:** WI-38 fibroblasts, IMR-90 fibroblasts, HUVEC endothelial cells, HAEC endothelial cells

**Method:** **mRNA RNA-seq** (NOT small RNA-seq)

**Raw Data:** **GEO: GSE130727** ✓ CONFIRMED

**Key Findings:**
- 50 RNAs consistently elevated and 18 consistently reduced across ALL senescence models
- lncRNA PURPL among most elevated across all models
- Provides a "core transcriptome signature" of senescence independent of cell type or inducer

**Why This Matters:** While this is mRNA-seq (not miRNA), the same samples/conditions could be paired with miRNA-seq data. The GEO dataset with doxorubicin conditions is valuable as a companion reference. Also useful for validating that TargetScan-predicted miRNA targets show expected mRNA changes in senescence.

**Priority:** MODERATE. Not directly usable for miRNA selection, but important reference for the same experimental conditions.

---

## 6. Databases and Resources

### 6.1 HAGR / CellAge Database
- **URL:** https://genomics.senescence.info/
- **CellAge:** 866 genes associated with cellular senescence + 1,259 differentially expressed genes from meta-analysis
- **URL:** https://genomics.senescence.info/cells/
- **Note:** Focuses on protein-coding genes, NOT miRNAs. No dedicated miRNA senescence database found within HAGR.

### 6.2 miRBase
- **URL:** https://www.mirbase.org/
- Standard reference for miRNA nomenclature and sequences.
- Not senescence-specific but essential for ID mapping and sequence retrieval.

### 6.3 No Dedicated Senescence miRNA Database Exists
The closest resource is the review by Munk et al. (2017, PMID: [28838538](https://pubmed.ncbi.nlm.nih.gov/28838538/)) which provides curated tables of senescence-associated miRNAs organized by pathway:
- Table 1: miRNAs in the p53 pathway
- Table 2: miRNAs in the p16INK4a pathway

---

## 7. Consolidated miRNA Candidate Table

| miRNA | Direction in Senescence | # Studies | Inducers | Cell Types | Intracellular? | Notes |
|-------|------------------------|-----------|----------|------------|---------------|-------|
| **miR-34a-5p** | UP | 3+ | Replicative, SIPS | HUVECs, IMR90, HDFs | Yes | Targets SIRT1; established marker |
| **miR-21-3p** | UP (intracellular) | 2 | SIPS | HDFs | **Yes — retained** | NOT secreted via EVs; ideal for intracellular sensing |
| **miR-22** | UP | 2+ | Doxorubicin, replicative | K562, IMR90 | Presumed | Targets SIRT1; dox-relevant |
| **miR-146a/b** | UP | 3+ | Replicative, various | BJ, IMR90, HDFs | Yes | SASP regulator (IRAK1) |
| **miR-215-5p** | UP | 1 | **Doxorubicin** | 5 human cell types | Unknown | Common across cell types (Weigl 2024) |
| **miR-184** | UP | 1 | **Doxorubicin** | 5 human cell types | Unknown | Common across cell types (Weigl 2024) |
| **miR-375** | UP | 1 | **Doxorubicin** | K562 | Unknown | Strongest in dox-induced K562 |
| **miR-96-5p** | UP | 1 | (overexpression) | IMR-90 | Unknown | Sufficient alone to induce senescence |
| **miR-181a** | UP | 2+ | Replicative | HUVECs, various | Yes | Targets SIRT1 |
| **miR-217** | UP | 1+ | Replicative | HUVECs | Unknown | Targets SIRT1 |
| **miR-17 family** | DOWN | 2+ | Replicative, SIPS | IMR90, HDFs | **miR-17-3p retained** | Potential OFF-switch candidate |
| **miR-15b-5p** | UP (secreted) | 1 | SIPS | HDFs | **No — secreted via EVs** | Poor ON-switch candidate |
| **miR-30a-3p** | UP (secreted) | 1 | SIPS | HDFs | **No — secreted via EVs** | Poor ON-switch candidate |
| **miR-199a-3p** | DOWN | 1 | Dox (cardiotoxicity) | Cardiac | Unknown | Targets GATA4; anti-senescent |

---

## 8. Key Gaps and Recommendations

### 8.1 Data Gaps
1. **No single study provides everything we need:** doxorubicin inducer + multiple cell types + small RNA-seq + absolute counts + deposited raw data. The Weigl/Grillari 2024 study comes closest but is a preprint with unconfirmed data availability.
2. **Intracellular vs. secreted distinction** is available from only one study (Terlecki-Zaniewicz 2019) and uses SIPS, not doxorubicin.
3. **No mouse in vivo doxorubicin senescence miRNA-seq study found.** Herbert's planned experiment would be the first.

### 8.2 Recommended Actions
1. **Obtain Weigl/Grillari 2024 raw data** — contact authors if not deposited. This is the single most impactful dataset for our project.
2. **Download and re-analyze GSE27404** (Dhahbi, replicative senescence, IMR90) and **GSE94410** (Terlecki-Zaniewicz, replicative senescence, HUVECs) to establish baseline count data.
3. **Herbert's doxorubicin small RNA-seq experiment is essential** and should be prioritized. The literature alone is insufficient for confident circuit design.
4. **Consider aging databases and bulk tissue aging studies** as supplementary data, keeping in mind that aging ≠ senescence (aged tissue contains a mix of senescent and non-senescent cells).

### 8.3 Strongest ON-Switch Candidates (Current Evidence)
Based on cross-study support, intracellular retention, and mechanistic plausibility:

1. **miR-21-3p** — upregulated in senescence AND selectively retained intracellularly (not secreted via EVs). Strongest candidate for intracellular sensing.
2. **miR-34a-5p** — most consistently reported across studies and senescence types. Established marker.
3. **miR-215-5p** — upregulated across 5 cell types in doxorubicin-specific senescence (Weigl 2024), but only one study.

### 8.4 Potential OFF-Switch / De-Targeting Candidates
- **miR-17 family members** — downregulated in senescence across multiple studies. If these are highly expressed in healthy cells and low in senescent cells, they could serve as de-targeting elements.

---

## References

1. Weigl M et al. bioRxiv. 2024. DOI: 10.1101/2024.04.10.588794
2. Devrukhkar A et al. Aging Cell. 2025. DOI: 10.1111/acel.70111
3. Dhahbi JM et al. PLoS ONE. 2011;6(5):e20509. PMID: 21637828
4. Terlecki-Zaniewicz L et al. Redox Biology. 2018;18:77-83. PMC: PMC6037909
5. Terlecki-Zaniewicz L et al. Aging. 2018;10(5):1103-1132. PMID: 29779019
6. Yang MY et al. PLoS ONE. 2012;7(5):e37205. PMID: 22606351
7. Faraonio R et al. Cell Death Differ. 2012;19(4):616-624. PMID: 22052189
8. Bonifacio LN, Jarstfer MB. PLoS ONE. 2010;5(9):e12519. PMID: 20824140
9. Santiago FE et al. PNAS. 2024;121(40):e2321182121
10. Henriques V et al. Cancer Gene Ther. 2023. PMC: PMC10581906
11. Casella G et al. Nucleic Acids Res. 2019;47(14):7294-7305. PMID: 31251810
12. Munk R et al. Int J Mol Sci. 2017. PMID: 28838538


---

## ADDENDUM: Natural Aging miRNA Datasets (Added 2026-04-06)

### Wagner et al. (2024) — Body-Wide ncRNA Aging Map (16 Mouse Tissues)

**Citation:** Wagner V, Kern F, Hahn O, Schaum N, Ludwig N, Fehlmann T, Engel A, Henn D, Rishik S, Isakova A, Tan M, Sit R, Neff N, Hart M, Meese E, Quake S, Wyss-Coray T, Keller A. Characterizing expression changes in noncoding RNAs during aging and heterochronic parabiosis across mouse tissues. *Nature Biotechnology*. 2024;42:109-118.

**PMID:** [37106037](https://pubmed.ncbi.nlm.nih.gov/37106037/)
**DOI:** 10.1038/s41587-023-01751-6
**PMC:** [PMC10791587](https://pmc.ncbi.nlm.nih.gov/articles/PMC10791587/)

**GEO Accessions:** GSE217458, GSE222857

**Organism:** *Mus musculus*

**Tissues (16):** Bone (femur/tibia), brain (hemibrain), brown adipose tissue (BAT), gonadal adipose tissue (GAT), heart, kidney, limb muscle (tibialis anterior), liver, lung, bone marrow, mesenteric adipose tissue (MAT), pancreas, skin, small intestine (duodenum), spleen, subcutaneous adipose tissue (SCAT)

**Ages:** 10 timepoints from 1 to 27 months

**Method:** Small RNA-seq; 771 samples; reads annotated to 87,590 RNA reference sequences across 8 RNA classes

**Cohort:** Tabula Muris Senis (TMS) — publicly available aging atlas

**Key Findings:**
- Molecular aging trajectories are largely **tissue-specific**
- **8 broadly deregulated miRNAs** found across tissues:
  - Positively correlated with age: **miR-29a-3p, miR-29c-3p, miR-155-5p, miR-184-3p, miR-1895**
  - Negatively correlated with age: **miR-300-3p, miR-487b-3p, miR-541-5p**
- miR-29c-3p showed the largest correlation with aging in solid organs, plasma, and EVs
- In mice rejuvenated by heterochronic parabiosis, miR-29c-3p was restored to young levels in liver
- miR-29c-3p targets extracellular matrix and secretion pathways

**Priority:** **VERY HIGH.** This is the most comprehensive natural aging miRNA dataset available. 16 tissues × 10 ages × replicates = 771 samples. Direct comparison of natural aging vs. chemotherapy-induced senescence miRNA changes is possible using this data.

**Note on comparison with senescence data:** Natural aging produces a mix of senescent and non-senescent cells in tissues. Comparing bulk tissue aging miRNA changes with in vitro senescence-specific changes can help distinguish miRNAs that are universal markers of cellular aging vs. those specific to pure senescent cell populations.
