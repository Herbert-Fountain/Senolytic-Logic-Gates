# GSE55164 Analysis Report
## Mouse Skeletal Muscle Aging — miRNA Expression Profiling

*Analysis date: 2026-04-06*

---

## 1. Study Summary

| Parameter | Details |
|-----------|---------|
| **GEO Accession** | [GSE55164](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE55164) |
| **Publication** | Kim JY et al. Genome-wide profiling of the microRNA-mRNA regulatory network in skeletal muscle with aging. *Aging*. 2014;6(7):524-544. PMID: [25063768](https://pubmed.ncbi.nlm.nih.gov/25063768/) |
| **Companion** | GSE55163 (mRNA-seq from same animals) |
| **Organism** | *Mus musculus* (C57BL/6) |
| **Tissue** | Gastrocnemius skeletal muscle |
| **Ages** | 6 months (young) vs 24 months (aged) |
| **Platform** | Illumina HiSeq 2000 |
| **Samples** | 12 total: n=6 young, n=6 aged |
| **Data format** | Log2 normalized expression values |
| **miRNAs detected** | 2,035 rows (some duplicates) |

## 2. Key Context

Skeletal muscle aging involves sarcopenia (muscle mass/strength loss), fiber type shifts, and mitochondrial dysfunction. The miRNA changes may reflect muscle-specific biology rather than universal senescence markers. However, aged muscle contains senescent cells (satellite cells, fibro-adipogenic progenitors), so some overlap with senescence-specific signatures is expected.

## 3. Results

### 3.1 Candidate miRNA Expression

Values are log2 normalized. Linear fold change estimated as 2^(aged - young).

| miRNA | Young (log2) | Aged (log2) | FC (linear) | Direction | Concordance with Other Data |
|-------|-------------|-------------|-------------|-----------|---------------------------|
| mmu-miR-34a-5p | 9.30 | 10.62 | **2.49x UP** | UP | **YES** — consistent across all datasets |
| mmu-miR-146a-5p | 11.47 | 12.77 | **2.45x UP** | UP | **PARTIAL** — UP here and in some mouse tissues (GSE217458), but no change in HUVECs (GSE94410) |
| mmu-miR-184-3p | 0.73 | 2.76 | **4.07x UP** | UP | Direction matches Wagner 2024, but baseline is near-zero (~1.7 linear counts) |
| mmu-miR-155-5p | 9.33 | 10.09 | **1.69x UP** | UP | **YES** — consistent with GSE217458 aging data |
| mmu-miR-29a-3p | 16.01 | 16.30 | 1.22x | Modest UP | **YES** — matches GSE217458 direction but smaller magnitude |
| mmu-miR-29c-3p | 14.20 | 14.41 | 1.16x | Modest UP | **YES** — matches but smaller than in other tissues |
| mmu-miR-22-3p | 22.14 | 22.15 | 1.00x | No change | Neutral — no change in muscle; DOWN in HUVECs; stable in most GSE217458 tissues |
| mmu-miR-21a-5p | 16.58 | 16.67 | 1.06x | No change | Neutral in muscle; modestly UP in other aging contexts |
| mmu-miR-21a-3p | 10.98 | 10.97 | 0.99x | No change | No change here or in HUVECs |
| mmu-miR-96-5p | 3.96 | 1.27 | **0.16x DOWN** | DOWN | Declining — consistent with low/absent expression trend |
| mmu-miR-17-5p | 9.18 | 8.91 | 0.83x | Slight DOWN | **YES** — modestly DOWN, consistent with miR-17 family decline |
| mmu-miR-122-5p | 0.00 | 1.64 | 3.13x UP | UP from zero | Not meaningful — baseline is 0 (not expressed in muscle) |

### 3.2 Notable Findings

**miR-34a-5p shows the strongest consistent signal across datasets:**

| Dataset | Context | FC | Absolute Level |
|---------|---------|-----|---------------|
| GSE94410 (HUVEC senescence) | In vitro, replicative | 5.2x UP | Low (239 counts) |
| GSE217458 (mouse 16 tissues) | In vivo, natural aging | 1.2-1.7x UP | Moderate (500-3800 RPMM) |
| GSE55164 (mouse muscle) | In vivo, natural aging | **2.5x UP** | Moderate (log2 ~10.6 ≈ 1,500) |

This is the most consistently upregulated miRNA across all datasets and contexts we've analyzed.

**miR-146a-5p is tissue-dependent:**
- UP 2.5x in aged muscle (this dataset)
- UP 2.3x in aged kidney (GSE217458)
- No change in HUVECs (GSE94410)
- No change in spleen, modest UP in other tissues (GSE217458)

This pattern suggests miR-146a-5p upregulation may be driven by inflammatory infiltration in aging tissues rather than cell-autonomous senescence, since it doesn't change in isolated cell culture (HUVECs).

## 4. Limitations

1. **Log2 normalized values, not raw counts.** We cannot assess absolute expression levels or verify normalization methodology. The log2 scale compresses differences at high expression.
2. **Skeletal muscle is a specialized tissue.** Muscle-specific miRNAs (myomiRs) dominate the profile. Some aging changes may reflect fiber type transitions rather than senescence.
3. **Bulk tissue.** Cannot distinguish senescent satellite cells from healthy myofibers.
4. **Mouse, not human.** Although most miRNAs are conserved, tissue-specific expression patterns may differ.
5. **Only two age points (6 vs 24 months).** Cannot determine onset timing or trajectory shape.

## 5. Conclusions

1. miR-34a-5p is consistently UP 2.5x in aged muscle, adding another tissue/context to its track record as the most reliable aging/senescence marker.
2. miR-146a-5p upregulation in aged muscle but not in cultured cells suggests it may be driven by tissue-level inflammation (immune cell infiltration) rather than cell-autonomous senescence.
3. The miR-29 family shows only modest changes in muscle (1.2x) compared to the larger changes seen across 16 tissues in GSE217458. Muscle may not be the primary tissue driving the pan-tissue miR-29 aging signal.
4. miR-184-3p continues to show upward trends from near-zero baselines — statistically detectable but practically irrelevant for circuit applications.

---

## References

1. Kim JY et al. *Aging*. 2014;6(7):524-544. PMID: 25063768
