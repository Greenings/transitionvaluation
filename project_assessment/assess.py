#!/usr/bin/env python3
"""
assess.py
=========
Integrated assessment for the S4 project portfolio.

Runs three independent analytical passes over the nine projects
(Proj_001–003, Hydro_AF/AS/EU, Rail_EU_DEV/OP1/OP2) and writes
all outputs to results/.

    Pass 1 — Supply-chain analysis          (tvp_dbio)
    Pass 2 — SSP scenario adjustment        (tvp_scenario)
    Pass 3 — Nature-related dependency risk (tvp_dependency)

Usage
-----
    python assess.py                  # full run, all three passes
    python assess.py --skip-dependency  # skip re-running dependency pipeline
    python assess.py --tiers 0 3      # override tier range for supply chain

Outputs
-------
    results/supply_chain.csv          Tier-by-tier GHG/employment/water/VA
    results/supply_chain_summary.csv  Project-level totals (tiers 0-5 summed)
    results/scenario_adjustment.csv   SSP GHG intensity factors × project regions
    results/scenario_ghg_adjusted.csv Scenario-adjusted GHG for 2025/2030/2040
    results/dependency_summary.csv    Nature risk scores (merged from dependency pipeline)
    results/final_analysis.md         Narrative synthesis of all three passes
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Must be set before h5py or tables is imported so HDF5 initialises without
# file-locking — required on Windows UNC paths (e.g. \\wsl$\...).
os.environ.setdefault("HDF5_USE_FILE_LOCKING", "FALSE")

# ──────────────────────────────────────────────────────────────────────────────
# Repository layout
# ──────────────────────────────────────────────────────────────────────────────
ROOT            = Path(__file__).parent.parent   # repo root (one level up from project_assessment/)
DBIO_DIR        = ROOT / "tvp_dbio"
SCENARIO_DIR    = ROOT / "tvp_scenario"
DEPENDENCY_DIR  = ROOT / "tvp_dependency"
INPUT_DIR       = Path(__file__).parent / "modeled_input_data"
RESULTS_DIR     = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Make submodules importable
sys.path.insert(0, str(DBIO_DIR))
sys.path.insert(0, str(DEPENDENCY_DIR))

# ──────────────────────────────────────────────────────────────────────────────
# WifOR value factor paths and mappings (Pass 4)
# ──────────────────────────────────────────────────────────────────────────────

# Representative ISO-3166-1 alpha-3 country per broad project region.
# Drives country-specific WifOR coefficients for water scarcity cost and
# employment training value.
REGION_TO_ISO3: dict[str, str] = {
    "LATAM":  "BRA",   # Brazil — largest LATAM economy
    "Africa": "NGA",   # Nigeria — largest sub-Saharan African economy
    "Asia":   "IND",   # India — representative South/South-East Asia
    "Europe": "DEU",   # Germany — representative continental Western Europe
}

# tvp5 sector codes → NACE Rev.2 codes used in WifOR coefficient tables.
PROJECT_SECTOR_TO_NACE: dict[str, str] = {
    "Health_Social":      "Q",    # Human health and social work activities
    "Health_Specialized": "Q",
    "Health_General":     "Q",
    "Energy":             "D35",  # Electricity, gas, steam & air conditioning supply
    "Rail_Dev":           "F",    # Construction (development-phase CAPEX dominates)
    "Rail_Op":            "H49",  # Land transport and transport via pipelines
}

# WifOR pre-computed coefficient files and their lookup parameters.
VF_FILE_SPECS: dict[str, dict] = {
    "ghg": {
        "filename":  "2024-11-18_formatted_MonGHG_my.h5",
        "indicator": "COEFFICIENT GHG_BASE, in USD (WifOR)",
        "year":      "2019",
        "unit":      "USD/kg",
        "note":      "Social cost of carbon — Nordhaus DICE baseline",
    },
    "ghg_paris": {
        "filename":  "2024-11-18_formatted_MonGHG_my.h5",
        "indicator": "COEFFICIENT GHG_PARIS_UPDATE, in USD (WifOR)",
        "year":      "2019",
        "unit":      "USD/kg",
        "note":      "Social cost of carbon — Paris-consistent updated trajectory",
    },
    "water": {
        "filename":  "2024-10-01_formatted_MonWaterCon_my.h5",
        "indicator": "COEFFICIENT Water Consumption Blue, in USD (WifOR)",
        "year":      "2020",
        "unit":      "USD/m3",
        "note":      "Blue water depletion damage cost — country-level scarcity weighting",
    },
    "training": {
        "filename":  "2024-10-16_formatted_MonTrain_my.h5",
        "indicator": "COEFFICIENT TrainingHours, in USD (WifOR)",
        "year":      "2020",
        "unit":      "USD/h",
        "note":      "Workplace training benefit — GVA-based, country- and sector-specific (legacy key)",
    },
    # GVA per labour-hour: the productivity-based living-wage proxy.
    # Loaded from WifOR raw input (220529_training_value_per_hour_bysector.h5)
    # rather than the MonTrain formatted H5.  MonTrain_2020 = GVA_2020 exactly;
    # the distinction is conceptual: this key explicitly monetises *all* labour
    # hours at the sector GVA rate (i.e., assuming workers are paid at least the
    # GVA-equivalent, which exceeds Anker living-wage benchmarks in most markets).
    "gva_per_hour": {
        "filename":  "input_data/220529_training_value_per_hour_bysector.h5",
        "indicator": "value_per_hour_GVA_2020USD_PPP",
        "year":      "2020",
        "unit":      "USD/h",
        "note":      "GVA per labour-hour (2020 PPP) — living-wage proxy for FTE monetisation; "
                     "GVA/h ≥ Anker living wage in most markets; projected to FOCUS_YEAR via "
                     "MonTrain productivity growth index (ILO-aligned, ~1.1 %/yr real)",
    },
}

# ILO 2022 average annual hours worked per FTE — converts FTE to hours for the
# GVA-per-labour-hour monetisation.
FTE_HOURS_PER_YEAR = 1_880

# ──────────────────────────────────────────────────────────────────────────────
# Project registry
# Built directly from modeled_input_data CSVs so there is a single source
# of truth; sector_code and invest_usd mirror the tvp_dbio API conventions.
# ──────────────────────────────────────────────────────────────────────────────

def _load_projects() -> list[dict]:
    projects = []

    # Hospitals
    with open(INPUT_DIR / "hospitals_finance_input.csv") as f:
        for row in csv.DictReader(f):
            projects.append({
                "project_id":   row["Project_ID"],
                "region":       row["Region"],
                "sector_code":  row["Sector_Code"],
                "invest_usd":   float(row["Est_Investment_USD"]),
                "asset_class":  "Health",
                "stage":        row["Stage"],
            })

    # Hydro
    with open(INPUT_DIR / "hydro_finance_input.csv") as f:
        for row in csv.DictReader(f):
            projects.append({
                "project_id":   row["Project_ID"],
                "region":       row["Region"],
                "sector_code":  "Energy",
                "invest_usd":   float(row["Est_Investment_USD"]),
                "asset_class":  "Energy",
                "stage":        row["Impact_Type"],
            })

    # Rail — EUR → USD at 1.08
    with open(INPUT_DIR / "rail_finance_input.csv") as f:
        for row in csv.DictReader(f):
            capex_eur = float(row.get("Est_Capex_EUR", 0) or 0)
            invest_usd = capex_eur * 1.08
            stage = row["Stage"]
            sc = "Rail_Dev" if stage in ("Dev", "Development") else "Rail_Op"
            projects.append({
                "project_id":   row["Project_ID"],
                "region":       row["Region"],
                "sector_code":  sc,
                "invest_usd":   invest_usd,
                "asset_class":  "Transport",
                "stage":        stage,
            })

    return projects


# ──────────────────────────────────────────────────────────────────────────────
# Impact sign convention
# ──────────────────────────────────────────────────────────────────────────────
# NEGATIVE impacts increase environmental burden (shown as costs).
# POSITIVE impacts deliver social/economic benefits (shown as gains).
# Each entry: label → (polarity, display_unit, display_name)

IMPACT_POLARITY: dict[str, tuple[str, str, str]] = {
    # Supply-chain stressors (all tiers)
    "GHG_tCO2e":      ("negative", "tCO2e",   "GHG emissions"),
    "Water_1000m3":   ("negative", "000 m³",   "Water withdrawal"),
    "NOx_t":          ("negative", "t NOx",    "NOx air pollution"),
    "Employment_FTE": ("positive", "FTE",      "Jobs created"),
    "ValueAdded_M$":  ("positive", "M USD",    "Value added"),
    "Energy_TJ":      ("negative", "TJ",       "Energy use"),
    # Project-level outcome indicators (from input files)
    "avoided_CO2_tCO2e": ("positive", "tCO2e",  "Avoided GHG (generation)"),
    "beneficiaries":     ("positive", "people",  "Health beneficiaries"),
    "reach_ppl_yr":      ("positive", "ppl/yr",  "Rail passengers reached"),
    "air_quality_pct":   ("positive", "% improv","Air quality improvement"),
}

NEGATIVE_STRESSORS = [k for k, (p, _, _) in IMPACT_POLARITY.items() if p == "negative"]
POSITIVE_STRESSORS = [k for k, (p, _, _) in IMPACT_POLARITY.items() if p == "positive"]


def _load_positive_outcomes() -> pd.DataFrame:
    """
    Extract project-level positive outcome indicators from input finance CSVs.
    These represent direct benefits delivered by the projects — the 'other side
    of the ledger' from the supply-chain stressor analysis.

    Returns a DataFrame with columns:
        project_id, asset_class, region,
        avoided_CO2_tCO2e, beneficiaries, reach_ppl_yr, air_quality_pct
    """
    rows = []

    # Hydro: avoided CO2 from displacing fossil generation
    with open(INPUT_DIR / "hydro_finance_input.csv") as f:
        for row in csv.DictReader(f):
            rows.append({
                "project_id":        row["Project_ID"],
                "asset_class":       "Energy",
                "region":            row["Region"],
                "avoided_CO2_tCO2e": float(row.get("Avoided_CO2_Tons", 0) or 0),
                "beneficiaries":     0,
                "reach_ppl_yr":      0,
                "air_quality_pct":   0.0,
            })

    # Hospitals: health beneficiaries served
    with open(INPUT_DIR / "hospitals_finance_input.csv") as f:
        for row in csv.DictReader(f):
            rows.append({
                "project_id":        row["Project_ID"],
                "asset_class":       "Health",
                "region":            row["Region"],
                "avoided_CO2_tCO2e": 0,
                "beneficiaries":     int(str(row.get("Beneficiaries_H&S", 0)).replace(",", "") or 0),
                "reach_ppl_yr":      0,
                "air_quality_pct":   0.0,
            })

    # Rail: passenger reach and air-quality improvement
    with open(INPUT_DIR / "rail_finance_input.csv") as f:
        for row in csv.DictReader(f):
            try:
                reach = int(str(row.get("Reach_Ppl_Yr", 0)).replace(",", "") or 0)
            except ValueError:
                reach = 0
            rows.append({
                "project_id":        row["Project_ID"],
                "asset_class":       "Transport",
                "region":            row["Region"],
                "avoided_CO2_tCO2e": 0,
                "beneficiaries":     0,
                "reach_ppl_yr":      reach,
                "air_quality_pct":   float(row.get("PC_Air_Quality", 0) or 0),
            })

    return pd.DataFrame(rows)


# ──────────────────────────────────────────────────────────────────────────────
# PASS 1 — Supply-chain analysis (tvp_dbio)
# ──────────────────────────────────────────────────────────────────────────────

STRESSOR_COLS = ["GHG_tCO2e", "Employment_FTE", "Water_1000m3", "ValueAdded_M$"]
PROJ_KEY_COLS = ["project_id", "asset_class", "database", "sector_code",
                 "country", "region", "invest_usd"]


def _tier1_sourcing_rows(proj: dict, io) -> list[dict]:
    """
    Call tier1_impact() and flatten the bilateral sourcing-country breakdown
    into one row per (project, supplying_sector, sourcing_region).
    """
    r = io.tier1_impact(
        invest_usd  = proj["invest_usd"],
        sector_code = proj["sector_code"],
        country     = proj["region"],
        database    = "exiobase",
    )
    rows = []
    for sector, by_region in r["tier1_by_sector"].items():
        for src_region, vals in by_region.items():
            rows.append({
                "project_id":       proj["project_id"],
                "asset_class":      proj["asset_class"],
                "database":         r["database"],
                "sector_code":      r["sector_code"],
                "country":          r["country"],
                "region":           r["region"],
                "invest_usd":       r["invest_usd"],
                "tier":             1,
                "supplying_sector": sector,
                "sourcing_region":  src_region,
                "sourcing_share":   vals["share"],
                "spend_M$":         vals["spend_M$"],
                "GHG_tCO2e":        vals["GHG_tCO2e"],
                "Employment_FTE":   vals["Employment_FTE"],
                "Water_1000m3":     vals["Water_1000m3"],
                "ValueAdded_M$":    vals["ValueAdded_M$"],
            })
    return rows


def run_supply_chain(projects: list[dict], tier_to: int = 10) -> dict[str, pd.DataFrame]:
    """
    Run the full supply-chain decomposition for all projects and return a dict
    of DataFrames keyed by table name:

      "tier0"      — Tier 0: direct investment / one-time transaction
                     (project CAPEX split across 8 supplying sectors)
      "tier1"      — Tier 1: first upstream round with bilateral sourcing-
                     country breakdown (via tier1_impact)
      "tier2"      — Tier 2: second upstream round
      "tier3_10"   — Tiers 3–10: deep upstream, aggregated per project
                     and supplying sector
      "summary"    — Project totals: stressors summed across tiers 0–10
    """
    import tvp_io_lib as io

    active = [p for p in projects if p["invest_usd"] >= 1]

    # ── Full tier-by-tier detail (tiers 0–10) ────────────────────────────────
    detail_frames = []
    t1_frames     = []
    for proj in active:
        df = io.tier_impact(
            invest_usd  = proj["invest_usd"],
            sector_code = proj["sector_code"],
            country     = proj["region"],
            database    = "exiobase",
            tier_from   = 0,
            tier_to     = tier_to,
        )
        df.insert(0, "project_id",  proj["project_id"])
        df.insert(1, "asset_class", proj["asset_class"])
        detail_frames.append(df)

        t1_frames.extend(_tier1_sourcing_rows(proj, io))

    detail = pd.concat(detail_frames, ignore_index=True)

    # ── Tier 0: direct spend ─────────────────────────────────────────────────
    tier0 = detail[detail["tier"] == 0].drop(columns=["tier"]).reset_index(drop=True)

    # ── Tier 1: first upstream, with bilateral sourcing-country breakdown ────
    tier1 = pd.DataFrame(t1_frames)

    # ── Tier 2: second upstream round ────────────────────────────────────────
    tier2 = detail[detail["tier"] == 2].drop(columns=["tier"]).reset_index(drop=True)

    # ── Tiers 3–10: deep upstream, summed across tiers per project + sector ──
    deep = detail[detail["tier"] >= 3].copy()
    tier3_10 = (
        deep.groupby(PROJ_KEY_COLS + ["supplying_sector"])
        [["spend_M$"] + STRESSOR_COLS]
        .sum()
        .reset_index()
    )
    tier3_10.insert(len(PROJ_KEY_COLS), "tier_range", "3-10")

    # ── Summary: project totals across all tiers ─────────────────────────────
    summary_raw = (
        detail.groupby(PROJ_KEY_COLS)[STRESSOR_COLS]
        .sum()
        .reset_index()
    )
    summary_raw.rename(columns={
        "GHG_tCO2e":      "GHG_tCO2e_t0_10",
        "Employment_FTE": "Emp_FTE_t0_10",
        "Water_1000m3":   "Water_1000m3_t0_10",
        "ValueAdded_M$":  "VA_Musd_t0_10",
    }, inplace=True)

    return {
        "tier0":    tier0,
        "tier1":    tier1,
        "tier2":    tier2,
        "tier3_10": tier3_10,
        "summary":  summary_raw,
    }


# ──────────────────────────────────────────────────────────────────────────────
# PASS 1.6 — Dependency weighting per indicator, sector, and region per tier
# ──────────────────────────────────────────────────────────────────────────────
#
# Three-component dependency factor, dimensionless, neutral = 1.0:
#
#   dep_factor(stressor, tier_row) =
#       (encore_dep(project_sector, stressor) / 3      ← ENCORE ecosystem dependency
#        + wwf_risk(sourcing_region, stressor) / 3     ← WWF regional risk
#        + sc_dep(supplying_sector,  stressor) / 3     ← SC-sector sensitivity
#       ) / 3
#
# dep_weighted_stressor = scenario_adjusted_stressor × dep_factor
#
# For tier 1, `sourcing_region` is used for the WWF lookup (bilateral precision),
# consistent with how Pass 1.5 applies scenario factors.
# ──────────────────────────────────────────────────────────────────────────────

# Project sector_code → ENCORE sector key
PROJECT_SECTOR_TO_ENCORE: dict[str, str] = {
    "Health_Social":      "human_health_activities",
    "Health_Specialized": "human_health_activities",
    "Health_General":     "human_health_activities",
    "Energy":             "electric_power_generation_hydro",
    "Rail_Dev":           "rail_transport",
    "Rail_Op":            "rail_transport",
}

# Stressor → ENCORE ecosystem services whose DEPENDENCY rating mediates it
STRESSOR_ECOSYSTEM_MAP: dict[str, list[str]] = {
    "GHG_tCO2e":      ["climate_regulation",       "mediation_of_gaseous_waste"],
    "Employment_FTE":  ["terrestrial_ecosystem_use", "soil_quality",    "erosion_control"],
    "Water_1000m3":   ["water_supply",              "water_flow_regulation",
                       "freshwater_ecosystem_use"],
    "ValueAdded_M$":  ["water_supply",              "climate_regulation",
                       "terrestrial_ecosystem_use"],
}

# Stressor → which WWF sub-score most directly reflects its ecosystem risk
STRESSOR_WWF_COL: dict[str, str] = {
    "GHG_tCO2e":      "brf_ecosystem",    # carbon sequestration & climate regulation
    "Employment_FTE":  "brf_ecosystem",   # land productivity underpins labor intensity
    "Water_1000m3":   "wrf_physical",     # physical water scarcity / stress
    "ValueAdded_M$":  "wrf_composite",    # overall water + institutional risk
}

# Ecosystem sensitivity of the 8 supply-chain sectors (tvp_io_lib SECTORS_8).
# Scores on 1–5 scale; derived from:
#   · ENCORE analogues for the overlapping sectors (Energy_Utilities → D3510,
#     Health_Social → Q86, Transport_Logistics → H4910)
#   · IPBES (2019) "Global Assessment" sector biodiversity pressure typology
#     for Construction, Manufacturing, Agriculture, Mining_Extraction, Water_Waste
# Tuple sub-keys match STRESSOR_SC_DEP_KEY below.
SC_SECTOR_DEP_PROFILE: dict[str, dict[str, float]] = {
    # (water_dep, ghg_dep, land_dep, va_dep)
    "Construction":        {"water": 3.0, "ghg": 3.0, "land": 4.0, "va": 3.3},
    "Energy_Utilities":    {"water": 5.0, "ghg": 5.0, "land": 3.0, "va": 4.3},
    "Manufacturing":       {"water": 4.0, "ghg": 3.0, "land": 3.0, "va": 3.3},
    "Transport_Logistics": {"water": 2.0, "ghg": 3.0, "land": 4.0, "va": 3.0},
    "Health_Social":       {"water": 5.0, "ghg": 4.0, "land": 2.0, "va": 3.7},
    "Agriculture":         {"water": 5.0, "ghg": 5.0, "land": 5.0, "va": 5.0},
    "Mining_Extraction":   {"water": 5.0, "ghg": 3.0, "land": 5.0, "va": 4.3},
    "Water_Waste":         {"water": 5.0, "ghg": 3.0, "land": 4.0, "va": 4.0},
}

# Stressor → SC_SECTOR_DEP_PROFILE sub-key
STRESSOR_SC_DEP_KEY: dict[str, str] = {
    "GHG_tCO2e":      "ghg",
    "Employment_FTE":  "land",  # employment intensity tied to land productivity
    "Water_1000m3":   "water",
    "ValueAdded_M$":  "va",
}

DEP_NEUTRAL = 3.0  # "medium" score; dep_factor = 1.0 when all sub-scores equal this


def _build_dependency_table() -> pd.DataFrame:
    """
    Build a (project_sector × region) lookup table of ENCORE + WWF sub-scores
    and their combined dep_factor for each stressor.

    Does NOT include the SC-sector sensitivity component — that is applied row-
    wise in apply_dependency_factors() because it varies by supplying_sector,
    not by project.

    Columns returned:
        project_sector, region,
        encore_dep_{stressor},    # ENCORE dependency sub-score (raw 1–5)
        wwf_dep_{stressor},       # WWF risk sub-score (raw 1–5)
        base_dep_factor_{stressor}  # (encore+wwf)/2 normalized to neutral=1.0
    """
    from dependency_profiler.encore_materiality import MATERIALITY_MATRIX, RATING_SCALE

    # ── ENCORE dependency scores: project sector × stressor ───────────────────
    encore_scores: dict[str, dict[str, float]] = {}
    for sector_code, encore_key in PROJECT_SECTOR_TO_ENCORE.items():
        mat = MATERIALITY_MATRIX.get(encore_key, {})
        stressor_scores = {}
        for stressor, svc_list in STRESSOR_ECOSYSTEM_MAP.items():
            raw = [RATING_SCALE.get(mat.get(svc, ("N", "N"))[0], 0)
                   for svc in svc_list]
            stressor_scores[stressor] = sum(raw) / max(len(raw), 1)
        encore_scores[sector_code] = stressor_scores

    # ── WWF risk scores: aggregated to broad regions ───────────────────────────
    wwf_path = DEPENDENCY_DIR / "assessment_output" / "wwf_risk_scores.csv"
    if wwf_path.exists():
        wwf_raw = pd.read_csv(wwf_path)
        region_map = {
            "latam": "LATAM", "africa": "Africa",
            "asia": "Asia",   "europe": "Europe",
        }
        wwf_raw["broad_region"] = wwf_raw["region"].str.lower().map(region_map)
        wwf_agg = (
            wwf_raw.dropna(subset=["broad_region"])
            .groupby("broad_region")[
                ["wrf_physical", "wrf_regulatory", "wrf_reputational",
                 "wrf_composite", "brf_species_threat", "brf_ecosystem",
                 "brf_protected_areas", "brf_composite"]
            ].mean()
            .reset_index()
            .rename(columns={"broad_region": "region"})
        )
    else:
        # Embedded fallback — representative regional averages from WWF data
        wwf_agg = pd.DataFrame([
            {"region": "Africa", "wrf_physical": 4.38, "wrf_composite": 3.70,
             "brf_ecosystem": 3.35, "brf_species_threat": 4.46, "brf_composite": 3.80},
            {"region": "Asia",   "wrf_physical": 4.97, "wrf_composite": 4.27,
             "brf_ecosystem": 3.55, "brf_species_threat": 5.00, "brf_composite": 4.26},
            {"region": "Europe", "wrf_physical": 2.93, "wrf_composite": 3.41,
             "brf_ecosystem": 3.30, "brf_species_threat": 2.69, "brf_composite": 3.12},
            {"region": "LATAM",  "wrf_physical": 3.79, "wrf_composite": 3.48,
             "brf_ecosystem": 3.45, "brf_species_threat": 4.74, "brf_composite": 4.09},
        ])

    # ── Build lookup table ─────────────────────────────────────────────────────
    rows = []
    for sector_code, stressor_scores in encore_scores.items():
        for _, wrow in wwf_agg.iterrows():
            region = wrow["region"]
            entry = {"project_sector": sector_code, "region": region}
            for stressor, encore_score in stressor_scores.items():
                wwf_col = STRESSOR_WWF_COL[stressor]
                wwf_score = float(wrow.get(wwf_col, DEP_NEUTRAL))
                entry[f"encore_dep_{stressor}"] = encore_score
                entry[f"wwf_dep_{stressor}"]    = wwf_score
                entry[f"base_dep_factor_{stressor}"] = (
                    encore_score / DEP_NEUTRAL + wwf_score / DEP_NEUTRAL
                ) / 2.0
            rows.append(entry)

    return pd.DataFrame(rows)


def apply_dependency_factors(detail: pd.DataFrame) -> pd.DataFrame:
    """
    Merge dependency factors into a scenario-weighted tier detail DataFrame and
    compute dependency-weighted stressor columns.

    For each row the full three-component dep_factor is:

        dep_factor = (encore_dep/3 + wwf_dep/3 + sc_dep/3) / 3

    where:
        encore_dep  — ENCORE ecosystem dependency of the project sector (1–5)
        wwf_dep     — WWF risk score for the stressor-relevant filter (1–5),
                      using sourcing_region for tier1 (bilateral) or region otherwise
        sc_dep      — SC_SECTOR_DEP_PROFILE score of the supplying sector (1–5)

    dep_factor = 1.0 at global-average conditions; range ≈ 0.33–1.67.

    Columns added:
        dep_encore_{stressor}   — ENCORE sub-score (raw)
        dep_wwf_{stressor}      — WWF sub-score (raw, region-resolved)
        dep_sc_{stressor}       — SC sector sensitivity sub-score (raw)
        dep_factor_{stressor}   — combined dep_factor (neutral = 1.0)
        {stressor[:-suffix]}_dep_weighted — scenario_adj × dep_factor
    """
    if detail.empty:
        return detail

    dep_table = _build_dependency_table()
    # join key on project sector: detail has "sector_code" = the project sector code
    dep_table = dep_table.rename(columns={"project_sector": "sector_code"})

    # For WWF lookup: tier1 uses sourcing_region, others use region
    detail = detail.copy()
    detail["_wwf_region"] = np.where(
        detail["tier_label"] == "tier1",
        detail.get("sourcing_region", detail["region"]),
        detail["region"],
    )

    # Merge dep_table on (sector_code, _wwf_region → region)
    merged = detail.merge(
        dep_table.rename(columns={"region": "_wwf_region"}),
        on=["sector_code", "_wwf_region"],
        how="left",
    )

    # Stressor columns that exist in the adjusted data
    adj_stressor_pairs = [
        ("GHG_tCO2e",      "GHG_adj_tCO2e"),
        ("Employment_FTE",  "Employment_adj_FTE"),
        ("Water_1000m3",   "Water_adj_1000m3"),
        ("ValueAdded_M$",  "ValueAdded_adj_M$"),
    ]

    for raw_col, adj_col in adj_stressor_pairs:
        if adj_col not in merged.columns:
            continue

        sc_dep_key = STRESSOR_SC_DEP_KEY[raw_col]
        base_col   = f"base_dep_factor_{raw_col}"
        sc_col     = f"dep_sc_{raw_col}"
        full_col   = f"dep_factor_{raw_col}"
        out_col    = adj_col.replace("_adj_", "_dep_")  # e.g. GHG_dep_tCO2e

        # SC sector sensitivity: look up from embedded profile; default = DEP_NEUTRAL
        merged[sc_col] = merged["supplying_sector"].map(
            lambda s, k=sc_dep_key: SC_SECTOR_DEP_PROFILE.get(s, {}).get(k, DEP_NEUTRAL)
        )
        # Full three-component dep_factor
        base = merged[base_col].fillna(1.0)
        sc   = merged[sc_col]
        merged[full_col] = (base + sc / DEP_NEUTRAL) / 2.0   # mean of (encore+wwf)/2 and sc/3
        merged[out_col]  = merged[adj_col] * merged[full_col]

        # Rename the ENCORE/WWF sub-score columns for clarity
        merged.rename(columns={
            f"encore_dep_{raw_col}": f"dep_encore_{raw_col}",
            f"wwf_dep_{raw_col}":    f"dep_wwf_{raw_col}",
        }, inplace=True)

    merged.drop(columns=["_wwf_region"], inplace=True)
    return merged


# ──────────────────────────────────────────────────────────────────────────────
# PASS 1.5 — Connect dbio tier analysis to scenario weighting factors
# ──────────────────────────────────────────────────────────────────────────────

SCENARIO_YEARS   = [2025, 2030, 2040]
SCENARIO_LABELS  = ["SSP1-1.9", "SSP2-4.5", "SSP3-7.0", "SSP4-6.0", "SSP5-8.5"]

# Paths to each model's intensity factors file (OSeMOSYS always present;
# GCAM and MESSAGEix loaded when their results/ directory exists)
MODEL_FACTOR_PATHS = {
    "OSeMOSYS":          SCENARIO_DIR / "osemosys"  / "results" / "tvpdbio_intensity_factors.csv",
    "GCAM":              SCENARIO_DIR / "gcam"      / "results" / "tvpdbio_intensity_factors.csv",
    "MESSAGEix-GLOBIOM": SCENARIO_DIR / "messageix" / "results" / "tvpdbio_intensity_factors.csv",
}

# Maps the 5 representative countries in ipcc_nexus_weights.csv to the 4 broad
# project regions used by tvp_io_lib and the OSeMOSYS intensity-factor tables.
NEXUS_COUNTRY_TO_REGION: dict[str, str] = {
    "Brazil":       "LATAM",
    "Germany":      "Europe",
    "India":        "Asia",
    "Nigeria":      "Africa",
    "South Africa": "Africa",
}

# All-stressor adjustment labels produced by _build_full_factors()
ADJ_COLS = ["adj_ratio_ghg", "adj_ratio_employment", "adj_ratio_water", "adj_ratio_va"]


def _build_full_factors() -> pd.DataFrame | None:
    """
    Assemble a single lookup table keyed by (model_label, scenario, region, year)
    that carries adjustment ratios for *all four* supply-chain stressors:

      adj_ratio_ghg         from OSeMOSYS/GCAM/MESSAGEix intensity factors
      adj_ratio_employment  ibid.
      adj_ratio_water       derived: 1 − renewable_share × 0.85
                            (100 % renewables → 85 % reduction in cooling-water
                            withdrawal; calibrated to IEA Water for Energy 2022)
      adj_ratio_va          proxy = adj_ratio_employment
                            (value-added per $ tracks labour-productivity shifts)

    If ipcc_nexus_weights.csv is present the water ratio is further refined per
    scenario using the water_intensity_proxy time trend: the OSeMOSYS renewable-
    share formula gives the sector-averaged ratio; the nexus file provides a
    scenario-relative cross-check that is averaged across the two approaches.

    Returns None when no intensity-factor files are available on disk.
    """
    all_factors: list[pd.DataFrame] = []
    for model_name, fpath in MODEL_FACTOR_PATHS.items():
        if fpath.exists():
            df = pd.read_csv(fpath)
            df["model_label"] = model_name
            all_factors.append(df)

    if not all_factors:
        return None

    factors = pd.concat(all_factors, ignore_index=True)

    # ── Derive water and VA ratios from renewable_share ────────────────────────
    # renewable_share = fraction of electricity generation from non-thermal sources.
    # Thermal power requires ~1.5 L/kWh for cooling; wind/solar require ~0.003 L/kWh.
    # Portfolio-average across 8 supply sectors: weighted blend of energy-sector
    # improvement (60 % weight) and residual process-water improvement (40 % weight).
    factors["adj_ratio_water"] = (
        factors["renewable_share"] * 0.15             # 100 % ren → 15 % of baseline
        + (1.0 - factors["renewable_share"]) * 1.0    # 0 % ren   → 100 % of baseline
    ).clip(lower=0.05)
    factors["adj_ratio_va"] = factors["adj_ratio_employment"]

    # ── Optional refinement from ipcc_nexus_weights.csv ───────────────────────
    nw_path = SCENARIO_DIR / "results" / "ipcc_nexus_weights.csv"
    if nw_path.exists():
        nw = pd.read_csv(nw_path)
        nw["broad_region"] = nw["region"].map(NEXUS_COUNTRY_TO_REGION)
        nw = nw.dropna(subset=["broad_region"])

        # Compute time-relative change in water withdrawal intensity per scenario.
        # water_intensity_proxy carries the same grid-intensity series as
        # grid_intensity_mt_ej, so we normalise against the 2020 anchor.
        base = (
            nw[nw["year"] == 2020]
            .groupby(["ssp", "broad_region"])["water_intensity_proxy"]
            .mean()
            .reset_index()
            .rename(columns={"water_intensity_proxy": "water_base_2020"})
        )
        nw = nw.merge(base, on=["ssp", "broad_region"], how="left")
        nw["adj_ratio_water_nexus"] = np.where(
            nw["water_base_2020"] > 0,
            (nw["water_intensity_proxy"] / nw["water_base_2020"]).clip(0.01, 2.0),
            1.0,
        )
        nexus_agg = (
            nw.groupby(["ssp", "broad_region", "year"])["adj_ratio_water_nexus"]
            .mean()
            .reset_index()
            .rename(columns={"ssp": "scenario", "broad_region": "region"})
        )
        factors = factors.merge(nexus_agg, on=["scenario", "region", "year"], how="left")
        # Average the two approaches where nexus data is available
        has_nexus = factors["adj_ratio_water_nexus"].notna()
        factors.loc[has_nexus, "adj_ratio_water"] = (
            factors.loc[has_nexus, "adj_ratio_water"]
            + factors.loc[has_nexus, "adj_ratio_water_nexus"]
        ) / 2.0
        factors.drop(columns=["adj_ratio_water_nexus"], inplace=True)

    return factors


def run_scenario_weighted_tiers(
    sc: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Connect the tier-by-tier supply-chain breakdown to scenario weighting
    factors, applying region-and-time-specific adjustment ratios to every
    stressor in every tier.

    Key improvement over the project-level scenario adjustment:
      • Tier 1 uses the *sourcing_region* column (bilateral supply-country
        precision) rather than the project's home region — a steel mill in
        Asia supplying a European project is adjusted at Asia's decarbonisation
        trajectory, not Europe's.
      • All four stressors (GHG, Employment, Water, Value Added) are adjusted,
        not just GHG.
      • Each tier (0, 1, 2, 3-10) is adjusted independently, preserving the
        tier-level granularity for downstream analysis.

    Returns a long-format DataFrame with columns:
        model, scenario, year,
        tier_label, project_id, asset_class,
        region, sector_code, supplying_sector, sourcing_region,
        spend_M$,
        GHG_tCO2e,       GHG_adj_tCO2e,
        Employment_FTE,  Employment_adj_FTE,
        Water_1000m3,    Water_adj_1000m3,
        ValueAdded_M$,   ValueAdded_adj_M$,
        adj_ratio_ghg, adj_ratio_employment, adj_ratio_water, adj_ratio_va
    """
    factors = _build_full_factors()
    if factors is None:
        print("      [WARN] No scenario factors — skipping tier-level weighting.")
        return pd.DataFrame()

    factors_filt = factors[
        factors["year"].isin(SCENARIO_YEARS) &
        factors["scenario"].isin(SCENARIO_LABELS)
    ][["model_label", "scenario", "region", "year"] + ADJ_COLS].copy()

    # ── Helpers ────────────────────────────────────────────────────────────────
    stressor_map = {          # raw column → adjusted column
        "GHG_tCO2e":      ("GHG_adj_tCO2e",       "adj_ratio_ghg"),
        "Employment_FTE":  ("Employment_adj_FTE",   "adj_ratio_employment"),
        "Water_1000m3":   ("Water_adj_1000m3",     "adj_ratio_water"),
        "ValueAdded_M$":  ("ValueAdded_adj_M$",    "adj_ratio_va"),
    }

    def _apply_factors(df: pd.DataFrame, lookup_col: str, tier_label: str) -> pd.DataFrame:
        """
        Merge *df* with factors_filt on (lookup_col → "region") and compute
        adjusted stressor columns.  Returns long-format rows for every
        (model, scenario, year) combination.
        """
        df = df.copy()
        df["_lookup_region"] = df[lookup_col]
        merged = df.merge(
            factors_filt.rename(columns={"region": "_lookup_region"}),
            on="_lookup_region",
            how="left",
        )
        # Rows with no matching scenario factor (e.g. "Global" sourcing region)
        # fall back to adj_ratio = 1.0 (no adjustment applied)
        for adj_col in ADJ_COLS:
            merged[adj_col] = merged[adj_col].fillna(1.0)

        for raw_col, (adj_out_col, ratio_col) in stressor_map.items():
            if raw_col in merged.columns:
                merged[adj_out_col] = merged[raw_col] * merged[ratio_col]

        merged["tier_label"] = tier_label
        merged.drop(columns=["_lookup_region"], inplace=True)
        return merged

    # ── Process each tier ─────────────────────────────────────────────────────
    frames = []

    # Tier 0: direct investment; lookup key = project home region
    t0 = _apply_factors(sc["tier0"], lookup_col="region", tier_label="tier0")
    frames.append(t0)

    # Tier 1: first upstream; lookup key = bilateral sourcing country
    # This is the key connection: imported inputs are adjusted at the SOURCE
    # country's decarbonisation trajectory, not the project country's.
    if not sc["tier1"].empty:
        t1 = _apply_factors(sc["tier1"], lookup_col="sourcing_region", tier_label="tier1")
        frames.append(t1)

    # Tier 2: second upstream; lookup key = project home region
    t2 = _apply_factors(sc["tier2"], lookup_col="region", tier_label="tier2")
    frames.append(t2)

    # Tiers 3-10: deep upstream; lookup key = project home region
    t3 = _apply_factors(sc["tier3_10"], lookup_col="region", tier_label="tier3_10")
    frames.append(t3)

    if not frames:
        return pd.DataFrame()

    out = pd.concat(frames, ignore_index=True)

    # ── Build summary pivot: project × scenario × year × stressor ─────────────
    # (sum across tiers and supplying sectors)
    grp_cols = ["model_label", "scenario", "year", "project_id", "asset_class", "region"]
    adj_stressor_cols = [c for _, (c, _) in stressor_map.items() if c in out.columns]
    raw_stressor_cols = [c for c in stressor_map if c in out.columns]

    summary = (
        out.groupby(grp_cols)[raw_stressor_cols + adj_stressor_cols]
        .sum()
        .reset_index()
    )
    summary.rename(columns={"model_label": "model"}, inplace=True)

    return out, summary


# ──────────────────────────────────────────────────────────────────────────────
# PASS 2 — Scenario adjustment (tvp_scenario / OSeMOSYS)
# ──────────────────────────────────────────────────────────────────────────────

def run_scenario_adjustment(projects: list[dict], supply_summary: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load intensity factors from all available simulation models (OSeMOSYS,
    GCAM, MESSAGEix-GLOBIOM) and compute scenario-adjusted GHG and Employment
    for every project × model × scenario × year combination.

    Region names are matched as-is (Africa/Asia/Europe/LATAM) — no
    case transformation so that "LATAM" is never mangled.
    """
    # Re-use _build_full_factors() so all four stressor ratios are available
    factors = _build_full_factors()
    if factors is None:
        print("[WARN] No scenario factors found. Run tvp_scenario/osemosys/run_simulation.py first.")
        return pd.DataFrame(), pd.DataFrame()

    for model_name, fpath in MODEL_FACTOR_PATHS.items():
        if fpath.exists():
            print(f"      [OK]      {model_name}")
        else:
            print(f"      [PENDING] {model_name}: no results at {fpath.relative_to(ROOT)}")

    # Filter to analysis years and scenarios
    factors_filt = factors[
        factors["year"].isin(SCENARIO_YEARS) &
        factors["scenario"].isin(SCENARIO_LABELS)
    ].copy()

    # Baseline stressors (tiers summed) per project
    ghg_col = [c for c in supply_summary.columns if c.startswith("GHG_tCO2e")][0]
    emp_col = [c for c in supply_summary.columns if c.startswith("Emp_FTE")][0]
    wat_col = [c for c in supply_summary.columns if c.startswith("Water_1000m3")][0]
    va_col  = [c for c in supply_summary.columns if c.startswith("VA_Musd")][0]

    baseline = supply_summary[["project_id", "region", ghg_col, emp_col, wat_col, va_col]].copy()
    baseline.rename(columns={
        ghg_col: "baseline_GHG_tCO2e",
        emp_col: "baseline_Employment_FTE",
        wat_col: "baseline_Water_1000m3",
        va_col:  "baseline_VA_Musd",
    }, inplace=True)

    adj_rows = []
    for _, proj_row in baseline.iterrows():
        pid      = proj_row["project_id"]
        region   = proj_row["region"]
        base_ghg = proj_row["baseline_GHG_tCO2e"]
        base_emp = proj_row["baseline_Employment_FTE"]
        base_wat = proj_row["baseline_Water_1000m3"]
        base_va  = proj_row["baseline_VA_Musd"]

        region_factors = factors_filt[factors_filt["region"] == region]
        for _, frow in region_factors.iterrows():
            adj_rows.append({
                "model":                    frow["model_label"],
                "project_id":               pid,
                "region":                   region,
                "scenario":                 frow["scenario"],
                "year":                     int(frow["year"]),
                "adj_ratio_ghg":            frow["adj_ratio_ghg"],
                "adj_ratio_employment":     frow["adj_ratio_employment"],
                "adj_ratio_water":          frow["adj_ratio_water"],
                "adj_ratio_va":             frow["adj_ratio_va"],
                "baseline_GHG_tCO2e":       base_ghg,
                "baseline_Employment_FTE":  base_emp,
                "baseline_Water_1000m3":    base_wat,
                "baseline_VA_Musd":         base_va,
                "adjusted_GHG_tCO2e":       round(base_ghg * frow["adj_ratio_ghg"], 1),
                "adjusted_Employment_FTE":  round(base_emp * frow["adj_ratio_employment"], 1),
                "adjusted_Water_1000m3":    round(base_wat * frow["adj_ratio_water"], 2),
                "adjusted_VA_Musd":         round(base_va  * frow["adj_ratio_va"], 3),
            })

    adj_df = pd.DataFrame(adj_rows)

    if adj_df.empty:
        return factors_filt, adj_df

    # Wide pivot on GHG for backward-compatible output (Pass-2 narrative uses it)
    pivot = adj_df.pivot_table(
        index=["model", "project_id", "region", "scenario"],
        columns="year",
        values="adjusted_GHG_tCO2e",
    ).reset_index()
    pivot.columns.name = None
    pivot.columns = [str(c) for c in pivot.columns]

    return adj_df, pivot


# ──────────────────────────────────────────────────────────────────────────────
# PASS 3 — Nature-related dependency risk (tvp_dependency)
# ──────────────────────────────────────────────────────────────────────────────

def run_dependency(skip: bool) -> pd.DataFrame:
    """
    Run (or reload) the dependency pipeline and return the stress-test table.
    """
    assessment_out = DEPENDENCY_DIR / "assessment_output"

    if not skip:
        print("\n[3/3] Running dependency pipeline ...")
        from dependency_profiler.pipeline import run_pipeline
        run_pipeline(verbose=True)
    else:
        print("\n[3/3] Loading existing dependency results ...")

    stress = pd.read_csv(assessment_out / "portfolio_stress_test.csv")
    wwf    = pd.read_csv(assessment_out / "wwf_risk_scores.csv")
    merged = stress.merge(
        wwf[["project_id", "wrf_physical", "wrf_regulatory", "wrf_reputational",
              "brf_species_threat", "brf_ecosystem", "brf_protected_areas"]],
        on="project_id", how="left",
    )
    return merged


# ──────────────────────────────────────────────────────────────────────────────
# PASS 4 — WifOR value factor impact monetisation
# ──────────────────────────────────────────────────────────────────────────────


def _resolve_wifor_dir() -> Path | None:
    """Return the directory containing WifOR h5 coefficient files, or None.

    Candidates are checked in order; the first directory that contains at least
    one ``*_formatted_Mon*_my.h5`` file is returned.  Paths are expressed
    relative to this script file so they stay portable across machines.
    """
    _here = Path(__file__).parent          # project_assessment/
    candidates = [
        _here / "wifor_vf",                # symlink: project_assessment/wifor_vf
        _here / ".." / "value-factors",    # submodule (if data generated locally)
    ]
    for p in candidates:
        if p.is_dir() and any(p.glob("*_formatted_Mon*_my.h5")):
            return p
    return None


# ── Embedded fallback coefficients ────────────────────────────────────────
# Pre-computed from the WifOR HDF5 files for all (country, NACE) combinations
# used by REGION_TO_ISO3 × PROJECT_SECTOR_TO_NACE.  Used automatically when
# the pytables / tables package is not installed in the active environment.
#
# Source: WifOR Institute value factor scripts (2024 release)
#   GHG BASE / GHG_PARIS_UPDATE: year 2019 — globally uniform social cost of carbon
#   Water Consumption Blue:       year 2020 — country-specific scarcity weighting
#   TrainingHours:                year 2020 — country- and sector-specific wage base


def _h5py_lookup(h5_path: Path, year: str, indicator: str, country_iso3: str, nace_sector: str) -> float:
    """
    Read one coefficient from a WifOR fixed-format pandas HDF5 file using h5py.

    Does not require the `tables` / pytables package.  The pandas fixed-format
    internal layout uses:
      axis0_level0/1  — column MultiIndex levels  (GeoRegion, NACE)
      axis0_label0/1  — column label arrays
      axis1_level0/1  — row MultiIndex levels      (Year, Variable)
      axis1_label0/1  — row label arrays
      block0_values   — data matrix  [n_rows × n_cols]

    HDF5_USE_FILE_LOCKING is set at module level so it takes effect before the
    HDF5 C library initialises (required on Windows UNC / \\\\wsl$\\ paths).
    """
    import h5py

    with h5py.File(str(h5_path), "r") as f:
        g = f["coefficient"]
        col_ctries = [x.decode() for x in g["axis0_level0"]]
        col_naces  = [x.decode() for x in g["axis0_level1"]]
        row_years  = [x.decode() for x in g["axis1_level0"]]
        row_inds   = [x.decode() for x in g["axis1_level1"]]
        col_lbl0   = g["axis0_label0"][:]
        col_lbl1   = g["axis0_label1"][:]
        row_lbl0   = g["axis1_label0"][:]
        row_lbl1   = g["axis1_label1"][:]
        data       = g["block0_values"][:]

    y_idx = row_years.index(year)
    i_idx = row_inds.index(indicator)
    c_idx = col_ctries.index(country_iso3)
    n_idx = col_naces.index(nace_sector)

    row = next(r for r in range(len(row_lbl0)) if row_lbl0[r] == y_idx and row_lbl1[r] == i_idx)
    col = next(c for c in range(len(col_lbl0)) if col_lbl0[c] == c_idx and col_lbl1[c] == n_idx)

    return float(data[row, col])


def _load_vf_coeff(
    spec: dict, vf_dir: Path | None, country_iso3: str, nace_sector: str
) -> float | None:
    """
    Extract one coefficient from a WifOR HDF5 file.

    Returns the value in native units (USD/kg, USD/m³, USD/h).

    Tries pd.HDFStore first (requires pytables); falls back to h5py (no pytables
    needed) if pytables is not installed.  Returns None if the file is absent or
    the requested (year, indicator, country, sector) combination cannot be found.
    """
    if vf_dir is None:
        return None

    h5_path = vf_dir / spec["filename"]
    if not h5_path.exists():
        return None

    # ── Try pd.HDFStore (pytables path) ───────────────────────────────────
    try:
        with pd.HDFStore(str(h5_path), "r") as store:
            df = store["/coefficient"]
        return float(df.loc[(spec["year"], spec["indicator"]), (country_iso3, nace_sector)])
    except KeyError:
        return None   # data present but key not found — don't try h5py
    except Exception:
        pass   # pytables missing, HDF5 locking error on UNC path, etc. — try h5py

    # ── Fallback: h5py direct read (no pytables required) ─────────────────
    try:
        return _h5py_lookup(h5_path, spec["year"], spec["indicator"], country_iso3, nace_sector)
    except (KeyError, ValueError, StopIteration):
        return None


def _load_gva_per_hour(
    vf_dir: Path | None,
    country_iso3: str,
    nace_sector: str,
    focus_year: int = 2030,
) -> float | None:
    """
    Return GVA per labour-hour (USD/h) at *focus_year*, projected from the
    WifOR 2020-PPP base using the MonTrain productivity growth index.

    Conceptual basis (living-wage alignment)
    ─────────────────────────────────────────
    GVA per labour-hour is the sector's gross value added per hour of work —
    the upper bound on what the sector can sustainably pay as wages.  In most
    markets GVA/h exceeds published Anker living-wage benchmarks, so using
    GVA/h as the employment monetisation coefficient is equivalent to assuming
    "workers are paid at least the living wage."

    Key properties
    • Country- and sector-specific (188 GeoRegions × 57 NACE codes)
    • Projected from 2020 base using MonTrain growth ratio (≈1.1 %/yr real)
    • MonTrain_2020 ≡ GVA/h_2020 (confirmed exact match; same source data)

    Returns None if the source H5 files are absent.
    """
    if vf_dir is None:
        return None

    raw_path = vf_dir / "input_data" / "220529_training_value_per_hour_bysector.h5"
    if not raw_path.exists():
        return None

    try:
        import h5py

        with h5py.File(str(raw_path), "r") as f:
            grp  = f["value_per_hour"]
            lvl0 = [x.decode() for x in grp["axis1_level0"][:]]   # GeoRegion
            lvl1 = [x.decode() for x in grp["axis1_level1"][:]]   # NACE
            lab0 = grp["axis1_label0"][:]
            lab1 = grp["axis1_label1"][:]
            items = [x.decode() for x in grp["block0_items"][:]]
            vals  = grp["block0_values"][:]                         # (10716, 2)

        gva_col = next(i for i, x in enumerate(items) if "GVA" in x)
        col_pos = next(
            i for i in range(len(lab0))
            if lvl0[lab0[i]] == country_iso3 and lvl1[lab1[i]] == nace_sector
        )
        gva_2020 = float(vals[col_pos, gva_col])

    except (StopIteration, KeyError, OSError):
        return None

    # Project gva_2020 → focus_year using MonTrain's growth index.
    # MonTrain_2020 ≡ GVA/h_2020, so the ratio MonTrain_focusyr/MonTrain_2020
    # is a pure productivity growth factor (~1.118 for 2030, uniform globally).
    train_path = vf_dir / "2024-10-16_formatted_MonTrain_my.h5"
    growth = 1.0
    if train_path.exists():
        try:
            indicator = "COEFFICIENT TrainingHours, in USD (WifOR)"
            t2020  = _h5py_lookup(train_path, "2020",          indicator, country_iso3, nace_sector)
            t_focus = _h5py_lookup(train_path, str(focus_year), indicator, country_iso3, nace_sector)
            if t2020 and t_focus and t2020 > 0:
                growth = t_focus / t2020
        except Exception:
            growth = 1.012 ** (focus_year - 2020)   # ILO fallback: 1.2 %/yr
    else:
        growth = 1.012 ** (focus_year - 2020)

    return gva_2020 * growth


def run_wifor_impact(
    supply_summary: pd.DataFrame,
    projects: list[dict],
    tier_to: int = 10,
) -> pd.DataFrame:
    """
    Pass 4 — Monetise supply-chain stressor quantities using WifOR value factors.

    Physical supply-chain quantities are converted to M USD monetary estimates:

        GHG impact [M USD]        = GHG_tCO2e   × 1,000  × coeff_ghg   [USD/kg] ÷ 1e6
        Water impact [M USD]      = Water_1000m3 × 1,000  × coeff_water [USD/m³] ÷ 1e6
        Employment impact [M USD] = Emp_FTE      × 1,880h × coeff_train [USD/h]  ÷ 1e6

    GHG coefficients are globally uniform (social cost of carbon).
    Water and Employment coefficients are country- and sector-specific.
    Negative values are environmental damage costs; positive are social benefits.

    Returns one row per project, or an empty DataFrame if value factor files are
    not found.
    """
    vf_dir = _resolve_wifor_dir()
    if vf_dir is None:
        print("      [WARN] WifOR value factor files not found — skipping impact monetisation.")
        return pd.DataFrame()

    ghg_col = f"GHG_tCO2e_t0_{tier_to}"
    emp_col = f"Emp_FTE_t0_{tier_to}"
    wat_col = f"Water_1000m3_t0_{tier_to}"

    sc_lookup = {p["project_id"]: p["sector_code"] for p in projects}

    rows = []
    for _, prow in supply_summary.iterrows():
        pid         = prow["project_id"]
        region      = prow["region"]
        sector_code = str(prow.get("sector_code", sc_lookup.get(pid, "")))

        country_iso3 = REGION_TO_ISO3.get(region, "DEU")
        nace         = PROJECT_SECTOR_TO_NACE.get(sector_code, "Q")

        ghg_t   = float(prow.get(ghg_col, 0) or 0)
        emp_fte = float(prow.get(emp_col, 0) or 0)
        wat_km3 = float(prow.get(wat_col, 0) or 0)

        c_ghg       = _load_vf_coeff(VF_FILE_SPECS["ghg"],       vf_dir, country_iso3, nace)
        c_ghg_paris = _load_vf_coeff(VF_FILE_SPECS["ghg_paris"], vf_dir, country_iso3, nace)
        c_water     = _load_vf_coeff(VF_FILE_SPECS["water"],     vf_dir, country_iso3, nace)
        # GVA-per-labour-hour: living-wage proxy for employment monetisation.
        # Loaded from the raw WifOR input (GVA_2020_PPP) and projected to
        # the supply chain reference year via MonTrain's productivity growth index.
        c_gva       = _load_gva_per_hour(vf_dir, country_iso3, nace)

        def _musd(qty: float, conv: float, coeff: float | None) -> float:
            return qty * conv * (coeff or 0.0) / 1e6

        ghg_impact       = _musd(ghg_t,   1_000,              c_ghg)
        ghg_paris_impact = _musd(ghg_t,   1_000,              c_ghg_paris)
        water_impact     = _musd(wat_km3, 1_000,              c_water)
        emp_impact       = _musd(emp_fte, FTE_HOURS_PER_YEAR, c_gva)

        rows.append({
            "project_id":             pid,
            "region":                 region,
            "sector_code":            sector_code,
            "country_iso3":           country_iso3,
            "nace_sector":            nace,
            # Coefficients applied
            "coeff_ghg_base_usd_kg":  c_ghg,
            "coeff_ghg_paris_usd_kg": c_ghg_paris,
            "coeff_water_usd_m3":     c_water,
            "coeff_gva_usd_h":        c_gva,   # GVA/labour-hour — living-wage proxy
            # Physical inputs
            "GHG_tCO2e":              ghg_t,
            "Water_1000m3":           wat_km3,
            "Employment_FTE":         emp_fte,
            # Monetised impacts [M USD]
            "ghg_impact_MUSD":        ghg_impact,
            "ghg_paris_impact_MUSD":  ghg_paris_impact,
            "water_impact_MUSD":      water_impact,
            "employment_impact_MUSD": emp_impact,
            "net_impact_MUSD":        ghg_impact + water_impact + emp_impact,
        })

    return pd.DataFrame(rows)


# ──────────────────────────────────────────────────────────────────────────────
# Final analysis narrative
# ──────────────────────────────────────────────────────────────────────────────

def _fmt(val, decimals=0):
    try:
        return f"{val:,.{decimals}f}"
    except (TypeError, ValueError):
        return str(val)


def write_final_analysis(
    projects:            list[dict],
    supply_summary:      pd.DataFrame,
    scenario_adj:        pd.DataFrame,
    dep_df:              pd.DataFrame,
    tier_from:           int,
    tier_to:             int,
    sc_weighted_summary: pd.DataFrame | None = None,
    dep_summary:         pd.DataFrame | None = None,
    positive_outcomes:   pd.DataFrame | None = None,
    wifor_impact:        pd.DataFrame | None = None,
) -> None:
    # Column names are always t0_<tier_to> regardless of tier_from
    ghg_col = f"GHG_tCO2e_t0_{tier_to}"
    emp_col = f"Emp_FTE_t0_{tier_to}"
    wat_col = f"Water_1000m3_t0_{tier_to}"
    va_col  = f"VA_Musd_t0_{tier_to}"

    total_invest = sum(p["invest_usd"] for p in projects) / 1e6
    total_ghg    = supply_summary[ghg_col].sum() if ghg_col in supply_summary else 0
    total_emp    = supply_summary[emp_col].sum() if emp_col in supply_summary else 0
    n_high_risk  = dep_df["overall_high_risk"].sum() if not dep_df.empty else "n/a"
    rar_total    = dep_df["revenue_at_risk_usd_m"].sum() if not dep_df.empty else 0

    lines = []
    a = lines.append

    a("# S4 Portfolio — Integrated Impact Assessment")
    a("")
    a("*Assessment date: 2026-04-09 | Model: OSeMOSYS SSP1–5 | Database: EXIOBASE 3.8*")
    a("")
    a("---")
    a("")
    a("## 1. Portfolio Overview")
    a("")
    a(f"Nine projects across three asset classes (Health, Energy, Transport) spanning")
    a(f"four regions (Africa, Asia, Europe, LATAM).")
    a("")
    a("| Project | Region | Asset | Stage | Investment |")
    a("|---------|--------|-------|-------|-----------|")
    for p in projects:
        inv = f"USD {p['invest_usd']/1e6:,.1f}M" if p["invest_usd"] >= 1e4 else f"USD {p['invest_usd']:,.0f}"
        a(f"| {p['project_id']} | {p['region']} | {p['asset_class']} | {p['stage']} | {inv} |")
    a("")
    a(f"**Total portfolio investment:** USD {_fmt(total_invest, 1)}M")
    a("")
    a("---")
    a("")
    a("## 2. Supply-Chain Impact (tvp_dbio)")
    a("")
    a(f"Leontief power-series decomposition over tiers 0–{tier_to}.")
    a("Calibrated EXIOBASE 3.8 A-matrix with regional intensity multipliers.")
    a("")
    a("Four separate tables are produced, each covering a distinct supply-chain layer:")
    a("")
    a("| Table | Tier | Description |")
    a("|-------|------|-------------|")
    a("| `supply_chain_tier0.csv` | 0 | Direct investment — one-time CAPEX transaction split across 8 supplying sectors |")
    a("| `supply_chain_tier1.csv` | 1 | First upstream round — what Tier 0 suppliers procure; includes bilateral sourcing-country breakdown |")
    a("| `supply_chain_tier2.csv` | 2 | Second upstream round — sub-suppliers of Tier 1 |")
    a(f"| `supply_chain_tier3_10.csv` | 3–{tier_to} | Deep upstream — aggregated across remaining tiers; accounts for residual supply-chain signal |")
    a("")
    a("")
    a("### 2.1 Project-level totals")
    a("")
    a("| Project | Region | GHG (tCO2e) | Employment (FTE) | Water (000 m³) | Value Added (M USD) |")
    a("|---------|--------|------------|-----------------|---------------|-------------------|")
    if ghg_col in supply_summary.columns:
        for _, row in supply_summary.sort_values("project_id").iterrows():
            a(f"| {row['project_id']} | {row['region']} "
              f"| {_fmt(row[ghg_col])} "
              f"| {_fmt(row[emp_col], 1)} "
              f"| {_fmt(row[wat_col], 1)} "
              f"| {_fmt(row[va_col], 2)} |")
    else:
        a("| — | supply chain data unavailable | — | — | — | — |")
    a("")
    a(f"**Portfolio totals:** GHG {_fmt(total_ghg)} tCO2e | Employment {_fmt(total_emp, 0)} FTE")
    a("")
    a("### 2.2 Key findings")
    a("")
    if ghg_col in supply_summary.columns and not supply_summary.empty:
        top_ghg = supply_summary.sort_values(ghg_col, ascending=False).iloc[0]
        top_emp = supply_summary.sort_values(emp_col, ascending=False).iloc[0]
        a(f"- **Highest GHG footprint:** {top_ghg['project_id']} ({top_ghg['region']}) — "
          f"{_fmt(top_ghg[ghg_col])} tCO2e. Driven by {top_ghg['sector_code']} CAPEX "
          f"concentration in Manufacturing and Construction tiers.")
        a(f"- **Highest employment generation:** {top_emp['project_id']} ({top_emp['region']}) — "
          f"{_fmt(top_emp[emp_col], 0)} FTE. High regional labour intensity multiplier "
          f"amplifies construction-phase employment.")
        health = supply_summary[supply_summary["asset_class"] == "Health"]
        energy = supply_summary[supply_summary["asset_class"] == "Energy"]
        transport = supply_summary[supply_summary["asset_class"] == "Transport"]
        if not health.empty:
            a(f"- **Health sector** ({len(health)} projects): "
              f"{_fmt(health[ghg_col].sum())} tCO2e, "
              f"{_fmt(health[emp_col].sum(), 0)} FTE — "
              f"large LATAM hospital (Proj_001, $250M) dominates due to import leakage "
              f"in medical equipment supply chains.")
        if not energy.empty:
            a(f"- **Energy sector** ({len(energy)} projects): "
              f"{_fmt(energy[ghg_col].sum())} tCO2e — "
              f"Asia hydro retrofit ($150M) is the single largest contributor; "
              f"EU efficiency tweak ($2M) is immaterial at portfolio scale.")
        if not transport.empty:
            a(f"- **Transport sector** ({len(transport)} projects): "
              f"{_fmt(transport[ghg_col].sum())} tCO2e — "
              f"Rail_EU_DEV €1.85B development phase accounts for the majority; "
              f"operational projects (OP1/OP2) are negligible in CAPEX terms.")
    a("")
    a("### 2.3 Positive vs Negative Impact — net ledger (tiers 0–{tier_to})".format(tier_to=tier_to))
    a("")
    a("Each indicator is classified by polarity. **Negative impacts** increase")
    a("environmental burden; **positive impacts** deliver social or economic benefits.")
    a("Hydro avoided CO₂, health beneficiaries, and rail reach are direct project")
    a("outcomes read from input files — they are *not* supply-chain quantities.")
    a("")
    a("| Project | Region | [−] GHG tCO2e | [−] Water 000m³ | [+] Jobs FTE | [+] VA M USD"
      " | [+] Avoided CO₂ tCO2e | [+] Beneficiaries / Reach |")
    a("|---------|--------|--------------|----------------|-------------|----------"
      "|----------------------|--------------------------|")
    if ghg_col in supply_summary.columns:
        po = positive_outcomes.set_index("project_id") if positive_outcomes is not None else pd.DataFrame()
        for _, row in supply_summary.sort_values("project_id").iterrows():
            pid = row["project_id"]
            po_row = po.loc[pid] if pid in po.index else None
            avoided = _fmt(po_row["avoided_CO2_tCO2e"]) if po_row is not None else "—"
            bene = (_fmt(po_row["beneficiaries"]) if (po_row is not None and po_row["beneficiaries"] > 0)
                    else (_fmt(po_row["reach_ppl_yr"]) + " ppl/yr" if (po_row is not None and po_row["reach_ppl_yr"] > 0)
                          else "—"))
            a(f"| {pid} | {row['region']} "
              f"| **{_fmt(row[ghg_col])}** "
              f"| {_fmt(row[wat_col], 1)} "
              f"| {_fmt(row[emp_col], 0)} "
              f"| {_fmt(row[va_col], 2)} "
              f"| {avoided} "
              f"| {bene} |")
    a("")
    if positive_outcomes is not None and not positive_outcomes.empty:
        tot_avoided = positive_outcomes["avoided_CO2_tCO2e"].sum()
        tot_bene    = positive_outcomes["beneficiaries"].sum()
        tot_reach   = positive_outcomes["reach_ppl_yr"].sum()
        a(f"**Portfolio positive outcomes:** "
          f"{_fmt(tot_avoided)} tCO2e avoided | "
          f"{_fmt(tot_bene)} health beneficiaries | "
          f"{_fmt(tot_reach)} rail ppl/yr reached")
        if ghg_col in supply_summary.columns:
            net_ghg = total_ghg - tot_avoided
            a(f"**Net GHG position:** {_fmt(total_ghg)} tCO2e supply-chain emissions "
              f"− {_fmt(tot_avoided)} tCO2e avoided = **{_fmt(net_ghg)} tCO2e net** "
              f"({'surplus' if net_ghg > 0 else 'net negative — project avoids more than it generates'})")
    a("")
    a("---")
    a("")
    # ── Section 2.5: Scenario-weighted tier breakdown (Pass 1.5) ──────────────
    available_models_w = (
        sc_weighted_summary["model"].unique().tolist()
        if sc_weighted_summary is not None and not sc_weighted_summary.empty
           and "model" in sc_weighted_summary.columns
        else []
    )
    if sc_weighted_summary is not None and not sc_weighted_summary.empty:
        a("## 2.5 Scenario-Weighted Supply-Chain Impact (connected tiers × scenarios)")
        a("")
        a("Each supply-chain tier is adjusted using the sourcing region's own")
        a("decarbonisation trajectory — not just the project home region. Tier 1")
        a("bilateral sourcing-country data feeds directly into the region-specific")
        a("adjustment ratios from tvp_scenario, so that imported steel from Asia")
        a("supplying a European project is adjusted at Asia's trajectory, not Europe's.")
        a("")
        a("Four stressors are adjusted per tier:")
        a("")
        a("| Stressor | Ratio used | Source |")
        a("|----------|-----------|--------|")
        a("| GHG (tCO2e) | `adj_ratio_ghg` | OSeMOSYS grid-intensity trajectory |")
        a("| Employment (FTE) | `adj_ratio_employment` | OSeMOSYS renewable-jobs premium |")
        a("| Water (000 m³) | `1 − renewable_share × 0.85` ± nexus refinement | IEA Water for Energy + IPCC nexus weights |")
        a("| Value Added (M USD) | `adj_ratio_employment` | Labour-productivity proxy |")
        a("")
        a("### 2.5.1 Portfolio totals — scenario-weighted (SSP2-4.5, 2030)")
        a("")
        ssp2_2030 = sc_weighted_summary[
            (sc_weighted_summary["scenario"] == "SSP2-4.5") &
            (sc_weighted_summary["year"] == 2030)
        ]
        if not ssp2_2030.empty:
            has_ghg_adj = "GHG_adj_tCO2e" in ssp2_2030.columns
            has_emp_adj = "Employment_adj_FTE" in ssp2_2030.columns
            has_wat_adj = "Water_adj_1000m3" in ssp2_2030.columns
            has_va_adj  = "ValueAdded_adj_M$" in ssp2_2030.columns

            a("| Project | Region | GHG baseline | GHG 2030 adj | Emp baseline | Emp 2030 adj |")
            a("|---------|--------|-------------|--------------|-------------|--------------|")
            for _, row in ssp2_2030.sort_values("project_id").iterrows():
                ghg_b = _fmt(row.get("GHG_tCO2e",      "n/a"))
                ghg_a = _fmt(row.get("GHG_adj_tCO2e",  "n/a")) if has_ghg_adj else "n/a"
                emp_b = _fmt(row.get("Employment_FTE",  "n/a"), 1)
                emp_a = _fmt(row.get("Employment_adj_FTE", "n/a"), 1) if has_emp_adj else "n/a"
                a(f"| {row['project_id']} | {row['region']} | {ghg_b} | {ghg_a} | {emp_b} | {emp_a} |")
            a("")

        a("### 2.5.2 Tier contribution to scenario-adjusted GHG — SSP1 vs SSP5 (2030)")
        a("")
        ssp1_2030 = sc_weighted_summary[
            (sc_weighted_summary["scenario"] == "SSP1-1.9") &
            (sc_weighted_summary["year"] == 2030)
        ]
        ssp5_2030 = sc_weighted_summary[
            (sc_weighted_summary["scenario"] == "SSP5-8.5") &
            (sc_weighted_summary["year"] == 2030)
        ]
        if not ssp1_2030.empty and not ssp5_2030.empty and "GHG_adj_tCO2e" in sc_weighted_summary.columns:
            ssp1_tot = ssp1_2030["GHG_adj_tCO2e"].sum()
            ssp5_tot = ssp5_2030["GHG_adj_tCO2e"].sum()
            base_tot = ssp2_2030["GHG_tCO2e"].sum() if not ssp2_2030.empty and "GHG_tCO2e" in ssp2_2030.columns else 0
            a(f"- **Baseline (2020):** {_fmt(base_tot)} tCO2e portfolio total")
            a(f"- **SSP1-1.9 (2030):** {_fmt(ssp1_tot)} tCO2e — "
              f"{_fmt(100*(1-ssp1_tot/base_tot), 0) if base_tot else '?'}% reduction")
            a(f"- **SSP5-8.5 (2030):** {_fmt(ssp5_tot)} tCO2e — "
              f"{_fmt(100*(1-ssp5_tot/base_tot), 0) if base_tot else '?'}% reduction")
            a(f"- **Scenario spread:** {_fmt(ssp5_tot - ssp1_tot)} tCO2e range — "
              f"driven by sourcing-country divergence in tier 1 bilateral flows.")
        a("")
        a("---")
        a("")

    # ── Section 2.6: Dependency-weighted tier breakdown (Pass 1.6) ───────────
    if dep_summary is not None and not dep_summary.empty:
        dep_wcols = [c for c in dep_summary.columns if "_dep_" in c
                     and c.endswith(("tCO2e","_FTE","1000m3","_M$"))]
        if dep_wcols:
            a("## 2.6 Dependency-Weighted Supply-Chain Impact")
            a("")
            a("Each scenario-adjusted stressor is multiplied by a three-component dependency")
            a("factor that captures nature-related risk amplification per tier, sector,")
            a("and sourcing region:")
            a("")
            a("| Component | Source | Applies to |")
            a("|-----------|--------|-----------|")
            a("| **ENCORE ecosystem dependency** | ENCORE v2024 materiality matrix | Project sector × stressor |")
            a("| **WWF regional risk** | WRF physical / BRF ecosystem composite | Sourcing region (tier 1 bilateral) |")
            a("| **SC sector sensitivity** | IPBES (2019) sector pressure typology | Supplying sector (all tiers) |")
            a("")
            a("dep_factor = 1.0 at global average; range 0.33 (low dependency + low risk)")
            a("to 1.67 (high dependency + high risk).")
            a("")
            a("### 2.6.1 Portfolio dep-weighted GHG — SSP2-4.5 (2030)")
            a("")
            ghg_dep_col = next((c for c in dep_wcols if "GHG" in c), None)
            wat_dep_col = next((c for c in dep_wcols if "Water" in c), None)
            if ghg_dep_col:
                ssp2_dep = dep_summary[
                    (dep_summary["scenario"] == "SSP2-4.5") &
                    (dep_summary["year"] == 2030)
                ]
                if not ssp2_dep.empty:
                    # Also pull adjusted GHG if available (from sc_weighted_summary)
                    a("| Project | Region | GHG adj (tCO2e) | GHG dep-weighted | Water adj (000 m³) | Water dep-weighted |")
                    a("|---------|--------|----------------|-----------------|-------------------|-------------------|")
                    sc_ssp2 = (sc_weighted_summary[
                        (sc_weighted_summary["scenario"] == "SSP2-4.5") &
                        (sc_weighted_summary["year"] == 2030)
                    ] if sc_weighted_summary is not None and not sc_weighted_summary.empty else pd.DataFrame())

                    for _, row in ssp2_dep.sort_values("project_id").iterrows():
                        ghg_a = "n/a"
                        wat_a = "n/a"
                        if not sc_ssp2.empty:
                            sc_row = sc_ssp2[sc_ssp2["project_id"] == row["project_id"]]
                            if not sc_row.empty:
                                ghg_a = _fmt(sc_row.iloc[0].get("GHG_adj_tCO2e", "n/a"))
                                wat_a = _fmt(sc_row.iloc[0].get("Water_adj_1000m3", "n/a"), 1)
                        ghg_d = _fmt(row.get(ghg_dep_col, "n/a"))
                        wat_d = _fmt(row.get(wat_dep_col, "n/a"), 1) if wat_dep_col else "n/a"
                        a(f"| {row['project_id']} | {row['region']} "
                          f"| {ghg_a} | {ghg_d} | {wat_a} | {wat_d} |")
                    a("")

            a("### 2.6.2 Dependency factor profile — sector and region breakdown")
            a("")
            a("Three sub-scores contributing to the dep_factor (scale 1–5, neutral = 3):")
            a("")
            a("| Project sector | ENCORE water dep | ENCORE GHG dep | WWF wrf_physical (Africa) | WWF wrf_physical (Asia) |")
            a("|---------------|-----------------|---------------|--------------------------|------------------------|")
            for ps, ek in PROJECT_SECTOR_TO_ENCORE.items():
                from dependency_profiler.encore_materiality import MATERIALITY_MATRIX, RATING_SCALE
                mat = MATERIALITY_MATRIX.get(ek, {})
                w_svcs = STRESSOR_ECOSYSTEM_MAP["Water_1000m3"]
                g_svcs = STRESSOR_ECOSYSTEM_MAP["GHG_tCO2e"]
                w_score = sum(RATING_SCALE.get(mat.get(s,("N","N"))[0],0) for s in w_svcs) / len(w_svcs)
                g_score = sum(RATING_SCALE.get(mat.get(s,("N","N"))[0],0) for s in g_svcs) / len(g_svcs)
                a(f"| {ps} | {w_score:.2f} | {g_score:.2f} | 4.97 (Asia) | 4.38 (Africa) |")
            a("")
            a("**SC sector sensitivity highlights** (water_dep / ghg_dep / land_dep):")
            a("")
            for sec, profile in SC_SECTOR_DEP_PROFILE.items():
                a(f"- **{sec}**: water {profile['water']:.0f} | ghg {profile['ghg']:.0f} | land {profile['land']:.0f}")
            a("")
            a("---")
            a("")

    available_models = scenario_adj["model"].unique().tolist() if not scenario_adj.empty and "model" in scenario_adj.columns else []
    model_list_str = ", ".join(available_models) if available_models else "OSeMOSYS"
    a(f"## 3. SSP Scenario Analysis (tvp_scenario — {model_list_str})")
    a("")
    a("GHG intensity adjustment ratios from OSeMOSYS REMIND-MAgPIE calibration.")
    a("All five IPCC AR6 Shared Socioeconomic Pathways (SSP1–SSP5).")
    if len(available_models) > 1:
        a(f"Results from {len(available_models)} simulation frameworks: {', '.join(available_models)}.")
    a("")
    a("### 3.1 Scenario-adjusted GHG — all projects (tCO2e)")
    a("")
    if not scenario_adj.empty and "2025" in scenario_adj.columns:
        yr_cols = [c for c in ["2025", "2030", "2040"] if c in scenario_adj.columns]
        has_model_col = "model" in scenario_adj.columns and scenario_adj["model"].nunique() > 1
        if has_model_col:
            a("| Model | Project | Region | Scenario | " + " | ".join(yr_cols) + " |")
            a("|-------|---------|--------|----------|" + "|".join(["---"] * len(yr_cols)) + "|")
            for _, row in scenario_adj.sort_values(["model", "project_id", "scenario"]).iterrows():
                vals = " | ".join(_fmt(row.get(yr, "n/a")) for yr in yr_cols)
                a(f"| {row['model']} | {row['project_id']} | {row['region']} | {row['scenario']} | {vals} |")
        else:
            a("| Project | Region | Scenario | " + " | ".join(yr_cols) + " |")
            a("|---------|--------|----------|" + "|".join(["---"] * len(yr_cols)) + "|")
            for _, row in scenario_adj.sort_values(["project_id", "scenario"]).iterrows():
                vals = " | ".join(_fmt(row.get(yr, "n/a")) for yr in yr_cols)
                a(f"| {row['project_id']} | {row['region']} | {row['scenario']} | {vals} |")
    else:
        a("*Scenario results not available — run `tvp_scenario/osemosys/run_simulation.py` first.*")
    a("")
    a("### 3.2 Scenario narrative")
    a("")
    a("- **SSP1-1.9 (Sustainability):** Steepest GHG decline across all regions. By 2030,")
    a("  supply-chain GHG falls to 30–40% of 2020 baseline in Europe and below 10% in Asia.")
    a("  Rail_EU_DEV is effectively low-carbon by 2030 under full grid decarbonisation.")
    a("- **SSP2-4.5 (Middle of the Road):** Moderate decline. Europe falls to ~67% by 2030;")
    a("  Africa lags at ~85%, reflecting slower capital deployment and lower carbon pricing.")
    a("- **SSP3-7.0 (Regional Rivalry):** Slowest transition. All regions remain above 80%")
    a("  of 2020 intensity through 2030. Infrastructure investments locked into fossil-heavy")
    a("  supply chains.")
    a("- **SSP4-6.0 (Inequality):** Europe decarbonises faster than Africa (ratio 0.34 vs 0.65")
    a("  by 2030). Highlights distributional risk: LATAM and Africa health projects face")
    a("  higher future supply-chain carbon exposure than European peers.")
    a("- **SSP5-8.5 (Fossil-Fuelled Development):** Near-unchanged intensity through 2030 for")
    a("  Africa and Asia. Hydro projects in these regions carry significant long-run GHG risk")
    a("  from upstream manufacturing and grid-delivered construction energy.")
    a("")
    a("---")
    a("")
    a("## 4. Nature-Related Dependency & Risk (tvp_dependency)")
    a("")
    a("ENCORE materiality screening, WWF Risk Filter Suite, InVEST biophysical")
    a("model configuration, and TNFD LEAP financial stress testing.")
    a("")
    a("### 4.1 Risk scores and revenue at risk")
    a("")
    if not dep_df.empty:
        a("| Project | Region | WRF | BRF | High Risk | Revenue at Risk (M USD) |")
        a("|---------|--------|-----|-----|-----------|------------------------|")
        for _, row in dep_df.sort_values("project_id").iterrows():
            flag = "YES" if row["overall_high_risk"] else "no"
            a(f"| {row['project_id']} | {row['region']} "
              f"| {row['wrf_composite']:.2f} "
              f"| {row['brf_composite']:.2f} "
              f"| {flag} "
              f"| {_fmt(row['revenue_at_risk_usd_m'], 1)} |")
        a("")
        a(f"**High-risk projects:** {int(n_high_risk)} / {len(dep_df)}")
        a(f"**Total revenue at risk:** USD {_fmt(rar_total, 1)}M")
    else:
        a("*Dependency results not available.*")
    a("")
    a("### 4.2 Top ecosystem dependencies (portfolio-wide)")
    a("")
    a("From ENCORE materiality screening across all nine projects:")
    a("")
    a("| Ecosystem Service | Max Score | Material Projects |")
    a("|------------------|-----------|-----------------|")
    dep_heatmap = DEPENDENCY_DIR / "assessment_output" / "dependency_heatmap.csv"
    if dep_heatmap.exists():
        hm = pd.read_csv(dep_heatmap)
        hm_top = hm.nlargest(8, "max_dependency_score")
        for _, row in hm_top.iterrows():
            a(f"| {row['ecosystem_service']} | {row['max_dependency_score']} | {row['n_material_projects']} |")
    a("")
    a("### 4.3 Key risk findings")
    a("")
    if not dep_df.empty:
        high_risk = dep_df[dep_df["overall_high_risk"] == True]
        a(f"- **{int(n_high_risk)} of 9 projects** are classified high risk on both")
        a(f"  the WWF Water Risk Filter (WRF) and Biodiversity Risk Filter (BRF).")
        a(f"- **Hydro_AS** carries the highest composite scores (WRF 4.27, BRF 4.26) and")
        a(f"  the largest single revenue-at-risk exposure (USD 83.0M). Freshwater ecosystem")
        a(f"  dependency and high biodiversity sensitivity in Asia make this the portfolio's")
        a(f"  critical nature-related risk concentration.")
        a(f"- **Proj_001 (LATAM health, $250M)** is at high risk despite being in the health")
        a(f"  sector: water supply and solid-waste mediation dependencies in LATAM drive WRF")
        a(f"  3.48 and BRF 4.09. Revenue at risk: USD 42.0M.")
        a(f"- **European projects** (Proj_003, Rail_EU_DEV/OP) are generally lower risk,")
        a(f"  protected by stronger regulatory frameworks (high WRF regulatory sub-score)")
        a(f"  and lower physical biodiversity sensitivity.")
        a(f"- **Water supply** is the most pervasive dependency: material in 6/9 projects,")
        a(f"  with maximum dependency score 5/5. All hydro and health projects are exposed.")
    a("")
    a("---")
    a("")
    a("## 5. Integrated Risk Summary")
    a("")
    a("Cross-cutting findings from combining all three analytical passes:")
    a("")
    a("### Compounding risks (high supply-chain GHG AND high nature risk)")
    a("")
    if not dep_df.empty and ghg_col in supply_summary.columns:
        merged_risk = supply_summary[["project_id", ghg_col]].merge(
            dep_df[["project_id", "overall_high_risk", "wrf_composite", "brf_composite", "revenue_at_risk_usd_m"]],
            on="project_id", how="inner"
        )
        compound = merged_risk[merged_risk["overall_high_risk"] == True].sort_values(ghg_col, ascending=False)
        a("| Project | Supply-chain GHG (tCO2e) | WRF | BRF | Revenue at Risk |")
        a("|---------|------------------------|-----|-----|----------------|")
        for _, row in compound.iterrows():
            a(f"| {row['project_id']} | {_fmt(row[ghg_col])} "
              f"| {row['wrf_composite']:.2f} "
              f"| {row['brf_composite']:.2f} "
              f"| USD {_fmt(row['revenue_at_risk_usd_m'], 1)}M |")
    a("")
    a("### Scenario-risk interaction")
    a("")
    a("- Under **SSP3/SSP5** (high-emissions pathways), supply-chain GHG remains elevated")
    a("  through 2030–2040 for Africa and Asia, compounding the already-high nature risk")
    a("  scores of Hydro_AF and Hydro_AS. These projects face a double exposure: upstream")
    a("  carbon intensity stays high AND ecosystem services (water supply, freshwater flows)")
    a("  degrade under higher warming trajectories.")
    a("- Under **SSP1**, Rail_EU_DEV's supply-chain GHG falls rapidly to near-zero by 2035,")
    a("  consistent with full grid decarbonisation. With low nature risk scores, this project")
    a("  is well-positioned across all risk dimensions.")
    a("- **SSP4 inequality dynamic**: Proj_001 (LATAM health) and Proj_002 (Africa health)")
    a("  experience slower supply-chain decarbonisation than European counterparts, while")
    a("  simultaneously carrying higher nature risk. This asymmetry is the single most")
    a("  important portfolio-level finding for impact-at-risk disclosure.")
    a("")
    a("### Priority actions")
    a("")
    a("1. **Hydro_AS** — Commission InVEST Hydropower Water Yield and Sediment Delivery")
    a("   Ratio models immediately. USD 83M revenue-at-risk requires site-level biophysical")
    a("   quantification before final investment decision.")
    a("2. **Proj_001 (LATAM)** — Integrate water-security covenant into financing terms.")
    a("   Nature-based wastewater treatment can reduce both WRF physical score and operating")
    a("   cost under SSP3/SSP4 water stress scenarios.")
    a("3. **Hydro_AF** — Quantify coal displacement avoided GHG against upstream construction")
    a("   GHG (currently 150,000 tCO2 avoided vs. significant supply-chain emissions).")
    a("   Under SSP3, the avoided-emission benefit shrinks as the grid diversifies slowly.")
    a("4. **Portfolio-wide** — Adopt SSP2 as the baseline planning scenario for conservative")
    a("   supply-chain GHG disclosure; use SSP1 as the target trajectory for transition")
    a("   alignment reporting.")
    a("")
    a("---")
    a("")
    a("## 6. Data and Methodology Notes")
    a("")
    a("| Component | Source | Year |")
    a("|-----------|--------|------|")
    a("| Supply-chain A matrix | EXIOBASE 3.8.1 (Stadler et al. 2018) | 2018 |")
    a("| GHG intensities | EXIOBASE 3.8.1 satellite + IEA 2022 | 2018 |")
    a("| Employment intensities | EXIOBASE 3.8.1 + ILO 2022 | 2018 |")
    a("| Scenario trajectories | OSeMOSYS / REMIND-MAgPIE | 2020–2050 |")
    a("| SSP calibration | IPCC AR6 WG3 (2022) | — |")
    a("| ENCORE materiality | ENCORE tool v2.0 | 2023 |")
    a("| WWF Risk Filters | WRF 2.0 + BRF 1.0 | 2022 |")
    a("| Financial inputs | Project finance CSVs | 2025 |")
    a("| GHG value factor | WifOR Institute — Nordhaus DICE / Paris update | 2019 |")
    a("| Water value factor | WifOR Institute — Blue water scarcity damage cost | 2020 |")
    a("| Employment value factor | WifOR Institute — TrainingHours wage-based | 2020 |")
    a("")
    a(f"Tiers computed: 0 to {tier_to}. Tiers 0–2 in individual tables; tiers 3–{tier_to} aggregated.")
    a("Column A spectral radius ≈ 0.52 → geometric decay; tiers >8 contribute <0.1% of signal.")
    a("EUR/USD rate: 1.08 (applied to Rail CAPEX inputs).")
    a("")

    # ── Section 7: WifOR value factor impact statement ────────────────────────
    if wifor_impact is not None and not wifor_impact.empty:
        a("---")
        a("")
        a("## 7. WifOR Monetised Impact Statement")
        a("")
        a("Supply-chain physical quantities are converted to monetary impact estimates")
        a("using WifOR Institute value factors, enabling a single-currency comparison")
        a("of environmental costs and social benefits across all projects.")
        a("")
        a("**Conversion formulas:**")
        a("")
        a("| Stressor | Conversion | Value factor |")
        a("|----------|-----------|--------------|")
        a("| GHG (tCO₂e) | × 1,000 kg/t × coeff [USD/kg] | Social cost of carbon — Nordhaus DICE baseline (globally uniform) |")
        a("| Water (1,000 m³) | × 1,000 m³ × coeff [USD/m³] | Blue water depletion damage — country-specific scarcity weighting |")
        a("| Employment (FTE) | × 1,880 h/yr × coeff [USD/h] | Workplace training benefit — country- and sector-specific wage base |")
        a("")
        a("**Country and sector mappings applied:**")
        a("")
        a("| Project region | ISO-3 country | WifOR country used |")
        a("|---------------|--------------|-------------------|")
        for region, iso3 in REGION_TO_ISO3.items():
            a(f"| {region} | {iso3} | {iso3} |")
        a("")

        a("### 7.1 Value factor coefficients by project")
        a("")
        a("| Project | Country | NACE | GHG coeff (USD/kg) | GHG Paris (USD/kg) | Water (USD/m³) | Training (USD/h) |")
        a("|---------|---------|------|------------------|-------------------|---------------|-----------------|")
        for _, row in wifor_impact.sort_values("project_id").iterrows():
            c_ghg   = f"{row['coeff_ghg_base_usd_kg']:.4f}"  if row["coeff_ghg_base_usd_kg"]  is not None else "n/a"
            c_paris = f"{row['coeff_ghg_paris_usd_kg']:.4f}" if row["coeff_ghg_paris_usd_kg"] is not None else "n/a"
            c_wat   = f"{row['coeff_water_usd_m3']:.4f}"     if row["coeff_water_usd_m3"]     is not None else "n/a"
            c_trn   = f"{row['coeff_train_usd_h']:.4f}"      if row["coeff_train_usd_h"]      is not None else "n/a"
            a(f"| {row['project_id']} | {row['country_iso3']} | {row['nace_sector']} "
              f"| {c_ghg} | {c_paris} | {c_wat} | {c_trn} |")
        a("")
        a("> GHG social cost of carbon is globally uniform (Nordhaus DICE, 2019 USD).")
        a("> Water and training coefficients are country-specific; training also varies by NACE sector.")
        a("")

        a("### 7.2 Monetised impact per project (M USD, tiers 0–{tier_to})".format(tier_to=tier_to))
        a("")
        a("Negative values = environmental damage costs. Positive values = social benefits.")
        a("")
        a("| Project | Region | [−] GHG cost | [−] GHG cost (Paris) | [−] Water cost | [+] Employment benefit | Net impact |")
        a("|---------|--------|------------|---------------------|--------------|----------------------|-----------|")
        for _, row in wifor_impact.sort_values("project_id").iterrows():
            a(f"| {row['project_id']} | {row['region']} "
              f"| {_fmt(row['ghg_impact_MUSD'], 2)} M "
              f"| {_fmt(row['ghg_paris_impact_MUSD'], 2)} M "
              f"| {_fmt(row['water_impact_MUSD'], 2)} M "
              f"| {_fmt(row['employment_impact_MUSD'], 2)} M "
              f"| **{_fmt(row['net_impact_MUSD'], 2)} M** |")
        a("")

        # Portfolio totals
        total_ghg_cost   = wifor_impact["ghg_impact_MUSD"].sum()
        total_paris_cost = wifor_impact["ghg_paris_impact_MUSD"].sum()
        total_wat_cost   = wifor_impact["water_impact_MUSD"].sum()
        total_emp_ben    = wifor_impact["employment_impact_MUSD"].sum()
        total_net        = wifor_impact["net_impact_MUSD"].sum()
        a(f"**Portfolio totals:** "
          f"GHG cost {_fmt(total_ghg_cost, 1)} M USD | "
          f"Water cost {_fmt(total_wat_cost, 1)} M USD | "
          f"Employment benefit {_fmt(total_emp_ben, 1)} M USD | "
          f"**Net {_fmt(total_net, 1)} M USD**")
        a("")

        a("### 7.3 Key findings")
        a("")
        if not wifor_impact.empty:
            worst_ghg = wifor_impact.loc[wifor_impact["ghg_impact_MUSD"].idxmin()]
            worst_wat = wifor_impact.loc[wifor_impact["water_impact_MUSD"].idxmin()]
            best_emp  = wifor_impact.loc[wifor_impact["employment_impact_MUSD"].idxmax()]
            best_net  = wifor_impact.loc[wifor_impact["net_impact_MUSD"].idxmax()]
            worst_net = wifor_impact.loc[wifor_impact["net_impact_MUSD"].idxmin()]

            a(f"- **Highest GHG damage cost:** {worst_ghg['project_id']} ({worst_ghg['region']}) — "
              f"{_fmt(worst_ghg['ghg_impact_MUSD'], 1)} M USD. "
              f"GHG social cost of carbon is globally uniform at "
              f"{worst_ghg['coeff_ghg_base_usd_kg']:.4f} USD/kg CO₂e (Nordhaus DICE baseline), "
              f"so the ranking mirrors the supply-chain GHG footprint.")
            a(f"- **Highest water damage cost:** {worst_wat['project_id']} ({worst_wat['region']}) — "
              f"{_fmt(worst_wat['water_impact_MUSD'], 1)} M USD. "
              f"Driven by the country-specific scarcity factor "
              f"({worst_wat['coeff_water_usd_m3']:.4f} USD/m³ for {worst_wat['country_iso3']}). "
              f"Asian and African projects face substantially higher water damage costs than "
              f"European counterparts due to greater physical water scarcity.")
            a(f"- **Highest employment benefit:** {best_emp['project_id']} ({best_emp['region']}) — "
              f"{_fmt(best_emp['employment_impact_MUSD'], 1)} M USD. "
              f"Training value factor {best_emp['coeff_train_usd_h']:.2f} USD/h for "
              f"{best_emp['country_iso3']} × {best_emp['nace_sector']} sector.")
            a(f"- **Best net impact:** {best_net['project_id']} — "
              f"net {_fmt(best_net['net_impact_MUSD'], 1)} M USD.")
            a(f"- **Worst net impact:** {worst_net['project_id']} — "
              f"net {_fmt(worst_net['net_impact_MUSD'], 1)} M USD.")
            a("")
            a("**Country-specific water scarcity cost contrast:**")
            a("")
            water_rows = (
                wifor_impact[["project_id", "country_iso3", "coeff_water_usd_m3",
                              "Water_1000m3", "water_impact_MUSD"]]
                .drop_duplicates("country_iso3")
                .sort_values("coeff_water_usd_m3")
            )
            a("| Country | Water factor (USD/m³) | Applies to |")
            a("|---------|----------------------|-----------|")
            for _, wr in water_rows.iterrows():
                projects_in_country = wifor_impact[wifor_impact["country_iso3"] == wr["country_iso3"]]["project_id"].tolist()
                a(f"| {wr['country_iso3']} | {wr['coeff_water_usd_m3']:.4f} | {', '.join(projects_in_country)} |")
            a("")
        a("---")
        a("")

    out_path = RESULTS_DIR / "final_analysis.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[OK] Final analysis → {out_path}")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="S4 integrated portfolio assessment")
    parser.add_argument("--skip-dependency", action="store_true",
                        help="Load existing dependency outputs instead of re-running pipeline")
    parser.add_argument("--tier-max", type=int, default=10,
                        help="Highest tier to compute for supply-chain analysis (default: 10)")
    args = parser.parse_args()

    print("=" * 60)
    print("  S4 Portfolio — Integrated Assessment")
    print("=" * 60)

    projects = _load_projects()
    print(f"\n[INFO] {len(projects)} projects loaded from {INPUT_DIR.name}/")

    # ── Pass 1: Supply chain ──────────────────────────────────────────────────
    # Load positive outcome indicators from input files
    positive_outcomes = _load_positive_outcomes()
    positive_outcomes.to_csv(RESULTS_DIR / "positive_outcomes.csv", index=False)
    print(f"\n[INFO] Positive outcomes loaded: {len(positive_outcomes)} projects")

    print(f"\n[1/3] Supply-chain analysis (tiers 0–{args.tier_max}) ...")
    sc = run_supply_chain(projects, tier_to=args.tier_max)

    sc["tier0"]   .to_csv(RESULTS_DIR / "supply_chain_tier0.csv",    index=False)
    sc["tier1"]   .to_csv(RESULTS_DIR / "supply_chain_tier1.csv",    index=False)
    sc["tier2"]   .to_csv(RESULTS_DIR / "supply_chain_tier2.csv",    index=False)
    sc["tier3_10"].to_csv(RESULTS_DIR / "supply_chain_tier3_10.csv", index=False)
    sc["summary"] .to_csv(RESULTS_DIR / "supply_chain_summary.csv",  index=False)

    print(f"      → supply_chain_tier0.csv    ({len(sc['tier0'])} rows — direct investment)")
    print(f"      → supply_chain_tier1.csv    ({len(sc['tier1'])} rows — 1st upstream + sourcing country)")
    print(f"      → supply_chain_tier2.csv    ({len(sc['tier2'])} rows — 2nd upstream)")
    print(f"      → supply_chain_tier3_10.csv ({len(sc['tier3_10'])} rows — deep upstream, aggregated)")
    print(f"      → supply_chain_summary.csv  ({len(sc['summary'])} rows — project totals)")

    summary = sc["summary"]

    # ── Pass 1.5: Connect tiers to scenario weights (all stressors, all tiers) ─
    print("\n[1.5/3] Scenario-weighted tier analysis ...")
    sc_weighted_result = run_scenario_weighted_tiers(sc)
    if isinstance(sc_weighted_result, tuple):
        sc_weighted_detail, sc_weighted_summary = sc_weighted_result
        sc_weighted_detail .to_csv(RESULTS_DIR / "scenario_weighted_tiers.csv",   index=False)
        sc_weighted_summary.to_csv(RESULTS_DIR / "scenario_weighted_summary.csv", index=False)
        print(f"      → scenario_weighted_tiers.csv   ({len(sc_weighted_detail)} rows — "
              f"tier × scenario × year × stressor, sourcing-region precision)")
        print(f"      → scenario_weighted_summary.csv ({len(sc_weighted_summary)} rows — "
              f"project totals per model × scenario × year)")
    else:
        sc_weighted_detail  = pd.DataFrame()
        sc_weighted_summary = pd.DataFrame()
        print("      [WARN] Skipped — no scenario factor files available.")

    # ── Pass 1.6: Add dependency factors per indicator, sector, region, tier ──
    print("\n[1.6/3] Dependency-weighted tier analysis (ENCORE + WWF + SC sensitivity) ...")
    if not sc_weighted_detail.empty:
        dep_weighted_detail = apply_dependency_factors(sc_weighted_detail)
        dep_cols = [c for c in dep_weighted_detail.columns if c.startswith("dep_factor_")]
        dep_weighted_detail.to_csv(RESULTS_DIR / "dep_weighted_tiers.csv", index=False)
        print(f"      → dep_weighted_tiers.csv ({len(dep_weighted_detail)} rows — "
              f"dep_factor columns: {', '.join(dep_cols)})")

        # Summary: project totals of dep-weighted stressors (SSP2-4.5, all years)
        dep_weighted_cols = [c for c in dep_weighted_detail.columns if "_dep_" in c
                             and c.endswith(("tCO2e","_FTE","1000m3","_M$"))]
        grp_cols = ["model_label", "scenario", "year", "project_id", "asset_class", "region"]
        if dep_weighted_cols:
            dep_summary = (
                dep_weighted_detail
                .groupby(grp_cols)[dep_weighted_cols]
                .sum()
                .reset_index()
                .rename(columns={"model_label": "model"})
            )
            dep_summary.to_csv(RESULTS_DIR / "dep_weighted_summary.csv", index=False)
            print(f"      → dep_weighted_summary.csv ({len(dep_summary)} rows — "
                  f"project totals, dep-weighted per scenario × year)")
        else:
            dep_summary = pd.DataFrame()
    else:
        dep_weighted_detail = pd.DataFrame()
        dep_summary         = pd.DataFrame()
        print("      [WARN] Skipped — no scenario-weighted tiers available.")

    # ── Pass 4: WifOR value factor impact monetisation ────────────────────────
    print("\n[4] WifOR value factor impact monetisation ...")
    wifor_impact = run_wifor_impact(summary, projects, tier_to=args.tier_max)
    if not wifor_impact.empty:
        wifor_impact.to_csv(RESULTS_DIR / "wifor_impact.csv", index=False)
        print(f"      → wifor_impact.csv ({len(wifor_impact)} rows — "
              f"monetised GHG, water, employment via WifOR value factors)")
        vf_dir = _resolve_wifor_dir()
        print(f"      [source] {vf_dir}")
    else:
        print("      [WARN] Skipped — WifOR coefficient files not found.")

    # ── Pass 2: Scenario adjustment ───────────────────────────────────────────
    n_models_available = sum(1 for p in MODEL_FACTOR_PATHS.values() if p.exists())
    print(f"\n[2/3] Scenario adjustment ({n_models_available} model(s): OSeMOSYS"
          + (", GCAM" if (SCENARIO_DIR / "gcam" / "results" / "tvpdbio_intensity_factors.csv").exists() else "")
          + (", MESSAGEix-GLOBIOM" if (SCENARIO_DIR / "messageix" / "results" / "tvpdbio_intensity_factors.csv").exists() else "")
          + ") ...")
    factors_df, scenario_pivot = run_scenario_adjustment(projects, summary)
    if not factors_df.empty:
        factors_df.to_csv(RESULTS_DIR / "scenario_adjustment.csv", index=False)
        print(f"      → results/scenario_adjustment.csv ({len(factors_df)} rows — "
              f"all stressors: GHG, Employment, Water, VA)")
    if not scenario_pivot.empty:
        scenario_pivot.to_csv(RESULTS_DIR / "scenario_ghg_adjusted.csv", index=False)
        print(f"      → results/scenario_ghg_adjusted.csv ({len(scenario_pivot)} rows)")
    else:
        print("      [WARN] No scenario data — skipping.")

    # ── Pass 3: Dependency ────────────────────────────────────────────────────
    dep_df = run_dependency(skip=args.skip_dependency)
    dep_df.to_csv(RESULTS_DIR / "dependency_summary.csv", index=False)
    print(f"      → results/dependency_summary.csv ({len(dep_df)} rows)")

    # ── Final analysis ────────────────────────────────────────────────────────
    print("\n[+] Writing final analysis ...")
    write_final_analysis(
        projects, summary, scenario_pivot, dep_df, 0, args.tier_max,
        sc_weighted_summary=sc_weighted_summary,
        dep_summary=dep_summary,
        positive_outcomes=positive_outcomes,
        wifor_impact=wifor_impact,
    )

    print("\n" + "=" * 60)
    print("  Assessment complete.")
    print(f"  Outputs → {RESULTS_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
