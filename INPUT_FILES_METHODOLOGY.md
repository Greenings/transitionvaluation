# Input Files Methodology and Data Origins

**All Six Value Factor Systems — Input Files and Data Provenance**
**Version**: 2.0
**Last Updated**: 2026-03-09

This document provides comprehensive documentation of input files and primary data sources used across all six value factor systems in the transitionvaluation framework (WifOR, EPS 2015d.1, UBA MC 4.0, CE Delft 2024, UK Wellbeing, eQALY). For each indicator a cross-system overview table is provided; detailed WifOR-specific methodology follows. Detailed input file documentation for CE Delft, UK Wellbeing, and eQALY is maintained in their respective submodule `INPUT_FILES_METHODOLOGY.md` files.

---

## Table of Contents

1. [Overview](#overview)
2. [Ecosystem Context](#ecosystem-context)
3. [General Framework](#general-framework)
4. [Shared Input Files](#shared-input-files)
5. [Indicator-Specific Input Files](#indicator-specific-input-files)
6. [External Sources and License Information](#external-sources-and-license-information)

---

## Overview

### Purpose

This documentation serves to:
- **Trace Data Provenance**: Document where each input file originates
- **Explain Methodologies**: Describe how pre-calculated values were derived
- **Enable Updates**: Provide information needed to refresh data files
- **Support Transparency**: Make methodologies open and auditable

### Input File Categories

Input files are organized into two categories:

1. **Shared Dependencies** (2 files): Used by all 8 value factor scripts
   - Model definitions (countries, sectors)
   - World Bank GDP deflators

2. **Indicator-Specific Data** (8 files): One per value factor
   - Pre-calculated damage costs or benefit coefficients
   - Source varies: External databases, academic research, or internal calculations

---

## Ecosystem Context

TVP input files are part of a broader ecosystem of impact valuation methodologies:

### Provider Landscape

**Tier 1: Public Good Methodologies**
- IFVI/VBA: Baseline methodology (open-source)
- Transparent/NCMA: EU-funded framework
- EPS (Chalmers): Academic open-access

**Tier 2: Established Providers**
- WifOR Institute: TVP foundation (15+ years)
- GIST Impact: 13,000+ companies covered
- Upright Project: Open-access platform

**Tier 3: Specialized Providers**
- CE Delft: LCA-based (ReCiPe)
- Valuing Impact: eQALY methodology
- Richmond Global Sciences: Financial integration

### Methodology Comparison

**GHG Example:**
- IFVI/VBA: USD 236/tonne CO2 (SCC, DICE model, 2023)
- WifOR: [current value] (Nordhaus DICE)
- GIST Impact: USD 180-250/tonne (FUND model)
- Upright: USD 417/tonne (comprehensive IAM)
- CE Delft: USD 150-200/tonne (ReCiPe)

**Convergence Trend:** Methodologies increasingly aligned through Value Commission transparency requirements

---

## General Framework

### WifOR Institute Foundation

All input files are integral to the **WifOR Institute's Impact Valuation framework**, developed by an independent economic research institute.

**Primary Objective**: Facilitate **Impact Valuation** by monetizing environmental and social impacts of business activities.

### Guiding Principles

#### 1. Value to Society Perspective
- Prioritize holistic costs and benefits to society
- Extend beyond financial implications for businesses
- Capture full social and environmental externalities

#### 2. Damage Cost Approach (Societal Perspective)

**What "Damage or Value to Society" Means:**

These values represent **total external costs or benefits to society**, not legal liability or company financial impacts.

- **Primary Method**: Estimate monetary costs of damages to society as a whole
  - Example: Health expenditures due to air pollution across entire affected population
  - Includes: Medical costs, lost productivity, premature mortality, reduced quality of life
  - Perspective: Society's total burden, not company's legal liability

- **Alternative Methods** (when direct societal costs infeasible):
  - **Abatement cost**: Expense society would pay to prevent the damage
  - **Willingness-to-pay**: What society values the benefit/cost at (market-based)

**Critical Distinction:**

| Aspect | Damage/Value to Society | Legal Liability / Company Cost |
|--------|------------------------|-------------------------------|
| **Scope** | All affected parties (even those who can't sue) | Only successful legal claims |
| **Perspective** | Society's total welfare loss/gain | Company's financial exposure |
| **Coverage** | Non-market values (air quality, biodiversity) | Compensable damages only |
| **Time Horizon** | Long-term, future generations | Current legal framework |
| **Example (Air Pollution)** | $5M in societal health costs from PM2.5 | $100K in fines + settlements |

**Use Case:** These societal values inform impact materiality, investment decisions, and strategic planning—NOT financial accounting for legal liabilities or compliance penalties.

#### 3. Academic and Institutional Foundation
- Built on authoritative research
- Sources include:
  - German Federal Environment Agency (UBA)
  - World Health Organization (WHO)
  - Intergovernmental Panel on Climate Change (IPCC)
  - Peer-reviewed academic publications

#### 4. Transparency
- All methodologies thoroughly documented
- Sources publicly shared
- Contributes to standardization in impact valuation
- Enables open discussion and peer review

### Data Flow

```
External Sources          Internal Calculations
(OECD, UBA, WHO, etc.)   (WifOR Methodology)
         │                        │
         └────────┬───────────────┘
                  │
         ┌────────▼────────┐
         │  Pre-calculated │
         │  Input Files    │
         │  (10 files)     │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │  Python Scripts │
         │  (8 indicators) │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │  Final Value    │
         │  Factor Outputs │
         └─────────────────┘
```

---

## Shared Input Files

### 1. Model Definitions

**File**: `Model_definitions_owntable.h5`

#### Origin
- **Source**: Internal WifOR database
- **Type**: Structural foundation data
- **Update Frequency**: Annual (low change frequency)

#### Contents
- **188 Countries**: ISO3 country codes (e.g., USA, DEU, CHN)
- **NACE Sectors**: Economic sector classifications
- **Purpose**: Provides dimensional structure for all outputs

#### Data Structure
```python
# HDF5 Key: 'owntable'
# Columns:
#   - country_code (ISO3)
#   - sector_code (NACE)
#   - Additional metadata
```

#### Methodology
- **Country List**: Based on UN member states and recognized territories
- **Sector Classification**: NACE Rev. 2 (Nomenclature of Economic Activities)
- **Maintained By**: WifOR Institute

#### Known Mappings
Country codes may require harmonization:
- SSD (South Sudan old) → SDS (South Sudan current)
- SDN (Sudan old) → SUD (Sudan current)

---

### 2. World Bank GDP Deflators

**File**: `241001_worldbank_deflator.h5`

#### Origin
- **Source**: World Bank Open Data
- **Indicator**: NY.GDP.DEFL.ZS (GDP deflator)
- **Current Version**: 2024-10-01
- **Update Frequency**: Quarterly

#### Purpose
- Enable temporal consistency via inflation adjustment
- Convert coefficients to constant base-year USD
- Applied globally using USA deflator (see ARCHITECTURE_DECISIONS.md ADR-001)

#### Data Structure
```python
# HDF5 Key: 'deflator'
# Index: year (int)
# Columns: country_code (ISO3)
# Values: GDP deflator (base year = 100)
```

#### Methodology
- **Deflator Calculation**: Based on GDP in current vs constant local currency
- **Base Year**: 100 (varies by country, typically recent year)
- **Normalization**: Scripts normalize to specific base year (2020 for most, 2019 for GHG)

#### Usage in Scripts
```python
# Calculate inflation factor
inflation_factor[year] = deflator[USA, year] / deflator[USA, base_year]

# Apply to coefficients
coefficient[year] = coefficient[base] × inflation_factor[year]
```

#### Public Database
- **World Bank Data**: https://data.worldbank.org
- **Direct API**: Can be fetched using `wbdata` Python library

---

## Indicator-Specific Input Files

This section documents input files and primary data sources for all six value factor systems. For each indicator a **Cross-System Input Sources** table appears first, followed by the detailed WifOR-specific file documentation.

### System Coverage Overview

| System | Folder | Indicators covered | Primary source |
|--------|--------|--------------------|----------------|
| **WifOR** | `value-factors/` | GHG, Air, Waste, Water consumption, Land use, Water pollution, Training, OHS | DICE/RICE; UBA/NEEDS; EPS/LANCA; USEtox; Psacharopoulos 2018; IHME GBD |
| **EPS 2015d.1** | `stockholm-value-factors/` | GHG, Air, N/P water, Waste, Land use, Heavy metals, Refrigerants, Noise, VOCs, Fossil resources, Radionuclides, Pesticides, Critical minerals | EPS 2015d.1 index (Steen 2015); 892 substances |
| **UBA MC 4.0** | `uba-value-factors/` | GHG, Air, Noise, N/P water, Refrigerants, Electricity, Heat, Transport, Agriculture | GIVE model (Anthoff 2025); EcoSenseWeb v1.3; UBA Handbook Tables 1–27 (Eser et al. 2025) |
| **CE Delft 2024** | `cedelft-value-factors/` | GHG, Air, N/P water, Land use, Heavy metals, Fossil ADP, Radionuclides, Critical minerals | Environmental Prices Handbook EU27 (De Vries et al. 2025) |
| **UK Wellbeing** | `uk-value-factors/` | WELLBY/QALY, Discount rates, Cultural engagement health | HM Treasury Green Book 2026; NICE HTA; Wellbeing Guidance 2021 |
| **eQALY** | `valuingimpact-value-factors/` | GHG (NatCap), Air (NatCap), N/P water (NatCap), Land use (LANCA), Water consumption, Training, OHS, Health DALY rates, HUI, HUT | IHME GBD 2019; World Bank; IMF WEO; LANCA v2.0; HUI/HUT welfare model |

---

### 1. Greenhouse Gas Emissions (GHG)

**File**: `20241022_scc_nordhaus.h5`
**Script**: `020_241024_prepare_GHG_my.py`

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | `20241022_scc_nordhaus.h5` | DICE/RICE (Nordhaus & Barrage 2024) — integrated assessment model; global SCC trajectory | USD (mixed) |
| **EPS 2015d.1** | EPS 2015d.1 index — `001_inorganic_gases` (Steen 2015) | Climate damage pathway via YOLL (50,000 ELU/person-year) + crop + fish + coastal | EUR 2015 |
| **UBA MC 4.0** | GIVE model (Anthoff 2025) → *UBA Handbook Table 1* (Eser et al. 2025) | Equity-weighted global SCC; 0 % and 1 % PRTP; direct CH₄/N₂O modelling (not GWP100 proxies) | EUR 2025 |
| **CE Delft 2024** | *Environmental Prices Handbook EU27* (De Vries et al. 2025) | Literature-based SCC; CO₂, CH₄, N₂O | EUR 2021 |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | NatCap GHG pathway; IHME GBD 2019 burden data | Income-utility–weighted climate damage | USD 2023 |

*WifOR-specific methodology below. For UBA MC 4.0: the GIVE (Global Impacts and Valuation of Emissions) model replaces DICE; it applies equity-weighting with German income as reference and provides two PRTP scenarios.*

#### Origin
- **Source**: DICE Model (Dynamic Integrated Climate-Economy)
- **Version**: 2024 iteration
- **Developer**: Barrage and William Nordhaus (Nobel laureate)
- **Current Version**: 2024-10-22 (most recent input file)

#### Methodology: Social Cost of Carbon (SCC)
- **Definition**: Monetary value of future economic harm from emitting one ton of CO2 today
- **Approach**: Integrated assessment model linking climate science with economics
- **Time Horizon**: Damages discounted to present value

#### Key Features
- **Global Value**: Same SCC for all countries (climate change is global)
- **Year-Specific**: Different SCC values by year (increases over time)
- **Scenario-Based**: Multiple scenarios with different assumptions
  - Discount rates: 1.5%, 2.5%, 5%
  - Climate sensitivity: Low, medium, high

#### Data Structure
```python
# HDF5 Key: 'df'
# Index: Multi-level (year, scenario)
# Values: SCC in USD/tonne CO2e
```

#### Public Database
- **DICE Model**: http://www.williamnordhaus.com/dice-rice-models
- **Documentation**: Comprehensive academic publications available

#### Ecosystem Comparison
- **Methodology Alignment**: Aligned with IFVI/VBA baseline, Transparent Project. Differs from GIST Impact/Upright on parameter choices.
- **Differences from**: IFVI/VBA uses a blended approach of FUND/DICE/PAGE models.
- **Convergence status**: High

#### Value Commission Assessment
- **Transparency**: High (model publicly documented)
- **Confidence criteria**: Met (widely peer-reviewed)
- **Value note**: Base for many global SCC estimates

#### Calculation Example
```
SCC[2030, base_scenario] = $100 per tonne CO2e

After conversion and inflation:
= $100 / 1000 (tonnes to kg)
= $0.10 per kg CO2e
× Inflation factor for 2030
= Final coefficient (negative, damage cost)
```

---

### 2. Air Pollution

**File**: `220707_Air pollution_update.xlsx`
**Script**: `008_241001_prepare_AirPollution_my.py`

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | `220707_Air pollution_update.xlsx` | UBA/NEEDS methodology (EcoSenseWeb); income-elasticity VFT; 188 countries | USD (mixed) |
| **EPS 2015d.1** | EPS 2015d.1 index — `001_inorganic_gases` + `002_particles` (Steen 2015) | YOLL pathway + crop + biodiversity + materials; Swedish income anchor | EUR 2015 |
| **UBA MC 4.0** | EcoSenseWeb v1.3 → *UBA Handbook Tables 2–4* (Eser et al. 2025) | German receptor data; three context tiers (unknown source, combustion, road traffic) | EUR 2025 |
| **CE Delft 2024** | *Environmental Prices Handbook EU27* (De Vries et al. 2025) | Impact pathway approach (IPA); EU27 average receptor data | EUR 2021 |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | NatCap air pathway; IHME GBD 2019 + Chen & Hoek 2020 dose-response | Income-utility–weighted health damage; LANCA exposure scaling | USD 2023 |

#### Origin
- **Primary Source**: German Federal Environment Agency (UBA) methodology
- **Foundational Data**: NEEDS EU project
- **Current Version**: 2022-07-07
- **Update Frequency**: Biannual

#### Methodology: Four Damage Categories

##### 1. Health Damages
- **Impacts**: Respiratory and cardiovascular diseases
- **Valuation**: Medical costs + productivity losses + pain & suffering
- **Key Pollutants**: PM2.5, PM10 (particulate matter)

##### 2. Biodiversity Loss
- **Impacts**: Ecosystem damage, species extinction
- **Mechanism**: Acidification and nutrient deposition
- **Key Pollutants**: NOx, SOx (nitrogen and sulfur oxides)

##### 3. Crop Damages
- **Impacts**: Agricultural yield reduction
- **Valuation**: Market value of lost production
- **Key Pollutants**: Ozone precursors (NOx, NMVOC)

##### 4. Material Damages
- **Impacts**: Corrosion, aesthetic degradation
- **Assets**: Buildings, infrastructure
- **Valuation**: Repair and maintenance costs

#### Pollutants Covered (6 total)
- PM2.5: Fine particulate matter (<2.5 μm)
- PM10: Coarse particulate matter (<10 μm)
- NOx: Nitrogen oxides
- SOx: Sulfur oxides
- NMVOC: Non-methane volatile organic compounds
- NH3: Ammonia

#### Data Structure
```
Sheet: WifOR_form
Index: Multi-level (pollutant, country_code)
Column: Value (damage cost in USD/kg)
```

#### Country Adjustment
- Base values from European context
- Adjusted for population density
- Scaled by income level (Value of Statistical Life correlation)

#### Value Transfer Mechanism

**Method**: **Income Elasticity Adjustment (for VSL)**

**Source Studies**:
- UBA (German Federal Environment Agency) - European base values
- OECD VSL estimates
- NEEDS EU project

**Transfer Method**: **Income Elasticity of Willingness-to-Pay**

**Formula**:
```
VSL[Country] = VSL[Base] × (GDP_per_capita[Country] / GDP_per_capita[Base])^elasticity
```

Where:
- `VSL` = Value of Statistical Life
- `elasticity` = Income elasticity parameter (typically 0.8-1.2)
- Higher income → higher WTP to avoid health risks

**Application to Air Pollution**:
```
Damage[Country, Pollutant] = Mortality_Risk[Pollutant]
                            × VSL[Country]
                            + Morbidity_Costs[Country, Pollutant]
```

**Rationale**:
- **Health Valuation**: People in wealthier countries willing to pay more to avoid premature death
- **Evidence-Based**: Extensive OECD research on income-VSL relationship
- **Context-Sensitive**: Adjusts for economic development levels

**Example** (PM2.5 health damages):
```
Base (Germany): USD 100/kg
USA (GDP per capita ~$70k, elasticity 1.0): USD 100 × (70/50)^1.0 = USD 140/kg
India (GDP per capita ~$2k, elasticity 1.0): USD 100 × (2/50)^1.0 = USD 4/kg
```

**Additional Adjustments**:
- **Population Density**: Higher density → more people exposed → higher aggregate damage
- **Urban/Rural**: Urban areas typically have higher exposure

**Reference**: Impact Valuation Sprint Report 2024 (line 7236):
> "Application of value transfer to translate WTP to different countries and check for income elasticity sensitivity."

**Transparency Note**: Specific elasticity parameters not documented in input files (see BACKLOG.md Q8)

#### Public Databases
- **UBA**: https://www.probas.umweltbundesamt.de/
- **NEEDS**: https://cordis.europa.eu/project/id/502687
- **openLCA**: https://www.openlca.org/project/needs/

#### Ecosystem Comparison
- **Methodology Alignment**: Aligned with UBA's best practice, compatible with NEEDS.
- **Differences from**: Other providers might use different exposure-response functions or economic valuation parameters.
- **Convergence status**: Medium (UBA is a key reference, but global application needs careful adjustment)

#### Value Commission Assessment
- **Transparency**: High (UBA methodology is well-documented)
- **Confidence criteria**: Met (based on extensive scientific research)
- **Value note**: Base for many European air pollution damage costs

---

### 3. Waste Management

**File**: `220509_Waste figures merged_update.xlsx`
**Script**: `007_241001_prepare_Waste_my.py`

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | `220509_Waste figures merged_update.xlsx` | IPCC landfill GHG + EXIOPOL accounts + PwC disamenity + HARAS leachate model; 188 countries | USD (mixed) |
| **EPS 2015d.1** | EPS 2015d.1 index — `012_waste` (Steen 2015) | Plastic litter to ground and water only; Swedish anchor | EUR 2015 |
| **UBA MC 4.0** | — not covered | — | — |
| **CE Delft 2024** | — not covered | — | — |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | — not covered | — | — |

#### Origin
- **Mixed Sources**:
  - IPCC (greenhouse gas emissions)
  - EXIOPOL (European environmental accounts)
  - PwC (disamenity costs)
- **Current Version**: 2022-05-09
- **Update Frequency**: Biannual

#### Methodology: Three Impact Pathways

##### 1. Air Emissions & GHG
- **Incineration**: Air pollutants (PM, NOx, SOx)
  - Values from UBA air pollution methodology
- **Landfill**: Methane emissions (GHG)
  - Emission factors from IPCC guidelines
  - Valued using Social Cost of Carbon

##### 2. Disamenity
- **Impact**: Reduced property values near waste sites
- **Method**: Hedonic pricing (willingness-to-pay)
- **Data**: Real estate value studies
- **Source**: PwC research

##### 3. Leachate Contamination
- **Impact**: Soil and groundwater pollution
- **Method**: Risk-based model (HARAS)
- **Valuation**: Clean-up and remediation costs
- **Substances**: Heavy metals, organic compounds

#### Waste Categories (6 total)
Coefficients calculated for:
- Waste_hazardous_incinerated
- Waste_hazardous_landfill
- Waste_hazardous_recovered (zero cost)
- Waste_nonhazardous_incinerated
- Waste_nonhazardous_landfill
- Waste_nonhazardous_recovered (zero cost)

**Note**: Recovery assigned zero damage cost (assumption: proper recycling has minimal external cost)

#### Data Structure
```
Sheets: 4 (one per treatment × hazard combination)
Columns: country_code, costs (USD/kg)
```

#### Public Databases
- **IPCC**: https://www.ipcc-nggip.iges.or.jp/EFDB/main.php
- **EXIOBASE**: https://www.exiobase.eu/

#### Ecosystem Comparison
- **Methodology Alignment**: Uses IPCC for GHG, EXIOPOL for accounts. Integrates specific PwC research.
- **Differences from**: Other providers may use different waste composition data or economic valuation methods for disamenity/leachate.
- **Convergence status**: Low to Medium (due to mixed-method approach)

#### Value Commission Assessment
- **Transparency**: Medium (some components publicly documented, others from proprietary research)
- **Confidence criteria**: Partial (IPCC is high, but disamenity/leachate components may vary)
- **Value note**: Provides granular categories often missing in broader assessments

---

### 4. Water Consumption

**File**: `220511_Water consumption_update.xlsx`
**Script**: `009_241001_prepare_WaterConsumption_my.py`

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | `220511_Water consumption_update.xlsx` | Ligthart & van Harmelen 2019 (economic damage) + Debarre et al. 2022 (DALY health damage) + WULCA AWARE scarcity scaling; 188 countries | USD (mixed) |
| **EPS 2015d.1** | — not covered | — | — |
| **UBA MC 4.0** | — not covered | — | — |
| **CE Delft 2024** | — not covered | — | — |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | NatCap water consumption pathway; IHME 2019 + WULCA AWARE + income utility | Country-specific via AWARE scarcity + income elasticity | USD 2023 |

#### Origin
- **Academic Research**:
  - Ligthart & van Harmelen (2019)
  - Debarre et al. (2022)
- **Current Version**: 2022-05-11
- **Maturity Status**: Experimental (high uncertainty)

#### Methodology: Dual Approach

##### 1. Economic Damages
- **Impact**: Agricultural output loss from water scarcity
- **Method**: Shadow pricing
  - Global baseline shadow price for water
  - Adjusted using AWARE factors

##### 2. Health Damages
- **Impact**: Domestic water deprivation effects on health
- **Metric**: Disability-Adjusted Life Years (DALYs)
  - Years of life lost (mortality)
  - Years lived with disability (morbidity)
- **Conversion**: DALY × Value of Statistical Life Year

#### AWARE Factors
- **Purpose**: Country-specific water scarcity adjustment
- **Method**: Assess available water minus environmental flow requirements
- **Source**: WULCA (Water Lifecycle Assessment) working group
- **Application**: Scales global values to local context

#### Data Structure
```
Sheet: Ergebnisse_final
Columns: country_code, Total damages (USD/m³)
Note: Total damages = Economic + Health
```

#### Known Issues
- **High Uncertainty**: Results "hard to explain" per README
- **Experimental Status**: Methodology under review
- **Future Work**: See BACKLOG.md Q1 for improvement suggestions

#### Public Databases
- **AWARE**: https://wulca-waterlca.org/aware/

#### Ecosystem Comparison
- **Methodology Alignment**: Uses academic research (Ligthart & van Harmelen, Debarre et al.) and AWARE factors.
- **Differences from**: Other water valuation methods (e.g., using only scarcity indices, or different DALY monetization approaches).
- **Convergence status**: Low (experimental nature, high uncertainty)

#### Value Commission Assessment
- **Transparency**: Medium (academic sources cited, but internal calculation details may need further documentation)
- **Confidence criteria**: Partial (experimental status indicates ongoing refinement)
- **Value note**: Innovative approach combining economic and health damages

---

### 5. Land Use

**File**: `230317_Landuse_update_ZK.xlsx`
**Script**: `010_241001_prepare_LandUse_my.py`

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | `230317_Landuse_update_ZK.xlsx` | EPS 2015d.1 ecosystem service monetisation + LANCA v2.5 country characterisation; 188 countries | USD (mixed) |
| **EPS 2015d.1** | EPS 2015d.1 index — `009_land_use` (23 land types; Steen 2015) | Five pathways: climate, crop, wood, water regulation, biodiversity (NEX); Swedish anchor | EUR 2015 |
| **UBA MC 4.0** | — not covered (explicitly excluded from MC 4.0; no standalone land-use VF recommended) | — | — |
| **CE Delft 2024** | *Environmental Prices Handbook EU27* (De Vries et al. 2025) — Table 6 land use | Ecosystem service loss; EU27 average | EUR 2021 |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | LANCA v2.0 (Fraunhofer IBP); HUT global average (0.7581) welfare multiplier | Ecosystem service value × HUT social return | USD 2023 |

#### Origin
- **Primary Framework**: Environmental Priority Strategies (EPS)
  - Original: 1992 (Steen)
  - Updated: 2015
- **Characterization**: LANCA (Land Use Indicator Value Calculation)
- **Current Version**: 2023-03-17

#### Methodology: EPS System

The EPS system monetizes ecosystem service loss from land conversion across four categories:

##### 1. Working Capacity
- **Impact**: Urban heat island effect on labor productivity
- **Mechanism**: Increased temperatures reduce work efficiency
- **Valuation**: Lost labor hours × wage rates

##### 2. Water Treatment
- **Impact**: Loss of natural filtration services
- **Alternative**: Constructed water treatment facilities
- **Valuation**: Replacement cost of built infrastructure

##### 3. Crop Growth
- **Impact**: Soil quality degradation, pollination loss
- **Mechanism**: Reduced agricultural productivity
- **Valuation**: Market value of yield reduction

##### 4. Biodiversity
- **Impact**: Species habitat loss
- **Method**: Willingness-to-pay for preservation
- **Valuation**: Conservation and restoration costs

#### LANCA Characterization
- **Purpose**: Adjust global EPS values to local conditions
- **Factors**: Climate, soil type, current land use
- **Application**: Country-specific multiplication factors

#### Land Use Types
Multiple categories (varies by data):
- Forestry
- Agriculture (multiple types)
- Urban development
- Industrial use
- Others

#### Data Structure
```
Sheet: Ergebnisse_final
Columns: country_code, [land_type_1], [land_type_2], ...
Each column contains damage cost (USD/ha)
```

#### Public Databases
- **EPS**: https://lifecyclecenter.se/projects/eps-environmental-priority-strategies-in-product-development/
- **LANCA**: https://www.ibp.fraunhofer.de/en/expertise/life-cycle-engineering/applied-methods/lanca.html

#### Ecosystem Comparison
- **Methodology Alignment**: Uses established EPS and LANCA frameworks.
- **Differences from**: Other land use valuation approaches (e.g., focusing solely on biodiversity, or using different impact categories).
- **Convergence status**: Medium (EPS/LANCA are well-known, but their specific application here is WifOR's)

#### Value Commission Assessment
- **Transparency**: High (EPS/LANCA are publicly documented frameworks)
- **Confidence criteria**: Met (based on recognized life cycle impact assessment methods)
- **Value note**: Provides detailed breakdown of land use impacts

---

### 6. Water Pollution

**File**: `230324_WaterPollution_Mon_Coef_Final_DC.xlsx`
**Script**: `013_241014_prepare_WaterPol_my.py`

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | `230324_WaterPollution_Mon_Coef_Final_DC.xlsx` | Steen 2020 (N, P nutrients via eutrophication pathway) + USEtox model (9 heavy metals); PPP value transfer from Ahlroth 2009 (Sweden base); 188 countries | USD (mixed) |
| **EPS 2015d.1** | EPS 2015d.1 index — `005_emissions_to_water` (Steen 2015) | Eutrophication via oxygen deficiency + fish/biodiversity/drinking water pathways; Swedish anchor | EUR 2015 |
| **UBA MC 4.0** | EcoSenseWeb + limiting-substance model → *UBA Handbook Tables 22–24* (Eser et al. 2025) | Conservative lower bound: only limiting nutrient (N or P) charged; air N valued via health pathway | EUR 2025 |
| **CE Delft 2024** | *Environmental Prices Handbook EU27* (De Vries et al. 2025) — Tables 1–2 (N, P) and Tables 3–5 (heavy metals to air, water, soil) | IPA; EU27 average | EUR 2021 |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | NatCap water pollution pathway; LANCA v2.0 + income utility | Country-specific via LANCA characterisation + income elasticity | USD 2023 |

#### Origin
- **Methodology**:
  - Steen (2020): Nitrogen and Phosphorus
  - USEtox model: Heavy metals
- **Generation**: Internal WifOR calculations
- **Current Version**: 2023-03-24
- **Maturity Status**: Experimental

#### Methodology by Pollutant Type

##### 1. Nutrients (N, P) - Steen 2020
- **Impact**: Freshwater eutrophication
- **Mechanisms**:
  - Algal blooms
  - Oxygen depletion
  - Fish kills
- **Damages**:
  - Reduced fish production (market value)
  - Biodiversity loss (willingness-to-pay)
  - Water treatment costs

##### 2. Heavy Metals - USEtox Model
- **Impact**: Human health and ecotoxicity
- **Pathways**:
  - Drinking water contamination
  - Bioaccumulation in fish
  - Direct aquatic toxicity
- **Valuation**:
  - Health: DALYs × VSL
  - Ecosystem: Potentially disappeared fraction of species

#### Value Transfer Mechanism

**Source Study**: Ahlroth (2009) - Sweden

**Base WTP Values (Sweden)**:
- **Freshwater Phosphorus**: USD 136/kg
- **Marine Phosphorus**: USD 68/kg
- **Marine Nitrogen**: USD 9/kg

**Transfer Method**: **Purchasing Power Parity (PPP) Adjustment**

**Formula**:
```
Value[Country] = Value[Sweden] × (PPP[Country] / PPP[Sweden])
```

**Rationale**:
- WTP for water quality varies with economic conditions
- PPP adjustment accounts for differences in purchasing power across countries
- Higher PPP ratio → higher damage valuation (wealthier countries value environmental quality more)

**Example**:
```
Sweden: P = USD 136/kg (base)
USA (PPP ratio ~1.0): P = USD 136 × 1.0 = USD 136/kg
India (PPP ratio ~0.3): P = USD 136 × 0.3 = USD 41/kg
```

**Reference**: Impact Valuation Sprint Report 2024 (lines 9720-9742):
> "To transfer these values from Sweden to other countries, we adjust the WTP values by PPP."

**Transparency Note**: PPP indices and base years used are not explicitly documented in input files (see BACKLOG.md Q8)

#### Pollutants Covered (11 total)
- **Nutrients**: Nitrogen (N), Phosphorus (P)
- **Heavy Metals**: Arsenic (As), Cadmium (Cd), Mercury (Hg), Chromium (Cr), Lead (Pb), Nickel (Ni), Copper (Cu), Zinc (Zn), Antimony (Sb)

#### Water Scarcity Adjustment
- Global base values scaled by country water scarcity
- More severe impacts in water-stressed regions
- Based on AWARE factors

#### Data Structure
```
Sheet: Results
Index: Multi-level (pollutant, country_code)
Column: Value (damage cost in USD/kg)
```

#### Known Issues
- **Experimental Status**: High uncertainty
- **Difficult Results**: Some coefficients hard to validate
- **Ongoing Research**: Methodology under refinement

#### Public Databases
- **USEtox**: https://usetox.org

#### Ecosystem Comparison
- **Methodology Alignment**: Integrates Steen (2020) and USEtox, recognized frameworks for specific pollutants.
- **Differences from**: Other water pollution models might use different characterization factors or valuation approaches.
- **Convergence status**: Medium (USEtox is standardized, but overall approach is mixed)

#### Value Commission Assessment
- **Transparency**: Medium (USEtox is public, Steen's work is academic, internal calculations need documentation)
- **Confidence criteria**: Partial (experimental status for overall approach)
- **Value note**: Combines well-established models for specific pollutants

---

### 7. Training

**File**: `220529_training_value_per_hour_bysector.h5`
**Script**: `014_241016_prepare_Training_my.py`

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | `220529_training_value_per_hour_bysector.h5` | Psacharopoulos & Patrinos 2018 returns to education (~9%/year); PPP + GVA sector adjustment; 188 countries × 21 NACE sectors | USD 2020 |
| **EPS 2015d.1** | — not covered | — | — |
| **UBA MC 4.0** | — not covered | — | — |
| **CE Delft 2024** | — not covered | — | — |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | Wages × HUI welfare multiplier; sector-specific GVA data; World Bank income data | Human capital benefit monetised via health utility of income | USD 2023 |

#### Origin
- **Theoretical Foundation**: Returns to schooling research
- **Key Reference**: Psacharopoulos & Patrinos (2018)
- **Generation**: Internal WifOR calculations
- **Current Version**: 2022-05-29
- **Unique Feature**: ONLY POSITIVE coefficient (benefit, not damage)

#### Methodology: Human Capital Investment

##### Conceptual Framework
Training as investment in human capital, similar to physical capital:

1. **Productivity Increase**: Training improves worker output
2. **Wage Premium**: Manifests as higher wages over career
3. **Present Value**: Future wage gains discounted to present

##### Calculation Steps

###### Step 1: Returns to Education Baseline
- **Source**: Global meta-analysis (Psacharopoulos & Patrinos)
- **Finding**: ~8-10% wage increase per year of schooling
- **Variation**: Higher in developing countries, lower in developed

###### Step 2: Training Equivalence
- **Assumption**: Training hours equivalent to formal education
- **Conversion**: 1 year schooling ≈ ~1,800 hours
- **Hourly Return**: Annual return / 1,800

###### Step 3: Lifetime Value Projection
```
Training_Value = Hourly_Wage
                × Return_Rate_per_Hour
                × Remaining_Working_Years
                × Discount_Factor
```

###### Step 4: Sector Adjustment
- **Variation**: Different returns by economic sector
- **High Returns**: Knowledge-intensive sectors (IT, finance)
- **Lower Returns**: Labor-intensive sectors (construction)
- **Data**: Sector-specific wage premiums from education data

#### Data Structure
```python
# HDF5 Key: 'value_per_hour'
# Structure: Sector × Country matrix
# Column: "value_per_hour_GVA_2020USD_PPP"
# Values: Positive (benefits in USD/hour)
```

#### Value Transfer Mechanism

**Method**: **Purchasing Power Parity (PPP) Adjustment based on GVA**

**Evidence**: Column name explicitly includes `_PPP` suffix

**Transfer Approach**:
1. **Base Calculation**: Returns to education estimated using sector-specific GVA (Gross Value Added)
2. **PPP Adjustment**: Values adjusted for purchasing power differences across countries
3. **Sector Differentiation**: Each country-sector combination has unique value

**Formula** (conceptual):
```
Value_per_hour[Country, Sector] = Base_Return[Sector]
                                  × GVA_per_worker[Country, Sector]
                                  × PPP_adjustment[Country]
```

**Rationale**:
- **Economic Context**: Training value tied to local wage levels and productivity
- **Sector Variation**: High-skill sectors (finance, tech) show higher returns than low-skill sectors
- **PPP Necessity**: Ensures cross-country comparability in real economic terms

**Example**:
```
IT Sector:
  USA (high GVA, PPP~1.0):     USD 50/hour training value
  Germany (high GVA, PPP~0.9): USD 45/hour training value
  India (lower GVA, PPP~0.3):  USD 15/hour training value

Construction Sector (lower skill premium):
  USA:     USD 20/hour
  Germany: USD 18/hour
  India:   USD 6/hour
```

**Data Source**: Internal WifOR calculations based on:
- Psacharopoulos & Patrinos (2018) - Returns to education research
- Sector-specific GVA data
- PPP indices (year not specified in input file)

**Transparency Note**: Full calculation methodology not documented in input files (see BACKLOG.md Q10)

#### Interpretation
- **Positive Sign**: Training adds value (opposite of damage costs)
- **Sector Variation**: Only indicator with sector-specific values
- **Per Hour**: Flexible unit for any training duration

#### Public Databases
- **OECD Education**: https://www.oecd.org/education/data/
- **Returns to Education**: https://www.nationmaster.com/country-info/stats/Education

#### Ecosystem Comparison
- **Methodology Alignment**: Grounded in established "returns to schooling" literature.
- **Differences from**: Other human capital valuation methods may use different metrics (e.g., skill premiums, job satisfaction).
- **Convergence status**: Low to Medium (due to "open methodological questions" and highly specific hourly valuation)

#### Value Commission Assessment
- **Transparency**: Medium (academic literature is public, but internal calculation details need further documentation)
- **Confidence criteria**: Partial (rated "Average" in README due to open methodological questions)
- **Value note**: Innovative approach to monetize human capital benefits

---

### 8. Occupational Health & Safety (OHS)

**File**: `220616_monetization_value_per_incident_NEW.xlsx`
**Script**: `015_241016_prepare_OHS_my.py`

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | `220616_monetization_value_per_incident_NEW.xlsx` | IHME GBD 2019 disability weights + Eurostat incident rates; global USD 200,000/DALY (uniform); 188 countries | USD (mixed) |
| **EPS 2015d.1** | — not covered | — | — |
| **UBA MC 4.0** | — not covered | — | — |
| **CE Delft 2024** | — not covered | — | — |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | IHME GBD 2019 DALY rates (occupational + WASH + dietary risk factors) × income utility (HUI); 188 countries | Country-specific DALY monetisation via HUI welfare multiplier | USD 2023 |

#### Origin
- **Methodology**: Health economics (DALY approach)
- **Data Sources**:
  - Eurostat (incident rates)
  - Global Burden of Disease (disability weights)
- **Generation**: Internal WifOR calculations
- **Current Version**: 2022-06-16
- **Maturity Status**: Well Established

#### Methodology: DALY-Based Valuation

##### Disability-Adjusted Life Years (DALYs)
Combines two components:
```
DALY = YLL + YLD

Where:
- YLL = Years of Life Lost (fatal incidents)
- YLD = Years Lived with Disability (non-fatal incidents)
```

##### Fatal Incidents
```
YLL = (Life_Expectancy - Age_at_Death) × Discount_Factor

Where:
- Life_Expectancy: Country-specific (WHO data)
- Age_at_Death: Average age for occupational fatalities
- Discount_Factor: Typically 3% annual discount rate
```

##### Non-Fatal Incidents
```
YLD = Duration × Disability_Weight × Discount_Factor

Where:
- Duration: Time with disability (temporary or permanent)
- Disability_Weight: Severity (0=perfect health, 1=death)
  - Injury: 0.1-0.4 (temporary disability)
  - Illness: 0.2-0.8 (chronic conditions)
- Source: Global Burden of Disease study
```

##### Monetization
```
Monetary_Value = DALY × Value_per_DALY

Where:
- Value_per_DALY: ~$200,000 (Value of Statistical Life Year)
- Varies by country income level
- Based on revealed/stated preference studies
```

#### Incident Categories (4 total)
- **Injury_nonfatal**: Workplace accidents, temporary disability
- **Disease_Illness_nonfatal**: Occupational diseases, chronic conditions
- **Injury_fatality**: Fatal workplace accidents
- **Disease_Illness_fatality**: Fatal occupational diseases

**Note**: Fatality categories use same base DALY value (YLL), but distinguished for data tracking

#### Data Structure
```
Sheet: Fatality
Columns: country_code, USD/Fatality

Sheet: Nonfatal
Columns: country_code, USD/Injury, USD/Illness
```

#### Country Variation
- **Income-Based**: Higher VSL in high-income countries
- **Typical Range**: $50,000-$500,000 per DALY
- **USA Baseline**: ~$200,000 per DALY

#### Value Transfer Mechanism

**Method**: **Global Value Transfer with Simplified Approach**

**Approach**: Single global DALY value applied across all countries (USD 200,000 per DALY)

**Formula**:
```
Damage[Country, Incident_Type] = DALY[Incident_Type] × USD 200,000
```

**Rationale for Global Value**:
- **Ethical Stance**: Equal value of human life regardless of country income
- **Simplicity**: Avoids complex country-specific adjustments
- **Conservative**: Middle-ground estimate suitable for global application

**Alternative Approach** (not currently used):
```
Value_per_DALY[Country] = Base_DALY_Value × (GDP_per_capita[Country] / GDP_per_capita[Base])^elasticity
```

**Current Implementation**: No country-specific adjustment applied

**Trade-offs**:
- **Advantage**: Ethical consistency, simpler methodology
- **Limitation**: May overestimate impacts in low-income countries, underestimate in high-income countries
- **Debate**: Ongoing discussion in impact valuation community about equity vs. WTP-based approaches

**Reference**: Impact Valuation Sprint Report 2024 (line 3088):
> "assumes a global value transfer mechanism to estimate a staggering total global damage of USD 14.2 trillion"

**Methodological Note**:
- This differs from other indicators (Air Pollution, Water Pollution) which use PPP or income elasticity
- Represents **simplified value transfer** rather than adjusted transfer
- Some practitioners advocate for income-adjusted VSL/DALY; WifOR chose uniform approach

**Comparison to Income-Adjusted Approach**:
```
Current (Global):
  All countries: USD 200,000/DALY

Income-Adjusted Alternative:
  USA (high income):     USD 400,000/DALY
  Germany (high income): USD 350,000/DALY
  India (lower income):  USD 50,000/DALY
```

#### Public Databases
- **Eurostat**: https://ec.europa.eu/eurostat/web/health/health-safety-work
- **GBD Study**: https://www.healthdata.org/gbd

#### Ecosystem Comparison
- **Methodology Alignment**: Based on established DALY approach and global health studies (GBD).
- **Differences from**: Other OHS valuation may use pure VSL without DALYs, or different monetization coefficients.
- **Convergence status**: High (DALY is a widely recognized metric)

#### Value Commission Assessment
- **Transparency**: High (GBD is public, DALY methodology is well-documented)
- **Confidence criteria**: Met (rated "Well Established" in README)
- **Value note**: Uses a single global DALY value for ethical consistency

---

### 9. Noise

*Not covered by WifOR. Primary systems: EPS 2015d.1, UBA MC 4.0.*

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | — not covered | — | — |
| **EPS 2015d.1** | EPS 2015d.1 index — `007_noise` (Steen 2015) | Road traffic; sleep disturbance → YOLL pathway; dB level converted via WHO exposure-response; Swedish anchor | EUR 2015 |
| **UBA MC 4.0** | EcoSenseWeb + health valuation → *UBA Handbook Tables 19–20* (Eser et al. 2025) | Road, rail, and air traffic noise; annoyance + cognitive impairment in children; per dB(A) class; German receptor data | EUR 2025 |
| **CE Delft 2024** | — not covered | — | — |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | — not covered | — | — |

**Key inputs for UBA noise (Tables 19–20):**
- WHO exposure–response functions (Guski et al. 2017) — % highly annoyed by dB(A) class
- EcoSenseWeb receptor density data — German population along road/rail/flight corridors
- Health valuation: VOLY (Value of a Life Year) from meta-analysis; German income anchor

---

### 10. Halogenated Compounds and Refrigerants

*Not covered by WifOR. Primary systems: EPS 2015d.1 (283 substances), UBA MC 4.0 (8 refrigerants), CE Delft 2024 (CFC-11 equivalent).*

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | — not covered | — | — |
| **EPS 2015d.1** | EPS 2015d.1 index — `004_halogenated_organics` (Steen 2015); 283 substances | Climate change + ozone depletion + human toxicity pathways; Swedish anchor | EUR 2015 |
| **UBA MC 4.0** | GIVE model GWP100 × CO₂ VF → *UBA Handbook Table 7* (Eser et al. 2025); 8 refrigerants | Climate pathway only (GWP100 × UBA CO₂ VF); R-32, R-410A, R-134a, R-507A, R-717, R-290, and others | EUR 2025 |
| **CE Delft 2024** | *Environmental Prices Handbook EU27* (De Vries et al. 2025) — Table 3 | CFC-11 equivalent; climate via SCC | EUR 2021 |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | — not covered | — | — |

**Key inputs for UBA refrigerants:** IPCC AR6 Table 7.SM.7 GWP100 values per refrigerant × UBA CO₂ VF from Table 1.

---

### 11. Electricity — Life-Cycle VF per kWh by Source

*Unique to UBA MC 4.0.*

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | — not covered | — | — |
| **EPS 2015d.1** | — not covered as per-kWh electricity VF (fossil resource depletion in §5.15) | — | — |
| **UBA MC 4.0** | LCA inventory + EcoSenseWeb + GIVE → *UBA Handbook Table 5* (Eser et al. 2025) | Life-cycle GHG + air pollutants per kWh per source; German grid losses and receptor data; 9 electricity sources | EUR-cent 2025/kWh |
| **CE Delft 2024** | — not covered | — | — |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | — not covered | — | — |

**UBA electricity sources (Table 5):** German mix, lignite, hard coal, natural gas, nuclear, wind onshore/offshore, solar PV, hydro, biomass.

---

### 12. Heat Generation — Life-Cycle VF per kWh by Source

*Unique to UBA MC 4.0.*

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | — not covered | — | — |
| **EPS 2015d.1** | — not covered | — | — |
| **UBA MC 4.0** | LCA inventory + EcoSenseWeb + GIVE → *UBA Handbook Table 6* (Eser et al. 2025) | Life-cycle GHG + AP per kWh final energy; 7 heat sources; German receptor data | EUR-cent 2025/kWh |
| **CE Delft 2024** | — not covered | — | — |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | — not covered | — | — |

**UBA heat sources (Table 6):** Natural gas, heating oil, hard coal, lignite, biomass, solar thermal, heat pumps (COP-adjusted).

---

### 13. Transport — per Vehicle-km and per Pkm/tkm

*Unique to UBA MC 4.0.*

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | — not covered | — | — |
| **EPS 2015d.1** | — not covered | — | — |
| **UBA MC 4.0** | LCA inventory + EcoSenseWeb + GIVE + infrastructure data → *UBA Handbook Tables 9–18* (Eser et al. 2025) | Cars, vans, heavy-duty trucks, buses, rail, air, ship; GHG + AP exhaust + AP abrasion + infrastructure + energy supply | EUR 2025/veh-km; EUR 2025/Pkm or tkm |
| **CE Delft 2024** | — not covered | — | — |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | — not covered | — | — |

**UBA transport tables:** Tables 9–16 (per vehicle-km by vehicle type and fuel); Tables 17–18 (per Pkm/tkm using ITF occupancy and load factors).

---

### 14. Agriculture — per kg Product and per kg Nutrient Surplus

*Primary system: UBA MC 4.0. CE Delft covers abiotic depletion only.*

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | — not covered (N/P nutrients partially in §5.6 Water Pollution) | — | — |
| **EPS 2015d.1** | — not covered as per-product VF | — | — |
| **UBA MC 4.0** | IPCC Tier 2 emission factors + EcoSenseWeb + Karzai & Hirschfeld 2024 → *UBA Handbook Tables 25–27* (Eser et al. 2025) | Milk, beef, pork, poultry, eggs; N fertiliser; N/P surpluses; GHG + NH₃ + N pathways | EUR 2025/kg product |
| **CE Delft 2024** | *Environmental Prices Handbook EU27* (De Vries et al. 2025) — Table 7 (fossil ADP, minerals) | Abiotic resource depletion for agricultural inputs only | EUR 2021 |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | — not covered | — | — |

**UBA agriculture key inputs:** IPCC Tier 2 livestock emission factors; FAO GLEAM GHG intensities; EcoSenseWeb for NH₃ health impacts; N/P to water via UBA Tables 22–24 limiting-substance approach.

---

### 15. Fossil Resource Depletion

*Not covered by WifOR or UBA as standalone. Primary systems: EPS 2015d.1, CE Delft 2024.*

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | — not covered | — | — |
| **EPS 2015d.1** | EPS 2015d.1 index — `010_fossil_resources` (Steen 2015); fossil oil, coal, lignite, natural gas | Future extraction cost increase + energy substitution cost; globally anchored, Swedish income | EUR 2015 |
| **UBA MC 4.0** | — not covered as standalone; embedded within electricity, heat, and transport life-cycle VFs | — | — |
| **CE Delft 2024** | *Environmental Prices Handbook EU27* (De Vries et al. 2025) — Table 7 (fossil ADP) | Abiotic depletion potential method; globally uniform | EUR 2021 |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | — not covered | — | — |

---

### 16. WELLBY / QALY Unit Value and Discount Rates

*Unique to UK Wellbeing system.*

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | — not covered | — | — |
| **EPS 2015d.1** | — not covered | — | — |
| **UBA MC 4.0** | — not covered | — | — |
| **CE Delft 2024** | — not covered | — | — |
| **UK Wellbeing** | HM Treasury Green Book 2026 (GBP 70,000/QALY); NICE HTA (GBP 20,000–30,000/QALY); Frontier Economics / DCMS Wellbeing Guidance 2021 (GBP 13,000/WELLBY); OECD 2025 geographic transfer guidance | WELLBY = midpoint of QALY-income anchor and QALY-value anchor; temporal uprating by GDP deflator × per-capita growth^1.3 | GBP 2019/2024 |
| **eQALY** | IHME GBD 2019 + World Bank GDP per capita + IMF WEO deflators → HUI (health utility of income) | Endogenous country-specific welfare multiplier on income impacts | USD 2023 |

**Key UK input files:** `01_wellby_valuations.xlsx` (WELLBY, QALY); `05_discount_rates.xlsx` (STPR 3.5%; health rate 1.5%); `04_cultural_engagement.xlsx` (GBP 122–1,310/person/yr).

---

### 17. HUI and HUT — Health Utility Welfare Multipliers

*Unique to eQALY system.*

#### Cross-System Input Sources

| System | Primary Input / Handbook Reference | Model / Methodology | Price Base |
|--------|------------------------------------|---------------------|------------|
| **WifOR** | — not covered | — | — |
| **EPS 2015d.1** | — not covered | — | — |
| **UBA MC 4.0** | — not covered | — | — |
| **CE Delft 2024** | — not covered | — | — |
| **UK Wellbeing** | — not covered | — | — |
| **eQALY** | IHME GBD 2019 health burden data + World Bank GDP per capita PPP + IMF WEO deflators → `01_hui_output.h5` / `02_hut_output.h5` | HUI (health utility of income): converts monetary income impact to welfare equivalent per country. HUT (health utility of taxes): social return on public investment (SROI). | USD 2023 |

**HUI application:** applied as country-specific multiplier on all income-generating indicators (Training, wages). **HUT application:** global average (0.7581) scales LANCA ecosystem values; country-specific HUT scales public revenue impacts.

---

## 6. External Sources and License Information

This section documents each external source used across all WifOR indicator scripts. Each entry provides the full citation, verified license terms, and conditions for commercial use and redistribution.

---

### 6.1 World Bank Open Data — GDP Deflators

| Attribute | Detail |
|-----------|--------|
| **Full citation** | World Bank (2024). *World Development Indicators*: NY.GDP.DEFL.ZS — GDP deflator (base year varies by country). The World Bank Group, Washington DC. https://data.worldbank.org |
| **License name** | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| **License URL** | https://creativecommons.org/licenses/by/4.0/ |
| **Commercial use** | ✓ Permitted |
| **Attribution required** | Yes — "Source: World Bank, World Development Indicators" |
| **Redistribution** | Permitted with attribution |
| **Notes** | Used for temporal deflation (converting coefficients to constant base-year USD) in all 8 WifOR indicator scripts. Data accessible via the `wbdata` Python library or the World Bank Data API. |

---

### 6.2 DICE / RICE Model — Social Cost of Carbon (GHG)

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Nordhaus, W., Barrage, L. (2024). *DICE/RICE Integrated Assessment Model*, 2024 update. Yale University. http://www.williamnordhaus.com/dice-rice-models |
| **License name** | No formal open-source licence declared |
| **License URL** | http://www.williamnordhaus.com/dice-rice-models |
| **Commercial use** | Unspecified — model freely distributed from author's website without explicit licence terms |
| **Attribution required** | Yes (academic convention) |
| **Redistribution** | Unspecified — code available for download; no redistribution terms stated |
| **Notes** | The DICE model (originally DICE123, 1991) has been openly distributed since its inception. The 2024 Barrage–Nordhaus update is provided in GAMS/Excel format without a formal open-source licence. Open-source re-implementations in Julia, R, and Python exist under MIT/Apache licences on GitHub. The DICE SCC trajectory forms the basis for the GHG value factor. |

---

### 6.3 UBA / ProBas — Air Pollution Damage Costs

| Attribute | Detail |
|-----------|--------|
| **Full citation** | German Federal Environment Agency (Umweltbundesamt — UBA). *ProBas: Prozessorientierte Basisdaten für Umweltmanagement-Instrumente*. https://www.probas.umweltbundesamt.de/ |
| **License name** | Data Licence Germany — Attribution — Version 2.0 (dl-de/by-2-0) |
| **License URL** | https://www.govdata.de/dl-de/by-2-0 |
| **Commercial use** | ✓ Permitted — data may be integrated in commercial products |
| **Attribution required** | Yes — Umweltbundesamt (UBA) must be cited |
| **Redistribution** | Permitted; data may be merged and redistributed with attribution |
| **Notes** | UBA publishes all publicly available governmental data under Data Licence Germany 2.0 (dl-de/by-2-0) by default. ProBas freely provides >20,000 process-level LCI datasets. The air pollution damage cost methodology (VOLY, VSL, exposure-response functions) is based on the EcoSenseWeb model, developed in the NEEDS EU project (§6.4). |

---

### 6.4 NEEDS EU Project — External Cost Database (Air Pollution)

| Attribute | Detail |
|-----------|--------|
| **Full citation** | New Energy Externalities Development for Sustainability (NEEDS). *FP6 Integrated Project 502687*. European Commission, 2004–2008. https://cordis.europa.eu/project/id/502687 |
| **License name** | European Union publication copyright |
| **License URL** | https://op.europa.eu/en/web/about-us/legal-notices/eu-publications |
| **Commercial use** | ✗ Not for commercial resale without permission; available for research and policy use |
| **Attribution required** | Yes |
| **Redistribution** | Non-commercial redistribution with attribution permitted |
| **Notes** | The NEEDS project developed the EcoSense external cost model and a comprehensive European air pollution externality database used by UBA and WifOR. Project deliverables are publicly accessible via CORDIS and openLCA (https://www.openlca.org/project/needs/). Pre-2011 EC-funded publications are not covered by EC Decision 2011/833/EU. |

---

### 6.5 IPCC — Emission Factors for Waste GHG

| Attribute | Detail |
|-----------|--------|
| **Full citation** | IPCC (2006). *2006 IPCC Guidelines for National Greenhouse Gas Inventories*. IPCC National Greenhouse Gas Inventories Programme. https://www.ipcc-nggip.iges.or.jp/EFDB/main.php |
| **License name** | Creative Commons Attribution 3.0 IGO (CC BY 3.0 IGO) |
| **License URL** | https://creativecommons.org/licenses/by/3.0/igo/ |
| **Commercial use** | ✓ Permitted |
| **Attribution required** | Yes — IPCC must be cited |
| **Redistribution** | Permitted with attribution |
| **Notes** | The IPCC Guidelines provide methane emission factors for landfill decomposition and incineration processes used in the Waste Management indicator GHG component. The Emission Factor Database (EFDB) is freely accessible. |

---

### 6.6 EXIOBASE — Environmentally Extended Input–Output Data (Waste)

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Wood, R. et al. (2015). Global Sustainability Accounting — Developing EXIOBASE for Multi-Regional Footprint Analysis. *Sustainability*, 7(1), 138–163. Database: https://www.exiobase.eu/ |
| **License name** | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| **License URL** | https://creativecommons.org/licenses/by/4.0/ |
| **Commercial use** | ✓ Permitted |
| **Attribution required** | Yes |
| **Redistribution** | Permitted with attribution |
| **Notes** | EXIOBASE (successor to the EXIOPOL project) provides multi-regional environmentally-extended input–output tables. These accounts underpin the Waste Management indicator's European-context waste composition data. Version 3.x is released under CC BY 4.0. |

---

### 6.7 WULCA AWARE — Water Scarcity Characterisation Factors

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Boulay, A.-M., Bare, J., Benini, L. et al. (2018). The WULCA consensus characterization model for water scarcity footprints: assessing impacts of water consumption based on available water remaining (AWARE). *The International Journal of Life Cycle Assessment*, 23, 368–378. https://doi.org/10.1007/s11367-017-1333-8. Factors: https://wulca-waterlca.org/aware/ |
| **License name** | Free to use with mandatory citation — no formal Creative Commons licence declared |
| **License URL** | https://wulca-waterlca.org/aware/faq/ |
| **Commercial use** | ✓ Permitted (no stated restriction) |
| **Attribution required** | Yes — citation to Boulay et al. 2018 required |
| **Redistribution** | Not explicitly stated; AWARE factors downloadable without registration |
| **Notes** | WULCA is a working group of the UNEP–SETAC Life Cycle Initiative. Per the WULCA FAQ: "There is no restriction in using the AWARE factors in your studies and environmental footprint methodologies. The only requirement is a proper citation." Used in both the Water Consumption indicator (AWARE scarcity scaling) and the Water Pollution indicator (water scarcity adjustment). |

---

### 6.8 Ligthart & van Harmelen (2019) — Water Consumption Shadow Prices

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Ligthart, T.N., van Harmelen, T. (2019). Estimation of shadow prices of soil organic carbon depletion and freshwater depletion for use in LCA. *The International Journal of Life Cycle Assessment*, 24, 1307–1318. https://doi.org/10.1007/s11367-019-01589-8 |
| **License name** | Springer Nature copyright (all rights reserved unless open-access option taken) |
| **License URL** | https://link.springer.com/article/10.1007/s11367-019-01589-8 |
| **Commercial use** | ✗ Journal copyright; reproduction requires publisher permission |
| **Attribution required** | Yes |
| **Redistribution** | Publisher permission required |
| **Notes** | Provides freshwater depletion shadow prices used in the Water Consumption economic damage pathway. An authors' accepted manuscript may be available via TNO or TU Delft institutional repositories. |

---

### 6.9 Debarre et al. (2022) — Water Consumption Health Damages

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Debarre, R. et al. (2022). [Full citation to be confirmed — DALY-based health damage from water deprivation]. Cited in `220511_Water consumption_update.xlsx`. |
| **License name** | To be determined |
| **License URL** | To be confirmed |
| **Commercial use** | To be determined |
| **Attribution required** | Yes |
| **Redistribution** | To be determined |
| **Notes** | Used for the DALY-based health damage pathway in the Water Consumption indicator. Full bibliographic details not yet included in WifOR input file metadata; flagged in BACKLOG.md. |

---

### 6.10 EPS — Environmental Priority Strategies (Land Use)

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Steen, B. (2015). *EPS 2015d.1 — A system for weighting environmental characteristics according to their contribution to safeguard subjects*. Swedish Life Cycle Center, Chalmers University of Technology. https://www.lifecyclecenter.se/projects/eps-environmental-priority-strategies-in-product-design/ |
| **License name** | Open academic access — no formal Creative Commons licence declared |
| **License URL** | https://www.lifecyclecenter.se/ |
| **Commercial use** | ✓ Broadly used in commercial LCA practice; no stated restriction |
| **Attribution required** | Yes |
| **Redistribution** | CPM LCA Database companion data freely accessible; no explicit redistribution restriction |
| **Notes** | The EPS system monetises ecosystem service loss across five safeguard subjects. The EPS 2015d.1 weighting factors are the basis for the Land Use indicator's ecosystem service damage costs (working capacity, water treatment, crop growth, biodiversity). |

---

### 6.11 LANCA — Land Use Characterisation Factors

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Bach, V., Lehmann, A., Görmer, M., Finkbeiner, M. (2020). *LANCA® Characterization Factors for Life Cycle Assessment, Version 2.5*. Fraunhofer Institute for Building Physics IBP. https://www.ibp.fraunhofer.de/en/expertise/life-cycle-engineering/applied-methods/lanca.html |
| **License name** | Fraunhofer IBP copyright — free for research and academic use; no formal CC licence |
| **License URL** | https://www.ibp.fraunhofer.de/en/expertise/life-cycle-engineering/applied-methods/lanca.html |
| **Commercial use** | Restricted — Fraunhofer IBP copyright; commercial use requires separate agreement |
| **Attribution required** | Yes |
| **Redistribution** | Not permitted without Fraunhofer IBP permission |
| **Notes** | LANCA provides country-level land use characterisation factors for four sub-indicators (mechanical filtration, physicochemical filtration, groundwater replenishment, biotic production capacity, erosion resistance) used to localise EPS global values to national conditions in the Land Use indicator. Factors are downloadable after registration from the Fraunhofer IBP website. |

---

### 6.12 Ahlroth (2009) — Water Pollution WTP Base Values (Sweden)

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Ahlroth, S. (2009). [Full citation to be confirmed — Swedish WTP estimates for N/P in freshwater and marine environments]. Cited in `230324_WaterPollution_Mon_Coef_Final_DC.xlsx` as the basis for PPP value transfer. |
| **License name** | To be determined (likely Swedish EPA report or journal article) |
| **License URL** | To be confirmed |
| **Commercial use** | To be determined |
| **Attribution required** | Yes |
| **Redistribution** | To be determined |
| **Notes** | Provides the Swedish baseline WTP values used in the Water Pollution PPP value transfer: freshwater phosphorus (USD 136/kg), marine phosphorus (USD 68/kg), marine nitrogen (USD 9/kg). Full bibliographic details not yet in WifOR input file metadata; flagged in BACKLOG.md. |

---

### 6.13 Steen (2020) — Water Pollution Nutrients (N, P)

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Steen, B. (2020). [Full citation to be confirmed — eutrophication damage valuation for N and P]. Swedish Life Cycle Center / Chalmers University of Technology. Cited in `230324_WaterPollution_Mon_Coef_Final_DC.xlsx`. |
| **License name** | Open academic access — Swedish Life Cycle Center; no formal CC licence declared |
| **License URL** | https://www.lifecyclecenter.se/ |
| **Commercial use** | ✓ Broadly used in academic and commercial LCA practice |
| **Attribution required** | Yes |
| **Redistribution** | Not explicitly stated |
| **Notes** | Provides the damage valuation methodology for freshwater eutrophication (N and P) used in the Water Pollution indicator nutrient pathway. Steen is the creator of the EPS framework; this 2020 work extends the EPS approach to nutrient damage costs. |

---

### 6.14 USEtox — Chemical Toxicity Model (Water Pollution — Heavy Metals)

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Rosenbaum, R.K. et al. (2008). USEtox — The UNEP-SETAC toxicity model for comparative assessment of chemicals (organic chemicals). *The International Journal of Life Cycle Assessment*, 13(7), 532–546. Model: https://usetox.org |
| **License name** | USEtox Licence Agreement — personal, royalty-free, non-exclusive, non-transferable, perpetual |
| **License URL** | https://www.usetox.org/model/license |
| **Commercial use** | ✓ Commercial use of *results* generated using USEtox is permitted; the model itself may not be redistributed or renamed |
| **Attribution required** | Yes — "USEtox" must be cited |
| **Redistribution** | ✗ Model redistribution not permitted; results (characterisation factors) may be used commercially |
| **Notes** | USEtox is endorsed by UNEP and SETAC as the international consensus model for human toxicity and ecotoxicity in LCA. Characterisation factors for heavy metals (As, Cd, Hg, Cr, Pb, Ni, Cu, Zn, Sb) in water are used in the Water Pollution indicator. Results generated with unmodified USEtox data may be labelled "USEtox factors." |

---

### 6.15 Psacharopoulos & Patrinos (2018) — Returns to Education (Training)

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Psacharopoulos, G., Patrinos, H.A. (2018). Returns to investment in education: a decennial review of the global literature. *Education Economics*, 26(5), 445–458. https://doi.org/10.1080/09645292.2018.1484426. Also available as World Bank Policy Research Working Paper WPS8402 (open access): https://documents.worldbank.org/curated/en/442521523465644318 |
| **License name** | Taylor & Francis copyright (journal version); World Bank Open Access — CC BY 3.0 IGO (WPS8402 version) |
| **License URL** | Journal: https://www.tandfonline.com/doi/abs/10.1080/09645292.2018.1484426 · WB WP: https://documents.worldbank.org/curated/en/442521523465644318 |
| **Commercial use** | ✗ Journal version (publisher copyright); ✓ World Bank WP version (open including commercial) |
| **Attribution required** | Yes |
| **Redistribution** | Journal version: publisher permission required; WB WP version: permitted with attribution |
| **Notes** | Provides the global meta-analysis of returns to schooling (~9% per year of education, with regional variation) that forms the basis for the Training indicator. The World Bank working paper version (WPS8402) is freely accessible and recommended for citation and reuse. |

---

### 6.16 GIVE Model — Global Impacts and Valuation of Emissions (UBA MC 4.0 GHG)

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Anthoff, D. (2025). *GIVE model — Global Impacts and Valuation of Emissions*. [Academic publication and model repository; version used in UBA Handbook MC 4.0.] |
| **License name** | To be confirmed — academic model; likely open-source (MIT or similar) on GitHub |
| **License URL** | To be confirmed |
| **Commercial use** | To be confirmed |
| **Attribution required** | Yes — Anthoff and UBA Handbook (Eser et al. 2025) must be cited |
| **Redistribution** | To be confirmed |
| **Notes** | The GIVE model (successor to the FUND model) is used exclusively by UBA MC 4.0 to derive GHG value factors (Table 1). It applies equity-weighted damage functions with German income as the reference point, providing two PRTP scenarios (0 % and 1 %). GIVE models CH₄ and N₂O directly (not via GWP100 proxies), unlike DICE/RICE. This is the key methodological distinction between UBA and WifOR GHG value factors. |

---

### 6.17 Environmental Prices Handbook EU27 — CE Delft 2024

| Attribute | Detail |
|-----------|--------|
| **Full citation** | De Vries, J. et al. (2025). *Environmental Prices Handbook EU27, 2024 edition*. CE Delft, Delft, April 2025. |
| **License name** | CE Delft proprietary — all rights reserved |
| **License URL** | https://ce.nl/en/ |
| **Commercial use** | ✗ Restricted — handbook purchased or licensed from CE Delft; value factors not freely redistributable |
| **Attribution required** | Yes — CE Delft and the specific handbook edition must be cited |
| **Redistribution** | ✗ Not permitted without CE Delft permission |
| **Notes** | Primary source for all CE Delft 2024 value factors (Tables 1–8 covering GHG, air pollutants, water, heavy metals, fossil ADP, radionuclides, critical minerals, land use). The handbook provides EU27-average values in EUR 2021 that must be transferred to other countries via VFT (see VALUE_TRANSFER.md). |

---

### 6.18 Eurostat — Occupational Safety Statistics (OHS)

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Eurostat (annual). *European Statistics on Accidents at Work (ESAW)*. Statistical Office of the European Union. https://ec.europa.eu/eurostat/web/health/health-safety-work |
| **License name** | Creative Commons Attribution 4.0 International (CC BY 4.0) — pursuant to EC Decision 2011/833/EU |
| **License URL** | https://creativecommons.org/licenses/by/4.0/ |
| **Commercial use** | ✓ Permitted |
| **Attribution required** | Yes — "Source: Eurostat" |
| **Redistribution** | Permitted with attribution |
| **Notes** | Provides European workplace incident rate statistics (fatal and non-fatal accidents, occupational diseases, by sector) used in the OHS indicator. Eurostat data are published under CC BY 4.0 terms applicable to all EC institutional data under Decision 2011/833/EU. |

---

### 6.19 IHME — Global Burden of Disease (OHS Disability Weights)

| Attribute | Detail |
|-----------|--------|
| **Full citation** | Institute for Health Metrics and Evaluation (IHME) (2019). *Global Burden of Disease Study 2019 (GBD 2019) Results*. University of Washington, Seattle. https://www.healthdata.org/gbd |
| **License name** | IHME Non-Commercial User Agreement |
| **License URL** | https://www.healthdata.org/data-tools-practices/data-practices/ihme-free-charge-non-commercial-user-agreement |
| **Commercial use** | ✗ Non-commercial and academic use only |
| **Attribution required** | Yes — IHME and GBD study year must be cited |
| **Redistribution** | Non-commercial redistribution with attribution permitted |
| **Notes** | GBD disability weights (severity scores 0–1 for each injury/disease category) are used in the OHS indicator to calculate Years Lived with Disability (YLD). The GBD study is the global standard for disability weights. Commercial applications using GBD data should contact IHME for licensing. |

---

## Data Update Guidance

### When to Update

Each input file has recommended update frequency:

| File | Frequency | Trigger |
|------|-----------|---------|
| Model definitions | Annual | New countries, sector updates |
| GDP deflators | Quarterly | World Bank releases |
| GHG (DICE) | Annual | Model updates |
| Air Pollution | Biannual | UBA methodology updates |
| Waste | Biannual | OECD data releases |
| Water Consumption | Annual | AWARE updates |
| Land Use | Annual | EPS/LANCA updates |
| Water Pollution | Annual | Methodology refinement |
| Training | Biannual | Education research updates |
| OHS | Annual | GBD study updates |

### How to Update

Detailed update procedures for each file are documented in **DATA_UPDATES.md**.

General process:
1. Monitor source for updates
2. Download new data
3. Validate schema compatibility
4. Backup current version
5. Replace file
6. Regenerate coefficients
7. Validate outputs
8. Document changes

---

## Quality and Limitations

### Data Quality Assessment

See README.md Section 6 for maturity levels:
- **Well Established**: GHG, OHS
- **Solid**: Waste, Air, Land Use
- **Average**: Training
- **Experimental**: Water Consumption, Water Pollution

### Known Limitations

1. **Pre-calculated Values**: 6 indicators use Excel pre-calculations
   - Formulas not in version control
   - Harder to audit and reproduce
   - See BACKLOG.md S14 for improvement plan

2. **Data Vintage**: Files from 2022-2024
   - Some based on older research
   - Inconsistent update cycles

3. **Experimental Methodologies**: Water indicators
   - High uncertainty acknowledged
   - Ongoing research needed

4. **Country Coverage**: Not all countries in all datasets
   - Missing data handled via interpolation or regional averages
   - Documented in individual scripts

---

## Related Documentation

- **METHODOLOGY.md**: How input files are processed into value factors
- **DATA_UPDATES.md**: Detailed update procedures for each file
- **ARCHITECTURE_DECISIONS.md**: Why certain data formats were chosen
- **BACKLOG.md**: Future improvements to data management

---

**Document Version**: 2.0
**Last Updated**: 2026-03-09
**Maintained by**: WifOR Development Team
**Contact**: dimitrij.euler@greenings.org
