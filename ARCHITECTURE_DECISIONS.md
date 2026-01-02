# Architecture Decision Records

**WifOR Value Factors - Design Rationale**
**Organization**: Transition Valuation Partnership under Greenings custodianship
**Version**: 1.0
**Last Updated**: 2026-01-02

This document records key architectural decisions made in the WifOR Value Factors project, including rationale and alternatives considered.

---

## ADR Template

Each decision follows this structure:
- **Title**: Short descriptive name
- **Status**: Accepted / Proposed / Deprecated / Superseded
- **Context**: Problem being solved
- **Decision**: What was decided
- **Rationale**: Why this was chosen
- **Consequences**: Positive and negative outcomes
- **Alternatives**: Options not chosen and why

---

## ADR-001: Use USA Inflation for All Countries

**Status**: Accepted

**Context**:
Value factors need temporal adjustment for inflation to maintain comparability across years (2014-2030, 2050, 2100). World Bank provides country-specific GDP deflators, but cross-country comparison requires consistent inflation adjustment.

**Decision**:
Apply USA GDP deflator to all countries instead of using country-specific deflators.

**Rationale**:
1. **Cross-Country Comparability**: Using different inflation rates per country makes it difficult to compare damage costs across countries in future years
2. **USD Denomination**: All coefficients denominated in USD; USA inflation reflects USD purchasing power
3. **Methodological Consistency**: Simplifies methodology - one global inflation factor rather than 188 different factors
4. **Precedent**: Established practice in international valuation frameworks

**Consequences**:

*Positive*:
- Simplified calculation (one inflation series instead of 188)
- Easy to understand and audit
- Cross-country comparisons more meaningful

*Negative*:
- Does not reflect local purchasing power changes
- May over/understate real cost changes in high/low inflation countries
- Country-specific inflation data available but unused

**Alternatives Considered**:
1. **Country-Specific Deflators**: Use each country's GDP deflator
   - Rejected: Breaks cross-country comparability
2. **Weighted Average Deflator**: Use GDP-weighted global deflator
   - Rejected: More complex, marginal benefit
3. **No Inflation Adjustment**: Keep base year values only
   - Rejected: Future projections need temporal consistency

**Review Date**: Annual review to assess if local inflation divergence warrants reconsideration

---

## ADR-002: Training as Only Positive Coefficient

**Status**: Accepted

**Context**:
All environmental indicators represent damage costs (negative impacts). Training represents human capital development.

**Decision**:
Training hours have positive coefficient (+1.0 sign) while all other indicators use negative coefficients (-1.0 sign).

**Rationale**:
1. **Economic Reality**: Training genuinely increases worker productivity and value
2. **Returns to Education Literature**: Well-established positive returns (8-10% per year of schooling)
3. **Impact Valuation Framework**: Benefits should have opposite sign from damages
4. **User Interpretation**: Clear distinction - negative = cost to society, positive = benefit

**Consequences**:

*Positive*:
- Intuitive interpretation (positive = good, negative = bad)
- Enables net impact calculation (sum damages + benefits)
- Reflects economic reality

*Negative*:
- Requires special handling in code (sign check)
- Risk of sign error in updates
- May confuse users expecting all coefficients to be costs

**Alternatives Considered**:
1. **All Negative with Footnote**: Make training negative but document as "negative cost"
   - Rejected: Confusing, mathematically awkward
2. **Separate Output Files**: Benefits in separate files from damages
   - Rejected: Unnecessary complexity for one indicator
3. **Absolute Values Only**: No sign convention
   - Rejected: Loses semantic meaning

**Implementation Notes**:
- Script `014_241016_prepare_Training_my.py` uses `coefficient_sign = 1.0`
- Validation checks verify Training positive, all others negative
- Documentation emphasizes this unique characteristic

---

## ADR-003: GHG Year-Specific, Not Country-Specific

**Status**: Accepted

**Context**:
Most indicators have country-specific damage costs (e.g., air pollution health impacts vary by country income/VSL). GHG emissions cause climate change.

**Decision**:
GHG coefficients are year-specific and global (all countries get same value for each year-scenario combination), unlike other indicators which are country-specific.

**Rationale**:
1. **Scientific Reality**: Climate change is a global phenomenon; CO2 emissions have same climate impact regardless of source country
2. **Social Cost of Carbon**: SCC represents global damage from marginal emissions
3. **Integrated Assessment Models**: DICE model produces global SCC, not country-specific
4. **Economic Theory**: Externality is global; location of emission doesn't affect total damage

**Consequences**:

*Positive*:
- Scientifically accurate representation
- Simpler data structure (no country differentiation needed)
- Aligns with climate economics literature

*Negative*:
- Different structure from other indicators (complicates code slightly)
- Country-specific climate vulnerability not captured
- Users may expect country variation

**Alternatives Considered**:
1. **Country-Specific SCC**: Adjust SCC by country climate vulnerability
   - Rejected: No established methodology; would introduce arbitrary assumptions
2. **Regional SCC**: Group countries by climate impact region
   - Rejected: DICE model doesn't support this; overly complex
3. **Distribute Global Damage**: Allocate SCC to countries by GDP or population
   - Rejected: Arbitrary allocation; loses theoretical foundation

**Implementation Notes**:
- Script `020_241024_prepare_GHG_my.py` has special logic for year-specific values
- All countries × sectors receive identical value for each (year, scenario)
- Documentation emphasizes this difference from other indicators

---

## ADR-004: Excel Pre-calculations for 6 Indicators

**Status**: Accepted (with reservations)

**Context**:
Six indicators (Waste, Air, Water Consumption, Land Use, Water Pollution, OHS) use Excel files with pre-calculated damage costs. Calculation logic not in Python scripts.

**Decision**:
Accept Excel pre-calculations as input, load values directly without recalculating in Python.

**Rationale**:
1. **Legacy System**: Calculations were done previously, validated, and published
2. **Data Provenance**: Excel files sourced from external organizations (OECD, UBA) or internal research
3. **Complexity**: Some calculations (e.g., UBA air pollution methodology) are complex multi-step processes
4. **Practicality**: Re-implementing would require significant effort and validation

**Consequences**:

*Positive*:
- Faster implementation
- Leverages existing validated calculations
- Maintains continuity with prior work

*Negative*:
- **Transparency Issue**: Formulas not in version control
- **Reproducibility**: Can't regenerate from raw source data
- **Auditability**: Harder to verify calculations
- **Maintainability**: Updates require Excel manipulation, not code changes
- **Duplication Risk**: Formulas may exist in multiple places

**Alternatives Considered**:
1. **Migrate to Python**: Reimplement all calculations in Python
   - Rejected for initial version: Too time-consuming, risk of errors
   - **Future Recommendation**: Gradual migration (see BACKLOG.md S9)
2. **Document Excel Formulas**: Extract formulas to documentation
   - Partially accepted: See BACKLOG.md S14 (high priority improvement)
3. **HDF5 Only**: Use only HDF5-based inputs
   - Rejected: Not feasible for externally-sourced data

**Mitigation Strategy**:
- Priority task: Extract and document Excel formulas (DATA_UPDATES.md)
- Long-term: Migrate calculations to Python for full transparency

**Review Date**: Annual review; consider migration if resources available

---

## ADR-005: GHG Base Year 2019 vs 2020 for Others

**Status**: Accepted

**Context**:
Most indicators use 2020 as base year for inflation adjustment. GHG uses 2019.

**Decision**:
Maintain different base years: 2019 for GHG, 2020 for all others.

**Rationale**:
1. **DICE Model Timing**: Nordhaus DICE model reference year is 2019
2. **Data Alignment**: GHG input data (SCC values) calibrated to 2019
3. **Minimal Impact**: One-year difference has negligible effect on comparisons
4. **Source Fidelity**: Preserves original data source conventions

**Consequences**:

*Positive*:
- Aligns with source data
- Maintains published DICE model conventions
- Avoids unnecessary conversions

*Negative*:
- Inconsistency across indicators
- Could confuse users expecting uniform base year
- Requires documentation

**Alternatives Considered**:
1. **Harmonize to 2020**: Convert GHG to 2020 base year
   - Rejected: Adds unnecessary conversion step, potential for errors
2. **Harmonize to 2019**: Convert all others to 2019
   - Rejected: GHG is outlier, not worth changing 7 others
3. **Latest Year**: Use 2024 for everything
   - Rejected: Historical convention established

**Implementation Notes**:
- Documented in METHODOLOGY.md
- config.yaml explicitly shows different base years
- Users warned in README.md

**Review Date**: If DICE model updates to new base year, reconsider

---

## ADR-006: Multi-Threaded Execution with ThreadPoolExecutor

**Status**: Accepted

**Context**:
Running 8 scripts sequentially takes ~500 seconds. Scripts are independent and could run in parallel.

**Decision**:
Implement `run_all_value_factors.py` using Python's `ThreadPoolExecutor` for parallel execution.

**Rationale**:
1. **Performance**: Reduce total execution time by ~60% (500s → 200s)
2. **Simplicity**: ThreadPoolExecutor is built-in, no external dependencies
3. **Independence**: Scripts don't depend on each other's outputs
4. **User Experience**: Faster execution encourages regular updates

**Consequences**:

*Positive*:
- Significant speedup (3-4x faster with 4 workers)
- Built-in to Python (no new dependencies)
- Easy to configure (`--max-workers` parameter)

*Negative*:
- Slightly higher memory usage (multiple scripts in memory)
- Threads not true parallelism (Python GIL), but scripts are I/O-bound
- More complex error handling

**Alternatives Considered**:
1. **Multiprocessing**: Use `ProcessPoolExecutor` instead of threads
   - Rejected: Overkill for I/O-bound tasks, higher overhead
2. **Sequential Execution**: Keep simple sequential loop
   - Rejected: Too slow for regular use
3. **External Tools**: Use GNU Parallel or Make
   - Rejected: Adds external dependency, less portable
4. **Async/Await**: Use asyncio
   - Rejected: More complex, no clear benefit for subprocess execution

**Implementation Notes**:
- Default 4 workers (configurable via `--max-workers`)
- Timeout per script: 3600s (configurable via `--timeout`)
- Real-time logging of script completion
- Summary report at end

**Performance Characteristics**:
- Fastest script: ~13s (Water Consumption)
- Slowest script: ~170s (Air Pollution)
- Total time: ~170s (vs ~500s sequential)
- Speedup: ~3x

---

## ADR-007: Coefficient Matrix Multi-Index Structure

**Status**: Accepted

**Context**:
Output data has 4 dimensions: Year, Indicator, Country, Sector. Need efficient storage and retrieval.

**Decision**:
Use pandas Multi-Index DataFrame with:
- Index: (Year, Indicator)
- Columns: (Country, Sector)

**Rationale**:
1. **Pandas Native**: Leverages powerful pandas multi-indexing
2. **Efficient Slicing**: Easy to extract specific year/country/indicator
3. **Industry Standard**: Familiar to data scientists
4. **Excel Export**: Translates well to hierarchical Excel sheets

**Consequences**:

*Positive*:
- Powerful query capabilities
- Standard pandas operations work
- Efficient memory usage
- Excel rendering is readable

*Negative*:
- Learning curve for users unfamiliar with Multi-Index
- Can be confusing to debug
- Some operations require `loc` or `.xs()` instead of simple indexing

**Alternatives Considered**:
1. **Separate DataFrames**: One per (year, indicator) combination
   - Rejected: Too many small DataFrames, hard to manage
2. **Long Format**: Rows of (year, indicator, country, sector, value)
   - Rejected: Much larger, slower queries
3. **3D/4D NumPy Array**: Use xarray or custom structure
   - Rejected: Less familiar, harder Excel export
4. **Database**: Use SQLite or similar
   - Rejected: Overkill for final outputs; adds dependency

**Implementation Notes**:
- Index levels: Year (int), Indicator (str)
- Column levels: GeoRegion (str/ISO3), Sector (str/NACE)
- Values: Float64 (USD)

**User Guidance**:
- README.md includes Multi-Index example
- METHODOLOGY.md visualizes structure

---

## ADR-008: HDF5 + Excel Dual Output Format

**Status**: Accepted

**Context**:
Coefficient data needs to be:
1. Efficiently stored for programmatic use
2. Human-readable for inspection and manual analysis

**Decision**:
Save outputs in BOTH HDF5 (.h5) and Excel (.xlsx) formats.

**Rationale**:
1. **HDF5 for Programs**: Efficient, structured, fast read/write
2. **Excel for Humans**: Widely used, easy to inspect, familiar
3. **Different Use Cases**: Programmers use HDF5, analysts use Excel
4. **Minimal Cost**: Storage is cheap, generation time negligible

**Consequences**:

*Positive*:
- Meets needs of both technical and non-technical users
- HDF5: 10x faster to read, smaller file size
- Excel: No special tools needed, widely compatible

*Negative*:
- Redundant storage (both formats contain same data)
- Maintenance of two formats (but generated automatically)
- Excel has row/column limits (1M rows, 16K columns) - not hit yet

**Alternatives Considered**:
1. **HDF5 Only**: More efficient, but excludes non-programmers
   - Rejected: Too restrictive
2. **Excel Only**: Universal access, but slow and large
   - Rejected: Inefficient for programmatic use
3. **CSV**: Simple format
   - Rejected: Doesn't handle Multi-Index well
4. **Parquet**: Modern efficient format
   - Rejected: Less familiar than HDF5/Excel combo

**Implementation Notes**:
- HDF5 keys: 'coefficients', 'units'
- Excel sheets: 'Coefficients', 'Units'
- Same content in both formats
- value_factor_utils.py handles both in one function

**File Sizes** (approximate):
- HDF5: ~1-5 MB per indicator
- Excel: ~2-20 MB per indicator (2-4x larger)

---

## ADR-009: Centralized Configuration (config.yaml + config.py)

**Status**: Accepted

**Context**:
Previously, each script had hard-coded file paths, years, and parameters. Changing settings required editing 8 scripts.

**Decision**:
Centralize configuration in:
- `config.yaml`: User-friendly YAML for non-programmers
- `config.py`: Python wrapper for programmatic access

**Rationale**:
1. **DRY Principle**: Don't repeat configuration across 8 scripts
2. **Maintainability**: Change one file instead of 8
3. **User-Friendly**: YAML is readable for non-programmers
4. **Flexibility**: Easy to add new indicators or change parameters

**Consequences**:

*Positive*:
- Single source of truth
- Easier to update file paths
- Clearer parameter management
- New indicators easy to add

*Negative*:
- Adds dependency (PyYAML)
- Indirection (have to look at config file to see settings)
- Potential for config errors breaking all scripts

**Alternatives Considered**:
1. **Environment Variables**: Use .env file
   - Rejected: Less structured, harder to validate
2. **Command-Line Arguments**: Pass everything as args
   - Rejected: Too verbose for 8+ parameters per script
3. **Hard-Coded in Scripts**: Keep as-is
   - Rejected: Defeats refactoring purpose
4. **JSON Config**: Use JSON instead of YAML
   - Rejected: YAML more human-friendly (comments, multi-line)

**Implementation Notes**:
- config.yaml: Indicator-specific sections
- config.py: `get_indicator_config(name)` function
- Validation: Checks file paths exist
- Default values: Provided for optional settings

**Configuration Structure**:
```yaml
waste:
  input_file: "input_data/220509_Waste..."
  output_dir: "output"
  base_year: 2020
```

---

## ADR-010: Years Selection (2014-2030, 2050, 2100)

**Status**: Accepted

**Context**:
Value factors needed for historical analysis, near-term projections, and long-term climate scenarios.

**Decision**:
Generate coefficients for:
- Annual: 2014-2030 (17 years)
- Milestone: 2050, 2100 (2 years)
- Total: 19 years

**Rationale**:
1. **Historical**: 2014-2023 covers recent past for backtesting
2. **Near-Term**: 2024-2030 for business planning horizon
3. **Climate Milestones**: 2050 (Paris Agreement mid-century), 2100 (end-of-century scenarios)
4. **Data Availability**: World Bank deflators available through 2023
5. **Scenario Analysis**: Long-term needed for climate impact assessment

**Consequences**:

*Positive*:
- Covers all typical use cases
- Aligns with climate scenario timelines
- Balances detail (annual) with long-term (milestones)

*Negative*:
- Deflator not available for 2050/2100 (uses last available)
- Annual 2024-2030 may be unnecessary for some use cases
- Gaps between 2030-2050 and 2050-2100

**Alternatives Considered**:
1. **Annual Through 2100**: 87 years
   - Rejected: Overkill, large files, no deflator data
2. **Decadal Only**: 2020, 2030, 2040, ..., 2100
   - Rejected: Loses granularity for near-term analysis
3. **User-Configurable**: Let users specify years
   - Partially accepted: See BACKLOG.md S18 (future enhancement)
4. **Only Historical**: 2014-2023
   - Rejected: No forward-looking capability

**Future Years Handling**:
- 2024-2030: Uses last available deflator (2023) → "2023USD" units
- 2050, 2100: Same approach

**Review Date**: Annually, as new deflator data becomes available

---

## ADR-011: License Acceptance Mechanism

**Status**: Accepted

**Context**:
Project uses Apache 2.0 License. Users must accept terms before use.

**Decision**:
Implement license acceptance check with `.license_accepted` file:
1. First run: Display license summary, prompt for acceptance
2. Acceptance stored in `.license_accepted` file (contains "Y")
3. Subsequent runs: Check file, skip prompt if accepted

**Rationale**:
1. **Legal Requirement**: User must explicitly accept license
2. **User Experience**: Only prompt once, not every run
3. **Simple Implementation**: Text file, no database needed
4. **Transparent**: File in project root, easy to see status

**Consequences**:

*Positive*:
- Clear legal compliance
- Minimal user friction (one-time prompt)
- Easy to reset (delete file)

*Negative*:
- Adds step before first use
- Can break automated workflows
- File-based state (not ideal for Docker/cloud)

**Alternatives Considered**:
1. **No License Check**: Assume acceptance by use
   - Rejected: Legally questionable
2. **Command-Line Flag**: `--accept-license`
   - Rejected: Easy to forget, less explicit
3. **Config File Setting**: Add to config.yaml
   - Rejected: License acceptance separate from configuration
4. **Database**: Store in SQLite
   - Rejected: Overkill for single boolean

**Implementation Notes**:
- `license_check.py`: Standalone module
- ` require_license_acceptance()`: Called at start of each script
- `.license_accepted` in `.gitignore` (user-specific)

**Automated Workflows**:
- CI/CD: Create `.license_accepted` file before running tests
- Docker: Include file in image build

---

## ADR-012: Value Transfer in Pre-Calculation Phase

**Status**: Accepted (with transparency limitations)

**Context**:
Value factors need to be applicable across 188 countries, but primary valuation studies typically come from specific regions (e.g., Sweden for water pollution, Germany for air pollution). Converting these base values to country-specific estimates requires **value transfer** - applying values from one context to another.

**Decision**:
Value transfer mechanisms (PPP adjustment, income elasticity) are applied **during input file creation** (Excel/external calculations), **NOT in Python scripts**. Python scripts only apply temporal adjustments (inflation).

**Rationale**:
1. **Historical Approach**: Input files inherited from prior WifOR work with pre-calculated country values
2. **Methodological Complexity**: Value transfer requires detailed economic data (PPP indices, income elasticity parameters) not readily available in pipeline
3. **Performance**: Pre-calculation avoids repeated calculations for same base values
4. **Stability**: Separates stable spatial transfer from variable temporal adjustments

**Consequences**:

*Positive*:
- **Simplicity**: Python scripts simpler (only inflation adjustment)
- **Performance**: Pre-calculated values load quickly
- **Separation of Concerns**: Spatial vs. temporal adjustments handled separately

*Negative*:
- **Transparency Limited**: Excel formulas not documented or version-controlled
- **Reproducibility Gap**: Cannot independently verify country-specific values from source studies
- **Update Complexity**: Changing transfer methodology requires Excel file updates, not just code
- **Auditability**: Black-box pre-calculations hinder external validation
- **Parameter Opacity**: PPP indices, elasticity values, base years not disclosed

**Value Transfer Methods Used**:

1. **PPP Adjustment** (Water Pollution, Training):
   ```
   Value[Country] = Value[Source] × (PPP[Country] / PPP[Source])
   ```

2. **Income Elasticity** (Air Pollution VSL):
   ```
   VSL[Country] = VSL[Base] × (GDP_pc[Country] / GDP_pc[Base])^elasticity
   ```

3. **Global Value** (OHS):
   ```
   All countries: USD 200,000/DALY (no adjustment)
   ```

**Alternatives Considered**:

1. **Implement Transfer in Python**:
   - **Advantages**: Full transparency, version control, reproducibility
   - **Disadvantages**: Requires adding economic data (PPP, GDP) to pipeline; significant refactoring
   - **Decision**: Rejected for v1.0 due to effort; recommended for v2.0 (see BACKLOG.md S-VT1)

2. **Document Excel Formulas**:
   - **Advantages**: Improves transparency without code changes
   - **Disadvantages**: Manual process, formulas may be complex
   - **Decision**: Recommended as interim step (see BACKLOG.md Q8)

3. **Country-Specific Primary Studies**:
   - **Advantages**: Highest accuracy, no transfer needed
   - **Disadvantages**: Prohibitively expensive for 188 countries
   - **Decision**: Rejected as infeasible

**Implementation Evidence**:

*Water Pollution* (`013_241014_prepare_WaterPol_my.py:53-55`):
```python
# Loads pre-calculated, PPP-adjusted values
coeffs_data = pd.read_excel(
    config["input_file"], sheet_name="Results", header=0, index_col=[1, 3]
)
```

*Training* (`014_241016_prepare_Training_my.py:61-63`):
```python
# Column name explicitly indicates PPP adjustment already applied
training_coeff = coeffs_data["value_per_hour_GVA_2020USD_PPP"].to_frame().T
```

**Transparency Gaps** (documented in BACKLOG.md):
- **Q8**: Excel formulas not extracted or documented
- **Q9**: Migration to Python for full transparency
- **Q10**: Training calculation methodology not disclosed

**Improvement Roadmap**:

**Phase 1** (Immediate): Document existing approach
- ✅ Add value transfer sections to METHODOLOGY.md
- ✅ Document methods in INPUT_FILES_METHODOLOGY.md
- ✅ Create ADR-012 (this document)

**Phase 2** (Short-term): Extract formulas
- [ ] Export Excel formulas to documentation
- [ ] Identify PPP indices and base years used
- [ ] Document elasticity parameters for income adjustments

**Phase 3** (Medium-term): Migrate to Python
- [ ] Add economic data (PPP, GDP per capita) to input pipeline
- [ ] Implement value transfer functions in `value_factor_utils.py`
- [ ] Validate outputs match existing Excel calculations
- [ ] Deprecate Excel pre-calculations

**Phase 4** (Long-term): Enhanced methodology
- [ ] Allow user-selectable transfer methods (PPP vs. income elasticity)
- [ ] Sensitivity analysis on transfer parameters
- [ ] Country-specific primary studies for high-impact countries

**Review Date**:
- **Immediate**: Quarterly review of documentation improvements
- **Annual**: Assessment of Python migration feasibility
- **Trigger-based**: If IFVI/VBA standardizes value transfer methodology

**References**:
- Impact Valuation Sprint Report 2024 (lines 2081, 3088, 7236, 9734)
- Ahlroth (2009) - WTP estimates for water pollution (Sweden)
- OECD VSL methodology for air pollution

---

## Summary Table

| ADR | Topic | Status | Impact | Review Frequency |
|-----|-------|--------|--------|------------------|
| 001 | USA Inflation Global | Accepted | High | Annual |
| 002 | Training Positive | Accepted | Medium | Stable |
| 003 | GHG Year-Specific | Accepted | Medium | If DICE updates |
| 004 | Excel Pre-calcs | Accepted* | High | Annual (migrate?) |
| 005 | GHG Base Year 2019 | Accepted | Low | If DICE updates |
| 006 | Multi-Threading | Accepted | Medium | Stable |
| 007 | Multi-Index Structure | Accepted | High | Stable |
| 008 | HDF5 + Excel Outputs | Accepted | Low | Stable |
| 009 | Centralized Config | Accepted | Medium | Stable |
| 010 | Years Selection | Accepted | Medium | Annual |
| 011 | License Acceptance | Accepted | Low | Stable |
| 012 | Value Transfer Pre-calc | Accepted* | **CRITICAL** | Quarterly |

*Accepted with transparency limitations; Python migration recommended (see BACKLOG.md)

---

## Future Decisions Needed

See BACKLOG.md "Decisions Needed" section for pending architectural questions:

1. **USA Inflation**: Keep or change to country-specific?
2. **Excel Migration**: Invest in Python migration?
3. **Value Transfer Transparency**: Extract Excel formulas or migrate to Python? (NEW - HIGH PRIORITY)
4. **Base Year Harmonization**: Align GHG to 2020?
5. **Data Versioning Tool**: DVC, Git LFS, or custom?

---

## Decision Process

When making new architectural decisions:

1. **Identify Need**: Problem or opportunity requiring decision
2. **Research**: Gather information, review alternatives
3. **Consult**: Discuss with stakeholders (WifOR team, users)
4. **Document**: Write ADR using template above
5. **Implement**: Execute decision in code
6. **Review**: Periodic review (see table above)
7. **Update**: If decision changes, mark as superseded and create new ADR

---

**Document Version**: 1.0
**Last Updated**: 2026-01-02
**Maintained by**: WifOR Development Team
**Contact**: dimitrij.euler@greenings.org
