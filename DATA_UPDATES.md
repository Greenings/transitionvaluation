# Data Update Procedures

**WifOR Value Factors - Data Maintenance Guide**
**Organization**: Transition Valuation Partnership under Greenings custodianship
**Version**: 1.0
**Last Updated**: 2026-01-02

This document describes procedures for updating input data files and regenerating value factor coefficients.

---

## Table of Contents

1. [Overview](#overview)
2. [Input Data Inventory](#input-data-inventory)
3. [Update Procedures](#update-procedures)
4. [Validation Steps](#validation-steps)
5. [Troubleshooting](#troubleshooting)
6. [Data Versioning](#data-versioning)

---

## Overview

### Data Update Lifecycle

```
┌─────────────────────┐
│ 1. Check for Updates│  Monitor data sources for new versions
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 2. Download New Data│  Obtain updated files
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 3. Validate Schema  │  Ensure structure compatibility
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 4. Backup Old Data  │  Archive current versions
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 5. Replace Files    │  Update input_data/ directory
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 6. Regenerate       │  Run affected scripts
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 7. Validate Output  │  Compare and verify results
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ 8. Document Changes │  Update CHANGELOG.md
└─────────────────────┘
```

### Update Frequency Recommendations

| Data File | Current Vintage | Recommended Refresh | Rationale |
|-----------|----------------|---------------------|-----------|
| **Shared Data** | | | |
| Model definitions | Static | Annual | Country/sector lists rarely change |
| World Bank deflators | 2024-10-01 | Quarterly | New GDP data published regularly |
| **Indicator-Specific** | | | |
| Waste figures | 2022-05-09 | Biannual | OECD updates semi-regularly |
| Air pollution | 2022-07-07 | Biannual | UBA methodology stable |
| Water consumption | 2022-05-11 | Annual | Academic research evolves |
| Land use | 2023-03-17 | Annual | EPS factors update periodically |
| Water pollution | 2023-03-24 | Annual | Internal methodology refinement |
| Training values | 2022-05-29 | Biannual | Returns to education research updates |
| OHS monetization | 2022-06-16 | Annual | VSL estimates evolve |
| GHG SCC Nordhaus | 2024-10-22 | Annual | DICE model updates regularly |

---

## Output File Naming and Structure Standards

To enhance **comparability** and **usability** across time periods and indicators:

### Naming Convention
```
YYYYMMDD_coefficients_IndicatorName.{xlsx,h5}

Examples:
- 2024-10-01_coefficients_Waste.xlsx
- 2024-10-01_coefficients_AirPollution.h5
- 2024-10-16_coefficients_Training.xlsx
```

**Components**:
- **YYYYMMDD**: Date of coefficient base data (NOT generation date)
- **coefficients**: Fixed term indicating value factor outputs
- **IndicatorName**: CamelCase, no spaces (e.g., WaterPollution, not Water_Pollution)
- **Extension**: .xlsx for human-readable, .h5 for programmatic use

### Excel File Structure Standards

All Excel outputs MUST follow this structure for consistency:

**Sheet 1: "Coefficients"**
- Multi-indexed DataFrame: (Year × Indicator) × (Country × Sector)
- Headers: Row 0 = Year, Row 1 = Indicator | Col 0 = Country, Col 1 = Sector
- Values: Numeric coefficients (float64)
- Missing values: NaN (not 0, not blank)

**Sheet 2: "Units"**
- Same structure as Coefficients
- Values: String format "{year}USD/{base_unit}"
- Examples: "2020USD/kg", "2025USD/m3", "2020USD/h"

**Sheet 3: "Metadata" (RECOMMENDED - not yet implemented)**
- Key-value pairs:
  - base_year: 2020
  - deflator_country: USA
  - value_transfer_method: PPP_adjustment | income_elasticity | global_value
  - source_study: Ahlroth (2009) [for Water Pollution]
  - last_updated: 2024-10-14
  - script_version: v1.2.3

### HDF5 File Structure Standards

```
/coefficients    Dataset (Year × Indicator) × (Country × Sector)
/units           Dataset (Year × Indicator) × (Country × Sector)
/metadata        Group
  /metadata/base_year          Attribute
  /metadata/deflator_country   Attribute
  /metadata/value_transfer     Attribute
  /metadata/source_study       Attribute
```

### Abbreviations and Terminology

**Consistent usage across all documentation**:
| Term | Usage | Do NOT Use |
|------|-------|------------|
| Value factor | Preferred | "impact factor", "coefficient" (except in technical context) |
| Coefficient | Technical term for numeric value | "factor", "value" |
| Indicator | Type of impact (e.g., GHG, OHS) | "metric", "KPI" |
| Damage cost | For negative impacts | "damage", "cost" (alone) |
| Benefit | For Training only | "positive impact", "value added" |
| PPP | Always spell out on first use: "Purchasing Power Parity (PPP)" | |
| VSL | Always spell out: "Value of Statistical Life (VSL)" | |

---

## Input Data Inventory

### Shared Dependencies (Used by ALL Scripts)

#### 1. Model Definitions
- **File**: `input_data/Model_definitions_owntable.h5`
- **Current Version**: Static (no date)
- **Contents**: 188 countries (ISO3) + NACE sectors
- **Update Source**: Internal WifOR database
- **Schema**:
  ```python
  pd.read_hdf('Model_definitions_owntable.h5', key='owntable')
  # Columns: country_code (ISO3), sector_code (NACE), ...
  ```

**Update Procedure**:
1. Export latest country/sector list from WifOR database
2. Validate 188 countries present (check for new countries or code changes)
3. Validate NACE sector completeness
4. Save as HDF5 with key 'owntable'
5. Regenerate ALL 8 scripts

**Critical Check**: Country code consistency
- Known mappings: SSD→SDS, SDN→SUD
- Verify no new mismatches introduced

---

#### 2. World Bank GDP Deflators
- **File**: `input_data/241001_worldbank_deflator.h5`
- **Current Version**: 2024-10-01
- **Contents**: GDP deflators by country and year
- **Update Source**: https://data.worldbank.org (Indicator: NY.GDP.DEFL.ZS)
- **Schema**:
  ```python
  pd.read_hdf('241001_worldbank_deflator.h5', key='deflator')
  # Index: year
  # Columns: country_code (ISO3)
  # Values: GDP deflator (base year = 100)
  ```

**Update Procedure**:
1. Download latest World Bank GDP deflator data:
   ```bash
   # Using wbdata Python library
   import wbdata
   deflators = wbdata.get_dataframe({"NY.GDP.DEFL.ZS": "deflator"}, convert_date=True)
   ```
2. Reshape to year × country matrix
3. Validate all 188 countries present (fill missing with interpolation or regional average)
4. Save as HDF5 with key 'deflator'
5. Update filename with current date (YYMMDD format)
6. Update config.yaml with new filename
7. Regenerate ALL 8 scripts

**Critical Check**: USA deflator must be present (used for global adjustment)

---

### Indicator-Specific Data

#### 3. Waste Figures
- **File**: `input_data/220509_Waste figures merged_update.xlsx`
- **Current Version**: 2022-05-09
- **Affected Script**: `007_241001_prepare_Waste_my.py`
- **Update Source**: OECD, IPCC, internal WifOR calculations
- **Schema**:
  ```
  Sheets: Waste_hazardous_incinerated, Waste_hazardous_landfill,
          Waste_nonhazardous_incinerated, Waste_nonhazardous_landfill
  Columns: country_code, costs (USD/kg)
  ```

**Update Procedure**:
1. **External Data**:
   - OECD waste statistics: https://stats.oecd.org
   - IPCC emission factors: https://www.ipcc-nggip.iges.or.jp
2. **Internal Calculation** (if formulas available):
   - Recalculate damage costs using updated emission factors
   - Apply latest health impact valuations
3. **File Update**:
   - Maintain sheet names (script expects exact names)
   - Ensure "costs" column present in each sheet
   - Validate all countries covered
4. **Save**: Update filename with new date (YYMMDD_Waste...)
5. **Config**: Update config.yaml → waste → input_file
6. **Regenerate**: Run `python 007_241001_prepare_Waste_my.py`

**Critical Check**: "costs" column must be in USD/kg (not EUR or other currency)

---

#### 4. Air Pollution
- **File**: `input_data/220707_Air pollution_update.xlsx`
- **Current Version**: 2022-07-07
- **Affected Script**: `008_241001_prepare_AirPollution_my.py`
- **Update Source**: German Federal Environment Agency (UBA)
- **Schema**:
  ```
  Sheet: WifOR_form
  Index: Multi-level (pollutant, country_code)
  Column: Value (USD/kg)
  ```

**Update Procedure**:
1. **External Data**:
   - UBA methodology: https://www.umweltbundesamt.de/en/topics/economics-consumption/economic-evaluation-of-environmental-damages/methodological-convention-30-to-assess-environmental-costs
   - Check for updated damage cost estimates
2. **File Update**:
   - Maintain multi-index structure
   - All 6 pollutants: PM2.5, PM10, NOx, SOx, NMVOC, NH3
   - Validate "Value" column present
3. **Save**: Update filename with new date
4. **Config**: Update config.yaml → air_pollution → input_file
5. **Regenerate**: Run `python 008_241001_prepare_AirPollution_my.py`

**Critical Check**: Pollutant names must match exactly (case-sensitive)

---

#### 5. Water Consumption
- **File**: `input_data/220511_Water consumption_update.xlsx`
- **Current Version**: 2022-05-11
- **Affected Script**: `009_241001_prepare_WaterConsumption_my.py`
- **Update Source**: Academic research, AWARE factors
- **Schema**:
  ```
  Sheet: Ergebnisse_final
  Columns: country_code, Total damages (USD/m³)
  ```

**Update Procedure**:
1. **External Data**:
   - AWARE factors: https://www.wulca-waterlca.org/aware.html
   - Academic updates (check citations in METHODOLOGY.md)
2. **Internal Calculation** (if methodology available):
   - Recalculate economic + health damages
   - Apply updated AWARE scarcity factors
3. **File Update**:
   - Sheet name: "Ergebnisse_final"
   - Column: "Total damages" (USD/m³)
4. **Save**: Update filename with new date
5. **Config**: Update config.yaml → water_consumption → input_file
6. **Regenerate**: Run `python 009_241001_prepare_WaterConsumption_my.py`

**Critical Check**: Units must be USD/m³ (cubic meters, not liters)

**Note**: Maturity status is "Experimental" - consider methodology improvements (see BACKLOG.md Q1)

---

#### 6. Land Use
- **File**: `input_data/230317_Landuse_update_ZK.xlsx`
- **Current Version**: 2023-03-17
- **Affected Script**: `010_241001_prepare_LandUse_my.py`
- **Update Source**: EPS system, LANCA characterization factors
- **Schema**:
  ```
  Sheet: Ergebnisse_final
  Columns: country_code, [land_type_1], [land_type_2], ..., [land_type_n]
  Each land type column contains damage costs (USD/ha)
  ```

**Update Procedure**:
1. **External Data**:
   - EPS 2015 update: Check for newer version
   - LANCA factors: https://lanca.ethz.ch
2. **Internal Calculation** (if methodology available):
   - Recalculate ecosystem service losses
   - Apply updated characterization factors
3. **File Update**:
   - Maintain land type column names
   - Drop metadata columns before processing (script handles this)
4. **Save**: Update filename with new date
5. **Config**: Update config.yaml → land_use → input_file
6. **Regenerate**: Run `python 010_241001_prepare_LandUse_my.py`

**Critical Check**: Units must be USD/ha (hectares)

---

#### 7. Water Pollution
- **File**: `input_data/230324_WaterPollution_Mon_Coef_Final_DC.xlsx`
- **Current Version**: 2023-03-24
- **Affected Script**: `013_241014_prepare_WaterPol_my.py`
- **Update Source**: Internal WifOR methodology (Steen 2020, USEtox)
- **Schema**:
  ```
  Sheet: Results
  Index: Multi-level (pollutant, country_code)
  Column: Value (USD/kg)
  ```

**Update Procedure**:
1. **Methodology Updates**:
   - Check for Steen methodology updates (N, P)
   - Check USEtox model updates (heavy metals)
2. **Internal Recalculation**:
   - Contact WifOR methodology team for updated calculations
   - Requires access to internal calculation scripts
3. **File Update**:
   - Maintain multi-index structure
   - All 11 pollutants: N, P, As, Cd, Hg, Cr, Pb, Ni, Cu, Zn, Sb
   - "Value" column (USD/kg)
4. **Save**: Update filename with new date
5. **Config**: Update config.yaml → water_pollution → input_file
6. **Regenerate**: Run `python 013_241014_prepare_WaterPol_my.py`

**Critical Check**: All 11 pollutants present

**Note**: Maturity status is "Experimental" - methodology improvements needed (see BACKLOG.md Q1)

---

#### 8. Training Values
- **File**: `input_data/220529_training_value_per_hour_bysector.h5`
- **Current Version**: 2022-05-29
- **Affected Script**: `014_241016_prepare_Training_my.py`
- **Update Source**: Internal WifOR calculations (returns to education research)
- **Schema**:
  ```python
  pd.read_hdf('220529_training_value_per_hour_bysector.h5', key='value_per_hour')
  # Index: sector_code (NACE)
  # Columns: country_code
  # Specific column used: "value_per_hour_GVA_2020USD_PPP"
  ```

**Update Procedure**:
1. **Literature Review**:
   - Check for updated returns to education research
   - Psacharopoulos & Patrinos updates
   - Country-specific studies
2. **Internal Recalculation**:
   - Contact WifOR methodology team
   - Requires internal calculation scripts
   - Recalculate using updated wage data and return rates
3. **File Update**:
   - Maintain HDF5 structure with key 'value_per_hour'
   - Column: "value_per_hour_GVA_2020USD_PPP"
   - Sector × Country matrix
4. **Save**: Update filename with new date
5. **Config**: Update config.yaml → training → input_file
6. **Regenerate**: Run `python 014_241016_prepare_Training_my.py`

**Critical Check**: This is the ONLY positive coefficient indicator - verify sign after update

---

#### 9. OHS Monetization
- **File**: `input_data/220616_monetization_value_per_incident_NEW.xlsx`
- **Current Version**: 2022-06-16
- **Affected Script**: `015_241016_prepare_OHS_my.py`
- **Update Source**: Internal WifOR calculations (VSL, DALY weights)
- **Schema**:
  ```
  Sheet: Fatality
  Columns: country_code, USD/Fatality

  Sheet: Nonfatal
  Columns: country_code, USD/Injury, USD/Illness
  ```

**Update Procedure**:
1. **VSL Updates**:
   - Check for updated Value of Statistical Life estimates
   - Current baseline: ~$200,000 per DALY
   - May vary by country income level
2. **DALY Weights**:
   - Global Burden of Disease study updates: https://www.healthdata.org/gbd
   - Updated disability weights for injuries/illnesses
3. **Internal Recalculation**:
   - Contact WifOR methodology team
   - Update VSL by country
   - Recalculate fatal/nonfatal valuations
4. **File Update**:
   - Two sheets: "Fatality", "Nonfatal"
   - Maintain column names exactly
5. **Save**: Update filename with new date
6. **Config**: Update config.yaml → ohs → input_file
7. **Regenerate**: Run `python 015_241016_prepare_OHS_my.py`

**Critical Check**: USD/case units, all negative coefficients

---

#### 10. GHG Social Cost of Carbon
- **File**: `input_data/20241022_scc_nordhaus.h5`
- **Current Version**: 2024-10-22 (MOST RECENT)
- **Affected Script**: `020_241024_prepare_GHG_my.py`
- **Update Source**: Nordhaus DICE model
- **Schema**:
  ```python
  pd.read_hdf('20241022_scc_nordhaus.h5', key='df')
  # Index: Multi-level (year, scenario)
  # Values: Social Cost of Carbon (USD/tonne CO2e)
  ```

**Update Procedure**:
1. **DICE Model Updates**:
   - Check Nordhaus website: https://williamnordhaus.com/dicerice-models
   - Download latest DICE model results
2. **Scenario Configuration**:
   - Define scenarios (discount rates, climate sensitivities)
   - Run DICE model for each scenario
3. **Extract SCC Values**:
   - Extract year-scenario matrix
   - Years: 2014-2030, 2050, 2100
4. **File Update**:
   - Save as HDF5 with key 'df'
   - Multi-index: (year, scenario)
5. **Save**: Update filename with new date (YYYYMMDD format, note different from others)
6. **Config**: Update config.yaml → ghg → input_file
7. **Regenerate**: Run `python 020_241024_prepare_GHG_my.py`

**Critical Check**:
- Units: USD/tonne CO2e (script converts to USD/kg by dividing by 1000)
- Base year: 2019 (different from other scripts)
- All countries get same value for each year-scenario

---

## Update Procedures

### Procedure 1: Update Single Indicator

Use when only one indicator needs updating (e.g., new GHG DICE results available).

```bash
# Step 1: Backup current data
cp input_data/20241022_scc_nordhaus.h5 archive/20241022_scc_nordhaus.h5

# Step 2: Download/create new data file
# (Manual step - obtain updated data)

# Step 3: Place in input_data/ with new date
mv new_scc_data.h5 input_data/20250115_scc_nordhaus.h5

# Step 4: Update config.yaml
# Edit: ghg → input_file: "input_data/20250115_scc_nordhaus.h5"

# Step 5: Regenerate coefficients
python 020_241024_prepare_GHG_my.py

# Step 6: Validate output
python test_validation.py --indicator ghg

# Step 7: Compare outputs
python scripts/compare_outputs.py \
    output/2024-11-18_coefficients_GHG.xlsx \
    output/2025-01-15_coefficients_GHG.xlsx

# Step 8: Document changes
# Add entry to CHANGELOG.md
```

### Procedure 2: Update All Indicators

Use for major refresh or annual update cycle.

```bash
# Step 1: Backup all current data
tar -czf archive/input_data_backup_$(date +%Y%m%d).tar.gz input_data/

# Step 2: Update shared dependencies first
# a. World Bank deflators
python scripts/download_wb_deflators.py  # If script exists
# b. Manually update Model_definitions if needed

# Step 3: Update each indicator sequentially
# Follow individual procedures (3-10 above)

# Step 4: Update config.yaml with all new filenames
# Edit each indicator's input_file path

# Step 5: Regenerate all coefficients
python run_all_value_factors.py

# Step 6: Validate all outputs
python test_validation.py --all

# Step 7: Generate comparison report
python scripts/generate_update_report.py \
    --old archive/output_$(date -d "1 month ago" +%Y%m%d)/ \
    --new output/

# Step 8: Document in CHANGELOG.md
```

### Procedure 3: Add New Country

Use when a new country joins the model (rare).

```bash
# Step 1: Update Model_definitions_owntable.h5
# Add new country with ISO3 code and NACE sectors

# Step 2: Update World Bank deflators
# Ensure new country has deflator data

# Step 3: Update each indicator data file
# Add new country rows/columns with appropriate coefficients
# For files 3-10, add country-specific values

# Step 4: Regenerate all scripts
python run_all_value_factors.py

# Step 5: Validate new country present in all outputs
python test_validation.py --check-country [NEW_ISO3]

# Step 6: Document in CHANGELOG.md
```

### Procedure 4: Emergency Correction

Use when an error is discovered in published coefficients.

```bash
# Step 1: Identify affected indicator(s)

# Step 2: Fix input data file or script logic

# Step 3: Create hotfix branch (if using Git)
git checkout -b hotfix-waste-calculation-error

# Step 4: Regenerate affected indicator
python 007_241001_prepare_Waste_my.py

# Step 5: Validate fix
python test_validation.py --indicator waste

# Step 6: Compare before/after
python scripts/compare_outputs.py \
    output/OLD_FILE.xlsx \
    output/NEW_FILE.xlsx \
    --detailed

# Step 7: Document in CHANGELOG.md with "HOTFIX" label

# Step 8: Notify users of correction
# Email stakeholders, update GitHub release notes
```

---

## Validation Steps

### Pre-Update Validation

Before updating any data file, validate the new file structure:

```python
import pandas as pd

# Example: Validate Waste data file
def validate_waste_file(filepath):
    """Validate waste figures file structure."""
    required_sheets = [
        'Waste_hazardous_incinerated',
        'Waste_hazardous_landfill',
        'Waste_nonhazardous_incinerated',
        'Waste_nonhazardous_landfill'
    ]

    for sheet in required_sheets:
        df = pd.read_excel(filepath, sheet_name=sheet)

        # Check required columns
        assert 'country_code' in df.columns, f"Missing country_code in {sheet}"
        assert 'costs' in df.columns, f"Missing costs in {sheet}"

        # Check data types
        assert df['costs'].dtype in ['float64', 'int64'], f"costs not numeric in {sheet}"

        # Check for nulls
        null_count = df['costs'].isnull().sum()
        if null_count > 0:
            print(f"Warning: {null_count} null values in {sheet}")

        # Check country coverage
        countries = df['country_code'].unique()
        print(f"{sheet}: {len(countries)} countries")

    print("✓ Validation passed")

# Run validation
validate_waste_file('input_data/NEW_Waste_file.xlsx')
```

### Post-Update Validation

After regenerating coefficients, validate outputs:

```python
def validate_output(filepath):
    """Validate output coefficient file."""
    # Load HDF5 or Excel
    if filepath.endswith('.h5'):
        df = pd.read_hdf(filepath, key='coefficients')
    else:
        df = pd.read_excel(filepath, sheet_name='Coefficients', index_col=[0, 1], header=[0, 1])

    # Check dimensions
    years = df.index.get_level_values(0).unique()
    indicators = df.index.get_level_values(1).unique()
    countries = df.columns.get_level_values(0).unique()
    sectors = df.columns.get_level_values(1).unique()

    print(f"Years: {len(years)} (expected 19)")
    print(f"Indicators: {len(indicators)}")
    print(f"Countries: {len(countries)} (expected 188)")
    print(f"Sectors: {len(sectors)}")

    # Check for nulls
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        print(f"Warning: {null_count} null values")

    # Check sign consistency (except Training)
    if 'Training' not in filepath:
        positive_count = (df > 0).sum().sum()
        if positive_count > 0:
            print(f"ERROR: {positive_count} positive coefficients (should be negative)")
    else:
        negative_count = (df < 0).sum().sum()
        if negative_count > 0:
            print(f"ERROR: {negative_count} negative coefficients (should be positive)")

    print("✓ Validation passed")

# Run validation
validate_output('output/2025-01-15_coefficients_GHG.xlsx')
```

### Comparison Validation

Compare new outputs to previous versions:

```python
def compare_outputs(old_file, new_file, threshold=0.10):
    """Compare two output files and flag major changes."""
    old = pd.read_excel(old_file, sheet_name='Coefficients', index_col=[0, 1], header=[0, 1])
    new = pd.read_excel(new_file, sheet_name='Coefficients', index_col=[0, 1], header=[0, 1])

    # Calculate relative difference
    rel_diff = (new - old) / old.abs()

    # Flag large changes
    large_changes = (rel_diff.abs() > threshold).sum().sum()

    print(f"Cells with >{threshold*100}% change: {large_changes}")

    if large_changes > 0:
        # Show examples
        large_mask = rel_diff.abs() > threshold
        examples = rel_diff[large_mask].stack().stack().head(10)
        print("\nExample large changes:")
        print(examples)

    # Overall statistics
    print(f"\nMean relative change: {rel_diff.mean().mean():.2%}")
    print(f"Median relative change: {rel_diff.median().median():.2%}")
    print(f"Max relative change: {rel_diff.abs().max().max():.2%}")

# Run comparison
compare_outputs(
    'output/2024-11-18_coefficients_GHG.xlsx',
    'output/2025-01-15_coefficients_GHG.xlsx'
)
```

---

## Troubleshooting

### Issue 1: File Not Found

**Symptom**: `FileNotFoundError: [Errno 2] No such file or directory`

**Solution**:
1. Verify file exists in `input_data/` directory
2. Check filename in config.yaml matches exactly (case-sensitive)
3. Ensure no typos in date prefix

### Issue 2: Schema Mismatch

**Symptom**: `KeyError: 'costs'` or `KeyError: 'Value'`

**Solution**:
1. Open Excel/HDF5 file and verify column names
2. Check for extra spaces in column names
3. Ensure sheet name matches exactly

### Issue 3: Country Code Mismatch

**Symptom**: Some countries missing in output

**Solution**:
1. Check for country code inconsistencies (SSD vs SDS, SDN vs SUD)
2. Add mapping in script if needed
3. Verify Model_definitions contains all countries

### Issue 4: Unit Conversion Error

**Symptom**: Coefficients are 1000x too large/small

**Solution**:
1. Check units in input file (kg vs tonnes, m³ vs liters, ha vs m²)
2. Verify no double conversion (GHG script divides by 1000)
3. Review unit column in output

### Issue 5: Negative Training Coefficients

**Symptom**: Training outputs have negative values

**Solution**:
1. Check `coefficient_sign` in script (should be +1.0 for Training)
2. Verify input data is positive
3. Check inflation adjustment not flipping sign

### Issue 6: Deflator Year Mismatch

**Symptom**: Future years show wrong unit year (e.g., "2030USD" when only 2023 deflator available)

**Solution**:
1. Expected behavior: Script uses last available deflator year
2. To fix: Update World Bank deflators to include more recent years
3. Or: Accept that forecast years use latest available deflator

---

## Data Versioning

### Current Approach

- **Filename Dating**: Date prefix in YYMMDD or YYYYMMDD format
- **No Formal Versioning**: Files not under version control
- **Manual Archiving**: Old files manually moved to archive/

### Recommended Approach

#### Option 1: Git LFS (Large File Storage)

```bash
# Initialize Git LFS
git lfs install

# Track large files
git lfs track "input_data/*.h5"
git lfs track "input_data/*.xlsx"

# Add .gitattributes
git add .gitattributes

# Commit data files
git add input_data/
git commit -m "Add input data files to Git LFS"

# Push to remote with LFS
git push origin main
```

**Pros**: Version history, easy rollback, integrates with Git workflow
**Cons**: Requires LFS setup, storage costs for large files

#### Option 2: DVC (Data Version Control)

```bash
# Initialize DVC
pip install dvc
dvc init

# Add data directory
dvc add input_data/

# Commit DVC files (not actual data)
git add input_data.dvc .dvc/.gitignore
git commit -m "Add input data to DVC"

# Configure remote storage (e.g., Google Cloud)
dvc remote add -d gcs gs://wifor-value-factors/data
dvc push

# To retrieve specific version
dvc checkout input_data.dvc
```

**Pros**: Designed for large data files, efficient storage, supports cloud backends
**Cons**: Additional tool to learn, requires remote storage setup

#### Option 3: Manual Versioning with Manifest

Create a `data_manifest.yaml`:

```yaml
version: "2025-01-15"
last_updated: "2025-01-15"

files:
  - name: "Model_definitions_owntable.h5"
    path: "input_data/Model_definitions_owntable.h5"
    md5: "a1b2c3d4e5f6..."
    size_bytes: 6369341
    last_modified: "2024-10-01"

  - name: "241001_worldbank_deflator.h5"
    path: "input_data/241001_worldbank_deflator.h5"
    md5: "f6e5d4c3b2a1..."
    size_bytes: 35088
    last_modified: "2024-10-01"
    update_frequency: "quarterly"
    next_check: "2025-04-01"

  # ... (repeat for each file)
```

**Pros**: Simple, no external tools, easy to understand
**Cons**: Manual process, no automatic rollback

### Provenance Tracking

Track which input versions produced which outputs:

```yaml
# execution_metadata.yaml
run_id: "20250115-143022"
timestamp: "2025-01-15 14:30:22"
scripts_executed:
  - name: "020_241024_prepare_GHG_my.py"
    input_files:
      - "input_data/20250115_scc_nordhaus.h5"
      - "input_data/Model_definitions_owntable.h5"
      - "input_data/241001_worldbank_deflator.h5"
    output_files:
      - "output/2025-01-15_coefficients_GHG.h5"
      - "output/2025-01-15_coefficients_GHG.xlsx"
    execution_time: 68.8
    status: "success"
```

---

## Checklist

Use this checklist when updating data files:

### Before Update
- [ ] Backup current input data files
- [ ] Backup current output files
- [ ] Document reason for update in CHANGELOG.md
- [ ] Validate new data file schema
- [ ] Check for breaking changes in data structure

### During Update
- [ ] Update input_data/ file with new version
- [ ] Update config.yaml with new filename
- [ ] Run affected script(s)
- [ ] Monitor execution for errors
- [ ] Check log files for warnings

### After Update
- [ ] Validate output file structure
- [ ] Check sign consistency (negative/positive)
- [ ] Compare to previous output
- [ ] Investigate large changes (>10%)
- [ ] Update CHANGELOG.md with results
- [ ] Commit changes (if using version control)
- [ ] Notify stakeholders of update

---

**Document Version**: 1.0
**Last Updated**: 2026-01-02
**Maintained by**: WifOR Development Team
**Contact**: dimitrij.euler@greenings.org
