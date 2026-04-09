# S4 Portfolio Assessment — Guide

How to run the integrated impact assessment for the nine S4 infrastructure
projects (Health, Energy, Transport) across Africa, Asia, Europe, and LATAM.

---

## What the assessment does

Three independent analytical passes over the same project inputs
(`project_assessment/modeled_input_data/`):

| Pass | Tool | What it measures |
|------|------|-----------------|
| 1 | **tvp_dbio** | Supply-chain GHG, employment, water use, and value added (tiers 0–5) |
| 2 | **tvp_scenario** | SSP1–5 scenario GHG adjustment factors for 2025 / 2030 / 2040 |
| 3 | **tvp_dependency** | Nature-related dependency risk (ENCORE, WWF, InVEST, TNFD LEAP) |

---

## Prerequisites

### Python environment

The simplest setup uses a single conda environment that satisfies all three
submodules. From the repository root:

```bash
conda env create -f tvp_dbio/environment.yml
conda activate env_dbio
pip install -r tvp_scenario/osemosys/requirements.txt
pip install pandas numpy
```

For the dependency pipeline only:

```bash
pip install pandas numpy
# InVEST (optional — only needed to execute biophysical models):
pip install natcap.invest
```

### Scenario results (optional pre-step)

The OSeMOSYS scenario results are **already committed** in
`tvp_scenario/osemosys/results/`. If you need to regenerate them:

```bash
cd tvp_scenario/osemosys
pip install -r requirements.txt
python run_simulation.py          # all 5 SSPs, ~45 s
cd ../..
```

GCAM and MESSAGEix alternatives require compiled C++ / GAMS installations;
see `tvp_scenario/doc/` for full instructions. `assess.py` uses OSeMOSYS
results by default.

---

## Running the assessment

### Full run (recommended)

From the repository root:

```bash
python assess.py
```

This runs all three passes and writes results to `results/`.

### Skip dependency re-run (faster)

The dependency pipeline outputs are already in
`tvp_dependency/assessment_output/`. To load them without re-running:

```bash
python assess.py --skip-dependency
```

### Custom tier range

By default, supply-chain tiers 0–5 are computed (captures >99% of the
upstream signal). To change:

```bash
python assess.py --tiers 0 8    # all tiers including deep upstream
python assess.py --tiers 0 2    # quick run: direct + first two upstream rounds
```

---

## Outputs

All files are written to `results/`:

| File | Description |
|------|-------------|
| `supply_chain.csv` | Tier-by-tier breakdown: sector, GHG, employment, water, value added |
| `supply_chain_summary.csv` | Project totals (tiers summed) |
| `scenario_adjustment.csv` | OSeMOSYS GHG intensity factors per region × scenario × year |
| `scenario_ghg_adjusted.csv` | Scenario-adjusted GHG per project × scenario (pivot table) |
| `dependency_summary.csv` | Merged WWF risk scores and TNFD stress-test table |
| `final_analysis.md` | Narrative synthesis: findings, compounding risks, priority actions |

Additional outputs from the dependency pipeline are in
`tvp_dependency/assessment_output/` (ENCORE materiality tables,
InVEST configs, heatmap).

---

## Running individual passes manually

### Supply-chain only (tvp_dbio)

```python
import sys
sys.path.insert(0, "tvp_dbio")
import tvp_io_lib as io

# Tier-by-tier breakdown for Rail_EU_DEV
df = io.tier_impact(
    invest_usd  = 1_998_000_000,
    sector_code = "Rail_Dev",
    country     = "Europe",
    database    = "exiobase",
    tier_from   = 0,
    tier_to     = 5,
)
print(df.groupby("tier")[["GHG_tCO2e", "Employment_FTE"]].sum())
```

### Scenario factors only (tvp_scenario)

```python
import pandas as pd
factors = pd.read_csv("tvp_scenario/osemosys/results/tvpdbio_intensity_factors.csv")
europe = factors[factors["region"] == "Europe"]
print(europe.pivot_table(index="scenario", columns="year", values="adj_ratio_ghg"))
```

### Dependency pipeline only (tvp_dependency)

```bash
cd tvp_dependency
python -m dependency_profiler.pipeline
# or
python dependency_profiler/pipeline.py
```

---

## Project inputs

All three passes read the same three CSV files:

```
project_assessment/modeled_input_data/
├── assumptions.txt                  Methodology and sector assumptions
├── hospitals_finance_input.csv      Proj_001 (LATAM), Proj_002 (Africa), Proj_003 (Europe)
├── hydro_finance_input.csv          Hydro_AF, Hydro_AS, Hydro_EU
└── rail_finance_input.csv           Rail_EU_DEV, Rail_EU_OP1, Rail_EU_OP2
```

To add or modify projects, edit these CSVs; `assess.py` and the dependency
pipeline both read them at runtime.

---

## Submodule reference

| Submodule | Path | Purpose |
|-----------|------|---------|
| tvp_dbio | `tvp_dbio/` | MRIO supply-chain library (`tvp_io_lib.py`) |
| tvp_scenario | `tvp_scenario/` | OSeMOSYS / GCAM / MESSAGEix SSP simulations |
| tvp_dependency | `tvp_dependency/` | ENCORE / WWF / InVEST / TNFD pipeline |
