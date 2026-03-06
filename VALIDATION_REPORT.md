# Validation Report Template

**All Three Value Factor Systems — WifOR · EPS (Steen / Stockholm) · UBA MC 4.0**
**Organization**: Transition Valuation Project under Greenings custodianship
**Version**: 2.0
**Last Updated**: 2026-03-05

This document provides a template for validating the outputs of all three value factor
submodules: WifOR (`value-factors/`), EPS 2015d.1 (`stockholm-value-factors/`), and
UBA MC 4.0 (`uba-value-factors/`). Run each section after executing the respective pipeline.

### System overview

| System | Script | Expected output | Countries | Substances / rows |
|--------|--------|----------------|-----------|-------------------|
| WifOR | `run_all_value_factors.py` | 8 × `.h5` + `.xlsx` | 188 | 8 indicator groups |
| EPS (Steen) | `run_all_eps_factors.py` | 12 × `.h5` + `.xlsx` | 189 | 892 substances |
| UBA MC 4.0 | `extract_uba_values.py` | 10 × `.csv` + `.xlsx` | 1 (DEU) | 546 rows |

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

---

# Part A — WifOR Value Factors (`value-factors/`)

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

---

# Part B — EPS Value Factors (`stockholm-value-factors/`)

**System:** EPS 2015d.1 — Environmental Priority Strategies
**Source:** Steen (2015), Swedish Life Cycle Center, Chalmers University of Technology
**Geographic anchor:** Sweden (globally applied via VFT; no built-in country differentiation)
**Price base:** EUR 2015 (Environmental Load Units, ELU ≈ EUR); EU HICP deflator applied

---

## B.1 Pre-Execution Validation

### B.1.1 Input Data Files Present

Navigate to `stockholm-value-factors/`:

- [ ] `data/` folder exists with EPS source CSV/Excel files (substance characterisation factors)
- [ ] `config.py` exists and is valid
- [ ] Python environment has: `pandas`, `numpy`, `openpyxl`, `tables`

### B.1.2 License / Attribution

EPS 2015d.1 is freely available but requires attribution to Steen (2015) and the Swedish Life Cycle Center. No separate license acceptance file is needed.

---

## B.2 Execution Validation

Run from `stockholm-value-factors/`:

```bash
python run_all_eps_factors.py
```

### B.2.1 Script Execution Status

| Script / Category | Status | Rows expected | Notes |
|-------------------|--------|---------------|-------|
| 001 Inorganic gases | [ ] Pass / [ ] Fail | 16 substances | CO₂, CH₄, N₂O, SO₂, NOₓ, NH₃, O₃, HF, HCl, HBr, HCN, H₂S, HNO₂, HNO₃, Hg variants |
| 002 Particles | [ ] Pass / [ ] Fail | 14 substances | PM>10, PM10, PM2.5, ultrafine, metals, PAH |
| 003 VOCs | [ ] Pass / [ ] Fail | 144 substances | Alkanes, aromatics, alcohols, aldehydes, terpenes, chlorinated |
| 004 Halogenated organics | [ ] Pass / [ ] Fail | 283 substances | CFCs, HCFCs, HFCs, PFCs, halons |
| 005 Emissions to water | [ ] Pass / [ ] Fail | 14 substances | BOD, COD, N, P, heavy metals |
| 006 Pesticides | [ ] Pass / [ ] Fail | 302 substances | Herbicides, insecticides, fungicides |
| 007 Noise | [ ] Pass / [ ] Fail | 2 substances | Road traffic noise (ELU/W) |
| 008 Radionuclides | [ ] Pass / [ ] Fail | 11 substances | C-14, H-3, I-129, Kr-85, Pb-210, and others |
| 009 Land use | [ ] Pass / [ ] Fail | 23 categories | Residential, arable, forestry, mining, corridors |
| 010 Fossil resources | [ ] Pass / [ ] Fail | 4 substances | Oil, coal, lignite, natural gas |
| 011 Other elements | [ ] Pass / [ ] Fail | 77 substances | Ag, rare earths, PGMs, Li, Co, In, Ga, Zr |
| 012 Waste (litter) | [ ] Pass / [ ] Fail | 2 substances | Litter to ground, plastic litter to water |
| **Total** | | **892 substances** | |

**Execution time expected:** < 60 seconds

---

## B.3 Output File Validation

### B.3.1 Files Generated

Navigate to `stockholm-value-factors/output/`:

- [ ] 12 indicator files (`NNN_uba4_*.csv` or `.h5`/`.xlsx` per pipeline convention)
- [ ] Execution log written

### B.3.2 Dimension Check

| Category | Years | Countries | Sectors | Sign |
|----------|-------|-----------|---------|------|
| All 12 categories | 19 (2014–2030, 2050, 2100) | 189 | 21 NACE | All negative (−1.0) |

**Critical:** EPS has NO country differentiation in its published values — all 189 countries carry the same ELU/kg coefficient before income-based value transfer. Verify this is preserved in the output (uniform columns across countries).

### B.3.3 Reference Values

| Substance | EPS index value | Unit | Notes |
|-----------|----------------|------|-------|
| CO₂ | ~0.05–0.10 | ELU/kg | Climate damage pathway sum |
| PM₂.₅ | >CO₂ per kg | ELU/kg | Health (YOLL) dominant |
| NOₓ | intermediate | ELU/kg | Health + acid deposition |
| SO₂ | intermediate | ELU/kg | Health + acid deposition |

Cross-check against Steen (2015) Table A.1 for substance-level EPS index values.

### B.3.4 Temporal Consistency

EPS uses EU HICP deflator for temporal adjustment:
- 2015 = 1.000 (base)
- 2023 = 1.241 (last available; verified against Eurostat)
- 2024–2100: frozen at 1.241 (no forecast; intentional)

**Check:** Values in 2023–2100 should be identical (deflator frozen).

---

## B.4 Known Limitations

- No country differentiation in base EPS values (uniform globally — Sweden-anchored WTP)
- Income-based VFT to other countries is described in `VALUE_TRANSFER.md` but not applied within the EPS pipeline itself
- Noise unit (ELU/W) is not directly comparable to UBA noise (EUR/person/year) without exposure conversion
- EPS 2015d.1 is not yet updated to reflect post-2015 emission inventory or valuation studies

---

# Part C — UBA Value Factors (`uba-value-factors/`)

**System:** UBA Handbook on Environmental Value Factors, Methodological Convention 4.0
**Source:** Eser, Matthey, Bünger — German Environment Agency (UBA), December 2025; ISSN 2363-832X
**Geographic anchor:** Germany (air/transport); global for GHG (GIVE model, Anthoff 2025)
**Price base:** EUR 2025

---

## C.1 Pre-Execution Validation

Navigate to `uba-value-factors/`:

### C.1.1 Files Present

- [ ] `pipeline.py` — data structures and builder functions
- [ ] `config.py` — table group configuration and output paths
- [ ] `extract_uba_values.py` — orchestrator
- [ ] `tables/` — 10 individual table scripts (`01_ghg.py` through `10_agriculture.py`)
- [ ] `output/` — directory exists or will be created
- [ ] Python environment has: `csv`, `openpyxl`, `pathlib`, `logging`

No license file required. Source: public UBA handbook (open access, ISSN 2363-832X).

---

## C.2 Execution Validation

```bash
cd uba-value-factors/
python extract_uba_values.py
# Expected: Done: 10/10 succeeded, 0 failed
```

### C.2.1 Script Execution Status

| ID | Key | Expected rows | Status |
|----|-----|---------------|--------|
| 01 | ghg | 54 | [ ] Pass / [ ] Fail |
| 02 | air_pollutants | 133 | [ ] Pass / [ ] Fail |
| 03 | electricity | 45 | [ ] Pass / [ ] Fail |
| 04 | heat | 45 | [ ] Pass / [ ] Fail |
| 05 | refrigerants | 16 | [ ] Pass / [ ] Fail |
| 06 | transport_vehkm | 142 | [ ] Pass / [ ] Fail |
| 07 | transport_pkm_tkm | 38 | [ ] Pass / [ ] Fail |
| 08 | noise | 42 | [ ] Pass / [ ] Fail |
| 09 | nitrogen_phosphorus | 11 | [ ] Pass / [ ] Fail |
| 10 | agriculture | 20 | [ ] Pass / [ ] Fail |
| **Total** | | **546** | |

**Execution time expected:** < 5 seconds

---

## C.3 Output File Validation

### C.3.1 Files Generated

Navigate to `uba-value-factors/output/`:

- [ ] 10 × `NN_uba4_KEY.csv` (UTF-8, comma-delimited)
- [ ] 10 × `NN_uba4_KEY.xlsx` (two sheets: "Value Factors" + "Metadata")
- [ ] `execution_log_YYYYMMDD_HHMMSS.txt`

### C.3.2 Known-Good Reference Values

Verify these exact values against the UBA MC 4.0 PDF (Table 1 and Table 2):

| Indicator | Substance | Year | PRTP | Value | Unit |
|-----------|-----------|------|------|-------|------|
| ghg | CO₂/CO₂-eq | 2025 | 0 % | **990** | EUR 2025/t |
| ghg | CO₂/CO₂-eq | 2025 | 1 % | **345** | EUR 2025/t |
| ghg | CH₄ | 2025 | 0 % | **9,220** | EUR 2025/t |
| ghg | N₂O | 2025 | 0 % | **282,300** | EUR 2025/t |
| air_pollutants | PM₂.₅ | — | — | **128,200** | EUR 2025/t (health, unknown source) |
| air_pollutants | NOₓ | — | — | **37,740** | EUR 2025/t (total, unknown source) |
| transport_vehkm | Car Petrol, all routes | — | 0 % | **30.91** | EUR-cent 2025/veh-km (total) |
| refrigerants | R-32 | — | 0 % | **670** | EUR 2025/kg |

```python
# Quick Python verification:
import pandas as pd

ghg = pd.read_csv("uba-value-factors/output/01_uba4_ghg.csv")
co2_2025 = ghg.query("substance=='CO2_CO2eq' and emission_year==2025 and prtp_pct==0")["value_factor"].iloc[0]
assert co2_2025 == 990, f"Reference mismatch: {co2_2025}"

ap = pd.read_csv("uba-value-factors/output/02_uba4_air_pollutants.csv")
pm25 = ap.query("substance=='PM2.5' and context=='unknown_source' and impact_component=='health'")["value_factor"].iloc[0]
assert pm25 == 128200, f"Reference mismatch: {pm25}"

print("UBA reference values: OK")
```

### C.3.3 Sign Convention

All UBA value factors are positive in the CSV (they are costs expressed as positive magnitudes). The sign convention (−1.0 for damages) is applied at the value-transfer step when populating the WifOR `C[y,i,c,s]` matrix. See `VALUE_TRANSFER.md`.

---

## C.4 Known Limitations

- Germany-specific receptor data for air pollutants and transport (EcoSenseWeb v1.3); not valid for other countries without value transfer
- Agriculture factors are lower bounds: exclude biodiversity, ecosystem services beyond N/P, animal welfare
- Noise factors cover annoyance and cognitive impairment in children only; exclude sleep disturbance health endpoints
- GHG series ends at 2050; no UBA projection to 2100 (unlike WifOR and EPS)
- Single price level (EUR 2025) with no time series deflation within the pipeline

---

# Summary: All Three Systems

| Check | WifOR | EPS (Steen) | UBA MC 4.0 |
|-------|:-----:|:-----------:|:----------:|
| Pipeline runs clean (0 failures) | [ ] | [ ] | [ ] |
| Row / substance counts match expected | [ ] | [ ] | [ ] |
| Sign convention correct | [ ] | [ ] | [ ] |
| Reference values verified | [ ] | [ ] | [ ] |
| Output files present and non-empty | [ ] | [ ] | [ ] |
| Execution log written | [ ] | [ ] | [ ] |

**Document Version**: 2.0
**Last Updated**: 2026-03-06
**Maintained by**: Dr Dimitrij Euler, Greenings
**Contact**: dimitrij.euler@greenings.org
