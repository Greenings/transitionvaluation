# User Guides by Role

**Purpose**: Tailored guidance for different user profiles and their decision journeys

---

## ⚠️ IMPORTANT: Understanding "Damage or Value to Society"

**Before using these guides, understand what the monetary values represent:**

### What You're Calculating

All WifOR value factors represent **damage or value to society as a whole**, NOT:
- ❌ Your company's financial costs
- ❌ Legal liability or lawsuit damages
- ❌ Regulatory fines or penalties
- ❌ What you'll pay if sued

### Practical Examples by Role

#### For Sustainability Analysts
When you calculate "-$850 damage from PM2.5 emissions":
- ✓ This is **society's health burden** (hospital costs, lost productivity, mortality across affected population)
- ✗ This is NOT your company's fine or settlement amount

**Why it matters:** Use these values for impact materiality assessment, NOT for financial provisioning.

#### For Portfolio Managers
When you see "-$5M water impact" for a portfolio company:
- ✓ This is **society's water scarcity cost** (agricultural losses, ecosystem degradation, community stress)
- ✗ This is NOT the company's water utility bill or regulatory risk

**Why it matters:** Societal damage indicates impact materiality and stakeholder concerns, not financial exposure.

#### For Risk Managers
When analyzing "$200/ton CO2e":
- ✓ This is **global climate damage** (crop losses, floods, health impacts, adaptation costs)
- ✗ This is NOT current or future carbon tax rates

**Why it matters:** Use for scenario analysis of transition pathways, NOT for carbon price forecasting.

#### For CFOs/Financial Analysts
When reviewing impact reports with large negative values:
- ✓ These show your **total societal footprint** (externalities not reflected in P&L)
- ✗ These are NOT balance sheet liabilities or provisions needed

**Why it matters:** Impact valuation reveals sustainability dependencies and stakeholder risks, not direct financial obligations.

### Magnitude Comparison

**Typical relationship:**
```
Societal Damage/Value = 10-100× Legal/Financial Costs

Example:
- Societal air pollution damage: $5,000,000
- Company fine for violations: $50,000
- Ratio: 100:1
```

The gap represents **externalities** - costs society bears but the company doesn't (yet) pay for.

### When to Use Each Type of Value

| Decision Context | Use Societal Values | Use Legal/Financial Costs |
|-----------------|--------------------|--------------------------|
| Impact materiality (CSRD ESRS) | ✓ | ✗ |
| ESG/sustainability reporting | ✓ | ✗ |
| Strategic planning (reduce harm) | ✓ | ✗ |
| Stakeholder engagement | ✓ | ✗ |
| Financial provisioning | ✗ | ✓ |
| Risk reserves for lawsuits | ✗ | ✓ |
| Regulatory compliance budget | ✗ | ✓ |
| Insurance coverage | ✗ | ✓ |

---

## 1. For Sustainability Analysts (Corporate)

### Your Use Case
You need to prepare CSRD/ESRS reports and conduct double materiality assessments.

### Relevant Value Factors
- **ALL 8 indicators** for comprehensive impact assessment
- **Priority**: GHG, Water, OHS (commonly material under ESRS)

### Decision Journey
1. **Input Stage**: Collect activity data (emissions, water use, incidents)
2. **Processing**: Multiply activity data by WifOR coefficients
3. **Output**: Monetized impacts by country, sector, year
4. **Outcome**: Compare to thresholds for materiality determination
5. **Reporting**: Disclose material impacts in ESRS format

### Key Documentation
- Start: README.md → METHODOLOGY.md → INPUT_FILES_METHODOLOGY.md
- For CSRD: README.md Section 5 "Impact Materiality Assessment"
- For validation: VALIDATION_REPORT.md

### Example Workflow
```
Activity Data: 1,000 kg PM2.5 emissions in Germany, NACE C29 (Motor vehicles)

Step 1: Look up coefficient
  File: 2024-10-01_coefficients_AirPollution.xlsx
  Sheet: Coefficients
  Index: (2024, "PM2.5") × ("DEU", "C29")
  Value: -0.85 USD/kg (example)

Step 2: Calculate impact
  Impact = 1,000 kg × (-0.85 USD/kg) = -850 USD
  Interpretation: 850 USD damage to society

Step 3: Aggregate across all sites
  Total Air Pollution Impact: -45,000 USD (example)

Step 4: Compare to materiality threshold
  Threshold: 50,000 USD (example from ESRS guidance)
  Result: Below threshold → Not material (but close - monitor)
```

---

## 2. For Portfolio Managers (Investors)

### Your Use Case
ESG integration, portfolio carbon footprinting, impact-weighted accounts.

### Relevant Value Factors
- **Primary**: GHG (for all portfolios)
- **Secondary**: Water, Air, OHS (sector-dependent)
- **Focus**: Cross-company comparability

### Decision Journey
1. **Screening**: Identify high-impact companies
2. **Comparison**: Rank companies by impact intensity
3. **Allocation**: Tilt portfolio toward lower-impact firms
4. **Engagement**: Use impact data in stewardship
5. **Reporting**: Impact-weighted financial performance

### Key Features for You
- **Comparability**: Same methodology across all countries/sectors
- **Granularity**: Country-sector specific for portfolio analysis
- **Scenarios**: GHG climate scenarios for transition risk

### Example Use Case: Carbon Footprinting
```
Portfolio Holdings:
- Company A (Germany, Automotive): 100 shares, 500 tons CO2e/year
- Company B (USA, Tech): 200 shares, 50 tons CO2e/year

Step 1: Get GHG coefficients
  Germany, Automotive (NACE C29), 2024: -0.12 USD/kg CO2e
  USA, Tech (NACE J62), 2024: -0.15 USD/kg CO2e

Step 2: Calculate impacts
  Company A: 500,000 kg × (-0.12) = -60,000 USD
  Company B: 50,000 kg × (-0.15) = -7,500 USD

Step 3: Normalize by revenue (impact intensity)
  Company A: -60,000 USD / 10M revenue = -6 USD impact per 1,000 USD revenue
  Company B: -7,500 USD / 5M revenue = -1.5 USD impact per 1,000 USD revenue

  Result: Company B is 4× less carbon-intensive
```

---

## 3. For Procurement Officers

### Your Use Case
Supplier screening, sustainable sourcing, supply chain risk management.

### Relevant Value Factors
- **Sector-specific**: Depends on procurement category
  - Raw materials: Water Consumption, Water Pollution, Land Use
  - Manufacturing: GHG, Air Pollution, Waste
  - Services: Training, OHS

### Decision Journey
1. **RFQ/RFP**: Request supplier impact data
2. **Screening**: Calculate supplier impact using WifOR factors
3. **Comparison**: Rank suppliers by impact
4. **Contracting**: Include impact reduction targets in contracts
5. **Monitoring**: Track supplier performance over time

### Key Features for You
- **Sector-specific coefficients**: Match to supplier NACE codes
- **Country-specific**: Account for supplier location
- **Action-oriented**: Link to procurement decisions

### Example: Textile Supplier Selection
```
Scenario: Sourcing cotton textiles from two suppliers

Supplier A (India, NACE C13 - Textiles):
- Water consumption: 10,000 m³/year
- Water pollution: 500 kg phosphorus/year

Supplier B (Portugal, NACE C13 - Textiles):
- Water consumption: 8,000 m³/year
- Water pollution: 300 kg phosphorus/year

Step 1: Get coefficients
  Water Consumption India: -0.50 USD/m³ (example)
  Water Consumption Portugal: -0.30 USD/m³ (example)
  Water Pollution India: -40 USD/kg P (example, PPP-adjusted)
  Water Pollution Portugal: -130 USD/kg P (example, PPP-adjusted)

Step 2: Calculate total impact
  Supplier A: (10,000 × -0.50) + (500 × -40) = -5,000 - 20,000 = -25,000 USD
  Supplier B: (8,000 × -0.30) + (300 × -130) = -2,400 - 39,000 = -41,400 USD

Step 3: Contextual decision
  - Supplier A has higher water pollution impact despite lower water consumption
  - BUT: India PPP-adjusted values lower → absolute impact higher for Supplier B
  - Decision: Consider eutrophication risk in local context, not just monetary value
  - Action: Require both suppliers to implement water treatment, select based on credible reduction plans
```

---

## 4. For CFOs and Finance Teams

### Your Use Case
Enterprise value assessment, transition risk quantification, integrated reporting.

### Relevant Value Factors
- **Material impacts** from double materiality assessment
- **GHG** (always material for transition risk)
- **Financial materiality focus**: Link impacts to costs, revenues, risks

### Decision Journey
1. **Risk Identification**: Which impacts pose financial risks?
2. **Quantification**: Monetize impacts using WifOR factors
3. **Integration**: Link to financial statements
4. **Scenario Analysis**: Stress-test under different regulations
5. **Disclosure**: Integrated reporting, TCFD alignment

### Key Features for You
- **Monetary units**: Already in USD → directly comparable to financial metrics
- **Scenarios**: GHG climate scenarios for sensitivity analysis
- **Temporal consistency**: Inflation-adjusted across years

### Example: Transition Risk Assessment
```
Company: Cement manufacturer, 500,000 tons CO2e/year

Current State (2024):
  GHG coefficient (no carbon price internalized): -0.12 USD/kg CO2e
  Total societal damage: 500M kg × (-0.12) = -60M USD

Scenario: EU Carbon Border Adjustment Mechanism (CBAM) 2030
  Carbon price assumption: 0.10 USD/kg CO2e (regulatory cost)
  Financial impact: 500M kg × 0.10 = 50M USD/year additional cost

  Compare to:
  - Current EBITDA: 200M USD/year
  - CBAM would reduce EBITDA by 25%
  - Materiality: HIGH → Strategic response needed

Action: Board decision to invest in carbon capture (150M USD capex)
  Payback: 150M / 50M = 3 years
  NPV analysis: Use WifOR GHG scenarios for long-term carbon price projections
```

---

## 5. For Researchers and Academics

### Your Use Case
Impact valuation methodology research, validation studies, peer review.

### Relevant Value Factors
- **ALL** for methodological comparison
- **Focus on transparency**: Source studies, value transfer methods

### Decision Journey
1. **Literature Review**: Compare to other methodologies (GIST, Transparent, TruCost)
2. **Validation**: Benchmark against primary studies
3. **Extension**: Develop new indicators (biodiversity, wages)
4. **Publication**: Peer-reviewed papers, working papers

### Key Documentation for You
- **METHODOLOGY.md**: Detailed algorithms, formulas
- **INPUT_FILES_METHODOLOGY.md**: Data provenance, source studies
- **ARCHITECTURE_DECISIONS.md**: Design rationale (ADRs)
- **Impact_Valuation_Sprint_Report_2024_Final-1.md**: Comparison to 10+ other providers

### Critical Evaluation Criteria
1. **Comparability**: How does WifOR compare to CE Delft, GIST Impact, Transparent?
2. **Verifiability**: Can you reproduce coefficients from source data?
   - **Current limitation**: Excel pre-calculations (see BACKLOG.md S-VT1-VT3)
3. **Validity**: Do transferred values align with primary studies?
   - **Example**: Water Pollution PPP adjustment from Ahlroth (2009) Sweden study
4. **Reliability**: Sensitivity to value transfer parameters?
   - **Gap**: Elasticity parameters not disclosed (see BACKLOG.md Q8b)

### Collaboration Opportunities
- Contribute to BACKLOG.md improvement suggestions
- Participate in IFVI/VBA methodology development
- Validate against regional primary studies
- Extend to new indicators (biodiversity, adequate wages, DEI)
