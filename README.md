# Huevanta

> Three beautiful Matplotlib themes — **Rosé Pine**, **Dracula**, **Palenight** —  
> each with **20 hand-crafted variants** and **20 unique accent colours** per variant.

A 20-bar chart will never repeat a colour. Works with **Matplotlib** and **Seaborn** globally — one call themes everything.

---

## Installation

```bash
pip install huevanta
```

---

## Quick Start

```python
import huevanta as hv
import seaborn as sns
import matplotlib.pyplot as plt

# one call — sets theme globally for ALL plots in the notebook
c = hv.rosepine.apply("dawn")
pal = hv.rosepine.palette("dawn")

# seaborn just works — no extra setup per cell
sns.countplot(x='meal_type', data=df, palette=pal)
plt.title("Meal Type", color=c['text'])
plt.xlabel("Meal Type")
plt.ylabel("Count")
plt.show()
```

---

## Themes & Variants

### 🌸 Rosé Pine — soft, romantic, botanical

| Variant     | Style               |
| ----------- | ------------------- |
| `main`      | classic dark purple |
| `moon`      | deep blue-purple    |
| `dawn`      | warm cream light    |
| `midnight`  | extreme dark        |
| `ember`     | warm amber dark     |
| `slate`     | cool blue-grey dark |
| `forest`    | deep green dark     |
| `desert`    | warm sand dark      |
| `ocean`     | deep navy dark      |
| `lavender`  | soft purple dark    |
| `crimson`   | deep red dark       |
| `teal`      | deep teal dark      |
| `sunset`    | warm orange dark    |
| `mono`      | pure greyscale      |
| `quartz`    | pink-rose dark      |
| `aurora`    | deep blue dark      |
| `parchment` | antique paper light |
| `linen`     | warm linen light    |
| `neon`      | electric dark       |
| `cosmos`    | deep violet dark    |

### 🧛 Dracula — bold, high-contrast, neon-gothic

`classic` · `soft` · `ink` · `blood` · `storm` · `toxic` · `amber` · `synthwave` · `volcanic` · `arctic` · `cyber` · `coffee` · `rose` · `void` · `galaxy` · `silver` · `jungle` · `velvet` · `neon` · `paper`

### 🌙 Palenight — deep indigo nights, cool blues

`default` · `contrast` · `midnight` · `abyss` · `noir` · `nebula` · `twilight` · `rose` · `dusk` · `arctic` · `steel` · `frost` · `ash` · `smoke` · `pebble` · `neon` · `vivid` · `day` · `lace` · `aurora`

---

## API Reference

### `apply()` — set theme globally

```python
c = hv.rosepine.apply(
    variant        = "dawn",        # variant name
    font           = "jetbrains",   # bundled font name or file path
    font_size_base = 13,            # base font size (default 13)
    font_weight    = "normal",      # "normal" | "bold" | "light"
    grid           = False,         # False | True | "x" | "y"
    font_color     = None,          # overrides ALL text colour
    label_color    = None,          # overrides axis labels + title only
    tick_color     = None,          # overrides tick numbers only
)
```

Returns `c` — a dict of all theme colours for that variant.

### `palette()` — get accent colours

```python
pal = hv.rosepine.palette("dawn")   # list of 20 unique hex colours
```

Pass directly to seaborn's `palette=pal` or matplotlib's `color=pal[:6]`.

### `figure()` — themed figure for pure matplotlib

```python
c, fig, ax = hv.rosepine.figure(
    "dawn",
    figsize = (10, 5),
    show    = False,    # True = preview empty canvas, False = no blank canvas
)
ax.bar(x, y, color=pal[:4])
ax.set_title("My Chart", color=c['text'])
plt.show()
```

### `figures()` — themed multi-axes figure

```python
c, fig, axes = hv.rosepine.figures(
    1, 3,               # nrows, ncols
    variant = "dawn",
    figsize = (15, 5),
)
axes[0].bar(x, y, color=pal[:4])
plt.show()
```

### `reapply()` — re-apply theme if reset by a library

```python
hv.reapply()
```

Normally not needed — the auto-hook handles everything. Only call this if a library explicitly resets `rcParams` after `apply()`.

---

## Colour Overrides

`font_color`, `label_color`, and `tick_color` accept either:

- A **hex string** — `"#ff0000"`
- A **theme colour key name** — any of the keys below

### Theme colour keys

| Key              | Role                                  |
| ---------------- | ------------------------------------- |
| `"base"`         | figure background                     |
| `"surface"`      | axes background                       |
| `"overlay"`      | borders, spines                       |
| `"muted"`        | de-emphasised text                    |
| `"subtle"`       | secondary text, labels                |
| `"text"`         | primary text                          |
| `"a1"` – `"a20"` | accent colours (bars, lines, patches) |

```python
# use theme key names directly
c = hv.rosepine.apply("dawn", font_color="text")      # primary text colour
c = hv.rosepine.apply("dawn", label_color="a1")       # first accent for labels
c = hv.rosepine.apply("dawn", tick_color="muted")     # muted for tick numbers

# or use raw hex
c = hv.rosepine.apply("dawn", font_color="#8b0000")
```

---

## Bundled Fonts

| Key                | Font                     |
| ------------------ | ------------------------ |
| `"jetbrains"`      | JetBrains Mono (default) |
| `"sourcecodepro"`  | Source Code Pro          |
| `"cascadia"`       | Cascadia Code            |
| `"fira_code"`      | Fira Code                |
| `"hack"`           | Hack                     |
| `"microsoft_sans"` | Microsoft Sans Serif     |
| `"operator_mono"`  | Operator Mono            |
| `"roboto"`         | Roboto                   |

```python
hv.rosepine.apply("moon", font="fira_code")
hv.rosepine.apply("moon", font="path/to/MyFont.ttf")   # custom font
hv.rosepine.apply("moon", font=None)                   # matplotlib default
```

---

## Seaborn Workflow

```python
import huevanta as hv
import seaborn as sns
import matplotlib.pyplot as plt

# Cell 1 — run once at the top of your notebook
c = hv.rosepine.apply("dawn", font="jetbrains", font_size_base=13, grid=False)
pal = hv.rosepine.palette("dawn")

# Cell 2 — just plot
sns.countplot(x='meal_type', data=df, palette=pal)
plt.title("Meal Type", color=c['text'])
plt.xlabel("Meal Type")
plt.ylabel("Count")
plt.grid(True, axis='y')
plt.show()

# Cell 3 — still themed, no setup needed
sns.barplot(x='restaurant_type', y='price', data=df, palette=pal)
plt.title("Price by Restaurant", color=c['text'])
plt.show()

# Cell 4 — pure matplotlib also themed automatically
plt.bar(x, y, color=pal[:4])
plt.title("My Chart", color=c['text'])
plt.show()
```

---

## Pure Matplotlib Workflow

```python
c, fig, ax = hv.rosepine.figure("moon", figsize=(10, 5))
pal = hv.rosepine.palette("moon")

ax.plot(x, y, color=pal[0], linewidth=2)
ax.set_title("My Line Chart", color=c['text'])
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
plt.show()
```

---

## Grid Options

```python
# no grid (default)
hv.rosepine.apply("dawn", grid=False)

# grid on both axes
hv.rosepine.apply("dawn", grid=True)

# grid on y axis only
hv.rosepine.apply("dawn", grid="y")

# grid on x axis only
hv.rosepine.apply("dawn", grid="x")

# or override per plot
plt.grid(True, axis='y')
```

Grid colour is automatically chosen for visibility — `muted` on light themes, `subtle` on dark themes.

---

## Access Raw Colours

```python
c = hv.rosepine.apply("dawn")

c['text']      # primary text colour
c['base']      # figure background
c['surface']   # axes background
c['muted']     # de-emphasised colour
c['a1']        # first accent colour
c['a5']        # fifth accent colour

# use in plots
plt.title("My Chart", color=c['text'])
plt.axhline(y=0, color=c['muted'], linestyle='--')
ax.bar(x, y, color=c['a1'])
```

---

## Print Full Reference

```python
import huevanta as hv
hv.info()               # full reference — all themes, variants, fonts
hv.rosepine.help()      # rosepine parameters
hv.dracula.help()       # dracula parameters
hv.palenight.help()     # palenight parameters
```

---

## Requirements

- Python ≥ 3.10
- matplotlib ≥ 3.5
- seaborn ≥ 0.12 _(optional)_

---

## Links

- GitHub: [github.com/msjahid/Huevanta](https://github.com/msjahid/Huevanta)
- Issues: [github.com/msjahid/Huevanta/issues](https://github.com/msjahid/Huevanta/issues)

---

_MIT License — Jahid Hasan_
