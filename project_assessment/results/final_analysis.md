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
| Hydro_AF | Africa | 21,290 | 835.4 | 137.6 | 31.64 |
| Hydro_AS | Asia | 99,279 | 3,769.5 | 659.6 | 158.21 |
| Hydro_EU | Europe | 755 | 25.7 | 4.8 | 2.11 |
| Proj_001 | LATAM | 131,993 | 5,679.2 | 1,033.1 | 262.76 |
| Proj_002 | Africa | 16,610 | 708.4 | 120.2 | 26.30 |
| Proj_003 | Europe | 24,568 | 987.1 | 194.7 | 78.77 |
| Rail_EU_DEV | Europe | 726,415 | 25,489.9 | 4,902.1 | 2,102.40 |
| Rail_EU_OP1 | Europe | 40 | 1.5 | 0.3 | 0.15 |
| Rail_EU_OP2 | Europe | 28 | 1.1 | 0.2 | 0.10 |

**Portfolio totals:** GHG 1,020,980 tCO2e | Employment 37,498 FTE

### 2.2 Key findings

- **Highest GHG footprint:** Rail_EU_DEV (Europe) — 726,415 tCO2e. Driven by Rail_Dev CAPEX concentration in Manufacturing and Construction tiers.
- **Highest employment generation:** Rail_EU_DEV (Europe) — 25,490 FTE. High regional labour intensity multiplier amplifies construction-phase employment.
- **Health sector** (3 projects): 173,171 tCO2e, 7,375 FTE — large LATAM hospital (Proj_001, $250M) dominates due to import leakage in medical equipment supply chains.
- **Energy sector** (3 projects): 121,325 tCO2e — Asia hydro retrofit ($150M) is the single largest contributor; EU efficiency tweak ($2M) is immaterial at portfolio scale.
- **Transport sector** (3 projects): 726,483 tCO2e — Rail_EU_DEV €1.85B development phase accounts for the majority; operational projects (OP1/OP2) are negligible in CAPEX terms.

---

## 3. SSP Scenario Analysis (tvp_scenario — OSeMOSYS)

GHG intensity adjustment ratios from OSeMOSYS REMIND-MAgPIE calibration.
All five IPCC AR6 Shared Socioeconomic Pathways (SSP1–SSP5).

### 3.1 Scenario-adjusted GHG — all projects (tCO2e)

| Project | Region | Scenario | 2025 | 2030 | 2040 |
|---------|--------|----------|---|---|---|
| Hydro_AF | Africa | SSP1-1.9 | 15,112 | 866 | 475 |
| Hydro_AF | Africa | SSP2-4.5 | 16,017 | 10,694 | 4,275 |
| Hydro_AF | Africa | SSP3-7.0 | 16,413 | 10,649 | 4,045 |
| Hydro_AF | Africa | SSP4-6.0 | 18,020 | 13,796 | 6,975 |
| Hydro_AF | Africa | SSP5-8.5 | 16,351 | 10,258 | 3,779 |
| Hydro_AS | Asia | SSP1-1.9 | 81,359 | 56,976 | 834 |
| Hydro_AS | Asia | SSP2-4.5 | 79,334 | 53,174 | 20,789 |
| Hydro_AS | Asia | SSP3-7.0 | 72,911 | 54,425 | 21,077 |
| Hydro_AS | Asia | SSP4-6.0 | 79,970 | 51,883 | 19,429 |
| Hydro_AS | Asia | SSP5-8.5 | 71,064 | 84,953 | 38,818 |
| Hydro_EU | Europe | SSP1-1.9 | 461 | 236 | 64 |
| Hydro_EU | Europe | SSP2-4.5 | 639 | 506 | 273 |
| Hydro_EU | Europe | SSP3-7.0 | 690 | 626 | 356 |
| Hydro_EU | Europe | SSP4-6.0 | 504 | 254 | 82 |
| Hydro_EU | Europe | SSP5-8.5 | 698 | 636 | 449 |
| Proj_001 | LATAM | SSP1-1.9 | 103,390 | 74,695 | 14,942 |
| Proj_001 | LATAM | SSP2-4.5 | 135,346 | 99,233 | 48,376 |
| Proj_001 | LATAM | SSP3-7.0 | 147,291 | 104,103 | 48,890 |
| Proj_001 | LATAM | SSP4-6.0 | 134,132 | 100,605 | 50,672 |
| Proj_001 | LATAM | SSP5-8.5 | 150,697 | 101,859 | 44,310 |
| Proj_002 | Africa | SSP1-1.9 | 11,790 | 676 | 370 |
| Proj_002 | Africa | SSP2-4.5 | 12,496 | 8,343 | 3,335 |
| Proj_002 | Africa | SSP3-7.0 | 12,804 | 8,308 | 3,156 |
| Proj_002 | Africa | SSP4-6.0 | 14,058 | 10,763 | 5,441 |
| Proj_002 | Africa | SSP5-8.5 | 12,756 | 8,003 | 2,948 |
| Proj_003 | Europe | SSP1-1.9 | 14,996 | 7,685 | 2,069 |
| Proj_003 | Europe | SSP2-4.5 | 20,780 | 16,461 | 8,891 |
| Proj_003 | Europe | SSP3-7.0 | 22,426 | 20,357 | 11,584 |
| Proj_003 | Europe | SSP4-6.0 | 16,392 | 8,275 | 2,661 |
| Proj_003 | Europe | SSP5-8.5 | 22,689 | 20,684 | 14,616 |
| Rail_EU_DEV | Europe | SSP1-1.9 | 443,404 | 227,223 | 61,164 |
| Rail_EU_DEV | Europe | SSP2-4.5 | 614,402 | 486,698 | 262,890 |
| Rail_EU_DEV | Europe | SSP3-7.0 | 663,072 | 601,908 | 342,505 |
| Rail_EU_DEV | Europe | SSP4-6.0 | 484,664 | 244,657 | 78,671 |
| Rail_EU_DEV | Europe | SSP5-8.5 | 670,845 | 611,569 | 432,145 |
| Rail_EU_OP1 | Europe | SSP1-1.9 | 24 | 12 | 3 |
| Rail_EU_OP1 | Europe | SSP2-4.5 | 34 | 27 | 14 |
| Rail_EU_OP1 | Europe | SSP3-7.0 | 36 | 33 | 19 |
| Rail_EU_OP1 | Europe | SSP4-6.0 | 27 | 14 | 4 |
| Rail_EU_OP1 | Europe | SSP5-8.5 | 37 | 34 | 24 |
| Rail_EU_OP2 | Europe | SSP1-1.9 | 17 | 9 | 2 |
| Rail_EU_OP2 | Europe | SSP2-4.5 | 23 | 18 | 10 |
| Rail_EU_OP2 | Europe | SSP3-7.0 | 25 | 23 | 13 |
| Rail_EU_OP2 | Europe | SSP4-6.0 | 18 | 9 | 3 |
| Rail_EU_OP2 | Europe | SSP5-8.5 | 26 | 23 | 16 |

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
| Proj_001 | 131,993 | 3.48 | 4.09 | USD 42.0M |
| Hydro_AS | 99,279 | 4.27 | 4.26 | USD 83.0M |
| Hydro_AF | 21,290 | 3.89 | 3.99 | USD 15.8M |
| Proj_002 | 16,610 | 3.51 | 3.60 | USD 3.6M |
| Hydro_EU | 755 | 3.62 | 3.23 | USD 0.8M |

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
