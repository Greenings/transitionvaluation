# S4 Portfolio — Integrated Impact Assessment

*Assessment date: 2026-04-09 | Model: OSeMOSYS SSP1–5 | Database: EXIOBASE 3.8*

---

## 1. Portfolio Overview

Nine projects across three asset classes (Health, Energy, Transport) spanning
four regions (Africa, Asia, Europe, LATAM).

| Project | Region | Asset | Stage | Investment |
|---------|--------|-------|-------|-----------|
| Proj_001 | LATAM | Health | Development | USD 250.0M |
| Proj_002 | Africa | Health | Development | USD 25.0M |
| Proj_003 | Europe | Health | Operational | USD 75.0M |
| Hydro_AF | Africa | Energy | Refurbishment | USD 30.0M |
| Hydro_AS | Asia | Energy | Large_Scale_Retrofit | USD 150.0M |
| Hydro_EU | Europe | Energy | Efficiency_Tweak | USD 2.0M |
| Rail_EU_DEV | Europe | Transport | Dev | USD 1,998.0M |
| Rail_EU_OP1 | Europe | Transport | Op | USD 0.1M |
| Rail_EU_OP2 | Europe | Transport | Op | USD 0.1M |

**Total portfolio investment:** USD 2,530.2M

---

## 2. Supply-Chain Impact (tvp_dbio)

Leontief power-series decomposition over tiers 0–10.
Calibrated EXIOBASE 3.8 A-matrix with regional intensity multipliers.

Four separate tables are produced, each covering a distinct supply-chain layer:

| Table | Tier | Description |
|-------|------|-------------|
| `supply_chain_tier0.csv` | 0 | Direct investment — one-time CAPEX transaction split across 8 supplying sectors |
| `supply_chain_tier1.csv` | 1 | First upstream round — what Tier 0 suppliers procure; includes bilateral sourcing-country breakdown |
| `supply_chain_tier2.csv` | 2 | Second upstream round — sub-suppliers of Tier 1 |
| `supply_chain_tier3_10.csv` | 3–10 | Deep upstream — aggregated across remaining tiers; accounts for residual supply-chain signal |


### 2.1 Project-level totals

| Project | Region | GHG (tCO2e) | Employment (FTE) | Water (000 m³) | Value Added (M USD) |
|---------|--------|------------|-----------------|---------------|-------------------|
| Hydro_AF | Africa | 20,276 | 792.4 | 130.2 | 31.64 |
| Hydro_AS | Asia | 96,302 | 3,651.2 | 633.7 | 158.21 |
| Hydro_EU | Europe | 818 | 28.1 | 5.2 | 2.11 |
| Proj_001 | LATAM | 130,146 | 5,623.3 | 1,018.5 | 262.76 |
| Proj_002 | Africa | 15,838 | 674.4 | 114.3 | 26.30 |
| Proj_003 | Europe | 26,640 | 1,069.5 | 210.1 | 78.77 |
| Rail_EU_DEV | Europe | 787,208 | 27,837.1 | 5,336.5 | 2,102.40 |
| Rail_EU_OP1 | Europe | 43 | 1.7 | 0.4 | 0.15 |
| Rail_EU_OP2 | Europe | 30 | 1.1 | 0.3 | 0.10 |

**Portfolio totals:** GHG 1,077,302 tCO2e | Employment 39,679 FTE

### 2.2 Key findings

- **Highest GHG footprint:** Rail_EU_DEV (Europe) — 787,208 tCO2e. Driven by Rail_Dev CAPEX concentration in Manufacturing and Construction tiers.
- **Highest employment generation:** Rail_EU_DEV (Europe) — 27,837 FTE. High regional labour intensity multiplier amplifies construction-phase employment.
- **Health sector** (3 projects): 172,624 tCO2e, 7,367 FTE — large LATAM hospital (Proj_001, $250M) dominates due to import leakage in medical equipment supply chains.
- **Energy sector** (3 projects): 117,396 tCO2e — Asia hydro retrofit ($150M) is the single largest contributor; EU efficiency tweak ($2M) is immaterial at portfolio scale.
- **Transport sector** (3 projects): 787,282 tCO2e — Rail_EU_DEV €1.85B development phase accounts for the majority; operational projects (OP1/OP2) are negligible in CAPEX terms.

### 2.3 Positive vs Negative Impact — net ledger (tiers 0–10)

Each indicator is classified by polarity. **Negative impacts** increase
environmental burden; **positive impacts** deliver social or economic benefits.
Hydro avoided CO₂, health beneficiaries, and rail reach are direct project
outcomes read from input files — they are *not* supply-chain quantities.

| Project | Region | [−] GHG tCO2e | [−] Water 000m³ | [+] Jobs FTE | [+] VA M USD | [+] Avoided CO₂ tCO2e | [+] Beneficiaries / Reach |
|---------|--------|--------------|----------------|-------------|----------|----------------------|--------------------------|
| Hydro_AF | Africa | **20,276** | 130.2 | 792 | 31.64 | 150,000 | — |
| Hydro_AS | Asia | **96,302** | 633.7 | 3,651 | 158.21 | 834,218 | — |
| Hydro_EU | Europe | **818** | 5.2 | 28 | 2.11 | 6,126 | — |
| Proj_001 | LATAM | **130,146** | 1,018.5 | 5,623 | 262.76 | 0 | 5,000,000 |
| Proj_002 | Africa | **15,838** | 114.3 | 674 | 26.30 | 0 | 3,000 |
| Proj_003 | Europe | **26,640** | 210.1 | 1,070 | 78.77 | 0 | 500,000 |
| Rail_EU_DEV | Europe | **787,208** | 5,336.5 | 27,837 | 2,102.40 | 0 | 5,500,000 ppl/yr |
| Rail_EU_OP1 | Europe | **43** | 0.4 | 2 | 0.15 | 0 | — |
| Rail_EU_OP2 | Europe | **30** | 0.3 | 1 | 0.10 | 0 | — |

**Portfolio positive outcomes:** 990,344 tCO2e avoided | 5,503,000 health beneficiaries | 5,500,000 rail ppl/yr reached
**Net GHG position:** 1,077,302 tCO2e supply-chain emissions − 990,344 tCO2e avoided = **86,958 tCO2e net** (surplus)

---

## 2.5 Scenario-Weighted Supply-Chain Impact (connected tiers × scenarios)

Each supply-chain tier is adjusted using the sourcing region's own
decarbonisation trajectory — not just the project home region. Tier 1
bilateral sourcing-country data feeds directly into the region-specific
adjustment ratios from tvp_scenario, so that imported steel from Asia
supplying a European project is adjusted at Asia's trajectory, not Europe's.

Four stressors are adjusted per tier:

| Stressor | Ratio used | Source |
|----------|-----------|--------|
| GHG (tCO2e) | `adj_ratio_ghg` | OSeMOSYS grid-intensity trajectory |
| Employment (FTE) | `adj_ratio_employment` | OSeMOSYS renewable-jobs premium |
| Water (000 m³) | `1 − renewable_share × 0.85` ± nexus refinement | IEA Water for Energy + IPCC nexus weights |
| Value Added (M USD) | `adj_ratio_employment` | Labour-productivity proxy |

### 2.5.1 Portfolio totals — scenario-weighted (SSP2-4.5, 2030)

| Project | Region | GHG baseline | GHG 2030 adj | Emp baseline | Emp 2030 adj |
|---------|--------|-------------|--------------|-------------|--------------|
| Hydro_AF | Africa | 19,810 | 10,065 | 777.2 | 854.4 |
| Hydro_AS | Asia | 94,348 | 50,811 | 3,587.4 | 3,882.3 |
| Hydro_EU | Europe | 793 | 524 | 27.3 | 30.3 |
| Proj_001 | LATAM | 127,310 | 94,215 | 5,524.2 | 6,267.3 |
| Proj_002 | Africa | 15,485 | 7,865 | 662.2 | 728.0 |
| Proj_003 | Europe | 25,807 | 17,062 | 1,040.6 | 1,156.3 |
| Rail_EU_DEV | Europe | 762,641 | 504,233 | 27,028.7 | 30,028.9 |
| Rail_EU_OP1 | Europe | 42 | 28 | 1.6 | 1.8 |
| Rail_EU_OP2 | Europe | 29 | 19 | 1.1 | 1.2 |

### 2.5.2 Tier contribution to scenario-adjusted GHG — SSP1 vs SSP5 (2030)

- **Baseline (2020):** 1,046,266 tCO2e portfolio total
- **SSP1-1.9 (2030):** 388,014 tCO2e — 63% reduction
- **SSP5-8.5 (2030):** 859,763 tCO2e — 18% reduction
- **Scenario spread:** 471,749 tCO2e range — driven by sourcing-country divergence in tier 1 bilateral flows.

---

## 2.6 Dependency-Weighted Supply-Chain Impact

Each scenario-adjusted stressor is multiplied by a three-component dependency
factor that captures nature-related risk amplification per tier, sector,
and sourcing region:

| Component | Source | Applies to |
|-----------|--------|-----------|
| **ENCORE ecosystem dependency** | ENCORE v2024 materiality matrix | Project sector × stressor |
| **WWF regional risk** | WRF physical / BRF ecosystem composite | Sourcing region (tier 1 bilateral) |
| **SC sector sensitivity** | IPBES (2019) sector pressure typology | Supplying sector (all tiers) |

dep_factor = 1.0 at global average; range 0.33 (low dependency + low risk)
to 1.67 (high dependency + high risk).

### 2.6.1 Portfolio dep-weighted GHG — SSP2-4.5 (2030)

| Project | Region | GHG adj (tCO2e) | GHG dep-weighted | Water adj (000 m³) | Water dep-weighted |
|---------|--------|----------------|-----------------|-------------------|-------------------|
| Hydro_AF | Africa | 10,065 | 86 | 66.6 | 135.6 |
| Hydro_AS | Asia | 50,811 | 88 | 364.6 | 141.1 |
| Hydro_EU | Europe | 524 | 86 | 3.0 | 122.1 |
| Proj_001 | LATAM | 94,215 | 80 | 601.2 | 105.7 |
| Proj_002 | Africa | 7,865 | 79 | 58.5 | 111.2 |
| Proj_003 | Europe | 17,062 | 78 | 120.1 | 97.7 |
| Rail_EU_DEV | Europe | 504,233 | 71 | 3,041.9 | 87.9 |
| Rail_EU_OP1 | Europe | 28 | 71 | 0.2 | 87.9 |
| Rail_EU_OP2 | Europe | 19 | 71 | 0.1 | 87.9 |

### 2.6.2 Dependency factor profile — sector and region breakdown

Three sub-scores contributing to the dep_factor (scale 1–5, neutral = 3):

| Project sector | ENCORE water dep | ENCORE GHG dep | WWF wrf_physical (Africa) | WWF wrf_physical (Asia) |
|---------------|-----------------|---------------|--------------------------|------------------------|
| Health_Social | 3.33 | 2.00 | 4.97 (Asia) | 4.38 (Africa) |
| Health_Specialized | 3.33 | 2.00 | 4.97 (Asia) | 4.38 (Africa) |
| Health_General | 3.33 | 2.00 | 4.97 (Asia) | 4.38 (Africa) |
| Energy | 5.00 | 2.50 | 4.97 (Asia) | 4.38 (Africa) |
| Rail_Dev | 2.67 | 1.50 | 4.97 (Asia) | 4.38 (Africa) |
| Rail_Op | 2.67 | 1.50 | 4.97 (Asia) | 4.38 (Africa) |

**SC sector sensitivity highlights** (water_dep / ghg_dep / land_dep):

- **Construction**: water 3 | ghg 3 | land 4
- **Energy_Utilities**: water 5 | ghg 5 | land 3
- **Manufacturing**: water 4 | ghg 3 | land 3
- **Transport_Logistics**: water 2 | ghg 3 | land 4
- **Health_Social**: water 5 | ghg 4 | land 2
- **Agriculture**: water 5 | ghg 5 | land 5
- **Mining_Extraction**: water 5 | ghg 3 | land 5
- **Water_Waste**: water 5 | ghg 3 | land 4

---

## 3. SSP Scenario Analysis (tvp_scenario — OSeMOSYS)

GHG intensity adjustment ratios from OSeMOSYS REMIND-MAgPIE calibration.
All five IPCC AR6 Shared Socioeconomic Pathways (SSP1–SSP5).

### 3.1 Scenario-adjusted GHG — all projects (tCO2e)

| Project | Region | Scenario | 2025 | 2030 | 2040 |
|---------|--------|----------|---|---|---|
| Hydro_AF | Africa | SSP1-1.9 | 14,392 | 825 | 452 |
| Hydro_AF | Africa | SSP2-4.5 | 15,254 | 10,185 | 4,072 |
| Hydro_AF | Africa | SSP3-7.0 | 15,631 | 10,142 | 3,852 |
| Hydro_AF | Africa | SSP4-6.0 | 17,162 | 13,139 | 6,642 |
| Hydro_AF | Africa | SSP5-8.5 | 15,572 | 9,769 | 3,599 |
| Hydro_AS | Asia | SSP1-1.9 | 78,919 | 55,268 | 809 |
| Hydro_AS | Asia | SSP2-4.5 | 76,955 | 51,579 | 20,166 |
| Hydro_AS | Asia | SSP3-7.0 | 70,724 | 52,793 | 20,445 |
| Hydro_AS | Asia | SSP4-6.0 | 77,571 | 50,327 | 18,846 |
| Hydro_AS | Asia | SSP5-8.5 | 68,933 | 82,405 | 37,654 |
| Hydro_EU | Europe | SSP1-1.9 | 500 | 256 | 69 |
| Hydro_EU | Europe | SSP2-4.5 | 692 | 548 | 296 |
| Hydro_EU | Europe | SSP3-7.0 | 747 | 678 | 386 |
| Hydro_EU | Europe | SSP4-6.0 | 546 | 276 | 89 |
| Hydro_EU | Europe | SSP5-8.5 | 756 | 689 | 487 |
| Proj_001 | LATAM | SSP1-1.9 | 101,944 | 73,650 | 14,733 |
| Proj_001 | LATAM | SSP2-4.5 | 133,452 | 97,844 | 47,699 |
| Proj_001 | LATAM | SSP3-7.0 | 145,230 | 102,646 | 48,206 |
| Proj_001 | LATAM | SSP4-6.0 | 132,255 | 99,198 | 49,963 |
| Proj_001 | LATAM | SSP5-8.5 | 148,588 | 100,434 | 43,690 |
| Proj_002 | Africa | SSP1-1.9 | 11,242 | 645 | 353 |
| Proj_002 | Africa | SSP2-4.5 | 11,915 | 7,955 | 3,180 |
| Proj_002 | Africa | SSP3-7.0 | 12,209 | 7,922 | 3,009 |
| Proj_002 | Africa | SSP4-6.0 | 13,405 | 10,263 | 5,188 |
| Proj_002 | Africa | SSP5-8.5 | 12,163 | 7,631 | 2,811 |
| Proj_003 | Europe | SSP1-1.9 | 16,261 | 8,333 | 2,243 |
| Proj_003 | Europe | SSP2-4.5 | 22,532 | 17,849 | 9,641 |
| Proj_003 | Europe | SSP3-7.0 | 24,317 | 22,074 | 12,561 |
| Proj_003 | Europe | SSP4-6.0 | 17,774 | 8,972 | 2,885 |
| Proj_003 | Europe | SSP5-8.5 | 24,602 | 22,428 | 15,848 |
| Rail_EU_DEV | Europe | SSP1-1.9 | 480,512 | 246,239 | 66,283 |
| Rail_EU_DEV | Europe | SSP2-4.5 | 665,821 | 527,429 | 284,891 |
| Rail_EU_DEV | Europe | SSP3-7.0 | 718,564 | 652,281 | 371,169 |
| Rail_EU_DEV | Europe | SSP4-6.0 | 525,225 | 265,132 | 85,255 |
| Rail_EU_DEV | Europe | SSP5-8.5 | 726,987 | 662,750 | 468,310 |
| Rail_EU_OP1 | Europe | SSP1-1.9 | 26 | 14 | 4 |
| Rail_EU_OP1 | Europe | SSP2-4.5 | 37 | 29 | 16 |
| Rail_EU_OP1 | Europe | SSP3-7.0 | 40 | 36 | 20 |
| Rail_EU_OP1 | Europe | SSP4-6.0 | 29 | 15 | 5 |
| Rail_EU_OP1 | Europe | SSP5-8.5 | 40 | 37 | 26 |
| Rail_EU_OP2 | Europe | SSP1-1.9 | 18 | 9 | 2 |
| Rail_EU_OP2 | Europe | SSP2-4.5 | 25 | 20 | 11 |
| Rail_EU_OP2 | Europe | SSP3-7.0 | 28 | 25 | 14 |
| Rail_EU_OP2 | Europe | SSP4-6.0 | 20 | 10 | 3 |
| Rail_EU_OP2 | Europe | SSP5-8.5 | 28 | 25 | 18 |

### 3.2 Scenario narrative

- **SSP1-1.9 (Sustainability):** Steepest GHG decline across all regions. By 2030,
  supply-chain GHG falls to 30–40% of 2020 baseline in Europe and below 10% in Asia.
  Rail_EU_DEV is effectively low-carbon by 2030 under full grid decarbonisation.
- **SSP2-4.5 (Middle of the Road):** Moderate decline. Europe falls to ~67% by 2030;
  Africa lags at ~85%, reflecting slower capital deployment and lower carbon pricing.
- **SSP3-7.0 (Regional Rivalry):** Slowest transition. All regions remain above 80%
  of 2020 intensity through 2030. Infrastructure investments locked into fossil-heavy
  supply chains.
- **SSP4-6.0 (Inequality):** Europe decarbonises faster than Africa (ratio 0.34 vs 0.65
  by 2030). Highlights distributional risk: LATAM and Africa health projects face
  higher future supply-chain carbon exposure than European peers.
- **SSP5-8.5 (Fossil-Fuelled Development):** Near-unchanged intensity through 2030 for
  Africa and Asia. Hydro projects in these regions carry significant long-run GHG risk
  from upstream manufacturing and grid-delivered construction energy.

---

## 4. Nature-Related Dependency & Risk (tvp_dependency)

ENCORE materiality screening, WWF Risk Filter Suite, InVEST biophysical
model configuration, and TNFD LEAP financial stress testing.

### 4.1 Risk scores and revenue at risk

| Project | Region | WRF | BRF | High Risk | Revenue at Risk (M USD) |
|---------|--------|-----|-----|-----------|------------------------|
| Hydro_AF | africa | 3.89 | 3.99 | YES | 15.8 |
| Hydro_AS | asia | 4.27 | 4.26 | YES | 83.0 |
| Hydro_EU | europe | 3.62 | 3.23 | YES | 0.8 |
| Proj_001 | latam | 3.48 | 4.09 | YES | 42.0 |
| Proj_002 | africa | 3.51 | 3.60 | YES | 3.6 |
| Proj_003 | europe | 3.31 | 2.97 | no | 0.0 |
| Rail_EU_DEV | europe | 3.38 | 3.13 | no | 0.0 |
| Rail_EU_OP1 | europe | 3.38 | 3.13 | no | 0.0 |
| Rail_EU_OP2 | europe | 3.38 | 3.13 | no | 0.0 |

**High-risk projects:** 5 / 9
**Total revenue at risk:** USD 145.2M

### 4.2 Top ecosystem dependencies (portfolio-wide)

From ENCORE materiality screening across all nine projects:

| Ecosystem Service | Max Score | Material Projects |
|------------------|-----------|-----------------|
| water_supply | 5 | 6 |
| climate_regulation | 5 | 6 |
| freshwater_ecosystem_use | 5 | 3 |
| water_flow_regulation | 5 | 3 |
| air_quality_regulation | 4 | 3 |
| erosion_control | 4 | 6 |
| genetic_materials | 4 | 3 |
| flood_and_storm_protection | 4 | 6 |

### 4.3 Key risk findings

- **5 of 9 projects** are classified high risk on both
  the WWF Water Risk Filter (WRF) and Biodiversity Risk Filter (BRF).
- **Hydro_AS** carries the highest composite scores (WRF 4.27, BRF 4.26) and
  the largest single revenue-at-risk exposure (USD 83.0M). Freshwater ecosystem
  dependency and high biodiversity sensitivity in Asia make this the portfolio's
  critical nature-related risk concentration.
- **Proj_001 (LATAM health, $250M)** is at high risk despite being in the health
  sector: water supply and solid-waste mediation dependencies in LATAM drive WRF
  3.48 and BRF 4.09. Revenue at risk: USD 42.0M.
- **European projects** (Proj_003, Rail_EU_DEV/OP) are generally lower risk,
  protected by stronger regulatory frameworks (high WRF regulatory sub-score)
  and lower physical biodiversity sensitivity.
- **Water supply** is the most pervasive dependency: material in 6/9 projects,
  with maximum dependency score 5/5. All hydro and health projects are exposed.

---

## 5. Integrated Risk Summary

Cross-cutting findings from combining all three analytical passes:

### Compounding risks (high supply-chain GHG AND high nature risk)

| Project | Supply-chain GHG (tCO2e) | WRF | BRF | Revenue at Risk |
|---------|------------------------|-----|-----|----------------|
| Proj_001 | 130,146 | 3.48 | 4.09 | USD 42.0M |
| Hydro_AS | 96,302 | 4.27 | 4.26 | USD 83.0M |
| Hydro_AF | 20,276 | 3.89 | 3.99 | USD 15.8M |
| Proj_002 | 15,838 | 3.51 | 3.60 | USD 3.6M |
| Hydro_EU | 818 | 3.62 | 3.23 | USD 0.8M |

### Scenario-risk interaction

- Under **SSP3/SSP5** (high-emissions pathways), supply-chain GHG remains elevated
  through 2030–2040 for Africa and Asia, compounding the already-high nature risk
  scores of Hydro_AF and Hydro_AS. These projects face a double exposure: upstream
  carbon intensity stays high AND ecosystem services (water supply, freshwater flows)
  degrade under higher warming trajectories.
- Under **SSP1**, Rail_EU_DEV's supply-chain GHG falls rapidly to near-zero by 2035,
  consistent with full grid decarbonisation. With low nature risk scores, this project
  is well-positioned across all risk dimensions.
- **SSP4 inequality dynamic**: Proj_001 (LATAM health) and Proj_002 (Africa health)
  experience slower supply-chain decarbonisation than European counterparts, while
  simultaneously carrying higher nature risk. This asymmetry is the single most
  important portfolio-level finding for impact-at-risk disclosure.

### Priority actions

1. **Hydro_AS** — Commission InVEST Hydropower Water Yield and Sediment Delivery
   Ratio models immediately. USD 83M revenue-at-risk requires site-level biophysical
   quantification before final investment decision.
2. **Proj_001 (LATAM)** — Integrate water-security covenant into financing terms.
   Nature-based wastewater treatment can reduce both WRF physical score and operating
   cost under SSP3/SSP4 water stress scenarios.
3. **Hydro_AF** — Quantify coal displacement avoided GHG against upstream construction
   GHG (currently 150,000 tCO2 avoided vs. significant supply-chain emissions).
   Under SSP3, the avoided-emission benefit shrinks as the grid diversifies slowly.
4. **Portfolio-wide** — Adopt SSP2 as the baseline planning scenario for conservative
   supply-chain GHG disclosure; use SSP1 as the target trajectory for transition
   alignment reporting.

---

## 6. Data and Methodology Notes

| Component | Source | Year |
|-----------|--------|------|
| Supply-chain A matrix | EXIOBASE 3.8.1 (Stadler et al. 2018) | 2018 |
| GHG intensities | EXIOBASE 3.8.1 satellite + IEA 2022 | 2018 |
| Employment intensities | EXIOBASE 3.8.1 + ILO 2022 | 2018 |
| Scenario trajectories | OSeMOSYS / REMIND-MAgPIE | 2020–2050 |
| SSP calibration | IPCC AR6 WG3 (2022) | — |
| ENCORE materiality | ENCORE tool v2.0 | 2023 |
| WWF Risk Filters | WRF 2.0 + BRF 1.0 | 2022 |
| Financial inputs | Project finance CSVs | 2025 |

Tiers computed: 0 to 10. Tiers 0–2 in individual tables; tiers 3–10 aggregated.
Column A spectral radius ≈ 0.52 → geometric decay; tiers >8 contribute <0.1% of signal.
EUR/USD rate: 1.08 (applied to Rail CAPEX inputs).
