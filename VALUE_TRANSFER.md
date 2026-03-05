# Value Transfer Description — WifOR, EPS (Steen) and UBA Value Factor Sets

**Transitionvaluation Framework | Greenings | Updated 2026-03-05**

---

## 1. Overview

This document describes how the three value factor sets in the transitionvaluation
framework can be integrated into the common WifOR coefficient matrix
`C[year, indicator, country, sector]` covering 188 countries and 21 NACE sectors.

### The three systems

| System | Folder | Geographic anchor | Price base | Indicators | Rows/substances |
|--------|--------|------------------|------------|------------|-----------------|
| **WifOR** | `value-factors/` | Global (188 countries, already differentiated) | USD (mixed base years) | 8 | 8 categories |
| **EPS 2015d.1** (Steen) | `stockholm-value-factors/` | Sweden (globally applied) | EUR 2015 (ELU ≈ EUR) | 12 | 892 substances |
| **UBA MC 4.0** | `uba-value-factors/` | Germany (GHG: global via GIVE) | EUR 2025 | 10 | 546 rows |

### General coefficient formula (WifOR convention)

```
C[y, i, c, s] = Sign(i) × D[i, c] × I_USD[y]

where:
  y           = year in {2014..2030, 2050, 2100}
  i           = indicator
  c           = country ISO3 code (188 countries)
  s           = NACE A21 sector
  Sign(i)     = −1.0 for damage costs; +1.0 for benefits (Training only)
  D[i, c]     = country-specific base value in USD after value transfer
  I_USD[y]    = USA GDP deflator[y] / USA GDP deflator[base_year]
```

### Value transfer approaches

| Approach | Abbreviation | When to use |
|---|---|---|
| **Unit Value Transfer** | UVT | Globally uniform damage (climate, refrigerants); currency conversion only |
| **Value Function Transfer** | VFT | WTP-income elasticity applied to rescale anchor-country value by GDP per capita |
| **Parameter Transfer** | PT | Re-derive value using country-specific physical parameters (energy mix, population density, water scarcity) with the same dose-response function |

### Geographic anchors and income scaling

When applying VFT from a national anchor, the income-scaling reference is:

```
D[i, c] = D[i, anchor]
            × (GDP_pc_PPP[c, base_year] / GDP_pc_PPP[anchor, base_year])^ε
            × FX[anchor_currency → USD, base_year]

Anchors:
  UBA  → DEU (Germany)    GDP_pc_PPP 2025 ≈ 59,000 USD
  EPS  → SWE (Sweden)     GDP_pc_PPP 2015 ≈ 46,000 USD
  WifOR → global (no anchor; factors already country-differentiated)
```

---

## 2. Indicator Map — Coverage Across the Three Systems

| Indicator | WifOR | EPS (Steen) | UBA MC 4.0 | Section |
|-----------|:-----:|:-----------:|:----------:|---------|
| **SAME — all three systems** | | | | |
| Greenhouse gases (CO₂, CH₄, N₂O) | ✓ | ✓ | ✓ | 3.1 |
| Air pollutants (PM, NOₓ, SO₂, NH₃, NMVOC) | ✓ | ✓ | ✓ | 3.2 |
| Nitrogen & phosphorus to water | ✓ | ✓ | ✓ | 3.3 |
| **SIMILAR — two of three systems** | | | | |
| Land use / habitat conversion | ✓ | ✓ | — | 4.1 |
| Noise | — | ✓ | ✓ | 4.2 |
| Waste | ✓ | ✓ | — | 4.3 |
| Heavy metals & toxics to air/water | ✓ | ✓ | — | 4.4 |
| Halogenated compounds / refrigerants | — | ✓ (004) | ✓ (05) | 4.5 |
| **DIFFERENT — unique to one system** | | | | |
| Water consumption (blue water) | ✓ | — | — | 5.1 |
| Training / human capital | ✓ | — | — | 5.2 |
| Occupational health & safety (OHS) | ✓ | — | — | 5.3 |
| Fossil resources depletion | — | ✓ (010) | — | 5.4 |
| VOCs — detailed speciation (144 substances) | — | ✓ (003) | — | 5.5 |
| Radionuclides | — | ✓ (008) | — | 5.6 |
| Pesticides | — | ✓ (006) | — | 5.7 |
| Critical minerals & other elements | — | ✓ (011) | — | 5.8 |
| Electricity (life-cycle per kWh by source) | — | — | ✓ (03) | 5.9 |
| Heat (life-cycle per kWh by source) | — | — | ✓ (04) | 5.10 |
| Transport (per vehicle-km and Pkm/tkm) | — | — | ✓ (06/07) | 5.11 |
| Agriculture (per kg product / nutrient surplus) | — | — | ✓ (10) | 5.12 |

---

## 3. Same Indicators — Covered by All Three Systems

These indicators have direct counterparts in WifOR, EPS and UBA. They can be
compared and, where methodologies align, cross-validated or merged.

---

### 3.1 Greenhouse Gas Emissions — CO₂, CH₄, N₂O

**Coverage**

| System | Indicator / Script | Unit | Method | Price base |
|--------|--------------------|------|--------|------------|
| WifOR | `020_GHG` | USD/kg CO₂e | DICE/RICE (Nordhaus/Barrage 2024); global SCC | USD (mixed) |
| EPS | `001_inorganic_gases` (CO₂, CH₄, N₂O) | ELU/kg | Climate change pathway → YOLL + crop + wood + fish + coastal; global | EUR 2015 |
| UBA | `01_ghg` (Table 1) | EUR 2025/t | GIVE model (Anthoff 2025); equity-weighted, German income reference; 0 % and 1 % PRTP | EUR 2025 |

**Key values at 2025 emission year**

| Gas | WifOR | EPS | UBA (0 % PRTP) | UBA (1 % PRTP) |
|-----|-------|-----|----------------|----------------|
| CO₂ | varies by year/scenario | ~0.05–0.10 ELU/kg | 990 EUR/t | 345 EUR/t |
| CH₄ | GWP100 × CO₂ SCC | pathway-derived | 9,220 EUR/t | 5,800 EUR/t |
| N₂O | GWP100 × CO₂ SCC | pathway-derived | 282,300 EUR/t | 118,700 EUR/t |

**Methodological differences**

- **WifOR** uses the DICE/RICE integrated assessment model (Nordhaus 2024
  update), producing a single global SCC trajectory. CH₄ and N₂O are expressed
  as CO₂-equivalent via AR6 GWP100.
- **EPS** sums pathway damages across five safeguard subjects using Swedish-
  derived monetary values (YOLL = 50,000 ELU/person-year). The result is
  globally applied but Swedish-income-anchored.
- **UBA** uses the GIVE model (successor to FUND), which models CH₄ and N₂O
  directly (not GWP100 proxies), with equity weighting using German per-capita
  income as reference. Two PRTP scenarios are provided.

**Value transfer**

GHG damage is intrinsically global (one tonne emitted anywhere causes the same
radiative forcing). No country-income adjustment is warranted for the climate
damage component. Only currency conversion and temporal deflation are needed.

```
D[GHG, gas, c]  =  VF[gas, source_system]  ×  FX → USD  (uniform across all c)

WifOR:  already in USD; apply I_USD[y] directly
EPS:    VF[ELU/kg] × EU_HICP_deflator[y→2015] × EUR_USD[2015]
UBA:    VF[EUR_2025/t] / 1000 × EUR_USD[2025]
        (then apply I_USD[y] from base 2025)
```

**Cross-validation:** UBA 0 % PRTP CO₂ value (990 EUR/t ≈ 1,059 USD/t in 2025)
is higher than typical DICE outputs (~200–400 USD/t at ~3 % discount rate)
because GIVE uses 0 % pure time preference and equity weighting. This is a
known and documented difference, not an error.

---

### 3.2 Air Pollutant Emissions — PM₂.₅, PM₁₀, NOₓ, SO₂, NH₃, NMVOC

**Coverage**

| System | Indicator / Script | Substances | Unit | Method |
|--------|--------------------|-----------|------|--------|
| WifOR | `008_AirPollution` | PM2.5, PM10, NOx, SOx, NMVOC, NH₃ | USD/t pollutant | UBA methodology + regional population-density adjustment; 188 countries |
| EPS | `001_inorganic_gases` + `002_particles` | PM>10, PM10, PM2.5, ultrafine PM; NOₓ, SO₂, HF, HCl, NH₃, O₃, and more | ELU/kg | Pathway model: YOLL (health) + crop + biodiversity + materials; Swedish anchor |
| UBA | `02_air_pollutants` (Tables 2–4) | PM2.5, PMcoarse, PM10_abrasion, NOₓ, SO₂, NMVOC, NH₃ | EUR 2025/t | EcoSenseWeb v1.3; German population density; three context tiers |

**Key values (health component, unknown source context)**

| Substance | WifOR (USD/t) | EPS (EUR 2015/t) | UBA (EUR 2025/t) |
|-----------|---------------|-----------------|-----------------|
| PM₂.₅ | country-specific | pathway-derived | 128,200 (health) |
| NOₓ | country-specific | pathway-derived | 37,740 (total) |
| SO₂ | country-specific | pathway-derived | 35,325 (total) |
| NH₃ | country-specific | pathway-derived | 30,275 (total) |

**Methodological differences**

- **WifOR** already applies population-density and income adjustment relative to
  Germany (it uses UBA as its methodological basis). Its country-specific factors
  are the output of a VFT + PT already applied.
- **EPS** monetizes through the YOLL pathway (50,000 ELU/person-year, Swedish
  WTP). Includes crop production, biodiversity (NEX), and building materials in
  addition to health. No country differentiation in published EPS index values.
- **UBA** provides three tiers: Table 2 (unknown source — recommended default),
  Table 3 (stationary combustion, differentiated by sector/height/surroundings),
  Table 4 (road traffic, by surroundings type). Germany-specific receptor data.

**Value transfer (EPS and UBA to other countries)**

Air pollutant health damage depends on (a) the monetary value of life-years
(income-elastic) and (b) the population exposed per tonne emitted (physical,
country-specific).

```
D[AP, substance, c]
  =  VF[substance, anchor]                        ← EPS anchor: SWE; UBA anchor: DEU
     × (GDP_pc_PPP[c] / GDP_pc_PPP[anchor])^ε_h   ← income elasticity (health WTP)
     × (POP_density[c] / POP_density[anchor])^α   ← exposure scaling
     × FX → USD

where:
  ε_h  ≈ 0.8–1.0   (health WTP income elasticity, literature consensus)
  α    ≈ 1.0        (linear for uniformly mixed regional pollutants)
  α    ≈ 0.5–0.7    (sub-linear for local pollutants: PM₂.₅ road traffic)

Non-health components (crop damage, material damage):
  Not income-elastic; use UVT with currency conversion only.
```

**WifOR note:** WifOR air pollution coefficients are already the result of
applying this VFT + PT to the UBA base values. For WifOR integration, use its
published D[i, c] values directly and apply I_USD[y].

---

### 3.3 Nitrogen and Phosphorus to Water

**Coverage**

| System | Indicator / Script | Substances | Unit |
|--------|--------------------|-----------|------|
| WifOR | `013_WaterPol` | N (NH₄, NO₃, TN), P (PO₄, TP) | USD/kg |
| EPS | `005_emissions_to_water` | N compounds, P compounds | ELU/kg |
| UBA | `09_nitrogen_phosphorus` (Tables 22–24) | N air (NOₓ, NH₃, N₂O), N water, P water | EUR 2025/kg N or kg P |

**Methodological differences**

- **WifOR** models health and ecosystem damage from N and P using the USEtox
  and Steen (2020) approach; 188 country-specific factors.
- **EPS** models eutrophication via oxygen deficiency pathway (BOD, N, P to
  freshwater and marine). Swedish-anchored monetary values for fish, biodiversity,
  and drinking water.
- **UBA** applies a limiting-substance assumption: only the limiting nutrient (N
  or P) causes eutrophication damage. This yields conservative lower bounds.
  Air N emissions (NOₓ, NH₃) are valued via health pathways (as per indicator 02).

**Value transfer (EPS and UBA)**

Eutrophication damage scales with water scarcity and ecosystem sensitivity,
which vary substantially by country.

```
D[N_water, c]  =  VF[N, anchor]
                   × AWARE[c]                       ← water scarcity (0.1–100, WULCA AWARE v2)
                   × (GDP_pc_PPP[c] / GDP_pc_PPP[anchor])^ε_eco
                   × FX → USD

D[N_air, c]    →  transfer as air pollutant (health pathway, indicator 3.2)

where:
  ε_eco  ≈ 0.4–0.6  (ecosystem WTP income elasticity; lower than health)
  anchor = SWE for EPS; DEU for UBA
```

**Limiting-substance caveat (UBA):** In countries where both N and P are
co-limiting, the UBA value is an underestimate. Supplement with EPS or
WifOR values where possible.

---

## 4. Similar Indicators — Covered by Two of Three Systems

These indicators have meaningful overlap between two systems. The third system
does not cover them, creating a gap to be filled either by transfer from one
of the covering systems or by noting the limitation.

---

### 4.1 Land Use / Habitat Conversion

**Covered by:** WifOR ✓ | EPS ✓ | UBA —

| System | Indicator | Scope | Unit |
|--------|-----------|-------|------|
| WifOR | `010_LandUse` | Ecosystem service losses; LANCA factors; 188 countries | USD/ha |
| EPS | `009_land_use` (23 land types) | Five pathways: climate, crop, wood, water regulation, NEX; Swedish anchor | ELU/m²·yr |

**UBA gap:** UBA MC 4.0 explicitly excludes land use (Chapters 8–12 are not
parsed; Chapter 8 building materials are illustrative only, no standalone VF
recommended). Agriculture (indicator 10) partially captures land via animal
product GHG and N pathways but does not include a dedicated land use VF.

**Integration approach:**

Use WifOR `010_LandUse` as the primary source for the 188-country coefficient
matrix. EPS `009` can serve as a cross-validation anchor.

```
EPS → WifOR cross-check:
  D[land, WifOR, c] should approximate
    EPS_land_VF[type]
    × (GDP_pc_PPP[c] / GDP_pc_PPP[SWE])^ε_eco
    × land_type_mapping[EPS → WifOR categories]
```

For UBA indicators that involve land (agriculture, transport infrastructure),
supplement with WifOR land use values applied to the physical land use
intensity (ha per tonne product or km per vehicle type).

---

### 4.2 Noise

**Covered by:** WifOR — | EPS ✓ | UBA ✓

| System | Indicator | Scope | Unit |
|--------|-----------|-------|------|
| EPS | `007_noise` | Road traffic noise; sleep disturbance → YOLL pathway; Swedish anchor | ELU/W (relative power) |
| UBA | `08_noise` (Tables 19–20) | Road, rail, air traffic; annoyance + cognitive impairment in children; by dB(A) class; German anchor | EUR 2025/person/year |

**WifOR gap:** WifOR does not include a noise indicator. Noise externalities
from transport are absent from the WifOR coefficient matrix.

**Unit reconciliation — EPS to UBA:**

EPS uses relative acoustic power (W = 10^(dB/10)) as the emission unit.
UBA uses person-year of exposure at a specific dB(A) class.

```
Conversion:
  EPS:  ELU per W of relative power
  UBA:  EUR/person/year at dB(A) class [45–49, 50–54, …, ≥75]

To bridge: apply WHO exposure-response function (Guski et al. 2017) to
translate relative power into % highly annoyed per exposed person, then
multiply by UBA per-person-year value:

  D[noise_EPS, dB, c]  ≈  %HA(dB) × pop_exposed × D[noise_UBA, dB, c]
                            × (GDP_pc_PPP[c] / GDP_pc_PPP[DEU])^ε_noise

where ε_noise ≈ 0.8 (Navrud 2002; Dekkers & van der Straaten 2009)
and anchor = DEU for UBA; SWE for EPS.
```

**Value transfer (both systems to 188 countries):**

```
D[noise, dB_class, mode, c]
  =  VF[noise, dB_class, mode, anchor]
     × (GDP_pc_PPP[c] / GDP_pc_PPP[anchor])^0.8
     × FX → USD
```

**Recommendation:** Use UBA noise values as the primary source (more granular
dB-class structure; covers road, rail, and air; updated 2025 German income base).
Transfer via VFT with Sweden as the EPS cross-validation point.

---

### 4.3 Waste

**Covered by:** WifOR ✓ | EPS ✓ | UBA —

| System | Indicator | Scope | Unit |
|--------|-----------|-------|------|
| WifOR | `007_Waste` | Hazardous and non-hazardous waste; incineration, landfill, recovery pathways; 188 countries | USD/kg |
| EPS | `012_waste` | Plastic litter to ground and water; Swedish anchor | ELU/unit |

**UBA gap:** UBA MC 4.0 does not include a waste indicator. Building materials
(Tables 28–29) are explicitly excluded as illustrative only.

**Integration approach:**

Use WifOR `007_Waste` for the 188-country coefficient matrix. EPS `012`
covers only litter (a narrower category) and is best used to supplement the
plastic waste sub-pathway.

**EPS → country transfer:**

```
D[waste_EPS, c]  =  EPS_VF[litter_type]
                     × (GDP_pc_PPP[c] / GDP_pc_PPP[SWE])^ε_eco
                     × EUR_USD[2015] × HICP[2015 → target_year]
```

---

### 4.4 Heavy Metals and Toxic Substances to Air and Water

**Covered by:** WifOR ✓ | EPS ✓ | UBA —

| System | Indicator | Substances | Unit |
|--------|-----------|-----------|------|
| WifOR | `013_WaterPol` | As, Cd, Hg, Cr, Pb, Ni, Cu, Zn, Sb (water) | USD/kg metal |
| EPS | `002_particles` (metals in PM) + `005_emissions_to_water` | As, Cd, Cr, Cu, Pb, Zn, PAH (air + water) | ELU/kg |

**UBA gap:** UBA covers only criteria air pollutants and N/P. No heavy metal
or organic toxicant value factors are provided.

**Integration approach:**

Use WifOR water pollution coefficients as primary. EPS provides the
substance-level characterization factors for cross-validation and for
substances not in WifOR.

```
D[metal, c] from EPS:
  D[metal, c]  =  EPS_VF[metal]
                   × (GDP_pc_PPP[c] / GDP_pc_PPP[SWE])^ε_h    ← health component
                   × (POP_density[c] / POP_density[SWE])       ← exposure
                   × EUR_USD[2015] × HICP[2015 → target_year]
```

---

### 4.5 Halogenated Compounds and Refrigerants

**Covered by:** WifOR — | EPS ✓ (004) | UBA ✓ (05)

| System | Indicator | Scope | Unit | Method |
|--------|-----------|-------|------|--------|
| EPS | `004_halogenated_organics` | CFCs, HCFCs, HFCs, PFCs, halons, chlorinated solvents (283 substances) | ELU/kg | Climate change + ozone depletion + human toxicity pathways |
| UBA | `05_refrigerants` (Table 7) | R-32, R-410A, R-134a, R-507A, R-717 (NH₃), R-290, and others (8 refrigerants) | EUR 2025/kg refrigerant | GWP100 × CO₂ social cost; climate only |

**WifOR gap:** WifOR does not have a dedicated halogenated compound or
refrigerant indicator. These are absent from the WifOR coefficient matrix.

**Methodological differences:**

- **EPS** covers three damage pathways (climate, ozone depletion, toxicity),
  producing a comprehensive ELU/kg per substance.
- **UBA** covers only the climate pathway (GWP100 × CO₂ VF), making it a
  conservative lower bound for substances with significant ozone depletion or
  toxicity impacts (e.g. CFCs).

**Value transfer:**

UBA refrigerant values are globally uniform (derived from global CO₂ VF):

```
D[refrigerant r, c]  =  GWP100[r] × UBA_VF[CO₂, 2025, PRTP] × EUR_USD[2025]
                         (uniform across all c — no country adjustment)
```

EPS halogenated values include non-climate pathways and are Sweden-anchored
for the monetary health component:

```
D[substance, c] from EPS:
  D[substance, c]  =  EPS_VF[substance]
                        × (GDP_pc_PPP[c] / GDP_pc_PPP[SWE])^ε     ← for health/toxicity share
                        × EUR_USD[2015] × HICP[2015 → target_year]
  (climate share: uniform; ozone depletion: uniform; toxicity: income-elastic)
```

**Recommendation:** For refrigerants covered by UBA, use the UBA value as the
primary climate-damage VF. For ozone-depleting substances (CFCs, HCFCs) not
in UBA, use the EPS value transferred via VFT from the Swedish anchor.

---

## 5. Different Indicators — Unique to One System

These indicators are covered by only one of the three systems. No cross-
validation is possible; value transfer from the single source must rely on
the standard VFT / PT / UVT framework.

---

### 5.1 Water Consumption (Blue Water) — WifOR only

**WifOR script:** `009_WaterConsumption` | Unit: USD/m³ | Method: economic
damage + DALYs; Ligthart & van Harmelen + Debarre et al.; 188 countries.

WifOR already provides country-specific coefficients. Apply I_USD[y] directly.

**Coverage gap in EPS and UBA:** Neither system includes blue water depletion.

---

### 5.2 Training / Human Capital — WifOR only

**WifOR script:** `014_Training` | Unit: USD/hour of training | Method: return
to education (Psacharopoulos & Patrinos 2018); positive benefit; 188 countries.

Sign convention: +1.0 (benefit). WifOR is the sole source; no transfer needed.

**Coverage gap in EPS and UBA:** Training benefits are absent from both systems.
EPS covers only environmental damage categories; UBA covers only environmental
externality costs.

---

### 5.3 Occupational Health & Safety (OHS) — WifOR only

**WifOR script:** `015_OHS` | Unit: USD/fatal or non-fatal incident | Method:
DALYs (Global Burden of Disease); VSL approach; 188 countries.

Sign: −1.0. Country-specific VSL derived from income elasticity (ε ≈ 1.0)
relative to a global reference VSL.

**Coverage gap in EPS and UBA:** OHS is absent from both. EPS human health
pathway captures population-level health effects of environmental exposures,
not workplace-specific incidents. UBA does not cover occupational risks.

---

### 5.4 Fossil Resource Depletion — EPS only

**EPS script:** `010_fossil_resources` | Substances: fossil oil, fossil coal,
lignite, natural gas | Unit: ELU/kg | Method: resource depletion → future
extraction cost increase + energy substitution cost; Swedish anchor.

**Value transfer to 188 countries:**

```
D[fossil_resource, c]  =  EPS_VF[resource]
                            × (GDP_pc_PPP[c] / GDP_pc_PPP[SWE])^ε_res
                            × EUR_USD[2015] × HICP[2015 → y]

ε_res  ≈ 0.5–0.8  (resource depletion WTP; lower than health; literature limited)
```

**Note:** UBA's electricity and heat value factors (indicators 5.9–5.10) implicitly
include upstream fossil resource extraction costs as part of the life-cycle damage.
These should not be double-counted with the EPS fossil resource indicator.

---

### 5.5 Volatile Organic Compounds — Detailed Speciation (EPS only)

**EPS script:** `003_VOCs` | Substances: 144 (alkanes, aromatics, alcohols,
aldehydes, terpenes, chlorinated solvents) | Unit: ELU/kg.

WifOR includes NMVOC as an aggregated category in air pollution. UBA includes
NMVOC in Tables 2–4 as an aggregate. EPS provides 144 individual compounds.

**Value transfer:**

```
D[VOC_compound, c]  =  EPS_VF[compound]
                         × (GDP_pc_PPP[c] / GDP_pc_PPP[SWE])^ε_h
                         × (POP_density[c] / POP_density[SWE])
                         × EUR_USD[2015] × HICP[2015 → y]
```

For integration, either (a) map EPS compounds to the NMVOC aggregate in WifOR
or UBA using mass-weighted averaging, or (b) maintain at substance level for
LCA-linked applications.

---

### 5.6 Radionuclides — EPS only

**EPS script:** `008_radionuclides` | Substances: C-14, H-3, I-129, Kr-85,
Pb-210, Po-210, Ra-226, Rn-222, Th-230, U-234, U-238 | Unit: ELU/TBq.

Radionuclide damage is primarily health-based (YOLL via radiation dose). The
EPS pathway uses UNSCEAR dose-response functions applied globally.

**Value transfer:**

```
D[radionuclide, c]  =  EPS_VF[nuclide]
                         × (GDP_pc_PPP[c] / GDP_pc_PPP[SWE])^ε_h
                         × EUR_USD[2015] × HICP[2015 → y]
(no population-density scaling: radiation disperses globally via atmospheric/oceanic pathways)
```

**Relevance:** Nuclear electricity generation and uranium mining. Cross-reference
with UBA electricity (indicator 5.9) for nuclear power plants (UBA Table 5
includes nuclear as an energy source).

---

### 5.7 Pesticides — EPS only

**EPS script:** `006_pesticides` | Substances: 302 (herbicides, insecticides,
fungicides, growth regulators) | Unit: ELU/kg active substance.

WifOR does not include pesticide costs. UBA does not include them either (agriculture
value factors in UBA focus on GHG, N, and P pathways, not pesticide toxicity).

**Value transfer:**

```
D[pesticide, c]  =  EPS_VF[pesticide]
                     × (GDP_pc_PPP[c] / GDP_pc_PPP[SWE])^ε_eco    ← ecosystem component dominant
                     × EUR_USD[2015] × HICP[2015 → y]

ε_eco  ≈ 0.4–0.6  (ecosystem WTP income elasticity)
```

For agricultural applications, the pesticide value factor should be added to
the UBA agriculture value factors to give a more complete damage picture.

---

### 5.8 Critical Minerals and Other Elements — EPS only

**EPS script:** `011_other_elements` | Substances: 77 (Ag to Zr: silver, rare
earth elements, platinum group, Li, Co, In, Ga, and other critical minerals) |
Unit: ELU/kg.

Method: future extraction cost increase + substitution cost; globally anchored
(no population-density dependence).

**Value transfer:**

```
D[element, c]  =  EPS_VF[element]
                   × EUR_USD[2015] × HICP[2015 → y]
(globally uniform; resource scarcity is not country-specific in EPS 2015d.1)
```

---

### 5.9 Electricity — Life-cycle VF per kWh by Source (UBA only)

**UBA script:** `03_electricity` (Table 5) | Unit: EUR-cent 2025/kWh_el |
Sources: German mix, Lignite, Hard coal, Natural gas, Nuclear, Wind, Solar PV,
Hydro, Biomass | Components: air pollutants + GHG (× 2 PRTP) per source.

**Germany-specific:** reflects the German supply chain, grid losses, and German
population receptor data.

**Value transfer to 188 countries:**

Apply a country energy-mix weighted average:

```
D[electricity, c]
  =  Σ_source  share[source, c]
        × [VF_GHG[source] × EUR_USD[2025]                          ← global (UVT)
         + VF_AP[source] × (GDP_pc_PPP[c] / GDP_pc_PPP[DEU])^ε_h  ← health-elastic (VFT)
                         × (POP_density[c] / POP_density[DEU])]    ← exposure (PT)

where share[source, c] = IEA World Energy Balances / Ember electricity generation shares
```

Simplified proxy (if mix data unavailable):

```
D[electricity, c]  ≈  D[German_mix, DEU]
                        × (emission_intensity[c] / emission_intensity[DEU])
                        × EUR_USD[2025]
```

---

### 5.10 Heat Generation — Life-cycle VF per kWh by Source (UBA only)

**UBA script:** `04_heat` (Table 6) | Unit: EUR-cent 2025/kWh_final_energy |
Sources: Natural gas, Heating oil, Hard coal, Lignite, Biomass, Solar thermal,
Heat pumps.

Apply the same country-energy-mix approach as electricity (indicator 5.9),
using national statistics on residential and district heating fuel use
(Eurostat Energy Balances, IEA).

For countries where district heating from CHP predominates (Nordic countries,
Russia, Eastern Europe), the district heating row from Table 6 is preferred
as a transfer base with income-elasticity adjustment for the health component.

---

### 5.11 Transport — per Vehicle-km and per Pkm/tkm (UBA only)

**UBA scripts:** `06_transport_vehkm` (Tables 9–16), `07_transport_pkm_tkm`
(Tables 17–18) | Vehicles: Cars, Vans, Heavy-duty trucks, Buses, Rail, Air,
Ship (by fuel type and route) | Components: GHG, AP exhaust, AP abrasion,
infrastructure, energy supply.

**Value transfer — component-wise:**

| Component | Method | Country adjustment |
|-----------|--------|--------------------|
| `ghg` | UVT | None (global) |
| `air_pollutants_exhaust` | VFT + PT | Income elasticity + population density along routes |
| `air_pollutants_abrasion` | VFT + PT | As above (urban/rural road network density) |
| `infra_and_vehicles` | UVT + PPP | Scale by local price level (construction costs) |
| `energy_supply` | PT | Country fuel/electricity mix (as indicator 5.9/5.10) |

```
D[vehkm, vehicle, route, c]
  =  VF_ghg    × EUR_USD[2025]
   + VF_ap     × (GDP_pc_PPP[c] / GDP_pc_PPP[DEU])^ε_h
               × (POP_dens_route[c] / POP_dens_route[DEU])
   + VF_infra  × (PPP[c] / PPP[DEU])
   + VF_energy × (emission_intensity[c] / emission_intensity[DEU])

D[Pkm, vehicle, c]  =  D[vehkm, vehicle, c]  /  occupancy_rate[vehicle, c]
```

---

### 5.12 Agriculture — per kg Product and per kg Nutrient Surplus (UBA only)

**UBA script:** `10_agriculture` (Tables 25–27) | Items: Milk, Beef, Pork,
Poultry, Eggs, N fertilizer, P fertilizer, N surplus, P surplus | Unit: EUR 2025/kg.

**UBA scope limitation:** Explicitly excludes biodiversity, ecosystem services
beyond N/P, and animal welfare. Values are partial lower bounds.

**Value transfer — component reconstruction:**

```
D[beef, c]
  =  GHG_intensity[beef] × D[CO2eq, c]          ← UVT (global, indicator 3.1)
   + NH3_intensity[beef] × D[NH3_health, c]      ← VFT (air AP, indicator 3.2)
   + N2O_intensity[beef] × D[N2O, c]             ← UVT (global, indicator 3.1)
   + land_intensity[beef] × D[land_use, c]       ← WifOR land use (indicator 4.1)

where physical emission intensities per kg product:
  from IPCC Tier 2 livestock emission factors / FAO GLEAM database
```

For fertilizer application (Table 26) and nutrient surplus (Table 27):
apply the same PT approach as indicator 3.3 (N/P to water), scaled by
AWARE water scarcity and income elasticity.

---

## 6. Summary: Value Transfer by Indicator

| # | Indicator | WifOR | EPS | UBA | Transfer method | Country variation | ε |
|---|-----------|:-----:|:---:|:---:|-----------------|-------------------|---|
| 3.1 | GHG (CO₂, CH₄, N₂O) | ✓ | ✓ | ✓ | UVT (climate damage global) | None | — |
| 3.2 | Air pollutants (PM, NOₓ, SO₂, NH₃, NMVOC) | ✓ | ✓ | ✓ | VFT + PT | Income + pop. density | 0.8–1.0 (health) |
| 3.3 | Nitrogen & phosphorus to water | ✓ | ✓ | ✓ | PT + VFT | AWARE + income | 0.4–0.6 (eco) |
| 4.1 | Land use | ✓ | ✓ | — | VFT (from WifOR primary) | Income | 0.4–0.6 |
| 4.2 | Noise | — | ✓ | ✓ | VFT | Income | 0.8 |
| 4.3 | Waste | ✓ | ✓ | — | VFT (from WifOR primary) | Income | 0.4–0.6 |
| 4.4 | Heavy metals & toxics | ✓ | ✓ | — | VFT + PT | Income + pop. density | 0.8–1.0 (health) |
| 4.5 | Halogenated / refrigerants | — | ✓ | ✓ | UVT (climate share); VFT (ozone + toxicity share) | None (climate); income (other) | 0.8–1.0 |
| 5.1 | Water consumption | ✓ | — | — | Already country-specific | — | — |
| 5.2 | Training | ✓ | — | — | Already country-specific | — | — |
| 5.3 | OHS | ✓ | — | — | Already country-specific | — | — |
| 5.4 | Fossil resources | — | ✓ | — | VFT (from SWE) | Income | 0.5–0.8 |
| 5.5 | VOCs (detailed) | — | ✓ | — | VFT + PT (from SWE) | Income + pop. density | 0.8–1.0 |
| 5.6 | Radionuclides | — | ✓ | — | VFT (from SWE) | Income | 0.8–1.0 |
| 5.7 | Pesticides | — | ✓ | — | VFT (from SWE) | Income | 0.4–0.6 |
| 5.8 | Critical minerals | — | ✓ | — | UVT (resource; globally uniform) | None | — |
| 5.9 | Electricity (per kWh by source) | — | — | ✓ | PT (energy mix) + VFT (AP component) | Country mix + income | 0.8–1.0 |
| 5.10 | Heat (per kWh by source) | — | — | ✓ | PT (heating mix) + VFT (AP component) | Country mix + income | 0.8–1.0 |
| 5.11 | Transport (vehicle-km; Pkm/tkm) | — | — | ✓ | Component-wise VFT + PT | Per component | 0.8–1.0 |
| 5.12 | Agriculture | — | — | ✓ | Component reconstruction from 3.1 + 3.2 + 3.3 | Per pathway | varies |

---

## 7. Required Datasets for Full Implementation

| Dataset | Used by | Source |
|---------|---------|--------|
| GDP per capita, PPP (2015 and 2025) | All VFT indicators | World Bank WDI |
| EUR/USD exchange rate (2015, 2025) | EPS, UBA → USD | ECB / World Bank |
| SEK/EUR exchange rate (2015) | EPS → EUR if needed | ECB |
| USA GDP deflator (time series 2014–2100) | All | World Bank WDI |
| EU HICP deflator (2015–2024; frozen post-2023) | EPS temporal adjustment | Eurostat |
| Population density by country | Air pollutants, noise, transport | World Bank / UN DESA |
| Urban population density along road corridors | Transport (AP component) | OpenStreetMap / Global Urban Network |
| Electricity generation mix by country and source | Electricity, heat | IEA World Energy Balances / Ember |
| Upstream GHG intensity of electricity (kg CO₂e/kWh) | Electricity | IPCC AR6 lifecycle values |
| National heating fuel mix | Heat | IEA / Eurostat Energy Balances |
| National vehicle occupancy and freight load rates | Transport Pkm/tkm | ITF / national travel surveys |
| AWARE water scarcity factors by country | N/P water, agriculture | WULCA AWARE v2 |
| Physical emission intensities for livestock | Agriculture | IPCC Tier 2 / FAO GLEAM |
| GWP100 values by refrigerant | Refrigerants | IPCC AR6 Table 7.SM.7 |

---

## 8. Integration into the Transitionvaluation Coefficient Matrix

All transferred values produce a DataFrame conforming to the WifOR convention:

```
Row MultiIndex:    (Year, Variable)
Column MultiIndex: (GeoRegion, NACE)

Variable naming convention:
  {System}_{Indicator}_{Substance/Context}_{Unit} ({PriceBase})

Examples:
  "WifOR_GHG_CO2eq, in USD/t CO2e (WifOR2020)"
  "EPS_InorgGas_CO2, in USD/kg (EPS2015)"
  "UBA_GHG_CO2_0pctPRTP, in USD/t (UBA2025)"
  "UBA_AirPollutants_PM2.5_health_unknownSource, in USD/t (UBA2025)"
  "EPS_Particles_PM2.5, in USD/kg (EPS2015)"
  "UBA_Noise_Road_50-54dB, in USD/person/yr (UBA2025)"
  "EPS_LandUse_Arable, in USD/m2yr (EPS2015)"
```

### Precedence rules when same indicator covered by multiple systems

Where two or three systems cover the same indicator, the following precedence
is suggested for the primary coefficient matrix. All alternatives are retained
as supplementary Variable rows for sensitivity analysis.

| Indicator | Primary | Supplementary | Rationale |
|-----------|---------|--------------|-----------|
| GHG | UBA (0 % PRTP) | WifOR, EPS | GIVE model most current; explicit PRTP; direct CH₄/N₂O modelling |
| Air pollutants | WifOR | UBA, EPS | Already country-differentiated; consistent with other WifOR indicators |
| N/P to water | WifOR | UBA, EPS | Country-specific; UBA limiting-substance is conservative lower bound |
| Noise | UBA | EPS | More granular (mode + dB class); updated 2025 income anchor |
| Land use | WifOR | EPS | Already country-differentiated; consistent with WifOR ecosystem framework |
| Waste | WifOR | EPS | Already country-differentiated; broader waste stream coverage than EPS |
| Refrigerants/HFCs | UBA + EPS | — | UBA: climate; EPS: supplement for ozone + toxicity pathways |

---

## 9. Limitations and Caveats

1. **Sweden anchor (EPS):** EPS monetary values are derived from Swedish/European
   WTP studies. Income transfer to non-OECD countries using ε ≈ 0.8 is a
   first-order approximation. Benefit transfer uncertainty is highest in low-
   income countries (>± 50 % is plausible).

2. **Germany anchor (UBA):** Germany has above-average population density.
   Population-density transfer to sparsely populated countries (Canada, Australia,
   much of Africa) will yield substantially lower air pollutant values. This is
   methodologically correct but should be noted in reporting.

3. **UBA limiting-substance assumption:** For N/P water emissions, UBA applies
   the conservative lower bound (only the limiting nutrient is charged). This
   underestimates damage in countries where both N and P co-limit aquatic systems.
   Supplement with EPS or WifOR values in such cases.

4. **UBA agriculture lower bounds:** UBA agriculture factors explicitly exclude
   biodiversity, ecosystem services beyond N/P, and animal welfare. Any transfer
   inherits these omissions. The reconstructed D[beef, c] from indicator 5.12
   should be treated as a partial lower bound.

5. **PRTP scenario selection:** For a single-scenario coefficient matrix, choose
   0 % PRTP for long-term or intergenerational analysis; 1 % PRTP for conventional
   cost-benefit analysis. Maintain both as separate Variable rows for full
   sensitivity coverage.

6. **Currency base consistency:** EPS is EUR_2015; UBA is EUR_2025; WifOR is USD
   (mixed). All must be converted to USD at the relevant year's exchange rate
   before applying I_USD[y] temporal deflation. Do not mix price bases within
   a single coefficient series.

7. **Double-counting:** UBA electricity/heat value factors already embed the GHG
   and air pollutant damage of upstream fuel supply. Do not add standalone GHG or
   air pollutant VFs to electricity VFs when constructing sector-level totals.

---

## 10. References

- Eser, N., Matthey, A., Bünger, B. (2025). UBA Handbook on Environmental Value Factors, MC 4.0. German Environment Agency.
- Steen, B. (2015). EPS 2015d.1 — Environmental Priority Strategies in product development. Swedish Life Cycle Center, Chalmers University.
- Anthoff, D. (2025). GIVE model — Global Impacts and Valuation of Emissions.
- Nordhaus, W., Barrage, L. (2024). DICE/RICE model update.
- Navrud, S. (2002). The State of the Art on Economic Valuation of Noise. EC DG Environment.
- Dekkers, J., van der Straaten, W. (2009). Monetary valuation of aircraft noise. *Ecological Economics*.
- Guski, R. et al. (2017). WHO Environmental Noise Guidelines for the European Region.
- Chen, J., Hoek, G. (2020). Long-term exposure to PM and all-cause and cause-specific mortality. *Environmental Health Perspectives*.
- WULCA (2021). AWARE v2 — Available Water Remaining characterisation factors.
- Psacharopoulos, G., Patrinos, H.A. (2018). Returns to investment in education: a decennial review of the global literature. *Education Economics*.
- World Bank (2025). World Development Indicators (GDP per capita PPP, deflators).
- IEA (2025). World Energy Balances.
- Karzai, S., Hirschfeld, J. (2024). Environmental costs of agricultural production. German Environment Agency working paper.

---

*Scripts: Dr Dimitrij Euler, Greenings (dimitrij.euler@greenings.org), with support of Claude Code (Anthropic) |
EPS Value Factors: Steen (2015), Swedish Life Cycle Center, Chalmers University |
WifOR Value Factors: WifOR Institute for Economic Research |
UBA Handbook: Nadia Eser, Dr. Astrid Matthey, Dr. Björn Bünger — German Environment Agency (UBA), December 2025 |
Document Version 2.0 | Last Updated 2026-03-05*
