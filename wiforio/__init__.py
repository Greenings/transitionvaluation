"""
wiforio
═══════════════════════════════════════════════════════════════════════════════
Supply-chain tier impact library for the WifORIO MRIO database.

WifORIO (Wif OR Input-Output) is a full Multi-Region Input-Output table
built by WifOR Institute, covering all countries × NACE Rev. 2 sectors
with historical years 2010–2022 (FIGARO base) and scenario projections
for 2030, 2050, 2100 under SSP2 and SSP5 pathways.

Quick start
───────────
    from wiforio import make_project_spend_vector, total_impact
    import pandas as pd

    A = pd.read_hdf("path/to/MacroFile.h5", key="Aspill2050")

    y0 = make_project_spend_vector(
        invest_usd   = 1_850_000_000 * 1.09,
        project_type = "Rail_Dev",
        country      = "DE",
        index        = A.index,
    )

    result = total_impact(y0, "path/to/MacroFile.h5", year="2050")
    print(result["total"])
    print(result["by_region"])

Data sources and licences
──────────────────────────
    from wiforio import print_license_summary
    print_license_summary()
"""

__version__ = "0.1.0"
__author__  = "Daniel Croner, Frank Pertermann, Dimitrij Euler (WifOR Institute)"

from wiforio.io_lib import (
    tier0_impact,
    tier1_impact,
    tier_impact,
    total_impact,
    compare_models,
    list_variables,
    list_countries,
    list_nace_codes,
    load_macrofile_info,
    clear_cache,
)

from wiforio.alloc import (
    make_spend_vector,
    make_project_spend_vector,
    aggregate_to_sectors8,
    NACE_ALLOC,
    SECTORS8_TO_NACE,
    NACE_TO_SECTOR8,
)

from wiforio.sources import (
    SOURCES,
    print_license_summary,
    get_citation,
    check_compliance,
    all_citations,
)

__all__ = [
    "tier0_impact", "tier1_impact", "tier_impact", "total_impact",
    "compare_models",
    "list_variables", "list_countries", "list_nace_codes",
    "load_macrofile_info", "clear_cache",
    "make_spend_vector", "make_project_spend_vector",
    "aggregate_to_sectors8",
    "NACE_ALLOC", "SECTORS8_TO_NACE", "NACE_TO_SECTOR8",
    "SOURCES", "print_license_summary", "get_citation",
    "check_compliance", "all_citations",
]
