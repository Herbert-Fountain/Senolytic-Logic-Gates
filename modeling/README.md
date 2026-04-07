# RNA Logic Gate Circuit Modeling Tool

An ODE-based simulation tool for designing, optimizing, and validating mRNA-based logic gate circuits that use the L7Ae/K-turn translational repression system to achieve miRNA-responsive gene expression.

## What This Tool Does

Given a circuit design (sensor mRNA + payload mRNA) and target/off-target cell types, this tool:

1. **Simulates** the intracellular dynamics of L7Ae production, miRNA-mediated silencing, K-turn binding, and payload translation
2. **Predicts** the fraction of cells that will be sfGFP+ (or payload-expressing) in flow cytometry
3. **Optimizes** the sensor:payload mRNA ratio to maximize selectivity or activation
4. **Designs** validation experiments with plate layouts, controls, and quantitative predictions
5. **Calibrates** itself from experimental results, improving predictions for the next round

## Quick Start

```bash
# Basic AND gate simulation (4T1 cell, no miR-122)
python modeling/run.py simulate --mirna 0 --sensor 2000 --payload 2000

# Same circuit in HuH7 (high miR-122)
python modeling/run.py simulate --mirna 50000 --sensor 2000 --payload 2000

# Find optimal sensor:payload ratio for 200ng total mRNA
python modeling/run.py optimize --total-ng 200 --objective balanced

# Generate a validation experiment plan
python modeling/run.py design --payload-ng 150 --sensor-range 10,25,50,100,150

# miR-122 dose-response curve
python modeling/run.py sweep --include-zero

# Run benchmark against experimental data
python modeling/run.py benchmark

# Calibrate model from your flow cytometry results
python modeling/run.py calibrate --csv your_results.csv --save-params fitted.json
```

## Commands

### `simulate`
Run a single-cell AND gate simulation. Shows peak sfGFP, L7Ae levels, and circuit efficiency.

```
python modeling/run.py simulate --mirna 50000 --sensor 2000 --payload 2000 --hours 24
```

### `optimize`
Find the optimal sensor:payload mRNA ratio for a given total dose. Supports three objectives:
- `selectivity`: maximize ON:OFF ratio
- `activation`: maximize % positive in ON cells
- `balanced`: maximize both (ON% * log(ratio))

```
python modeling/run.py optimize --total-ng 200 --objective selectivity
```

### `design`
Generate a complete validation experiment plan with plate layout, required materials, controls, and quantitative predictions for every condition.

```
python modeling/run.py design --payload-ng 150 --sensor-range 0,10,25,50,100,150 --replicates 3 --output plate_map.csv
```

### `calibrate`
Feed experimental flow cytometry results back into the model to refine parameters. Input CSV must have columns: `cell_type`, `sensor_ng`, `payload_ng`, `observed_pct`.

```
python modeling/run.py calibrate --csv results.csv --fit-params mirna_mean,mirna_cv --save-params fitted.json
```

### `sweep`
Generate a miR-122 dose-response curve showing how circuit output changes with miRNA concentration.

```
python modeling/run.py sweep --sensor 2000 --payload 2000 --include-zero
```

### `benchmark`
Run the full benchmark suite comparing model predictions against experimental flow cytometry data from the miR-122 ON switch experiment (3/31/2026).

## Circuit Architecture

The tool models the Saito lab's L7Ae/K-turn AND gate architecture:

```
mRNA-1 (Sensor):   5'[miRNA-MRE]---[L7Ae CDS]---3'
                         |
                    miRNA-RISC binds here
                    and silences L7Ae

mRNA-2 (Payload):  5'[2xK-turn]---[sfGFP/DTA CDS]---3'
                         |
                    L7Ae binds here
                    and blocks translation
```

**When miRNA is ABSENT** (off-target cell):
- Sensor translates freely, L7Ae accumulates
- L7Ae binds K-turns on payload, blocks ribosome scanning
- Payload is silenced; sfGFP OFF

**When miRNA is PRESENT** (target cell):
- miRNA-RISC silences sensor mRNA via AGO2 cleavage
- L7Ae is not produced (or produced briefly then decays)
- Payload translates freely; sfGFP ON

## Model Components

### 1. Intracellular ODE (`and_gate.py`)
Eight state variables tracking all molecular species over time:

| Species | Description |
|---------|-------------|
| M_sensor_free | Free sensor mRNA (translatable) |
| M_sensor_bound | Sensor mRNA bound to RISC-miRNA (silenced) |
| RISC | Free RISC-miRNA complexes |
| L7Ae | Free L7Ae protein |
| M_payload_free | Free payload mRNA (translatable) |
| M_payload_repr | Payload mRNA with L7Ae bound (repressed) |
| sfGFP | sfGFP protein |
| L7Ae_bound | L7Ae molecules bound to payload K-turns |

Solved using scipy `solve_ivp` with LSODA integrator.

### 2. Population Layer (`population.py`)
Converts single-cell ODE results into flow cytometry-like readouts:
- Lognormal mRNA delivery distribution (CV = 0.5)
- Correlated sensor/payload delivery (correlation = 0.7)
- Cell-to-cell miRNA variability (lognormal)
- Cell-type-specific transfection efficiency and expression factors
- Circuit failure rate (stochastic noise)
- Detection threshold (calibrated from free payload controls)

### 3. Optimizer (`optimizer.py`)
Sweeps sensor:payload ratios and finds the optimal balance between activation and selectivity. Supports fixed-total and independent-dose optimization.

### 4. Experiment Designer (`experiment.py`)
Generates structured experiment plans with:
- Plate map and well assignments
- Required controls and their purpose
- Quantitative predictions with tolerance ranges
- Key testable hypotheses

### 5. Model Calibrator (`experiment.py`)
Fits model parameters to experimental data using Nelder-Mead optimization:
- Ingests CSV of flow cytometry results
- Adjusts miRNA levels, CV, failure rate, expression ratio
- Reports parameter changes and prediction improvement
- Saves fitted parameters for future sessions

## Kinetic Parameters

All parameters are from published literature with citations. Key values:

| Parameter | Value | Source |
|-----------|-------|--------|
| mRNA half-life | 12h | Mauger et al., PNAS 2019 |
| Translation rate | 100 proteins/mRNA/hr | Schwanhausser et al., Nature 2011 |
| RISC-MRE kon | 0.003 mol^-1 cell hr^-1 | Briskin et al., Mol Cell 2019 |
| AGO2 cleavage | 18 hr^-1 | Wang & Bartel, Mol Cell 2024 |
| L7Ae-Kturn KD | 0.9 nM (1,084 molecules) | Turner et al., RNA 2005 |
| L7Ae repression | ~1000-fold (near-complete block) | Calibrated from flow data |
| sfGFP half-life | 26h | Li et al., PEDS 1998 |
| L7Ae half-life | 20h | Estimated |

See `core/parameters.py` for the complete parameter table with citations.

## Calibration Against Experimental Data

The model was calibrated against flow cytometry data from a miR-122 ON switch experiment (NIH 4T1 vs HuH7 cells, p065 + p069B AND gate, Lipofectamine MessengerMAX, NovoCyte Quanteon).

| Metric | Model | Experiment |
|--------|-------|------------|
| 4T1 AND gate (OFF) | 1.29% | 1.32% |
| HuH7 AND gate (ON) | 28.8% | 26.7% |
| ON:OFF ratio | 22.5x | 20.2x |
| Dose robustness (50ng) | 22.2x | 17.3x |

Key biological insights from calibration:
- L7Ae binding the 5'UTR K-turn is a near-complete translational block (~1000-fold)
- The circuit acts as a binary switch per cell with a critical miR-122 threshold (~25,700 copies)
- Functional RISC-loaded miR-122 in HuH7 is ~8,000 copies/cell (lower than bulk estimates of 50-120K)
- HuH7 translates 5.5x more sfGFP per mRNA than 4T1 (from MFI data)
- 4.4% stochastic circuit failure rate accounts for the irreducible OFF-cell leakage

See `docs/phase3_benchmark_report.md` for the full calibration report.

## Key Prediction: Optimal Sensor:Payload Ratio

The optimizer predicts that the commonly used 1:1 sensor:payload ratio is far from optimal:

| S:P Ratio | Sensor | Payload | HuH7 (ON) | 4T1 (OFF) | Selectivity |
|-----------|--------|---------|-----------|-----------|-------------|
| 1:1 (current) | 100ng | 100ng | 28% | 1.3% | 22x |
| **0.15:1 (optimal)** | **26ng** | **174ng** | **94%** | **1.4%** | **68x** |

Reducing sensor to ~15% of total mRNA improves both activation (3.4x more ON cells) and selectivity (3x better ON:OFF ratio) because even a small amount of sensor produces enough L7Ae to repress the payload in OFF cells, while excess sensor creates an unnecessary L7Ae burst in ON cells.

## Design-Experiment-Calibrate Loop

The tool supports an iterative workflow:

```
    DESIGN                    RUN                     CALIBRATE
  (computer)               (bench)                  (computer)
      |                       |                         |
  Generate             Run the experiment          Input flow
  experiment plan      as designed                 cytometry CSV
  with predictions         |                         |
      |                    |                     Fit parameters
  Plate layout,        Flow cytometry            to minimize
  controls,            analysis                  prediction error
  predictions              |                         |
      |                    |                     Updated model
      +--------------------+-------------------------+
                           |
                    IMPROVED PREDICTIONS
                    for next experiment
```

## Directory Structure

```
modeling/
  run.py              # Command-line interface (start here)
  core/               # Core simulation engine
    parameters.py     # Kinetic parameters with literature citations
    and_gate.py       # AND gate ODE model (8 species)
    intracellular.py  # Simple ON/OFF switch model (4 species)
    population.py     # Population-level flow cytometry simulation
    optimizer.py      # Sensor:payload ratio optimization
    experiment.py     # Experiment design and model calibration
  docs/               # Documentation and reports
    phase1_research_and_pseudocode.md
    phase3_benchmark_report.md
  tests/              # Benchmark tests
    test_benchmark.py
```

## Requirements

- Python 3.10+
- NumPy
- SciPy

## Development Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Research and pseudocode | Complete |
| 2 | Core intracellular ODE model | Complete |
| 3 | Benchmark against miR-122 flow data | Complete |
| 4 | AND gate with L7Ae dynamics | Complete |
| 5 | Population layer and optimization | Complete |
| 6 | Stochastic (Gillespie) mode | Planned |
| 7 | Small RNA-seq data integration | Planned |
| 8 | Sensitivity analysis and export | Planned |
| 9 | Full interactive interface (web/GUI) | Planned |

## Integration with Circuit Designer

The circuit designer tool (`tools/circuit_designer.py`) identifies candidate miRNAs from small RNA-seq data and proposes circuit architectures. This modeling tool takes those designs and simulates performance:

```
Small RNA-seq data
    -> Circuit Designer (tools/circuit_designer.py)
        -> Candidate miRNAs and circuit architectures
            -> Modeling Tool (modeling/run.py)
                -> Performance predictions
                    -> Experiment Design
                        -> Experimental validation
                            -> Model calibration (feedback loop)
```
