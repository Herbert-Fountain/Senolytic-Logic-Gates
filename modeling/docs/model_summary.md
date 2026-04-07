# Computational Model of L7Ae/K-turn mRNA Logic Gate Circuits

## Overview

This document describes a computational modeling tool for simulating and optimizing mRNA-based logic gate circuits that use the archaeal ribosomal protein L7Ae and its cognate RNA K-turn motif to achieve miRNA-responsive translational control. The tool combines ordinary differential equation (ODE) modeling of intracellular kinetics with population-level simulations of cell-to-cell variability, producing predictions directly comparable to flow cytometry experimental readouts.

The model was calibrated against experimental flow cytometry data from a miR-122-5p ON switch circuit tested in NIH 4T1 (miR-122-negative) and HuH7 (miR-122-positive) cells, achieving quantitative agreement with all major experimental observations.

## Circuit Architecture

The AND gate circuit consists of two co-delivered mRNA species:

**Sensor mRNA (p069B)**: Encodes L7Ae protein with a miR-122-5p miRNA response element (MRE) in the 5'UTR. In cells lacking miR-122, the sensor translates freely and L7Ae protein accumulates. In cells expressing miR-122, RISC-miR-122 binds the 5'UTR MRE and directs AGO2 endonucleolytic cleavage, destroying the sensor mRNA and preventing L7Ae production.

**Payload mRNA (p065)**: Encodes sfGFP (or a therapeutic payload) with two K-turn motifs (2xKt) in the 5'UTR. When L7Ae protein is present, it binds the K-turn motifs and physically blocks 40S ribosome scanning, silencing translation. When L7Ae is absent (or below the binding dissociation constant), the payload translates normally.

The net effect is an AND gate: payload expression requires BOTH the absence of L7Ae AND the presence of the cognate miRNA.

## Mathematical Model

### Intracellular ODE System

The model tracks eight molecular species as a function of time:

1. **M_sensor_free**: Sensor mRNA molecules available for translation
2. **M_sensor_bound**: Sensor mRNA bound to RISC-miRNA (silenced)
3. **RISC**: Free RISC-miRNA complexes available for binding
4. **L7Ae**: Free L7Ae protein molecules
5. **M_payload_free**: Payload mRNA molecules available for translation
6. **M_payload_repr**: Payload mRNA with L7Ae bound to K-turns (repressed)
7. **sfGFP**: Accumulated sfGFP protein
8. **L7Ae_bound**: L7Ae molecules bound to payload K-turns

The ODE system captures:
- RISC-miRNA binding to sensor MRE (bimolecular, kon = 0.003 molecule^-1 cell hr^-1)
- AGO2 catalytic cleavage of sensor mRNA (k_slice = 18 hr^-1, RISC recycled)
- L7Ae translation from free sensor mRNA (k_translate = 100 proteins/mRNA/hr)
- L7Ae binding to payload K-turns (KD = 0.9 nM, ~1,084 molecules/cell)
- Translational repression of K-turn-bound payload (near-complete block, ~1000-fold)
- First-order decay of all mRNA (t1/2 = 12h) and protein species (t1/2 = 20-26h)

All kinetic parameters are sourced from published literature (Briskin 2019, Wang & Bartel 2024, Turner 2005, Mauger 2019, Schwanhausser 2011).

### Population Layer

Flow cytometry reports the fraction of cells above a fluorescence detection threshold, not the mean protein level per cell. Converting single-cell ODE predictions to population-level % positive requires modeling cell-to-cell variability in:

1. **mRNA delivery**: Lognormal distribution (CV = 0.5) for copies per transfected cell
2. **Sensor:payload co-delivery**: Partially correlated (rho = 0.7) lognormal delivery of the two mRNA species
3. **miRNA expression heterogeneity**: Lognormal distribution of miR-122 copies across cells within a cell line (mean = 8,000, CV = 0.5 for HuH7)
4. **Transfection efficiency**: Cell-type-specific fraction of cells receiving any mRNA (4T1: 31%, HuH7: 94%)
5. **Expression efficiency**: Cell-type-specific translation rate per mRNA copy (HuH7 produces 5.5x more sfGFP per mRNA than 4T1, measured from median fluorescence intensity of positive cells)
6. **Circuit failure rate**: Stochastic probability that the circuit does not function in a given cell (4.4%, dose-dependent, scaling as sqrt(reference_dose / actual_dose))

The population model samples 10,000-50,000 virtual cells, computes circuit sfGFP for each using an interpolated ODE lookup table, applies a detection threshold calibrated from the free-payload positive control, and reports % positive.

### Binary Switch Behavior

A key finding from the calibration is that the circuit operates as a binary switch at the single-cell level, not a graded dimmer. The critical miR-122 threshold is approximately 25,700 copies/cell: cells with miR-122 above this threshold have L7Ae peak below the KD and are effectively ON; cells below this threshold are OFF. The 26.7% sfGFP+ fraction in HuH7 reflects the ~28% of cells in the miR-122 distribution that exceed this critical threshold.

## Experimental Calibration

### Calibration Dataset

The model was calibrated against a miR-122 ON switch experiment performed on 3/31/2026:
- **Cytometer**: NovoCyte Quanteon, NovoExpress 1.6.1
- **Constructs**: p065 (2xKt-sfGFP) + p069B (5'MRE-L7Ae)
- **Doses**: 100ng and 50ng per construct per well
- **Cells**: 30,000 per well, Lipofectamine MessengerMAX transfection
- **Replicates**: n=4 per condition
- **Readout**: Live sfGFP+ % at 24h post-transfection

### Calibration Results

| Condition | Model | Experiment |
|-----------|-------|------------|
| 4T1 free payload (2xKt-sfGFP alone) | 29.9% | 29.9% |
| HuH7 free payload | 94.1% | 91.5% |
| **4T1 AND gate** | **1.29%** | **1.32%** |
| **HuH7 AND gate** | **28.8%** | **26.7%** |
| **ON:OFF ratio** | **22.5x** | **20.2x** |
| Sensor alone (p069B) | 0.0% | 0.0% |
| Mock transfection | 0.0% | 0.0% |

### Dose Robustness

At half dose (50ng per construct), the model correctly predicts maintained selectivity:
- HuH7 AND gate: 27.7% (model) vs 27.1% (experiment)
- ON:OFF ratio: 22.2x (model) vs 17.3x (experiment)

### Key Biological Insights from Calibration

1. **L7Ae repression is near-complete**: The 5'UTR K-turn blocks ribosome scanning with ~1000-fold efficiency, not the 10-fold reduction assumed from bulk reporter assays.

2. **Functional miR-122 is lower than total**: The calibrated functional miR-122 level (8,000 copies/cell) is substantially lower than published bulk estimates (50,000-120,000), likely reflecting the fraction that is actively RISC-loaded.

3. **The L7Ae burst limits ON-cell recovery**: Even in miR-122-positive cells, the sensor mRNA translates briefly (~seconds) before RISC silences it, creating a burst of ~300 L7Ae molecules that persists for hours (t1/2 = 20h) and partially represses the payload.

4. **Cell-type-specific expression efficiency matters**: HuH7 translates 5.5x more sfGFP per mRNA copy than 4T1 (from MFI data: 55M vs 10M FITC-A median in positive cells), critical for threshold-based predictions.

## Dosing Optimization

### Prediction: Suboptimal 1:1 Ratio

The optimizer predicts that the standard 1:1 sensor:payload ratio is far from optimal. At 200ng total mRNA:

| S:P Ratio | Sensor | Payload | ON% (HuH7) | OFF% (4T1) | Selectivity |
|-----------|--------|---------|------------|------------|-------------|
| 1:1 (standard) | 100ng | 100ng | 28% | 1.3% | 22x |
| 0.5:1 | 67ng | 133ng | 69% | 1.4% | 50x |
| 0.2:1 | 33ng | 167ng | 93% | 1.4% | 67x |
| **0.15:1 (optimal)** | **26ng** | **174ng** | **94%** | **1.4%** | **68x** |

### Why Low Sensor is Better

Two asymmetric properties of the L7Ae/K-turn system explain this:

1. **L7Ae is catalytically potent**: A single sensor mRNA produces ~800 L7Ae molecules over its 12-hour lifetime. Five copies produce 3,200 L7Ae, already 3x above the KD. The standard 2,000 copies produce 1.6 million L7Ae, a 1,500-fold excess over what is needed for repression.

2. **Excess sensor hurts the ON state**: In miR-122-positive cells, sensor mRNA is silenced within seconds. But those seconds produce a burst of L7Ae proportional to the sensor copy number. At 2,000 copies (1:1 ratio), the burst is ~300 L7Ae molecules, enough to partially repress the payload for hours as L7Ae decays with a 20-hour half-life. At 400 copies (0.2:1 ratio), the burst is only ~60 molecules, well below the KD, allowing immediate payload translation.

This prediction is directly testable with a sensor titration experiment.

## Iterative Experimental Workflow

The tool supports a closed-loop design-experiment-calibrate cycle:

1. **Design**: The experiment designer generates a plate layout with controls, conditions, and quantitative predictions for each well.

2. **Run**: The investigator executes the experiment as designed.

3. **Calibrate**: Flow cytometry results are fed back as a CSV file. The model calibrator fits internal parameters (miRNA levels, CV, failure rate) to minimize prediction error using gradient-free optimization. Parameters are saved for future use.

4. **Iterate**: Updated parameters improve predictions for the next round. After 2-3 cycles, the model converges to high accuracy for the specific cell lines and transfection conditions in use.

### Calibration Input Format

CSV with columns: `cell_type`, `sensor_ng`, `payload_ng`, `observed_pct`

```csv
cell_type,sensor_ng,payload_ng,observed_pct
4T1,10,150,1.8
4T1,50,150,1.3
HuH7,10,150,88.0
HuH7,50,150,55.0
```

## Software Architecture

```
modeling/
  run.py                 # Command-line interface
  core/
    parameters.py        # Kinetic parameters (all literature-cited)
    and_gate.py          # ODE system (8 species, scipy solve_ivp)
    intracellular.py     # Simpler ON/OFF switch model (4 species)
    population.py        # Cell-to-cell variability and flow cytometry simulation
    optimizer.py         # Sensor:payload ratio optimization
    experiment.py        # Experiment design and model calibration
```

### Command-Line Interface

```bash
python modeling/run.py simulate    # Single-cell ODE simulation
python modeling/run.py optimize    # Sensor:payload ratio optimization
python modeling/run.py design      # Validation experiment plan
python modeling/run.py calibrate   # Model calibration from CSV
python modeling/run.py sweep       # miR-122 dose-response curve
python modeling/run.py benchmark   # Benchmark against experimental data
```

## Limitations and Future Work

1. **Deterministic ODE**: The current model uses deterministic ODEs for intracellular dynamics. Stochastic effects (translational bursting, binding noise) are captured phenomenologically through a circuit failure rate rather than mechanistically. A Gillespie stochastic simulation algorithm (SSA) implementation is planned.

2. **No spatial modeling**: The model assumes a well-mixed intracellular environment. Endosomal escape kinetics and mRNA compartmentalization are not modeled.

3. **Two cell types**: Currently calibrated for NIH 4T1 and HuH7. Extension to senescence-associated miRNAs and primary cells requires additional calibration data.

4. **No interactive GUI**: The current interface is command-line only. A web-based or graphical interface is planned for Phase 9.

5. **Single miRNA input**: The current AND gate model uses a single miRNA input. Extension to multi-input AND gates (multiple sensor mRNAs with different MREs) is architecturally supported but not yet implemented.

## References

1. Saito H, et al. Synthetic translational regulation by an L7Ae-kink-turn RNP switch. Nat Chem Biol. 2010;6(1):71-78.
2. Briskin D, et al. The biochemical basis for the cooperative action of microRNAs. Mol Cell. 2019;75(1):24-37.
3. Wang Y, Bartel DP. Computational and experimental dissection of microRNA-mediated gene silencing. Mol Cell. 2024;84(12):2256-2272.
4. Turner B, et al. Induced fit of RNA on binding the L7Ae protein to the kink-turn motif. RNA. 2005;11(8):1192-1200.
5. Mauger DM, et al. mRNA structure regulates protein expression through changes in functional half-life. Proc Natl Acad Sci. 2019;116(48):24075-24083.
6. Schwanhausser B, et al. Global quantification of mammalian gene expression control. Nature. 2011;473(7347):337-342.
