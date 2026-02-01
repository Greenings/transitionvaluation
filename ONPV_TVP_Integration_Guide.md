# ONPV and Transition Valuation Project Integration Guide

This document maps the four ONPV differentiation steps to the existing Transition Valuation Project (TVP) infrastructure and recommends integration approaches.

---

## 1. Overview: Mapping ONPV to TVP

| ONPV Step | TVP Coverage | Integration Status |
|:---|:---|:---|
| **Step 1: Value Factors** | Fully covered by `value-factors/` scripts | **Strong** - Direct integration |
| **Step 2: Exposure Factors** | Partially covered (sector/country structure) | **Medium** - Extension needed |
| **Step 3: Vulnerability Factors** | Not covered | **Gap** - New module required |
| **Step 4: Attribution Factors** | Not covered | **Gap** - New module required |

---

## 2. Step 1: Value Factors - Full Integration

### TVP Assets Available

The `value-factors/` folder provides complete infrastructure for Step 1:

| TVP Component | ONPV Use | Location |
|:---|:---|:---|
| GHG Emissions coefficients | Social Cost of Carbon | `020_241024_prepare_GHG_my.py` |
| Air Pollution coefficients | PM2.5, NOx, SO2, etc. | `008_241001_prepare_AirPollution_my.py` |
| Water Consumption | AWARE-based scarcity costs | `009_241001_prepare_WaterConsumption_my.py` |
| Water Pollution | N, P, heavy metals | `013_241014_prepare_WaterPol_my.py` |
| Waste Management | Hazardous/non-hazardous | `007_241001_prepare_Waste_my.py` |
| Land Use | EPS-based ecosystem costs | `010_241001_prepare_LandUse_my.py` |
| OHS | DALY-based injury costs | `015_241016_prepare_OHS_my.py` |
| Training | Positive human capital | `014_241016_prepare_Training_my.py` |

### Integration Recommendation

**Direct Usage:** The Step 1 methodology documents should reference TVP value-factors directly:

```
Step1_Value_Factors_Methodology.md
          │
          ▼
value-factors/
├── output/GHG.h5           → GHG coefficients (DICE 2023)
├── output/AirPollution.h5  → Air pollution (UBA methodology)
├── output/WaterConsumption.h5
├── output/WaterPollution.h5
├── output/Waste.h5
├── output/LandUse.h5
├── output/OHS.h5
└── output/Training.h5
```

### Key Parameters from TVP

| Parameter | TVP Value | Source |
|:---|:---|:---|
| Social Discount Rate | 1.5% | WifOR methodology |
| VSL per DALY | $200,000 | Global estimate |
| Base Year | 2020 USD | Inflation-adjusted |
| Country Coverage | 188 countries | Model definitions |
| Sector Coverage | NACE classification | Model definitions |
| Year Range | 2014-2030, 2050, 2100 | Projection |

### Update Step 1 Document

Add to `Step1_Value_Factors_Methodology.md`:

```markdown
## TVP Value Factors Integration

The ONPV Step 1 coefficients are sourced directly from the Transition Valuation
Project value-factors module. See `value-factors/` for:

- **Scripts**: 8 Python scripts generating coefficients
- **Methodology**: `METHODOLOGY.md`
- **Data Dictionary**: `value-factors/DATA_DICTIONARY.md`
- **Input Provenance**: `INPUT_FILES_METHODOLOGY.md`

### Using TVP Outputs

Load coefficients from HDF5 files:
```python
import pandas as pd
ghg_coeff = pd.read_hdf('value-factors/output/GHG.h5', 'coefficients')
```
```

---

## 3. Step 2: Exposure Factors - Extension Needed

### TVP Assets Partially Available

| TVP Component | ONPV Use | Availability |
|:---|:---|:---|
| NACE sector structure | Sector dependency mapping | Available in Model definitions |
| 188 country list | Regional adjustments | Available in Model definitions |
| Sector-specific coefficients | Sector materiality weighting | Available for some indicators |

### Gap Analysis

TVP provides the **structural foundation** but not the **exposure scoring** methodology:

| Exposure Component | TVP Status | Integration Approach |
|:---|:---|:---|
| Natural Capital (ENCORE) | Not in TVP | External data + new module |
| Human Capital (SASB) | Partial (OHS, Training indicators) | Extend with SASB mapping |
| Social Capital | Not in TVP | New module required |
| Built Capital | Not in TVP | Financial data integration |

### Recommended New Module

Create `exposure-factors/` with:

```
exposure-factors/
├── README.md
├── 001_prepare_NaturalCapital_ENCORE.py
├── 002_prepare_HumanCapital_SASB.py
├── 003_prepare_SocialCapital.py
├── 004_prepare_BuiltCapital.py
├── config.yaml
├── exposure_factor_utils.py
└── input_data/
    ├── ENCORE_sector_mapping.xlsx
    ├── SASB_industry_materiality.xlsx
    └── Regional_infrastructure_indices.xlsx
```

### Integration with TVP NACE Structure

Leverage TVP's Model definitions for sector mapping:

```python
# Use TVP country/sector structure
from value_factors import load_common_data
countries, nace_sectors, _ = load_common_data()

# Map ENCORE sectors to TVP NACE sectors
encore_to_nace = {
    'Crops': ['A01'],
    'Food, Beverage & Tobacco': ['C10', 'C11', 'C12'],
    # ... etc
}

# Calculate exposure scores per TVP structure
exposure_df = pd.DataFrame(
    index=pd.MultiIndex.from_product([countries, nace_sectors]),
    columns=['Natural', 'Human', 'Social', 'Built']
)
```

---

## 4. Step 3: Vulnerability Factors - New Module Required

### TVP Assets Available

| TVP Component | Potential ONPV Use |
|:---|:---|
| Country list (188) | Country-level vulnerability scoring |
| NACE sectors | Sector pathway assessment |
| Double materiality framework | Transition risk context |

### Gap Analysis

TVP focuses on **impact valuation** (inside-out), not **transition readiness** assessment:

| Vulnerability Component | TVP Status | Integration Approach |
|:---|:---|:---|
| Country-Level Policy | Not in TVP | External data (CAT, IEA) |
| Sector Pathways | Not in TVP | External data (IEA, MPP) |
| Management Scorecard (QMS) | Not in TVP | New methodology |
| Just Transition Readiness | Not in TVP | MDB principles integration |

### Recommended New Module

Create `vulnerability-factors/` with:

```
vulnerability-factors/
├── README.md
├── 001_prepare_CountryVulnerability.py
├── 002_prepare_SectorVulnerability.py
├── 003_prepare_ManagementScorecard.py
├── 004_calculate_CompositeVulnerability.py
├── config.yaml
├── vulnerability_utils.py
└── input_data/
    ├── CAT_country_ratings.xlsx
    ├── IEA_sector_pathways.xlsx
    ├── SBTi_company_database.xlsx
    └── CDP_disclosure_scores.xlsx
```

### Link to TVP Double Materiality

TVP's double materiality framework provides context:

```
TVP Value Factors (Step 1)          Vulnerability (Step 3)
        │                                    │
        │                                    │
        ▼                                    ▼
┌─────────────────┐               ┌─────────────────┐
│ Impact          │               │ Transition      │
│ Materiality     │     links     │ Readiness       │
│ (inside-out)    │ ◄──────────► │ Assessment      │
└─────────────────┘               └─────────────────┘
        │                                    │
        │                                    │
        ▼                                    ▼
"What damage does              "How prepared is the
the company cause?"             company for change?"
```

---

## 5. Step 4: Attribution Factors - New Module Required

### TVP Assets Available

TVP does not currently address investor attribution, but the **use case framework** in `README.md` provides context:

| TVP Use Case | ONPV Attribution Relevance |
|:---|:---|
| Investment Decision-Making | Requires attribution to investor |
| Engagement | Implies control/influence dynamic |
| Risk Management (Transition Risk) | Attribution affects risk allocation |

### Gap Analysis

| Attribution Component | TVP Status | Integration Approach |
|:---|:---|:---|
| Equity Control Tiers | Not in TVP | Financial data + PCAF alignment |
| Debt Covenant Scoring | Not in TVP | Bond prospectus analysis |
| Distress Multiplier | Not in TVP | Z-Score calculation |
| Instrument Type Adjustment | Not in TVP | MDB methodology integration |

### Recommended New Module

Create `attribution-factors/` with:

```
attribution-factors/
├── README.md
├── 001_calculate_EquityAttribution.py
├── 002_calculate_DebtAttribution.py
├── 003_calculate_DistressMultiplier.py
├── 004_apply_PortfolioAttribution.py
├── config.yaml
├── attribution_utils.py
└── input_data/
    ├── ownership_positions.xlsx
    ├── debt_covenant_terms.xlsx
    └── financial_health_metrics.xlsx
```

### Link to TVP Impact Calculation

Attribution sits at the end of the TVP value chain:

```
TVP Value Factors     ONPV Differentiation      Attributed Impact
(Societal Damage)     (Exposure × Vulnerability)  (Investor Share)
        │                      │                        │
        ▼                      ▼                        ▼
   -$100M GHG          ×0.7 Exposure Factor      ×10% Attribution
                       ×(1-0.3) Vulnerability

        └──────────────────────┬────────────────────────┘
                               │
                               ▼
                    Differentiated Attributed Impact
                         = -$100M × 0.7 × 0.7 × 0.1
                         = -$4.9M to this investor
```

---

## 6. Implementation Roadmap

### Phase 1: Integrate Step 1 (Immediate)

**Actions:**
1. Update `Step1_Value_Factors_Methodology.md` to reference TVP value-factors
2. Document coefficient loading from TVP HDF5 outputs
3. Align coefficient tables with TVP output structure
4. Validate consistency between ONPV parameters and TVP methodology

**Effort:** Low (documentation update only)

### Phase 2: Build Step 2 Module (Short-term)

**Actions:**
1. Create `exposure-factors/` folder structure
2. Build ENCORE → NACE sector mapping
3. Develop SASB materiality integration
4. Implement four-capital scoring methodology

**Effort:** Medium (new Python scripts required)

### Phase 3: Build Step 3 Module (Medium-term)

**Actions:**
1. Create `vulnerability-factors/` folder structure
2. Integrate external data sources (CAT, SBTi, CDP)
3. Implement Quantified Management Scorecard
4. Add Just Transition Readiness scoring (MDB principles)

**Effort:** Medium-High (external data integration)

### Phase 4: Build Step 4 Module (Medium-term)

**Actions:**
1. Create `attribution-factors/` folder structure
2. Implement tiered equity attribution
3. Build debt attribution with distress multiplier
4. Create portfolio aggregation tools

**Effort:** Medium (financial data structures)

---

## 7. Updated TVP Repository Structure

After integration, the TVP repository would be structured as:

```
transitionvaluation/
├── README.md                         # Updated with ONPV overview
├── METHODOLOGY.md                    # Existing (Step 1 focus)
├── ONPV_METHODOLOGY.md               # NEW: Full 4-step methodology
│
├── value-factors/                    # STEP 1: Existing
│   ├── scripts (8)
│   ├── output/
│   └── input_data/
│
├── exposure-factors/                 # STEP 2: NEW
│   ├── scripts
│   ├── output/
│   └── input_data/
│
├── vulnerability-factors/            # STEP 3: NEW
│   ├── scripts
│   ├── output/
│   └── input_data/
│
├── attribution-factors/              # STEP 4: NEW
│   ├── scripts
│   ├── output/
│   └── input_data/
│
├── integration/                      # NEW: End-to-end calculation
│   ├── calculate_differentiated_impact.py
│   ├── portfolio_aggregation.py
│   └── reporting/
│
└── documentation/
    ├── Step1_Value_Factors_Methodology.md
    ├── Step2_Exposure_Methodology.md
    ├── Step3_Vulnerability_Methodology.md
    ├── Step4_Attribution_Methodology.md
    └── MDB_Sources_Integration_Guide.md
```

---

## 8. Key Integration Points

### 8.1 Shared Data Structures

All modules should use TVP's existing Model definitions:

```python
# Standard import across all modules
from common import load_model_definitions
countries, nace_sectors = load_model_definitions()
```

### 8.2 Consistent Output Format

All new modules should follow TVP's HDF5/Excel output pattern:

```python
# Standard output for all steps
save_results(
    data_df=result_df,
    output_h5=f'output/{date}_{step}_coefficients.h5',
    output_excel=f'output/{date}_{step}_coefficients.xlsx'
)
```

### 8.3 Configuration Management

Extend TVP's `config.yaml` pattern:

```yaml
# config.yaml additions
exposure_factors:
  encore_mapping: input_data/ENCORE_sector_mapping.xlsx
  sasb_materiality: input_data/SASB_industry_materiality.xlsx
  weights:
    natural: 0.40
    human: 0.25
    social: 0.15
    built: 0.20

vulnerability_factors:
  cat_data: input_data/CAT_country_ratings.xlsx
  sbti_database: input_data/SBTi_company_database.xlsx
  qms_weights:
    target_ambition: 0.30
    disclosure_quality: 0.25
    track_record: 0.25
    just_transition: 0.20

attribution_factors:
  equity_tiers:
    controlling: 1.5
    influential: 1.2
    minority: 1.0
  debt_base_rates:
    investment_grade: 0.15
    high_yield: 0.25
```

---

## 9. Summary

| ONPV Step | TVP Status | Action Required |
|:---|:---|:---|
| **Step 1** | Fully implemented | Document linkage |
| **Step 2** | Structure available | Build new module |
| **Step 3** | Not implemented | Build new module |
| **Step 4** | Not implemented | Build new module |

The Transition Valuation Project provides an excellent foundation for ONPV implementation, particularly for Step 1 (Value Factors). The infrastructure (country/sector structure, HDF5 outputs, configuration management) can be extended to support Steps 2-4 with new modules following the same patterns.

---

*Document Version: 1.0 | Date: 2026-02-01*
