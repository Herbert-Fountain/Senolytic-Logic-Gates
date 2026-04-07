# RNA Logic Gate Circuit Modeling Tool

Simulates the dynamics of mRNA-based logic gate circuits to predict circuit performance before wet-lab experiments.

## Status: Phase 1 (Research and Architecture)

## Directory Structure

```
modeling/
  core/           # Core simulation engine (ODE solver, Gillespie algorithm)
  interface/      # Interactive UI (sliders, plots, configuration)
  data/           # Small RNA-seq import and processing
  docs/           # Model documentation, equations, parameter references
  tests/          # Validation tests and benchmarks
  results/        # Simulation output logs (JSON/CSV)
```

## Development Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Research and pseudocode | In progress |
| 2 | Core intracellular ODE model (single ON switch) | Pending |
| 3 | Benchmark against miR-122 HuH7/4T1 data | Pending |
| 4 | Multi-construct, AND gate, L7Ae dynamics | Pending |
| 5 | Population layer and co-culture | Pending |
| 6 | Stochastic (Gillespie) mode | Pending |
| 7 | Small RNA-seq data integration | Pending |
| 8 | Sensitivity analysis and export | Pending |
| 9 | Full interactive interface | Pending |

## Integration with Circuit Designer

The circuit designer tool (`tools/circuit_designer.py`) identifies candidate miRNAs and proposes circuit architectures. This modeling tool takes those designs and simulates their expected performance, answering questions like:

- Will the proposed miRNA fold change produce sufficient ON/OFF switching?
- How sensitive is the circuit to delivery dose and transfection variability?
- What kill rate and therapeutic index can we expect in a co-culture experiment?

Together, the two tools form a complete computational pipeline:
**Data -> Circuit Designer -> Modeling Tool -> Experiment Design**
