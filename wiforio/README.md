# wiforio — Supply-Chain Tier Impact Library for WifORIO

A Python library for computing supply-chain tier impacts from infrastructure
investment using the **WifORIO** Multi-Region Input-Output (MRIO) database,
covering all countries × NACE sectors at full resolution.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Data Sources & Licences](#2-data-sources--licences)
3. [WifORIO MacroFile Structure](#3-wiforio-macrofile-structure)
4. [Model Variants: indirect vs spill](#4-model-variants-indirect-vs-spill)
5. [API Reference](#5-api-reference)
6. [Usage Examples](#6-usage-examples)
7. [Citation](#7-citation)

---

## 1. Overview

**WifORIO** (Wif OR Input-Output) is a global MRIO table constructed by
WifOR Institute based on FIGARO (Eurostat) for the base years 2010–2022,
extended to full global country coverage via a gravity-model approach
("Own Table 2.0"), balanced using the KRAS algorithm, and projected to
2030, 2050, and 2100 under IPCC SSP2 and SSP5 climate scenarios.

This library (`wiforio/`) provides a clean Python API to run supply-chain
tier impact analyses on top of WifORIO MacroFile HDF5 outputs.

| Function | Math | Description |
|---|---|---|
| `tier0_impact()` | `impact₀ = quota · diag(y₀)` | Direct spend only |
| `tier1_impact()` | `y₁ = A·y₀ → quota · diag(y₁)` | First upstream round |
| `tier_impact()` | `yₙ = Aⁿ·y₀` for each tier n | Power-series decomposition |
| `total_impact()` | `y_total = L·y₀ → quota · diag(y_total)` | Exact Leontief total via pre-inverted L |

Key design features:
- **Full MRIO resolution**: ~160 countries × 64 NACE sectors.
- **Trade endogenous**: bilateral trade flows are built into the A matrix.
- **Pre-inverted Leontief**: `total_impact()` uses `L = (I−A)⁻¹` directly —
  exact and fast.
- **Two multiplier types**: "indirect" (Type I, production only) and "spill"
  (Type II, with workforce-consumption feedback).
- **All satellite variables**: `quota` carries dozens of physical and monetary
  impact indicators.

---

## 2. Data Sources & Licences

WifORIO draws on nine external databases. Licence terms vary significantly;
the two most restrictive are IMF WEO and UN Comtrade.

```python
from wiforio import print_license_summary
print_license_summary()
```

### 2.1 FIGARO — Base IO Table

**Provider:** Eurostat / European Commission  
**Licence:** CC BY 4.0  
**Commercial use:** YES  
**Redistribution:** YES  
**URL:** https://ec.europa.eu/eurostat/web/esa-supply-use-input-tables/information-data

FIGARO (Full International and Global Accounts for Research in Input-Output
analysis) is the methodological backbone of WifORIO. It provides the base
industry-by-industry transaction matrix (Z / Tindirect) for 46 regions ×
64 NACE Rev. 2 sectors for years 2010–2022. Satellite accounts (compensation
of employees D1, taxes D21X31, net other taxes D29X39, gross operating
surplus B2A3G) are also extracted from FIGARO.

> **Attribution:** "Source: Eurostat, FIGARO — Full International and Global
> Accounts for Research in Input-Output analysis, 24th edition."

The 46 FIGARO regions are: EU-27 member states, GB, CH, NO, TR, and 14 non-EU
major trading partners (AR, AU, BR, CA, CN, ID, IN, JP, KR, MX, RU, SA,
US, ZA) plus a Rest-of-World aggregate (FIGW1).

**Citation:**  
Eurostat (2024). *FIGARO: Full International and Global Accounts for Research
in Input-Output analysis*, 24th edition. European Commission.
https://ec.europa.eu/eurostat/web/esa-supply-use-input-tables/information-data

---

### 2.2 Eurostat NAIO — National Accounts Constraints

**Provider:** Eurostat / European Commission  
**Licence:** CC BY 4.0  
**Commercial use:** YES  
**Redistribution:** YES  
**URL:** https://ec.europa.eu/eurostat/web/national-accounts/data/database

The NAIO tables (NAIO_10_FCP_II3 for Gross Output; NAIO_10_FCP_II4 for
Intermediate Consumption) provide row and column accounting totals by NACE
sector for EU member states. These are used as hard constraints in the KRAS
balancing procedure to align the FIGARO base table with national accounts.
Coverage: 2010–2024 (EU27 + EEA).

> **Note:** Liechtenstein and some micro-states have additional redistribution
> restrictions; these are either excluded or imputed in WifORIO.

**Citation:**  
Eurostat (2025). *National Accounts Input-Output tables* (NAIO_10_FCP_II3,
NAIO_10_FCP_II4). European Commission.
https://ec.europa.eu/eurostat/web/national-accounts/data/database

---

### 2.3 UN System of National Accounts (SNA)

**Provider:** United Nations Statistics Division (UNSD)  
**Licence:** UN open data (public domain)  
**Commercial use:** YES  
**Redistribution:** YES  
**URL:** https://unstats.un.org/unsd/nationalaccount/data.asp

The UN SNA Main Aggregates Database provides gross output and intermediate
consumption constraints for non-EU / non-OECD countries not covered by
Eurostat NAIO. This is particularly important for LATAM, Sub-Saharan Africa,
and Asia-Pacific countries in the Own Table 2.0 global extension.
Coverage: 2010–2023.

**Citation:**  
United Nations Statistics Division (2025). *National Accounts Main Aggregates
Database*. https://unstats.un.org/unsd/nationalaccount/data.asp

---

### 2.4 IMF World Economic Outlook (WEO)

**Provider:** International Monetary Fund  
**Licence:** IMF Copyright — **RESTRICTED fair use only**  
**Commercial use:** NO ⚠  
**Redistribution:** NO ⚠  
**URL:** https://www.imf.org/en/Publications/WEO  
**Permissions:** copyright@imf.org

> **IMPORTANT:** IMF data is protected by copyright. Fair use is limited to
> excerpts of ≤ 1,000 words or one-quarter of content (whichever is less)
> for **non-commercial purposes only**. Commercial exploitation requires prior
> written permission from the IMF.

IMF WEO (October 2022 edition) provides GDP growth forecasts for ~190
countries in current and constant USD. These growth rates are applied as
factorial constraints in the KRAS balancing for years 2023–2029, bridging
the historical FIGARO data (up to 2022) to the IPCC SSP scenarios
(starting from 2030).

**Citation:**  
International Monetary Fund (2022). *World Economic Outlook Database*,
October 2022. IMF.
https://www.imf.org/en/Publications/WEO/weo-database/2022/October

---

### 2.5 World Bank — GDP & GVA

**Provider:** World Bank Group  
**Licence:** CC BY 4.0  
**Commercial use:** YES  
**Redistribution:** YES  
**URL:** https://databank.worldbank.org/source/world-development-indicators

World Bank WDI series (NY.GDP.MKTP.CD for GDP; sectoral GVA shares) provide
auxiliary constraints for countries with limited national accounts coverage,
and serve as the economic mass variable in the gravity model used for Own
Table 2.0 country extension.

**Citation:**  
World Bank (2025). *World Development Indicators*. The World Bank Group.
https://databank.worldbank.org

---

### 2.6 BACI — Bilateral Trade in Goods

**Provider:** CEPII  
**Licence:** Etalab 2.0 (French open data licence, equivalent to CC BY 4.0)  
**Commercial use:** YES  
**Redistribution:** YES  
**URL:** http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37  
**Contact:** baci@cepii.fr

BACI provides reconciled bilateral trade flows in goods (HS product codes
mapped to NACE via concordance tables), covering 2010–2023. Used to construct
the trade weight matrix TW which distributes import rows across sourcing
countries in the KRAS constraint framework.

**Citation:**  
Gaulier, G. and Zignago, S. (2010). BACI: International Trade Database at
the Product-Level. The 1994-2007 Version. *CEPII Working Paper*, N°2010-23.
http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37

---

### 2.7 UN Comtrade — Bilateral Trade in Services

**Provider:** United Nations Statistics Division  
**Licence:** Proprietary — **NO commercial use; NO redistribution** ⚠  
**Commercial use:** NO ⚠  
**Redistribution:** NO ⚠  
**URL:** https://comtradeplus.un.org/  
**Permissions:** comtrade@un.org

> **IMPORTANT:** UN Comtrade imposes a strict licence agreement. Automated
> downloading, bulk redistribution, and commercial exploitation are strictly
> prohibited without prior written permission.

UN Comtrade services data (BPM6 classification mapped to NACE service sectors
J–N) complements BACI (goods only) for constructing the bilateral trade weight
matrix TW. It covers transport, travel, financial, insurance, ICT, and other
business service flows for 2017–2022.

For commercial applications using WifORIO, either obtain written permission
from comtrade@un.org, or replace with OECD TiVA service trade data (CC BY 4.0).

**Citation:**  
United Nations Statistics Division (2024). *UN Comtrade Database*.
https://comtradeplus.un.org/

---

### 2.8 IPCC AR6 — SSP GDP & Population Scenarios

**Provider:** IPCC / IIASA SSP database  
**Licence:** CC BY 4.0  
**Commercial use:** YES  
**Redistribution:** YES  
**URL:** https://www.ipcc.ch/report/ar6/wg1/resources/data-access/

IPCC AR6 SSP scenarios provide the long-horizon GDP and population
projections used to project WifORIO tables to 2030, 2050, and 2100.

| Scenario | Description | Years |
|---|---|---|
| SSP2 | "Middle of the Road" — moderate growth and challenges | 2030, 2050, 2100 |
| SSP5 | "Fossil-Fuelled Development" — high growth, high emissions | 2030, 2050, 2100 |

**Citations:**  
IPCC (2021). *Sixth Assessment Report — Working Group I. Scenario Data*.
IPCC Data Distribution Centre.
https://www.ipcc.ch/report/ar6/wg1/resources/data-access/

O'Neill, B.C. et al. (2017). The roads ahead: Narratives for shared
socioeconomic pathways describing world futures in the 21st century.
*Global Environmental Change* 42, 169–180.
doi:10.1016/j.gloenvcha.2015.01.004

---

### 2.9 CEPII Gravity Database

**Provider:** CEPII  
**Licence:** Etalab 2.0 (equivalent to CC BY 4.0)  
**Commercial use:** YES  
**Redistribution:** YES  
**URL:** http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8

Bilateral distances, contiguity, common language, colonial ties, and regional
trade agreement indicators. Used in the gravity model that underpins the Own
Table 2.0 global extension.

**Citation:**  
Conte, M., P. Cotterlaz and T. Mayer (2022). The CEPII Gravity database.
*CEPII Working Paper* N°2022-05.
http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8

---

### 2.10 Licence Compliance Summary

| Source | Licence | Commercial | Redistribute |
|---|---|---|---|
| FIGARO | CC BY 4.0 | YES | YES |
| Eurostat NAIO | CC BY 4.0 | YES | YES |
| UN SNA | UN open data | YES | YES |
| IMF WEO | IMF copyright | **NO** ⚠ | **NO** ⚠ |
| World Bank | CC BY 4.0 | YES | YES |
| BACI | Etalab 2.0 | YES | YES |
| UN Comtrade | Proprietary | **NO** ⚠ | **NO** ⚠ |
| IPCC AR6 SSP | CC BY 4.0 | YES | YES |
| CEPII Gravity | Etalab 2.0 | YES | YES |

```python
from wiforio import check_compliance
for w in check_compliance(commercial=True):
    print(w)
```

---

## 3. WifORIO MacroFile Structure

### 3.1 Final MacroFile

**Filename pattern:** `{version}_MacroFile_{year}{scenario}.h5`  
**Location:** `05 FINAL/`

| HDF5 Key | Shape | Description |
|---|---|---|
| `Aspill{year}` | n × n | Technical coefficient matrix, WF-closed |
| `Lindirect{year}` | n × n | Leontief inverse, open model |
| `Lspill{year}` | n × n | Leontief inverse, WF-closed |
| `FD{year}` | n × fd | Final demand (GOV, HH, NPISH, GFCF, INVEN) |
| `SR{year}` | — | Supply ratios |
| `TW{year}` | — | Trade weights (bilateral import shares) |
| `variables{year}` | vars × n | Satellite account absolute values |
| `quota{year}` | vars × n | Satellite intensities per unit GOspill |
| `Variables2Name` | vars | Code → human-readable name mapping |
| `info` | 7 | Metadata: date, author, IOTunit, year, scenario |

> **Note:** `Aindirect{year}` is not stored in the final MacroFile.
> Use `model="spill"` with the final MacroFile, or pass the closed-model H5
> path for `model="indirect"` tier functions.

### 3.2 Closed Model File (intermediate)

**Filename pattern:** `{version}_Result_{year}{scenario}_closed.h5`  
**Location:** `03 Constraints/Result/`

Contains `Aindirect`, `Aspill`, `Lindirect`, `Lspill` with **no year suffix**.
The library's `_load()` function handles both key conventions automatically.

### 3.3 MultiIndex Structure

All matrices use a two-level MultiIndex: **(GeoRegion, NACE)**

**GeoRegion codes:**
- FIGARO core (46): ISO-2 — EU-27, plus GB, CH, NO, TR, AR, AU, BR, CA, CN,
  ID, IN, JP, KR, MX, RU, SA, US, ZA, and FIGW1 (Rest-of-World).
- Own Table 2.0 extension: additional ISO-3 codes for global coverage.
- Special: `WF` = Workforce account (WF-closed model only).

Use `list_countries()` to see all available codes in a MacroFile.

**NACE codes** (64 sectors, Eurostat FIGARO notation):

| Sector | Representative NACE codes |
|---|---|
| Agriculture | A01, A02, A03 |
| Mining & quarrying | B |
| Manufacturing | C10-12 … C33 (20 sub-sectors) |
| Utilities (energy) | D35 |
| Utilities (water/waste) | E36, E37-39 |
| Construction | F |
| Trade & transport | G45–G47, H49–H53 |
| ICT & finance | I, J58–J63, K64–K66, L |
| Professional services | M69_70–M74_75, N77–N82 |
| Public & social | O84, P85, Q86, Q87_88, R90–R93, S94–S96, T, U |

NACE notation: hyphens for ranges (`C10-12`, `E37-39`); underscores for
paired codes (`C31_32`, `Q87_88`).

### 3.4 Satellite Variables

`quota` rows are satellite variable codes. Common ones:

| Code | Description |
|---|---|
| `GOspill` | Gross output (WF-closed) |
| `GOindirect` | Gross output (open) |
| `GVA` | Gross value added |
| `IC` | Intermediate consumption |
| `LAB` | Labour (persons or FTE) |
| `COMP` | Compensation of employees |
| `TXSP` | Taxes less subsidies on products |
| `OSM` | Gross operating surplus |

```python
from wiforio import list_variables
vars_df = list_variables("path/to/MacroFile.h5", year="2050")
print(vars_df[vars_df["in_quota"]])
```

### 3.5 Scenarios and Years

| Year | Type | Scenarios |
|---|---|---|
| 2010–2022 | Historical | (none — FIGARO base) |
| 2030 | Scenario | SSP2, SSP5 |
| 2050 | Scenario | SSP2, SSP5 |
| 2100 | Scenario | SSP2, SSP5 |

---

## 4. Model Variants: indirect vs spill

| | `model="indirect"` | `model="spill"` (default) |
|---|---|---|
| **Name** | Open Leontief (Type I) | WF-closed / spill (Type II) |
| **Matrices** | Aindirect, Lindirect | Aspill, Lspill |
| **Captures** | Production supply chain only | Production + household consumption feedback |
| **Mechanism** | CAPEX → upstream procurement chain | + wages → household spending → further output |
| **Multiplier** | 1.0× (reference) | Typically 1.5–2.5× for labour-intensive sectors |
| **Use case** | Environmental footprinting | Full economic impact (GVA, employment, income) |
| **A in MacroFile** | Not stored ⚠ | `Aspill{year}` available |
| **L in MacroFile** | `Lindirect{year}` available | `Lspill{year}` available |

**When to use "indirect":**
Use for environmental footprinting (GHG, water, waste) where induced
consumption effects should not be attributed to the project.

**When to use "spill":**
Use for socio-economic impact assessment (employment, GVA, income) where the
full multiplier effect — including wages spent in the local economy — is
the relevant measure.

---

## 5. API Reference

### Impact functions

#### `tier0_impact(y0, macrofile_path, year, model="spill")`
Direct spend impact. No supply-chain propagation.

**Returns:** `dict` — `tier`, `model`, `year`, `invest_M$`, `total` (dict),
`by_sector` (DataFrame: variables × (GeoRegion, NACE)),
`by_region` (DataFrame: variables × GeoRegion).

#### `tier1_impact(y0, macrofile_path, year, model="spill")`
First upstream round. For `model="indirect"` pass the closed-model H5.

**Returns:** same structure with `"tier": 1`.

#### `tier_impact(y0, macrofile_path, year, tier_from=0, tier_to=6, model="spill")`
Power-series decomposition, tier by tier.

**Returns:** `pd.DataFrame` shape `(n_tiers, n_variables)`, index = `"tier"`.

> For full WifORIO (n ≈ 10 000), each A multiplication takes 0.1–0.5 s.
> Use `total_impact()` when only the aggregate is needed.

#### `total_impact(y0, macrofile_path, year, model="spill")`
Exact Leontief total using pre-inverted L. Recommended for production use.

**Returns:** same structure as `tier0_impact()` with `"tier": None`.

#### `compare_models(y0, macrofile_path, year, variables=None)`
Run `total_impact()` for both models.

**Returns:** `pd.DataFrame` with columns
`["indirect", "spill", "ratio_spill_indirect"]`.

---

### Spend-vector helpers

#### `make_project_spend_vector(invest_usd, project_type, country, index)`

```python
project_type  # "Rail_Dev" | "Rail_Op" | "Energy" |
              # "Health_Social" | "Health_Specialized" | "Health_General"
country       # GeoRegion code (e.g. "DE", "BR", "ZA")
index         # MacroFile MultiIndex from pd.read_hdf(..., key="Aspill2050").index
```

#### `make_spend_vector(invest_usd, alloc, country, index)`
Generic version accepting any `{nace_code: share}` dict.

#### `aggregate_to_sectors8(series_or_df, axis=0)`
Aggregate NACE-level results to 8 broad sector buckets
(Construction, Energy_Utilities, Manufacturing, Transport_Logistics,
Health_Social, Agriculture, Mining_Extraction, Water_Waste).

#### `NACE_ALLOC`
Dict of project-type → `{nace_code: share}` (all shares sum to 1.0).

---

### Utility functions

| Function | Returns |
|---|---|
| `list_variables(macrofile_path, year)` | DataFrame: codes, names, in_quota flag |
| `list_countries(macrofile_path, year, model)` | Sorted list of GeoRegion codes |
| `list_nace_codes(macrofile_path, year, country, model)` | Sorted list of NACE codes |
| `load_macrofile_info(macrofile_path)` | Metadata Series from 'info' key |
| `clear_cache()` | Releases cached matrices from memory |

---

## 6. Usage Examples

### Basic: total Leontief impact of a rail project

```python
import pandas as pd
from wiforio import make_project_spend_vector, total_impact

MACROFILE = "05 FINAL/20250923_MacroFile_2050_SSP5.h5"
YEAR      = "2050"

A_ref = pd.read_hdf(MACROFILE, key=f"Aspill{YEAR}")

y0 = make_project_spend_vector(
    invest_usd   = 1_850_000_000 * 1.09,   # EUR → USD
    project_type = "Rail_Dev",
    country      = "DE",
    index        = A_ref.index,
)

result = total_impact(y0, MACROFILE, YEAR, model="spill")

for var, val in result["total"].items():
    print(f"  {var:<25}: {val:>15,.1f}")

print(result["by_region"].T.head())
```

### Tier-by-tier decomposition

```python
from wiforio import tier_impact

tiers_df = tier_impact(y0, MACROFILE, YEAR, tier_from=0, tier_to=6)
print(tiers_df[["LAB", "GVA", "COMP"]])
```

### Comparing model variants

```python
from wiforio import compare_models

cmp = compare_models(y0, MACROFILE, YEAR, variables=["LAB", "GVA", "COMP"])
print(cmp)
```

### Custom NACE allocation (solar farm)

```python
from wiforio import make_spend_vector, tier0_impact

SOLAR_NACE = {
    "F":      0.32,
    "C27":    0.28,
    "C28":    0.12,
    "D35":    0.08,
    "H49":    0.10,
    "B":      0.06,
    "E37-39": 0.04,
}

y0_solar = make_spend_vector(500_000_000, SOLAR_NACE, "BR", A_ref.index)
result0  = tier0_impact(y0_solar, MACROFILE, YEAR)
print(result0["total"])
```

### Aggregating results to broad sector buckets

```python
from wiforio import aggregate_to_sectors8, total_impact

result      = total_impact(y0, MACROFILE, YEAR)
by_sector8  = aggregate_to_sectors8(result["by_sector"], axis=1)
print(by_sector8[["LAB", "GVA"]].T)
```

### Checking data source licences

```python
from wiforio import print_license_summary, check_compliance, get_citation

print_license_summary()

for w in check_compliance(commercial=True):
    print("⚠ ", w)

print(get_citation("baci"))
```

---

## 7. Citation

When publishing results based on this library and the WifORIO database, cite:

**WifORIO database:**
> Croner, D. and Pertermann, F. (WifOR Institute). *WifORIO: WifOR
> Multi-Region Input-Output database, Own Table 2.0*, version 20250923.
> Based on Eurostat FIGARO 24th edition.

**This library:**
> Euler, D., Croner, D. and Pertermann, F. (WifOR Institute). *wiforio:
> Supply-Chain Tier Impact Library for WifORIO*. Version 0.1.0. 2025.

**Required data source citations:** see Section 2 above.

```python
from wiforio import all_citations
print(all_citations())
```
