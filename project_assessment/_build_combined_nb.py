"""
Build investment_analysis.ipynb by merging investment_sankey.ipynb
and investment_dependency.ipynb into a single notebook.

Strategy
--------
- Shared infrastructure cells (params, imports, IO, scenario+dep, legend)
  come from the dep notebook (it is a strict superset).
- IO cell: dep's version (t2_raw/t3_raw) + aliases at the end so sankey
  sections (which use t2_df_raw / t3_df_raw / COLS) still work.
- Section cells come first from sankey (S1-S7) then from dep (S8-S14),
  with section-number comments updated throughout.
"""

import json
import re
from pathlib import Path

PA = Path(__file__).parent

with open(PA / "investment_sankey.ipynb") as f:
    sn = json.load(f)
with open(PA / "investment_dependency.ipynb") as f:
    dp = json.load(f)


# ── helpers ──────────────────────────────────────────────────────────────────

def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }


def md_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source,
    }


def src(nb, idx: int) -> str:
    return "".join(nb["cells"][idx]["source"])


def renumber_section(text: str, old: int, new: int) -> str:
    """Replace 'SECTION <old>' with 'SECTION <new>' in comment headers."""
    return re.sub(
        rf"(#\s*SECTION\s*){old}(\s*[—–-])",
        rf"\g<1>{new}\2",
        text,
    )


# ── Cell 0: title ─────────────────────────────────────────────────────────────

title = md_cell(
    "# Investment Supply-Chain & Nature Dependency Analysis\n\n"
    "Combines IO-based supply-chain footprint (Sankey / waterfall / scenario "
    "comparison) with a three-layer nature dependency overlay "
    "(ENCORE materiality · WWF Risk Filter · supply-chain sector sensitivity). "
    "Edit the **PARAMETERS** cell then **Run All**."
)

# ── Cell 1: params (dep version — superset) ───────────────────────────────────

params = code_cell(src(dp, 1))

# ── Cell 2: imports (dep version — superset) ──────────────────────────────────

imports = code_cell(src(dp, 2))

# ── Cell 3: IO analysis ───────────────────────────────────────────────────────
# Use the dep version (t2_raw / t3_raw, richer print table) and append aliases
# so sankey section cells (which use t2_df_raw / t3_df_raw / COLS) still work.

io_base = src(dp, 3)
io_aliases = (
    "\n"
    "# ── Aliases so sankey sections (S1-S7) work alongside dep sections (S8-S14)\n"
    "t2_df_raw = t2_raw\n"
    "t3_df_raw = t3_raw\n"
    "COLS      = COLS_SC\n"
)
io_cell = code_cell(io_base + io_aliases)

# ── Cell 4: scenario + dependency setup (dep version) ─────────────────────────

scenario_dep = code_cell(src(dp, 4))

# ── Cell 5: legend (dep version — includes ENCORE sector) ─────────────────────

legend = code_cell(src(dp, 5))

# ── Cells 6-12: Supply-chain sections (from sankey, sections 1-7) ─────────────

sankey_sections = []
for orig_num, cell_idx in enumerate(range(6, 13), start=1):
    cell_src = src(sn, cell_idx)
    # The section numbers in the sankey are already 1-7; keep them.
    # Just add a top-level group comment if the first section.
    if orig_num == 1:
        cell_src = (
            "# ══════════════════════════════════════════════════════════════════\n"
            "# PART A — SUPPLY-CHAIN FOOTPRINT  (Sections 1–7)\n"
            "# ══════════════════════════════════════════════════════════════════\n\n"
            + cell_src
        )
    sankey_sections.append(code_cell(cell_src))

# ── Cells 13-19: Nature dependency sections (from dep, sections 1-7 → 8-14) ───

dep_sections = []
for orig_num, cell_idx in enumerate(range(6, 13), start=1):
    cell_src = src(dp, cell_idx)
    new_num  = orig_num + 7        # 1→8, 2→9, …, 7→14
    cell_src = renumber_section(cell_src, orig_num, new_num)
    if orig_num == 1:
        cell_src = (
            "# ══════════════════════════════════════════════════════════════════\n"
            "# PART B — NATURE DEPENDENCY OVERLAY  (Sections 8–14)\n"
            "# ══════════════════════════════════════════════════════════════════\n\n"
            + cell_src
        )
    dep_sections.append(code_cell(cell_src))

# ── Assemble notebook ─────────────────────────────────────────────────────────

cells = (
    [title, params, imports, io_cell, scenario_dep, legend]
    + sankey_sections
    + dep_sections
)

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3.10.0"},
    },
    "cells": cells,
}

out = PA / "investment_analysis.ipynb"
with open(out, "w") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Written: {out}  ({out.stat().st_size:,} bytes, {len(cells)} cells)")
for i, c in enumerate(cells):
    src_text = "".join(c["source"])
    first = next(
        (l.strip() for l in src_text.split("\n")
         if l.strip() and "══" not in l and "──" not in l),
        src_text[:60],
    )
    print(f"  Cell {i:2d} [{c['cell_type']:8s}]  {first[:90]}")
