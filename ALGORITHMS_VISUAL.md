# Visual Algorithm Flowcharts

**WifOR Value Factors - Visual Documentation**
**Organization**: Transition Valuation Project under Greenings custodianship
**Version**: 1.0
**Last Updated**: 2026-01-02

This document provides visual representations of the value factor calculation algorithms.

---

## Common Architecture Flowchart

```
┌─────────────────────────────────────────────────────────────┐
│                    START VALUE FACTOR SCRIPT                 │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ SECTION 1: CONFIGURATION                                     │
│  ├─ Load config from config.py                              │
│  ├─ Get indicator name (e.g., "waste", "air_pollution")     │
│  ├─ Get input file path                                      │
│  ├─ Get output directory                                     │
│  ├─ Get base_year (2020 for most, 2019 for GHG)             │
│  └─ Define years: [2014-2030, 2050, 2100]                   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ SECTION 2: LOAD DATA                                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ SHARED DATA (All Scripts)                              │ │
│  │  ├─ Model_definitions_owntable.h5                      │ │
│  │  │   └─ 188 countries (ISO3), NACE sectors             │ │
│  │  └─ 241001_worldbank_deflator.h5                       │ │
│  │      └─ GDP deflators by country × year                │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ INDICATOR-SPECIFIC DATA                                │ │
│  │  ├─ If Excel: pd.read_excel(input_file, sheet=...)    │ │
│  │  └─ If HDF5: pd.read_hdf(input_file, key=...)         │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ SECTION 3: PROCESS COEFFICIENT DATA                         │
│  ├─ Clean and reshape raw data                              │
│  │   ├─ Handle missing values                               │
│  │   ├─ Transpose if needed (indicators→rows, countries→cols)│
│  │   └─ Fix country code mismatches (SSD→SDS, SDN→SUD)     │
│  ├─ Create empty coefficient matrix                         │
│  │   └─ Structure: (Year × Indicator) × (Country × Sector) │
│  ├─ Populate matrix with raw values                         │
│  │   ├─ Apply sign convention:                              │
│  │   │   ├─ -1.0 for damages (7 indicators)                │
│  │   │   └─ +1.0 for benefits (Training only)              │
│  │   ├─ For GHG: Apply to all years (year-specific)        │
│  │   └─ For others: Same value across years (then inflate) │
│  └─ Result: Coefficient matrix filled with base values      │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ SECTION 4: APPLY MULTI-YEAR DEFLATION                       │
│  ├─ Calculate inflation factors                             │
│  │   └─ For each year:                                      │
│  │       factor[y] = deflator[USA,y] / deflator[USA,base]   │
│  ├─ Apply factors to coefficients                           │
│  │   └─ coeff[y] = coeff[y] × factor[y]                    │
│  └─ Result: Coefficients in constant base-year USD          │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ SECTION 5: SAVE RESULTS                                     │
│  ├─ Create units dataframe                                  │
│  │   └─ Format: "2020USD/kg", "2025USD/m3", etc.           │
│  ├─ Save to HDF5                                            │
│  │   ├─ Key: 'coefficients' → coefficient matrix           │
│  │   └─ Key: 'units' → unit metadata                       │
│  ├─ Save to Excel                                           │
│  │   ├─ Sheet: 'Coefficients' → coefficient matrix         │
│  │   └─ Sheet: 'Units' → unit metadata                     │
│  └─ Output files:                                           │
│      ├─ output/YYYYMMDD_coefficients_[Indicator].h5        │
│      └─ output/YYYYMMDD_coefficients_[Indicator].xlsx      │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                          END                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      INPUT DATA SOURCES                      │
└─────────────────────────────────────────────────────────────┘
         │                           │                     │
         │ Shared Data               │ Indicator Data     │ External
         │                           │                     │
    ┌────▼─────┐              ┌─────▼──────┐        ┌────▼─────┐
    │ Model    │              │ 220509     │        │ OECD     │
    │ Defs     │              │ Waste.xlsx │        │ World    │
    │ .h5      │              │            │        │ Bank     │
    └────┬─────┘              │ 220707     │        │ UBA      │
         │                    │ Air.xlsx   │        │ DICE     │
    ┌────▼─────┐              │            │        │ etc.     │
    │ Deflator │              │ ... (8     │        └──────────┘
    │ .h5      │              │ files)     │
    └────┬─────┘              └─────┬──────┘
         │                           │
         │                           │
         └────────────┬──────────────┘
                      │
             ┌────────▼─────────┐
             │ VALUE FACTOR     │
             │ SCRIPTS (8)      │
             │  ├─ 007 Waste    │
             │  ├─ 008 Air      │
             │  ├─ 009 Water C. │
             │  ├─ 010 Land     │
             │  ├─ 013 Water P. │
             │  ├─ 014 Training │
             │  ├─ 015 OHS      │
             │  └─ 020 GHG      │
             └────────┬─────────┘
                      │
         ┌────────────┴─────────────┐
         │                          │
    ┌────▼─────┐              ┌────▼─────┐
    │ OUTPUT   │              │ OUTPUT   │
    │ .h5      │              │ .xlsx    │
    │ (8 files)│              │ (8 files)│
    └──────────┘              └──────────┘
```

---

## Multi-Index Structure Visualization

### Coefficient Matrix Structure

```
Index (Rows): 2-level MultiIndex
├─ Level 0: Year
│   ├─ 2014
│   ├─ 2015
│   ├─ ...
│   ├─ 2030
│   ├─ 2050
│   └─ 2100  (19 total)
│
└─ Level 1: Indicator
    ├─ COEFFICIENT [Indicator Name 1]
    ├─ COEFFICIENT [Indicator Name 2]
    └─ ...  (varies by script: 1-11 indicators)

Columns: 2-level MultiIndex
├─ Level 0: Country (GeoRegion)
│   ├─ USA
│   ├─ DEU
│   ├─ CHN
│   └─ ...  (188 total)
│
└─ Level 1: Sector (NACE)
    ├─ Sector 1
    ├─ Sector 2
    └─ ...  (varies)

Values: Float64 (damage costs in USD)
```

### Example Structure

```
                      │ USA                    │ DEU                    │
                      │ Sector1 │ Sector2 │... │ Sector1 │ Sector2 │... │
──────────────────────┼─────────┼─────────┼────┼─────────┼─────────┼────┤
2020 │ COEFF Waste_haz│ -2.45   │ -2.45   │... │ -3.12   │ -3.12   │... │
     │ COEFF Waste_non│ -0.82   │ -0.82   │... │ -1.05   │ -1.05   │... │
──────────────────────┼─────────┼─────────┼────┼─────────┼─────────┼────┤
2025 │ COEFF Waste_haz│ -2.63   │ -2.63   │... │ -3.35   │ -3.35   │... │
     │ COEFF Waste_non│ -0.88   │ -0.88   │... │ -1.13   │ -1.13   │... │
──────────────────────┼─────────┼─────────┼────┼─────────┼─────────┼────┤
...
```

---

## Inflation Adjustment Flow

```
┌─────────────────────────────────────────────────────────────┐
│ Base Coefficient (from input data, single value)            │
│ Example: Waste hazardous incineration = -2.45 USD/kg (2020) │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Replicate across
                         │ all years initially
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Pre-Inflation Matrix (all years = same base value)          │
│  2014: -2.45                                                 │
│  2015: -2.45                                                 │
│  ...                                                         │
│  2030: -2.45                                                 │
│  2050: -2.45                                                 │
│  2100: -2.45                                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Apply USA inflation
                         │ factor for each year
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Calculate Inflation Factors                                  │
│  factor[2014] = deflator[USA,2014] / deflator[USA,2020]     │
│             = 95.2 / 100.0 = 0.952                          │
│  factor[2015] = deflator[USA,2015] / deflator[USA,2020]     │
│             = 96.1 / 100.0 = 0.961                          │
│  ...                                                         │
│  factor[2020] = deflator[USA,2020] / deflator[USA,2020]     │
│             = 100.0 / 100.0 = 1.000  (base year)            │
│  ...                                                         │
│  factor[2030] = deflator[USA,2030] / deflator[USA,2020]     │
│             = 115.8 / 100.0 = 1.158                         │
│  factor[2050] = deflator[USA,2023] / deflator[USA,2020]     │
│             = 108.5 / 100.0 = 1.085  (uses last available)  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Multiply each year's
                         │ coefficients by factor
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Post-Inflation Matrix (constant 2020 USD)                   │
│  2014: -2.45 × 0.952 = -2.33  (2014USD/kg)                  │
│  2015: -2.45 × 0.961 = -2.35  (2015USD/kg)                  │
│  ...                                                         │
│  2020: -2.45 × 1.000 = -2.45  (2020USD/kg) ← base           │
│  ...                                                         │
│  2030: -2.45 × 1.158 = -2.84  (2030USD/kg)                  │
│  2050: -2.45 × 1.085 = -2.66  (2023USD/kg) ← last available │
└─────────────────────────────────────────────────────────────┘
```

---

## Script-Specific Flows

### 007-015: Country-Specific Indicators (7 scripts)

```
Input Data                Process                  Output
─────────────────────────────────────────────────────────
Country-specific    ┌─►  Same value across     Multi-year
damage costs            all years initially    coefficients
(single year)       │                          (19 years)
                    │
Example:            │    Apply inflation       Country-specific
USA: -2.45         ─┴─►  factor per year   ──► USA: [-2.33, ..., -2.84]
DEU: -3.12                                      DEU: [-2.97, ..., -3.61]
CHN: -1.85                                      CHN: [-1.76, ..., -2.14]
```

### 020: GHG Year-Specific Indicator (1 script)

```
Input Data                Process                  Output
─────────────────────────────────────────────────────────
Year-specific       ┌─►  ALREADY year-          Multi-year
SCC values              specific in input       coefficients
(varies by year)    │                          (19 years)
                    │
Example:            │    Apply inflation       Global (all countries
2020: -0.185       ─┴─►  factor per year   ──► get same value)
2025: -0.215                                    ALL: [-0.176, ..., -0.249]
2030: -0.250                                    (example for one scenario)
```

**Key Difference**: GHG input already varies by year; others start with single value and inflate

---

## Sign Convention Decision Tree

```
                    ┌─────────────────────┐
                    │ Load Indicator Data │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼───────────┐
                    │ Is this Training?    │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼──────────┐
                    │        YES          │
                    │ coefficient_sign    │
                    │     = +1.0          │
                    │  (Benefit)          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Result: POSITIVE      │
                    │ coefficients          │
                    │ (Training hours add   │
                    │  value to workers)    │
                    └──────────────────────┘

                    ┌──────────────────────┐
                    │        NO            │
                    │ coefficient_sign     │
                    │     = -1.0           │
                    │  (Damage Cost)       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Result: NEGATIVE      │
                    │ coefficients          │
                    │ (Environmental/social │
                    │  damages cost society)│
                    └──────────────────────┘
```

---

## Data Transformation Examples

### Example 1: Waste (Excel → MultiIndex)

```
INPUT (Excel):
              country_code │ costs (USD/kg)
─────────────────────────────────────────
              USA          │ -2.45
              DEU          │ -3.12
              CHN          │ -1.85
              ...          │ ...

TRANSPOSE:
              USA    │ DEU    │ CHN    │ ...
─────────────────────────────────────────────
costs         -2.45  │ -3.12  │ -1.85  │ ...

EXPAND TO MULTI-INDEX:
                                USA               DEU               CHN
                                Sec1 │ Sec2 │... │ Sec1 │ Sec2 │... │ ...
─────────────────────────────────────────────────────────────────────────
2020│COEFF Waste_haz_inc       -2.45│-2.45│... │-3.12│-3.12│... │ ...
    │COEFF Waste_haz_land       ...
...

APPLY INFLATION:
                                USA               DEU               CHN
                                Sec1 │ Sec2 │... │ Sec1 │ Sec2 │... │ ...
─────────────────────────────────────────────────────────────────────────
2014│COEFF Waste_haz_inc       -2.33│-2.33│... │-2.97│-2.97│... │ ...
2015│COEFF Waste_haz_inc       -2.35│-2.35│... │-2.99│-2.99│... │ ...
...
2020│COEFF Waste_haz_inc       -2.45│-2.45│... │-3.12│-3.12│... │ ... (base)
...
2030│COEFF Waste_haz_inc       -2.84│-2.84│... │-3.61│-3.61│... │ ...
```

### Example 2: Air Pollution (Multi-indexed Excel → MultiIndex)

```
INPUT (Excel with multi-index):
              pollutant │ country_code │ Value (USD/kg)
────────────────────────────────────────────────────
              PM2.5     │ USA          │ -523.00
              PM2.5     │ DEU          │ -678.00
              PM10      │ USA          │ -125.00
              PM10      │ DEU          │ -162.00
              ...

UNSTACK:
              USA     │ DEU     │ CHN     │ ...
───────────────────────────────────────────────
PM2.5         -523.00 │ -678.00 │ -385.00 │ ...
PM10          -125.00 │ -162.00 │ -92.00  │ ...
NOx           -45.50  │ -59.00  │ -33.50  │ ...
...

EXPAND TO MULTI-INDEX (same as Waste example above)
APPLY INFLATION (same as Waste example above)
```

---

## Parallel Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│ run_all_value_factors.py --max-workers 4                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                ┌────────▼────────┐
                │ ThreadPoolExecutor
                │ (4 worker threads)│
                └────────┬────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼─────┐     ┌────▼─────┐    ┌────▼─────┐    ┌──────────┐
   │ Thread 1 │     │ Thread 2 │    │ Thread 3 │    │ Thread 4 │
   │  007     │     │  008     │    │  009     │    │  010     │
   │  Waste   │     │  Air     │    │  Water C │    │  Land    │
   └────┬─────┘     └────┬─────┘    └────┬─────┘    └────┬─────┘
        │                │                │                │
        │ Completes      │                │                │
        │ (50s)          │                │                │
        ▼                │                │                │
   ┌─────────┐           │                │                │
   │ Thread 1│           │                │                │
   │  013    │           │                │                │
   │  Water P│           │ Completes      │ Completes      │
   └────┬────┘           │ (169s)         │ (13s)          │
        │                ▼                ▼                │
        │           ┌─────────┐      ┌─────────┐          │
        │           │ Thread 2│      │ Thread 3│          │
        │           │  (idle) │      │  014    │          │
        │           └─────────┘      │  Training│          │
        │                            └────┬────┘          │
        │                                 │               │
        │                                 │ Completes     │ Completes
        │                                 │ (18s)         │ (93s)
        │                                 ▼               ▼
        │ Completes                  ┌─────────┐    ┌─────────┐
        │ (96s)                      │ Thread 3│    │ Thread 4│
        ▼                            │  015    │    │  020    │
   ┌─────────┐                       │  OHS    │    │  GHG    │
   │ (idle)  │                       └────┬────┘    └────┬────┘
   └─────────┘                            │              │
                                          │ Completes    │ Completes
                                          │ (38s)        │ (69s)
                                          ▼              ▼
                                     ┌─────────┐    ┌─────────┐
                                     │ (idle)  │    │ (idle)  │
                                     └─────────┘    └─────────┘
                                          │              │
                                          └──────┬───────┘
                                                 │
                                     ┌───────────▼────────────┐
                                     │ All scripts complete    │
                                     │ Total time: ~170s       │
                                     │ (vs ~500s sequential)   │
                                     └─────────────────────────┘
```

---

**Document Version**: 1.0
**Last Updated**: 2026-01-02
**Maintained by**: WifOR Development Team
**Contact**: dimitrij.euler@greenings.org
