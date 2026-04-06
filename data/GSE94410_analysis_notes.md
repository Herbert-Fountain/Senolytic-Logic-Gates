# GSE94410 Analysis Notes
## HUVEC Replicative Senescence miRNA Counts (Terlecki-Zaniewicz 2018)

**Dataset:** GSE94410 — 2,578 miRNAs, 15 samples (4 passage stages × 3-4 donors)
**Cell type:** Human umbilical vein endothelial cells (HUVECs)
**Senescence inducer:** Replicative exhaustion (NOT doxorubicin)

### Sample Groups
- S0: Tissue-derived (youngest) — 3 donors
- S1: Early culture — 4 donors  
- S2: Aging cells — 4 donors
- S3: Old/senescent cells — 4 donors

### Candidate miRNA Expression (Raw Counts, Mean per Group)

| miRNA | S0 (young) | S3 (old) | FC(S3/S0) | Absolute Level | Verdict |
|-------|-----------|---------|-----------|---------------|---------|
| miR-34a-5p | 46 | 239 | 5.2x UP | LOW-MED | Consistent with literature but LOW counts |
| miR-21-3p | 387 | 462 | 1.2x | MED | Barely changes — NOT a good switch input here |
| miR-21-5p | 407,800 | 1,070,778 | 2.6x UP | VERY HIGH | High counts but also very high in young |
| miR-22-3p | 58,962 | 18,652 | 0.3x DOWN | HIGH | OPPOSITE of literature reports — goes DOWN |
| miR-146a-5p | 401 | 410 | 1.0x | MED | No change |
| miR-215-5p | 40 | 7 | 0.2x DOWN | VERY LOW | OPPOSITE of Weigl 2024, essentially absent |
| miR-184 | 1 | 2 | ~1x | NEGLIGIBLE | Not expressed in HUVECs |
| miR-96-5p | 8 | 2 | 0.2x DOWN | NEGLIGIBLE | Not expressed in HUVECs |
| miR-181a-5p | 29,629 | 5,391 | 0.2x DOWN | HIGH | Goes DOWN (opposite of some reports) |
| miR-217 | 820 | 1,388 | 1.7x UP | HIGH | Modest increase, decent counts |
| miR-375 | 5 | 0 | DOWN | NEGLIGIBLE | Not expressed in HUVECs |
| miR-17-5p | 1,544 | 9,083 | 5.9x UP | HIGH | Goes UP — opposite of expected |
| miR-17-3p | 65 | 80 | 1.2x | LOW | Low counts, minimal change |
| miR-15b-5p | 310 | 294 | 0.9x | MED | No change |
| miR-30a-3p | 7,331 | 2,223 | 0.3x DOWN | HIGH | Goes DOWN |
| miR-122-5p | 108 | 21 | 0.2x DOWN | LOW | Liver-specific, low in HUVECs as expected |

### Critical Observations

1. **Most literature-reported "senescence miRNAs" do NOT show the expected pattern in this dataset.** miR-22 goes DOWN instead of UP, miR-215-5p drops to near zero, miR-181a goes DOWN, miR-146a shows no change.

2. **This confirms the Weigl 2024 finding that senescence miRNA changes are highly cell-type specific.** What's upregulated in fibroblast senescence may be downregulated in endothelial cell senescence.

3. **Several candidate miRNAs have extremely low absolute counts** (miR-184: 1-2 counts, miR-96-5p: 2-8 counts, miR-375: 0-5 counts). These are essentially NOT EXPRESSED in HUVECs and would be completely useless as switch inputs regardless of fold change.

4. **miR-21-5p has very high counts (400K-1M+) but is also very high in young cells.** The 2.6-fold increase means it's going from "very high" to "even higher" — not a clean ON/OFF switch. However, the absolute intracellular abundance would make it a RELIABLE switch input if the circuit can tolerate partial activation in young cells.

5. **miR-34a-5p shows the expected pattern (5.2x UP) but at low absolute counts (46→239).** The question is whether 239 counts is enough for reliable switch activation. This is the stoichiometric balance problem Saito's group warned about.

6. **This is replicative senescence, NOT doxorubicin-induced.** Herbert's planned doxorubicin experiment may show different patterns.
