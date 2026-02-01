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

- **value-factors/** - WifOR Value Factors implementation for calculating environmental and social impact coefficients
  - 8 sustainability indicators (GHG, Air Pollution, Water, Waste, Land Use, OHS, Training)
  - 188 countries with country-specific coefficients
  - Multi-year projections (2014-2030, 2050, 2100)
  - NACE sector granularity

Each component has its own setup requirements and documentation. Navigate to the relevant subdirectory and consult its README.md for specific installation steps.

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
tvp1/
├── README.md                                           # This file
├── value-factors/                                      # WifOR Value Factors implementation
│
├── Core Documentation/
│   ├── METHODOLOGY.md                                  # Calculation methodology
│   ├── ARCHITECTURE_DECISIONS.md                       # Design rationale
│   ├── INPUT_FILES_METHODOLOGY.md                      # Data sources
│   ├── USABILITY_INTEGRATION_RECOMMENDATIONS.md        # User experience framework
│   ├── DATA_UPDATES.md                                 # Maintenance procedures
│   ├── VALIDATION_REPORT.md                            # Quality assurance
│   └── TROUBLESHOOTING.md                              # Common issues
│
├── Reports and Research/
│   ├── Impact_Valuation_Sprint_Report_2024_Final-1.md  # 286-page sprint findings
│   ├── Valuing Impact Materiality Report_Final_20250227.md  # CSRD methods (44 pages)
│   └── ssrn-4545204.md                                 # Agile development research (47 pages)
│
└── Project Management/
    ├── BACKLOG.md                                      # Development roadmap
    └── DOCUMENTATION_UPDATE_RECOMMENDATIONS.md         # Documentation strategy
```
