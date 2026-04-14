#!/usr/bin/env python3
"""
Generate one investment_integrated_finance notebook per project in the
modeled input data. Each notebook is a copy of the template with its
params cell updated for the specific project.

Projects sourced from:
  modeled_input_data/rail_finance_input.csv
  modeled_input_data/hospitals_finance_input.csv
  modeled_input_data/hydro_finance_input.csv
"""
import json, copy, pathlib, textwrap

BASE    = pathlib.Path(__file__).parent
TEMPLATE = BASE / "investment_integrated_finance.ipynb"
OUT_DIR  = BASE / "integrated_finance"
OUT_DIR.mkdir(exist_ok=True)

# EUR → USD exchange rate (use a conservative fixed rate for consistency)
EUR_TO_USD = 1.08

# ─────────────────────────────────────────────────────────────────
# Project registry: one dict per project
#   project_id   – matches scenario_adjustment.csv / dependency_summary.csv
#   country      – ISO-2 or broad label used by REGION_TO_ISO3
#   region       – exact region key used in scenario_adjustment.csv
#   sector       – one of Health_Social | Health_Specialized | Health_General
#                          Energy | Rail_Dev | Rail_Op
#   capex_usd    – capital expenditure in USD
#   avoided_co2  – annual avoided tCO2e from operations (0 if N/A)
#   revenue_yield– annual revenue as fraction of CAPEX
#   opex_ratio   – annual OPEX as fraction of CAPEX
#   bond_years   – bond lifetime
#   project_years– operational lifetime
#   wacc_base    – base WACC
#   scenario     – default SSP scenario for single-scenario cells
# ─────────────────────────────────────────────────────────────────
PROJECTS = [
    # ── Rail ──────────────────────────────────────────────────────
    dict(
        project_id    = "Rail_EU_DEV",
        country       = "DE",
        region        = "Europe",
        sector        = "Rail_Dev",
        capex_usd     = round(1_850_000_000 * EUR_TO_USD),
        avoided_co2   = 50_000,
        revenue_yield = 0.12,
        opex_ratio    = 0.04,
        bond_years    = 10,
        project_years = 30,
        wacc_base     = 0.065,
        scenario      = "SSP2-4.5",
        notes         = "Large-scale European rail development; CAPEX converted from EUR 1,850 M",
    ),
    dict(
        project_id    = "Rail_EU_OP1",
        country       = "DE",
        region        = "Europe",
        sector        = "Rail_Op",
        capex_usd     = round(130_000 * EUR_TO_USD),
        avoided_co2   = 0,
        revenue_yield = 0.10,
        opex_ratio    = 0.06,
        bond_years    = 5,
        project_years = 15,
        wacc_base     = 0.055,
        scenario      = "SSP2-4.5",
        notes         = "Operational rail maintenance tranche; CAPEX EUR 130k",
    ),
    dict(
        project_id    = "Rail_EU_OP2",
        country       = "DE",
        region        = "Europe",
        sector        = "Rail_Op",
        capex_usd     = round(90_000 * EUR_TO_USD),
        avoided_co2   = 0,
        revenue_yield = 0.10,
        opex_ratio    = 0.06,
        bond_years    = 5,
        project_years = 15,
        wacc_base     = 0.055,
        scenario      = "SSP2-4.5",
        notes         = "Operational rail maintenance tranche; CAPEX EUR 90k",
    ),
    # ── Health / Hospitals ────────────────────────────────────────
    dict(
        project_id    = "Proj_001",
        country       = "BR",
        region        = "LATAM",
        sector        = "Health_Social",
        capex_usd     = 250_000_000,
        avoided_co2   = 0,
        revenue_yield = 0.08,
        opex_ratio    = 0.06,
        bond_years    = 10,
        project_years = 25,
        wacc_base     = 0.080,
        scenario      = "SSP2-4.5",
        notes         = "Primary/preventative care hub; 5M beneficiaries; LATAM PPP import leakage",
    ),
    dict(
        project_id    = "Proj_002",
        country       = "NG",
        region        = "Africa",
        sector        = "Health_Specialized",
        capex_usd     = 25_000_000,
        avoided_co2   = 0,
        revenue_yield = 0.09,
        opex_ratio    = 0.07,
        bond_years    = 7,
        project_years = 20,
        wacc_base     = 0.090,
        scenario      = "SSP2-4.5",
        notes         = "Tertiary/surgical specialised hospital; 3,000 beneficiaries; Africa risk premium",
    ),
    dict(
        project_id    = "Proj_003",
        country       = "DE",
        region        = "Europe",
        sector        = "Health_General",
        capex_usd     = 75_000_000,
        avoided_co2   = 0,
        revenue_yield = 0.09,
        opex_ratio    = 0.05,
        bond_years    = 10,
        project_years = 25,
        wacc_base     = 0.060,
        scenario      = "SSP2-4.5",
        notes         = "General hospital; 500k beneficiaries; European regulated tariff",
    ),
    # ── Hydro ─────────────────────────────────────────────────────
    dict(
        project_id    = "Hydro_AF",
        country       = "NG",
        region        = "Africa",
        sector        = "Energy",
        capex_usd     = 30_000_000,
        avoided_co2   = 150_000,
        revenue_yield = 0.11,
        opex_ratio    = 0.03,
        bond_years    = 10,
        project_years = 30,
        wacc_base     = 0.085,
        scenario      = "SSP2-4.5",
        notes         = "Hydro refurbishment; 150k tCO2e/yr avoided; coal displacement",
    ),
    dict(
        project_id    = "Hydro_AS",
        country       = "IN",
        region        = "Asia",
        sector        = "Energy",
        capex_usd     = 150_000_000,
        avoided_co2   = 834_218,
        revenue_yield = 0.11,
        opex_ratio    = 0.03,
        bond_years    = 15,
        project_years = 35,
        wacc_base     = 0.075,
        scenario      = "SSP2-4.5",
        notes         = "Large-scale hydro retrofit; 834k tCO2e/yr avoided; coal-heavy grid displacement",
    ),
    dict(
        project_id    = "Hydro_EU",
        country       = "DE",
        region        = "Europe",
        sector        = "Energy",
        capex_usd     = 2_000_000,
        avoided_co2   = 6_126,
        revenue_yield = 0.10,
        opex_ratio    = 0.04,
        bond_years    = 5,
        project_years = 20,
        wacc_base     = 0.060,
        scenario      = "SSP2-4.5",
        notes         = "Small efficiency tweak; 6,126 tCO2e/yr avoided; European low-carbon grid",
    ),
]

# ─────────────────────────────────────────────────────────────────
# Load template notebook
# ─────────────────────────────────────────────────────────────────
with open(TEMPLATE) as f:
    template = json.load(f)

def make_params_cell(p: dict) -> str:
    """Generate a replacement params cell source for project p."""
    capex_m = p["capex_usd"] / 1e6
    return textwrap.dedent(f"""\
        # ══════════════════════════════════════════════════════════════════
        # PARAMETERS  ← auto-generated for {p['project_id']}
        # {p['notes']}
        # ══════════════════════════════════════════════════════════════════
        from pathlib import Path

        # ── Project / IO parameters ───────────────────────────────────────
        CAPEX_USD    = {p['capex_usd']:_}       # Project CAPEX (USD)
        COUNTRY      = "{p['country']}"              # ISO-2 / broad region → REGION_TO_ISO3
        SECTOR       = "{p['sector']}"        # IO sector key
        DATABASE     = "exiobase"
        SCENARIO     = "{p['scenario']}"       # default SSP scenario
        FOCUS_YEAR   = 2030
        # Notebooks live in integrated_finance/ (one level below project_assessment/)
        RESULTS_DIR  = Path("../results")       # → project_assessment/results/
        REPO_ROOT    = Path(".").resolve().parent.parent  # → tvp5/
        TOP_N        = 5

        # ── Integrated finance parameters ────────────────────────────────
        BOND_YEARS         = {p['bond_years']}          # Bond lifetime (years)
        PROJECT_YEARS      = {p['project_years']}          # Operational lifetime (years)
        WACC_BASE          = {p['wacc_base']:.3f}       # Base WACC
        REVENUE_YIELD      = {p['revenue_yield']:.2f}        # Annual revenue fraction of CAPEX
        OPEX_RATIO         = {p['opex_ratio']:.2f}        # Annual OPEX fraction of CAPEX

        ANNUAL_AVOIDED_CO2_tCO2e = {p['avoided_co2']:_}   # tCO2e / year (0 if N/A)

        ESG_MAX_DISCOUNT   = 0.0010      # 10 bps maximum WACC sustainability discount

        print(f"Project          : {p['project_id']}")
        print(f"Bond lifetime    : {{BOND_YEARS}} years")
        print(f"Project lifetime : {{PROJECT_YEARS}} years")
        print(f"CAPEX            : ${{CAPEX_USD/1e6:.1f}} M")
        print(f"WACC base        : {{WACC_BASE*100:.2f}} %")
        print(f"Revenue yield    : {{REVENUE_YIELD*100:.1f}} % of CAPEX/yr")
        print(f"OPEX ratio       : {{OPEX_RATIO*100:.1f}} % of CAPEX/yr")
        print(f"Avoided CO\u2082      : {{ANNUAL_AVOIDED_CO2_tCO2e:,}} tCO\u2082e/yr")
    """)

def make_calib_cell(p: dict) -> str:
    """Generate calibration cell with the correct project_id."""
    proj_id   = p['project_id']
    capex_str = f"${p['capex_usd']/1e6:.1f} M"
    wacc_str  = f"{p['wacc_base']*100:.1f}%"
    region    = p['region']

    # Build the HTML separately to avoid nested triple-quote conflicts
    html_rows = (
        f"<tr class='ok'>"
        f"<td>CAPEX (USD)</td><td>{capex_str}</td>"
        f"<td>modeled_input_data input CSV</td>"
        f"<td>OK &#8212; direct from input data</td></tr>\n"
        f"<tr class='ok'>"
        f"<td>WACC_BASE</td><td>{wacc_str}</td>"
        f"<td>Sector/region risk-adjusted; infra WACC 5&#8211;9%</td>"
        f"<td>OK &#8212; region-adjusted for {region}</td></tr>\n"
        "<tr class='warn'>"
        "<td>SCC &#8212; GHG (c_ghg)</td><td>WifOR GHG_BASE @ 2030 (~$105/tCO&#8322;e)</td>"
        "<td>IPCC AR6 WG3 central: $171/tCO&#8322;e; Paris-aligned: ~$115/tCO&#8322;e</td>"
        "<td>CONSERVATIVE &#8212; 38&#8211;61% of IPCC central; outputs are lower bounds</td></tr>\n"
        "<tr class='err'>"
        "<td>Legal risk (L_legal)</td><td>Not modelled</td>"
        "<td>Wetzer et al. (Science 383:152, 2024)</td>"
        "<td>GAP &#8212; understates downside risk</td></tr>"
    )
    html_block = (
        "<h3>Plausibility Check &#8212; "
        + proj_id +
        " vs Portfolio Data &amp; Literature</h3>\n"
        "<style>\n"
        ".plaus td, .plaus th { padding:5px 10px; border:1px solid #ccc; font-size:13px; }\n"
        ".plaus th { background:#2c3e50; color:#fff; }\n"
        ".plaus .ok  { background:#d5f5e3; }\n"
        ".plaus .warn{ background:#fdebd0; }\n"
        ".plaus .err { background:#fadbd8; }\n"
        "</style>\n"
        "<table class='plaus'>\n"
        "<tr><th>Parameter</th><th>Notebook value</th><th>Source</th><th>Status</th></tr>\n"
        + html_rows +
        "\n</table>"
    )

    # Use repr() so the HTML string embeds cleanly as a Python literal
    html_repr = repr(html_block)

    lines = [
        f"# {'='*66}",
        f"# CALIBRATION -- Real portfolio data vs modelled parameters",
        f"# Project: {proj_id}",
        f"# {'='*66}",
        "import pathlib, warnings",
        "import pandas as pd",
        "from IPython.display import display, HTML",
        "",
        "_BASE    = pathlib.Path('..')  # integrated_finance/ → project_assessment/",
        f"PROJ_ID  = '{proj_id}'",
        "YEAR_CAL = 2030",
        "",
        "# -- Load scenario adjustment factors ---------------------------------",
        "try:",
        "    sa = pd.read_csv(_BASE / 'results/scenario_adjustment.csv')",
        "    sa_proj = sa[",
        "        (sa['project_id'] == PROJ_ID) &",
        "        (sa['year'] == YEAR_CAL)",
        "    ][['scenario','adj_ratio_ghg','adj_ratio_employment','adj_ratio_water']].copy()",
        "    sa_proj.columns = ['SSP','adj_ghg','adj_employment','adj_water']",
        "    sa_proj = sa_proj.sort_values('SSP').reset_index(drop=True)",
        "    print(f'Scenario adjustment factors  --  {PROJ_ID} @ year {YEAR_CAL}:')",
        "    display(sa_proj.to_html(index=False, float_format=lambda x: f'{x:.4f}'))",
        "except FileNotFoundError:",
        "    warnings.warn('scenario_adjustment.csv not found -- skipping')",
        "    sa_proj = pd.DataFrame()",
        "",
        "# -- Load dependency summary ------------------------------------------",
        "try:",
        "    ds = pd.read_csv(_BASE / 'results/dependency_summary.csv')",
        "    ds_proj = ds[ds['project_id'] == PROJ_ID]",
        "    if ds_proj.empty:",
        "        ds_proj = ds.head(1)",
        "    cols = ['project_id','wrf_physical','wrf_composite','brf_composite',",
        "            'overall_high_risk','revenue_at_risk_usd_m','top_dependency']",
        "    cols = [c for c in cols if c in ds_proj.columns]",
        "    print(f'\\nNature-dependency scores  --  {PROJ_ID}:')",
        "    display(ds_proj[cols].to_html(index=False))",
        "except FileNotFoundError:",
        "    warnings.warn('dependency_summary.csv not found -- skipping')",
        "    ds_proj = pd.DataFrame()",
        "",
        "# -- Plausibility check HTML table ------------------------------------",
        f"_html = {html_repr}",
        "display(HTML(_html))",
        "",
        "# -- WifOR H5 value factors for this project -------------------------",
        "try:",
        "    import sys as _sys",
        "    _sys.path.insert(0, str(_BASE.resolve()))",
        "    from assess import VF_FILE_SPECS, _resolve_wifor_dir, _load_vf_coeff, REGION_TO_ISO3, PROJECT_SECTOR_TO_NACE",
        f"    _sec  = '{p['sector']}'",
        f"    _reg  = '{p['region']}'",
        "    _iso3 = REGION_TO_ISO3.get(_reg, 'DEU')",
        "    _nace = PROJECT_SECTOR_TO_NACE.get(_sec, 'Q')",
        "    _VF_DIR = _resolve_wifor_dir()",
        "    if _VF_DIR:",
        "        _vf_rows = []",
        "        for _key, _lbl, _unit in [",
        "            ('ghg',       'GHG BASE (Nordhaus DICE)', 'USD/kg'),",
        "            ('ghg_paris', 'GHG PARIS-aligned',        'USD/kg'),",
        "            ('water',     'Water (Blue Consumption)', 'USD/m3'),",
        "            ('training',  'Training / Employment',    'USD/h'),",
        "        ]:",
        "            _spec = {**VF_FILE_SPECS[_key], 'year': str(YEAR_CAL)}",
        "            _v = _load_vf_coeff(_spec, _VF_DIR, _iso3, _nace)",
        "            _eq = f'${abs(_v)*1000:.2f}/t' if _key.startswith('ghg') and _v else '-'",
        "            _vf_rows.append(f'<tr><td>{_lbl}</td><td>{_iso3}/{_nace}</td>'",
        "                            f'<td>{_v:.6f} {_unit}</td><td>{_eq}</td></tr>')",
        f"        _vf_html = ('<h4>WifOR H5 Value Factors &mdash; {proj_id} @ ' + str(YEAR_CAL) + '</h4>'",
        "                    '<style>.vft td,.vft th{padding:4px 10px;border:1px solid #ccc;font-size:12px}'",
        "                    '.vft th{background:#34495e;color:#fff}</style>'",
        "                    \"<table class='vft'><tr><th>Factor</th><th>Country/NACE</th>\"",
        "                    '<th>Coefficient</th><th>Per-tonne equiv</th></tr>'",
        "                    + ''.join(_vf_rows) + '</table>')",
        "        display(HTML(_vf_html))",
        "    else:",
        "        print('WifOR H5 directory not found -- value factor table skipped')",
        "except Exception as _e:",
        "    print(f'Value factor table skipped: {_e}')",
    ]
    return "\n".join(lines) + "\n"

# ─────────────────────────────────────────────────────────────────
# Generate one notebook per project
# ─────────────────────────────────────────────────────────────────
generated = []

for p in PROJECTS:
    nb = copy.deepcopy(template)
    cells = nb["cells"]

    # Clear all execution outputs so the notebook opens clean
    for c in cells:
        if c["cell_type"] == "code":
            c["outputs"] = []
            c["execution_count"] = None

    # ── Update title cell [0] ────────────────────────────────────
    old_title = "".join(cells[0]["source"])
    new_title = old_title.replace(
        "# Integrated Finance Analysis",
        f"# Integrated Finance Analysis — {p['project_id']}"
    ).replace(
        "> **Note on SCC:**",
        f"> **Project:** {p['project_id']} | {p['sector']} | {p['region']} "
        f"| CAPEX ${p['capex_usd']/1e6:.1f} M | Avoided CO\u2082: "
        f"{p['avoided_co2']:,} tCO\u2082e/yr  \n"
        "> **Note on SCC:**"
    )
    cells[0]["source"] = [new_title]

    # ── Replace params cell [1] ──────────────────────────────────
    cells[1]["source"] = [make_params_cell(p)]

    # ── Replace calibration cell [2] ────────────────────────────
    cells[2]["source"] = [make_calib_cell(p)]

    # ── Write output notebook ────────────────────────────────────
    out_path = OUT_DIR / f"integrated_finance_{p['project_id']}.ipynb"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    generated.append((p["project_id"], out_path))
    print(f"  Written: {out_path.name}")

print(f"\nTotal: {len(generated)} notebooks in {OUT_DIR}/")
