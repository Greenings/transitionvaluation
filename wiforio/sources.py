"""
wiforio/sources.py
─────────────────────────────────────────────────────────────────────────────
Metadata, citations, and licence information for every external data source
that feeds into the WifORIO MRIO database.

Use ``print_license_summary()`` for a quick compliance overview, or access
``SOURCES[key]`` for programmatic use.
"""

from __future__ import annotations

# ─────────────────────────────────────────────────────────────────────────────
# Source catalogue
# ─────────────────────────────────────────────────────────────────────────────

SOURCES: dict[str, dict] = {

    # ── 1. FIGARO ────────────────────────────────────────────────────────────
    "figaro": {
        "name": "FIGARO",
        "full_name": (
            "Full International and Global Accounts for Research "
            "in Input-Output analysis"
        ),
        "provider": "Eurostat / European Commission",
        "version": "24th edition (reference year 2022)",
        "years_covered": "2010–2022",
        "url": (
            "https://ec.europa.eu/eurostat/web/"
            "esa-supply-use-input-tables/information-data"
        ),
        "license": "CC BY 4.0",
        "license_url": "https://ec.europa.eu/eurostat/help/copyright-notice",
        "attribution_required": True,
        "attribution_text": (
            "Source: Eurostat, FIGARO — Full International and Global "
            "Accounts for Research in Input-Output analysis, 24th edition."
        ),
        "commercial_use": True,
        "redistribution": True,
        "share_alike": False,
        "role_in_wiforio": (
            "Base transaction matrix (Tindirect / Z matrix). Provides the "
            "initial industry-by-industry IO table for 46 regions × 64 NACE "
            "sectors for years 2010–2022. All monetary flows in the WifORIO "
            "base table originate from FIGARO before KRAS rebalancing. "
            "Satellite accounts (D1, D21X31, D29X39, B2A3G) also sourced "
            "here."
        ),
        "citation": (
            "Eurostat (2024). FIGARO: Full International and Global Accounts "
            "for Research in Input-Output analysis, 24th edition. European "
            "Commission. "
            "https://ec.europa.eu/eurostat/web/"
            "esa-supply-use-input-tables/information-data"
        ),
        "doi": None,
        "notes": (
            "FIGARO is the methodological backbone of WifORIO. It covers "
            "EU-27 member states, the UK, Switzerland, Norway, Turkey, and "
            "12 major non-EU trading partners (AR, AU, BR, CA, CN, ID, IN, "
            "JP, KR, MX, RU, SA, US, ZA) plus a Rest-of-World aggregate."
        ),
    },

    # ── 2. Eurostat NAIO (national accounts constraints) ─────────────────────
    "eurostat_naio": {
        "name": "Eurostat NAIO",
        "full_name": (
            "Eurostat National Accounts Input-Output tables "
            "(NAIO_10_FCP_II3 Gross Output; NAIO_10_FCP_II4 "
            "Intermediate Consumption)"
        ),
        "provider": "Eurostat / European Commission",
        "version": "Annual release 2024",
        "years_covered": "2010–2024",
        "url": "https://ec.europa.eu/eurostat/web/national-accounts/data/database",
        "license": "CC BY 4.0",
        "license_url": "https://ec.europa.eu/eurostat/help/copyright-notice",
        "attribution_required": True,
        "attribution_text": "Source: Eurostat, National Accounts (NAIO), accessed 2025.",
        "commercial_use": True,
        "redistribution": True,
        "share_alike": False,
        "role_in_wiforio": (
            "Row and column constraints for the KRAS balancing procedure. "
            "Gross output (GO) and intermediate consumption (IC) by NACE "
            "sector and EU member state provide the most reliable anchors for "
            "rebalancing the FIGARO base table to national accounting totals. "
            "Used for 2010–2024; forecast years use IMF WEO growth rates."
        ),
        "citation": (
            "Eurostat (2025). National Accounts Input-Output tables "
            "(NAIO_10_FCP_II3, NAIO_10_FCP_II4). European Commission. "
            "https://ec.europa.eu/eurostat/web/national-accounts/data/database"
        ),
        "doi": None,
        "notes": (
            "Liechtenstein, Monaco and some micro-states have restricted "
            "commercial redistribution rights under Eurostat's licence. "
            "These countries are either excluded or imputed in WifORIO."
        ),
    },

    # ── 3. UN SNA ─────────────────────────────────────────────────────────────
    "un_sna": {
        "name": "UN SNA",
        "full_name": "United Nations System of National Accounts",
        "provider": "United Nations Statistics Division (UNSD)",
        "version": "2018 SNA framework; data through 2023",
        "years_covered": "2010–2023",
        "url": "https://unstats.un.org/unsd/nationalaccount/data.asp",
        "license": "UN open data (public domain)",
        "license_url": "https://www.un.org/en/about-us/terms-of-use",
        "attribution_required": True,
        "attribution_text": (
            "Source: United Nations Statistics Division, National Accounts "
            "Main Aggregates Database."
        ),
        "commercial_use": True,
        "redistribution": True,
        "share_alike": False,
        "role_in_wiforio": (
            "Supplementary gross output and intermediate consumption "
            "constraints for non-EU / non-OECD countries not covered by "
            "Eurostat NAIO. Particularly important for LATAM, Africa, and "
            "Asia-Pacific countries in the Own Table 2.0 extension. "
            "Used alongside Eurostat data in the KRAS constraint set."
        ),
        "citation": (
            "United Nations Statistics Division (2025). National Accounts "
            "Main Aggregates Database. "
            "https://unstats.un.org/unsd/nationalaccount/data.asp"
        ),
        "doi": None,
        "notes": (
            "UN SNA terms of use permit free use and redistribution with "
            "attribution. The UN makes no warranty on data accuracy for "
            "individual country submissions."
        ),
    },

    # ── 4. IMF WEO ────────────────────────────────────────────────────────────
    "imf_weo": {
        "name": "IMF WEO",
        "full_name": "International Monetary Fund World Economic Outlook",
        "provider": "International Monetary Fund (IMF)",
        "version": "October 2022 edition (WEOOct2022)",
        "years_covered": "Forecast 2023–2029",
        "url": "https://www.imf.org/en/Publications/WEO",
        "license": "IMF copyright — restricted fair use",
        "license_url": "https://www.imf.org/en/about/copyright-and-terms",
        "attribution_required": True,
        "attribution_text": (
            "Source: International Monetary Fund, World Economic Outlook "
            "Database, October 2022."
        ),
        "commercial_use": False,
        "redistribution": False,
        "share_alike": False,
        "role_in_wiforio": (
            "GDP growth rates used to project the FIGARO base table forward "
            "from the last historical year (2022) through 2029. IMF WEO "
            "provides GDP forecasts for ~190 countries in current USD and "
            "constant prices, applied as factorial constraints in KRAS for "
            "the gross output rows. Replaced by IPCC SSP scenarios for "
            "2030/2050/2100 projections."
        ),
        "citation": (
            "International Monetary Fund (2022). World Economic Outlook "
            "Database, October 2022. IMF. "
            "https://www.imf.org/en/Publications/WEO/weo-database/2022/October"
        ),
        "doi": None,
        "notes": (
            "IMPORTANT: IMF data is copyright protected. Fair use is limited "
            "to excerpts of up to 1,000 words or one quarter of content "
            "(whichever is less) for NON-COMMERCIAL purposes only. "
            "Commercial use requires written permission from copyright@imf.org. "
            "WifORIO models that use IMF WEO growth rates for commercial "
            "products must obtain IMF permission or replace this source."
        ),
    },

    # ── 5. World Bank ─────────────────────────────────────────────────────────
    "worldbank": {
        "name": "World Bank",
        "full_name": (
            "World Bank World Development Indicators — "
            "GDP and Gross Value Added by sector"
        ),
        "provider": "World Bank Group",
        "version": "March 2025 update",
        "years_covered": "2010–2024",
        "url": "https://databank.worldbank.org/source/world-development-indicators",
        "license": "CC BY 4.0",
        "license_url": "https://datacatalog.worldbank.org/public-licenses",
        "attribution_required": True,
        "attribution_text": (
            "Source: World Bank, World Development Indicators, "
            "GDP and GVA series, 2025."
        ),
        "commercial_use": True,
        "redistribution": True,
        "share_alike": False,
        "role_in_wiforio": (
            "GDP (NY.GDP.MKTP.CD) and sectoral GVA data used as auxiliary "
            "constraints in KRAS, particularly for countries with limited "
            "national accounts coverage. Also used to construct the bilateral "
            "gravity model for Own Table 2.0 country extension (GDP as "
            "economic mass). GVA by broad sector constrains the value-added "
            "satellite account."
        ),
        "citation": (
            "World Bank (2025). World Development Indicators. The World Bank "
            "Group. https://databank.worldbank.org"
        ),
        "doi": None,
        "notes": (
            "CC BY 4.0 — fully open for commercial and non-commercial use "
            "with attribution. Preferred source for GDP-based constraints "
            "given global coverage and open licence."
        ),
    },

    # ── 6. BACI ───────────────────────────────────────────────────────────────
    "baci": {
        "name": "BACI",
        "full_name": (
            "Base pour l'Analyse du Commerce International — "
            "CEPII International Trade Database"
        ),
        "provider": "CEPII (Centre d'Études Prospectives et d'Informations Internationales)",
        "version": "HS 2017 revision, 2024 release",
        "years_covered": "2010–2023 (goods trade)",
        "url": "http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37",
        "license": "Etalab 2.0 (French open data licence)",
        "license_url": "https://www.etalab.gouv.fr/wp-content/uploads/2018/11/open-licence.pdf",
        "attribution_required": True,
        "attribution_text": (
            "Source: CEPII, BACI International Trade Database. "
            "Gaulier, G. & Zignago, S. (2010). BACI: International Trade "
            "Database at the Product-Level. CEPII Working Paper N°2010-23."
        ),
        "commercial_use": True,
        "redistribution": True,
        "share_alike": False,
        "role_in_wiforio": (
            "Bilateral trade flows in goods (HS product codes reconciled to "
            "NACE via concordance tables). Used to construct the trade weight "
            "matrix TW, which distributes each row's imports across sourcing "
            "countries in the KRAS framework. BACI reconciles UN Comtrade "
            "mirror flows, providing a more consistent set of bilateral trade "
            "data than raw Comtrade."
        ),
        "citation": (
            "Gaulier, G. and Zignago, S. (2010). BACI: International Trade "
            "Database at the Product-Level. The 1994-2007 Version. CEPII "
            "Working Paper, N°2010-23. http://www.cepii.fr/CEPII/en/"
            "bdd_modele/bdd_modele_item.asp?id=37"
        ),
        "doi": None,
        "notes": (
            "Etalab 2.0 is functionally equivalent to CC BY 4.0 and permits "
            "commercial use, redistribution, and adaptation with attribution."
        ),
    },

    # ── 7. UN Comtrade ────────────────────────────────────────────────────────
    "un_comtrade": {
        "name": "UN Comtrade",
        "full_name": "United Nations Comtrade Database (services trade)",
        "provider": "United Nations Statistics Division",
        "version": "API v2 — 2024 access",
        "years_covered": "2017–2022 (services)",
        "url": "https://comtradeplus.un.org/",
        "license": "Proprietary — restricted use",
        "license_url": "https://comtrade.un.org/licenseagreement.html",
        "attribution_required": True,
        "attribution_text": "Source: UN Comtrade Database, United Nations.",
        "commercial_use": False,
        "redistribution": False,
        "share_alike": False,
        "role_in_wiforio": (
            "Bilateral trade flows in services (BPM6 classification mapped "
            "to NACE service sectors). Used as a complement to BACI (goods) "
            "for sectors J–N, constructing bilateral service import weights "
            "in the TW constraint matrix. Covers EBOPS categories: "
            "transport, travel, financial, insurance, ICT, other business "
            "services, government."
        ),
        "citation": (
            "United Nations Statistics Division (2024). UN Comtrade Database. "
            "https://comtradeplus.un.org/"
        ),
        "doi": None,
        "notes": (
            "IMPORTANT: UN Comtrade is subject to a restricted licence. "
            "Automated downloading, bulk redistribution, and commercial "
            "exploitation are strictly prohibited without prior written "
            "permission from comtrade@un.org. WifORIO uses this data for "
            "research purposes only. Any commercial application must either "
            "obtain Comtrade permission or substitute with an open-licensed "
            "services trade source (e.g. OECD TiVA service trade data, "
            "available under CC BY 4.0)."
        ),
    },

    # ── 8. IPCC AR6 SSP scenarios ─────────────────────────────────────────────
    "ipcc_ar6": {
        "name": "IPCC AR6 SSP",
        "full_name": (
            "IPCC Sixth Assessment Report — Shared Socioeconomic Pathways "
            "(SSP) GDP and Population Projections"
        ),
        "provider": (
            "IPCC (Intergovernmental Panel on Climate Change) / "
            "IIASA SSP database"
        ),
        "version": "AR6 WG1/WG3 — scenario data release 2021",
        "years_covered": "2030, 2050, 2100 (scenario years)",
        "url": "https://www.ipcc.ch/report/ar6/wg1/resources/data-access/",
        "license": "CC BY 4.0",
        "license_url": "https://www.ipcc-data.org/",
        "attribution_required": True,
        "attribution_text": (
            "Source: IPCC, Sixth Assessment Report (AR6), SSP GDP and "
            "Population Projections. IPCC Data Distribution Centre."
        ),
        "commercial_use": True,
        "redistribution": True,
        "share_alike": False,
        "role_in_wiforio": (
            "Long-horizon GDP and population projections for SSP1–SSP5 "
            "scenarios, used to project WifORIO tables to 2030, 2050, and "
            "2100. GDP growth multipliers derived from SSP2 ('Middle of the "
            "Road') and SSP5 ('Fossil-Fuelled Development') drive the "
            "factorial constraints in KRAS for forecast years. Country-level "
            "SSP2 and SSP5 are the primary scenarios in the current WifORIO "
            "release."
        ),
        "citation": (
            "IPCC (2021). Sixth Assessment Report — Working Group I. "
            "Scenario Data. IPCC Data Distribution Centre. "
            "https://www.ipcc.ch/report/ar6/wg1/resources/data-access/\n"
            "\n"
            "O'Neill, B.C. et al. (2017). The roads ahead: Narratives for "
            "shared socioeconomic pathways describing world futures in the "
            "21st century. Global Environmental Change 42, 169–180. "
            "doi:10.1016/j.gloenvcha.2015.01.004"
        ),
        "doi": "10.1016/j.gloenvcha.2015.01.004",
        "notes": (
            "SSP scenarios are produced by the IIASA SSP scenario database "
            "(Keywan Riahi et al., 2017, Global Environmental Change) and "
            "distributed through the IPCC Data Distribution Centre. "
            "Registration is requested to track scientific use but is not "
            "legally required for access under CC BY 4.0."
        ),
    },

    # ── 9. CEPII Gravity ──────────────────────────────────────────────────────
    "cepii_gravity": {
        "name": "CEPII Gravity",
        "full_name": "CEPII Gravity Database (bilateral distances and trade costs)",
        "provider": "CEPII",
        "version": "2022 release (Conte, Cotterlaz & Mayer 2022)",
        "years_covered": "1948–2020",
        "url": "http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8",
        "license": "Etalab 2.0",
        "license_url": "https://www.etalab.gouv.fr/wp-content/uploads/2018/11/open-licence.pdf",
        "attribution_required": True,
        "attribution_text": (
            "Source: CEPII Gravity Database. Conte, M., P. Cotterlaz and "
            "T. Mayer (2022), 'The CEPII Gravity database', CEPII Working "
            "Paper N°2022-05."
        ),
        "commercial_use": True,
        "redistribution": True,
        "share_alike": False,
        "role_in_wiforio": (
            "Bilateral distances (simple, population-weighted, and port-to-"
            "port), contiguity, common language, colonial ties, and trade "
            "agreement indicators. Used in the gravity model underpinning the "
            "Own Table 2.0 extension — countries not in the FIGARO 46-region "
            "core are assigned trade shares proportional to their estimated "
            "bilateral trade potential, derived from CEPII gravity predictors "
            "scaled by World Bank GDP."
        ),
        "citation": (
            "Conte, M., P. Cotterlaz and T. Mayer (2022). The CEPII Gravity "
            "database. CEPII Working Paper N°2022-05. "
            "http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8"
        ),
        "doi": None,
        "notes": (
            "Etalab 2.0 permits commercial use with attribution. "
            "The gravity database is freely downloadable without registration."
        ),
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Utility functions
# ─────────────────────────────────────────────────────────────────────────────

def print_license_summary() -> None:
    """Print a compliance-oriented summary table of all data sources."""
    w = [22, 30, 12, 13]
    header = (
        f"{'Source':<{w[0]}} {'Licence':<{w[1]}} "
        f"{'Commercial':<{w[2]}} {'Redistribute':<{w[3]}}"
    )
    sep = "─" * sum(w) + "─" * 3

    print("\nWifORIO — Data Source Licence Summary")
    print("=" * (sum(w) + 3))
    print(header)
    print(sep)

    for key, src in SOURCES.items():
        com  = "YES" if src["commercial_use"]  else "NO ⚠"
        redi = "YES" if src["redistribution"]  else "NO ⚠"
        print(
            f"{src['name']:<{w[0]}} {src['license']:<{w[1]}} "
            f"{com:<{w[2]}} {redi:<{w[3]}}"
        )

    print(sep)
    print(
        "\n⚠  IMF WEO and UN Comtrade impose the most significant "
        "commercial-use restrictions.\n"
        "   For commercial applications, replace or obtain written "
        "permission from:\n"
        "     IMF WEO  → copyright@imf.org\n"
        "     Comtrade → comtrade@un.org\n"
    )


def get_citation(source_key: str) -> str:
    """Return the full citation string for a source key."""
    if source_key not in SOURCES:
        raise KeyError(
            f"Unknown source '{source_key}'. "
            f"Valid keys: {list(SOURCES.keys())}"
        )
    return SOURCES[source_key]["citation"]


def check_compliance(commercial: bool = False) -> list[str]:
    """
    Return a list of warnings for sources that restrict the requested use.

    Parameters
    ----------
    commercial : if True, also flag sources that prohibit commercial use.

    Returns a list of warning strings (empty = no issues).
    """
    warnings: list[str] = []
    for key, src in SOURCES.items():
        if commercial and not src["commercial_use"]:
            warnings.append(
                f"{src['name']} ({src['license']}): commercial use prohibited. "
                f"Contact: {src['license_url']}"
            )
        if not src["redistribution"]:
            warnings.append(
                f"{src['name']} ({src['license']}): redistribution of derived "
                f"data prohibited. Contact: {src['license_url']}"
            )
    return warnings


def all_citations() -> str:
    """Return a formatted reference list for all WifORIO data sources."""
    lines = ["WifORIO — Data Source Citations", "=" * 40, ""]
    for src in SOURCES.values():
        lines.append(src["citation"])
        lines.append("")
    return "\n".join(lines)
