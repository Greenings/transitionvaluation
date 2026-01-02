# Input Files Methodology and Data Origins

**WifOR Value Factors - Data Provenance Documentation**
**Version**: 1.0
**Last Updated**: 2026-01-02

This document provides comprehensive documentation of input files used within the WifOR Impact Valuation framework, detailing their origins, underlying methodologies, and the processes used to generate the data.

---

## Table of Contents

1. [Overview](#overview)
2. [Ecosystem Context](#ecosystem-context)
3. [General Framework](#general-framework)
4. [Shared Input Files](#shared-input-files)
5. [Indicator-Specific Input Files](#indicator-specific-input-files)
6. [Public Data Sources](#public-data-sources)

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

### 1. Greenhouse Gas Emissions (GHG)

**File**: `20241022_scc_nordhaus.h5`
**Script**: `020_241024_prepare_GHG_my.py`

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

## Public Data Sources

### Comprehensive List

#### International Organizations

**World Bank**
- GDP Deflators
- Economic indicators
- https://data.worldbank.org

**OECD**
- Waste statistics
- Water data
- Education data
- https://stats.oecd.org

**WHO (World Health Organization)**
- Life expectancy
- Health burden data
- https://www.who.int/data

**IPCC (Intergovernmental Panel on Climate Change)**
- Emission factors
- Climate data
- https://www.ipcc-nggip.iges.or.jp

#### Regional Agencies

**UBA (German Federal Environment Agency)**
- Air pollution methodology
- Environmental damage costs
- https://www.probas.umweltbundesamt.de/

**Eurostat**
- Occupational safety data
- European statistics
- https://ec.europa.eu/eurostat

#### Research Projects

**NEEDS (EU Project)**
- External cost database
- https://cordis.europa.eu/project/id/502687

**EXIOBASE**
- Environmentally-extended input-output database
- https://www.exiobase.eu/

**USEtox**
- Chemical toxicity model
- https://usetox.org

**AWARE**
- Water scarcity indicators
- https://wulca-waterlca.org/aware/

**EPS (Environmental Priority Strategies)**
- Ecosystem valuation
- https://lifecyclecenter.se/projects/eps

**LANCA**
- Land use characterization
- https://www.ibp.fraunhofer.de/en/expertise/life-cycle-engineering/applied-methods/lanca.html

#### Academic Resources

**DICE Model (Nordhaus)**
- Social Cost of Carbon
- http://www.williamnordhaus.com/dice-rice-models

**Global Burden of Disease**
- Disability weights
- https://www.healthdata.org/gbd

**Returns to Education Research**
- Psacharopoulos & Patrinos (2018)
- Available through OECD and academic databases

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

**Document Version**: 1.0
**Last Updated**: 2026-01-02
**Maintained by**: WifOR Development Team
**Contact**: dimitrij.euler@greenings.org
