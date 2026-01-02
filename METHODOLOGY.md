# Value Factor Calculation Methodology

**WifOR Impact Valuation Framework**
**Version**: 1.0
**Last Updated**: 2026-01-02

This document describes the detailed methodology for calculating environmental and social value factors used in WifOR's impact valuation framework.

---

## Table of Contents

1. [Common Architecture](#common-architecture)
2. [Mathematical Framework](#mathematical-framework)
3. [Script-Specific Methodologies](#script-specific-methodologies)
4. [Data Processing Pipeline](#data-processing-pipeline)
5. [Quality Assurance](#quality-assurance)

---

## Conceptual Foundation: Damage or Value to Society

### Theoretical Basis

The WifOR methodology calculates **damage or value to society** using welfare economics principles, not legal liability or company financial impacts.

#### Definition

**Damage/Value to Society** = Total external costs or benefits imposed on/provided to all of society
- Measured from society's collective welfare perspective
- Includes all affected parties (not just those with legal standing)
- Captures non-market values (ecosystem services, public health, climate stability)
- Extends to future generations and long-term impacts

**This is fundamentally different from:**
- Legal liability under tort law (Handlungsstörer, Zustandsstörer, nuisance doctrine)
- Regulatory penalties and compliance costs
- Company financial provisions or risk reserves
- Insurance claims or lawsuit settlements

### Methodological Approach

#### 1. Damage Cost Method (Primary)

**Formula:**
```
Societal Damage = ∑(Physical Impact × Damage Cost Coefficient)
```

Where:
- **Physical Impact**: Quantified environmental/social change (e.g., tons CO2, kg PM2.5, m³ water)
- **Damage Cost Coefficient**: Monetary value of harm per unit to society

**Example: Air Pollution (PM2.5)**
```
Physical Impact: 100 tons PM2.5 emitted
Damage Coefficient: $5,000 / ton (premature mortality, morbidity, productivity losses)
Societal Damage: 100 × $5,000 = $500,000

This represents:
✓ Total health burden on affected population
✓ Medical costs + lost productivity + mortality value
✓ All exposure victims (not just those who file claims)

This does NOT represent:
✗ Fine paid to environmental agency ($10,000)
✗ Lawsuit settlement with neighbors ($50,000)
✗ Compliance costs for pollution controls ($200,000)
```

#### 2. Alternative Methods

When direct damage costs are infeasible:

**Abatement Cost Approach:**
- Cost society would bear to prevent/remediate the damage
- Used when damage pathways are uncertain but prevention is measurable
- Example: Cost of CO2 capture to prevent climate damages

**Willingness-to-Pay (WTP):**
- Market-based valuation of society's preferences
- Used for non-market goods (recreation, biodiversity)
- Example: Value of preserving endangered species habitat

#### 3. Benefit Valuation (Positive Values)

For positive social impacts (e.g., training):

**Formula:**
```
Societal Value = ∑(Activity × Value Coefficient)
```

**Example: Worker Training**
```
Activity: 10,000 hours of training provided
Value Coefficient: +$25/hour (productivity gains, innovation, economic growth)
Societal Value: 10,000 × $25 = +$250,000

This represents:
✓ Total value to society from skilled workforce
✓ Increased GDP, innovation capacity, competitiveness

This does NOT represent:
✗ Company's training budget expenditure
✗ ROI to the company from improved employee performance
```

### Comparison: Societal vs. Legal/Financial

| Dimension | Damage/Value to Society (This Methodology) | Legal Liability / Company Cost |
|-----------|-------------------------------------------|-------------------------------|
| **Conceptual Basis** | Welfare economics, externalities | Tort law, regulatory compliance |
| **Scope** | All affected parties globally | Only legally recognized claimants |
| **Time Horizon** | Long-term, future generations | Current legal framework period |
| **Coverage** | Market + non-market values | Compensable damages only |
| **Measurement** | Social cost of carbon, VSL, DALYs | Court awards, fines, settlements |
| **Magnitude** | Typically 10-100× larger | Limited by legal doctrines |
| **Use Case** | Impact materiality, ESG, strategy | Financial accounting, risk reserves |

### Practical Implications

**For Developers:**
- Coefficients represent marginal societal harm/benefit, not marginal company cost
- Sign convention: Negative = damage to society, Positive = benefit to society
- Values do not include company internalized costs (already in P&L)
- Do not use for financial provisioning or legal liability estimation

**For Data Validation:**
- Expect societal values >> regulatory fines or typical lawsuit damages
- Cross-sector variation reflects differential societal impacts, not legal risk
- Country-specific coefficients reflect local damage (e.g., health costs), not legal systems

---

## Common Architecture

### Overview

All 8 value factor preparation scripts follow an identical 5-section workflow:

```
┌─────────────────────┐
│ 1. CONFIGURATION    │  Load indicator settings from config.py
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 2. LOAD DATA        │  Load indicator data + shared dependencies
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 3. PROCESS COEFF    │  Transform raw data into coefficient matrices
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 4. APPLY DEFLATION  │  Adjust for inflation across time periods
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 5. SAVE RESULTS     │  Export to HDF5 and Excel
└─────────────────────┘
```

### Shared Infrastructure

All scripts leverage **value_factor_utils.py** containing 11 reusable functions:

#### Data Loading Functions
- `load_common_data()`: Loads model definitions (188 countries, NACE sectors) and World Bank GDP deflators
- Returns: `(countries, nace_sectors, deflators_df)`

#### Coefficient Processing Functions
- `create_coefficient_dataframe(years, indicators, countries, nace_sectors)`
  - Creates multi-indexed DataFrame: `(Year × Indicator) × (Country × Sector)`
  - Initializes all values to 0.0

- `populate_coefficients(coeff_df, raw_data, coefficient_sign, indicator_mapping)`
  - Fills coefficient matrix with country/indicator-specific values
  - Applies sign convention: -1.0 for damages, +1.0 for benefits

#### Inflation Adjustment Functions
- `calculate_inflation_factors(deflators_df, years, base_year, reference_country='USA')`
  - Computes inflation multipliers normalized to base year
  - Formula: `factor[year] = deflator[year] / deflator[base_year]`
  - Uses USA deflator for global consistency

- `apply_deflation(coeff_df, inflation_factors)`
  - Multiplies all coefficients by year-specific inflation factors
  - Converts to constant base-year USD

#### Unit Management Functions
- `create_units_dataframe(indicators, countries, nace_sectors, base_unit)`
  - Creates unit metadata structure matching coefficient dimensions

- `update_units_with_years(units_df, years, base_year, last_deflator_year, base_unit)`
  - Adds year prefixes: "2020USD/kg", "2025USD/m3", etc.
  - For forecast years beyond deflator data, uses last available year

#### Output Functions
- `save_results(coeff_df, units_df, output_path_h5, output_path_excel, hdf_key='coefficients')`
  - Exports coefficients to HDF5 (structured, efficient)
  - Exports to Excel with separate sheets for coefficients and units

### Common Data Dependencies

#### Model Definitions (Used by ALL scripts)
- **File**: `input_data/Model_definitions_owntable.h5`
- **Key**: `owntable`
- **Contents**:
  - 188 countries with ISO3 codes (e.g., USA, DEU, CHN)
  - NACE economic sector classifications
  - Provides structural foundation for all outputs

#### GDP Deflators (Used by ALL scripts)
- **File**: `input_data/241001_worldbank_deflator.h5`
- **Key**: `deflator`
- **Contents**:
  - World Bank GDP deflators by country and year
  - Enables temporal consistency via inflation adjustment
  - Normalized to base year (2020 for most, 2019 for GHG)

---

## Mathematical Framework

### General Formula

For most indicators (country-specific damage costs):

```
C[y, i, c, s] = Sign × D[i, c] × I[y]
```

Where:
- `C[y, i, c, s]` = Final coefficient for year y, indicator i, country c, sector s
- `Sign` = -1.0 for damage costs (7 indicators) or +1.0 for benefits (Training only)
- `D[i, c]` = Raw damage cost for indicator i in country c (from input data)
- `I[y]` = Inflation factor for year y

### Inflation Factor Calculation

```
I[y] = Deflator[USA, y] / Deflator[USA, base_year]
```

Rationale: USA deflator used globally for cross-country comparability

---

## Value Transfer Mechanism

### Overview

**Value transfer** is the process of applying economic values estimated in one geographic or economic context to another context. In the WifOR framework, value transfer is used to derive country-specific damage costs from original research studies.

**CRITICAL**: Value transfer calculations are **performed during input file creation** (pre-calculation phase), **NOT in the Python scripts**. The Python scripts only apply temporal adjustments (inflation).

### Two-Stage Valuation Process

```
Stage 1: SPATIAL TRANSFER                    Stage 2: TEMPORAL TRANSFER
(Pre-calculation - Excel/External)           (Python Scripts)
┌─────────────────────────────┐              ┌──────────────────────────┐
│ Base Study (e.g., Sweden)  │              │ Country-Specific Values  │
│ WTP = USD X                 │              │ (from input files)       │
└──────────┬──────────────────┘              └──────────┬───────────────┘
           │                                            │
      ┌────▼────┐                                  ┌────▼────┐
      │   PPP   │ Value Transfer                   │ Inflation│ Temporal
      │Adjustment│ Mechanism                        │ Factors │ Adjustment
      └────┬────┘                                  └────┬────┘
           │                                            │
┌──────────▼──────────────────┐              ┌──────────▼───────────────┐
│ 188 Country-Specific Values │   ──────>    │ Multi-Year Coefficients  │
│ (Stored in input files)     │   Loaded by  │ (Final outputs)          │
└─────────────────────────────┘   Python     └──────────────────────────┘
```

### Value Transfer Methods Used

#### 1. Purchasing Power Parity (PPP) Adjustment

**Used by**: Water Pollution (N, P), Training

**Formula**:
```
D[i, c] = D_base[i, source_country] × (PPP[c] / PPP[source_country])
```

Where:
- `D[i, c]` = Damage cost for indicator i in country c
- `D_base` = Base damage cost from source study
- `PPP[c]` = Purchasing Power Parity index for country c

**Example - Water Pollution**:
- **Source Study**: Ahlroth (2009) - Sweden
- **Base WTP Values**:
  - Freshwater Phosphorus: USD 136/kg (Sweden)
  - Marine Phosphorus: USD 68/kg (Sweden)
  - Marine Nitrogen: USD 9/kg (Sweden)
- **Transfer**: PPP-adjusted to 188 countries
- **Result**: Country-specific damage costs in `230324_WaterPollution_Mon_Coef_Final_DC.xlsx`

**Example - Training**:
- **Input**: `value_per_hour_GVA_2020USD_PPP` (column name explicitly indicates PPP)
- **Method**: Training hour values adjusted by PPP to reflect local wage levels
- **Result**: Sector × Country matrix with PPP-adjusted benefit values

#### 2. Income Elasticity Adjustment

**Used by**: Air Pollution (health impacts), potentially others

**Formula**:
```
D[i, c] = D_base[i] × (GDP_per_capita[c] / GDP_per_capita[base])^elasticity
```

Where:
- `elasticity` = Income elasticity of WTP (typically 0.8-1.2 for health)
- Higher income countries → higher WTP for health/environmental quality

**Application**: Adjusts Value of Statistical Life (VSL) and morbidity valuations across countries based on income levels.

#### 3. Global Value Transfer (Simplified)

**Used by**: OHS (Occupational Health & Safety)

**Approach**: Single global value applied to all countries without adjustment
- **Base**: USD 200,000 per DALY
- **Rationale**: Simplified approach assuming uniform health valuation
- **Trade-off**: Simplicity vs. country-specific accuracy

**Note**: This is the most conservative form of value transfer, essentially assuming no geographic variation.

### Input Files with Pre-Applied Value Transfer

| Indicator | Input File | Transfer Method | Source Study/Region |
|-----------|------------|-----------------|---------------------|
| Water Pollution | `230324_WaterPollution_Mon_Coef_Final_DC.xlsx` | PPP adjustment | Ahlroth (2009) - Sweden |
| Training | `220529_training_value_per_hour_bysector.h5` | PPP adjustment | Internal WifOR (GVA-based) |
| Air Pollution | `220707_air_pollution.xlsx` | Income elasticity | Multiple studies (VSL) |
| OHS | `220616_monetization_value_per_incident_NEW.xlsx` | Global value | USD 200k/DALY (global) |
| Waste | `220509_waste_figures.xlsx` | Regional averages | Multiple sources |
| Water Consumption | `230317_WaterConsumption_update_ZK.xlsx` | AWARE methodology | WULCA framework |
| Land Use | `230317_Landuse_update_ZK.xlsx` | LANCA/EPS | EPS 2015 + LANCA |

### Transparency Limitations

**Current State**: Value transfer calculations are embedded in Excel files with limited documentation.

**Known Gaps** (see BACKLOG.md Q8-Q10):
1. Excel formulas not extracted or documented
2. PPP indices and years used not specified
3. Income elasticity parameters not disclosed
4. Source-to-target transfer assumptions not explicit

**Improvement Priority**: HIGH - Migrating value transfer logic to Python for full transparency and reproducibility.

### Methodological Considerations

#### Advantages of Value Transfer
- **Cost-Effective**: Avoids expensive country-specific primary studies
- **Consistency**: Ensures comparable methodology across all countries
- **Feasibility**: Makes global coverage (188 countries) practical

#### Limitations of Value Transfer
- **Accuracy Trade-off**: Transferred values less accurate than primary studies
- **Context Differences**: PPP/income may not fully capture cultural/institutional differences in WTP
- **Aggregation Errors**: Regional/global averages may mask local variation
- **Assumption Dependency**: Results sensitive to elasticity parameters and PPP base year

#### Best Practices Applied
1. **Peer-Reviewed Sources**: Base studies from academic literature (Ahlroth, OECD, etc.)
2. **Economic Adjustment**: PPP or income elasticity rather than simple currency conversion
3. **Conservative Assumptions**: Where transfer validity uncertain, use lower-bound estimates
4. **Transparency Aspiration**: Document source studies and intended transfer methods

### GHG Special Formula (Year-specific, not country-specific)

```
C[y, scenario, c, s] = -1.0 × SCC[scenario, y] / 1000 × I[y]
```

Where:
- `SCC[scenario, y]` = Social Cost of Carbon for scenario and year (USD/tonne CO2e)
- Division by 1000 converts tonnes to kg
- All countries receive same value for each year-scenario combination

### Unit Construction

```
Unit[y] = {
    year_prefix + "USD/" + unit_base   if y <= last_deflator_year
    last_year + "USD/" + unit_base     if y > last_deflator_year
}
```

Examples:
- 2020: "2020USD/kg"
- 2025: "2025USD/kg"
- 2050: "2023USD/kg" (if deflator only available through 2023)

---

## Script-Specific Methodologies

### 007: Waste Management

**File**: `007_241001_prepare_Waste_my.py`

#### Methodology Overview
Monetizes damage costs from waste treatment (incineration, landfill, recovery) for hazardous and non-hazardous waste.

#### Algorithm Pseudocode
```python
# 1. Load 4 sheets from Excel (incineration/landfill × hazardous/non-hazardous)
waste_haz_inc = load_excel("Waste_hazardous_incinerated")
waste_haz_land = load_excel("Waste_hazardous_landfill")
waste_nonhaz_inc = load_excel("Waste_nonhazardous_incinerated")
waste_nonhaz_land = load_excel("Waste_nonhazardous_landfill")

# 2. Extract "costs" column (USD/kg) and rename columns
data = [
    (waste_haz_inc["costs"], "COEFFICIENT Waste_hazardous_incinerated"),
    (waste_haz_land["costs"], "COEFFICIENT Waste_hazardous_landfill"),
    (waste_nonhaz_inc["costs"], "COEFFICIENT Waste_nonhazardous_incinerated"),
    (waste_nonhaz_land["costs"], "COEFFICIENT Waste_nonhazardous_landfill")
]

# 3. Add zero-cost recovery types
data.append((zeros, "COEFFICIENT Waste_hazardous_recovered"))
data.append((zeros, "COEFFICIENT Waste_nonhazardous_recovered"))

# 4. Transpose: countries as columns, indicators as rows
raw_data = transpose(data)

# 5. Adjust country codes for compatibility
raw_data.rename(columns={"SSD": "SDS", "SDN": "SUD"})

# 6. Create coefficient matrix (Years × Indicators) × (Countries × Sectors)
coeff_matrix = create_coefficient_dataframe(years, indicators, countries, sectors)

# 7. Populate with damage costs (sign = -1.0)
populate_coefficients(coeff_matrix, raw_data, sign=-1.0)

# 8. Apply USA inflation adjustment
apply_deflation(coeff_matrix, inflation_factors)

# 9. Create units (yearUSD/kg)
units = create_units_dataframe(indicators, countries, sectors, "USD/kg")
update_units_with_years(units, years, base_year=2020)

# 10. Save to HDF5 and Excel
save_results(coeff_matrix, units, "output/Waste.h5", "output/Waste.xlsx")
```

#### Input Data Structure
- **File**: `220509_Waste figures merged_update.xlsx`
- **Sheets**: 4 (one per waste type)
- **Columns**:
  - `country_code`: ISO3 country codes
  - `costs`: Pre-calculated damage costs in USD/kg
- **Source**: OECD, IPCC, EXIOPOL, PwC

#### Damage Cost Components
1. Air emissions from incineration (health impacts)
2. GHG emissions from landfills (climate impacts)
3. Leachate contamination (water pollution)
4. Disamenity costs (local impacts)

#### Output
- **Indicators**: 6 (3 hazardous + 3 non-hazardous)
- **Units**: yearUSD/kg
- **Sign**: Negative (damage costs)
- **Spatial**: Country-specific

---

### 008: Air Pollution

**File**: `008_241001_prepare_AirPollution_my.py`

#### Methodology Overview
Monetizes health, biodiversity, crop, and material damages from 6 air pollutants.

#### Algorithm Pseudocode
```python
# 1. Load multi-indexed Excel (pollutant, country)
data = load_excel("WifOR_form", index_col=[0, 1])  # Multi-index

# 2. Extract "Value" column
damage_costs = data["Value"]

# 3. Unstack: pollutants as rows, countries as columns
raw_data = damage_costs.unstack(level=1)

# 4. Standardize indicator names
raw_data.index = "COEFFICIENT AirEmission_" + raw_data.index + ", in USD (WifOR)"

# 5. Create coefficient matrix
coeff_matrix = create_coefficient_dataframe(years, pollutants, countries, sectors)

# 6. Populate with damage costs (sign = -1.0)
populate_coefficients(coeff_matrix, raw_data, sign=-1.0)

# 7. Apply USA inflation
apply_deflation(coeff_matrix, inflation_factors)

# 8. Create units (yearUSD/kg)
units = create_units_dataframe(pollutants, countries, sectors, "USD/kg")
update_units_with_years(units, years, base_year=2020)

# 9. Save results
save_results(coeff_matrix, units, "output/AirPollution.h5", "output/AirPollution.xlsx")
```

#### Input Data Structure
- **File**: `220707_Air pollution_update.xlsx`
- **Sheet**: `WifOR_form`
- **Index**: Multi-level (pollutant, country_code)
- **Column**: `Value` (damage cost in USD/kg)
- **Source**: German Federal Environment Agency (UBA), NEEDS EU project

#### Damage Cost Components
1. **Health**: Respiratory and cardiovascular diseases (PM2.5, PM10)
2. **Biodiversity**: Ecosystem damage from acidification (NOx, SOx)
3. **Crops**: Agricultural yield losses
4. **Materials**: Corrosion and building damage

#### Pollutants
- PM2.5: Fine particulate matter
- PM10: Coarse particulate matter
- NOx: Nitrogen oxides
- SOx: Sulfur oxides
- NMVOC: Non-methane volatile organic compounds
- NH3: Ammonia

#### Output
- **Indicators**: 6 pollutants
- **Units**: yearUSD/kg
- **Sign**: Negative
- **Spatial**: Country-specific

---

### 009: Water Consumption

**File**: `009_241001_prepare_WaterConsumption_my.py`

#### Methodology Overview
Values freshwater (blue water) depletion using economic damages (agricultural loss) and health damages (DALYs).

#### Algorithm Pseudocode
```python
# 1. Load Excel sheet
data = load_excel("Ergebnisse_final")

# 2. Extract "Total damages" column (USD/m³)
damages = data["Total damages"]

# 3. Create single indicator
damages.name = "COEFFICIENT Water Consumption Blue, in USD (WifOR)"

# 4. Transpose to get countries as columns
raw_data = damages.to_frame().T

# 5. Create coefficient matrix
coeff_matrix = create_coefficient_dataframe(years, [indicator], countries, sectors)

# 6. Populate (sign = -1.0)
populate_coefficients(coeff_matrix, raw_data, sign=-1.0)

# 7. Apply USA inflation
apply_deflation(coeff_matrix, inflation_factors)

# 8. Create units (yearUSD/m3)
units = create_units_dataframe([indicator], countries, sectors, "USD/m3")
update_units_with_years(units, years, base_year=2020)

# 9. Save results
save_results(coeff_matrix, units, "output/WaterConsumption.h5", "output/WaterConsumption.xlsx")
```

#### Input Data Structure
- **File**: `220511_Water consumption_update.xlsx`
- **Sheet**: `Ergebnisse_final`
- **Columns**:
  - `country_code`: ISO3
  - `Total damages`: Sum of economic + health damages (USD/m³)
- **Source**: Academic research (Ligthart & van Harmelen 2019, Debarre et al. 2022)

#### Damage Cost Components
1. **Economic Damages**: Agricultural output loss from water scarcity
   - Shadow pricing based on marginal productivity
2. **Health Damages**: DALYs from reduced water availability
   - Waterborne diseases, malnutrition
3. **AWARE Factors**: Country-specific water scarcity adjustments

#### Output
- **Indicators**: 1 (blue water consumption)
- **Units**: yearUSD/m3
- **Sign**: Negative
- **Spatial**: Country-specific
- **Maturity**: Experimental (high uncertainty)

---

### 010: Land Use

**File**: `010_241001_prepare_LandUse_my.py`

#### Methodology Overview
Monetizes ecosystem service loss from land conversion using Environmental Priority Strategies (EPS) system.

#### Algorithm Pseudocode
```python
# 1. Load Excel with land use types as columns
data = load_excel("Ergebnisse_final")

# 2. Drop metadata columns
data = data.drop(columns=["country_name", "unit", "ISO2", ...])

# 3. Transpose: land types as rows, countries as columns
raw_data = data.T

# 4. Add "COEFFICIENT Landuse_" prefix
raw_data.index = "COEFFICIENT Landuse_" + raw_data.index

# 5. Create coefficient matrix
coeff_matrix = create_coefficient_dataframe(years, land_types, countries, sectors)

# 6. Populate (sign = -1.0)
populate_coefficients(coeff_matrix, raw_data, sign=-1.0)

# 7. Apply USA inflation
apply_deflation(coeff_matrix, inflation_factors)

# 8. Create units (yearUSD/ha)
units = create_units_dataframe(land_types, countries, sectors, "USD/ha")
update_units_with_years(units, years, base_year=2020)

# 9. Save results
save_results(coeff_matrix, units, "output/LandUse.h5", "output/LandUse.xlsx")
```

#### Input Data Structure
- **File**: `230317_Landuse_update_ZK.xlsx`
- **Sheet**: `Ergebnisse_final`
- **Columns**: Each column = one land use type (Forestry, Agriculture, Urban, etc.)
- **Rows**: Countries
- **Source**: EPS system (Steen 1999, 2015), LANCA characterization factors

#### Damage Cost Components (EPS Framework)
1. **Working Capacity**: Heat island effects on labor productivity
2. **Water Treatment**: Loss of natural filtration services
3. **Crop Growth**: Soil quality and pollination services
4. **Biodiversity**: Species habitat loss
5. **Recreation**: Aesthetic and cultural values

#### Output
- **Indicators**: Multiple land use types
- **Units**: yearUSD/ha
- **Sign**: Negative
- **Spatial**: Country-specific

---

### 013: Water Pollution

**File**: `013_241014_prepare_WaterPol_my.py`

#### Methodology Overview
Quantifies damage costs from water pollutants (nutrients and heavy metals) using Steen (2020) and USEtox models.

#### Algorithm Pseudocode
```python
# 1. Load multi-indexed Excel
data = load_excel("Results", index_col=[0, 1])

# 2. Extract "Value" column
damage_costs = data["Value"]

# 3. Unstack: pollutants as rows, countries as columns
raw_data = damage_costs.unstack(level=1)

# 4. Add "COEFFICIENT " prefix
raw_data.index = "COEFFICIENT " + raw_data.index

# 5. Create coefficient matrix
coeff_matrix = create_coefficient_dataframe(years, pollutants, countries, sectors)

# 6. Populate (sign = -1.0)
populate_coefficients(coeff_matrix, raw_data, sign=-1.0)

# 7. Apply USA inflation
apply_deflation(coeff_matrix, inflation_factors)

# 8. Create units (yearUSD/kg)
units = create_units_dataframe(pollutants, countries, sectors, "USD/kg")
update_units_with_years(units, years, base_year=2020)

# 9. Save results
save_results(coeff_matrix, units, "output/WaterPollution.h5", "output/WaterPollution.xlsx")
```

#### Input Data Structure
- **File**: `230324_WaterPollution_Mon_Coef_Final_DC.xlsx`
- **Sheet**: `Results`
- **Index**: Multi-level (pollutant, country_code)
- **Column**: `Value` (damage cost in USD/kg)
- **Source**: Internally generated (WifOR methodology)

#### Damage Cost Components
1. **Nutrients (N, P)**: Eutrophication damage using Steen (2020)
   - Fish production reduction
   - Biodiversity loss in freshwater ecosystems
2. **Heavy Metals**: Human health impacts using USEtox model
   - Arsenic, Cadmium, Mercury, Chromium, Lead, Nickel, Copper, Zinc, Antimony
   - Toxicity to aquatic life and drinking water contamination

#### Pollutants (11 total)
- Nitrogen (N)
- Phosphorus (P)
- As, Cd, Hg, Cr, Pb, Ni, Cu, Zn, Sb (heavy metals)

#### Output
- **Indicators**: 11 pollutants
- **Units**: yearUSD/kg
- **Sign**: Negative
- **Spatial**: Country-specific
- **Maturity**: Experimental

---

### 014: Training (UNIQUE - Positive Benefit)

**File**: `014_241016_prepare_Training_my.py`

#### Methodology Overview
**ONLY POSITIVE COEFFICIENT** - Values training as human capital investment using returns to schooling research.

#### Algorithm Pseudocode
```python
# 1. Load HDF5 file
data = load_hdf5("value_per_hour")

# 2. Extract sector × country value column
training_values = data["value_per_hour_GVA_2020USD_PPP"]

# 3. Transpose to single row
raw_data = training_values.to_frame().T

# 4. Rename indicator
raw_data.index = ["COEFFICIENT TrainingHours, in USD (WifOR)"]

# 5. Create coefficient matrix
coeff_matrix = create_coefficient_dataframe(years, [indicator], countries, sectors)

# 6. Populate with POSITIVE sign (+1.0) ← KEY DIFFERENCE
populate_coefficients(coeff_matrix, raw_data, sign=+1.0)

# 7. Apply USA inflation
apply_deflation(coeff_matrix, inflation_factors)

# 8. Create units (yearUSD/h)
units = create_units_dataframe([indicator], countries, sectors, "USD/h")
update_units_with_years(units, years, base_year=2020)

# 9. Save results
save_results(coeff_matrix, units, "output/Training.h5", "output/Training.xlsx")
```

#### Input Data Structure
- **File**: `220529_training_value_per_hour_bysector.h5`
- **Key**: `value_per_hour`
- **Structure**: Sector × Country matrix
- **Column**: `value_per_hour_GVA_2020USD_PPP` (value in USD/hour)
- **Source**: Internally generated

#### Valuation Methodology
1. **Returns to Schooling**: Based on Psacharopoulos & Patrinos (2018)
   - Estimated productivity increase: ~8-10% per year of schooling
2. **Training Equivalence**: Extrapolate schooling returns to training hours
   - Assumption: Training has proportional productivity impact
3. **Lifetime Value**: Calculate present value of productivity gains over working life
4. **Sector Adjustment**: Different returns by economic sector (knowledge-intensive vs. labor-intensive)

#### Calculation Logic (External to Python Script)
```
Training_Value[sector, country] =
    Hourly_Wage[sector, country]
    × Return_Rate[sector]
    × Remaining_Working_Years
    × Discount_Factor
```

#### Output
- **Indicators**: 1 (training hours)
- **Units**: yearUSD/h
- **Sign**: **POSITIVE** (benefit, not damage)
- **Spatial**: Country-specific AND sector-specific
- **Maturity**: Average

---

### 015: Occupational Health & Safety

**File**: `015_241016_prepare_OHS_my.py`

#### Methodology Overview
Monetizes workplace injuries and illnesses using Value of Statistical Life (VSL) and Disability-Adjusted Life Years (DALYs).

#### Algorithm Pseudocode
```python
# 1. Load two sheets
fatal = load_excel("Fatality")
nonfatal = load_excel("Nonfatal")

# 2. Extract cost columns
fatal_cost = fatal["USD/Fatality"]
injury_cost = nonfatal["USD/Injury"]
illness_cost = nonfatal["USD/Illness"]

# 3. Create 4 indicators
indicators = {
    "COEFFICIENT Injury_nonfatal": injury_cost,
    "COEFFICIENT Disease_Illness_nonfatal": illness_cost,
    "COEFFICIENT Injury_fatality": fatal_cost,
    "COEFFICIENT Disease_Illness_fatality": fatal_cost  # Same value
}

# 4. Transpose
raw_data = DataFrame(indicators).T

# 5. Create coefficient matrix
coeff_matrix = create_coefficient_dataframe(years, indicators, countries, sectors)

# 6. Populate (sign = -1.0)
populate_coefficients(coeff_matrix, raw_data, sign=-1.0)

# 7. Apply USA inflation
apply_deflation(coeff_matrix, inflation_factors)

# 8. Create units (yearUSD/case)
units = create_units_dataframe(indicators, countries, sectors, "USD/case")
update_units_with_years(units, years, base_year=2020)

# 9. Save results
save_results(coeff_matrix, units, "output/OHS.h5", "output/OHS.xlsx")
```

#### Input Data Structure
- **File**: `220616_monetization_value_per_incident_NEW.xlsx`
- **Sheets**:
  - `Fatality`: One column (`USD/Fatality`)
  - `Nonfatal`: Two columns (`USD/Injury`, `USD/Illness`)
- **Rows**: Countries
- **Source**: Internally generated

#### Valuation Methodology
1. **Value of Statistical Life (VSL)**: ~$200,000 per DALY
   - Based on global VSL estimates from health economics literature
2. **Fatal Incidents**: Years of life lost (YLL)
   - Calculated from age at death and life expectancy
3. **Non-fatal Incidents**: Years lived with disability (YLD)
   - Severity weights from Global Burden of Disease study
   - Injury: Temporary disability
   - Illness: Chronic/occupational diseases

#### DALY Calculation
```
DALY = YLL + YLD

YLL[fatal] = (Life_Expectancy - Age_at_Death) × Discount_Factor
YLD[nonfatal] = Duration × Disability_Weight × Discount_Factor

Monetized_Value = DALY × VSL
```

#### Output
- **Indicators**: 4 (2 × 2: injury/illness × fatal/nonfatal)
- **Units**: yearUSD/case
- **Sign**: Negative
- **Spatial**: Country-specific
- **Maturity**: Well Established

---

### 020: Greenhouse Gas Emissions (UNIQUE - Year-Specific)

**File**: `020_241024_prepare_GHG_my.py`

#### Methodology Overview
**YEAR-SPECIFIC, NOT COUNTRY-SPECIFIC** - Uses Social Cost of Carbon from Nordhaus DICE model with multiple scenarios.

#### Algorithm Pseudocode
```python
# 1. Load HDF5 with [year, scenario] multi-index
data = load_hdf5("df")

# 2. Unstack years: scenarios as rows, years as columns
raw_data = data.unstack(level=0)

# 3. Add "COEFFICIENT GHG_" prefix
raw_data.index = "COEFFICIENT GHG_" + raw_data.index

# 4. Convert from USD/tonne to USD/kg (divide by 1000)
raw_data = raw_data / 1000

# 5. Create coefficient matrix
coeff_matrix = create_coefficient_dataframe(years, scenarios, countries, sectors)

# 6. Populate with YEAR-SPECIFIC values (sign = -1.0)
#    All countries get same value for each [year, scenario] combination
for year in years:
    for scenario in scenarios:
        value = raw_data.loc[scenario, year]
        coeff_matrix.loc[(year, scenario), :] = -1.0 * value

# 7. Apply USA inflation (base year 2019, different from others)
apply_deflation(coeff_matrix, inflation_factors, base_year=2019)

# 8. Create units (yearUSD/kg)
units = create_units_dataframe(scenarios, countries, sectors, "USD/kg")
update_units_with_years(units, years, base_year=2019)

# 9. Save results
save_results(coeff_matrix, units, "output/GHG.h5", "output/GHG.xlsx")
```

#### Input Data Structure
- **File**: `20241022_scc_nordhaus.h5`
- **Key**: `df`
- **Index**: Multi-level (year, scenario)
- **Values**: Social Cost of Carbon (USD/tonne CO2e)
- **Source**: Nordhaus DICE model (Nobel laureate)

#### Social Cost of Carbon (SCC) Methodology
1. **Integrated Assessment Model**: DICE (Dynamic Integrated Climate-Economy)
   - Links climate science with economic growth
   - Projects damages from temperature increases
2. **Damage Function**: Economic harm from climate change
   - Agricultural losses, sea level rise, health impacts, ecosystem damages
3. **Discounting**: Future damages discounted to present value
   - Different scenarios use different discount rates (1.5%, 2.5%, 5%)
4. **Climate Sensitivity**: Temperature response to CO2 doubling
   - Multiple scenarios (low, medium, high sensitivity)

#### Scenarios (Examples)
- Base case (3% discount, medium sensitivity)
- Low discount (1.5% - higher SCC, values future more)
- High discount (5% - lower SCC, values future less)
- High climate sensitivity (larger temperature response)
- Low climate sensitivity (smaller temperature response)

#### Key Differences from Other Scripts
1. **Global values**: All countries get same coefficient for each year
   - Rationale: Climate change is a global phenomenon
2. **Base year 2019**: Different from others (2020)
   - Aligns with DICE model reference year
3. **Unit conversion**: Tonnes to kg (÷1000)
4. **Most recent data**: 2024-10-22 (others from 2022-2023)

#### Output
- **Indicators**: Multiple scenarios
- **Units**: yearUSD/kg
- **Sign**: Negative
- **Spatial**: Global (year-specific, not country-specific)
- **Maturity**: Well Established (but high sensitivity to assumptions)

---

## Data Processing Pipeline

### Step-by-Step Flow

#### 1. Configuration Loading
```python
config = get_indicator_config('air_pollution')
input_file = config['input_file']
output_dir = config['output_dir']
base_year = config.get('base_year', 2020)
years = range(2014, 2031) + [2050, 2100]
```

#### 2. Data Loading
```python
# Load shared data (all scripts)
countries, nace_sectors, deflators_df = load_common_data(
    model_def_path="input_data/Model_definitions_owntable.h5",
    deflator_path="input_data/241001_worldbank_deflator.h5"
)

# Load indicator-specific data (varies by script)
if file_extension == '.xlsx':
    raw_data = pd.read_excel(input_file, sheet_name=sheet_name)
elif file_extension == '.h5':
    raw_data = pd.read_hdf(input_file, key=hdf_key)
```

#### 3. Data Preprocessing
```python
# Clean and reshape data
raw_data = raw_data.dropna()
raw_data = raw_data.set_index('country_code')
raw_data = raw_data.transpose()  # Indicators as rows, countries as columns

# Standardize indicator names
raw_data.index = "COEFFICIENT " + raw_data.index + ", in USD (WifOR)"

# Handle country code mismatches
raw_data = raw_data.rename(columns=country_mapping)
```

#### 4. Coefficient Matrix Creation
```python
# Create empty multi-indexed DataFrame
coeff_df = create_coefficient_dataframe(
    years=years,
    indicators=indicator_list,
    countries=countries,
    nace_sectors=nace_sectors
)
# Structure: (Year × Indicator) × (Country × Sector)
# Initial values: 0.0
```

#### 5. Coefficient Population
```python
# Fill matrix with raw data
for indicator in indicator_list:
    for country in countries:
        value = raw_data.loc[indicator, country]

        # Apply to all years and sectors
        for year in years:
            for sector in nace_sectors:
                coeff_df.loc[(year, indicator), (country, sector)] = (
                    coefficient_sign * value
                )
```

Where:
- `coefficient_sign = -1.0` for 7 scripts (damages)
- `coefficient_sign = +1.0` for Training (benefit)

#### 6. Inflation Adjustment
```python
# Calculate inflation factors (USA deflator)
inflation_factors = calculate_inflation_factors(
    deflators_df=deflators_df,
    years=years,
    base_year=base_year,
    reference_country='USA'
)

# inflation_factors[year] = deflator[USA, year] / deflator[USA, base_year]

# Apply to coefficients
for year in years:
    factor = inflation_factors[year]
    coeff_df.loc[year, :] *= factor
```

#### 7. Unit Creation
```python
# Determine last available deflator year
last_deflator_year = deflators_df.index.max()

# Create unit strings
units_df = create_units_dataframe(
    indicators=indicator_list,
    countries=countries,
    nace_sectors=nace_sectors,
    base_unit=base_unit  # e.g., "USD/kg"
)

# Add year prefixes
update_units_with_years(
    units_df=units_df,
    years=years,
    base_year=base_year,
    last_deflator_year=last_deflator_year,
    base_unit=base_unit
)

# Result: "2020USD/kg", "2025USD/kg", "2023USD/kg" (for 2050)
```

#### 8. Output Export
```python
# Save to HDF5 (efficient, structured)
save_results(
    coeff_df=coeff_df,
    units_df=units_df,
    output_path_h5=f"output/{date}_coefficients_{indicator}.h5",
    output_path_excel=f"output/{date}_coefficients_{indicator}.xlsx",
    hdf_key='coefficients'
)

# HDF5 keys: 'coefficients', 'units'
# Excel sheets: 'Coefficients', 'Units'
```

---

## Quality Assurance

### Built-in Validation Checks

#### 1. Data Completeness
- All 188 countries present in output
- All NACE sectors covered
- All years in range [2014-2030, 2050, 2100]

#### 2. Sign Consistency
- Training: All positive coefficients
- All others: All negative coefficients

#### 3. Temporal Consistency
- Smooth inflation adjustment (no sudden jumps)
- Coefficients scale reasonably across years

#### 4. Spatial Consistency
- GHG: Identical values across countries for each year
- Others: Country-specific values present

#### 5. Unit Consistency
- Units match indicator type (kg, m3, ha, h, case)
- Year prefixes match coefficient years

### Recommended Manual Checks

#### Before Execution
1. Verify input files exist and are readable
2. Check config.yaml settings
3. Ensure output directory exists

#### After Execution
1. Review log files for errors/warnings
2. Spot-check coefficient values for reasonableness
3. Compare to previous outputs for consistency
4. Validate units match expectations

### Known Limitations

#### Methodological
1. **USA Inflation**: Applies USA deflator globally
   - May not reflect local purchasing power
   - Chosen for cross-country comparability

2. **Constant Coefficients**: No temporal variation in base damage costs
   - Assumes damage functions don't change over time
   - Only inflation adjustment applied

3. **Sector Uniformity**: Most indicators apply same value to all sectors
   - Exception: Training has sector differentiation
   - May not reflect sector-specific risks

#### Data Quality
1. **Vintage Inconsistency**: Input files from 2022-2024
   - Some indicators based on older research
   - Refresh schedule unclear

2. **Experimental Indicators**: Water Consumption & Pollution
   - High uncertainty acknowledged
   - Results "hard to explain" per README

3. **Excel Pre-calculations**: 6 indicators use pre-calculated values
   - Formulas not in version control
   - Harder to audit and reproduce

---

## References

### Academic Literature
- Psacharopoulos, G., & Patrinos, H. A. (2018). Returns to investment in education: a decennial review of the global literature. *Education Economics*.
- Steen, B. (1999). A systematic approach to environmental priority strategies in product development (EPS). *Journal of Cleaner Production*.
- Ligthart, T., & van Harmelen, T. (2019). Water footprint and environmental impacts of freshwater consumption.
- Nordhaus, W. (2017). Revisiting the social cost of carbon. *PNAS*.

### Data Sources
- OECD Data Explorer: https://data.oecd.org
- World Bank: https://data.worldbank.org
- German Federal Environment Agency (UBA): https://www.umweltbundesamt.de
- Global Burden of Disease Study: https://www.healthdata.org/gbd

### Methodology References
- WifOR Institute: https://www.wifor.com
- DICE Model: https://williamnordhaus.com/dicerice-models

---

**Document Version**: 1.0
**Last Updated**: 2026-01-02
**Maintained by**: WifOR Development Team
**Contact**: dimitrij.euler@greenings.org
