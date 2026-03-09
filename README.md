# transitionvaluation

## 1. Project: Transition Valuation

## 2. Description:
This open-source repository contains resources for the valuation of corporate transitions to net zero. The intended users are researchers, analysts, and developers for academic and professional applications, primarily in the fields of sustainability and finance: asset owners, asset managers, impact valuation providers, policy-makers and regulators. This repo is curated by the project managers and sprint teams of the Transition Valuation Project under the custodianship of Greenings, the Swiss-based non-profit organization for sustainable transitions.

### Background and Context

The Transition Valuation Project represents a convergence of the **Impact Accounting** movement with the principles of **double materiality** as outlined in the EU Corporate Sustainability Reporting Directive (CSRD). For over 15 years, pioneering organizations including GIST Impact, Trucost, WifOR, PwC, KPMG, Capitals Coalition, Valuing Impact, and the German Environmental Agency (UBA) have been developing methodologies to better integrate external effects of business activities into corporate decision-making and financial reporting.

This initiative builds on:
- **Academic Research**: Collaboration with Oxford Net Zero, Frankfurt School of Finance, and leading universities
- **Industry Practice**: Value Balancing Alliance sprints with global financial institutions and corporations
- **Regulatory Alignment**: Methods designed for CSRD/ESRS, GRI, and ISSB standards
- **Open Science**: Published research including SSRN working papers on agile sustainable development

### Key Collaborators

This repository represents collaborative work from:
- **Value Balancing Alliance (VBA)** - Sprint coordination and methodology development
- **WifOR Institute** - Economic research and impact valuation frameworks
- **Greenings** - Custodian organization for sustainable transitions
- **Oxford Net Zero** - Academic research and user experience frameworks
- **Global Participants**: BNPP, Caixa, Deloitte, EY, KPMG, PwC, IFC, Mizuho, Novartis, Roche, S&P Global, UBS, WBCSD, and others

---

## 3. Installation and Setup

This repository contains multiple components for impact valuation. Please refer to the specific subdirectories for detailed installation instructions:

### Six value factor systems are available as submodules:

| Submodule | System | Geographic anchor | Price base | Indicators | Scale |
|-----------|--------|------------------|------------|------------|-------|
| `value-factors/` | WifOR | Global (already country-differentiated) | USD (mixed base years) | 8 | 188 countries × NACE |
| `stockholm-value-factors/` | EPS 2015d.1 (Steen / Sweden) | Sweden (globally applied) | EUR 2015 (ELU) | 12 | 189 countries × 21 NACE, 892 substances |
| `uba-value-factors/` | UBA MC 4.0 (Germany) | Germany (GHG: global) | EUR 2025 | 10 | 546 rows; Germany-specific |
| `cedelft-value-factors/` | CE Delft Env. Prices 2024 (EU27) | EU27 (no country variation) | EUR 2021 | 6 table groups | 114 rows; EU27 average |
| `uk-value-factors/` | UK Wellbeing & Health (HM Treasury) | United Kingdom | GBP (2019/2024) | 5 table groups | 72 rows; UK-specific |
| `valuingimpact-value-factors/` | eQALY (Valuing Impact) | Global (188 countries, country-varying) | USD 2023 | 6 | 188 countries × 21 NACE |

- **value-factors/** — WifOR Value Factors: environmental and social damage costs, country-differentiated
  - 8 indicators: GHG, Air Pollution, Water Consumption, Land Use, Water Pollution, Waste, OHS, Training
  - 188 countries with income- and population-adjusted coefficients; NACE A21 sectors
  - Multi-year projections (2014–2030, 2050, 2100); USD output via USA GDP deflator
  - License: Apache 2.0 (accept via `.license_accepted`)
  - Maintainer: WifOR Institute (wifor-impactanalysis/WifOR-Value-Factors)

- **stockholm-value-factors/** — EPS 2015d.1 characterisation factors (Steen, Chalmers University)
  - 12 LCIA impact categories: inorganic gases, particles, VOC, halogenated organics, emissions to water, pesticides, noise, radionuclides, land use, fossil resources, other elements, waste
  - 892 substances covering all major emission flows to air, water, and soil
  - 189 countries × 21 NACE sectors; EU HICP deflator-adjusted; years 2014–2100
  - Globally applied from Swedish anchor; all signs negative (damages); ELU ≈ EUR
  - Maintainer: Dr Dimitrij Euler, Greenings (d1mitrij/Stockholm_ValueFactors)

- **uba-value-factors/** — UBA Handbook on Environmental Value Factors, MC 4.0 (December 2025)
  - 10 table groups: GHG, air pollutants, electricity, heat, refrigerants, transport (veh-km + Pkm/tkm), noise, nitrogen/phosphorus, agriculture
  - 546 rows; Germany-specific for air/transport; global for GHG (GIVE model, Anthoff 2025)
  - Two PRTP scenarios (0 % and 1 %) for GHG-derived indicators; EUR 2025 price base
  - Source: Eser, Matthey, Bünger — German Environment Agency (UBA), December 2025; ISSN 2363-832X
  - Maintainer: Dr Dimitrij Euler, Greenings (d1mitrij/UBA_ValueFactors, branch `dima`)

- **cedelft-value-factors/** — CE Delft Environmental Prices Handbook 2024: EU27 version
  - 6 table groups: air pollutants (20), water pollutants (44), soil pollutants (21), land use (1), ReCiPe 2016 midpoints (19), PEF CAT I/II midpoints (9)
  - 114 rows; lower/central/upper uncertainty variants; EUR 2021 price level
  - Derivation: Impact Pathway Approach (IPA) with EEA/GAINS dispersion + ReCiPe 2016 H; no value transfer (direct EU27 average)
  - Source: De Vries et al., CE Delft, April 2025 (Version 1.1, Reference 230107)
  - Maintainer: Dr Dimitrij Euler, Greenings (d1mitrij/cedelft_vf, branch `dima`)

- **uk-value-factors/** — UK Wellbeing & Health Value Factors (HM Treasury / DCMS)
  - 5 table groups: WELLBY/QALY unit values (19), discount rates (8), cultural engagement health benefits per person (15), societal totals (13), workplace wellbeing parameters (17)
  - 72 rows; GBP 2019 / GBP 2024 price levels; UK-specific
  - Value transfer: WELLBY uprating via income elasticity (GDP/capita^1.3); geographic transfer via OECD (2025) guidance
  - Sources: HM Treasury Green Book 2026; Wellbeing Guidance 2021; OECD 2025; Frontier Economics / DCMS 2024
  - Maintainer: Dr Dimitrij Euler, Greenings (d1mitrij/greenbook_vf, branch `dima`)

- **valuingimpact-value-factors/** — eQALY Impact Valuation Method (Valuing Impact, 2025)
  - 6 indicators: HUI (health utility of income), HUT (health utility of taxes), wages (low/medium/high skill), health DALY rates (16 risk factors), NatCap pollution (16 LCA midpoints), NatCap land use (LANCA v2.0)
  - 188 countries × 21 NACE sectors; USD 2023 price base; HDF5 + Excel output
  - Value transfer: country-specific welfare adjustment via HUI and HUT multipliers (endogenous VT); LANCA v2.0 country-specific land values
  - Sources: IHME GBD 2019; ILO; World Bank; CE Delft; LANCA v2.0; OECD; IMF
  - Maintainer: Dr Dimitrij Euler, Greenings (d1mitrij/ValuingImpact_vf, branch `dima`)

Each submodule has its own setup requirements and documentation. Navigate to the relevant subdirectory and consult its README.md for specific installation steps.

**Value transfer across systems:** See `VALUE_TRANSFER.md` in this repository for a full description of how each indicator from EPS (Sweden anchor), UBA (Germany anchor), CE Delft (EU27 anchor), UK (GBP), and eQALY (188 countries, country-varying) can be integrated into the common WifOR coefficient matrix, covering same, similar, and unique indicators across all six systems.

### Core Documentation in This Repository

The following documents provide comprehensive guidance and research findings:

#### **Methodology and Architecture**
- **METHODOLOGY.md** - Detailed calculation methodology for value factors
- **ARCHITECTURE_DECISIONS.md** - Design rationale and architectural choices
- **INPUT_FILES_METHODOLOGY.md** - Data sources and methodological origins

#### **Reports and Research**
- **Impact_Valuation_Sprint_Report_2024_Final-1.md** (286 pages) - Comprehensive sprint findings from global collaboration
- **Valuing Impact Materiality Report_Final_20250227.md** (44 pages) - Methods for materiality thresholds and benchmarks under EU CSRD
- **ssrn-4545204.md** (47 pages) - "Agile Sustainable Development" working paper (Oxford/VBA)

#### **Implementation Guidance**
- **USABILITY_INTEGRATION_RECOMMENDATIONS.md** - User experience framework for decision-useful impact data
- **DATA_UPDATES.md** - Data maintenance and update procedures
- **VALIDATION_REPORT.md** - Quality assurance and validation results
- **TROUBLESHOOTING.md** - Common issues and solutions

#### **Project Management**
- **BACKLOG.md** - Feature roadmap and development priorities
- **DOCUMENTATION_UPDATE_RECOMMENDATIONS.md** - Documentation improvement strategy

---

## 4. Impact Valuation Methodology

### Framework Overview

The TVP methodology aligns with three complementary frameworks:

#### 1. IFVI/VBA Impact Accounting Methodology (2024)
**Public Good Baseline**
- Open-source, standardized approach
- VTPC governance oversight
- Starting with GHG and wages, expanding

**Core Principles:**
1. **Value to Society**: Holistic costs/benefits beyond financial
2. **Damage Cost Approach**: Monetary costs of damages where feasible
3. **Academic Foundation**: UBA, WHO, IPCC, peer-reviewed research
4. **Transparency**: All methodologies documented publicly

#### 2. Transparent NCMA Framework
**Natural Capital Management Accounting**
- Developed by VBA, Capitals Coalition, WBCSD, EU Commission
- Integrates with corporate accounting
- Aligns with EU Taxonomy DNSH
- Supports CSRD/ESRS compliance

#### 3. WifOR Economic Research Foundation
**15+ Years of Development**
- Evidence-based decision making
- Sustainable development focus
- Valid and comparable data
- Economic impact modeling

### Understanding "Damage or Value to Society"

**Critical Distinction:** The monetary values calculated in this repository represent **damage or value to society as a whole**, not legal liability or financial costs to the company.

#### What These Values Represent

**Damage or Value to Society:**
- Total external costs/benefits imposed on or provided to society
- Health impacts, environmental degradation, ecosystem services, human capital development
- Measured from society's perspective, not the entity's financial position
- Includes impacts on people who cannot or will not seek legal remedies
- Captures non-market values (clean air, biodiversity, worker well-being)

**Examples:**

| Impact | Societal Damage/Value | What It Is NOT |
|--------|----------------------|----------------|
| **GHG Emissions** | $200/ton CO2e in climate damages (global crop losses, flood damages, health impacts, ecosystem disruption) | Carbon tax paid by company, or potential lawsuit damages |
| **Air Pollution** | $5,000/ton PM2.5 in health costs (premature deaths, asthma, lost productivity across affected population) | Fines for permit violations, or settlements with neighbors |
| **Training** | +$25/hour in societal value (increased productivity, innovation, economic growth from skilled workforce) | Training budget cost, or ROI to the company |
| **Water Use** | $2/m³ in water scarcity damages (agricultural losses, ecosystem degradation, community water stress) | Water utility bills, or damages paid for over-extraction |

#### Why This Matters

**Societal damage/value is typically MUCH LARGER** than legal liability or company costs because:

1. **Comprehensive Scope**: All affected parties vs. only successful legal claimants
2. **Non-Market Impacts**: Ecosystem services, public health, climate stability (no legal owner to sue)
3. **Future Generations**: Long-term impacts beyond current legal frameworks
4. **Preventive Information**: Decision-making tool, not litigation provisioning

#### Intended Use Cases

These societal values support:
- **Impact Materiality Assessment** (CSRD/ESRS inside-out perspective)
- **Investment Decision-Making** (understanding true societal footprint)
- **Strategic Planning** (identifying high-impact activities for improvement)
- **Stakeholder Communication** (transparent disclosure of externalities)

They are **NOT designed for**:
- Calculating legal liability reserves
- Estimating lawsuit damages or settlements
- Determining compliance penalties or fines
- Financial accounting provisions

### Relationship to Double Materiality

```
┌─────────────────────────────────────────────┐
│        DOUBLE MATERIALITY ASSESSMENT        │
├─────────────────────┬───────────────────────┤
│  Financial          │  Impact               │
│  Materiality        │  Materialty          │
│  (outside-in)       │  (inside-out)         │
├─────────────────────┼───────────────────────┤
│  Effects of systems │  Effects of entity    │
│  ON entity          │  ON systems           │
│                     │                       │
│  - Transition risks │  - Environmental      │
│  - Physical risks   │    impacts ← TVP      │
│  - Opportunities    │  - Social impacts     │
└─────────────────────┴───────────────────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │  TVP Value Factors    │
           │  (Precursor Input)    │
           ├───────────────────────┤
           │  • Quantify impacts   │
           │  • Enable comparisons │
           │  • Support thresholds │
           │  • Does NOT define    │
           │    materialty alone  │
           └───────────────────────┘
```

**Key Point:** Impact valuation is a **tool** for materiality assessment, not a replacement for professional judgment, stakeholder engagement, or governance oversight.

### Key Use Cases for Impact Valuation

TVP's monetized impact values serve a broad range of decision-making contexts:

#### 1. Engagement
- **Due Diligence**: Assess material impacts of potential investments or acquisitions before commitment.
- **Operational Monitoring**: Track ongoing impact performance of portfolio companies or internal operations, driving continuous improvement.
- **Exit or De-investment**: Inform decisions to divest from entities with unmanageable negative impacts or poor engagement on sustainability issues.
- **Impact-Oriented Engagement**: Guide active ownership strategies or collaborative initiatives (e.g., Climate Action 100+).
  - **Thematic Screening**: Identify and engage with companies based on specific impact themes (e.g., water scarcity, biodiversity loss).
  - **Negative Screening**: Exclude companies from portfolios or supply chains based on unacceptable impact profiles.

#### 2. Risk Management
- **Transition Risk**: Quantify financial risks arising from the transition to a low-carbon economy (e.g., carbon pricing, stranded assets, regulatory changes).
- **Physical Risk**: Monetize physical impacts of climate change (e.g., asset damage from extreme weather, supply chain disruptions from resource scarcity).
- **Reputational Risk**: Assess the potential economic impact of negative public perception due to unmanaged social or environmental impacts.
- **Litigation Risk**: Evaluate potential liabilities from environmental damages or human rights violations.

#### 3. Regulatory Compliance
- **Jurisdiction-Specific Reporting**: Meet mandatory disclosure requirements across various legal environments (e.g., CSRD/ESRS in EU, TCFD globally, SEC climate rules in US).
- **Legal Environment Integration**: Align with national and international environmental and social legislation, ensuring compliance and proactive risk mitigation.
- **Standard Setting**: Inform development of future regulatory frameworks by providing robust, comparable impact data.

#### 4. Strategy & Public Policy
- **Corporate Strategy Development**: Integrate impact considerations into long-term business planning, R&D, and capital allocation decisions.
- **Public Policy Advocacy**: Provide evidence-based insights to support policy discussions on sustainable development, climate action, and social equity.
- **Scenario Analysis**: Model the financial implications of different policy pathways (e.g., carbon taxes, subsidies for green technologies).
- **Impact Investment Product Development**: Design and market financial products aligned with specific sustainability outcomes.

### Value Factor Categories

[Keep existing categories, add:]

#### Threshold Integration

TVP values can be integrated into materiality thresholds using the **Type 4 framework**:

| Element | Source | Integration |
|---------|--------|-------------|
| **Quantitative Impact** | TVP calculations | Monetary values by driver |
| **Comparability** | Sector benchmarks | Industry peer performance |
| **Specificity** | Location/activity data | Entity-specific context |
| **Scientific Basis** | Ecological thresholds | Planetary boundaries, SBTi |

**Result**: Highest usability for decision-makers (Type 4: high specificity + high comparability)

### Coverage Beyond Core 8 Factors

**Extensions in Development:**
- Biodiversity (ESRS E4) - Preservation costs, PDF, MSA
- Adequate Wages (ESRS S1) - Living wage gaps, HUI, WUI
- Child Labour (ESRS S1) - Lost education value
- Forced Labour (ESRS S1) - Mental health + exploitation
- DEI (ESRS S1) - Gender pay gaps (research phase)

**Climate Scenario Integration:**
- NGFS scenarios (MESSAGEix-GLOBIOM, GCAM, REMIND-MAgPIE)
- Transition pathways (Below 2°C, Net Zero 2050, Current Policies)
- Carbon pricing trajectories (region-specific)
---

## 5. Credits and License

Thank you to our collaborators at the Transition Valuation Initiative: www.greenings.org.

**Key Contributors:**
- Dimitrij Euler (Value Balancing Alliance / Greenings) - Director and Editor
- Dennis West (Oxford Net Zero) - Research and User Experience Framework
- WifOR Institute Team - Louisanne Knierim, Daniel Croner, Laura Hoffner
- Value Balancing Alliance - Clara Ulmer, Clarisse Machado, Magdalena Wottke, Francisco Ortin, Michael Verbücheln
- Global Sprint Participants from BNPP, Caixa, Datamaran, Deloitte, EY, Frankfurt School, GIST Impact, IFC, KPMG, Mizuho, Novartis, PwC, Roche, S&P Global, UBS, Upright Project, WBCSD, World Benchmarking Alliance, and others

**Citation:**
- VBA et al., Impact Valuation Sprint Report 2024, 2024, www.value-balancing.com
- VBA et al., Valuing Impact Materiality 2025, 2025, www.value-balancing.com
- West, D. & Euler, D., Agile Sustainable Development, SSRN Working Paper 4545204, 2023

Released under CC BY 4.0 Attribution 4.0: https://creativecommons.org/licenses/by/4.0/.

You are free to:
- **Share** — copy and redistribute the material in any medium or format for any purpose, even commercially.
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially.

The licensor cannot revoke these freedoms as long as you follow the license terms.

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **No additional restrictions** — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

---

## Contact & Support

**Organization**: Transition Valuation Project under Greenings custodianship

**Website**: www.greenings.org

**Value Balancing Alliance**: www.value-balancing.com

**Project Lead**: Dimitrij Euler (dimitrij.euler@greenings.org)

For specific component questions, please refer to the documentation in the relevant subdirectory.

---

## Repository Contents

```
transitionvaluation/
├── README.md                                           # This file
├── VALUE_TRANSFER.md                                   # Cross-system value transfer guide (WifOR / EPS / UBA)
│
├── Value Factor Submodules/
│   ├── value-factors/                                  # WifOR Value Factors (wifor-impactanalysis/WifOR-Value-Factors)
│   │     8 indicators · 188 countries · USD · Apache 2.0
│   ├── stockholm-value-factors/                        # EPS 2015d.1 (d1mitrij/Stockholm_ValueFactors)
│   │     12 categories · 892 substances · EUR 2015 (ELU) · Sweden anchor
│   ├── uba-value-factors/                              # UBA MC 4.0 (d1mitrij/UBA_ValueFactors, branch dima)
│   │     10 table groups · 546 rows · EUR 2025 · Germany anchor
│   ├── cedelft-value-factors/                          # CE Delft Env. Prices 2024 (d1mitrij/cedelft_vf, branch dima)
│   │     6 table groups · 114 rows · EUR 2021 · EU27 anchor · IPA direct derivation
│   ├── uk-value-factors/                               # UK Wellbeing & Health (d1mitrij/greenbook_vf, branch dima)
│   │     5 table groups · 72 rows · GBP 2019/2024 · UK anchor · WELLBY/QALY
│   └── valuingimpact-value-factors/                    # eQALY (d1mitrij/ValuingImpact_vf, branch dima)
│         6 indicators · 188 countries × 21 NACE · USD 2023 · HUI/HUT welfare VT
│
├── Core Documentation/
│   ├── METHODOLOGY.md                                  # Calculation methodology (WifOR-focused; see submodule docs for EPS/UBA)
│   ├── ARCHITECTURE_DECISIONS.md                       # Design rationale
│   ├── INPUT_FILES_METHODOLOGY.md                      # Data sources and methodological origins
│   ├── DATA_UPDATES.md                                 # Maintenance procedures
│   ├── VALIDATION_REPORT.md                            # Quality assurance (all three systems)
│   ├── ALGORITHMS_VISUAL.md                            # Pipeline flowcharts
│   └── TROUBLESHOOTING.md                              # Common issues
│
├── Reports and Research/
│   ├── Impact_Valuation_Sprint_Report_2024_Final-1.md  # 286-page sprint findings
│   ├── Valuing Impact Materiality Report_Final_20250227.md  # CSRD methods (44 pages)
│   └── ssrn-4545204.md                                 # Agile development research (47 pages)
│
└── Project Management/
    ├── BACKLOG.md                                      # Development roadmap
    ├── CONTRIBUTING_OPPORTUNITIES.md                   # Contribution guidance
    └── USER_GUIDES_BY_ROLE.md                          # Role-specific guidance
```
