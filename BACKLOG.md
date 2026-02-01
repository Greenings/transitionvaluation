# WifOR Value Factors - Backlog

**Organization**: Transition Valuation Project under Greenings custodianship
**Last Updated**: 2026-02-01

This document tracks open questions, improvement suggestions, and future work items for the WifOR Value Factors project.

---

## ONPV INTEGRATION (Based on ONPV_TVP_Integration_Guide.md)

### Overview

This section tracks tasks for integrating the four ONPV (Outcomes-based Net Present Value) differentiation steps with the existing TVP infrastructure.

| ONPV Step | TVP Status | Priority |
|:---|:---|:---|
| **Step 1: Value Factors** | Fully covered | Immediate |
| **Step 2: Exposure Factors** | Structure available | Short-term |
| **Step 3: Vulnerability Factors** | Not implemented | Medium-term |
| **Step 4: Attribution Factors** | Not implemented | Medium-term |

---

### Phase 1: Step 1 Integration (Immediate)

#### High Priority
- **ONPV-1.1**: Update Step1_Value_Factors_Methodology.md to reference TVP value-factors
  - Add TVP integration section with code examples
  - Document HDF5 output loading patterns
  - Reference METHODOLOGY.md and INPUT_FILES_METHODOLOGY.md
  - Owner: TBD
  - Estimated effort: 1-2 days

- **ONPV-1.2**: Align coefficient tables with TVP output structure
  - Validate consistency between ONPV parameters and TVP methodology
  - Document any parameter differences (SDR, VSL, base year)
  - Owner: TBD
  - Estimated effort: 1-2 days

- **ONPV-1.3**: Create coefficient loading utility functions
  - Add functions to load all 8 indicators from HDF5
  - Include example Jupyter notebook
  - Owner: TBD
  - Estimated effort: 2-3 days

---

### Phase 2: Step 2 Module (Short-term)

#### High Priority
- **ONPV-2.1**: Create `exposure-factors/` folder structure
  - README.md with methodology overview
  - config.yaml following TVP pattern
  - exposure_factor_utils.py for common functions
  - Owner: TBD
  - Estimated effort: 1-2 days

- **ONPV-2.2**: Build ENCORE → NACE sector mapping
  - Source ENCORE sector dependency data
  - Create mapping table to TVP NACE sectors
  - Validate coverage (all TVP sectors mapped)
  - Owner: TBD
  - Estimated effort: 3-5 days

- **ONPV-2.3**: Develop SASB materiality integration
  - Download SASB industry materiality map
  - Map to TVP NACE sectors
  - Create Human Capital exposure scores
  - Owner: TBD
  - Estimated effort: 3-5 days

#### Medium Priority
- **ONPV-2.4**: Implement four-capital scoring methodology
  - Script: 001_prepare_NaturalCapital_ENCORE.py
  - Script: 002_prepare_HumanCapital_SASB.py
  - Script: 003_prepare_SocialCapital.py
  - Script: 004_prepare_BuiltCapital.py
  - Owner: TBD
  - Estimated effort: 10-15 days

- **ONPV-2.5**: Create exposure factor output files
  - Follow TVP HDF5/Excel output pattern
  - Include metadata sheet with methodology reference
  - Owner: TBD
  - Estimated effort: 2-3 days

---

### Phase 3: Step 3 Module (Medium-term)

#### High Priority
- **ONPV-3.1**: Create `vulnerability-factors/` folder structure
  - README.md with methodology overview
  - config.yaml with QMS weights and data sources
  - vulnerability_utils.py for common functions
  - Owner: TBD
  - Estimated effort: 1-2 days

- **ONPV-3.2**: Integrate Climate Action Tracker (CAT) data
  - Source CAT country ratings
  - Map to TVP 188-country list
  - Create country-level vulnerability scores
  - Owner: TBD
  - Estimated effort: 3-5 days

- **ONPV-3.3**: Integrate IEA sector pathway data
  - Source IEA Net Zero scenario data
  - Map sectors to TVP NACE classification
  - Create sector-level vulnerability scores
  - Owner: TBD
  - Estimated effort: 3-5 days

#### Medium Priority
- **ONPV-3.4**: Implement Quantified Management Scorecard (QMS)
  - Define scoring rubric for Target Ambition
  - Define scoring rubric for Disclosure Quality
  - Define scoring rubric for Track Record
  - Create composite QMS calculation
  - Owner: TBD
  - Estimated effort: 5-7 days

- **ONPV-3.5**: Add Just Transition Readiness scoring
  - Integrate MDB 5 Principles
  - Create scoring methodology per principle
  - Add to composite vulnerability calculation
  - Owner: TBD
  - Estimated effort: 3-5 days

- **ONPV-3.6**: Integrate SBTi and CDP data sources
  - Source SBTi company database
  - Source CDP disclosure scores
  - Map to company-level management scores
  - Owner: TBD
  - Estimated effort: 5-7 days

---

### Phase 4: Step 4 Module (Medium-term)

#### High Priority
- **ONPV-4.1**: Create `attribution-factors/` folder structure
  - README.md with methodology overview
  - config.yaml with equity tiers and debt base rates
  - attribution_utils.py for common functions
  - Owner: TBD
  - Estimated effort: 1-2 days

- **ONPV-4.2**: Implement tiered equity attribution
  - Script: 001_calculate_EquityAttribution.py
  - Implement Tier 1/2/3 control factors
  - Include engagement level assessment
  - Owner: TBD
  - Estimated effort: 3-5 days

- **ONPV-4.3**: Build debt attribution with distress multiplier
  - Script: 002_calculate_DebtAttribution.py
  - Implement base rate by credit quality
  - Add covenant factor scoring
  - Implement Z-Score based distress multiplier
  - Owner: TBD
  - Estimated effort: 5-7 days

#### Medium Priority
- **ONPV-4.4**: Add MDB instrument type adjustments
  - Implement green bond discount
  - Implement sustainability-linked bond discount
  - Add adaptation activity type credits
  - Owner: TBD
  - Estimated effort: 2-3 days

- **ONPV-4.5**: Create portfolio aggregation tools
  - Script: 004_apply_PortfolioAttribution.py
  - Sum attributed impacts across positions
  - Generate portfolio-level reports
  - Owner: TBD
  - Estimated effort: 3-5 days

---

### Phase 5: Integration Module (Future)

#### Medium Priority
- **ONPV-5.1**: Create end-to-end calculation pipeline
  - Script: integration/calculate_differentiated_impact.py
  - Chain Steps 1-4 calculations
  - Allow step-by-step or full pipeline execution
  - Owner: TBD
  - Estimated effort: 5-7 days

- **ONPV-5.2**: Create reporting templates
  - Excel report template with all steps
  - Summary dashboard visualization
  - Comparison to benchmarks
  - Owner: TBD
  - Estimated effort: 3-5 days

- **ONPV-5.3**: Add validation and quality checks
  - Cross-step consistency validation
  - Range checks for all factors
  - Automated testing for pipeline
  - Owner: TBD
  - Estimated effort: 3-5 days

---

### Data Sources Required

| Step | Data Source | Availability | Action |
|:---|:---|:---|:---|
| Step 1 | TVP value-factors | Available | Direct use |
| Step 2 | ENCORE | Public | Download and map |
| Step 2 | SASB Materiality Map | Public | Download and map |
| Step 3 | Climate Action Tracker | Public | API or scrape |
| Step 3 | IEA Net Zero | Licensed | Acquire license |
| Step 3 | SBTi Database | Public | Download |
| Step 3 | CDP Scores | Licensed | Acquire license |
| Step 4 | Bloomberg/Refinitiv | Licensed | Acquire license |
| Step 4 | SEC EDGAR | Public | API access |

---

## OPEN QUESTIONS

### Data Quality & Methodology

#### High Priority
- **Q1**: Why do Water Consumption and Water Pollution have "Experimental" maturity status with "results hard to explain"?
  - Action: Review methodology and validate against independent sources
  - Owner: TBD
  - Timeline: TBD

- **Q2**: Should we update the 2022-dated input files (6 out of 8 scripts use 2022 data)?
  - Action: Contact data providers for latest versions
  - Affected scripts: 007, 008, 009, 014, 015
  - Owner: TBD
  - Timeline: TBD

- **Q3**: Why is USA inflation applied globally instead of country-specific deflators?
  - Current: All countries adjusted using USA GDP deflator
  - Alternative: Use country-specific World Bank deflators (already in input data)
  - Impact: May significantly change country-relative values
  - Decision needed: Is this methodologically sound or legacy constraint?

#### Medium Priority
- **Q4**: What happens for deflator years beyond available data (2050, 2100)?
  - Current behavior: Uses last available deflator year (typically 2023)
  - Question: Should we extrapolate inflation or use different approach?

- **Q5**: How are country code mismatches handled systematically?
  - Current: Hard-coded mappings (SSD→SDS, SDN→SUD) in some scripts
  - Question: Is there a master mapping table? Are there other mismatches?

- **Q6**: Why does GHG use 2019 base year while all others use 2020?
  - Question: Is this intentional due to DICE model timing, or should we harmonize?

#### Low Priority
- **Q7**: What is the rationale for zero-cost "recovered" waste types?
  - Current: Recovery has coefficient = 0
  - Question: Does recovery really have zero environmental cost/benefit?

### Calculation Transparency

#### High Priority - Value Transfer Mechanisms (NEW FOCUS AREA)
- **Q8**: What formulas are embedded in the 6 Excel input files?
  - Current: Pre-calculated values loaded from Excel, calculation logic not in Python
  - **CRITICAL**: Value transfer calculations (PPP, income elasticity) are "black box"
  - Action: Extract and document Excel formulas
  - Affected: 007, 008, 009, 010, 013, 015
  - **Related to**: ADR-012 (Value Transfer in Pre-Calculation Phase)

- **Q9**: Can we migrate Excel-based calculations to Python for full transparency?
  - Current: 6 scripts depend on Excel pre-calculations
  - Benefit: Version control, reproducibility, transparency
  - Effort: High (requires understanding original Excel logic)
  - **Priority Elevated**: Value transfer transparency is CRITICAL for IFVI/VBA alignment

- **Q8a** (NEW): What PPP indices and base years were used for value transfer?
  - Current: PPP adjustment applied in Water Pollution and Training, but indices not documented
  - Action: Identify PPP data source (World Bank? OECD? Year?)
  - Affected: 013 (Water Pollution), 014 (Training)
  - Estimated effort: 1-2 days (if Excel files accessible)

- **Q8b** (NEW): What income elasticity parameters are used for VSL adjustment?
  - Current: Air Pollution uses income elasticity, but parameter not documented
  - Action: Extract elasticity value (typically 0.8-1.2)
  - Affected: 008 (Air Pollution)
  - Estimated effort: 1 day

#### Medium Priority
- **Q10**: How were Training value-per-hour coefficients calculated?
  - Input: HDF5 file with pre-calculated "value_per_hour_GVA_2020USD_PPP"
  - Question: Where is the calculation code? Can we document or open-source it?
  - **NEW**: Particularly important to document PPP adjustment methodology

- **Q11**: What is the full GHG scenario naming convention?
  - Current: Multiple scenarios in output, naming not fully documented
  - Action: Document all scenario names and their parameter assumptions

### Data Governance

#### High Priority
- **Q12**: How are input data files versioned?
  - Current: Date prefixes in filenames (YYMMDD_)
  - Question: Should we use formal version control (e.g., DVC, Git LFS)?

- **Q13**: Who has authority to update input data files?
  - Question: Approval process for data updates?
  - Question: How to ensure backward compatibility?

#### Medium Priority
- **Q14**: What is the data refresh schedule?
  - Question: How often should each indicator be updated?
  - Question: Are some indicators more time-sensitive than others?

- **Q15**: How do we handle input data schema changes?
  - Current: Scripts expect specific Excel sheet names, column names
  - Question: Should we add schema validation?

---

## IMPROVEMENT SUGGESTIONS

### Overview

This section contains **93+ improvement tasks** organized by category and priority:

**NEW CRITICAL CATEGORIES** (Added 2026-01-02):
1. **Value Transfer Transparency** (S-VT1 to S-VT6) - Migrate Excel pre-calculations to Python for full transparency
2. **Usability and User Experience** (S-UX1 to S-UX15) - Make value factors decision-useful for diverse user profiles

**Existing Categories**:
3. **Code Quality** (S1-S8) - Testing, validation, logging
4. **Data Management** (S9-S15) - Versioning, updates, quality checks
5. **Documentation** (S16-S20) - Guides, examples, FAQs
6. **Features** (S21-S24) - New capabilities, performance
7. **Infrastructure** (S25-S28) - CI/CD, deployment, monitoring

**Implementation Timeline**:
- **Q1 2026**: Foundation (S-UX1-3, S-VT1) - 10-15 days total
- **Q2 2026**: Enhancement (S-UX4-7, S-VT2-3) - 20-30 days total
- **Q3 2026**: Validation (S-UX8-11, S-VT4) - 25-35 days total
- **Q4 2026+**: Standardization (S-UX12-15, S-VT5-6) - Ongoing

---

### Value Transfer Transparency (NEW CRITICAL CATEGORY)

#### High Priority
- **S-VT1**: Extract and document value transfer parameters from Excel files
  - Action: Open Excel files, extract formulas for PPP/income elasticity adjustments
  - Document: PPP indices source and base year, income elasticity values
  - Create: VALUE_TRANSFER_PARAMETERS.md documentation file
  - Benefit: Transparency, reproducibility, external validation possible
  - Estimated effort: 3-5 days
  - **Priority**: CRITICAL for IFVI/VBA alignment and external audits

- **S-VT2**: Create value transfer validation report
  - Compare transferred values against known benchmarks
  - Example: Compare USA air pollution VSL to OECD published estimates
  - Example: Validate PPP-adjusted water values against regional studies if available
  - Create: VALUE_TRANSFER_VALIDATION.md
  - Benefit: Quality assurance, identify potential errors
  - Estimated effort: 5-7 days
  - **Priority**: HIGH for credibility

- **S-VT3**: Implement value transfer in Python (Phase 1: Parallel verification)
  - Don't replace Excel yet, implement alongside for verification
  - Add PPP indices to input data (World Bank or OECD)
  - Add GDP per capita data for income elasticity
  - Implement transfer functions in value_factor_utils.py
  - Compare outputs to Excel-generated values
  - Benefit: Verify Excel calculations, prepare for migration
  - Estimated effort: 10-15 days
  - **Priority**: HIGH (prerequisite for S-VT4)

#### Medium Priority
- **S-VT4**: Migrate value transfer to Python (Phase 2: Full migration)
  - After S-VT3 validation successful, replace Excel pre-calculations
  - Make value transfer parameters configurable (allow users to update PPP/elasticity)
  - Add sensitivity analysis capability
  - Deprecate Excel input files (or reduce to raw data only)
  - Benefit: Full transparency, version control, user configurability
  - Estimated effort: 15-20 days
  - **Prerequisites**: S-VT1, S-VT3 completed

- **S-VT5**: Add alternative value transfer methods as options
  - Current: Single method per indicator (PPP or income elasticity)
  - Enhancement: Allow users to select transfer method
  - Example: OHS could optionally use income-adjusted DALY instead of global value
  - Benefit: Flexibility, sensitivity analysis, methodological comparison
  - Estimated effort: 5-7 days
  - **Prerequisites**: S-VT4 completed

#### Low Priority
- **S-VT6**: Country-specific primary studies for high-impact countries
  - Identify top 10-20 countries by economic size or environmental impact
  - Commission or collect primary valuation studies where available
  - Replace transferred values with primary values where quality higher
  - Benefit: Improved accuracy for major economies
  - Estimated effort: Ongoing (external research required)
  - **Timeline**: Long-term (2-5 years)

### Code Quality

#### High Priority
- **S1**: Add input data validation
  - Check required columns exist
  - Validate data types and ranges
  - Detect missing countries or sectors
  - Estimated effort: 2-3 days

- **S2**: Add output validation tests
  - Verify all coefficients have correct sign (Training positive, others negative)
  - Check all 188 countries present
  - Validate unit consistency
  - Test temporal continuity
  - Estimated effort: 3-4 days

- **S3**: Create unit tests for value_factor_utils.py
  - Test all 11 utility functions
  - Mock data for reproducible tests
  - Estimated effort: 2-3 days

#### Medium Priority
- **S4**: Add logging throughout scripts
  - Current: Minimal logging
  - Benefit: Easier debugging, audit trail
  - Estimated effort: 1-2 days

- **S5**: Implement data schema validation
  - Use libraries like Pydantic or Pandera
  - Validate input files before processing
  - Estimated effort: 2-3 days

- **S6**: Add pre-commit hooks
  - Black formatting
  - Isort import sorting
  - Type checking with mypy
  - Estimated effort: 1 day

#### Low Priority
- **S7**: Add type hints throughout codebase
  - Current: Minimal type annotations
  - Benefit: Better IDE support, catch errors earlier
  - Estimated effort: 3-4 days

- **S8**: Create performance benchmarks
  - Track execution time over time
  - Identify optimization opportunities
  - Estimated effort: 1-2 days

### Data Management

#### High Priority
- **S9**: Implement data versioning strategy
  - Use DVC or Git LFS for large files
  - Track input file versions with outputs
  - Estimated effort: 2-3 days

- **S10**: Create data update automation
  - Scripts to fetch latest data from sources
  - Automated validation after updates
  - Estimated effort: 5-7 days

- **S11**: Add data provenance tracking
  - Log which input file versions produced which outputs
  - Timestamped execution metadata
  - Estimated effort: 2-3 days

#### Medium Priority
- **S12**: Create data quality dashboard
  - Visualize data vintage by indicator
  - Track maturity status
  - Show coverage gaps
  - Estimated effort: 3-5 days

- **S13**: Implement output comparison tool
  - Compare outputs across runs
  - Detect unexpected changes
  - Estimated effort: 2-3 days

### Documentation

#### High Priority
- **S14**: Document Excel calculation formulas
  - Extract formulas from 6 Excel input files
  - Create formula documentation
  - Estimated effort: 3-5 days

- **S15**: Create video tutorials
  - Installation and setup
  - Running scripts
  - Interpreting outputs
  - Estimated effort: 2-3 days

#### Medium Priority
- **S16**: Add inline code comments
  - Current: Minimal inline comments
  - Focus on complex transformations
  - Estimated effort: 2-3 days

- **S17**: Create API documentation
  - Auto-generate from docstrings using Sphinx
  - Host on Read the Docs
  - Estimated effort: 2-3 days

#### Low Priority
- **S17a**: Standardize terminology across core documentation (Priority 3 from consistency review)
  - **Files to update**: ARCHITECTURE_DECISIONS.md, VALIDATION_REPORT.md, CONTRIBUTING_OPPORTUNITIES.md
  - **Changes**:
    - ARCHITECTURE_DECISIONS.md: Replace "societal costs" with "damage or value to society"
    - VALIDATION_REPORT.md: Replace "damage cost indicators" with "damage to society indicators"
    - CONTRIBUTING_OPPORTUNITIES.md: Replace "damage/benefit coefficients" with "damage or value to society coefficients"
  - **Rationale**: Ensure consistent terminology matching updated user-facing documentation
  - **Impact**: Low - meanings are already clear, this improves consistency
  - **Estimated effort**: 0.5 days (simple search-replace with review)
  - **Status**: Identified 2026-01-02 during documentation consistency audit
  - **Priority**: Low - cosmetic improvement, no functional impact

### Functionality Enhancements

#### High Priority
- **S18**: Support custom year ranges
  - Current: Hard-coded 2014-2030, 2050, 2100
  - Allow users to specify custom years
  - Estimated effort: 2-3 days

- **S19**: Add scenario comparison for GHG
  - Built-in tools to compare GHG scenarios
  - Visualization of scenario differences
  - Estimated effort: 3-4 days

#### Medium Priority
- **S20**: Support partial execution
  - Run only specific indicators
  - Skip indicators with up-to-date outputs
  - Estimated effort: 2-3 days

- **S21**: Add interactive configuration wizard
  - Guide users through config.yaml setup
  - Validate settings before execution
  - Estimated effort: 3-4 days

- **S22**: Create output visualization tools
  - Built-in plotting functions
  - Country/sector/year comparisons
  - Estimated effort: 4-5 days

#### Low Priority
- **S23**: Support additional output formats
  - Current: HDF5 + Excel
  - Add: CSV, Parquet, SQLite
  - Estimated effort: 2-3 days

- **S24**: Add parallel country processing
  - Current: Sequential country processing within scripts
  - Potential speedup: 2-4x
  - Estimated effort: 3-4 days

### Usability and User Experience (NEW - Based on SSRN-4545204 Analysis)

#### High Priority (Phase 1: Foundation - Q1 2026)
- **S-UX1**: Add "Relevance to Standards" section to README.md
  - Create alignment table: WifOR indicators → CSRD/ESRS topics
  - Map to SDG targets (Goals 3, 6, 7, 8, 12, 13, 15)
  - Show ISSB/TCFD compatibility (Governance, Strategy, Risk, Metrics)
  - Benefit: Users can assess if value factors meet regulatory requirements
  - Estimated effort: 2-3 days
  - **Status**: ✅ Recommendations created in USABILITY_INTEGRATION_RECOMMENDATIONS.md
  - **Related to**: SSRN paper Section III "Information User Profiles"

- **S-UX2**: Create USER_GUIDES_BY_ROLE.md with 5 user profiles
  - **Profile 1**: Sustainability Analysts (CSRD reporting)
  - **Profile 2**: Portfolio Managers (ESG integration)
  - **Profile 3**: Procurement Officers (Supplier screening)
  - **Profile 4**: CFOs (Enterprise value, transition risk)
  - **Profile 5**: Researchers (Methodology validation)
  - Each profile includes: Use case, relevant factors, decision journey, example workflow
  - Benefit: Role-specific guidance improves adoption and correct usage
  - Estimated effort: 5-7 days
  - **Priority**: CRITICAL for user adoption

- **S-UX3**: Add "Output File Standards" section to DATA_UPDATES.md
  - Document naming convention: YYYYMMDD_coefficients_IndicatorName.{xlsx,h5}
  - Standardize Excel structure (Coefficients, Units, Metadata sheets)
  - Define HDF5 structure standards
  - Create abbreviations and terminology table
  - Benefit: Consistency → easier integration, fewer user errors
  - Estimated effort: 1-2 days

#### Medium Priority (Phase 2: Enhancement - Q2 2026)
- **S-UX4**: Add Metadata sheet to all Excel outputs
  - Update all 8 preparation scripts to generate metadata
  - Fields: base_year, deflator_country, value_transfer_method, source_study, last_updated, script_version
  - Benefit: Enhanced verifiability → users can trace methodology
  - Estimated effort: 5-7 days (update 8 scripts + testing)
  - **Related to**: ADR-012 (Value Transfer transparency)
  - **Prerequisites**: None (can start immediately)

- **S-UX5**: Create DECISION_USEFULNESS_ASSESSMENT.md
  - Evaluate each indicator against quality characteristics:
    - Relevance to user decisions
    - Comparability across entities/periods
    - Verifiability (can results be reproduced?)
    - Timeliness (update frequency adequate?)
    - Understandability (clear for target audience?)
  - Identify gaps and improvement priorities per indicator
  - Benefit: Data-driven prioritization of documentation/methodology improvements
  - Estimated effort: 4-5 days

- **S-UX6**: Add "Common Decision Journeys" examples to METHODOLOGY.md
  - Example 1: Strategic decision-making (capital allocation using GHG scenarios)
  - Example 2: Operational decisions (procurement using water factors)
  - Example 3: Financial reporting (materiality assessment using all 8 factors)
  - Show logic model: Inputs → Activities → Outputs → Outcomes → Impacts → Valuation
  - Benefit: Users understand how to apply value factors in context
  - Estimated effort: 3-4 days

- **S-UX7**: Create visual decision journey diagrams
  - Add to ALGORITHMS_VISUAL.md
  - Diagram 1: User profile mapping (14 user types → relevant indicators)
  - Diagram 2: Decision journey flowchart (from data collection to action)
  - Diagram 3: Logic model with example calculations
  - Tool: Mermaid diagrams or similar
  - Benefit: Visual learners, onboarding new users
  - Estimated effort: 2-3 days

#### Medium Priority (Phase 3: Validation - Q3 2026)
- **S-UX8**: Conduct user testing with 3-5 real users
  - Recruit from different profiles: 1 analyst, 1 portfolio manager, 1 procurement officer, 1 CFO, 1 researcher
  - Task-based testing: "Calculate impact for your use case"
  - Observe: Where do users get stuck? What's confusing?
  - Document: Pain points, feature requests, usability issues
  - Benefit: Real-world validation of documentation effectiveness
  - Estimated effort: 10-15 days (recruitment, testing, analysis)
  - **Prerequisites**: S-UX2 completed (user guides must exist)

- **S-UX9**: Survey user satisfaction on quality characteristics
  - Questions (1-5 scale):
    - Comparability: "Can you compare impacts across companies/countries?"
    - Verifiability: "Can you trace coefficients to source studies?"
    - Timeliness: "Is data fresh enough for your decisions?"
    - Understandability: "Is documentation clear and actionable?"
  - Target: ≥4.0 average across all characteristics
  - Distribution: Email to known users, GitHub discussions, LinkedIn
  - Benefit: Quantitative baseline for improvement tracking
  - Estimated effort: 3-5 days (survey design, distribution, analysis)

- **S-UX10**: Document findings in USER_FEEDBACK_REPORT.md
  - Summary of user testing results (S-UX8)
  - Summary of satisfaction survey (S-UX9)
  - Identified usability issues (prioritized)
  - Action plan for Phase 4 improvements
  - Benefit: Transparent, evidence-based improvement roadmap
  - Estimated effort: 2-3 days
  - **Prerequisites**: S-UX8, S-UX9 completed

- **S-UX11**: Prioritize usability improvements based on feedback
  - Categorize issues: Critical / High / Medium / Low
  - Estimate effort for each improvement
  - Create timeline for implementation
  - Update BACKLOG.md with new tasks
  - Benefit: User-driven development priorities
  - Estimated effort: 1-2 days
  - **Prerequisites**: S-UX10 completed

#### Low Priority (Phase 4: Standardization - Q4 2026 and beyond)
- **S-UX12**: Align with IFVI/VBA General Methodology 1 user definitions
  - Review IFVI/VBA GM1 user profile definitions (paragraph 22)
  - Update TVP documentation to match terminology
  - Cross-reference IFVI/VBA methodologies where applicable
  - Benefit: Consistency with global impact valuation standards
  - Estimated effort: 3-5 days
  - **Timeline**: When IFVI/VBA GM1 finalized (ongoing)

- **S-UX13**: Contribute to ESRS implementation guidance
  - Participate in EFRAG working groups (if invited)
  - Provide case studies using WifOR value factors for ESRS compliance
  - Publish blog posts/guides on "Using WifOR for CSRD"
  - Benefit: Industry adoption, thought leadership
  - Estimated effort: Ongoing (5-10 days per contribution)
  - **Timeline**: As ESRS implementation progresses (2026-2027)

- **S-UX14**: Participate in ISSB/GRI alignment initiatives
  - Monitor ISSB-GRI interoperability work
  - Ensure WifOR value factors compatible with both frameworks
  - Contribute to public consultations
  - Benefit: Multi-framework compatibility → broader user base
  - Estimated effort: Ongoing (3-5 days per consultation)
  - **Timeline**: As standards evolve

- **S-UX15**: Publish academic paper on decision-usefulness of value factors
  - Title: "Decision-Usefulness of Monetized Impact Factors: Evidence from User Studies"
  - Authors: WifOR team + academic collaborators
  - Content: User testing results (S-UX8-11), methodological innovations, usability framework
  - Venue: Accounting, Organizations and Society or similar
  - Benefit: Academic credibility, attract researcher users
  - Estimated effort: 20-30 days (writing, peer review, revisions)
  - **Timeline**: Submit Q4 2026, publish 2027
  - **Prerequisites**: S-UX8-11 completed (need empirical data)

### Infrastructure

#### High Priority
- **S25**: Set up continuous integration (CI)
  - GitHub Actions for automated testing
  - Run on each commit/PR
  - Estimated effort: 2-3 days

- **S26**: Create Docker container
  - Reproducible environment
  - Easier deployment
  - Estimated effort: 2-3 days

#### Medium Priority
- **S27**: Add monitoring/alerting
  - Track script execution failures
  - Alert on data anomalies
  - Estimated effort: 3-4 days

- **S28**: Create cloud deployment guide
  - AWS/GCP/Azure setup
  - Automated data pipeline
  - Estimated effort: 3-5 days

---

## TECHNICAL DEBT

### Code Refactoring Needed
- **TD1**: Hard-coded country mappings (SSD→SDS, SDN→SUD)
  - Location: Multiple scripts
  - Solution: Centralize in config or mapping file

- **TD2**: Inconsistent base year (2019 for GHG, 2020 for others)
  - Location: config.py
  - Solution: Document rationale or harmonize

- **TD3**: Magic numbers in code (e.g., 1000 for tonnes to kg)
  - Location: 020_241024_prepare_GHG_my.py
  - Solution: Define as named constants

- **TD4**: Repetitive transpose operations
  - Location: All scripts
  - Solution: Create utility function for common pattern

### Data Issues
- **TD5**: Excel files as primary data source (not version-controlled)
  - Impact: 6 out of 8 scripts
  - Solution: Migrate to structured formats (HDF5, Parquet)

- **TD6**: No automated data validation
  - Impact: Silent failures possible
  - Solution: Add schema validation (S5)

- **TD7**: Data vintage inconsistency (2022-2024)
  - Impact: Some indicators based on older data
  - Solution: Establish refresh schedule (S10)

### Documentation Gaps
- **TD8**: Calculation logic in Excel, not documented in code
  - Impact: 6 scripts non-transparent
  - Solution: Extract formulas (S14)

- **TD9**: No change log for input data updates
  - Impact: Hard to track what changed
  - Solution: Data versioning (S9)

---

## RESEARCH QUESTIONS

### Methodology Improvements
- **R1**: Can we improve Water Consumption methodology to reduce "Experimental" status?
  - Current issue: "High uncertainty, results hard to explain"
  - Potential: Review alternative methodologies (e.g., different AWARE factors)

- **R2**: Can we improve Water Pollution methodology?
  - Current issue: "Experimental" status
  - Potential: Validate against independent studies

- **R3**: Should Training consider diminishing returns?
  - Current: Linear returns to training hours
  - Question: Is there empirical support for linearity?

- **R4**: Should we add sector-specific coefficients for more indicators?
  - Current: Only Training has sector differentiation
  - Question: Do waste/pollution damages vary by sector?

### New Indicators
- **R5**: What other environmental/social indicators should be added?
  - Candidates: Biodiversity, noise pollution, resource depletion
  - Priority: Based on user demand

- **R6**: Should we add positive environmental coefficients?
  - Example: Carbon sequestration, renewable energy generation
  - Current: Only Training is positive (social)

### Cross-Indicator Analysis
- **R7**: How do indicators interact?
  - Example: Air pollution from waste incineration (double counting?)
  - Need: Cross-indicator consistency checks

- **R8**: Can we create composite indicators?
  - Example: Total environmental footprint
  - Challenge: Different units (kg, m3, ha)

---

## EXTERNAL DEPENDENCIES

### Data Provider Relationships
- **E1**: Establish formal data sharing agreements
  - OECD Data Explorer
  - World Bank
  - German Federal Environment Agency (UBA)

- **E2**: Clarify data usage licenses
  - Current: Unclear for some sources
  - Action: Document licenses for each input file

### Software Dependencies
- **E3**: Monitor dependency updates
  - Current: requirements.txt with minimum versions
  - Risk: Breaking changes in pandas, numpy
  - Solution: Pin exact versions or use poetry/pipenv

- **E4**: Evaluate alternative libraries
  - Example: Polars instead of pandas for performance
  - Benefit: Potential 10x speedup for large datasets

### Academic Collaboration
- **E5**: Peer review of methodologies
  - Current: Internal WifOR methodology
  - Potential: Submit for academic publication

- **E6**: Benchmark against other valuation frameworks
  - Compare to: TruCost, EXIOBASE, LIME
  - Validate: Are results in similar ranges?

---

## PRIORITIZATION MATRIX

### Must Do (Next Sprint)
- S1: Add input data validation
- S2: Add output validation tests
- S9: Implement data versioning
- S14: Document Excel formulas
- Q1: Investigate experimental methodologies
- Q2: Check for data updates

### Should Do (Next Quarter)
- S3: Unit tests for utilities
- S5: Schema validation
- S10: Data update automation
- S25: Set up CI/CD
- S26: Docker container
- Q3: Review USA inflation decision

### Could Do (Next 6 Months)
- S7: Add type hints
- S18: Custom year ranges
- S22: Visualization tools
- R1-R4: Methodology research

### Won't Do (Deferred)
- S24: Parallel country processing (premature optimization)
- R5-R6: New indicators (requires stakeholder input)
- E4: Alternative libraries (not critical)

---

## DECISION LOG

### Decisions Needed
1. **USA Inflation for All Countries**: Keep or change to country-specific? (Q3)
2. **Excel Migration**: Invest in migrating to Python or keep Excel? (Q9)
3. **Base Year Harmonization**: Align GHG to 2020 or keep 2019? (Q6)
4. **Data Versioning Tool**: DVC, Git LFS, or custom solution? (S9)

### Decisions Made
- **2026-01-02**: Accepted Apache 2.0 License for project use
- **2024**: Refactored codebase to reduce duplication by 60%
- **2024**: Centralized configuration in config.yaml and config.py

---

## CONTACT & GOVERNANCE

### Issue Tracking
- GitHub Issues: https://github.com/wifor-impactanalysis/WifOR-Value-Factors/issues
- Email: dimitrij.euler@greenings.org

### Change Request Process
1. Submit issue on GitHub or email
2. Discuss priority and feasibility
3. Assign owner and timeline
4. Implement and test
5. Document in CHANGELOG.md
6. Update this backlog

### Quarterly Review
- Review and prioritize backlog items
- Update maturity status of indicators
- Plan next quarter's work

---

**Note**: This backlog is a living document. Add items as they arise, and move completed items to CHANGELOG.md.
