"""
Transforms Greenings backtesting data (s4_backtesting/20260317_Data_Greenings_clean_NG.xlsx)
and s4_backtesting/finance data into project assessment input files for the TVP4 framework.

Output files (written to the same directory):
  01_project_master.csv         — project metadata + financial parameters
  02_impact_indicators.csv      — all indicator observations mapped to ESRS
  03_monetisation_inputs.csv    — wide-format table ready for TVP value-factor application
"""

import pandas as pd
import numpy as np
from pathlib import Path

HERE = Path(__file__).parent
S4 = Path(__file__).parent.parent.parent / "s4_backtesting"

# ── 1. PROJECT MASTER ─────────────────────────────────────────────────────────

projects = [
    # Hospitals
    dict(project_id="HOSP-1", sector="Hospitals",         region="LATAM",   country="Brazil",   stage="Development",  capex_musd=147),
    dict(project_id="HOSP-2", sector="Hospitals",         region="Africa",  country="Nigeria",  stage="Development",  capex_musd=250),
    dict(project_id="HOSP-3", sector="Hospitals",         region="Europe",  country="Germany",  stage="Operational",  capex_musd=150),
    # Hydro Power Plants
    dict(project_id="HYDRO-1", sector="Hydro Power Plant", region="Africa", country="Nigeria",  stage="Construction", capex_musd=200),
    dict(project_id="HYDRO-2", sector="Hydro Power Plant", region="Asia",   country="Malaysia", stage="Development",  capex_musd=400),
    dict(project_id="HYDRO-3", sector="Hydro Power Plant", region="Europe", country="Germany",  stage="Operation",    capex_musd=47),
    # Rail
    dict(project_id="RAIL-1",  sector="Rail",              region="Europe", country="Germany",  stage="Development",  capex_musd=1190),
    dict(project_id="RAIL-2",  sector="Rail",              region="Europe", country="Germany",  stage="Operation",    capex_musd=1350),
    dict(project_id="RAIL-3",  sector="Rail",              region="Europe", country="Germany",  stage="Operation",    capex_musd=2460),
]

master = pd.DataFrame(projects)

# Merge in financial parameters from bond portfolio forecast
finance = pd.read_csv(S4 / "finance" / "bond_portfolio_forecast_10y.csv")
# align column names
finance = finance.rename(columns={
    "Principal": "capex_musd",
    "Yield":     "bond_yield",
    "Annual_Coupon": "annual_coupon_musd",
    "Total_10Y":     "total_10y_return_musd",
})
finance["sector_key"] = finance["Sector"].map({"health": "Hospitals", "energy": "Hydro Power Plant", "transport": "Rail"})
finance = finance.drop(columns=["Region", "Country", "Sector"])

master = master.merge(
    finance.rename(columns={"sector_key": "sector"}),
    on=["sector", "capex_musd"],
    how="left",
)
master["data_year"] = 2025
master["source_file"] = "20260317_Data_Greenings_clean_NG.xlsx"

master.to_csv(HERE / "01_project_master.csv", index=False)
print(f"Written 01_project_master.csv  ({len(master)} rows)")


# ── 2. IMPACT INDICATORS (long format) ────────────────────────────────────────
#
# Greenings indicator taxonomy (not ESRS-native):
#   S7  = Health & Safety / community well-being       → ESRS S1
#   E2  = GHG (avoided emissions)                      → ESRS E1
#   E4  = Pollution Prevention / Land Use              → ESRS E2 / E4
#   R5  = Resilience / Climate Adaptation              → ESRS E1 (adaptation)
#
# Note: Greenings uses its own "E2/E4" coding that differs from ESRS E2/E4.
# The mapping below captures the correct ESRS alignment.

INDICATOR_META = {
    "S7.P5W":   ("S1", "S1-89",      "Health and Safety",     "Improvement of H&S for surrounding communities (Yes/No)", "boolean"),
    "S7.LJ9":   ("S1", "S1-89",      "Health and Safety",     "Project contribution category to H&S",                   "categorical"),
    "S7.EJ2":   ("E4", "E4-AR34",    "Biodiversity / NbS",    "Nature-Based Solutions applied (Yes/No)",                "boolean"),
    "S7.P8B":   ("S1", "S1-89",      "Health and Safety",     "Quantification method for H&S measures",                 "categorical"),
    "S7.P8B.1": ("S1", "S1-89",      "Health and Safety",     "H&S expenditure as % of project CAPEX",                  "percent"),
    "S7.P8B.3": ("S1", "S1-89",      "Health and Safety",     "Annual expenditure on H&S measures (USD)",               "monetary"),
    "S7.X4B":   ("S1", "S1-89",      "Health and Safety",     "Number of people with improved H&S from the project",    "persons"),
    "E2.Q8W.A": ("E1", "E1-34a",     "GHG",                   "Avoided GHG emissions — prior calendar year (tCO2e/yr)", "tCO2e_yr"),
    "E2.Q8W.B": ("E1", "E1-34a",     "GHG",                   "Avoided GHG emissions — first year of operations (tCO2e/yr)", "tCO2e_yr"),
    "E4.O5C":   ("E2", "E2-28a",     "Air Pollution",         "Type of pollution improvement claimed",                  "categorical"),
    "E4.2MB.1": ("E2", "E2-39a",     "Air Pollution",         "Pollution-prevention measure as % of project CAPEX",     "percent"),
    "E4.T9A":   ("E2", "E2-39a",     "Air Pollution",         "Number of people impacted by pollution reduction",        "persons"),
    "R5.V4H.1": ("E1", "E1-69a",     "Climate Adaptation",    "Domain in which resilience is improved",                 "categorical"),
    "R5.B6D.1": ("E1", "E1-69a",     "Climate Adaptation",    "Resilience measure as % of project CAPEX",               "percent"),
    "R5.U2X.A": ("E1", "E1-69a",     "Climate Adaptation",    "Number of people benefiting from resilience measure",    "persons"),
}

# Raw observations extracted from the Excel file
# (project_id, indicator_code, claimed_pc, value_raw, notes)
observations = [
    # ── HOSPITALS ──
    ("HOSP-1", "S7.P5W",   True,  "Yes",                                              ""),
    ("HOSP-1", "S7.LJ9",   True,  "Contribution to Health Infra, Contribution to Medical Equipment", ""),
    ("HOSP-1", "S7.EJ2",   True,  "Yes",                                              ""),
    ("HOSP-1", "S7.P8B",   True,  "Measures accounted in Proj CAPEX",                 ""),
    ("HOSP-1", "S7.P8B.1", True,  "2.72",                                             ""),
    ("HOSP-1", "S7.P8B.3", True,  None,                                               "Not answered"),
    ("HOSP-1", "S7.X4B",   True,  "5000000",                                          "22y operation; 17 600 consultations/month; 1 650 medical services/month"),

    ("HOSP-2", "S7.P5W",   True,  "Yes",                                              ""),
    ("HOSP-2", "S7.LJ9",   True,  "Contribution to Diagnostics, Consumables, Or Drugs and Medication", ""),
    ("HOSP-2", "S7.EJ2",   True,  "No",                                               ""),
    ("HOSP-2", "S7.P8B",   True,  "Measures accounted in CAPEX and P&L",              ""),
    ("HOSP-2", "S7.P8B.1", True,  "100",                                              ""),
    ("HOSP-2", "S7.P8B.3", True,  "250000000",                                        "250 million USD"),
    ("HOSP-2", "S7.X4B",   True,  "3000",                                             "20y operation; 150-200 children/year"),

    ("HOSP-3", "S7.P5W",   True,  "Yes",                                              ""),
    ("HOSP-3", "S7.LJ9",   True,  "Contribution to Health Infra",                     ""),
    ("HOSP-3", "S7.EJ2",   True,  "Yes",                                              ""),
    ("HOSP-3", "S7.P8B",   True,  "Measures accounted in Proj CAPEX and P&L",         ""),
    ("HOSP-3", "S7.P8B.1", True,  "100",                                              ""),
    ("HOSP-3", "S7.P8B.3", True,  None,                                               "Not answered"),
    ("HOSP-3", "S7.X4B",   True,  "500000",                                           "1.8 million patients/year"),

    # ── HYDRO POWER PLANTS ──
    # Source: E2.Q8W.A = "N/A" (not yet operational / prior-year baseline absent)
    ("HYDRO-1", "E2.Q8W.A", False, "N/A",    "Source shows N/A — plant not yet operational in prior calendar year"),
    ("HYDRO-1", "E2.Q8W.B", True,  "150000", ""),
    ("HYDRO-1", "S7.X4B",   True,  "15000",  "New/modern equipment; support of departmental hospital"),

    ("HYDRO-2", "E2.Q8W.A", False, "N/A",       "Source shows N/A — plant not yet operational in prior calendar year"),
    ("HYDRO-2", "E2.Q8W.B", True,  "834218.74", ""),
    ("HYDRO-2", "S7.X4B",   False, "Not a claimed PC", "Not a claimed PC"),

    ("HYDRO-3", "E2.Q8W.A", True,  "6126", ""),
    ("HYDRO-3", "E2.Q8W.B", False, "N/A",  "Source shows N/A — prior-year figure used for operational plant"),
    ("HYDRO-3", "S7.X4B",   False, "Not a claimed PC", "Not a claimed PC"),

    # ── RAIL ──
    ("RAIL-1", "E2.Q8W.A",  True,  "23364",           ""),
    ("RAIL-1", "E4.O5C",    True,  "Improved Air Quality", ""),
    ("RAIL-1", "E4.2MB.1",  True,  "<1",              "Less than 1% of CAPEX"),
    ("RAIL-1", "E4.T9A",    True,  "150000",          ""),
    ("RAIL-1", "R5.V4H.1",  True,  "Critical infrastructure", ""),
    ("RAIL-1", "R5.B6D.1",  True,  "<5",              "Less than 5% of CAPEX"),
    ("RAIL-1", "R5.U2X.A",  True,  "5500000",         "5.5 million people/year"),

    ("RAIL-2", "E2.Q8W.A",  True,  "130000", ""),
    ("RAIL-2", "E4.O5C",    False, None,     "Not a claimed PC"),
    ("RAIL-2", "R5.V4H.1",  False, None,     "Not a claimed PC"),

    ("RAIL-3", "E2.Q8W.A",  True,  "90000",  ""),
    ("RAIL-3", "E4.O5C",    False, None,     "Not a claimed PC"),
    ("RAIL-3", "R5.V4H.1",  False, None,     "Not a claimed PC"),
]

rows = []
for project_id, code, claimed, val_raw, notes in observations:
    esrs_std, esrs_ref, impact_driver, description, unit = INDICATOR_META[code]
    # derive numeric value where possible
    val_num = np.nan
    if val_raw is not None:
        try:
            val_num = float(val_raw)
        except (ValueError, TypeError):
            pass
    rows.append(dict(
        project_id=project_id,
        greenings_indicator=code,
        esrs_standard=esrs_std,
        esrs_reference=esrs_ref,
        impact_driver=impact_driver,
        indicator_description=description,
        unit=unit,
        claimed_positive_contribution=claimed,
        value_raw=val_raw,
        value_numeric=val_num,
        notes=notes,
    ))

indicators = pd.DataFrame(rows)
indicators.to_csv(HERE / "02_impact_indicators.csv", index=False)
print(f"Written 02_impact_indicators.csv  ({len(indicators)} rows)")


# ── 3. MONETISATION INPUTS (wide format, one row per project) ─────────────────
#
# Selects the numeric indicators that feed directly into TVP value-factor
# multiplication:
#   • ghg_avoided_tco2e_yr          → GHG value factor (USD/tCO2e)
#   • health_beneficiaries          → OHS / well-being value factor (USD/person)
#   • health_capex_pct              → CAPEX allocation check
#   • pollution_beneficiaries       → Air pollution value factor (USD/person)
#   • pollution_capex_pct           → CAPEX allocation check
#   • resilience_beneficiaries      → Climate adaptation (avoided damages)
#   • resilience_capex_pct          → CAPEX allocation check

def first_numeric(df, pid, code):
    row = df[(df.project_id == pid) & (df.greenings_indicator == code) & df.claimed_positive_contribution]
    if row.empty:
        return np.nan
    return row.iloc[0]["value_numeric"]

def first_raw(df, pid, code):
    row = df[(df.project_id == pid) & (df.greenings_indicator == code)]
    if row.empty:
        return None
    return row.iloc[0]["value_raw"]

monrows = []
for p in projects:
    pid = p["project_id"]
    # GHG: prefer prior-year if available, else first-year
    ghg_py = first_numeric(indicators, pid, "E2.Q8W.A")
    ghg_fy = first_numeric(indicators, pid, "E2.Q8W.B")
    ghg = ghg_py if not np.isnan(ghg_py) else ghg_fy

    monrows.append(dict(
        project_id=pid,
        sector=p["sector"],
        region=p["region"],
        country=p["country"],
        stage=p["stage"],
        capex_musd=p["capex_musd"],
        # GHG
        ghg_avoided_tco2e_yr=ghg,
        ghg_indicator=("E2.Q8W.A" if not np.isnan(ghg_py) else "E2.Q8W.B") if not np.isnan(ghg) else None,
        # Health & Safety
        health_beneficiaries=first_numeric(indicators, pid, "S7.X4B"),
        health_capex_pct=first_numeric(indicators, pid, "S7.P8B.1"),
        health_contribution_type=first_raw(indicators, pid, "S7.LJ9"),
        nbs_applied=(first_raw(indicators, pid, "S7.EJ2") == "Yes"),
        # Air Pollution
        pollution_improvement_type=first_raw(indicators, pid, "E4.O5C"),
        pollution_capex_pct_upper=(
            1.0 if first_raw(indicators, pid, "E4.2MB.1") == "<1" else np.nan
        ),
        pollution_beneficiaries=first_numeric(indicators, pid, "E4.T9A"),
        # Climate Resilience / Adaptation
        resilience_domain=first_raw(indicators, pid, "R5.V4H.1"),
        resilience_capex_pct_upper=(
            5.0 if first_raw(indicators, pid, "R5.B6D.1") == "<5" else np.nan
        ),
        resilience_beneficiaries=first_numeric(indicators, pid, "R5.U2X.A"),
    ))

mondf = pd.DataFrame(monrows)

# Merge financial parameters for discount-rate-based NPV calculations
fin_cols = ["project_id", "bond_yield", "annual_coupon_musd", "total_10y_return_musd"]
mondf = mondf.merge(master[fin_cols], on="project_id", how="left")

mondf.to_csv(HERE / "03_monetisation_inputs.csv", index=False)
print(f"Written 03_monetisation_inputs.csv  ({len(mondf)} rows)")

print("\nDone. Files written to:", HERE)
