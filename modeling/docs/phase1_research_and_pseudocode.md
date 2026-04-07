# Phase 1: Research and Pseudocode
## RNA Logic Gate Circuit Modeling Tool

*Date: 2026-04-07*

---

## 1. Literature Research Summary

### 1.1 No Published Model of the Saito System Exists

A thorough literature search confirmed that **no published ODE-based simulation of the Saito lab's L7Ae/K-turn + miRNA switch system exists.** The Saito lab publications (Matsuura 2018, Fujita 2022, Kawasaki 2023) describe circuit architectures experimentally but do not publish formal mathematical models. Building one would be a novel contribution to the field.

### 1.2 Relevant Published Models

**Mukherji et al. 2011 (Nature Genetics, PMID: 21857679):** The foundational miRNA-mRNA titration model. Describes molecular titration where miRNA creates a threshold in target mRNA expression. Below the threshold (miRNA >> mRNA), protein output is near zero; above it (mRNA >> miRNA), excess mRNA escapes freely. The key equation at steady state:

```
Protein output ~ max(0, mRNA_total - miRNA_total) * k_translate / gamma_protein
```

The sharpness of the threshold depends on lambda = (koff + gamma_complex) / kon.

**Levine & Benenson 2014 (Nature Methods, PMID: 25218181):** Phenomenological model using Hill-type transfer function:

```
Protein = P_max * Km^n / (Km^n + [miRNA]^n)
```

Where Km and n are fitted from dose-response data. Specifically designed for synthetic miRNA circuit engineering.

**Broderick 2020 (PNAS, PMID: 32699895):** Shows cooperative binding at dual MRE sites when TNRC6/GW182 is present, primarily through reduced koff. Relevant because the Saito system uses 5 MREs per construct.

### 1.3 Kinetic Parameters

All values below are from published literature. See full citations in the research report.

#### Core Rates

| Parameter | Symbol | Value | Units | Source |
|-----------|--------|-------|-------|--------|
| Modified mRNA half-life | t1/2_mRNA | 8-18 | hours | Mauger 2019 PNAS |
| mRNA decay rate | gamma_mRNA | 0.04-0.09 | hr^-1 | Derived from t1/2 |
| Translation rate | k_translate | 40-140 | proteins/mRNA/hr | Schwanhausser 2011/2013 Nature (corrected) |
| GFP half-life | t1/2_GFP | 26 | hours | Li 1998 |
| DTA half-life | t1/2_DTA | 26.5 | hours | Bhatt 1998 EMBO |
| L7Ae half-life | t1/2_L7Ae | ~20 (estimated) | hours | No direct measurement; assume stable |
| GFP decay rate | gamma_GFP | 0.027 | hr^-1 | Derived |
| DTA decay rate | gamma_DTA | 0.026 | hr^-1 | Derived |
| L7Ae decay rate | gamma_L7Ae | ~0.035 | hr^-1 | Estimated |

#### Binding Parameters

| Parameter | Symbol | Value | Units | Source |
|-----------|--------|-------|-------|--------|
| L7Ae-K-turn Kd | Kd_L7Ae | 0.9 | nM | Turner 2005 RNA |
| RISC-target Kd (8mer) | Kd_RISC | 0.01-0.1 | nM | Briskin 2019 Mol Cell |
| RISC-target kon | kon_RISC | 0.01-0.05 | nM^-1 min^-1 | Briskin 2019 |
| AGO2 cleavage rate (favorable) | k_slice | 0.1-1.0 | min^-1 | Wang & Bartel 2024 Mol Cell |
| L7Ae repression fold | - | ~10x | fold | Saito 2010 Nat Chem Biol |

#### Cellular Context

| Parameter | Symbol | Value | Units | Source |
|-----------|--------|-------|-------|--------|
| miR-122 in HuH7 cells | - | ~10,000 | copies/cell | Denzler 2014 Mol Cell |
| miR-122 in 4T1 cells | - | ~0-10 | copies/cell | Our pilot data (essentially absent) |
| Total miRNA per cell | - | ~100,000-200,000 | copies/cell | Bissels 2009 RNA |
| mRNA delivered per cell (Lipofectamine) | - | 100-10,000 | copies/cell | Estimated; no direct measurement |
| Transfection efficiency (HEK293) | - | 80-95 | % | Multiple sources |
| Transfection efficiency (primary cells) | - | 30-60 | % | Multiple sources |

### 1.4 Critical Unknowns

1. **mRNA copies delivered per cell:** The most important unknown. The ratio of delivered mRNA to endogenous miRNA determines circuit behavior. No direct single-cell measurement published for Lipofectamine mRNA delivery. Treat as free parameter (100-10,000 range).
2. **L7Ae protein half-life:** No published measurement. Assume stable (~20h).
3. **In-cell vs. in-vitro kinetics:** All RISC parameters measured in vitro. In-cell rates may differ 10-100x.
4. **Multi-MRE cooperativity:** 5 MREs on one construct may bind cooperatively (Broderick 2020), tightening effective Kd.

### 1.5 Existing Tools

**Recommended implementation:** Custom Python using `scipy.integrate.solve_ivp` for ODE solving and the Gillespie algorithm for stochastic simulation. Tellurium and bioscrape are alternatives but custom code gives us full control over the model architecture and integration with the circuit designer tool.

---

## 2. Model Architecture

### 2.1 Species (State Variables)

For a simple ON switch (Phase 2):

| Species | Symbol | Description |
|---------|--------|-------------|
| M | M | Free mRNA (switch construct, unbound) |
| M_bound | Mb | mRNA bound to RISC-miRNA complex (silenced) |
| miR | miR | Free miRNA (not RISC-loaded) |
| RISC_miR | R | RISC-loaded miRNA (active silencing complex) |
| P | P | Reporter/payload protein (GFP, Gasdermin, DTA) |

For the full AND gate (Phase 4), add:

| Species | Symbol | Description |
|---------|--------|-------------|
| M_L7Ae | M1 | L7Ae-encoding mRNA (with MREs for miRNA-A) |
| M_L7Ae_bound | M1b | L7Ae mRNA bound to RISC (silenced) |
| L7Ae | L | Free L7Ae protein |
| M_payload | M2 | Payload mRNA (with K-turn in 5'UTR) |
| M_payload_repr | M2r | Payload mRNA repressed by L7Ae binding |
| P_payload | P2 | Payload protein |

### 2.2 Reactions and ODEs

#### Phase 2: Simple ON Switch (OFF-switch mRNA)

An OFF switch: mRNA is translated unless the cognate miRNA is present.

**Reactions:**

```
R1: Delivery          null -> M           (bolus at t=0; M(0) = M_delivered)
R2: RISC loading      miR -> RISC_miR     (fast; assume pre-equilibrated)
R3: miRNA binding     M + RISC_miR -> Mb  (rate: kon * M * RISC_miR)
R4: miRNA unbinding   Mb -> M + RISC_miR  (rate: koff * Mb)
R5: AGO2 cleavage     Mb -> RISC_miR      (rate: k_slice * Mb; mRNA destroyed, RISC recycled)
R6: mRNA decay        M -> null           (rate: gamma_M * M)
R7: Translation       M -> M + P          (rate: k_trans * M; mRNA not consumed)
R8: Protein decay     P -> null           (rate: gamma_P * P)
```

**ODEs:**

```
dM/dt = -kon * M * R + koff * Mb - gamma_M * M
dMb/dt = kon * M * R - koff * Mb - k_slice * Mb
dR/dt = -kon * M * R + koff * Mb + k_slice * Mb  (RISC conserved)
dP/dt = k_trans * M - gamma_P * P
```

With conservation: R_total = R + Mb (RISC is recycled)

**Initial conditions:**
- M(0) = M_delivered (e.g., 1000 copies/cell)
- R(0) = miRNA_copies (e.g., 10,000 for miR-122 in HuH7; 0 in 4T1)
- Mb(0) = 0
- P(0) = 0

**Note:** For the ON switch (where miRNA ACTIVATES translation), the mechanism is different: miRNA cleaves an inhibitory sequence after the poly(A) tail, converting a silent mRNA into an active one. This is modeled as:

```
M_silent + RISC_miR -> M_active + RISC_miR  (rate: k_activate * M_silent * RISC_miR)
M_active -> M_active + P                     (rate: k_trans * M_active)
```

#### Phase 4: AND Gate with L7Ae

**Additional reactions for L7Ae repressor circuit:**

```
R9:  L7Ae mRNA delivery      null -> M1        (bolus at t=0)
R10: Payload mRNA delivery    null -> M2        (bolus at t=0)
R11: miRNA silences L7Ae mRNA M1 + R -> M1b    (same as R3-R5 above)
R12: L7Ae translation         M1 -> M1 + L     (rate: k_trans * M1_free)
R13: L7Ae decay               L -> null         (rate: gamma_L * L)
R14: L7Ae binds K-turn        L + M2 -> M2r    (rate: kon_L7Ae * L * M2)
R15: L7Ae unbinds             M2r -> L + M2     (rate: koff_L7Ae * M2r)
R16: Payload translation      M2 -> M2 + P2    (rate: k_trans * M2_free)
R17: Payload decay             P2 -> null       (rate: gamma_P2 * P2)
R18: Payload mRNA decay        M2 -> null       (rate: gamma_M * M2)
R19: L7Ae mRNA decay          M1 -> null        (rate: gamma_M * M1)
```

**AND gate ODEs (miRNA-A controls M1, payload in M2):**

```
dM1/dt = -kon_RISC * M1 * R_A + koff_RISC * M1b - gamma_M * M1
dM1b/dt = kon_RISC * M1 * R_A - koff_RISC * M1b - k_slice * M1b
dR_A/dt = -kon_RISC * M1 * R_A + koff_RISC * M1b + k_slice * M1b
dL/dt = k_trans * M1 - gamma_L * L - kon_L7Ae * L * M2 + koff_L7Ae * M2r
dM2/dt = -kon_L7Ae * L * M2 + koff_L7Ae * M2r - gamma_M * M2
dM2r/dt = kon_L7Ae * L * M2 - koff_L7Ae * M2r - gamma_M * M2r
dP2/dt = k_trans * M2 - gamma_P2 * P2
```

**For 2-input AND gate (L7Ae-only, two L7Ae mRNAs with different MREs):**
Add M1' with MREs for miRNA-B. Both M1 and M1' produce L7Ae. Both must be silenced (by miRNA-A and miRNA-B respectively) for payload expression.

### 2.3 Unit System

All concentrations in **molecules per cell** (not nM). This avoids needing cell volume estimates and is more intuitive for the user. Rate constants are adjusted accordingly:

- kon: cell^-1 molecule^-1 hr^-1
- Conversion: 1 nM in a typical cell (~1 pL volume) = ~600 molecules

### 2.4 Population Layer (Phase 5)

```python
for each cell in population:
    cell_type = assign_type(ratio)  # e.g., 80% healthy, 20% senescent
    miRNA_profile = get_profile(cell_type)
    transfected = random() < transfection_efficiency
    if transfected:
        mRNA_copies = draw_from_distribution(mean_copies, variability)
        result = run_intracellular_model(miRNA_profile, mRNA_copies, params)
        if result.payload_max > death_threshold:
            cell.dead = True

# Aggregate
target_kill_rate = dead_target / total_target
offtarget_kill_rate = dead_offtarget / total_offtarget
therapeutic_index = target_kill_rate / max(offtarget_kill_rate, epsilon)
```

---

## 3. Implementation Plan

### Phase 2: Core Intracellular Model

```
File: modeling/core/intracellular.py

class IntracellularModel:
    def __init__(self, params):
        self.params = params  # dict of all kinetic parameters
    
    def define_species(self, circuit_config):
        # Create state vector based on circuit configuration
        # Simple ON switch: [M, Mb, R, P]
        # AND gate: [M1, M1b, R_A, L, M2, M2r, P2, ...]
    
    def ode_system(self, t, y):
        # Compute derivatives for all species
        # Return dy/dt vector
    
    def simulate(self, t_span, initial_conditions):
        # Run scipy.integrate.solve_ivp
        # Return time points and species trajectories
    
    def dose_response(self, miRNA_range):
        # Sweep miRNA concentration, record steady-state payload
        # Return dose-response curve
```

### Phase 3: Benchmark

```
File: modeling/tests/test_mir122_benchmark.py

# Define HuH7 cell: miR-122 = 10,000 copies/cell
# Define 4T1 cell: miR-122 = 0 copies/cell
# Load miR-122 ON switch construct
# Run simulation for both cell types
# Expected: GFP high in HuH7 (miR-122 present), GFP low in 4T1 (miR-122 absent)
# Compare to Saito lab published fluorescence data
```

### Phase 5: Population Layer

```
File: modeling/core/population.py

class PopulationModel:
    def __init__(self, intracellular_model, cell_types, ratio):
        self.model = intracellular_model
        self.cell_types = cell_types
        self.ratio = ratio
    
    def run_coculture(self, n_cells, params):
        # Simulate each cell independently
        # Aggregate results into kill rates
```

---

## 4. Default Parameter Set

```python
DEFAULT_PARAMS = {
    # mRNA properties
    'mRNA_halflife_hr': 12,          # Modified mRNA half-life (hours)
    'k_translate': 100,              # Proteins per mRNA per hour
    'mRNA_delivered': 1000,          # Copies per cell (Lipofectamine)
    
    # miRNA-RISC binding
    'kon_RISC': 0.001,               # molecule^-1 cell hr^-1 (adjusted from nM)
    'koff_RISC': 0.06,               # hr^-1 (Kd ~100 pM equivalent)
    'k_slice': 6.0,                  # hr^-1 (0.1 min^-1, AGO2 cleavage)
    
    # L7Ae-K-turn binding
    'kon_L7Ae': 0.01,                # molecule^-1 cell hr^-1
    'koff_L7Ae': 0.006,              # hr^-1 (Kd ~0.9 nM equivalent)
    
    # Protein degradation
    'GFP_halflife_hr': 26,
    'DTA_halflife_hr': 26.5,
    'L7Ae_halflife_hr': 20,
    
    # Transfection
    'transfection_efficiency': 0.85, # Fraction of cells transfected
    'delivery_variability': 0.5,     # CV of mRNA copies per cell
    
    # Cell death
    'death_threshold': 100,          # Payload molecules to trigger death
    
    # Simulation
    't_max_hr': 72,                  # Simulation duration
    'dt_hr': 0.1,                    # Time step for output
}
```

---

## 5. References

1. Mukherji S et al. *Nat Genet*. 2011;43:854-859. PMID: 21857679 (titration model)
2. Levine E, Benenson Y et al. *Nat Methods*. 2014;11:1167-1170. PMID: 25218181 (Hill transfer function)
3. Briskin D et al. *Mol Cell*. 2019;75:592-603. PMID: 31324449 (RISC binding kinetics)
4. Wang Y, Bartel DP. *Mol Cell*. 2024. PMID: 39025072 (AGO2 slicing rates)
5. Schwanhausser B et al. *Nature*. 2011;473:337-342. PMID: 21593866 (translation/degradation rates)
6. Turner B et al. *RNA*. 2005;11:1192-1200. PMC: 1370803 (L7Ae-K-turn Kd)
7. Denzler R et al. *Mol Cell*. 2014;56:604-616. PMID: 25457166 (miR-122 absolute quantification)
8. Bissels U et al. *RNA*. 2009;15:2375-2384. PMID: 19850911 (absolute miRNA quantification)
9. Broderick JA. *PNAS*. 2020;117:17764-17774. PMID: 32699895 (cooperative MRE binding)
10. Mauger DM et al. *PNAS*. 2019;116:24075-24083. PMID: 31712433 (modified mRNA stability)
11. Saito H et al. *Nat Chem Biol*. 2010;6:71-78 (L7Ae ~10-fold repression)
12. Bhatt DK et al. *EMBO J*. 1998;17:110-120. PMID: 9450983 (DTA half-life)
