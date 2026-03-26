"""
Huevanta.themes
===============
Three Matplotlib themes — Rosé Pine, Dracula, Palenight.

Each variant defines:
  • 6  structural keys  (base, surface, overlay, muted, subtle, text)
  • 20 accent keys      (a1 … a20)  — one unique colour per bar/line/patch

This means a 20-bar chart never repeats a colour.

API
---
  hv.rosepine.apply(variant)    hv.rosepine.palette(variant)    hv.rosepine.subplots(...)
  hv.dracula.apply(variant)     hv.dracula.palette(variant)     hv.dracula.subplots(...)
  hv.palenight.apply(variant)   hv.palenight.palette(variant)   hv.palenight.subplots(...)
"""

from __future__ import annotations
import warnings
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# 20 accent slot names — shared by every theme/variant
_A = [f"a{i}" for i in range(1, 21)]   # ["a1", "a2", ..., "a20"]

# ---------------------------------------------------------------------------
# Active theme state + auto-persistence hooks
# ---------------------------------------------------------------------------
_ACTIVE: dict = {}
_HOOK_CONNECTED = False


def _store_active(theme, variant, font, font_size_base, grid,
                  font_weight, font_color, label_color, tick_color):
    _ACTIVE.update(theme=theme, variant=variant, font=font,
                   font_size_base=font_size_base, grid=grid,
                   font_weight=font_weight, font_color=font_color,
                   label_color=label_color, tick_color=tick_color)
    _connect_hooks()


def _get_active_colors():
    if not _ACTIVE:
        return None
    return {"rosepine": _RP, "dracula": _DR, "palenight": _PN}[
        _ACTIVE["theme"]][_ACTIVE["variant"]]


def _connect_hooks():
    """
    Patch Figure and Axes creation so every figure/axes made anywhere
    (including inside seaborn) gets the active theme automatically.
    """
    global _HOOK_CONNECTED
    if _HOOK_CONNECTED:
        return

    # ── patch Figure.__init__ ────────────────────────────────────────────
    _orig_fig_init = mpl.figure.Figure.__init__

    def _fig_init(self, *args, **kwargs):
        _orig_fig_init(self, *args, **kwargs)
        c = _get_active_colors()
        if c is not None:
            self.patch.set_facecolor(c["base"])
            self.set_facecolor(c["base"])

    mpl.figure.Figure.__init__ = _fig_init

    # ── patch Figure.add_axes and Figure.add_subplot ─────────────────────
    # seaborn goes through these rather than Axes.__init__ directly
    _orig_add_axes    = mpl.figure.Figure.add_axes
    _orig_add_subplot = mpl.figure.Figure.add_subplot

    def _add_axes(self, *args, **kwargs):
        ax = _orig_add_axes(self, *args, **kwargs)
        c = _get_active_colors()   # always read fresh — never stale
        if c is not None:
            _apply_ax_theme(ax, self, c)
        return ax

    def _add_subplot(self, *args, **kwargs):
        ax = _orig_add_subplot(self, *args, **kwargs)
        c = _get_active_colors()   # always read fresh — never stale
        if c is not None:
            _apply_ax_theme(ax, self, c)
        return ax

    mpl.figure.Figure.add_axes    = _add_axes
    mpl.figure.Figure.add_subplot = _add_subplot

    _HOOK_CONNECTED = True


def reapply():
    """
    Re-apply the last Huevanta theme rcParams globally.

    Normally not needed since the auto-hook handles all figure/axes
    creation. Call this only if a library explicitly resets rcParams::

        hv.reapply()
    """
    if not _ACTIVE:
        raise RuntimeError(
            "[Huevanta] No theme applied yet. "
            "Call hv.rosepine.apply() / hv.dracula.apply() / hv.palenight.apply() first."
        )
    theme = _ACTIVE["theme"]
    kw = {k: v for k, v in _ACTIVE.items() if k != "theme"}
    {"rosepine": rosepine, "dracula": dracula, "palenight": palenight}[theme].apply(**kw)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Bundled fonts
# ---------------------------------------------------------------------------
#
# Two fonts are shipped inside  Huevanta/fonts/ :
#
#   "jetbrains"   JetBrainsMono-Regular.ttf   — modern monospace, great for data
#   "sourcecodepro"  SourceCodePro-Regular.otf  — classic monospace, warm & readable
#
# Usage:
#   hv.rosepine.apply("moon", font="jetbrains")       # bundled JetBrains Mono
#   hv.rosepine.apply("moon", font="sourcecodepro")   # bundled Source Code Pro
#   hv.rosepine.apply("moon", font="path/to/My.ttf")  # your own font file
#   hv.rosepine.apply("moon", font=None)              # Matplotlib default

_BUNDLED_FONTS = {
    "jetbrains":        "JetBrainsMono-Regular.ttf",
    "sourcecodepro":    "SourceCodePro-Regular.ttf",
    "cascadia":         "CascadiaCode.ttf",
    "fira_code":        "Fira Code Regular 400.ttf",
    "hack":             "Hack-Regular.ttf",
    "microsoft_sans":   "Microsoft Sans Serif.ttf",
    "operator_mono":    "Operator Mono Book Regular.otf",
    "roboto":           "Roboto-Regular.ttf",
}

_DEFAULT_FONT = "jetbrains"


def _resolve_font(font) -> str:
    """
    Resolve font argument to a Matplotlib font-family name.

    Parameters
    ----------
    font : str | None
        "jetbrains"      — bundled JetBrains Mono (default)
        "sourcecodepro"  — bundled Source Code Pro
        a file path      — any .ttf / .otf file on disk
        None             — Matplotlib default monospace
    """
    if font is None:
        return "monospace"

    fonts_dir = Path(__file__).parent / "fonts"

    # named bundled font
    if isinstance(font, str) and font.lower() in _BUNDLED_FONTS:
        p = fonts_dir / _BUNDLED_FONTS[font.lower()]
        if p.exists():
            fm.fontManager.addfont(str(p))
            return fm.FontProperties(fname=str(p)).get_name()
        warnings.warn(
            f"[Huevanta] Bundled font {p.name!r} not found. "
            f"Download it and place it in {fonts_dir}",
            stacklevel=3,
        )
        return "monospace"

    # custom file path
    p = Path(font)
    if p.exists():
        fm.fontManager.addfont(str(p))
        return fm.FontProperties(fname=str(p)).get_name()

    warnings.warn(f"[Huevanta] Font not found: {p}. Using monospace.", stacklevel=3)
    return "monospace"


def _apply_ax_theme(ax, fig, c):
    """
    Apply all theme colours directly to an axes object.
    Fixes Jupyter inline backend which ignores rcParams for
    figure background, spine colours and tick label colours.
    """
    # detect light vs dark theme for visible grid/spine colors
    _base_r = int(c["base"][1:3], 16)
    _base_g = int(c["base"][3:5], 16)
    _base_b = int(c["base"][5:7], 16)
    _is_light = (_base_r + _base_g + _base_b) > 382
    _grid_color = c["muted"] if _is_light else c["subtle"]

    # resolve font_color / label_color / tick_color from _ACTIVE
    def _rc(val, fallback):
        if val is None:
            return fallback
        if val in c:
            return c[val]
        return val

    _font_color  = _ACTIVE.get("font_color",  None) if _ACTIVE else None
    _label_color = _ACTIVE.get("label_color", None) if _ACTIVE else None
    _tick_color  = _ACTIVE.get("tick_color",  None) if _ACTIVE else None

    _text  = _rc(_font_color,  c["text"])
    _label = _rc(_label_color, _rc(_font_color, c["subtle"]))
    _tick  = _rc(_tick_color,  _rc(_font_color, c["subtle"]))

    fig.patch.set_facecolor(c["base"])
    ax.set_facecolor(c["surface"])
    ax.spines["left"].set_color(_grid_color)
    ax.spines["bottom"].set_color(_grid_color)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors=_tick)
    ax.xaxis.label.set_color(_label)
    ax.yaxis.label.set_color(_label)
    ax.title.set_color(_text)
    # enforce grid exactly as configured — seaborn enables grid by default
    # which overrides rcParams, so we must set it directly on the axes
    grid = _ACTIVE.get("grid", False) if _ACTIVE else False
    if grid is False or grid is None:
        ax.grid(False)
    elif grid is True:
        ax.grid(True, color=_grid_color, linewidth=0.6,
                linestyle="--", alpha=0.6)
    elif isinstance(grid, str):
        ax.grid(True, axis=grid, color=_grid_color,
                linewidth=0.6, linestyle="--", alpha=0.6)


def _build_rc(c, font_family, font_size_base, grid, cmap,
              font_weight, font_color, label_color, tick_color):
    """
    font_weight  : "normal" | "bold" | "light"  — applied globally
    font_color   : hex str | None  — overrides theme text colour for all text
    label_color  : hex str | None  — overrides axis label / title colour only
    tick_color   : hex str | None  — overrides tick label colour only
    """
    ts = round(font_size_base * 0.85)
    tt = round(font_size_base * 1.15)

    # resolve colour overrides — fall back to theme colours
    # also accept theme key names e.g. "text", "subtle", "a1", "a3" etc.
    def _resolve_color(val, fallback):
        if val is None:
            return fallback
        if val in c:          # e.g. "text", "muted", "a1", "a5" …
            return c[val]
        return val            # assume raw hex string

    _text   = _resolve_color(font_color,  c["text"])
    _label  = _resolve_color(label_color, _resolve_color(font_color, c["subtle"]))
    _tick   = _resolve_color(tick_color,  _resolve_color(font_color, c["subtle"]))

    # detect light theme — if base is bright (high R+G+B), use muted for
    # grid/spines so they're actually visible against the light background
    _base_r = int(c["base"][1:3], 16)
    _base_g = int(c["base"][3:5], 16)
    _base_b = int(c["base"][5:7], 16)
    _is_light = (_base_r + _base_g + _base_b) > 382  # ~50% brightness threshold
    _grid_color = c["muted"] if _is_light else c["subtle"]

    return {
        "figure.facecolor":      c["base"],
        "figure.edgecolor":      c["base"],
        "figure.dpi":            130,
        "axes.facecolor":        c["surface"],
        "axes.edgecolor":        _grid_color,
        "axes.labelcolor":       _label,
        "axes.titlecolor":       _text,
        "axes.titlesize":        tt,
        "axes.labelsize":        font_size_base,
        "axes.linewidth":        0.8,
        "axes.spines.top":       False,
        "axes.spines.right":     False,
        "axes.prop_cycle":       mpl.cycler(color=[c[k] for k in _A]),
        "axes.grid":             bool(grid),
        "axes.grid.axis":        grid if isinstance(grid, str) else "both",
        "axes.axisbelow":        True,
        "grid.color":            _grid_color,
        "grid.linewidth":        0.6,
        "grid.linestyle":        "--",
        "grid.alpha":            0.6,
        "xtick.color":           c["muted"],
        "ytick.color":           c["muted"],
        "xtick.labelcolor":      _tick,
        "ytick.labelcolor":      _tick,
        "xtick.labelsize":       ts,
        "ytick.labelsize":       ts,
        "xtick.major.size":      4,
        "ytick.major.size":      4,
        "xtick.minor.visible":   False,
        "ytick.minor.visible":   False,
        "legend.facecolor":      c["overlay"],
        "legend.edgecolor":      c["muted"],
        "legend.labelcolor":     _text,
        "legend.fontsize":       ts,
        "legend.title_fontsize": font_size_base,
        "legend.framealpha":     0.85,
        "legend.borderpad":      0.6,
        "lines.linewidth":       1.8,
        "lines.markersize":      6,
        "patch.edgecolor":       c["overlay"],
        "patch.linewidth":       0.5,
        "scatter.edgecolors":    "none",
        "text.color":            _text,
        "font.family":           font_family,
        "font.size":             font_size_base,
        "font.weight":           font_weight,
        "axes.titleweight":      font_weight,
        "axes.labelweight":      font_weight,
        "image.cmap":            cmap,
        "savefig.facecolor":     c["base"],
        "savefig.edgecolor":     c["base"],
        "savefig.bbox":          "tight",
        "savefig.dpi":           180,
    }


# ===========================================================================
#  ROSÉ PINE — 20 variants × 20 unique accent colours each
#  Flavour: soft, romantic, botanical — pinks · teals · golds · purples
# ===========================================================================

_RP = {
    "main": {
        "base": "#191724", "surface": "#1f1d2e", "overlay": "#26233a",
        "muted": "#6e6a86", "subtle": "#908caa", "text": "#e0def4",
        "a1": "#eb6f92", "a2": "#9ccfd8", "a3": "#f6c177", "a4": "#c4a7e7",
        "a5": "#31748f", "a6": "#ebbcba", "a7": "#e58c8a", "a8": "#56949f",
        "a9": "#f0a7c4", "a10": "#b4a0d4", "a11": "#d4a7c4", "a12": "#a0c8d4",
        "a13": "#e8c8a0", "a14": "#c0d4a8", "a15": "#a8b8d8", "a16": "#d8a8b8",
        "a17": "#a8c8b8", "a18": "#c8b8a0", "a19": "#b8a8c8", "a20": "#a0b8c0",
    },
    "moon": {
        "base": "#232136", "surface": "#2a273f", "overlay": "#393552",
        "muted": "#6e6a86", "subtle": "#908caa", "text": "#e0def4",
        "a1": "#eb6f92", "a2": "#9ccfd8", "a3": "#f6c177", "a4": "#c4a7e7",
        "a5": "#3e8fb0", "a6": "#ea9a97", "a7": "#f0a0c0", "a8": "#80c8d8",
        "a9": "#e8b890", "a10": "#b098d8", "a11": "#d0a0b8", "a12": "#90c0d0",
        "a13": "#f0d090", "a14": "#a8c8a0", "a15": "#a0b0d8", "a16": "#d8a0a8",
        "a17": "#a0c8b8", "a18": "#c8b898", "a19": "#b8a0c8", "a20": "#98b8c8",
    },
    "dawn": {
        "base": "#faf4ed", "surface": "#fffaf3", "overlay": "#f2e9de",
        "muted": "#9893a5", "subtle": "#797593", "text": "#575279",
        "a1": "#b4637a", "a2": "#56949f", "a3": "#ea9d34", "a4": "#907aa9",
        "a5": "#286983", "a6": "#d7827e", "a7": "#c86070", "a8": "#3d8f9e",
        "a9": "#d08828", "a10": "#7a6898", "a11": "#c87878", "a12": "#4a8a88",
        "a13": "#a87828", "a14": "#887898", "a15": "#c09080", "a16": "#508890",
        "a17": "#b89060", "a18": "#887090", "a19": "#b07878", "a20": "#608898",
    },
    "midnight": {
        "base": "#0d0b14", "surface": "#13101e", "overlay": "#1c1828",
        "muted": "#524d6a", "subtle": "#716c88", "text": "#ebe8fc",
        "a1": "#f07898", "a2": "#a2dce4", "a3": "#fad08a", "a4": "#ceaff0",
        "a5": "#4aa0b8", "a6": "#f2c8c6", "a7": "#e888b0", "a8": "#78d0e0",
        "a9": "#f8c070", "a10": "#b890e8", "a11": "#50b8c8", "a12": "#f0b8b0",
        "a13": "#f898c0", "a14": "#88e0e8", "a15": "#f8d888", "a16": "#c8a0f8",
        "a17": "#60c8d8", "a18": "#f8c8c0", "a19": "#d0a8f8", "a20": "#70d8e8",
    },
    "ember": {
        "base": "#1c1410", "surface": "#251c16", "overlay": "#332419",
        "muted": "#7a6048", "subtle": "#9e8066", "text": "#f5ece0",
        "a1": "#ff7a8a", "a2": "#a0dcc8", "a3": "#ffd47a", "a4": "#d4aef5",
        "a5": "#52aaa0", "a6": "#ffbcaa", "a7": "#ff9870", "a8": "#80d8b8",
        "a9": "#f8e090", "a10": "#c898e8", "a11": "#60b8a8", "a12": "#ffc898",
        "a13": "#ff8878", "a14": "#90e0c0", "a15": "#f8d070", "a16": "#d8a8f0",
        "a17": "#70c8b0", "a18": "#ffd8a8", "a19": "#e8a0d8", "a20": "#88c8a8",
    },
    "slate": {
        "base": "#141820", "surface": "#1c2028", "overlay": "#262c38",
        "muted": "#506070", "subtle": "#708090", "text": "#d0d8e8",
        "a1": "#c87090", "a2": "#78c8d8", "a3": "#c8b068", "a4": "#9878c8",
        "a5": "#3888a8", "a6": "#c8a0a0", "a7": "#b86888", "a8": "#68b8c8",
        "a9": "#b8a058", "a10": "#8868b8", "a11": "#2878a0", "a12": "#b89090",
        "a13": "#d880a0", "a14": "#88d0d8", "a15": "#d8c078", "a16": "#a888d8",
        "a17": "#4898b8", "a18": "#d8b0b0", "a19": "#e890b0", "a20": "#98d8e0",
    },
    "forest": {
        "base": "#0e1812", "surface": "#141e18", "overlay": "#1e2e22",
        "muted": "#4e7058", "subtle": "#6e9070", "text": "#d8f0dc",
        "a1": "#e87888", "a2": "#78e8a8", "a3": "#e8d078", "a4": "#b898e0",
        "a5": "#38c880", "a6": "#e8b8b0", "a7": "#d86878", "a8": "#58d890",
        "a9": "#d8c068", "a10": "#a088d0", "a11": "#28b870", "a12": "#d8a8a0",
        "a13": "#f88898", "a14": "#68f8b0", "a15": "#f8e088", "a16": "#c8a8f0",
        "a17": "#48e898", "a18": "#f8c8b8", "a19": "#d0b0f8", "a20": "#78f8c0",
    },
    "desert": {
        "base": "#1e1808", "surface": "#28220e", "overlay": "#382e16",
        "muted": "#806840", "subtle": "#a08858", "text": "#f8f0d8",
        "a1": "#e87070", "a2": "#88d8b8", "a3": "#f0c040", "a4": "#c898e0",
        "a5": "#50a888", "a6": "#f0a888", "a7": "#d86060", "a8": "#70c8a8",
        "a9": "#e0b030", "a10": "#b888d0", "a11": "#409878", "a12": "#e09878",
        "a13": "#f08080", "a14": "#98e8c0", "a15": "#f8d050", "a16": "#d8a8f0",
        "a17": "#60b898", "a18": "#f8b890", "a19": "#e0b8f8", "a20": "#80d0b0",
    },
    "ocean": {
        "base": "#0a1220", "surface": "#101a2c", "overlay": "#182438",
        "muted": "#385878", "subtle": "#588898", "text": "#c0e0f8",
        "a1": "#d06888", "a2": "#60d8f0", "a3": "#d0c060", "a4": "#9878d0",
        "a5": "#3098c0", "a6": "#d0a8b0", "a7": "#c05878", "a8": "#50c8e0",
        "a9": "#c0b050", "a10": "#8868c0", "a11": "#2088b0", "a12": "#c09898",
        "a13": "#e07898", "a14": "#70e0f8", "a15": "#e0d070", "a16": "#a888e0",
        "a17": "#40a8d0", "a18": "#e0b8c0", "a19": "#b898e8", "a20": "#58c8e0",
    },
    "lavender": {
        "base": "#18162a", "surface": "#201e36", "overlay": "#2c2848",
        "muted": "#685880", "subtle": "#8878a8", "text": "#e8e0f8",
        "a1": "#f088a8", "a2": "#88d0e0", "a3": "#f0c880", "a4": "#c8a0f8",
        "a5": "#5090a8", "a6": "#f0b8c8", "a7": "#e07898", "a8": "#78c0d0",
        "a9": "#e0b870", "a10": "#b890e8", "a11": "#409898", "a12": "#e0a8b8",
        "a13": "#f898b8", "a14": "#98d8e8", "a15": "#f8d890", "a16": "#d8b0f8",
        "a17": "#60a8b8", "a18": "#f8c8d8", "a19": "#e8c0f8", "a20": "#80c8d8",
    },
    "crimson": {
        "base": "#1a0c10", "surface": "#24121a", "overlay": "#321824",
        "muted": "#784058", "subtle": "#985878", "text": "#fce8f0",
        "a1": "#ff5878", "a2": "#80e0d0", "a3": "#f8c868", "a4": "#c890f0",
        "a5": "#40b090", "a6": "#ff98b0", "a7": "#f04868", "a8": "#70d0c0",
        "a9": "#e8b858", "a10": "#b880e0", "a11": "#30a080", "a12": "#f08898",
        "a13": "#ff6888", "a14": "#90e8d8", "a15": "#f8d878", "a16": "#d8a0f8",
        "a17": "#50c0a0", "a18": "#ffa8c0", "a19": "#e8b0f8", "a20": "#80d8c8",
    },
    "teal": {
        "base": "#0c1a1c", "surface": "#122224", "overlay": "#1c3032",
        "muted": "#38686c", "subtle": "#589094", "text": "#c8f0f0",
        "a1": "#e07088", "a2": "#50f0d8", "a3": "#e8d060", "a4": "#a880d8",
        "a5": "#30d0b8", "a6": "#e8b0b8", "a7": "#d06078", "a8": "#40e0c8",
        "a9": "#d8c050", "a10": "#9870c8", "a11": "#20c0a8", "a12": "#d8a0a8",
        "a13": "#f08098", "a14": "#60f8e0", "a15": "#f8e070", "a16": "#c090e8",
        "a17": "#40e8d0", "a18": "#f8c0c8", "a19": "#d0a0e8", "a20": "#70f0e0",
    },
    "sunset": {
        "base": "#1c1008", "surface": "#261808", "overlay": "#38220e",
        "muted": "#886038", "subtle": "#a88050", "text": "#fff0d8",
        "a1": "#ff6868", "a2": "#88e0c0", "a3": "#ffc840", "a4": "#d098f0",
        "a5": "#48b098", "a6": "#ffb080", "a7": "#f05858", "a8": "#70d0b0",
        "a9": "#f8b830", "a10": "#c088e0", "a11": "#38a088", "a12": "#f8a070",
        "a13": "#ff7878", "a14": "#98f0d0", "a15": "#ffd850", "a16": "#e0a8f8",
        "a17": "#58c0a8", "a18": "#ffc090", "a19": "#d0b0f8", "a20": "#80d8c0",
    },
    "mono": {
        "base": "#111111", "surface": "#1a1a1a", "overlay": "#282828",
        "muted": "#555555", "subtle": "#888888", "text": "#eeeeee",
        "a1": "#e06070", "a2": "#70c8c8", "a3": "#d0a850", "a4": "#9878c0",
        "a5": "#508888", "a6": "#c89898", "a7": "#c85060", "a8": "#58b8b8",
        "a9": "#c09840", "a10": "#8868b0", "a11": "#407878", "a12": "#b88888",
        "a13": "#e08090", "a14": "#80d8d8", "a15": "#e0b860", "a16": "#a888d0",
        "a17": "#609898", "a18": "#d8a8a8", "a19": "#b898d8", "a20": "#70c0c0",
    },
    "quartz": {
        "base": "#1e1018", "surface": "#281820", "overlay": "#38242e",
        "muted": "#805870", "subtle": "#a07890", "text": "#fce8f4",
        "a1": "#ff70a0", "a2": "#80e0e0", "a3": "#f8d080", "a4": "#d0a0f8",
        "a5": "#50a8c0", "a6": "#ffa8c8", "a7": "#f06090", "a8": "#70d0d0",
        "a9": "#e8c070", "a10": "#c090e8", "a11": "#4098b0", "a12": "#f098b8",
        "a13": "#ff80b0", "a14": "#90e8e8", "a15": "#f8e090", "a16": "#e0b0f8",
        "a17": "#60b8c8", "a18": "#ffb8d8", "a19": "#d0c0f8", "a20": "#80e0e8",
    },
    "aurora": {
        "base": "#0a1020", "surface": "#101828", "overlay": "#182438",
        "muted": "#406080", "subtle": "#6088b0", "text": "#d0e8ff",
        "a1": "#d870a0", "a2": "#50f0d0", "a3": "#f0e060", "a4": "#a060f0",
        "a5": "#30d8a0", "a6": "#e0a8c0", "a7": "#c86090", "a8": "#40e0c0",
        "a9": "#e0d050", "a10": "#9050e0", "a11": "#20c890", "a12": "#d09898",
        "a13": "#e880b0", "a14": "#60f8e0", "a15": "#f8f070", "a16": "#b070f8",
        "a17": "#40e8b0", "a18": "#f0b8d0", "a19": "#c090f8", "a20": "#68f0d8",
    },
    "parchment": {
        "base": "#f0e8d8", "surface": "#f8f0e4", "overlay": "#e4d8c4",
        "muted": "#a09078", "subtle": "#807058", "text": "#3c3020",
        "a1": "#a84858", "a2": "#388888", "a3": "#b07820", "a4": "#785898",
        "a5": "#206878", "a6": "#b87878", "a7": "#983848", "a8": "#287878",
        "a9": "#a06810", "a10": "#684888", "a11": "#105868", "a12": "#a86868",
        "a13": "#b85868", "a14": "#489898", "a15": "#c08830", "a16": "#8868a8",
        "a17": "#307888", "a18": "#c08888", "a19": "#986898", "a20": "#508898",
    },
    "linen": {
        "base": "#f5f0e8", "surface": "#fdf8f2", "overlay": "#ebe0d0",
        "muted": "#a09088", "subtle": "#786858", "text": "#302018",
        "a1": "#c05068", "a2": "#309090", "a3": "#c07818", "a4": "#886898",
        "a5": "#187080", "a6": "#c08070", "a7": "#b04058", "a8": "#208080",
        "a9": "#b06808", "a10": "#785888", "a11": "#086070", "a12": "#b07060",
        "a13": "#d06078", "a14": "#40a0a0", "a15": "#d08828", "a16": "#9878a8",
        "a17": "#288090", "a18": "#d09080", "a19": "#a888a8", "a20": "#409098",
    },
    "neon": {
        "base": "#080810", "surface": "#10101c", "overlay": "#181828",
        "muted": "#303060", "subtle": "#5050a0", "text": "#f0f0ff",
        "a1": "#ff2060", "a2": "#20f0e0", "a3": "#f0e020", "a4": "#a020f0",
        "a5": "#20d0a0", "a6": "#ff70c0", "a7": "#ff4080", "a8": "#40f8e8",
        "a9": "#f8f040", "a10": "#c040f8", "a11": "#40e8b8", "a12": "#ff90d0",
        "a13": "#ff0040", "a14": "#00f8d0", "a15": "#f8e800", "a16": "#8800f8",
        "a17": "#00d8a0", "a18": "#ff60b0", "a19": "#e000f0", "a20": "#20f8e0",
    },
    "cosmos": {
        "base": "#100820", "surface": "#180c30", "overlay": "#241440",
        "muted": "#604880", "subtle": "#8068b0", "text": "#f0e8ff",
        "a1": "#ff40a0", "a2": "#40f8e0", "a3": "#f8e040", "a4": "#c040ff",
        "a5": "#40e0b0", "a6": "#ff90d0", "a7": "#f02890", "a8": "#28f0d0",
        "a9": "#f0d028", "a10": "#b028f0", "a11": "#28d0a0", "a12": "#f080c0",
        "a13": "#ff50b0", "a14": "#50f8e8", "a15": "#f8e850", "a16": "#d050ff",
        "a17": "#50f0c0", "a18": "#ffa0d8", "a19": "#e070ff", "a20": "#70f8e8",
    },
}


class rosepine:
    """
    Rosé Pine — 20 variants, each with 20 unique accent colours (a1–a20).
    A 20-bar chart will never repeat a colour.

    Variants
    --------
    main · moon · dawn · midnight · ember · slate · forest · desert ·
    ocean · lavender · crimson · teal · sunset · mono · quartz ·
    aurora · parchment · linen · neon · cosmos
    """
    VARIANTS = list(_RP)
    COLORS   = _RP

    @staticmethod
    def apply(variant="main", font="jetbrains", font_size_base=13, grid=False,
              font_weight="normal", font_color=None, label_color=None, tick_color=None):
        """
        Apply Rosé Pine theme globally — works for ALL plots including seaborn.

        This is the recommended one-liner for seaborn workflows::

            c = hv.rosepine.apply("dawn")
            pal = hv.rosepine.palette("dawn")
            # now just use seaborn/matplotlib normally — theme is global
            sns.countplot(x='col', data=df, palette=pal)
            plt.show()

        Parameters
        ----------
        variant       : str        one of rosepine.VARIANTS
        font          : str | None "jetbrains" | "sourcecodepro" | file path | None
        font_size_base: int        base font size (default 13)
        grid          : bool | "x" | "y"
        font_weight   : str        "normal" | "bold" | "light"  (default "normal")
        font_color    : str | None hex colour — overrides ALL text colour
        label_color   : str | None hex colour — overrides axis label/title only
        tick_color    : str | None hex colour — overrides tick labels only
        """
        if variant not in _RP:
            raise ValueError(f"rosepine variant must be one of {rosepine.VARIANTS!r}")
        c = _RP[variant]
        plt.rcParams.update(_build_rc(c, _resolve_font(font), font_size_base,
                                      grid, "magma", font_weight,
                                      font_color, label_color, tick_color))
        _store_active("rosepine", variant, font, font_size_base, grid,
                      font_weight, font_color, label_color, tick_color)
        return c

    @staticmethod
    def palette(variant="main"):
        if variant not in _RP:
            raise ValueError(f"rosepine variant must be one of {rosepine.VARIANTS!r}")
        return [_RP[variant][k] for k in _A]

    @staticmethod
    def subplots(*args, variant="main", **kwargs):
        c   = rosepine.apply(variant=variant)
        fig, axes = plt.subplots(*args, **kwargs)
        fig.patch.set_facecolor(c["base"])
        return fig, axes

    @staticmethod
    def figure(variant="main", font="jetbrains", font_size_base=13,
               grid=False, font_weight="normal", font_color=None,
               label_color=None, tick_color=None, show=False, **fig_kwargs):
        """
        One-call themed figure. Returns (colour_dict, fig, ax).

        For seaborn use apply() instead — it sets the theme globally
        and seaborn picks it up automatically with no blank canvas issue::

            c = hv.rosepine.apply("dawn")
            pal = hv.rosepine.palette("dawn")
            sns.countplot(x='col', data=df, palette=pal)
            plt.title("My chart", color=c['text'])
            plt.show()

        For pure matplotlib, figure() gives you fig and ax directly::

            c, fig, ax = hv.rosepine.figure("dawn", figsize=(10, 5))
            pal = hv.rosepine.palette("dawn")
            ax.bar(cats, vals, color=pal[:6])
            ax.set_title("My chart", color=c['text'])
            plt.show()

        show=False (default): no blank canvas in setup cell.
        show=True: preview the empty styled canvas.
        """
        c = rosepine.apply(variant, font=font, font_size_base=font_size_base,
                           grid=grid, font_weight=font_weight,
                           font_color=font_color, label_color=label_color,
                           tick_color=tick_color)
        fig, ax = plt.subplots(**fig_kwargs)
        _apply_ax_theme(ax, fig, c)
        if not show:
            # Remove from pyplot's display manager so Jupyter won't
            # render the blank canvas, but fig/ax objects stay fully usable.
            try:
                from matplotlib._pylab_helpers import Gcf
                Gcf.destroy_fig(fig)
            except Exception:
                plt.close(fig)
        return c, fig, ax

    @staticmethod
    def figures(nrows=1, ncols=1, variant="main", font="jetbrains",
                font_size_base=13, grid=False, font_weight="normal",
                font_color=None, label_color=None, tick_color=None,
                **fig_kwargs):
        """
        One-call themed multi-axes figure for Jupyter.
        Returns (colour_dict, fig, axes) — all axes are themed automatically.

        Usage
        -----
        c, fig, axes = hv.rosepine.figures(1, 3, "dawn", figsize=(15, 5))
        pal = hv.rosepine.palette("dawn")
        axes[0].bar(cats, vals, color=pal[:6])
        plt.show()
        """
        c = rosepine.apply(variant, font=font, font_size_base=font_size_base,
                           grid=grid, font_weight=font_weight,
                           font_color=font_color, label_color=label_color,
                           tick_color=tick_color)
        fig, axes = plt.subplots(nrows, ncols, **fig_kwargs)
        fig.patch.set_facecolor(c["base"])
        ax_list = axes.flatten() if hasattr(axes, "flatten") else [axes]
        for ax in ax_list:
            _apply_ax_theme(ax, fig, c)
        return c, fig, axes

    @staticmethod
    def help():
        """Print all apply() parameters for rosepine."""
        print("\n  hv.rosepine.apply() parameters")
        print("  " + "─"*40)
        params = [
            ("variant",        str(rosepine.VARIANTS)),
            ("font",           "jetbrains | sourcecodepro | cascadia | fira_code | hack | microsoft_sans | operator_mono | roboto | None"),
            ("font_size_base", "int  — default 13"),
            ("font_weight",    "normal | bold | light"),
            ("grid",           "False | True | x | y"),
            ("font_color",     "#rrggbb  — overrides all text"),
            ("label_color",    "#rrggbb  — axis labels & title only"),
            ("tick_color",     "#rrggbb  — tick labels only"),
        ]
        for param, desc in params:
            print(f"    {param:<18}  {desc}")
        print()


# ===========================================================================
#  DRACULA — 20 variants × 20 unique accent colours each
#  Flavour: bold, high-contrast, neon-gothic
# ===========================================================================

_DR = {
    "classic": {
        "base": "#282A36", "surface": "#343746", "overlay": "#44475A",
        "muted": "#6272A4", "subtle": "#8B9BC8", "text": "#F8F8F2",
        "a1": "#BD93F9", "a2": "#FF79C6", "a3": "#8BE9FD", "a4": "#50FA7B",
        "a5": "#FFB86C", "a6": "#F1FA8C", "a7": "#FF5555", "a8": "#C8A8F8",
        "a9": "#FF90D0", "a10": "#A0F0FF", "a11": "#78FF98", "a12": "#FFC888",
        "a13": "#F8FFA0", "a14": "#FF7878", "a15": "#D8B8FF", "a16": "#FFB0E0",
        "a17": "#C0F8FF", "a18": "#A0FFB8", "a19": "#FFD8A8", "a20": "#FFA0A0",
    },
    "soft": {
        "base": "#21222C", "surface": "#2D2F3F", "overlay": "#3D3F50",
        "muted": "#5A6490", "subtle": "#7B88B8", "text": "#E8E8E0",
        "a1": "#A580E8", "a2": "#E86DB5", "a3": "#72D4E8", "a4": "#44E06A",
        "a5": "#E8A45A", "a6": "#E0E07A", "a7": "#E84444", "a8": "#B898E0",
        "a9": "#E088C0", "a10": "#88D0E0", "a11": "#68E080", "a12": "#E0B878",
        "a13": "#D8D888", "a14": "#E06868", "a15": "#C8A8E8", "a16": "#E8A0C8",
        "a17": "#98D8E8", "a18": "#88E898", "a19": "#E8C890", "a20": "#E89090",
    },
    "ink": {
        "base": "#13141f", "surface": "#1b1c2c", "overlay": "#262838",
        "muted": "#484a6e", "subtle": "#686aa0", "text": "#eeeef8",
        "a1": "#c0a0ff", "a2": "#ff88d4", "a3": "#88f0ff", "a4": "#60ff90",
        "a5": "#ffb878", "a6": "#ffff90", "a7": "#ff6060", "a8": "#d0b8ff",
        "a9": "#ffa0e0", "a10": "#a0f8ff", "a11": "#80ffa8", "a12": "#ffc890",
        "a13": "#ffffa0", "a14": "#ff8080", "a15": "#e0c8ff", "a16": "#ffb8e8",
        "a17": "#b8f8ff", "a18": "#a0ffb8", "a19": "#ffd8a8", "a20": "#ffa0a0",
    },
    "blood": {
        "base": "#1a0808", "surface": "#240e0e", "overlay": "#341818",
        "muted": "#784040", "subtle": "#a06060", "text": "#fce8e8",
        "a1": "#ff3030", "a2": "#78e8f8", "a3": "#f8f070", "a4": "#50f878",
        "a5": "#f8a858", "a6": "#d880f8", "a7": "#ff78c8", "a8": "#ff5050",
        "a9": "#90f0f8", "a10": "#f8f888", "a11": "#70f898", "a12": "#f8b870",
        "a13": "#e890f8", "a14": "#ff90d8", "a15": "#ff6868", "a16": "#a0f8f8",
        "a17": "#f8f898", "a18": "#88f8a8", "a19": "#f8c888", "a20": "#f0a0f8",
    },
    "storm": {
        "base": "#0c1824", "surface": "#142030", "overlay": "#1e2e40",
        "muted": "#386080", "subtle": "#588898", "text": "#c8e8f8",
        "a1": "#a088f0", "a2": "#f088c8", "a3": "#50e8f8", "a4": "#50f888",
        "a5": "#f0a870", "a6": "#f0f088", "a7": "#f07080", "a8": "#b8a0f8",
        "a9": "#f8a0d8", "a10": "#70f0f8", "a11": "#70f8a0", "a12": "#f8b888",
        "a13": "#f8f8a0", "a14": "#f88898", "a15": "#c8b0f8", "a16": "#f8b0e0",
        "a17": "#88f8f8", "a18": "#88f8b0", "a19": "#f8c8a0", "a20": "#f8a0a8",
    },
    "toxic": {
        "base": "#0a1408", "surface": "#101c0e", "overlay": "#182818",
        "muted": "#407040", "subtle": "#60a060", "text": "#d8f8d0",
        "a1": "#40ff60", "a2": "#c090f0", "a3": "#f090c8", "a4": "#80f0e0",
        "a5": "#f0c060", "a6": "#e8ff40", "a7": "#f06060", "a8": "#68ff80",
        "a9": "#d0a8f8", "a10": "#f8a8d8", "a11": "#98f8e8", "a12": "#f8d078",
        "a13": "#f0ff60", "a14": "#f07878", "a15": "#88ff98", "a16": "#e0b8f8",
        "a17": "#f8b8e0", "a18": "#a8f8f0", "a19": "#f8e090", "a20": "#f88888",
    },
    "amber": {
        "base": "#1c1008", "surface": "#281810", "overlay": "#382218",
        "muted": "#806040", "subtle": "#a08050", "text": "#fff0d8",
        "a1": "#ffa030", "a2": "#c888f0", "a3": "#f888b8", "a4": "#80e0f0",
        "a5": "#80f090", "a6": "#ffe030", "a7": "#ff5040", "a8": "#ffb848",
        "a9": "#d8a0f8", "a10": "#f8a0c8", "a11": "#98e8f8", "a12": "#98f8a8",
        "a13": "#fff050", "a14": "#ff6858", "a15": "#ffc860", "a16": "#e8b0f8",
        "a17": "#f8b0d0", "a18": "#a8f0f8", "a19": "#a8f8b8", "a20": "#fff870",
    },
    "synthwave": {
        "base": "#0d0921", "surface": "#150e32", "overlay": "#201545",
        "muted": "#5a3a80", "subtle": "#8050b8", "text": "#f0e8ff",
        "a1": "#e040ff", "a2": "#ff40d0", "a3": "#40e8ff", "a4": "#40ff80",
        "a5": "#ff9020", "a6": "#ffe820", "a7": "#ff2060", "a8": "#f060ff",
        "a9": "#ff60e0", "a10": "#60f0ff", "a11": "#60ff98", "a12": "#ffa840",
        "a13": "#fff040", "a14": "#ff4080", "a15": "#f880ff", "a16": "#ff80e8",
        "a17": "#80f8ff", "a18": "#80ffb0", "a19": "#ffb858", "a20": "#ff6090",
    },
    "volcanic": {
        "base": "#180c04", "surface": "#221004", "overlay": "#301808",
        "muted": "#885030", "subtle": "#b07040", "text": "#fff0d8",
        "a1": "#ff3020", "a2": "#c070e0", "a3": "#f070a8", "a4": "#60d8e8",
        "a5": "#70e870", "a6": "#ffe040", "a7": "#ff8020", "a8": "#ff5030",
        "a9": "#d088f0", "a10": "#f888b8", "a11": "#78e8f8", "a12": "#88f888",
        "a13": "#fff050", "a14": "#ff9030", "a15": "#ff6840", "a16": "#e0a0f8",
        "a17": "#f8a0c8", "a18": "#90f0f8", "a19": "#a0f8a0", "a20": "#fff868",
    },
    "arctic": {
        "base": "#0e1a28", "surface": "#162230", "overlay": "#1e2e40",
        "muted": "#486880", "subtle": "#6890a8", "text": "#d0ecff",
        "a1": "#a090f8", "a2": "#f090d0", "a3": "#60f0ff", "a4": "#60f898",
        "a5": "#f8b878", "a6": "#f8f898", "a7": "#f88090", "a8": "#b8a8f8",
        "a9": "#f8a8e0", "a10": "#80f8ff", "a11": "#80f8b0", "a12": "#f8c890",
        "a13": "#f8f8b0", "a14": "#f8a0a8", "a15": "#c8b8f8", "a16": "#f8b8e8",
        "a17": "#98f8ff", "a18": "#98f8c0", "a19": "#f8d8a8", "a20": "#f8b0b8",
    },
    "cyber": {
        "base": "#0a0a18", "surface": "#101028", "overlay": "#181838",
        "muted": "#383870", "subtle": "#5858b0", "text": "#e8e8ff",
        "a1": "#c030ff", "a2": "#ff30c8", "a3": "#30f8ff", "a4": "#30ff78",
        "a5": "#ff9830", "a6": "#fff030", "a7": "#ff1848", "a8": "#d050ff",
        "a9": "#ff50d8", "a10": "#50f8ff", "a11": "#50ff90", "a12": "#ffaa48",
        "a13": "#fff850", "a14": "#ff3860", "a15": "#e070ff", "a16": "#ff70e0",
        "a17": "#70f8ff", "a18": "#70ffa0", "a19": "#ffba60", "a20": "#ff5070",
    },
    "coffee": {
        "base": "#1a1008", "surface": "#221810", "overlay": "#302018",
        "muted": "#806040", "subtle": "#9e8058", "text": "#f8ece0",
        "a1": "#b880d8", "a2": "#e880b0", "a3": "#80c8d8", "a4": "#80c880",
        "a5": "#e09050", "a6": "#e0d870", "a7": "#e06858", "a8": "#c898e0",
        "a9": "#f098c0", "a10": "#98d8e8", "a11": "#98d898", "a12": "#e8a868",
        "a13": "#e8e888", "a14": "#e88070", "a15": "#d8a8e8", "a16": "#f8a8d0",
        "a17": "#a8e8f8", "a18": "#a8e8a8", "a19": "#f8b880", "a20": "#f89088",
    },
    "rose": {
        "base": "#1c0e18", "surface": "#261620", "overlay": "#36202e",
        "muted": "#785068", "subtle": "#987088", "text": "#fce8f4",
        "a1": "#ff80d0", "a2": "#d890f8", "a3": "#80e0f0", "a4": "#80f898",
        "a5": "#f8a880", "a6": "#f8f880", "a7": "#ff5880", "a8": "#ff98d8",
        "a9": "#e8a0f8", "a10": "#98e8f8", "a11": "#98f8a8", "a12": "#f8b890",
        "a13": "#f8f898", "a14": "#ff7090", "a15": "#ffb0e0", "a16": "#f0b0f8",
        "a17": "#a8f0f8", "a18": "#a8f8b8", "a19": "#f8c8a0", "a20": "#ff8898",
    },
    "void": {
        "base": "#080808", "surface": "#101010", "overlay": "#202020",
        "muted": "#484848", "subtle": "#787878", "text": "#f8f8f8",
        "a1": "#c878f8", "a2": "#f878c8", "a3": "#78e8f8", "a4": "#78f888",
        "a5": "#f8a860", "a6": "#f8f860", "a7": "#f85858", "a8": "#d898f8",
        "a9": "#f898d8", "a10": "#98f0f8", "a11": "#98f8a0", "a12": "#f8b878",
        "a13": "#f8f878", "a14": "#f87070", "a15": "#e8a8f8", "a16": "#f8a8e0",
        "a17": "#a8f8f8", "a18": "#a8f8b0", "a19": "#f8c890", "a20": "#f88888",
    },
    "galaxy": {
        "base": "#100818", "surface": "#180c22", "overlay": "#221430",
        "muted": "#584878", "subtle": "#7868a8", "text": "#f0e8ff",
        "a1": "#d058ff", "a2": "#ff58e0", "a3": "#58f0ff", "a4": "#58ff90",
        "a5": "#ffa850", "a6": "#ffe850", "a7": "#ff4870", "a8": "#e078ff",
        "a9": "#ff78e8", "a10": "#78f8ff", "a11": "#78ffa8", "a12": "#ffb868",
        "a13": "#fff068", "a14": "#ff6080", "a15": "#e898ff", "a16": "#ff98f0",
        "a17": "#98f8ff", "a18": "#98ffb8", "a19": "#ffc878", "a20": "#ff7890",
    },
    "silver": {
        "base": "#181820", "surface": "#202028", "overlay": "#2c2c38",
        "muted": "#606070", "subtle": "#8888a0", "text": "#e0e0f0",
        "a1": "#a898e0", "a2": "#e098c8", "a3": "#88c8e0", "a4": "#88d898",
        "a5": "#d8a878", "a6": "#d8d880", "a7": "#d87880", "a8": "#b8a8e8",
        "a9": "#e8a8d8", "a10": "#98d0e8", "a11": "#98e0a8", "a12": "#e0b888",
        "a13": "#e0e090", "a14": "#e09090", "a15": "#c8b8e8", "a16": "#f0b8e0",
        "a17": "#a8d8e8", "a18": "#a8e8b8", "a19": "#e8c898", "a20": "#e8a0a0",
    },
    "jungle": {
        "base": "#0c1610", "surface": "#121e16", "overlay": "#1c2c20",
        "muted": "#406848", "subtle": "#608868", "text": "#d0f0d4",
        "a1": "#50f070", "a2": "#b088e0", "a3": "#e888b8", "a4": "#88e8f8",
        "a5": "#f8d060", "a6": "#f07878", "a7": "#88f0a0", "a8": "#c0a0f0",
        "a9": "#f0a0c8", "a10": "#a0f0f8", "a11": "#f8e078", "a12": "#f89090",
        "a13": "#68f888", "a14": "#d0b0f8", "a15": "#f8b0d8", "a16": "#b0f8f8",
        "a17": "#f8e890", "a18": "#f8a0a0", "a19": "#80f8a8", "a20": "#e0c0f8",
    },
    "velvet": {
        "base": "#1a1028", "surface": "#221838", "overlay": "#302048",
        "muted": "#684878", "subtle": "#886898", "text": "#f0d8ff",
        "a1": "#d880ff", "a2": "#ff80e8", "a3": "#80e8ff", "a4": "#80ff98",
        "a5": "#ffb880", "a6": "#fff080", "a7": "#ff6080", "a8": "#e898ff",
        "a9": "#ff98f0", "a10": "#98f0ff", "a11": "#98ffb0", "a12": "#ffc898",
        "a13": "#fff898", "a14": "#ff7898", "a15": "#f0a8ff", "a16": "#ffa8f8",
        "a17": "#a8f8ff", "a18": "#a8ffc0", "a19": "#ffd8a8", "a20": "#ff90a8",
    },
    "neon": {
        "base": "#080810", "surface": "#101018", "overlay": "#181820",
        "muted": "#303060", "subtle": "#5050a0", "text": "#ffffff",
        "a1": "#d040ff", "a2": "#ff40c8", "a3": "#40f8ff", "a4": "#40ff80",
        "a5": "#ff9020", "a6": "#ffff20", "a7": "#ff2020", "a8": "#e060ff",
        "a9": "#ff60d8", "a10": "#60f8ff", "a11": "#60ff98", "a12": "#ffa840",
        "a13": "#ffff40", "a14": "#ff4040", "a15": "#f080ff", "a16": "#ff80e0",
        "a17": "#80ffff", "a18": "#80ffb0", "a19": "#ffb860", "a20": "#ff6060",
    },
    "paper": {
        "base": "#f5f5e8", "surface": "#fdfdf5", "overlay": "#e5e5d8",
        "muted": "#808078", "subtle": "#606058", "text": "#202028",
        "a1": "#7050a0", "a2": "#c03878", "a3": "#207888", "a4": "#187030",
        "a5": "#c05818", "a6": "#787800", "a7": "#c01818", "a8": "#8060b0",
        "a9": "#d04888", "a10": "#309898", "a11": "#288840", "a12": "#d06828",
        "a13": "#888810", "a14": "#d02828", "a15": "#9070c0", "a16": "#e05898",
        "a17": "#40a8a8", "a18": "#389850", "a19": "#e07838", "a20": "#989820",
    },
}


class dracula:
    """
    Dracula — 20 variants, each with 20 unique accent colours (a1–a20).
    A 20-bar chart will never repeat a colour.

    Variants
    --------
    classic · soft · ink · blood · storm · toxic · amber · synthwave ·
    volcanic · arctic · cyber · coffee · rose · void · galaxy ·
    silver · jungle · velvet
    """
    VARIANTS = list(_DR)
    COLORS   = _DR

    @staticmethod
    def apply(variant="classic", font="jetbrains", font_size_base=13, grid=False,
              font_weight="normal", font_color=None, label_color=None, tick_color=None):
        """
        Apply Dracula theme globally.

        Parameters
        ----------
        variant       : str        one of dracula.VARIANTS
        font          : str | None "jetbrains" | "sourcecodepro" | file path | None
        font_size_base: int        base font size (default 13)
        grid          : bool | "x" | "y"
        font_weight   : str        "normal" | "bold" | "light"  (default "normal")
        font_color    : str | None hex colour — overrides ALL text colour
        label_color   : str | None hex colour — overrides axis label/title only
        tick_color    : str | None hex colour — overrides tick labels only
        """
        if variant not in _DR:
            raise ValueError(f"dracula variant must be one of {dracula.VARIANTS!r}")
        c = _DR[variant]
        plt.rcParams.update(_build_rc(c, _resolve_font(font), font_size_base,
                                      grid, "plasma", font_weight,
                                      font_color, label_color, tick_color))
        _store_active("dracula", variant, font, font_size_base, grid,
                      font_weight, font_color, label_color, tick_color)
        return c

    @staticmethod
    def palette(variant="classic"):
        if variant not in _DR:
            raise ValueError(f"dracula variant must be one of {dracula.VARIANTS!r}")
        return [_DR[variant][k] for k in _A]

    @staticmethod
    def subplots(*args, variant="classic", **kwargs):
        c   = dracula.apply(variant=variant)
        fig, axes = plt.subplots(*args, **kwargs)
        fig.patch.set_facecolor(c["base"])
        return fig, axes

    @staticmethod
    def figure(variant="classic", font="jetbrains", font_size_base=13,
               grid=False, font_weight="normal", font_color=None,
               label_color=None, tick_color=None, show=False, **fig_kwargs):
        """One-call themed figure. Returns (c, fig, ax).
        For seaborn use apply() instead. For pure matplotlib use this.
        show=False (default): no blank canvas. show=True: preview empty canvas.
        """
        c = dracula.apply(variant, font=font, font_size_base=font_size_base,
                          grid=grid, font_weight=font_weight,
                          font_color=font_color, label_color=label_color,
                          tick_color=tick_color)
        fig, ax = plt.subplots(**fig_kwargs)
        _apply_ax_theme(ax, fig, c)
        if not show:
            try:
                from matplotlib._pylab_helpers import Gcf
                Gcf.destroy_fig(fig)
            except Exception:
                plt.close(fig)
        return c, fig, ax

    @staticmethod
    def figures(nrows=1, ncols=1, variant="classic", font="jetbrains",
                font_size_base=13, grid=False, font_weight="normal",
                font_color=None, label_color=None, tick_color=None,
                **fig_kwargs):
        """One-call themed multi-axes figure. Returns (c, fig, axes)."""
        c = dracula.apply(variant, font=font, font_size_base=font_size_base,
                          grid=grid, font_weight=font_weight,
                          font_color=font_color, label_color=label_color,
                          tick_color=tick_color)
        fig, axes = plt.subplots(nrows, ncols, **fig_kwargs)
        fig.patch.set_facecolor(c["base"])
        ax_list = axes.flatten() if hasattr(axes, "flatten") else [axes]
        for ax in ax_list:
            _apply_ax_theme(ax, fig, c)
        return c, fig, axes

    @staticmethod
    def help():
        """Print all apply() parameters for dracula."""
        print("\n  hv.dracula.apply() parameters")
        print("  " + "─"*40)
        params = [
            ("variant",        str(dracula.VARIANTS)),
            ("font",           "jetbrains | sourcecodepro | cascadia | fira_code | hack | microsoft_sans | operator_mono | roboto | None"),
            ("font_size_base", "int  — default 13"),
            ("font_weight",    "normal | bold | light"),
            ("grid",           "False | True | x | y"),
            ("font_color",     "#rrggbb  — overrides all text"),
            ("label_color",    "#rrggbb  — axis labels & title only"),
            ("tick_color",     "#rrggbb  — tick labels only"),
        ]
        for param, desc in params:
            print(f"    {param:<18}  {desc}")
        print()


# ===========================================================================
#  PALENIGHT — 20 variants × 20 unique accent colours each
#  Flavour: deep indigo nights, cool blues, muted greens
# ===========================================================================

_PN = {
    "default": {
        "base": "#292D3E", "surface": "#34324a", "overlay": "#444267",
        "muted": "#676E95", "subtle": "#8B92B8", "text": "#A6ACCD",
        "a1": "#82aaff", "a2": "#c3e88d", "a3": "#c792ea", "a4": "#ffcb6b",
        "a5": "#89ddff", "a6": "#f78c6c", "a7": "#f07178", "a8": "#ff869a",
        "a9": "#98b8ff", "a10": "#d4f0a0", "a11": "#d8a8f8", "a12": "#ffd888",
        "a13": "#a0e8ff", "a14": "#f8a888", "a15": "#f88890", "a16": "#ffa0b0",
        "a17": "#b0c8ff", "a18": "#e0f8b8", "a19": "#e8c0ff", "a20": "#ffe8a0",
    },
    "contrast": {
        "base": "#202331", "surface": "#292D3E", "overlay": "#383a4e",
        "muted": "#585d7a", "subtle": "#7b82a8", "text": "#BEC3E0",
        "a1": "#7aa3f5", "a2": "#b8df82", "a3": "#bc8cdf", "a4": "#f5c260",
        "a5": "#7fd4f5", "a6": "#ec7d60", "a7": "#e86870", "a8": "#f57d95",
        "a9": "#90b8f8", "a10": "#c8e898", "a11": "#cc9ee8", "a12": "#f8d070",
        "a13": "#90d8f8", "a14": "#f89878", "a15": "#f88080", "a16": "#f890a8",
        "a17": "#a8c8f8", "a18": "#d8f0a8", "a19": "#d8a8f8", "a20": "#f8e088",
    },
    "midnight": {
        "base": "#1a1c2e", "surface": "#222438", "overlay": "#303250",
        "muted": "#585c80", "subtle": "#7880a8", "text": "#c0c8f0",
        "a1": "#78a0f0", "a2": "#b0d880", "a3": "#b888e0", "a4": "#f0c060",
        "a5": "#78d0f0", "a6": "#e87860", "a7": "#e06068", "a8": "#f07890",
        "a9": "#88b0f8", "a10": "#c0e090", "a11": "#c898e8", "a12": "#f8d070",
        "a13": "#88d8f8", "a14": "#f89070", "a15": "#f07878", "a16": "#f888a0",
        "a17": "#a0c0f8", "a18": "#d0e8a0", "a19": "#d8a8f0", "a20": "#f8e090",
    },
    "abyss": {
        "base": "#141520", "surface": "#1c1e30", "overlay": "#282a40",
        "muted": "#484c70", "subtle": "#686c98", "text": "#b8c0e8",
        "a1": "#6898e8", "a2": "#a8d078", "a3": "#b080d8", "a4": "#e8b858",
        "a5": "#70c8e8", "a6": "#e07058", "a7": "#d85860", "a8": "#e87088",
        "a9": "#78a8f0", "a10": "#b8e088", "a11": "#c090e0", "a12": "#f0c870",
        "a13": "#80d0f0", "a14": "#e88068", "a15": "#e87070", "a16": "#f08098",
        "a17": "#90b8f8", "a18": "#c8e898", "a19": "#d0a0e8", "a20": "#f8d080",
    },
    "noir": {
        "base": "#0e1018", "surface": "#161820", "overlay": "#222430",
        "muted": "#404460", "subtle": "#606488", "text": "#d0d8ff",
        "a1": "#88b0ff", "a2": "#c0e890", "a3": "#c898f0", "a4": "#ffd070",
        "a5": "#90e0ff", "a6": "#f89068", "a7": "#f07080", "a8": "#ff90a8",
        "a9": "#98c0ff", "a10": "#d0f0a0", "a11": "#d8a8f8", "a12": "#ffe080",
        "a13": "#a0e8ff", "a14": "#f8a078", "a15": "#f88090", "a16": "#ffa0b8",
        "a17": "#b0d0ff", "a18": "#e0f8b0", "a19": "#e8b8ff", "a20": "#fff090",
    },
    "nebula": {
        "base": "#1c1a30", "surface": "#242240", "overlay": "#302e50",
        "muted": "#585580", "subtle": "#7875a8", "text": "#c8c5f0",
        "a1": "#80a8ff", "a2": "#b0e088", "a3": "#d090f0", "a4": "#f8c870",
        "a5": "#88d8f8", "a6": "#f09068", "a7": "#e87080", "a8": "#f888b0",
        "a9": "#90b8ff", "a10": "#c0e898", "a11": "#e0a0f8", "a12": "#f8d880",
        "a13": "#98e0f8", "a14": "#f8a078", "a15": "#f08090", "a16": "#f898c0",
        "a17": "#a8c8ff", "a18": "#d0f0a8", "a19": "#e8b0ff", "a20": "#f8e890",
    },
    "twilight": {
        "base": "#201820", "surface": "#2c2030", "overlay": "#3a2e40",
        "muted": "#705868", "subtle": "#907880", "text": "#f0d8e8",
        "a1": "#9090f0", "a2": "#b8e098", "a3": "#d898f0", "a4": "#f8c878",
        "a5": "#98d8f0", "a6": "#f09878", "a7": "#e87888", "a8": "#f890b8",
        "a9": "#a0a0f8", "a10": "#c8e8a8", "a11": "#e8a8f8", "a12": "#f8d888",
        "a13": "#a8e0f8", "a14": "#f8a888", "a15": "#f08898", "a16": "#f8a0c8",
        "a17": "#b0b0f8", "a18": "#d8f0b8", "a19": "#f0b8f8", "a20": "#f8e898",
    },
    "rose": {
        "base": "#1e1520", "surface": "#281c2c", "overlay": "#362838",
        "muted": "#785870", "subtle": "#987888", "text": "#f0d8ec",
        "a1": "#9898f0", "a2": "#b8e898", "a3": "#e098f8", "a4": "#f8d080",
        "a5": "#98e0f8", "a6": "#f8a080", "a7": "#f07888", "a8": "#ff98c0",
        "a9": "#a8a8f8", "a10": "#c8f0a8", "a11": "#f0a8f8", "a12": "#f8e090",
        "a13": "#a8e8f8", "a14": "#f8b090", "a15": "#f88898", "a16": "#ffb0d0",
        "a17": "#b8b8f8", "a18": "#d8f8b8", "a19": "#f8b8f8", "a20": "#f8f0a0",
    },
    "dusk": {
        "base": "#1c1820", "surface": "#262028", "overlay": "#342c38",
        "muted": "#686068", "subtle": "#888088", "text": "#e8d8e8",
        "a1": "#8898e8", "a2": "#b0d888", "a3": "#c888e0", "a4": "#e8c070",
        "a5": "#88d0e8", "a6": "#e89070", "a7": "#e07080", "a8": "#f088a8",
        "a9": "#98a8f0", "a10": "#c0e098", "a11": "#d898e8", "a12": "#f0d080",
        "a13": "#98d8f0", "a14": "#f0a080", "a15": "#e88090", "a16": "#f098b8",
        "a17": "#a8b8f8", "a18": "#d0e8a8", "a19": "#e8a8f0", "a20": "#f0e090",
    },
    "arctic": {
        "base": "#101c28", "surface": "#182430", "overlay": "#223040",
        "muted": "#486878", "subtle": "#6888a0", "text": "#c8e0f8",
        "a1": "#70a8f0", "a2": "#a8d880", "a3": "#a880d8", "a4": "#e8c060",
        "a5": "#70d0f0", "a6": "#e08860", "a7": "#d87078", "a8": "#e88098",
        "a9": "#80b8f8", "a10": "#b8e090", "a11": "#b890e0", "a12": "#f0d070",
        "a13": "#80d8f8", "a14": "#e89870", "a15": "#e08088", "a16": "#f090a8",
        "a17": "#98c8f8", "a18": "#c8e8a0", "a19": "#c8a0e8", "a20": "#f0e080",
    },
    "steel": {
        "base": "#141820", "surface": "#1c2028", "overlay": "#282c38",
        "muted": "#506070", "subtle": "#708090", "text": "#c8d8e8",
        "a1": "#6898e0", "a2": "#a0c878", "a3": "#a078c8", "a4": "#d8b858",
        "a5": "#68c8d8", "a6": "#d88058", "a7": "#c86870", "a8": "#d87888",
        "a9": "#78a8e8", "a10": "#b0d888", "a11": "#b088d0", "a12": "#e0c870",
        "a13": "#78d0e0", "a14": "#e09070", "a15": "#d07880", "a16": "#e08898",
        "a17": "#90b8f0", "a18": "#c0e098", "a19": "#c098d8", "a20": "#e8d880",
    },
    "frost": {
        "base": "#101820", "surface": "#181e28", "overlay": "#222a34",
        "muted": "#487080", "subtle": "#6890a0", "text": "#c0d8e8",
        "a1": "#60a0e8", "a2": "#98d078", "a3": "#9870c0", "a4": "#d8b050",
        "a5": "#60c8d8", "a6": "#d87850", "a7": "#c06068", "a8": "#d07888",
        "a9": "#70b0f0", "a10": "#a8e088", "a11": "#a880c8", "a12": "#e0c060",
        "a13": "#70d0e0", "a14": "#e08860", "a15": "#c87078", "a16": "#e08898",
        "a17": "#88c0f8", "a18": "#b8e898", "a19": "#b890d0", "a20": "#e8d070",
    },
    "ash": {
        "base": "#1c1c24", "surface": "#242430", "overlay": "#303040",
        "muted": "#606070", "subtle": "#808090", "text": "#d0d0e0",
        "a1": "#7888c8", "a2": "#98b878", "a3": "#9878b8", "a4": "#c8a858",
        "a5": "#78a8b8", "a6": "#c07858", "a7": "#b86870", "a8": "#c87888",
        "a9": "#8898d0", "a10": "#a8c888", "a11": "#a888c0", "a12": "#d0b868",
        "a13": "#88b8c8", "a14": "#c88868", "a15": "#c07880", "a16": "#d08898",
        "a17": "#98a8d8", "a18": "#b8d098", "a19": "#b898c8", "a20": "#d8c878",
    },
    "smoke": {
        "base": "#1a1a22", "surface": "#222228", "overlay": "#2e2e38",
        "muted": "#585868", "subtle": "#787888", "text": "#c8c8d8",
        "a1": "#7080b8", "a2": "#90a870", "a3": "#9070a8", "a4": "#b89850",
        "a5": "#7098a8", "a6": "#b87050", "a7": "#a86068", "a8": "#b87080",
        "a9": "#8090c0", "a10": "#a0b880", "a11": "#a080b0", "a12": "#c0a860",
        "a13": "#80a8b8", "a14": "#c08060", "a15": "#b07078", "a16": "#c08090",
        "a17": "#90a0c8", "a18": "#b0c890", "a19": "#b090b8", "a20": "#c8b870",
    },
    "pebble": {
        "base": "#202028", "surface": "#282830", "overlay": "#34343e",
        "muted": "#686878", "subtle": "#888898", "text": "#d8d8e8",
        "a1": "#8090c0", "a2": "#a0b880", "a3": "#a080b8", "a4": "#c0a860",
        "a5": "#80a8b8", "a6": "#c08060", "a7": "#b87078", "a8": "#c08090",
        "a9": "#9098c8", "a10": "#b0c890", "a11": "#b090c0", "a12": "#c8b870",
        "a13": "#90b8c8", "a14": "#c89070", "a15": "#c08088", "a16": "#d09098",
        "a17": "#a0a8d0", "a18": "#c0d0a0", "a19": "#c0a0c8", "a20": "#d0c880",
    },
    "neon": {
        "base": "#080a14", "surface": "#101220", "overlay": "#181a2e",
        "muted": "#303058", "subtle": "#505090", "text": "#f0f0ff",
        "a1": "#4488ff", "a2": "#88ff44", "a3": "#cc44ff", "a4": "#ffee00",
        "a5": "#44eeff", "a6": "#ff8800", "a7": "#ff2244", "a8": "#ff44aa",
        "a9": "#66aaff", "a10": "#aaff66", "a11": "#dd66ff", "a12": "#ffee44",
        "a13": "#66eeff", "a14": "#ffaa44", "a15": "#ff4466", "a16": "#ff66cc",
        "a17": "#88ccff", "a18": "#ccff88", "a19": "#ee88ff", "a20": "#ffff66",
    },
    "vivid": {
        "base": "#10121e", "surface": "#181a28", "overlay": "#202234",
        "muted": "#404068", "subtle": "#6060a0", "text": "#e8e8ff",
        "a1": "#5090ff", "a2": "#90ff50", "a3": "#d050ff", "a4": "#fff020",
        "a5": "#50f0ff", "a6": "#ff9010", "a7": "#ff3050", "a8": "#ff50b8",
        "a9": "#70a8ff", "a10": "#a8ff70", "a11": "#e070ff", "a12": "#fff040",
        "a13": "#70f8ff", "a14": "#ffa830", "a15": "#ff5070", "a16": "#ff70c8",
        "a17": "#90c0ff", "a18": "#c0ff90", "a19": "#f090ff", "a20": "#ffff60",
    },
    "day": {
        "base": "#f0f0f8", "surface": "#f8f8ff", "overlay": "#e0e0f0",
        "muted": "#909090", "subtle": "#686880", "text": "#292D3E",
        "a1": "#3060c8", "a2": "#407820", "a3": "#7030a8", "a4": "#a07800",
        "a5": "#207890", "a6": "#c05020", "a7": "#c02030", "a8": "#b02868",
        "a9": "#4878d8", "a10": "#508830", "a11": "#8040b8", "a12": "#b08810",
        "a13": "#3088a0", "a14": "#d06030", "a15": "#d03040", "a16": "#c03878",
        "a17": "#6090e0", "a18": "#609840", "a19": "#9050c0", "a20": "#c09820",
    },
    "lace": {
        "base": "#f5f0f8", "surface": "#fdf8ff", "overlay": "#e8e0f0",
        "muted": "#909098", "subtle": "#706878", "text": "#282038",
        "a1": "#3858c0", "a2": "#387818", "a3": "#6828a0", "a4": "#986800",
        "a5": "#187080", "a6": "#b84818", "a7": "#b81828", "a8": "#a82060",
        "a9": "#4868c8", "a10": "#488828", "a11": "#7838b0", "a12": "#a87810",
        "a13": "#288090", "a14": "#c85828", "a15": "#c82838", "a16": "#b83070",
        "a17": "#5878d0", "a18": "#589838", "a19": "#8848c0", "a20": "#b88820",
    },
    "aurora": {
        "base": "#181028", "surface": "#201838", "overlay": "#2e2448",
        "muted": "#605880", "subtle": "#8078a8", "text": "#e8d8ff",
        "a1": "#88b0ff", "a2": "#a8f088", "a3": "#d898ff", "a4": "#fff098",
        "a5": "#88f0ff", "a6": "#ffb888", "a7": "#ff8898", "a8": "#ffb8e8",
        "a9": "#a0c0ff", "a10": "#c0f8a0", "a11": "#e8b0ff", "a12": "#fff8a8",
        "a13": "#a0f8ff", "a14": "#ffc8a0", "a15": "#ff98a8", "a16": "#ffc8f0",
        "a17": "#b8d0ff", "a18": "#d0f8b8", "a19": "#f0c0ff", "a20": "#ffffe0",
    },
}


class palenight:
    """
    Palenight — 20 variants, each with 20 unique accent colours (a1–a20).
    A 20-bar chart will never repeat a colour.

    Variants
    --------
    default · contrast · midnight · abyss · noir · nebula · twilight ·
    rose · dusk · arctic · steel · frost · ash · smoke · pebble ·
    neon · vivid · day · lace · aurora
    """
    VARIANTS = list(_PN)
    COLORS   = _PN

    @staticmethod
    def apply(variant="default", font="jetbrains", font_size_base=13, grid=False,
              font_weight="normal", font_color=None, label_color=None, tick_color=None):
        """
        Apply Palenight theme globally.

        Parameters
        ----------
        variant       : str        one of palenight.VARIANTS
        font          : str | None "jetbrains" | "sourcecodepro" | file path | None
        font_size_base: int        base font size (default 13)
        grid          : bool | "x" | "y"
        font_weight   : str        "normal" | "bold" | "light"  (default "normal")
        font_color    : str | None hex colour — overrides ALL text colour
        label_color   : str | None hex colour — overrides axis label/title only
        tick_color    : str | None hex colour — overrides tick labels only
        """
        if variant not in _PN:
            raise ValueError(f"palenight variant must be one of {palenight.VARIANTS!r}")
        c = _PN[variant]
        plt.rcParams.update(_build_rc(c, _resolve_font(font), font_size_base,
                                      grid, "cool", font_weight,
                                      font_color, label_color, tick_color))
        _store_active("palenight", variant, font, font_size_base, grid,
                      font_weight, font_color, label_color, tick_color)
        return c

    @staticmethod
    def palette(variant="default"):
        if variant not in _PN:
            raise ValueError(f"palenight variant must be one of {palenight.VARIANTS!r}")
        return [_PN[variant][k] for k in _A]

    @staticmethod
    def subplots(*args, variant="default", **kwargs):
        c   = palenight.apply(variant=variant)
        fig, axes = plt.subplots(*args, **kwargs)
        fig.patch.set_facecolor(c["base"])
        return fig, axes

    @staticmethod
    def figure(variant="default", font="jetbrains", font_size_base=13,
               grid=False, font_weight="normal", font_color=None,
               label_color=None, tick_color=None, show=False, **fig_kwargs):
        """One-call themed figure. Returns (c, fig, ax).
        For seaborn use apply() instead. For pure matplotlib use this.
        show=False (default): no blank canvas. show=True: preview empty canvas.
        """
        c = palenight.apply(variant, font=font, font_size_base=font_size_base,
                            grid=grid, font_weight=font_weight,
                            font_color=font_color, label_color=label_color,
                            tick_color=tick_color)
        fig, ax = plt.subplots(**fig_kwargs)
        _apply_ax_theme(ax, fig, c)
        if not show:
            try:
                from matplotlib._pylab_helpers import Gcf
                Gcf.destroy_fig(fig)
            except Exception:
                plt.close(fig)
        return c, fig, ax

    @staticmethod
    def figures(nrows=1, ncols=1, variant="default", font="jetbrains",
                font_size_base=13, grid=False, font_weight="normal",
                font_color=None, label_color=None, tick_color=None,
                **fig_kwargs):
        """One-call themed multi-axes figure. Returns (c, fig, axes)."""
        c = palenight.apply(variant, font=font, font_size_base=font_size_base,
                            grid=grid, font_weight=font_weight,
                            font_color=font_color, label_color=label_color,
                            tick_color=tick_color)
        fig, axes = plt.subplots(nrows, ncols, **fig_kwargs)
        fig.patch.set_facecolor(c["base"])
        ax_list = axes.flatten() if hasattr(axes, "flatten") else [axes]
        for ax in ax_list:
            _apply_ax_theme(ax, fig, c)
        return c, fig, axes

    @staticmethod
    def help():
        """Print all apply() parameters for palenight."""
        print("\n  hv.palenight.apply() parameters")
        print("  " + "─"*40)
        params = [
            ("variant",        str(palenight.VARIANTS)),
            ("font",           "jetbrains | sourcecodepro | cascadia | fira_code | hack | microsoft_sans | operator_mono | roboto | None"),
            ("font_size_base", "int  — default 13"),
            ("font_weight",    "normal | bold | light"),
            ("grid",           "False | True | x | y"),
            ("font_color",     "#rrggbb  — overrides all text"),
            ("label_color",    "#rrggbb  — axis labels & title only"),
            ("tick_color",     "#rrggbb  — tick labels only"),
        ]
        for param, desc in params:
            print(f"    {param:<18}  {desc}")
        print()