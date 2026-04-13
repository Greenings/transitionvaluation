#!/usr/bin/env python3
"""
investment_sankey.py — Dynamic supply-chain Sankey for any investment

Usage
─────
  python investment_sankey.py --capex 100M --country DE --sector Rail_Dev
  python investment_sankey.py -c 50000000 -C Brazil -s Health_Social
  python investment_sankey.py --capex 200M --country Africa --sector Energy \\
         --scenario SSP2-4.5 --year 2030 --no-browser

Sector codes
────────────
  Health_Social | Health_Specialized | Health_General
  Energy | Rail_Dev | Rail_Op

Country
───────
  ISO2 code  : DE, BR, ZA, NG, IN, CN, FR, GB, ...
  Region name: Europe | LATAM | Africa | Asia

CAPEX formats
─────────────
  100M   → $100,000,000
  1.5B   → $1,500,000,000
  250000000 → $250,000,000
"""

import argparse
import re
import sys
import webbrowser
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ── Path setup ──────────────────────────────────────────────────────────────
_HERE = Path(__file__).resolve().parent       # project_assessment/
_ROOT = _HERE.parent                          # tvp5/
sys.path.insert(0, str(_ROOT / "tvp_dbio"))

from tvp_io_lib import (
    tier0_impact, tier1_impact, tier_impact,
    ISO2_TO_REGION, SECTOR_ALLOC,
)

# ── Constants ───────────────────────────────────────────────────────────────
VALID_SECTORS  = list(SECTOR_ALLOC.keys())
VALID_REGIONS  = ("Europe", "LATAM", "Africa", "Asia", "Global")
VALID_SSPS     = ("SSP1-1.9", "SSP2-4.5", "SSP3-7.0", "SSP4-6.0", "SSP5-8.5")
VALID_YEARS    = (2025, 2030, 2040)

# Stressor config: (csv_col, display_name, unit, hex_color, polarity_sign)
STRESSORS = [
    ("GHG_tCO2e",      "GHG",        "tCO₂e",  "#d62728", "[−]"),
    ("Employment_FTE", "Employment", "FTE",     "#2ca02c", "[+]"),
    ("Water_1000m3",   "Water",      "000 m³",  "#1f77b4", "[−]"),
]

TOP_N = 5   # max breakdown nodes per tier in Sankey

# Common full country names → ISO2 (case-insensitive lookup)
COUNTRY_NAME_TO_ISO2: dict[str, str] = {
    "germany": "DE", "france": "FR", "united kingdom": "GB", "uk": "GB",
    "spain": "ES", "italy": "IT", "netherlands": "NL", "poland": "PL",
    "sweden": "SE", "norway": "NO", "switzerland": "CH", "turkey": "TR",
    "ukraine": "UA",
    "brazil": "BR", "mexico": "MX", "argentina": "AR", "colombia": "CO",
    "chile": "CL", "peru": "PE", "venezuela": "VE", "ecuador": "EC",
    "south africa": "ZA", "nigeria": "NG", "kenya": "KE", "ethiopia": "ET",
    "ghana": "GH", "tanzania": "TZ", "egypt": "EG", "morocco": "MA",
    "china": "CN", "india": "IN", "japan": "JP", "south korea": "KR",
    "indonesia": "ID", "thailand": "TH", "vietnam": "VN", "philippines": "PH",
    "malaysia": "MY", "pakistan": "PK", "bangladesh": "BD", "russia": "RU",
    "united states": "US", "usa": "US", "canada": "CA", "australia": "AU",
}

# Node colours by tier
TIER_NODE = {"t0": "#4e79a7", "t1": "#f28e2b", "t2": "#59a14f", "t3": "#b07aa1"}
TIER_LINK = {
    "t0": "rgba(78,121,167,0.35)",
    "t1": "rgba(242,142,43,0.35)",
    "t2": "rgba(89,161,79,0.35)",
    "t3": "rgba(176,122,161,0.35)",
}
INTER_NODE = {"t0": "#aec7e8", "t1": "#ffbb78", "t2": "#98df8a", "t3": "#c5b0d5"}

# Scenario intensity factor CSV (tvp_scenario output)
INTENSITY_CSV = (
    _ROOT / "tvp_scenario" / "osemosys" / "results" / "tvpdbio_intensity_factors.csv"
)


# ══════════════════════════════════════════════════════════════════════════════
# INPUT HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def parse_capex(value: str) -> float:
    """Parse '100M', '1.5B', '250000000' → float USD."""
    v = value.strip().upper().replace(",", "").replace("_", "")
    m = re.match(r"^([\d.]+)([KMB]?)$", v)
    if not m:
        raise argparse.ArgumentTypeError(
            f"Cannot parse CAPEX '{value}'. Use e.g. 100M, 1.5B, 250000000"
        )
    num = float(m.group(1))
    mult = {"K": 1e3, "M": 1e6, "B": 1e9}.get(m.group(2), 1.0)
    return num * mult


def resolve_country(raw: str) -> str:
    """ISO2 code, full country name, or region name → canonical broad region."""
    upper = raw.strip().upper()
    # Direct ISO2 match
    if upper in ISO2_TO_REGION:
        return ISO2_TO_REGION[upper]
    # Region name match (case-insensitive)
    region_upper = {r.upper(): r for r in VALID_REGIONS}
    if upper in region_upper:
        return region_upper[upper]
    # Full country name match
    lower = raw.strip().lower()
    iso2 = COUNTRY_NAME_TO_ISO2.get(lower)
    if iso2 and iso2 in ISO2_TO_REGION:
        return ISO2_TO_REGION[iso2]
    return "Global"


def fmt_capex(capex: float) -> str:
    if capex >= 1e9:
        return f"${capex / 1e9:.2f}B"
    if capex >= 1e6:
        return f"${capex / 1e6:.1f}M"
    return f"${capex:,.0f}"


# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO ADJUSTMENT
# ══════════════════════════════════════════════════════════════════════════════

def load_scenario_factors(region: str, scenario: str, year: int) -> dict | None:
    """
    Load per-stressor adjustment ratios from the pre-computed OSeMOSYS intensity
    factor CSV.  Returns None if the file or matching row is not found.
    """
    if not INTENSITY_CSV.exists():
        return None
    df  = pd.read_csv(INTENSITY_CSV)
    row = df[
        (df["region"]   == region) &
        (df["scenario"] == scenario) &
        (df["year"]     == float(year))
    ]
    if row.empty:
        return None
    r  = row.iloc[0]
    rs = float(r.get("renewable_share", 0.5))
    return {
        "GHG_tCO2e":      float(r["adj_ratio_ghg"]),
        "Employment_FTE": float(r["adj_ratio_employment"]),
        "Water_1000m3":   float(rs * 0.15 + (1.0 - rs) * 1.0),
        "ValueAdded_M$":  float(r["adj_ratio_employment"]),
    }


def adj(value: float, col: str, factors: dict | None) -> float:
    """Apply scenario factor to a stressor value."""
    if factors is None or value == 0:
        return value
    return value * factors.get(col, 1.0)


# ══════════════════════════════════════════════════════════════════════════════
# SANKEY CONSTRUCTION
# ══════════════════════════════════════════════════════════════════════════════

def _top_n_other(series: pd.Series, n: int = TOP_N) -> pd.Series:
    """Keep top-N entries; fold the remainder into 'Other'."""
    series = series[series > 0]
    if len(series) <= n:
        return series
    top  = series.nlargest(n)
    rest = series[~series.index.isin(top.index)].sum()
    if rest > 0:
        top = pd.concat([top, pd.Series({"Other": rest})])
    return top


def _sankey_data(
    col: str,
    t0_res: dict,
    t1_res: dict,
    t2_df:  pd.DataFrame,
    t3_df:  pd.DataFrame,
    factors: dict | None,
) -> dict:
    """
    Build Plotly Sankey node/link arrays for one stressor column.

    Node layout
    ───────────
    Layer 0 (sources):  Tier 0 / 1 / 2 / 3-10  (4 fixed nodes)
    Layer 1 (middle):   T0 sector / T1 sourcing-region / T2 sector / T3+ sector
    Layer 2 (sink):     single terminal node labelled with total
    """
    nodes, n_color = [], []
    src, tgt, val, lnk_col = [], [], [], []

    def node(label: str, color: str) -> int:
        if label not in nodes:
            nodes.append(label)
            n_color.append(color)
        return nodes.index(label)

    def add_flow(tier_idx: int, breakdown: pd.Series, tk: str, prefix: str):
        for name, v in breakdown.items():
            mid = node(f"{prefix}{name}", INTER_NODE[tk])
            c   = TIER_LINK[tk]
            src.extend([tier_idx, mid])
            tgt.extend([mid, term_idx])
            val.extend([v, v])
            lnk_col.extend([c, c])

    # Stressor metadata
    meta = next(m for m in STRESSORS if m[0] == col)
    _, sname, sunit, s_col, ssign = meta

    # ── Tier totals (scenario-adjusted) ─────────────────────────────────────
    t0_total = adj(t0_res[col], col, factors)
    t1_total = adj(t1_res[col], col, factors)
    t2_total = adj(t2_df[col].sum(), col, factors) if (not t2_df.empty and col in t2_df.columns) else 0.0
    t3_total = adj(t3_df[col].sum(), col, factors) if (not t3_df.empty and col in t3_df.columns) else 0.0
    grand    = t0_total + t1_total + t2_total + t3_total

    # Terminal node — added first so its index is stable
    term_label = f"{sname}\n{grand:,.0f} {sunit}"
    i0   = node("Tier 0\nDirect CAPEX",       TIER_NODE["t0"])
    i1   = node("Tier 1\nBilateral Sourcing",  TIER_NODE["t1"])
    i2   = node("Tier 2\nSecond Upstream",     TIER_NODE["t2"])
    i3   = node("Tier 3–10\nDeep Upstream",    TIER_NODE["t3"])
    term_idx = node(term_label, s_col)

    # ── Tier 0: sector breakdown ─────────────────────────────────────────────
    t0_sec = _top_n_other(pd.Series({
        sec: adj(v[col], col, factors)
        for sec, v in t0_res["impact_by_sector"].items()
        if v.get(col, 0) > 0
    }))
    add_flow(i0, t0_sec, "t0", "T0 ")

    # ── Tier 1: sourcing-region breakdown (bilateral) ────────────────────────
    t1_reg = _top_n_other(pd.Series({
        reg: adj(v[col], col, factors)
        for reg, v in t1_res["sourcing_summary"].items()
        if v.get(col, 0) > 0
    }))
    add_flow(i1, t1_reg, "t1", "T1 ")

    # ── Tier 2: sector breakdown ─────────────────────────────────────────────
    if t2_total > 0:
        t2_sec = _top_n_other(
            t2_df.groupby("supplying_sector")[col].sum()
            .apply(lambda v: adj(v, col, factors))
        )
        add_flow(i2, t2_sec, "t2", "T2 ")

    # ── Tier 3-10: sector breakdown ──────────────────────────────────────────
    if t3_total > 0:
        t3_sec = _top_n_other(
            t3_df.groupby("supplying_sector")[col].sum()
            .apply(lambda v: adj(v, col, factors))
        )
        add_flow(i3, t3_sec, "t3", "T3+ ")

    return dict(
        nodes=nodes, n_color=n_color,
        src=src, tgt=tgt, val=val, lnk_col=lnk_col,
        grand=grand, term_label=term_label,
        sname=sname, sunit=sunit, s_col=s_col, ssign=ssign,
        t0=t0_total, t1=t1_total, t2=t2_total, t3=t3_total,
    )


def build_figure(
    capex:    float,
    country:  str,
    region:   str,
    sector:   str,
    t0_res:   dict,
    t1_res:   dict,
    t2_df:    pd.DataFrame,
    t3_df:    pd.DataFrame,
    scenario: str | None,
    year:     int,
    factors:  dict | None,
) -> go.Figure:
    """Assemble the three-panel Sankey figure."""
    n  = len(STRESSORS)
    gap   = 0.03
    width = (1.0 - gap * (n - 1)) / n

    fig = go.Figure()

    for i, (col, *_) in enumerate(STRESSORS):
        d  = _sankey_data(col, t0_res, t1_res, t2_df, t3_df, factors)
        x0 = i * (width + gap)
        x1 = x0 + width

        fig.add_trace(go.Sankey(
            domain=dict(x=[x0, x1], y=[0.0, 0.90]),
            arrangement="snap",
            node=dict(
                label=d["nodes"], color=d["n_color"],
                pad=14, thickness=18,
                line=dict(color="white", width=0.4),
            ),
            link=dict(
                source=d["src"], target=d["tgt"],
                value=d["val"],  color=d["lnk_col"],
            ),
        ))

        sc_tag = f" · {scenario} {year}" if scenario else ""
        fig.add_annotation(
            x=(x0 + x1) / 2, y=1.0,
            xref="paper", yref="paper",
            text=(
                f"<b>{d['ssign']} {d['sname']}</b>{sc_tag}"
                f"<br><span style='font-size:11px;color:{d['s_col']}'>"
                f"{d['grand']:,.0f} {d['sunit']}</span>"
            ),
            showarrow=False, font=dict(size=13), align="center",
        )

    sc_note = f" — {scenario} {year}" if scenario else " — Baseline"
    fig.update_layout(
        title=dict(
            text=(
                f"<b>Supply-Chain Sankey</b>{sc_note}"
                f"<br><span style='font-size:12px;color:#555'>"
                f"Investment: {fmt_capex(capex)}"
                f" · Country: {country} ({region})"
                f" · Sector: {sector}"
                f"</span>"
            ),
            x=0.01, xanchor="left",
            font=dict(size=15),
        ),
        height=600,
        margin=dict(l=20, r=20, t=105, b=20),
        paper_bgcolor="#fafafa",
        font=dict(family="Arial", size=10),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# CONSOLE SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

def print_summary(
    capex:    float,
    country:  str,
    region:   str,
    sector:   str,
    t0_res:   dict,
    t1_res:   dict,
    t2_df:    pd.DataFrame,
    t3_df:    pd.DataFrame,
    scenario: str | None,
    year:     int,
    factors:  dict | None,
):
    all_cols = ["GHG_tCO2e", "Employment_FTE", "Water_1000m3", "ValueAdded_M$"]

    def safe(d: dict, col: str) -> float:
        return adj(d.get(col, 0.0), col, factors)

    def df_sum(df: pd.DataFrame, col: str) -> float:
        return adj(df[col].sum() if (not df.empty and col in df.columns) else 0.0, col, factors)

    tiers = {
        "Tier 0  Direct CAPEX":     {c: safe(t0_res, c) for c in all_cols},
        "Tier 1  Bilateral":        {c: safe(t1_res, c) for c in all_cols},
        "Tier 2  Second upstream":  {c: df_sum(t2_df, c) for c in all_cols},
        "Tier 3-10  Deep upstream": {c: df_sum(t3_df, c) for c in all_cols},
    }
    total = {c: sum(v[c] for v in tiers.values()) for c in all_cols}

    sc_line = f"  Scenario : {scenario} | Year: {year}\n" if scenario else ""
    print()
    print("═" * 75)
    print(f"  Supply-Chain Impact Analysis")
    print(f"  CAPEX    : {fmt_capex(capex)}")
    print(f"  Country  : {country}  ({region})")
    print(f"  Sector   : {sector}")
    print(sc_line, end="")
    print("─" * 75)
    print(f"  {'Layer':<28} {'GHG tCO2e [−]':>14} {'Jobs FTE [+]':>12}"
          f" {'Water 000m3 [−]':>15} {'VA M$ [+]':>10}")
    print("─" * 75)
    for tname, vals in tiers.items():
        print(f"  {tname:<28} "
              f"{vals['GHG_tCO2e']:>14,.1f} "
              f"{vals['Employment_FTE']:>12,.1f} "
              f"{vals['Water_1000m3']:>15,.1f} "
              f"{vals['ValueAdded_M$']:>10,.2f}")
    print("─" * 75)
    print(f"  {'TOTAL':<28} "
          f"{total['GHG_tCO2e']:>14,.1f} "
          f"{total['Employment_FTE']:>12,.1f} "
          f"{total['Water_1000m3']:>15,.1f} "
          f"{total['ValueAdded_M$']:>10,.2f}")
    print("═" * 75)

    # Tier 1 sourcing breakdown
    ghg_t1 = adj(t1_res["GHG_tCO2e"], "GHG_tCO2e", factors)
    if ghg_t1 > 0:
        print("\n  Tier 1 bilateral GHG sourcing:")
        for reg, v in sorted(t1_res["sourcing_summary"].items(),
                              key=lambda x: -x[1]["GHG_tCO2e"]):
            g = adj(v["GHG_tCO2e"], "GHG_tCO2e", factors)
            if g > 0:
                pct = g / ghg_t1 * 100
                bar = "█" * int(pct / 5)
                print(f"    {reg:<10}  {g:>9,.1f} tCO₂e  {pct:5.1f}%  {bar}")
    print()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        prog="investment_sankey",
        description="Dynamic supply-chain Sankey for any investment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Sector codes: " + " | ".join(VALID_SECTORS) + "\n"
            "Countries  : ISO2 (DE, BR, ZA, NG, IN, CN, FR ...) or region name\n"
            "Scenarios  : " + " | ".join(VALID_SSPS) + "\n"
        ),
    )
    parser.add_argument("--capex",    "-c", required=True, type=parse_capex,
        metavar="AMOUNT", help="Investment in USD: 100M, 1.5B, 250000000")
    parser.add_argument("--country",  "-C", required=True,
        metavar="COUNTRY", help="ISO2 code or region (Europe, Africa, Asia, LATAM)")
    parser.add_argument("--sector",   "-s", required=True, choices=VALID_SECTORS,
        metavar="SECTOR",  help="Sector archetype (see epilog)")
    parser.add_argument("--scenario", "-S", default=None, choices=list(VALID_SSPS),
        metavar="SSP",     help="SSP scenario for adjustment (optional)")
    parser.add_argument("--year",     "-y", default=2030, type=int, choices=list(VALID_YEARS),
        metavar="YEAR",    help="Analysis year for scenario (default: 2030)")
    parser.add_argument("--database", "-d", default="exiobase",
        metavar="DB",      help="IO database (default: exiobase)")
    parser.add_argument("--output",   "-o", default=None,
        metavar="PATH",    help="HTML output path (default: auto-named in results/)")
    parser.add_argument("--no-browser", action="store_true",
        help="Do not open browser after generating")

    args = parser.parse_args()

    region = resolve_country(args.country)
    if region == "Global":
        print(f"[WARN] '{args.country}' not recognised; defaulting to Global.")

    print()
    print(f"  Investment  : {fmt_capex(args.capex)}")
    print(f"  Country     : {args.country}  →  {region}")
    print(f"  Sector      : {args.sector}")
    print(f"  Database    : {args.database}")
    if args.scenario:
        print(f"  Scenario    : {args.scenario} ({args.year})")

    # ── IO analysis ──────────────────────────────────────────────────────────
    print("\n[1/4] Tier 0 — direct CAPEX spend ...", end=" ", flush=True)
    t0_res = tier0_impact(args.capex, args.sector, region, args.database)
    print(f"GHG {t0_res['GHG_tCO2e']:,.0f} tCO₂e")

    print("[2/4] Tier 1 — bilateral first upstream ...", end=" ", flush=True)
    t1_res = tier1_impact(args.capex, args.sector, region, args.database)
    print(f"GHG {t1_res['GHG_tCO2e']:,.0f} tCO₂e  |  regions: {list(t1_res['sourcing_summary'].keys())}")

    print("[3/4] Tier 2 — second upstream ...", end=" ", flush=True)
    t2_df = tier_impact(args.capex, args.sector, region, args.database, tier_from=2, tier_to=2)
    print(f"{len(t2_df)} rows")

    print("[4/4] Tier 3-10 — deep upstream ...", end=" ", flush=True)
    t3_df = tier_impact(args.capex, args.sector, region, args.database, tier_from=3, tier_to=10)
    print(f"{len(t3_df)} rows")

    # ── Scenario factors ─────────────────────────────────────────────────────
    factors = None
    if args.scenario:
        factors = load_scenario_factors(region, args.scenario, args.year)
        if factors:
            print(f"\n[INFO] Scenario factors ({region} / {args.scenario} / {args.year}):")
            for k, v in factors.items():
                print(f"         {k:<22} × {v:.4f}")
        else:
            print(f"\n[WARN] No scenario factors for {region}/{args.scenario}/{args.year}; "
                  "showing baseline.")

    # ── Console table ────────────────────────────────────────────────────────
    print_summary(args.capex, args.country, region, args.sector,
                  t0_res, t1_res, t2_df, t3_df,
                  args.scenario, args.year, factors)

    # ── Build Sankey ─────────────────────────────────────────────────────────
    fig = build_figure(
        args.capex, args.country, region, args.sector,
        t0_res, t1_res, t2_df, t3_df,
        args.scenario, args.year, factors,
    )

    # ── Save HTML ────────────────────────────────────────────────────────────
    out_dir = _HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.output:
        out_path = Path(args.output)
    else:
        sc_tag = f"_{args.scenario}_{args.year}" if args.scenario else ""
        ctag   = args.country.upper().replace(" ", "_")
        ctag2  = f"{ctag}_{region}" if ctag not in VALID_REGIONS else ctag
        mtag   = (f"{args.capex/1e9:.1f}B" if args.capex >= 1e9
                  else f"{args.capex/1e6:.0f}M")
        out_path = out_dir / f"sankey_{args.sector}_{ctag2}_{mtag}{sc_tag}.html"

    fig.write_html(str(out_path), include_plotlyjs="cdn")
    print(f"[OK] Sankey saved  →  {out_path}")

    if not args.no_browser:
        webbrowser.open(out_path.as_uri())
        print("[OK] Opened in browser.")


if __name__ == "__main__":
    main()
