# Validation Report Template

**WifOR Value Factors - Output Quality Assurance**
**Organization**: Transition Valuation Partnership under Greenings custodianship
**Version**: 1.0
**Last Updated**: 2026-01-02

This document provides a template for validating value factor outputs and documenting quality checks.

---

## Understanding What's Being Validated

These validation checks ensure the integrity of **damage or value to society** calculations:

### Conceptual Foundation

**Damage or value to society** = Total external costs or benefits imposed on/provided to all of society

- **Damage costs** (negative values): Total harm to society, not company legal liability
  - Example: -$5,000/ton PM2.5 = society's health burden (mortality, morbidity, productivity losses)
  - NOT the company's regulatory fines or lawsuit settlements

- **Benefit values** (positive values): Total value to society, not company ROI
  - Example: +$25/hour training = society's gains (skilled workforce, innovation, GDP growth)
  - NOT the company's training budget or internal ROI

- **Magnitude expectations**: Societal values are typically **10-100× larger** than regulatory fines or company costs
  - This is correct and expected - the gap represents externalities society bears

### Why This Matters for Validation

When validating outputs, expect:
- ✓ Large absolute values (millions of USD for typical industrial activities)
- ✓ Negative values for environmental/social damages
- ✓ Positive values only for training (benefits to society)
- ✓ Values much larger than typical company regulatory costs

**For detailed conceptual explanation, see:**
- METHODOLOGY.md → "Conceptual Foundation: Damage or Value to Society" section
- README.md → "Understanding 'Damage or Value to Society'" section

---

## Validation Checklist

### Date: [YYYY-MM-DD]
### Executed by: [Name]
### Run ID: [run_all_value_factors execution timestamp]

---

## 1. Pre-Execution Validation

### 1.1 Input Data Files Present

- [ ] Model_definitions_owntable.h5
- [ ] 241001_worldbank_deflator.h5
- [ ] 220509_Waste figures merged_update.xlsx
- [ ] 220707_Air pollution_update.xlsx
- [ ] 220511_Water consumption_update.xlsx
- [ ] 230317_Landuse_update_ZK.xlsx
- [ ] 230324_WaterPollution_Mon_Coef_Final_DC.xlsx
- [ ] 220529_training_value_per_hour_bysector.h5
- [ ] 220616_monetization_value_per_incident_NEW.xlsx
- [ ] 20241022_scc_nordhaus.h5

**Notes**: ___________________________________________

### 1.2 Configuration Validation

- [ ] config.yaml exists and is valid YAML
- [ ] All input_file paths match actual filenames
- [ ] Output directory exists or can be created
- [ ] Base years configured (2020 for most, 2019 for GHG)

**Notes**: ___________________________________________

### 1.3 License Acceptance

- [ ] .license_accepted file exists with "Y"

---

## 2. Execution Validation

### 2.1 All Scripts Executed Successfully

| Script | Status | Execution Time | Notes |
|--------|--------|----------------|-------|
| 007_Waste | [ ] Pass / [ ] Fail | ____s | |
| 008_AirPollution | [ ] Pass / [ ] Fail | ____s | |
| 009_WaterConsumption | [ ] Pass / [ ] Fail | ____s | |
| 010_LandUse | [ ] Pass / [ ] Fail | ____s | |
| 013_WaterPol | [ ] Pass / [ ] Fail | ____s | |
| 014_Training | [ ] Pass / [ ] Fail | ____s | |
| 015_OHS | [ ] Pass / [ ] Fail | ____s | |
| 020_GHG | [ ] Pass / [ ] Fail | ____s | |

**Total Execution Time**: ________ seconds

**Errors Encountered**: ___________________________________________

---

## 3. Output File Validation

### 3.1 Files Generated

- [ ] 2024-10-01_coefficients_Waste.xlsx
- [ ] 2024-10-01_coefficients_AirPollution.xlsx
- [ ] 2024-10-01_coefficients_WaterConsumption.xlsx
- [ ] 2024-10-01_coefficients_LandUse.xlsx
- [ ] 2024-10-14_coefficients_WaterPollution.xlsx
- [ ] 2024-10-16_coefficients_Training.xlsx
- [ ] 2024-10-16_coefficients_OHS.xlsx
- [ ] 2024-11-18_coefficients_GHG.xlsx

**Missing Files**: ___________________________________________

### 3.2 File Size Check

| File | Size (MB) | Expected Range | Status |
|------|-----------|----------------|--------|
| Waste | ____ | 3-5 MB | [ ] OK / [ ] Warn |
| AirPollution | ____ | 15-20 MB | [ ] OK / [ ] Warn |
| WaterConsumption | ____ | 0.5-1 MB | [ ] OK / [ ] Warn |
| LandUse | ____ | 6-8 MB | [ ] OK / [ ] Warn |
| WaterPollution | ____ | 7-9 MB | [ ] OK / [ ] Warn |
| Training | ____ | 1.5-2.5 MB | [ ] OK / [ ] Warn |
| OHS | ____ | 2-3 MB | [ ] OK / [ ] Warn |
| GHG | ____ | 5-7 MB | [ ] OK / [ ] Warn |

**Notes**: Significant size deviations may indicate data issues

---

## 4. Data Structure Validation

### 4.1 Dimensions Check

For each output file, verify:

| Indicator | Years | Indicators | Countries | Sectors | Status |
|-----------|-------|------------|-----------|---------|--------|
| Waste | 19 | 6 | 188 | ___ | [ ] Pass |
| AirPollution | 19 | 6 | 188 | ___ | [ ] Pass |
| WaterConsumption | 19 | 1 | 188 | ___ | [ ] Pass |
| LandUse | 19 | ___ | 188 | ___ | [ ] Pass |
| WaterPollution | 19 | 11 | 188 | ___ | [ ] Pass |
| Training | 19 | 1 | 188 | ___ | [ ] Pass |
| OHS | 19 | 4 | 188 | ___ | [ ] Pass |
| GHG | 19 | ___ | 188 | ___ | [ ] Pass |

**Expected Years**: 2014-2030 (17), 2050, 2100 (total: 19)

**Expected Countries**: 188 (ISO3 codes)

**Failures**: ___________________________________________

### 4.2 Null Value Check

| Indicator | Null Cells | Total Cells | Null % | Status |
|-----------|------------|-------------|--------|--------|
| Waste | ___ | ___ | ___% | [ ] Pass (<1%) |
| AirPollution | ___ | ___ | ___% | [ ] Pass |
| WaterConsumption | ___ | ___ | ___% | [ ] Pass |
| LandUse | ___ | ___ | ___% | [ ] Pass |
| WaterPollution | ___ | ___ | ___% | [ ] Pass |
| Training | ___ | ___ | ___% | [ ] Pass |
| OHS | ___ | ___ | ___% | [ ] Pass |
| GHG | ___ | ___ | ___% | [ ] Pass |

**Threshold**: <1% nulls acceptable for data gaps

**Issues**: ___________________________________________

---

## 5. Sign Convention Validation

### 5.1 Damage Cost Indicators (Should be Negative)

| Indicator | Positive Cells | Total Cells | % Positive | Status |
|-----------|----------------|-------------|------------|--------|
| Waste | ___ | ___ | ___% | [ ] Pass (0%) |
| AirPollution | ___ | ___ | ___% | [ ] Pass |
| WaterConsumption | ___ | ___ | ___% | [ ] Pass |
| LandUse | ___ | ___ | ___% | [ ] Pass |
| WaterPollution | ___ | ___ | ___% | [ ] Pass |
| OHS | ___ | ___ | ___% | [ ] Pass |
| GHG | ___ | ___ | ___% | [ ] Pass |

**Failures**: ___________________________________________

### 5.2 Benefit Indicator (Should be Positive)

| Indicator | Negative Cells | Total Cells | % Negative | Status |
|-----------|----------------|-------------|------------|--------|
| Training | ___ | ___ | ___% | [ ] Pass (0%) |

**Failures**: ___________________________________________

---

## 6. Unit Consistency Validation

### 6.1 Expected Units

| Indicator | Expected Unit | Actual Unit (sample) | Status |
|-----------|---------------|----------------------|--------|
| Waste | yearUSD/kg | __________ | [ ] Pass |
| AirPollution | yearUSD/kg | __________ | [ ] Pass |
| WaterConsumption | yearUSD/m3 | __________ | [ ] Pass |
| LandUse | yearUSD/ha | __________ | [ ] Pass |
| WaterPollution | yearUSD/kg | __________ | [ ] Pass |
| Training | yearUSD/h | __________ | [ ] Pass |
| OHS | yearUSD/case | __________ | [ ] Pass |
| GHG | yearUSD/kg | __________ | [ ] Pass |

**Note**: "year" should be 2020 for most, 2019 for GHG

**Examples for 2050/2100**: May show "2023USD" if deflator only available through 2023

**Failures**: ___________________________________________

---

## 7. Temporal Consistency Validation

### 7.1 Inflation Adjustment Check

Sample a few cells and verify inflation adjustment is smooth:

**Waste - Hazardous Incinerated - USA - Sample Sector**:
- 2020: ____________ (base year)
- 2025: ____________ (should be ~5-10% higher)
- 2030: ____________ (should be ~10-20% higher)

**Trend**: [ ] Smooth increase / [ ] Irregular / [ ] Decrease (unexpected)

### 7.2 GHG Year-Specific Values

Verify all countries have identical values for each year-scenario:

**GHG - Scenario [___] - Year 2025**:
- USA: ____________
- DEU: ____________
- CHN: ____________

**Status**: [ ] All identical (expected) / [ ] Differ (error)

---

## 8. Spatial Consistency Validation

### 8.1 Country-Specific Variation

Sample indicator (e.g., Air Pollution PM2.5, Year 2020):
- USA: ____________
- DEU: ____________
- CHN: ____________
- BRA: ____________

**Status**: [ ] Values differ by country (expected) / [ ] All identical (error)

### 8.2 Sector-Specific Variation (Training Only)

Training - Year 2020 - USA:
- Sector 1: ____________
- Sector 2: ____________
- Sector 3: ____________

**Status**: [ ] Values differ by sector (expected) / [ ] All identical (check if intended)

**Other Indicators**: Should have same value across all sectors for a given country-year

---

## 9. Value Range Validation

### 9.1 Reasonableness Check

Sample values and verify in expected ranges:

| Indicator | Sample Value | Unit | Reasonable? | Notes |
|-----------|--------------|------|-------------|-------|
| Waste Hazardous Incinerate | ____ | USD/kg | [ ] Yes | Expect $0.1-$10/kg |
| Air PM2.5 | ____ | USD/kg | [ ] Yes | Expect $10-$1000/kg |
| Water Consumption | ____ | USD/m3 | [ ] Yes | Expect $0.01-$10/m3 |
| Land Use | ____ | USD/ha | [ ] Yes | Expect $100-$50000/ha |
| Training | ____ | USD/h | [ ] Yes | Expect $5-$100/h |
| OHS Fatality | ____ | USD/case | [ ] Yes | Expect $1M-$10M/case |
| GHG | ____ | USD/kg | [ ] Yes | Expect $0.05-$0.50/kg CO2e |

**Outliers**: ___________________________________________

---

## 10. Comparison to Previous Run

### 10.1 Change Analysis

Compare to previous execution (if available):

| Indicator | Previous Date | New Date | Mean Change | Max Change | Status |
|-----------|---------------|----------|-------------|------------|--------|
| Waste | ______ | ______ | ___% | ___% | [ ] <10% / [ ] >10% |
| AirPollution | ______ | ______ | ___% | ___% | [ ] <10% / [ ] >10% |
| WaterConsumption | ______ | ______ | ___% | ___% | [ ] <10% / [ ] >10% |
| LandUse | ______ | ______ | ___% | ___% | [ ] <10% / [ ] >10% |
| WaterPollution | ______ | ______ | ___% | ___% | [ ] <10% / [ ] >10% |
| Training | ______ | ______ | ___% | ___% | [ ] <10% / [ ] >10% |
| OHS | ______ | ______ | ___% | ___% | [ ] <10% / [ ] >10% |
| GHG | ______ | ______ | ___% | ___% | [ ] <10% / [ ] >10% |

**Note**: Changes >10% warrant investigation (unless data update expected)

**Explanation for Large Changes**: ___________________________________________

---

## 11. Cross-Indicator Consistency

### 11.1 Relative Magnitudes

Verify expected relationships:

- [ ] Air Pollution PM2.5 damage > PM10 damage (finer particles more harmful)
- [ ] OHS Fatality damage > Nonfatal damage
- [ ] Hazardous Waste damage > Non-hazardous Waste damage

**Failures**: ___________________________________________

### 11.2 Country Rankings

Sample indicator (Air PM2.5, Year 2020) - Top 5 countries by damage cost:
1. ______ : ______
2. ______ : ______
3. ______ : ______
4. ______ : ______
5. ______ : ______

**Expected**: High-income countries typically have higher VSL-based damages

**Status**: [ ] Reasonable / [ ] Unexpected ranking

---

## 12. Documentation Validation

- [ ] CHANGELOG.md updated with this run
- [ ] Input file versions documented
- [ ] Execution log saved (execution_log_YYYYMMDD_HHMMSS.txt)
- [ ] This validation report completed

---

## 13. Summary

### Overall Validation Status

- **Total Checks**: ______
- **Passed**: ______
- **Failed**: ______
- **Warnings**: ______

### Pass/Fail Determination

- [ ] **PASS** - All critical checks passed, output approved for use
- [ ] **PASS WITH WARNINGS** - Minor issues, acceptable for use with noted limitations
- [ ] **FAIL** - Critical issues found, output should not be used until resolved

### Critical Issues Identified

1. ___________________________________________
2. ___________________________________________
3. ___________________________________________

### Recommended Actions

1. ___________________________________________
2. ___________________________________________
3. ___________________________________________

---

## 14. Approval

**Validated by**: ________________________

**Date**: ________________________

**Signature**: ________________________

---

## Appendix: Automated Validation Script

```python
"""
Automated validation script for WifOR Value Factors outputs.
Run after executing run_all_value_factors.py
"""

import pandas as pd
from pathlib import Path

def validate_output(filepath, expected_dims):
    """Validate single output file."""
    print(f"\nValidating {filepath.name}...")

    # Load data
    df = pd.read_excel(filepath, sheet_name='Coefficients',
                       index_col=[0,1], header=[0,1])

    # Check dimensions
    years = df.index.get_level_values(0).unique()
    indicators = df.index.get_level_values(1).unique()
    countries = df.columns.get_level_values(0).unique()
    sectors = df.columns.get_level_values(1).unique()

    print(f"  Dimensions: {len(years)} years, {len(indicators)} indicators, "
          f"{len(countries)} countries, {len(sectors)} sectors")

    assert len(years) == 19, f"Expected 19 years, got {len(years)}"
    assert len(countries) == 188, f"Expected 188 countries, got {len(countries)}"

    # Check for nulls
    null_count = df.isnull().sum().sum()
    null_pct = null_count / df.size * 100
    print(f"  Null values: {null_count} ({null_pct:.2f}%)")
    if null_pct > 1:
        print(f"  WARNING: >1% null values")

    # Check sign
    if 'Training' in filepath.name:
        negative_count = (df < 0).sum().sum()
        if negative_count > 0:
            print(f"  ERROR: {negative_count} negative coefficients in Training")
    else:
        positive_count = (df > 0).sum().sum()
        if positive_count > 0:
            print(f"  ERROR: {positive_count} positive coefficients")

    print("  ✓ Validation complete")

# Run validation
output_dir = Path('output')
files = {
    'Waste': {'indicators': 6},
    'AirPollution': {'indicators': 6},
    'WaterConsumption': {'indicators': 1},
    'LandUse': {'indicators': None},  # Variable
    'WaterPollution': {'indicators': 11},
    'Training': {'indicators': 1},
    'OHS': {'indicators': 4},
    'GHG': {'indicators': None}  # Variable scenarios
}

for indicator, dims in files.items():
    file_pattern = f"*_coefficients_{indicator}.xlsx"
    matches = list(output_dir.glob(file_pattern))
    if matches:
        validate_output(matches[0], dims)
    else:
        print(f"\nWARNING: No file found for {indicator}")

print("\n" + "="*70)
print("Validation complete")
print("="*70)
```

---

**Document Version**: 1.0
**Last Updated**: 2026-01-02
**Maintained by**: WifOR Development Team
**Contact**: dimitrij.euler@greenings.org
