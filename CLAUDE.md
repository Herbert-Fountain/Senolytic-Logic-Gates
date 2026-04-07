# CLAUDE.md -- Project Guidance for AI Assistants

## Project Overview

This repo contains tools for designing mRNA-based logic gate circuits that use the
L7Ae/K-turn translational repression system to selectively kill senescent cells.

Two main tools:
- **Circuit designer** (`tools/circuit_designer.py`): identifies miRNA candidates from small RNA-seq data
- **Modeling tool** (`modeling/`): ODE-based simulation of AND gate circuits calibrated against flow cytometry data

## Key Directories

- `modeling/core/` -- Core simulation modules (and_gate.py, population.py, optimizer.py, experiment.py, history.py, bridge.py, parameters.py, flow_parser.py, sensitivity.py)
- `modeling/app.py` -- Streamlit web GUI (launch: `streamlit run modeling/app.py`)
- `modeling/run.py` -- CLI interface
- `modeling/api.py` -- JSON API for programmatic/AI access
- `modeling/data/history.json` -- Persistent experiment database
- `tools/circuit_designer.py` -- miRNA candidate identification
- `analysis/` -- Cross-study synthesis documents

## Important Conventions

- All kinetic parameters have literature citations in `parameters.py`
- The model was calibrated against a miR-122 ON switch experiment (3/31/2026)
- Key calibrated values: L7Ae_repression_fold=1000, miR-122 in HuH7 mean=8000 CV=0.5
- `cells_per_well` is a user-configurable parameter (default 30,000)
- Do not use em dashes in any output
- Keep output professional (no first names in reports)

## Testing

```bash
python modeling/run.py benchmark
```

## Dependencies

numpy, scipy, streamlit, pandas
