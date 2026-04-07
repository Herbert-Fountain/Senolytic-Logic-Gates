# Circuit Design Report
*Generated: 2026-04-07 01:22*
*Mode: cancer*

---

## 1. Data Summary

- Total miRNAs analyzed: 1631
- Upregulated in target: 780
- Downregulated in target: 671
- Stable: 180

## 2. Thresholds Used

| Parameter | Value |
|-----------|-------|
| Minimum target expression (ON switch) | 50 CPM |
| Minimum control expression (OFF switch) | 100 CPM |
| Minimum fold change (ON) | 1.5x |
| Maximum fold change (OFF) | 0.5x |

## 3. ON-Switch Candidates (Upregulated in Target)

| Rank | miRNA | Target CPM | Control CPM | FC | Discrimination |
|------|-------|-----------|------------|-----|---------------|
| 1 | mmu-miR-125b-1-3p | 7528 | 19 | 404.51x | 404.51x |
| 2 | mmu-miR-183-3p | 175 | 2 | 101.43x | 101.43x |
| 3 | mmu-miR-466k | 69 | 1 | 77.09x | 77.09x |
| 4 | mmu-miR-297a-5p | 964 | 15 | 63.86x | 63.86x |
| 5 | mmu-miR-466b-5p | 426 | 7 | 62.75x | 62.75x |
| 6 | mmu-miR-1983 | 421 | 7 | 62.16x | 62.16x |
| 7 | mmu-miR-183-5p | 3802 | 61 | 61.83x | 61.83x |
| 8 | mmu-miR-466i-3p | 62 | 1 | 61.80x | 61.80x |
| 9 | mmu-miR-466o-5p | 59 | 1 | 60.72x | 60.72x |
| 10 | mmu-miR-466f-3p | 501 | 8 | 59.75x | 59.75x |

## 4. OFF-Switch Candidates (Downregulated in Target)

| Rank | miRNA | Target CPM | Control CPM | FC | Discrimination |
|------|-------|-----------|------------|-----|---------------|
| 1 | mmu-miR-34b-3p | 0 | 102 | 0.00x | infx |
| 2 | mmu-miR-1a-1-5p | 0 | 285 | 0.00x | infx |
| 3 | mmu-miR-802-5p | 0 | 605 | 0.00x | infx |
| 4 | mmu-miR-133a-5p | 0 | 163 | 0.00x | infx |
| 5 | mmu-miR-216b-5p | 0 | 171 | 0.00x | infx |
| 6 | mmu-miR-122-3p | 0 | 5094 | 0.00x | 115678.69x |
| 7 | mmu-miR-142a-5p | 0 | 10286 | 0.00x | 25227.83x |
| 8 | mmu-miR-122-5p | 3 | 66242 | 0.00x | 19913.79x |
| 9 | mmu-miR-142a-3p | 6 | 102673 | 0.00x | 16179.05x |
| 10 | mmu-miR-34b-5p | 0 | 641 | 0.00x | 14547.92x |

## 5. Recommended Circuit Designs

All designs use the L7Ae-only AND gate architecture:
each input miRNA controls a separate L7Ae mRNA. The payload
mRNA has a K-turn in its 5'UTR. All L7Ae sources must be
eliminated for payload expression.

**Selectivity estimates are approximate** (multiplicative model;
actual response is nonlinear/sigmoidal). Use for ranking, not prediction.

### Design 1: mmu-miR-125b-1-3p + mmu-miR-34b-3p

| Property | Value |
|----------|-------|
| ON inputs | mmu-miR-125b-1-3p |
| OFF inputs | mmu-miR-34b-3p |
| Total mRNAs | 3 (1 ON + 1 OFF + 1 payload) |
| Estimated selectivity | ~infx |

| miRNA | Type | Target CPM | Control CPM | Discrimination |
|-------|------|-----------|------------|---------------|
| mmu-miR-125b-1-3p | ON | 7528 | 19 | 404.51x |
| mmu-miR-34b-3p | OFF | 0 | 102 | infx |

---

### Design 2: mmu-miR-125b-1-3p + mmu-miR-1a-1-5p

| Property | Value |
|----------|-------|
| ON inputs | mmu-miR-125b-1-3p |
| OFF inputs | mmu-miR-1a-1-5p |
| Total mRNAs | 3 (1 ON + 1 OFF + 1 payload) |
| Estimated selectivity | ~infx |

| miRNA | Type | Target CPM | Control CPM | Discrimination |
|-------|------|-----------|------------|---------------|
| mmu-miR-125b-1-3p | ON | 7528 | 19 | 404.51x |
| mmu-miR-1a-1-5p | OFF | 0 | 285 | infx |

---

### Design 3: mmu-miR-125b-1-3p + mmu-miR-802-5p

| Property | Value |
|----------|-------|
| ON inputs | mmu-miR-125b-1-3p |
| OFF inputs | mmu-miR-802-5p |
| Total mRNAs | 3 (1 ON + 1 OFF + 1 payload) |
| Estimated selectivity | ~infx |

| miRNA | Type | Target CPM | Control CPM | Discrimination |
|-------|------|-----------|------------|---------------|
| mmu-miR-125b-1-3p | ON | 7528 | 19 | 404.51x |
| mmu-miR-802-5p | OFF | 0 | 605 | infx |

---

### Design 4: mmu-miR-183-3p + mmu-miR-34b-3p

| Property | Value |
|----------|-------|
| ON inputs | mmu-miR-183-3p |
| OFF inputs | mmu-miR-34b-3p |
| Total mRNAs | 3 (1 ON + 1 OFF + 1 payload) |
| Estimated selectivity | ~infx |

| miRNA | Type | Target CPM | Control CPM | Discrimination |
|-------|------|-----------|------------|---------------|
| mmu-miR-183-3p | ON | 175 | 2 | 101.43x |
| mmu-miR-34b-3p | OFF | 0 | 102 | infx |

---

### Design 5: mmu-miR-183-3p + mmu-miR-1a-1-5p

| Property | Value |
|----------|-------|
| ON inputs | mmu-miR-183-3p |
| OFF inputs | mmu-miR-1a-1-5p |
| Total mRNAs | 3 (1 ON + 1 OFF + 1 payload) |
| Estimated selectivity | ~infx |

| miRNA | Type | Target CPM | Control CPM | Discrimination |
|-------|------|-----------|------------|---------------|
| mmu-miR-183-3p | ON | 175 | 2 | 101.43x |
| mmu-miR-1a-1-5p | OFF | 0 | 285 | infx |

---

### Design 6: mmu-miR-183-3p + mmu-miR-802-5p

| Property | Value |
|----------|-------|
| ON inputs | mmu-miR-183-3p |
| OFF inputs | mmu-miR-802-5p |
| Total mRNAs | 3 (1 ON + 1 OFF + 1 payload) |
| Estimated selectivity | ~infx |

| miRNA | Type | Target CPM | Control CPM | Discrimination |
|-------|------|-----------|------------|---------------|
| mmu-miR-183-3p | ON | 175 | 2 | 101.43x |
| mmu-miR-802-5p | OFF | 0 | 605 | infx |

---

### Design 7: mmu-miR-466k + mmu-miR-34b-3p

| Property | Value |
|----------|-------|
| ON inputs | mmu-miR-466k |
| OFF inputs | mmu-miR-34b-3p |
| Total mRNAs | 3 (1 ON + 1 OFF + 1 payload) |
| Estimated selectivity | ~infx |

| miRNA | Type | Target CPM | Control CPM | Discrimination |
|-------|------|-----------|------------|---------------|
| mmu-miR-466k | ON | 69 | 1 | 77.09x |
| mmu-miR-34b-3p | OFF | 0 | 102 | infx |

---

### Design 8: mmu-miR-466k + mmu-miR-1a-1-5p

| Property | Value |
|----------|-------|
| ON inputs | mmu-miR-466k |
| OFF inputs | mmu-miR-1a-1-5p |
| Total mRNAs | 3 (1 ON + 1 OFF + 1 payload) |
| Estimated selectivity | ~infx |

| miRNA | Type | Target CPM | Control CPM | Discrimination |
|-------|------|-----------|------------|---------------|
| mmu-miR-466k | ON | 69 | 1 | 77.09x |
| mmu-miR-1a-1-5p | OFF | 0 | 285 | infx |

---

### Design 9: mmu-miR-466k + mmu-miR-802-5p

| Property | Value |
|----------|-------|
| ON inputs | mmu-miR-466k |
| OFF inputs | mmu-miR-802-5p |
| Total mRNAs | 3 (1 ON + 1 OFF + 1 payload) |
| Estimated selectivity | ~infx |

| miRNA | Type | Target CPM | Control CPM | Discrimination |
|-------|------|-----------|------------|---------------|
| mmu-miR-466k | ON | 69 | 1 | 77.09x |
| mmu-miR-802-5p | OFF | 0 | 605 | infx |

---

### Design 10: mmu-miR-125b-1-3p + mmu-miR-183-3p + mmu-miR-34b-3p

| Property | Value |
|----------|-------|
| ON inputs | mmu-miR-125b-1-3p, mmu-miR-183-3p |
| OFF inputs | mmu-miR-34b-3p |
| Total mRNAs | 4 (2 ON + 1 OFF + 1 payload) |
| Estimated selectivity | ~infx |

| miRNA | Type | Target CPM | Control CPM | Discrimination |
|-------|------|-----------|------------|---------------|
| mmu-miR-125b-1-3p | ON | 7528 | 19 | 404.51x |
| mmu-miR-183-3p | ON | 175 | 2 | 101.43x |
| mmu-miR-34b-3p | OFF | 0 | 102 | infx |

---

## 6. Important Caveats

1. **Selectivity estimates are order-of-magnitude approximations.** The actual
   miRNA-to-switch response is sigmoidal, not linear (Mukherji et al., Nature, 2011).
   Small fold changes may produce binary or no response depending on threshold position.

2. **CPM normalization corrects for library size but not composition bias.** TMM or
   DESeq2 normalization is recommended for formal analysis.

3. **Sequencing counts are not copies per cell.** Absolute intracellular abundance
   depends on ligation bias, extraction efficiency, and cell number input.

4. **Empirical validation is required.** Test with fluorescent reporter before
   switching to cytotoxic payload.

