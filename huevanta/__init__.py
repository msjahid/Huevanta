"""
huevanta
========
Three beautiful Matplotlib themes — Rosé Pine, Dracula, Palenight —
each with 20 hand-crafted colour variants, 20 unique accent colours each.

Quick start
-----------
>>> import huevanta as hv
>>> hv.info()                           # full reference
>>> hv.rosepine.apply("moon")
>>> pal = hv.rosepine.palette("moon")  # list of 20 unique hex colours
"""

from .themes import rosepine, dracula, palenight, _BUNDLED_FONTS

__version__ = "0.1"
__author__  = "Jahid Hasan"
__all__ = ["rosepine", "dracula", "palenight"]


def info():
    """
    Print a full reference of:
      - how many themes
      - each theme name + how many variants
      - every variant name per theme
      - all available fonts

    >>> import huevanta as ts
    >>> hv.info()
    """
    div = "=" * 56

    print(div)
    print(f"  huevanta v{__version__}  —  by {__author__}")
    print(div)

    # ── 1. themes summary ────────────────────────────────────────────────
    themes = [
        ("rosepine",   rosepine),
        ("dracula",    dracula),
        ("palenight",  palenight),
    ]

    print(f"\n  Total themes : {len(themes)}")
    print()
    for name, cls in themes:
        print(f"  hv.{name:<12}  →  {len(cls.VARIANTS)} variants")

    # ── 2. variants per theme ────────────────────────────────────────────
    for name, cls in themes:
        print(f"\n  {'─'*54}")
        print(f"  hv.{name}  —  {len(cls.VARIANTS)} variants")
        print(f"  {'─'*54}")
        for i, v in enumerate(cls.VARIANTS, 1):
            print(f"    {i:>2}.  {v}")

    # ── 3. fonts ─────────────────────────────────────────────────────────
    print(f"\n  {'─'*54}")
    print(f"  Bundled fonts  —  {len(_BUNDLED_FONTS)} available")
    print(f"  {'─'*54}")
    for i, (name, filename) in enumerate(_BUNDLED_FONTS.items(), 1):
        print(f"    {i:>2}.  {name:<18}  →  {filename}")

    # ── 4. quick usage ───────────────────────────────────────────────────
    print(f"\n  {'─'*54}")
    print(f"  apply() parameters")
    print(f"  {'─'*54}")
    params = [
        ("variant",        "e.g. \"moon\", \"classic\", \"nebula\""),
        ("font",           "e.g. \"jetbrains\", \"fira_code\", \"hack\""),
        ("font_size_base", "int  — default 13"),
        ("font_weight",    "\"normal\" | \"bold\" | \"light\""),
        ("grid",           "False | True | \"x\" | \"y\""),
        ("font_color",     "#rrggbb  — overrides all text"),
        ("label_color",    "#rrggbb  — axis labels & title only"),
        ("tick_color",     "#rrggbb  — tick labels only"),
    ]
    for param, desc in params:
        print(f"    {param:<18}  {desc}")

    print(f"\n{div}\n")