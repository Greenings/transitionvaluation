"""
wiforio/alloc.py
─────────────────────────────────────────────────────────────────────────────
Spend-vector construction helpers and NACE sector allocation tables.

These map project-type CAPEX breakdowns directly to WifORIO NACE sector codes.

NACE notation follows FIGARO / Eurostat convention:
  • Hyphens for range aggregates:  C10-12, E37-39
  • Underscores for pair aggregates: C31_32, Q87_88

Public API
──────────
  NACE_ALLOC              — dict: project_type → {nace_code: share}
  SECTORS8_TO_NACE        — dict: sector8_label → [nace_codes] mapping
  make_spend_vector()     — build a full (GeoRegion, NACE) spend Series
  make_project_spend_vector() — convenience wrapper for project archetypes
  aggregate_to_sectors8() — aggregate a WifORIO result to 8 broad sectors
"""

from __future__ import annotations

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# 1. NACE → 8-sector mapping
# ─────────────────────────────────────────────────────────────────────────────

SECTORS8_TO_NACE: dict[str, list[str]] = {
    "Construction": [
        "F",
    ],
    "Energy_Utilities": [
        "D35",
        "E36",
    ],
    "Manufacturing": [
        "C10-12", "C13-15", "C16", "C17", "C18", "C19",
        "C20", "C21", "C22", "C23", "C24", "C25", "C26",
        "C27", "C28", "C29", "C30", "C31_32", "C33",
    ],
    "Transport_Logistics": [
        "G45", "G46", "G47",
        "H49", "H50", "H51", "H52", "H53",
    ],
    "Health_Social": [
        "Q86",
        "Q87_88",
    ],
    "Agriculture": [
        "A01", "A02", "A03",
    ],
    "Mining_Extraction": [
        "B",
    ],
    "Water_Waste": [
        "E37-39",
    ],
}

# Reverse mapping: NACE → broad sector label
NACE_TO_SECTOR8: dict[str, str] = {
    nace: sector
    for sector, naces in SECTORS8_TO_NACE.items()
    for nace in naces
}


# ─────────────────────────────────────────────────────────────────────────────
# 2. Project-type CAPEX allocations (NACE level)
#    Shares sum to 1.0 for each project type.
#    Sources:
#      • World Bank / PPIAF (2020) hospital cost breakdowns
#      • IRENA (2022) renewable power cost structure
#      • ITF/OECD (2019) rail infrastructure cost analysis
# ─────────────────────────────────────────────────────────────────────────────

NACE_ALLOC: dict[str, dict[str, float]] = {

    # ── Rail_Dev (construction phase) ─────────────────────────────────────────
    "Rail_Dev": {
        "F":      0.35,   # Civil works, tunnels, viaducts, earthworks
        "D35":    0.10,   # Catenary / traction power provision
        "C28":    0.14,   # Signalling systems, machinery
        "C30":    0.14,   # Rolling stock, rail vehicles
        "H49":    0.10,   # Land transport / construction logistics
        "Q86":    0.04,   # Occupational health services
        "A01":    0.01,   # Vegetation clearance, track-side management
        "B":      0.08,   # Quarrying: ballast, aggregates
        "E37-39": 0.04,   # Site waste, drainage, remediation
    },

    # ── Rail_Op (operational phase) ───────────────────────────────────────────
    "Rail_Op": {
        "F":      0.10,   # Track, station maintenance & renewal
        "D35":    0.35,   # Traction electricity (dominant OpEx)
        "C33":    0.09,   # Repair and maintenance of rolling stock
        "C28":    0.06,   # Signalling / infrastructure maintenance
        "H49":    0.14,   # Train operations (land transport)
        "H52":    0.06,   # Warehousing, depot support activities
        "Q86":    0.04,   # Passenger health / station medical
        "Q87_88": 0.04,   # Social services (accessibility, assisted travel)
        "A01":    0.01,   # Track-side vegetation management
        "B":      0.03,   # Rail and track material
        "C23":    0.02,   # Ballast, surfacing materials
        "E37-39": 0.06,   # Wastewater, depot waste management
    },

    # ── Energy (renewable / hydro power plant) ────────────────────────────────
    "Energy": {
        "F":      0.38,   # Civil construction (dam, foundations, roads)
        "D35":    0.10,   # Grid interconnection works
        "C27":    0.16,   # Generators, transformers, electrical equipment
        "C28":    0.10,   # Turbines, mechanical plant equipment
        "C25":    0.06,   # Structural steel, fabricated metals
        "H49":    0.07,   # Equipment delivery, construction logistics
        "Q86":    0.03,   # Occupational health
        "A01":    0.01,   # Land clearance and preparation
        "B":      0.05,   # Quarrying for civil works materials
        "C23":    0.02,   # Concrete, cement, aggregate products
        "E37-39": 0.02,   # Site waste and drainage
    },

    # ── Health_Social (general hospital) ─────────────────────────────────────
    "Health_Social": {
        "F":      0.28,   # Hospital building construction
        "D35":    0.08,   # HVAC, medical gas, energy systems
        "C21":    0.10,   # Pharmaceuticals and medical consumables
        "C26":    0.08,   # Diagnostic equipment, electronic devices
        "C27":    0.07,   # Electrical systems (lifts, lighting, IT)
        "H49":    0.07,   # Medical supply logistics
        "Q86":    0.10,   # Clinical health services
        "Q87_88": 0.08,   # Allied health, social care integration
        "A01":    0.02,   # Patient catering / food supply
        "B":      0.03,   # Construction materials (stone, clay)
        "C23":    0.02,   # Masonry, ceramic, glass products
        "E37-39": 0.07,   # Medical waste treatment and sanitation
    },

    # ── Health_Specialized (research / cancer / specialist facility) ───────────
    "Health_Specialized": {
        "F":      0.22,   # Specialized facility construction
        "D35":    0.07,   # Critical energy / clean room infrastructure
        "C21":    0.14,   # Specialized pharmaceuticals, biologics
        "C26":    0.14,   # Precision/optical instruments, lab equipment
        "C27":    0.07,   # Electrical systems for sensitive equipment
        "H49":    0.06,   # Logistics for specialized supplies
        "Q86":    0.18,   # Specialized clinical services
        "A01":    0.01,   # Minimal (landscaping, patient gardens)
        "B":      0.04,   # Building foundation materials
        "C23":    0.02,   # Specialist construction materials
        "E37-39": 0.05,   # Biomedical waste disposal
    },

    # ── Health_General (district / rural hospital) ────────────────────────────
    "Health_General": {
        "F":      0.30,   # District hospital construction
        "D35":    0.10,   # Basic energy / water heating systems
        "C21":    0.08,   # Essential medicines
        "C26":    0.07,   # Basic diagnostic equipment
        "C27":    0.07,   # Electrical systems
        "H49":    0.08,   # Medical supplies / ambulance logistics
        "Q86":    0.10,   # Primary healthcare services
        "Q87_88": 0.05,   # Community nursing, social referrals
        "A01":    0.02,   # Food provisioning for patients
        "B":      0.03,   # Local building materials
        "C23":    0.02,   # Cement, brickwork
        "E37-39": 0.08,   # Sanitation and clinical waste management
    },
}

# Validate allocations sum to 1.0 at import time
for _ptype, _alloc in NACE_ALLOC.items():
    _total = round(sum(_alloc.values()), 10)
    assert abs(_total - 1.0) < 1e-9, (
        f"NACE_ALLOC['{_ptype}'] sums to {_total:.6f}, expected 1.0"
    )


# ─────────────────────────────────────────────────────────────────────────────
# 3. Spend-vector construction
# ─────────────────────────────────────────────────────────────────────────────

def make_spend_vector(
    invest_usd: float,
    alloc: dict[str, float],
    country: str,
    index: pd.MultiIndex,
) -> pd.Series:
    """
    Build a full (GeoRegion, NACE) spend vector aligned to a WifORIO MacroFile.

    Parameters
    ----------
    invest_usd : Investment in USD (converted to M$ internally).
    alloc      : {nace_code: share}, shares must sum to 1.0.
    country    : GeoRegion code as used in the MacroFile (ISO2 for FIGARO core
                 countries, ISO3 for extended Own Table 2.0 coverage).
                 Use ``list_countries()`` in io_lib to see available codes.
    index      : Full (GeoRegion, NACE) MultiIndex from the MacroFile matrix.
                 Obtain via ``pd.read_hdf(macrofile, 'Aspill{year}').index``.

    Returns
    -------
    pd.Series with the same MultiIndex as `index`, values in M$.
    Non-specified (country, NACE) pairs are zero.
    """
    total = sum(alloc.values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(
            f"Allocation shares sum to {total:.6f}; they must sum to 1.0."
        )

    invest_m = invest_usd / 1e6
    y0 = pd.Series(0.0, index=index, dtype=float)

    available_regions = index.get_level_values("GeoRegion").unique()
    if country not in available_regions:
        raise ValueError(
            f"Country '{country}' not found in MacroFile index. "
            f"Available GeoRegions: {sorted(available_regions.tolist())}"
        )

    available_nace = (
        index[index.get_level_values("GeoRegion") == country]
        .get_level_values("NACE")
    )
    missing = [n for n in alloc if n not in available_nace]
    if missing:
        raise ValueError(
            f"NACE code(s) {missing} not found for country '{country}'. "
            f"Available NACE codes: {sorted(available_nace.tolist())}"
        )

    for nace, share in alloc.items():
        y0.loc[(country, nace)] = share * invest_m

    return y0


def make_project_spend_vector(
    invest_usd: float,
    project_type: str,
    country: str,
    index: pd.MultiIndex,
) -> pd.Series:
    """
    Convenience wrapper: build a spend vector from a named project archetype.

    Parameters
    ----------
    invest_usd   : Investment in USD.
    project_type : One of the keys in NACE_ALLOC:
                   'Rail_Dev', 'Rail_Op', 'Energy', 'Health_Social',
                   'Health_Specialized', 'Health_General'.
    country      : GeoRegion code in the MacroFile.
    index        : Full (GeoRegion, NACE) MultiIndex from the MacroFile.
    """
    if project_type not in NACE_ALLOC:
        raise ValueError(
            f"Unknown project_type '{project_type}'. "
            f"Valid types: {list(NACE_ALLOC.keys())}"
        )
    return make_spend_vector(invest_usd, NACE_ALLOC[project_type], country, index)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Aggregation: WifORIO (NACE) → 8 broad sectors
# ─────────────────────────────────────────────────────────────────────────────

def aggregate_to_sectors8(
    series_or_df: pd.Series | pd.DataFrame,
    axis: int = 0,
) -> pd.Series | pd.DataFrame:
    """
    Aggregate a WifORIO result indexed on the NACE level to 8 broad sector
    buckets (Construction, Energy_Utilities, Manufacturing, Transport_Logistics,
    Health_Social, Agriculture, Mining_Extraction, Water_Waste).

    Parameters
    ----------
    series_or_df : Series or DataFrame whose NACE-level index (or column
                   MultiIndex with a 'NACE' level) will be aggregated.
    axis         : 0 to aggregate rows; 1 to aggregate columns.

    Returns
    -------
    Series or DataFrame with NACE replaced by broad sector labels.
    NACE codes not in NACE_TO_SECTOR8 are grouped under 'Other'.
    """
    def _map_nace(label):
        nace = label[-1] if isinstance(label, tuple) else label
        return NACE_TO_SECTOR8.get(nace, "Other")

    if isinstance(series_or_df, pd.Series):
        return series_or_df.groupby(series_or_df.index.map(_map_nace)).sum()

    df = series_or_df
    if axis == 1:
        return df.groupby(df.columns.map(_map_nace), axis=1).sum()
    return df.groupby(df.index.map(_map_nace)).sum()
