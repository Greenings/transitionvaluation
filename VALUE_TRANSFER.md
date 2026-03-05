# Value Transfer Description — UBA Value Factors

**Handbook on Environmental Value Factors, MC 4.0 (December 2025)**

---

## Overview

### What is value transfer?

Value transfer is the process of adapting an environmental monetary value estimated
in one geographic or economic context (the **study site**) to another context
(the **policy site**). For this dataset the UBA MC 4.0 handbook provides
Germany-specific or global values in EUR_2025. The transitionvaluation framework
requires country-differentiated coefficient matrices of shape
`C[year, indicator, country, sector]` covering 188 countries and 19 or 21
NACE sectors.

This document describes, for each of the 10 UBA table groups, how the
Germany-specific base value can be transferred to the full country matrix
using one of three recognised approaches:

| Approach | Abbreviation | Description |
|---|---|---|
| **Unit value transfer** | UVT | Apply the German base value directly, adjusted only for price level (PPP or market rate) and income |
| **Value function transfer** | VFT | Apply an empirical WTP-income elasticity function to rescale the German value by GDP per capita |
| **Parameter transfer** | PT | Re-derive the value using country-specific physical parameters (population density, water scarcity, energy mix) with the same dose-response function |

### General coefficient formula (WifOR convention)

```
C[y, i, c, s] = Sign(i) × D[i, c] × I_USD[y]

where:
  y           = year in {2014..2030, 2050, 2100}
  i           = indicator (UBA table group key)
  c           = country ISO3 code (188 countries)
  s           = NACE A21 sector (uniform for most indicators; see exceptions below)
  Sign(i)     = −1.0 for damage costs;  +1.0 for benefits
  D[i, c]     = country-specific base damage/benefit value in USD (after value transfer)
  I_USD[y]    = USA GDP deflator[y] / USA GDP deflator[base_year]
```

**Currency conversion:** UBA values are in EUR_2025. Convert to USD using the
average EUR/USD exchange rate for 2025 (approximately 1.07) before applying the
value transfer adjustments. All output coefficients should be in USD for
compatibility with the WifOR `C[y,i,c,s]` convention.

---

## Indicator 01 — Greenhouse Gas Emissions (`ghg`)

**UBA source:** Table 1, GIVE model (Anthoff 2025), equity-weighted with German
income as reference

**UBA scope:** Year-specific social cost per tonne CO₂/CO₂-eq / CH₄ / N₂O in
EUR_2025, two PRTP scenarios (0 % and 1 %)

**Value transfer approach: Unit Value Transfer (UVT) — minimal adjustment needed**

GHG climate damage is intrinsically global: one tonne of CO₂ emitted anywhere
causes the same global warming. The GIVE model produces a global social cost;
the UBA equity-weighting uses German income only as a reference scale for
intranational equity — the underlying damage is not Germany-specific.

### Transfer formula

```
D[ghg, c]  =  UBA_VF[gas, emission_year, PRTP]  ×  EUR_USD_2025

Notes:
  - D is uniform across all countries (same value for c = DEU, CHN, BRA, …)
  - No PPP or income adjustment needed (global damage, not local WTP)
  - Separate D per (gas, emission_year, PRTP_scenario)
```

### Coefficient matrix

| Dimension | Treatment |
|---|---|
| Year | Apply USA GDP deflator from base year 2025 |
| Country | Uniform across all 188 countries |
| Sector | Uniform (GHG is emitted by all sectors equally per tonne) |
| Sign | −1.0 for CO₂, CH₄, N₂O |

### Implementation steps

1. Convert EUR_2025 → USD_2025 (× 1.07).
2. Expand: broadcast D[gas, emission_year, PRTP] across all 188 countries and
   all NACE sectors.
3. Apply USA GDP deflator row by row for years 2014–2030, 2050, 2100.
4. Output: one coefficient matrix per PRTP scenario, or add PRTP as a second
   `Variable` level in the MultiIndex alongside gas name.

---

## Indicator 02 — Air Pollutant Emissions (`air_pollutants`)

**UBA source:** Tables 2–4, EcoSenseWeb v1.3, German population and
receptor data; Chen and Hoek (2020) dose-response functions

**UBA scope:** Health + crop + material damage per tonne emitted in Germany,
differentiated by source type and surroundings

**Value transfer approach: Value Function Transfer (VFT) + Parameter Transfer (PT)**

Air pollutant health damage depends on (a) the monetary value of a life-year or
DALY (income-elastic) and (b) the population exposed per unit of emission
(physical, country-specific). Both require explicit adjustment.

### Transfer formula

```
D[AP_substance, c]
  =  UBA_VF[substance, Table2_health_component]
     × (GDP_pc[c] / GDP_pc[DEU])^ε_health          ← income elasticity for health WTP
     × (POP_density[c] / POP_density[DEU])^α_pop   ← population exposure scaling
     × EUR_USD_2025

where:
  ε_health  ≈ 0.8–1.0  (income elasticity of WTP for health, standard range in literature)
  α_pop     ≈ 1.0       (linear population exposure for uniformly mixed pollutants)

  Note: crop and material components are not income-elastic and do not require
  income adjustment (use UVT with EUR/USD conversion only for those components).
```

### Special case — Road traffic (Table 4, urban surroundings)

Urban PM₂.₅ values (e.g. 511,600 EUR/t for urban exposure) are particularly
high because they reflect dense German urban population. For countries with
lower urban population density, scale by the country's average urban population
density relative to Germany's.

### Coefficient matrix

| Dimension | Treatment |
|---|---|
| Country | Differentiated via income elasticity + population density |
| Sector | Possible differentiation: transport emissions use Table 4 values; stationary combustion uses Table 3; unknown source uses Table 2 |
| Sign | −1.0 for all components |

---

## Indicator 03 — Electric Power Generation (`electricity`)

**UBA source:** Table 5, full life-cycle value factors per kWh by energy source

**UBA scope:** Germany-specific; reflects the German electricity supply chain,
grid losses, and German population receptor data

**Value transfer approach: Parameter Transfer (PT) — country energy mix required**

The electricity value factor for a country depends on its energy mix.
Germany's mix cannot be applied globally. Instead, compute a weighted average
value factor per kWh for each country using country-specific generation shares.

### Transfer formula

```
D[electricity, c]
  =  Σ_{source s} share[s, c]
       × D_AP[source, c]           ← air pollutant component (value-transferred per indicator 02)
       × (1 + GHG_share[source])   ← GHG component from indicator 01

where:
  share[s, c]  = country c's electricity generation share for source s
                 (IEA World Energy Balances or Ember electricity data)
  D_AP[source, c]  = air pollutant damage for source s in country c
                     (transferred as per indicator 02)
  GHG_share    = GHG intensity per kWh by source (from IPCC AR6 lifecycle GHG)

Unit:  EUR-cent_2025/kWh_el  →  USD/kWh after conversion
```

### Simplified proxy (if country energy-mix data unavailable)

Use the IEA regional average emission intensity (kg CO₂e/kWh) to scale the
German value proportionally:

```
D[electricity, c]  ≈  D[German_mix, DEU]
                        × (emission_intensity[c] / emission_intensity[DEU])
                        × EUR_USD_2025
```

### Coefficient matrix

| Dimension | Treatment |
|---|---|
| Country | Differentiated by energy mix and air pollutant transfer |
| Sector | Uniform (electricity as an input commodity) |
| Sign | −1.0 |

---

## Indicator 04 — Heat Generation (`heat`)

**UBA source:** Table 6, value factors per kWh final energy by heat source

**Value transfer approach: Parameter Transfer (PT) — same logic as electricity**

Heat generation mix and building stock vary by country. Apply the same
country-energy-mix approach as for electricity, using national statistics on
residential and district heating fuel use (Eurostat, IEA).

### Transfer formula

```
D[heat, c]
  =  Σ_{source s} share_heat[s, c]
       × VF[source, c]    ← air pollutant component value-transferred
       × EUR_USD_2025
```

For countries where district heating predominates (Nordic countries, Russia),
the district heating row from Table 6 may be used directly with income-elasticity
adjustment for the health component.

---

## Indicator 05 — Refrigerants (`refrigerants`)

**UBA source:** Table 7, GWP100-based value factors per kg refrigerant lost

**Value transfer approach: Unit Value Transfer (UVT) — derives from global GHG value**

Refrigerant value factors are derived mechanically from GWP100 values and the
CO₂ social cost (indicator 01). Because CO₂ damage is global (see indicator 01),
the refrigerant value factors are also globally uniform.

### Transfer formula

```
D[refrigerant r, c]
  =  GWP100[r]  ×  D[CO2, emission_year=2025, PRTP]  ×  EUR_USD_2025

  =  GWP100[r]  ×  UBA_VF[CO2, 2025, PRTP]  ×  EUR_USD_2025

  Uniform across all countries (same as GHG indicator).
```

---

## Indicator 06 — Passenger and Freight Transport — per vehicle km (`transport_vehkm`)

**UBA source:** Tables 9–16, five-component value factors per vehicle-km by
route type (all routes / motorway / rural / urban), vehicle type, and PRTP

**UBA scope:** Germany-specific (German road network, vehicle fleet standards,
German population along routes)

**Value transfer approach: Component-wise VFT + PT**

The five cost components require different transfer methods:

| Component | Transfer method |
|---|---|
| `ghg` | Global (as indicator 01) — no country adjustment |
| `air_pollutants_exhaust` | VFT: income elasticity + population density (as indicator 02) |
| `air_pollutants_abrasion` | VFT: same as exhaust but using road-traffic Table 4 values |
| `infra_and_vehicles` | UVT + PPP: infrastructure and vehicle costs scale with local price levels |
| `energy_supply` | PT: depends on country electricity/fuel mix and upstream emissions |

### Transfer formula (per vehicle-km)

```
D[vehkm, vehicle, route, c]
  =  VF_ghg[vehicle, route]  ×  EUR_USD_2025                        ← global
   + VF_ap[vehicle, route]   × (GDP_pc[c]/GDP_pc[DEU])^ε            ← health-elastic
                              × (POP_dens_route[c]/POP_dens_DEU)    ← exposure
   + VF_infra[vehicle, route] × (PPP[c]/PPP[DEU])                   ← price-elastic
   + VF_energy[vehicle, route] × (emission_int[c]/emission_int[DEU])← mix-elastic
```

**Note on route types:** Urban values (Table 15/16) require country-specific
urban population density along roads. If not available, use the `all_routes`
values (Table 9/10) as the default transfer base.

---

## Indicator 07 — Passenger and Freight Transport — per Pkm or tkm (`transport_pkm_tkm`)

**UBA source:** Tables 17–18, occupation/utilization rates and total VF per
passenger-km or tonne-km

**Value transfer approach: Derived from indicator 06 + country occupation rates**

Per-Pkm/tkm factors are vehicle-km factors divided by occupation or load rates.
These rates vary by country (e.g. higher car occupancy in developing countries).

### Transfer formula

```
D[Pkm, vehicle, c]  =  D[vehkm, vehicle, c]  /  occupancy_rate[vehicle, c]

where occupancy_rate[vehicle, c] comes from national transport statistics
(Eurostat, ITF, national travel surveys).
```

If country-specific occupancy rates are unavailable, use the German rates from
Table 17 as a fallback (conservative proxy for OECD countries; likely
underestimates per-km damage in countries with higher vehicle utilization).

---

## Indicator 08 — Traffic Noise (`noise`)

**UBA source:** Tables 19–20, annoyance and cognitive-impairment value factors
per person per year by dB(A) class and transport mode

**UBA scope:** Germany-specific WTP (contingent valuation studies, German income
base); exposure function derived from European WHO guidelines

**Value transfer approach: Value Function Transfer (VFT)**

Noise annoyance WTP is strongly income-elastic. The noise exposure–response
function (WHO ERF, Guski et al. 2017) is treated as universal; only the
monetary per-DALY value is transferred.

### Transfer formula

```
D[noise, dBclass, mode, c]
  =  UBA_VF[noise, dBclass, mode]
     × (GDP_pc[c] / GDP_pc[DEU])^ε_noise
     × EUR_USD_2025

where:
  ε_noise  ≈ 0.8  (income elasticity for noise annoyance WTP,
                    based on meta-analyses by Navrud 2002; Dekkers & van der Straaten 2009)
```

**Per-person-year to per-vehicle-km conversion:**

To integrate with the transport indicator, multiply by estimated noise-exposed
population per vehicle-km. This requires country-level road network density and
population along road corridors (available from OpenStreetMap / Global Urban
Network datasets).

---

## Indicator 09 — Nitrogen and Phosphorus Emissions (`nitrogen_phosphorus`)

**UBA source:** Tables 22–24, value factors per kg N or P emitted to air or water

**UBA scope:** Germany-specific; limiting-substance assumption applied to
German water bodies (mesotrophic inland waters, German coastal waters)

**Value transfer approach: Parameter Transfer (PT) — water scarcity and
eutrophication sensitivity differ substantially by country**

### Transfer formula

#### Air emissions (N, Table 22)

NOₓ and NH₃ air emission values (per kg N) derive from health damage — transfer
as per indicator 02 (income-elastic, population-density scaled):

```
D[NOx_air, c]  =  UBA_VF[NOx, air]
                   × (GDP_pc[c] / GDP_pc[DEU])^ε_health
                   × (POP_density[c] / POP_density[DEU])
                   × EUR_USD_2025
```

#### Water emissions (N, P — Tables 23–24)

Eutrophication damage scales with:
(a) **water scarcity**: scarcer water = higher damage per kg nutrient (AWARE factors)
(b) **ecosystem sensitivity**: nutrient thresholds vary by water body type
(c) **WTP for aquatic ecosystem quality**: income-elastic

```
D[N_water, c]  =  UBA_VF[N, inland_waters]
                   × AWARE[c]                      ← water scarcity factor (0.1–100)
                   × (GDP_pc[c] / GDP_pc[DEU])^ε_eco
                   × EUR_USD_2025

ε_eco  ≈ 0.4–0.6  (lower elasticity than health; based on biodiversity WTP literature)
```

The limiting-substance correction (N vs P limiting) should be re-evaluated
per country using national eutrophication monitoring data where available
(EEA, national water agencies).

---

## Indicator 10 — Agriculture (`agriculture`)

**UBA source:** Tables 25–27, value factors for animal products (per kg),
fertilizer application (per kg applied), nutrient surplus (per kg excess)

**UBA scope:** Germany-specific (conventional German agriculture, German input
and output prices)

**Value transfer approach: Component-wise UVT + VFT**

Agricultural value factors integrate multiple damage pathways with different
transfer requirements:

| Sub-table | Dominant pathway | Transfer method |
|---|---|---|
| Table 25 (animal products) | GHG + NH₃ + N₂O | Transfer each pathway via indicators 01 and 09; recombine |
| Table 26 (fertilizer application) | N leaching + GHG | PT: scale by country N surplus intensity and leaching risk |
| Table 27 (nutrient surplus) | Water eutrophication | PT: same as indicator 09 (N, P water) |

### Transfer formula for animal products

```
D[beef, c]
  =  D[GHG, CO2eq/kg_beef, c]           ← from indicator 01 (global)
   + D[NH3, kg/kg_beef, c]              ← from indicator 02 (country-adjusted)
   + D[N2O, kg/kg_beef, c]              ← from indicator 01 (global)
   + D[land_use, ha/kg_beef, c]         ← from land use (PPP-adjusted)
```

Where `CO2eq/kg_beef`, `NH3/kg_beef`, etc. are physical emission intensities
per kg of product (from IPCC/FAO lifecycle inventories for livestock).

This reconstructs the animal product value factor from its constituent damage
pathways, each transferred appropriately.

---

## Summary Table: Value Transfer by Indicator

| ID | Key | UBA scope | Transfer approach | Country variation | Sector variation |
|----|-----|-----------|-------------------|-------------------|------------------|
| 01 | ghg | Global (GIVE model) | UVT (currency only) | None | None |
| 02 | air_pollutants | Germany | VFT + PT | Income + pop. density | By source type (Table 2/3/4) |
| 03 | electricity | Germany | PT (energy mix) | Country energy mix | None (commodity) |
| 04 | heat | Germany | PT (energy mix) | Country energy mix | None |
| 05 | refrigerants | Global (via GWP100 × CO₂) | UVT (currency only) | None | None |
| 06 | transport_vehkm | Germany | Component-wise VFT + PT | Per component | By route type |
| 07 | transport_pkm_tkm | Germany | Derived from 06 + occupancy | As indicator 06 | None |
| 08 | noise | Germany | VFT (income elasticity) | Income-scaled | None |
| 09 | nitrogen_phosphorus | Germany | PT (AWARE) + VFT | Water scarcity + income | None |
| 10 | agriculture | Germany | Component-wise (01 + 02 + 09) | Per pathway | None |

---

## Required Datasets for Full Implementation

| Dataset | Used by | Source |
|---|---|---|
| GDP per capita (PPP, 2025) | 02, 06, 07, 08, 09, 10 | World Bank WDI |
| EUR/USD exchange rate 2025 | All | ECB / World Bank |
| USA GDP deflator (time series) | All | World Bank WDI |
| Population density by country | 02, 06, 08 | World Bank / UN DESA |
| Urban population density along roads | 06, 08 | Global Urban Road Network |
| Electricity generation mix by country | 03, 04 | IEA World Energy Balances / Ember |
| Upstream GHG intensity of electricity (kg/kWh) | 03 | IPCC AR6 lifecycle values |
| National vehicle occupancy and load rates | 07 | ITF / national surveys |
| AWARE water scarcity factors by country | 09, 10 | WULCA AWARE v2 |
| Physical emission intensities for livestock | 10 | IPCC Tier 2 / FAO GLEAM |
| Income elasticity literature values | 02, 06, 08, 09 | Navrud 2002; Dekkers 2009; EC IMPACT |

---

## Integration into the Transitionvaluation Coefficient Matrix

Once value-transferred, each UBA indicator produces a DataFrame conforming to
the WifOR transitionvaluation convention:

```python
# Row MultiIndex:    (Year, Variable)
# Column MultiIndex: (GeoRegion, NACE)

# Example for ghg, CO2, 0% PRTP, year 2025:
C.loc[("2025", "UBA_GHG_CO2_0pct_PRTP, in USD/t (UBA2025)"), ("DEU", "A")]
# → -0.990 × 1.07 × I_USD[2025]

# For air pollutants, PM2.5, health, Germany:
C.loc[("2025", "UBA_AirPollutants_PM2.5_health, in USD/t (UBA2025)"), ("DEU", "A")]
# → -128200 × 1.07 × I_USD[2025]

# For Brazil (income-adjusted, lower GDP/cap than Germany):
C.loc[("2025", "UBA_AirPollutants_PM2.5_health, in USD/t (UBA2025)"), ("BRA", "A")]
# → -128200 × (GDP_pc[BRA]/GDP_pc[DEU])^0.9 × pop_dens_factor × 1.07 × I_USD[2025]
```

### Output file naming

Following the steen-vf1 / WifOR convention:

```
output/
  11_uba4_ghg_transferred.h5
  12_uba4_air_pollutants_transferred.h5
  13_uba4_electricity_transferred.h5
  ...
```

Each `.h5` file contains keys `"coefficient"` and `"unit"` matching the
WifOR HDF5 schema.

---

## Limitations and Caveats

1. **Germany-specific dose-response functions.** Tables 3 and 4 use EcoSenseWeb
   v1.3 with German receptor data. Parameter transfer (population density) is a
   first-order approximation; full spatial modelling would require running
   EcoSenseWeb for each target country.

2. **Limiting-substance assumption (N/P water).** UBA applies the conservative
   lower-bound (limiting substance only). In countries where both N and P are
   simultaneously limiting, the true damage is higher.

3. **Agriculture excludes biodiversity and animal welfare.** UBA explicitly
   excludes these pathways. Any value transfer inherits this limitation.

4. **PRTP scenario selection.** For integration into a single coefficient matrix,
   choose one PRTP scenario (0 % for long-term/intergenerational analysis;
   1 % for conventional cost-benefit analysis) or maintain both as separate
   Variable rows.

5. **Currency base.** UBA values are EUR_2025. After EUR/USD conversion, the
   temporal deflation uses the USA GDP deflator (WifOR convention), not the
   EU HICP deflator used in the steen-vf1 pipeline. This is intentional for
   WifOR framework compatibility.

---

## References

- Eser, N., Matthey, A., Bünger, B. (2025). UBA Handbook on Environmental Value Factors, MC 4.0.
- Anthoff, D. (2025). GIVE model.
- Navrud, S. (2002). The State of the Art on Economic Valuation of Noise. EC DG Environment.
- Dekkers, J., van der Straaten, W. (2009). Monetary valuation of aircraft noise. *Ecol. Econ.*
- Guski, R. et al. (2017). WHO Environmental Noise Guidelines for the European Region.
- Chen, J., Hoek, G. (2020). Long-term exposure to PM and mortality. *Environ. Health Perspect.*
- WULCA (2021). AWARE v2 — Available Water Remaining characterisation factors.
- World Bank (2025). World Development Indicators (GDP per capita, deflators).
- IEA (2025). World Energy Balances.
- Steen, B. (2015). EPS 2015d.1 — Environmental Priority Strategies.

---

*Scripts: Dr Dimitrij Euler, Greenings (dimitrij.euler@greenings.org), with support of Claude Code (Anthropic) |
Handbook: Nadia Eser, Dr. Astrid Matthey, Dr. Björn Bünger — German Environment Agency (UBA), December 2025 | Document Version 1.0 | Last Updated 2026-03-05*
