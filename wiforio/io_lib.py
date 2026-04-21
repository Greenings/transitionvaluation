"""
wiforio/io_lib.py
─────────────────────────────────────────────────────────────────────────────
Supply-chain tier impact functions for the WifORIO MRIO database.

Public API
──────────
  tier0_impact(y0, macrofile_path, year, model)
      → dict: direct spend impacts   impact₀ = quota · diag(y₀)

  tier1_impact(y0, macrofile_path, year, model)
      → dict: first upstream round   y₁ = A · y₀  →  quota · diag(y₁)

  tier_impact(y0, macrofile_path, year, tier_from, tier_to, model)
      → DataFrame: tier-by-tier power-series decomposition

  total_impact(y0, macrofile_path, year, model)
      → dict: full Leontief total    y_total = L · y₀  →  quota · diag(y_total)

  list_variables(macrofile_path, year)
  list_countries(macrofile_path, year, model)
  list_nace_codes(macrofile_path, year, country, model)
  load_macrofile_info(macrofile_path)
  compare_models(y0, macrofile_path, year, variables)
  clear_cache()


Model variants
──────────────
  "spill"    (default)
      Workforce-closed model (Type II Leontief multiplier).
      Uses Aspill and Lspill. Endogenises household consumption feedback.
      Recommended for socio-economic impact assessment.

  "indirect"
      Open Leontief model (Type I), production effects only.
      Uses Aindirect and Lindirect.
      For tier1_impact / tier_impact with model="indirect", Aindirect must
      be available in the HDF5 file (present in the closed-model H5 but
      commented out in the final MacroFile pipeline). Use model="spill" with
      the final MacroFile, or pass the closed-model H5 path.

HDF5 key conventions
────────────────────
  Final MacroFile  ({version}_MacroFile_{year}{scenario}.h5):
      Aspill{year}, Lspill{year}, Lindirect{year},
      FD{year}, SR{year}, TW{year}, variables{year}, quota{year},
      Variables2Name, info

  Closed model  ({version}_Result_{year}{scenario}_closed.h5):
      Aindirect, Aspill, Lindirect, Lspill,
      Tindirect, Tspill, variables, TW, SR, FD   (no year suffix)

  _load() tries the year-suffixed key first, then falls back to the bare key.

Return structure (tier0, tier1, total)
──────────────────────────────────────
  {
    "tier"       : int | None,
    "model"      : str,
    "year"       : str,
    "invest_M$"  : float,
    "total"      : dict,           # {variable_code: float}
    "by_sector"  : pd.DataFrame,   # variables × (GeoRegion, NACE)
    "by_region"  : pd.DataFrame,   # variables × GeoRegion
  }
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# Internal cache
# ─────────────────────────────────────────────────────────────────────────────

_MATRIX_CACHE: dict[tuple, pd.DataFrame] = {}


def clear_cache() -> None:
    """Release all cached matrices from memory."""
    _MATRIX_CACHE.clear()


def _load(h5_path: Path | str, base_key: str, year: str) -> pd.DataFrame:
    """
    Load a DataFrame from HDF5, trying '{base_key}{year}' first (final
    MacroFile), then bare '{base_key}' (closed-model). Results are cached.
    """
    h5_path = Path(h5_path)
    cache_key = (str(h5_path.resolve()), base_key, year)

    if cache_key in _MATRIX_CACHE:
        return _MATRIX_CACHE[cache_key]

    if not h5_path.exists():
        raise FileNotFoundError(f"WifORIO file not found: {h5_path}")

    for key in (f"{base_key}{year}", base_key):
        try:
            df = pd.read_hdf(h5_path, key=key)
            _MATRIX_CACHE[cache_key] = df
            return df
        except KeyError:
            continue

    try:
        import h5py
        with h5py.File(h5_path, "r") as f:
            available = list(f.keys())
    except Exception:
        available = ["<could not list keys>"]

    raise KeyError(
        f"Key '{base_key}{year}' or '{base_key}' not found in {h5_path}.\n"
        f"Available HDF5 keys: {available}\n"
        f"Tip: for model='indirect' tier functions, use the closed-model H5."
    )


def _maybe_drop_year(df: pd.DataFrame | pd.Series, year: str) -> pd.DataFrame | pd.Series:
    idx = df.index if hasattr(df, "index") else None
    if idx is not None and isinstance(idx, pd.MultiIndex) and idx.names[0] == "Year":
        return df.loc[year]
    return df


def _build_result(
    impact_by_sector: pd.DataFrame,
    invest_m: float,
    year: str,
    model: str,
    tier: Optional[int],
) -> dict:
    by_region = impact_by_sector.groupby(level="GeoRegion", axis=1).sum()
    return {
        "tier":        tier,
        "model":       model,
        "year":        year,
        "invest_M$":   invest_m,
        "total":       impact_by_sector.sum(axis=1).to_dict(),
        "by_sector":   impact_by_sector,
        "by_region":   by_region,
    }


def _align_y0(y0: pd.Series, ref_index: pd.MultiIndex) -> pd.Series:
    return y0.reindex(ref_index, fill_value=0.0)


# ─────────────────────────────────────────────────────────────────────────────
# Core impact functions
# ─────────────────────────────────────────────────────────────────────────────

def tier0_impact(
    y0: pd.Series,
    macrofile_path: str | Path,
    year: str,
    model: str = "spill",
) -> dict:
    """
    Tier 0 (direct spend) impact.

    Math:  impact₀ = quota · diag(y₀)

    Parameters
    ----------
    y0             : Spend vector in M$, indexed by (GeoRegion, NACE) MultiIndex.
                     Build with ``alloc.make_project_spend_vector()``.
    macrofile_path : Path to the WifORIO HDF5 MacroFile.
    year           : Data year string, e.g. '2022' or '2050'.
    model          : 'spill' (default) or 'indirect'.
    """
    quota = _load(macrofile_path, "quota", year)
    quota = _maybe_drop_year(quota, year)
    impact = quota.mul(_align_y0(y0, quota.columns), axis=1)
    return _build_result(impact, float(y0.sum()), year, model, tier=0)


def tier1_impact(
    y0: pd.Series,
    macrofile_path: str | Path,
    year: str,
    model: str = "spill",
) -> dict:
    """
    Tier 1 (first upstream round) impact.

    Math:  y₁ = A · y₀;   impact₁ = quota · diag(y₁)

    Trade is fully endogenous in WifORIO's A matrix — no separate bilateral
    trade lookup is needed.

    Parameters
    ----------
    y0             : Spend vector in M$, indexed by (GeoRegion, NACE).
    macrofile_path : Path to the WifORIO HDF5 file.
                     For model='indirect': use the closed-model H5 (contains
                     'Aindirect'); for model='spill': final MacroFile suffices.
    year           : Data year string.
    model          : 'spill' (default) or 'indirect'.
    """
    a_key = "Aspill" if model == "spill" else "Aindirect"
    A     = _load(macrofile_path, a_key, year)
    quota = _load(macrofile_path, "quota", year)
    quota = _maybe_drop_year(quota, year)
    y1    = A.dot(_align_y0(y0, A.columns))
    impact = quota.mul(y1, axis=1)
    return _build_result(impact, float(y0.sum()), year, model, tier=1)


def tier_impact(
    y0: pd.Series,
    macrofile_path: str | Path,
    year: str,
    tier_from: int = 0,
    tier_to: int = 6,
    model: str = "spill",
) -> pd.DataFrame:
    """
    Tier-by-tier supply-chain impact using power-series decomposition.

    For each tier t in [tier_from, tier_to]:
        yₜ = Aᵗ · y₀
        impactₜ = Σⱼ quota[:,j] · yₜ[j]

    Parameters
    ----------
    y0             : Spend vector in M$, indexed by (GeoRegion, NACE).
    macrofile_path : Path to the WifORIO HDF5 file.
    year           : Data year string.
    tier_from      : First tier to compute (default 0 = direct spend).
    tier_to        : Last tier to compute inclusive (default 6).
    model          : 'spill' (default) or 'indirect'.

    Returns
    -------
    pd.DataFrame — shape (n_tiers, n_variables), index name = 'tier'.

    Performance note
    ────────────────
    Each A-matrix multiplication on the full WifORIO dimension (n ≈ 10 000)
    takes 0.1–0.5 s. Use ``total_impact()`` for a single exact aggregate.
    """
    if tier_from < 0:
        raise ValueError(f"tier_from must be >= 0, got {tier_from}")
    if tier_to < tier_from:
        raise ValueError(f"tier_to ({tier_to}) must be >= tier_from ({tier_from})")

    a_key  = "Aspill" if model == "spill" else "Aindirect"
    A      = _load(macrofile_path, a_key, year)
    quota  = _load(macrofile_path, "quota", year)
    quota  = _maybe_drop_year(quota, year)

    y_cur = _align_y0(y0, A.columns)
    for _ in range(tier_from):
        y_cur = A.dot(y_cur)

    records: list[pd.Series] = []
    for t in range(tier_from, tier_to + 1):
        row = quota.mul(y_cur, axis=1).sum(axis=1)
        row.name = t
        records.append(row)
        y_cur = A.dot(y_cur)

    df = pd.DataFrame(records)
    df.index.name = "tier"
    return df


def total_impact(
    y0: pd.Series,
    macrofile_path: str | Path,
    year: str,
    model: str = "spill",
) -> dict:
    """
    Full Leontief supply-chain impact (exact sum of all tiers).

    Uses the pre-computed Leontief inverse L = (I − A)⁻¹.
    Equivalent to tier_impact() with tier_to=∞, but exact and fast.

    Math:  y_total = L · y₀  =  Σ_{t=0}^{∞} Aᵗ · y₀

    Parameters
    ----------
    y0             : Spend vector in M$, indexed by (GeoRegion, NACE).
    macrofile_path : Path to the WifORIO HDF5 file.
    year           : Data year string.
    model          : 'spill' → Lspill (Type II, WF-closed);
                     'indirect' → Lindirect (Type I, open).
    """
    l_key = "Lspill" if model == "spill" else "Lindirect"
    L     = _load(macrofile_path, l_key, year)
    quota = _load(macrofile_path, "quota", year)
    quota = _maybe_drop_year(quota, year)
    y_total = L.dot(_align_y0(y0, L.columns))
    impact  = quota.mul(y_total, axis=1)
    return _build_result(impact, float(y0.sum()), year, model, tier=None)


# ─────────────────────────────────────────────────────────────────────────────
# Introspection utilities
# ─────────────────────────────────────────────────────────────────────────────

def list_variables(
    macrofile_path: str | Path,
    year: str,
) -> pd.DataFrame:
    """
    Return a DataFrame mapping variable codes to human-readable names.

    Columns: name, in_quota (bool — whether the variable appears in the quota
    matrix for this year).
    """
    h5_path = Path(macrofile_path)
    v2n = pd.read_hdf(h5_path, key="Variables2Name")
    if isinstance(v2n, pd.Series):
        v2n_df = v2n.to_frame(name="name")
    else:
        v2n_df = v2n.copy()
        if "name" not in v2n_df.columns and v2n_df.shape[1] == 1:
            v2n_df.columns = ["name"]

    try:
        quota = _load(macrofile_path, "quota", year)
        quota = _maybe_drop_year(quota, year)
        v2n_df["in_quota"] = v2n_df.index.isin(set(quota.index.tolist()))
    except (KeyError, FileNotFoundError):
        v2n_df["in_quota"] = pd.NA

    return v2n_df.sort_index()


def list_countries(
    macrofile_path: str | Path,
    year: str,
    model: str = "spill",
) -> list[str]:
    """Return sorted list of available GeoRegion codes."""
    a_key = "Aspill" if model == "spill" else "Aindirect"
    A = _load(macrofile_path, a_key, year)
    return sorted(A.columns.get_level_values("GeoRegion").unique().tolist())


def list_nace_codes(
    macrofile_path: str | Path,
    year: str,
    country: Optional[str] = None,
    model: str = "spill",
) -> list[str]:
    """Return sorted list of NACE sector codes, optionally filtered by country."""
    a_key = "Aspill" if model == "spill" else "Aindirect"
    A = _load(macrofile_path, a_key, year)
    idx = A.columns
    if country is not None:
        idx = idx[idx.get_level_values("GeoRegion") == country]
    return sorted(idx.get_level_values("NACE").unique().tolist())


def load_macrofile_info(macrofile_path: str | Path) -> pd.Series:
    """Return the metadata Series stored in the 'info' key of a MacroFile."""
    return pd.read_hdf(Path(macrofile_path), key="info")


def compare_models(
    y0: pd.Series,
    macrofile_path: str | Path,
    year: str,
    variables: Optional[list[str]] = None,
) -> pd.DataFrame:
    """
    Run total_impact() for both model variants and return a comparison.

    Returns pd.DataFrame with columns
    ['indirect', 'spill', 'ratio_spill_indirect'], indexed by variable code.
    """
    res_ind = total_impact(y0, macrofile_path, year, model="indirect")
    res_spl = total_impact(y0, macrofile_path, year, model="spill")

    df = pd.concat([
        pd.Series(res_ind["total"], name="indirect"),
        pd.Series(res_spl["total"], name="spill"),
    ], axis=1)

    safe = df["indirect"].replace(0, np.nan)
    df["ratio_spill_indirect"] = (df["spill"] / safe).round(3)

    if variables is not None:
        df = df.loc[df.index.isin(variables)]

    return df.sort_index()
