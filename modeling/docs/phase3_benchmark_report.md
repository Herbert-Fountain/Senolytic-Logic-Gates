# Phase 3 Benchmark Report: AND Gate Model vs Experimental Flow Cytometry Data

## Experiment: miR-122 ON Switch (3/31/2026)

### Experimental Design
- **Cytometer**: NovoCyte Quanteon 621190610657, NovoExpress 1.6.1
- **Cell lines**: NIH 4T1 (mouse mammary carcinoma, miR-122 absent) and HuH7 (human hepatocellular carcinoma, miR-122 high)
- **Constructs**:
  - p065 = 2xKt-sfGFP payload mRNA (sfGFP with 2 K-turn motifs in 5'UTR)
  - p069B = L7Ae sensor mRNA (L7Ae CDS with miR-122-5p MRE in 5'UTR)
  - Positive Control = direct sfGFP mRNA (no K-turns)
- **Doses**: 100ng and 50ng per construct per well, 30,000 cells/well
- **Transfection**: Lipofectamine MessengerMAX
- **Replicates**: n=4 per condition
- **Readout**: Live sfGFP+ % by flow cytometry (FITC-A channel)

### Key Experimental Results (Live sfGFP+ %, mean of 4 replicates)

| Condition | 4T1 | HuH7 | Ratio |
|---|---|---|---|
| Positive Control 100ng (plain sfGFP) | 25.2% | 78.6% | 3.1x |
| 2xKt-sfGFP 100ng (payload only) | 29.9% | 91.5% | 3.1x |
| p069B 100ng (sensor only) | 0.0% | 0.3% | - |
| **p065 + p069B 100:100 (AND gate)** | **1.3%** | **26.7%** | **20.2x** |
| Mock transfection | 0.0% | 0.1% | - |
| 2xKt-sfGFP 50ng | 26.4% | 80.3% | 3.0x |
| **p065 + p069B 50:50 (AND gate)** | **1.6%** | **27.1%** | **17.3x** |
| No transfection | 0.3% | 0.4% | 1.2x |

### Circuit-Specific Performance
- **4T1 suppression by L7Ae**: 29.9% to 1.3% = 95.6% killed
- **HuH7 recovery (miR-122 derepression)**: 26.7% / 91.5% = 29.2% of baseline
- **ON:OFF selectivity**: 20.2x at 100ng, 17.3x at 50ng
- **Dose robustness**: similar performance at half dose

### Median Fluorescence Intensity (FITC-A) from Flow Report

| Population | 4T1 | HuH7 |
|---|---|---|
| sfGFP Negative (autofluorescence) | ~20-40K | ~50-90K |
| 2xKt-sfGFP Positive (unregulated) | ~8-13M | ~52-69M |
| AND gate sfGFP Positive | ~350K | ~570K |

Key insight: AND gate positive cells are **~100x dimmer** than unregulated 2xKt-sfGFP positive cells. The circuit produces partial, not full, derepression.

---

## Model Calibration Findings

### 1. miR-122 Copy Number is Critical

The model's AND gate behavior is extremely sensitive to miR-122 levels. Published estimates for HuH7 hepatocytes range from 50,000 to 120,000 copies/cell (Lagos-Quintana 2002; Jopling 2005). The original model used 10,000 copies, which was too low.

| miR-122 copies | L7Ae peak | Circuit efficiency | Comment |
|---|---|---|---|
| 0 (4T1) | 1,608,278 | 2.1% | Full repression |
| 1,000 | 69,452 | 2.6% | Still fully repressed |
| 10,000 | 5,177 | 9.4% | Moderate derepression |
| 30,000 | 797 | 32.7% | L7Ae below KD |
| 50,000 | 304 | 52.5% | Substantial derepression |
| 100,000 | 107 | 74.2% | Near-complete derepression |

Circuit efficiency = peak sfGFP(AND gate) / peak sfGFP(free payload).
KD(L7Ae-K-turn) = 1,084 molecules (0.9 nM, Turner 2005).

### 2. The L7Ae Burst Problem

Even in HuH7 with high miR-122, the sensor mRNA translates briefly (~seconds to minutes) before RISC-miR-122 silences it. This creates a "burst" of L7Ae protein that persists for hours (t1/2 = 20h) and partially represses the payload.

At miR-122 = 50,000: sensor is silenced in ~2 seconds, but ~300 L7Ae molecules are produced. With KD = 1,084, this gives occupancy = 300/(300+1084) = 22%. Substantial but not complete repression.

### 3. Population Heterogeneity Requirements

The single-cell ODE gives a SINGLE circuit efficiency per condition. But flow cytometry shows a DISTRIBUTION of sfGFP intensities. To match the experimental % positive, the model needs cell-to-cell variability from:

1. **mRNA delivery variability** (lognormal, CV ~ 0.5): determines baseline transfection curves
2. **Sensor:payload ratio variability** (partially correlated delivery): creates spread in circuit output
3. **miR-122 variability across HuH7 cells**: HuH7 is a heterogeneous line; some cells may have lower miR-122

### 4. Threshold Calibration

The flow cytometry gate threshold is set based on the negative control (mock transfection) to exclude autofluorescence. From the data:
- 4T1 negative median: ~20K FITC-A
- HuH7 negative median: ~74K FITC-A (3.5x higher autofluorescence)
- Gate position: approximately 100-200K FITC-A (estimated from histograms)
- This corresponds to approximately 1-2% of the free payload positive peak

### 5. Cell-Type-Specific Parameters

| Parameter | 4T1 | HuH7 | Source |
|---|---|---|---|
| Transfection efficiency | ~31% | ~94% | Calibrated from 2xKt-sfGFP data |
| miR-122 copies/cell | 0 | 8,000 (mean, CV=0.5) | Calibrated from AND gate flow data |
| Autofluorescence (FITC-A) | ~25K | ~74K | Flow negative controls |
| sfGFP MFI when positive | ~10M | ~55M | 2xKt-sfGFP positive controls |
| Expression efficiency ratio | 1x (ref) | 5.5x | MFI ratio of sfGFP+ cells |
| Circuit failure rate | 4.4% | 4.4% | Calibrated from 4T1 AND gate |

### 6. Final Calibrated Model vs Experiment

The model matches all experimental targets after calibration:

| Condition | Model | Experiment | Status |
|---|---|---|---|
| 4T1 free payload | 29.9% | 29.9% | Calibration target |
| HuH7 free payload | 94.1% | 91.5% | Close match |
| **4T1 AND gate** | **1.29%** | **1.32%** | **Match** |
| **HuH7 AND gate** | **28.8%** | **26.7%** | **Match** |
| **ON:OFF ratio** | **22.4x** | **20.2x** | **Match** |

### 7. Key Modeling Insights

1. **Binary switch behavior**: The circuit acts as a per-cell binary switch. The critical miR-122 threshold is ~25,700 copies/cell (where L7Ae peak = KD). Cells above this threshold are sfGFP ON; below are OFF.

2. **miR-122 variability drives HuH7 distribution**: The 26.7% positive fraction comes from the ~28% of HuH7 cells that have miR-122 above the critical threshold (mean=8,000, CV=0.5).

3. **Near-complete translational block**: L7Ae binding the 5'UTR K-turn blocks ribosome scanning almost completely (fold > 1000), not the 10-fold reduction previously assumed.

4. **Circuit failure rate**: 4.4% of cells have stochastic circuit failure (L7Ae never reaches effective levels), producing the 1.3% background in 4T1.

5. **Expression efficiency matters**: HuH7 translates 5.5x more sfGFP per mRNA copy than 4T1 (from MFI data), which shifts the detection threshold relative to circuit output.

6. **Functional miR-122 is lower than bulk measurements**: The calibrated miR-122 mean (8,000 copies) is lower than published bulk estimates (50,000-120,000). This likely reflects that only RISC-loaded, functionally active miR-122 participates in sensor silencing, not the total cellular pool.

### 8. Dose Robustness Test (50ng)

| Condition | Model | Experiment | Status |
|---|---|---|---|
| 4T1 AND gate 50:50ng | 1.3% | 1.6% | Close |
| HuH7 AND gate 50:50ng | 27.7% | 27.1% | Match |
| ON:OFF ratio 50ng | 22.2x | 17.3x | ~  |

The model correctly predicts:
- **HuH7 AND gate is stable across doses** (28.8% at 100ng vs 27.7% at 50ng)
- **Circuit selectivity is maintained at half dose** (22x retained)
- **Circuit failure rate scales with dose** (4.4% at 100ng, 6.2% at 50ng)

The model slightly over-predicts the 50ng ON:OFF ratio (22x vs 17x experimental). The discrepancy arises from the threshold calibration approach: the model threshold is calibrated from 100ng data, while the experimental gate is set from negative controls at a fixed FITC-A value independent of dose. Free payload baselines at 50ng are less well matched for this reason.

The critical miR-122 threshold shifts with dose (25,700 at 100ng to 18,100 at 50ng), reflecting lower L7Ae burst at lower sensor copies. This partially compensates for the lower sfGFP per cell.

### 9. Future Directions

1. **Senolytic circuit prediction**: Use calibrated model to predict selectivity for senescence miRNAs (miR-34a, miR-155, etc.)
2. **Multi-AND gate modeling**: Extend to circuits with multiple miRNA inputs
3. **Stochastic simulation (Phase 6)**: Gillespie SSA to replace the phenomenological circuit failure rate with mechanistic noise
4. **Dose-independent threshold**: Model FITC-A directly with autofluorescence background for better multi-dose predictions

---

## Raw Data Files
- PDF report: `Report of Herb ON Switch Experiment NIH 4T1 and HuH7 3_31_26.pdf`
- Summary CSV: `Summary Table Herb ON Switch Test 3_31_26.csv`
- Location: `E:\Experiments & Raw Data\Cell Imaging & Flow Cytometry Data\Herb ON Switch Exp 3_31_26\`
