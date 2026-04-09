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

Leontief power-series decomposition over tiers 0–5.
Calibrated EXIOBASE 3.8 A-matrix with regional intensity multipliers.

### 2.1 Project-level totals

| Project | Region | GHG (tCO2e) | Employment (FTE) | Water (000 m³) | Value Added (M USD) |
|---------|--------|------------|-----------------|---------------|-------------------|
| Hydro_AF | Africa | 21,065 | 826.6 | 135.8 | 31.27 |
| Hydro_AS | Asia | 98,228 | 3,729.5 | 650.9 | 156.37 |
| Hydro_EU | Europe | 748 | 25.4 | 4.7 | 2.08 |
| Proj_001 | LATAM | 130,595 | 5,627.8 | 1,021.9 | 260.06 |
| Proj_002 | Africa | 16,437 | 701.6 | 118.8 | 26.02 |
| Proj_003 | Europe | 24,309 | 977.9 | 192.6 | 77.97 |
| Rail_EU_DEV | Europe | 718,847 | 25,223.4 | 4,841.6 | 2,078.81 |
| Rail_EU_OP1 | Europe | 40 | 1.5 | 0.3 | 0.14 |
| Rail_EU_OP2 | Europe | 27 | 1.1 | 0.2 | 0.10 |

**Portfolio totals:** GHG 1,010,296 tCO2e | Employment 37,115 FTE

### 2.2 Key findings

- **Highest GHG footprint:** Rail_EU_DEV (Europe) — 718,847 tCO2e. Driven by Rail_Dev CAPEX concentration in Manufacturing and Construction tiers.
- **Highest employment generation:** Rail_EU_DEV (Europe) — 25,223 FTE. High regional labour intensity multiplier amplifies construction-phase employment.
- **Health sector** (3 projects): 171,341 tCO2e, 7,307 FTE — large LATAM hospital (Proj_001, $250M) dominates due to import leakage in medical equipment supply chains.
- **Energy sector** (3 projects): 120,041 tCO2e — Asia hydro retrofit ($150M) is the single largest contributor; EU efficiency tweak ($2M) is immaterial at portfolio scale.
- **Transport sector** (3 projects): 718,914 tCO2e — Rail_EU_DEV €1.85B development phase accounts for the majority; operational projects (OP1/OP2) are negligible in CAPEX terms.

---

## 3. SSP Scenario Analysis (tvp_scenario — OSeMOSYS)

GHG intensity adjustment ratios from OSeMOSYS REMIND-MAgPIE calibration.
All five IPCC AR6 Shared Socioeconomic Pathways (SSP1–SSP5).

### 3.1 Scenario-adjusted GHG — all projects (tCO2e)

| Project | Region | Scenario | 2025 | 2030 | 2040 |
|---------|--------|----------|---|---|---|
| Hydro_AF | Africa | SSP1-1.9 | 14,952 | 857 | 470 |
| Hydro_AF | Africa | SSP2-4.5 | 15,847 | 10,581 | 4,230 |
| Hydro_AF | Africa | SSP3-7.0 | 16,239 | 10,537 | 4,002 |
| Hydro_AF | Africa | SSP4-6.0 | 17,829 | 13,650 | 6,901 |
| Hydro_AF | Africa | SSP5-8.5 | 16,178 | 10,149 | 3,739 |
| Hydro_AS | Asia | SSP1-1.9 | 80,498 | 56,373 | 825 |
| Hydro_AS | Asia | SSP2-4.5 | 78,494 | 52,611 | 20,569 |
| Hydro_AS | Asia | SSP3-7.0 | 72,139 | 53,849 | 20,854 |
| Hydro_AS | Asia | SSP4-6.0 | 79,123 | 51,334 | 19,223 |
| Hydro_AS | Asia | SSP5-8.5 | 70,312 | 84,054 | 38,407 |
| Hydro_EU | Europe | SSP1-1.9 | 456 | 234 | 63 |
| Hydro_EU | Europe | SSP2-4.5 | 632 | 501 | 271 |
| Hydro_EU | Europe | SSP3-7.0 | 682 | 620 | 352 |
| Hydro_EU | Europe | SSP4-6.0 | 499 | 252 | 81 |
| Hydro_EU | Europe | SSP5-8.5 | 690 | 629 | 445 |
| Proj_001 | LATAM | SSP1-1.9 | 102,295 | 73,903 | 14,783 |
| Proj_001 | LATAM | SSP2-4.5 | 133,912 | 98,181 | 47,863 |
| Proj_001 | LATAM | SSP3-7.0 | 145,730 | 103,000 | 48,372 |
| Proj_001 | LATAM | SSP4-6.0 | 132,710 | 99,539 | 50,135 |
| Proj_001 | LATAM | SSP5-8.5 | 149,100 | 100,780 | 43,841 |
| Proj_002 | Africa | SSP1-1.9 | 11,667 | 669 | 366 |
| Proj_002 | Africa | SSP2-4.5 | 12,366 | 8,256 | 3,301 |
| Proj_002 | Africa | SSP3-7.0 | 12,671 | 8,222 | 3,123 |
| Proj_002 | Africa | SSP4-6.0 | 13,912 | 10,651 | 5,385 |
| Proj_002 | Africa | SSP5-8.5 | 12,624 | 7,919 | 2,918 |
| Proj_003 | Europe | SSP1-1.9 | 14,838 | 7,604 | 2,047 |
| Proj_003 | Europe | SSP2-4.5 | 20,561 | 16,287 | 8,798 |
| Proj_003 | Europe | SSP3-7.0 | 22,190 | 20,143 | 11,462 |
| Proj_003 | Europe | SSP4-6.0 | 16,219 | 8,187 | 2,633 |
| Proj_003 | Europe | SSP5-8.5 | 22,450 | 20,466 | 14,462 |
| Rail_EU_DEV | Europe | SSP1-1.9 | 438,784 | 224,855 | 60,527 |
| Rail_EU_DEV | Europe | SSP2-4.5 | 608,001 | 481,628 | 260,151 |
| Rail_EU_DEV | Europe | SSP3-7.0 | 656,164 | 595,637 | 338,936 |
| Rail_EU_DEV | Europe | SSP4-6.0 | 479,615 | 242,108 | 77,851 |
| Rail_EU_DEV | Europe | SSP5-8.5 | 663,855 | 605,198 | 427,642 |
| Rail_EU_OP1 | Europe | SSP1-1.9 | 24 | 12 | 3 |
| Rail_EU_OP1 | Europe | SSP2-4.5 | 33 | 26 | 14 |
| Rail_EU_OP1 | Europe | SSP3-7.0 | 36 | 33 | 19 |
| Rail_EU_OP1 | Europe | SSP4-6.0 | 26 | 13 | 4 |
| Rail_EU_OP1 | Europe | SSP5-8.5 | 36 | 33 | 24 |
| Rail_EU_OP2 | Europe | SSP1-1.9 | 17 | 9 | 2 |
| Rail_EU_OP2 | Europe | SSP2-4.5 | 23 | 18 | 10 |
| Rail_EU_OP2 | Europe | SSP3-7.0 | 25 | 23 | 13 |
| Rail_EU_OP2 | Europe | SSP4-6.0 | 18 | 9 | 3 |
| Rail_EU_OP2 | Europe | SSP5-8.5 | 25 | 23 | 16 |

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
| Proj_001 | 130,595 | 3.48 | 4.09 | USD 42.0M |
| Hydro_AS | 98,228 | 4.27 | 4.26 | USD 83.0M |
| Hydro_AF | 21,065 | 3.89 | 3.99 | USD 15.8M |
| Proj_002 | 16,437 | 3.51 | 3.60 | USD 3.6M |
| Hydro_EU | 748 | 3.62 | 3.23 | USD 0.8M |

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

Tiers summed: 0 to 5 (captures >99% of supply-chain signal for A spectral radius ≈ 0.52).
EUR/USD rate: 1.08 (applied to Rail CAPEX inputs).
