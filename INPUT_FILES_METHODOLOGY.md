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

**Script**: `001_generate_air_pollution.py`
**Replaces**: `220707_Air pollution_update.xlsx`

#### Generation Process

The `001_generate_air_pollution.py` script programmatically generates air pollution damage costs, replacing the previous static Excel file. It implements the UBA (German Federal Environment Agency) methodology, including an income elasticity-based value transfer to apply German base values to 188 countries.

#### Methodology Overview

The script calculates damage costs for six key pollutants across four environmental impact categories.

- **Pollutants**: PM2.5, PM10, NOx, SOx, NMVOC, NH3
- **Damage Categories**: Health, Biodiversity, Crop, Material

The core of the methodology is to take base damage costs established for Germany and adjust them for other countries based on their GDP per capita, reflecting differences in willingness-to-pay for environmental quality and health.

#### Data Sources and Data Gathering

1.  **UBA Methodenkonvention 3.1 (Methodological Convention 3.1)**
    *   **Data Provided**: Base damage costs for Germany (in EUR/tonne for the year 2020).
    *   **Data Gathering Methodology**: The UBA's framework is a comprehensive national standard for assessing environmental costs. It synthesizes a wide range of data from national economic accounts, scientific studies, and environmental monitoring. The values are derived from detailed impact pathway assessments, which model the cause-and-effect chain from pollutant emission to final environmental or health impact, and then monetize these impacts using various economic valuation techniques (e.g., medical costs, productivity loss, repair costs).

2.  **NEEDS (New Energy Externalities Developments for Sustainability) EU Project**
    *   **Data Provided**: Dose-response functions and other foundational data used in impact pathway assessments.
    *   **Data Gathering Methodology**: As a major EU research project, NEEDS collected and harmonized data from numerous sources, including administrative records, health surveys, and environmental monitoring stations across Europe. It employed a range of participatory and survey-based tools to gather primary data and ensure its reliability through triangulation.

3.  **World Bank Open Data**
    *   **Data Provided**: GDP per capita (PPP, current international $) and GDP deflators.
    *   **Data Gathering Methodology**: The World Bank compiles economic data from the national accounts of its member countries. The data is standardized to ensure cross-country comparability. GDP and PPP data are collected through annual surveys of national statistical offices.

#### Value Transfer Mechanism

To adapt the German-centric UBA base costs for global application, the script employs an **income elasticity adjustment**.

*   **Formula**: `V_target = V_base × (GDP_target / GDP_base) ^ elasticity`
    *   `V_target`: The calculated damage cost for the target country.
    *   `V_base`: The base damage cost from UBA for Germany.
    *   `GDP_target`: GDP per capita of the target country.
    *   `GDP_base`: GDP per capita of Germany.
    *   `elasticity`: An income elasticity parameter (set to 1.0 in the script, based on research by Viscusi & Aldy and OECD meta-analyses), which represents how willingness-to-pay for health and environmental quality changes with income.

This method allows for a systematic and economically grounded way to estimate damage costs in countries where detailed local studies are not available.

#### Final Output

The script generates a detailed output file (`air_pollution_damage_costs_detailed.h5` and `.xlsx`) containing the calculated damage costs for each pollutant, country, and damage category, as well as a summary file with the total damage costs.

---

### 3. Waste Management

**Script**: `002_generate_waste.py`
**Replaces**: `220509_Waste figures merged_update.xlsx`

#### Generation Process

The `002_generate_waste.py` script calculates damage costs for waste management, categorized by waste type (hazardous, non-hazardous) and treatment method (incineration, landfill, recovery). It replaces a previous Excel-based calculation with a transparent and reproducible Python script.

#### Methodology Overview

The script uses a mixed-method approach, combining data from multiple sources to value the different impact pathways of waste management.

*   **Landfill**: The cost is a sum of GHG emissions from methane, disamenity costs (nuisance to nearby residents), and the risk of leachate contamination.
*   **Incineration**: The cost is based on the air pollution damages from emissions.
*   **Recovery**: This is assumed to have a zero or negative cost, representing an avoided impact, though it is currently set to zero as a conservative assumption.

#### Data Sources and Data Gathering

1.  **IPCC Emission Factor Database (EFDB)**
    *   **Data Provided**: Methane emission factors for different types of landfills.
    *   **Data Gathering Methodology**: The EFDB is a repository of emission factors collected from various sources, including scientific literature, industry measurements, and national inventory reports. Data is peer-reviewed and must meet quality standards defined in the IPCC Guidelines for National Greenhouse Gas Inventories.

2.  **EXIOBASE**
    *   **Data Provided**: Environmentally-extended multi-regional input-output tables, which provide a detailed picture of the economic and environmental flows between industries and countries.
    *   **Data Gathering Methodology**: EXIOBASE is constructed by harmonizing and detailing supply and use tables from multiple countries. It uses a top-down approach, reconciling national-level data with global economic estimates and then disaggregating it to a high level of detail.

3.  **UBA (German Federal Environment Agency)**
    *   **Data Provided**: Air pollution damage costs used to value the emissions from waste incineration.
    *   **Data Gathering Methodology**: See the "Air Pollution" section for a detailed explanation of the UBA's data gathering methodology.

4.  **PwC Research**
    *   **Data Provided**: Disamenity costs associated with landfills.
    *   **Data Gathering Methodology**: This data is from proprietary research conducted by PwC, likely based on hedonic pricing studies that analyze the impact of proximity to waste sites on property values.

#### Final Output

The script generates a detailed output file (`waste_damage_costs_detailed.h5` and `.xlsx`) with damage costs for each waste category, treatment method, and country, as well as a summary file.

---

### 4. Water Consumption

**Script**: `003_generate_water_consumption.py`
**Replaces**: `220511_Water consumption_update.xlsx`
**Status**: EXPERIMENTAL

#### Generation Process

The `003_generate_water_consumption.py` script calculates the damage costs of freshwater consumption. It replaces a previous Excel-based calculation with a Python script that, while still experimental, is more transparent. The methodology has high uncertainty and should be used with caution.

#### Methodology Overview

The script uses a dual approach to value water consumption, capturing both economic and health-related impacts.

*   **Economic Damages**: Calculated using a shadow pricing method, where the price of water is adjusted based on local water scarcity.
*   **Health Damages**: Valued using the Disability-Adjusted Life Years (DALYs) approach, which quantifies the health burden of inadequate water access.

#### Data Sources and Data Gathering

1.  **WULCA AWARE (Available WAter REmaining)**
    *   **Data Provided**: Water scarcity characterization factors (AWARE factors).
    *   **Data Gathering Methodology**: AWARE is a consensus-based method developed by the WULCA (Water Use in Life Cycle Assessment) working group. It quantifies the relative available water remaining per area after the demands of humans and ecosystems have been met. The calculation is based on a global hydrological model (WaterGAP) and provides a measure of water scarcity from 0.1 (abundant) to 100 (scarce).

2.  **Global Burden of Disease (GBD) Study**
    *   **Data Provided**: Disability-Adjusted Life Years (DALYs) associated with unsafe water sources.
    *   **Data Gathering Methodology**: The GBD study is a comprehensive global research program that assesses mortality and disability from major diseases, injuries, and risk factors. It synthesizes data from a wide range of sources, including vital registration systems, household surveys, and health facility records, using complex statistical modeling to estimate health burdens for all regions of the world.

3.  **Academic Research (Ligthart & van Harmelen, 2019; Debarre et al., 2022)**
    *   **Data Provided**: The conceptual basis for the shadow pricing and health damage methodologies.
    *   **Data Gathering Methodology**: These are academic publications that provide the theoretical framework and models for valuing water consumption, rather than raw data.

#### Final Output

The script generates an experimental output file (`water_consumption_damage_costs_EXPERIMENTAL.h5` and `.xlsx`) containing the economic, health, and total damage costs per cubic meter of water consumed for each country.

---

### 5. Land Use

**Script**: `004_generate_land_use.py`
**Replaces**: `230317_Landuse_update_ZK.xlsx`

#### Generation Process

The `004_generate_land_use.py` script generates damage costs associated with land use change. It replaces a previous Excel-based calculation with a Python script that implements the Environmental Priority Strategies (EPS) methodology, adjusted with LANCA characterization factors.

#### Methodology Overview

The script calculates the value of ecosystem services lost when natural land is converted to other uses. It covers several land use types and monetizes the loss of four key ecosystem services.

*   **Land Use Types**: Urban, Arable, Permanent Crops, Pasture, Forest, Wetland, and Other Natural Land.
*   **Ecosystem Services Valued**: Working Capacity, Water Treatment, Crop Growth, and Biodiversity.

The methodology uses global average values from the EPS system and adjusts them to local conditions using LANCA regional factors and a GDP-based income elasticity adjustment.

#### Data Sources and Data Gathering

1.  **EPS (Environmental Priority Strategies) System**
    *   **Data Provided**: Base values for ecosystem service loss (in EUR per hectare per year).
    *   **Data Gathering Methodology**: The EPS system, developed by the Swedish Environmental Research Institute (IVL), is a Life Cycle Assessment (LCA) based method. It aggregates environmental impacts into a single unit (Environmental Load Unit, ELU), which is then monetized. The data is derived from a comprehensive inventory of materials and processes and their environmental impacts.

2.  **LANCA (Land Use Indicator Value Calculation) Model**
    *   **Data Provided**: Regional characterization factors to adjust the global EPS values.
    *   **Data Gathering Methodology**: LANCA is a map-based model that assesses land use impacts on a local to global scale. It uses geo-ecological classification systems and area-specific input data to calculate characterization factors for various impact categories, including biodiversity.

3.  **Steen (2020)**
    *   **Data Provided**: The underlying environmental valuation methodology for the EPS system.
    *   **Data Gathering Methodology**: This is an academic publication that provides the theoretical framework for the EPS system.

#### Final Output

The script generates a detailed output file (`land_use_damage_costs_detailed.h5` and `.xlsx`) containing the damage costs for each land use type, ecosystem service, and country, as well as a summary file.

---

### 6. Water Pollution

**Script**: `005_generate_water_pollution.py`
**Replaces**: `230324_WaterPollution_Mon_Coef_Final_DC.xlsx`
**Status**: EXPERIMENTAL

#### Generation Process

The `005_generate_water_pollution.py` script calculates damage costs for water pollution, covering both nutrient pollution (eutrophication) and heavy metal contamination. It replaces a previous Excel-based calculation with a more transparent, albeit still experimental, Python script.

#### Methodology Overview

The script uses a hybrid approach, combining different methodologies for different types of pollutants.

*   **Nutrients (Nitrogen, Phosphorus)**: The damage costs are based on the methodology of Steen (2020), which focuses on the impacts of eutrophication.
*   **Heavy Metals**: The script uses the USEtox model for characterization, combined with a damage cost to value the impacts.
*   **Value Transfer**: The script uses a Purchasing Power Parity (PPP) adjustment to transfer Willingness-to-Pay (WTP) values from a Swedish context (Ahlroth, 2009) to other countries.
*   **Water Scarcity Adjustment**: The final damage costs are adjusted based on local water scarcity using AWARE factors.

#### Data Sources and Data Gathering

1.  **Steen (2020)**
    *   **Data Provided**: The methodology for valuing the impacts of nutrient pollution (eutrophication).
    *   **Data Gathering Methodology**: An academic publication providing a framework for valuation.

2.  **USEtox Model**
    *   **Data Provided**: Characterization factors for heavy metals.
    *   **Data Gathering Methodology**: USEtox is a scientific consensus model that provides characterization factors for human and ecotoxicological impacts of chemical emissions. It is based on a comprehensive database of chemical properties and environmental fate and transport models.

3.  **Ahlroth (2009)**
    *   **Data Provided**: Base Willingness-to-Pay (WTP) values for nutrient pollution in a Swedish context.
    *   **Data Gathering Methodology**: An academic study that likely used contingent valuation or other economic survey methods to elicit WTP values from the public.

4.  **WULCA AWARE (Available WAter REmaining)**
    *   **Data Provided**: Water scarcity characterization factors (AWARE factors).
    *   **Data Gathering Methodology**: See the "Water Consumption" section for a detailed explanation.

5.  **World Bank Open Data**
    *   **Data Provided**: Purchasing Power Parity (PPP) data for the value transfer mechanism.
    *   **Data Gathering Methodology**: See the "Air Pollution" section for a detailed explanation.

#### Final Output

The script generates an experimental output file (`water_pollution_damage_costs_EXPERIMENTAL.h5` and `.xlsx`) containing the damage costs for each pollutant and country.

---

### 7. Training

**Script**: `014_241016_prepare_Training_my.py`
**Replaces**: `220529_training_value_per_hour_bysector.h5`

#### Generation Process

The `014_241016_prepare_Training_my.py` script generates coefficients for the economic benefit of employee training. This is the only value factor with a positive coefficient, as it represents a benefit to society rather than a damage cost. The script replaces a previous HDF5 file with a more transparent calculation process.

#### Methodology Overview

The script is based on the human capital theory, which treats training as an investment that yields returns in the form of increased productivity and higher wages.

*   **Core Concept**: The value of training is the present value of the future wage increases that result from it.
*   **Calculation Steps**:
    1.  Establish a baseline for the returns to education using a global meta-analysis.
    2.  Equate training hours to formal education years.
    3.  Project the lifetime value of the wage premium from training.
    4.  Adjust the value for different economic sectors and countries using PPP and GVA data.

#### Data Sources and Data Gathering

1.  **Psacharopoulos & Patrinos (2018), "Returns to investment in education: a global update"**
    *   **Data Provided**: A global meta-analysis of the returns to schooling, finding an average 9-10% wage increase per additional year of schooling.
    *   **Data Gathering Methodology**: This is a comprehensive review of 1120 estimates from 139 countries between 1950 and 2014, using the Mincerian earnings function and full discounting method.

2.  **OECD Education Data**
    *   **Data Provided**: Data on education systems, including sector-specific wage premiums.
    *   **Data Gathering Methodology**: The OECD collects data on the structure, finances, and performance of education systems from its member countries, following international standards to ensure comparability.

3.  **World Bank Open Data**
    *   **Data Provided**: Purchasing Power Parity (PPP) and Gross Value Added (GVA) per worker data, used for value transfer and sector-specific adjustments.
    *   **Data Gathering Methodology**: See the "Air Pollution" section for a detailed explanation.

#### Final Output

The script generates an output file (`training_value_per_hour.h5` and `.xlsx`) containing the monetized benefit of one hour of training for each country and economic sector.

---

### 8. Occupational Health & Safety (OHS)

**Script**: `006_generate_ohs.py`
**Replaces**: `220616_monetization_value_per_incident_NEW.xlsx`

#### Generation Process

The `006_generate_ohs.py` script calculates the damage costs of occupational health and safety incidents. It replaces a previous Excel-based calculation with a Python script that implements a DALY-based valuation methodology.

#### Methodology Overview

The script calculates the monetary value of harm from workplace incidents by quantifying the Disability-Adjusted Life Years (DALYs) lost.

*   **DALY Calculation**: `DALY = YLL (Years of Life Lost) + YLD (Years Lived with Disability)`
*   **Monetization**: The calculated DALYs are multiplied by a Value of a Statistical Life Year (VSLY) to arrive at a monetary damage cost.
*   **Value Transfer**: The script can be configured to use either a single global VSLY for all countries (the "ethical" approach) or an income-adjusted VSLY based on the country's GDP per capita (the "Willingness-to-Pay" approach).

#### Data Sources and Data Gathering

1.  **Eurostat**
    *   **Data Provided**: Data on the incidence rates of fatal and non-fatal occupational accidents.
    *   **Data Gathering Methodology**: Eurostat collects data from the national statistical authorities of EU member states. The data is harmonized according to the European Statistics on Accidents at Work (ESAW) methodology to ensure comparability.

2.  **Global Burden of Disease (GBD) Study**
    *   **Data Provided**: Disability weights for various health states, which are used to calculate the Years Lived with Disability (YLD).
    *   **Data Gathering Methodology**: See the "Water Consumption" section for a detailed explanation of the GBD's data gathering methodology.

3.  **World Health Organization (WHO)**
    *   **Data Provided**: Life expectancy data for each country, which is used to calculate the Years of Life Lost (YLL).
    *   **Data Gathering Methodology**: The WHO calculates life expectancy from life tables, which are constructed using sex- and age-specific death rates from national civil registration systems and other sources.

#### Final Output

The script generates a detailed output file (`ohs_damage_costs_detailed.h5` and `.xlsx`) with the DALYs per incident, the VSLY used, and the final damage cost for each incident category and country, as well as a summary file.

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
