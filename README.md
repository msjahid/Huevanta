# Huevanta

**Three beautiful Matplotlib themes — Rosé Pine · Dracula · Palenight**
Each theme has **20 variants** × **20 unique accent colours**.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Info & Help](#info--help)
4. [Themes & Variants](#themes--variants)
5. [apply() — full parameter reference](#apply--full-parameter-reference)
6. [palette()](#palette)
7. [subplots()](#subplots)
8. [Font Guide](#font-guide)
9. [Grid Control](#grid-control)
10. [Font Styling](#font-styling)
11. [Works with Seaborn](#works-with-seaborn)
12. [Legend Customisation](#legend-customisation)
13. [Real Example](#real-example)

---

## Installation

````bash
pip install # Huevanta

**Three beautiful Matplotlib themes — Rosé Pine · Dracula · Palenight**
Each theme has **20 variants** × **20 unique accent colours**.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Info & Help](#info--help)
4. [Themes & Variants](#themes--variants)
5. [apply() — full parameter reference](#apply--full-parameter-reference)
6. [palette()](#palette)
7. [subplots()](#subplots)
8. [Font Guide](#font-guide)
9. [Grid Control](#grid-control)
10. [Font Styling](#font-styling)
11. [Works with Seaborn](#works-with-seaborn)
12. [Legend Customisation](#legend-customisation)
13. [Real Example](#real-example)

---

## Installation

```bash
pip install Huevanta
````

Add fonts to the package folder (optional but recommended):

```
huevanta/
└── fonts/
    ├── JetBrainsMono-Regular.ttf
    ├── SourceCodePro-Regular.ttf
    ├── CascadiaCode.ttf
    ├── Fira Code Regular 400.ttf
    ├── Hack-Regular.ttf
    ├── Microsoft Sans Serif.ttf
    ├── Operator Mono Book Regular.otf
    └── Roboto-Regular.ttf
```

Download sources:

- JetBrains Mono → https://github.com/JetBrains/JetBrainsMono/releases
- Source Code Pro → https://github.com/adobe-fonts/source-code-pro/releases
- Cascadia Code → https://github.com/microsoft/cascadia-code/releases
- Fira Code → https://github.com/tonsky/FiraCode/releases
- Hack → https://github.com/source-foundry/Hack/releases
- Roboto → https://fontsgoogle.com/specimen/Roboto

---

## Quick Start

```python
import huevanta as hv
import matplotlib.pyplot as plt
import numpy as np

# 1. Apply a theme ONCE at the top
hvrosepine.apply("moon")

# 2. Get the 20 accent colours
pal = hvrosepine.palette("moon")

# 3. Plot normally — theme is applied globally
x = np.linspace(0, 2 * np.pi, 100)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, np.sin(x), color=pal[0], label="sin")
ax.plot(x, np.cos(x), color=pal[1], label="cos")
ax.legend()
plt.show()
```

---

## Info & Help

```python
import huevanta as hv

# package version & author
print(hv__version__)          # 0.1.0
print(hv__author__)           # Jahid Hasan

# theme list
print(hv__all__)
# ['rosepine', 'dracula', 'palenight']

# variant lists per theme
print(hvrosepine.VARIANTS)    # list of 20 variant names
print(hvdracula.VARIANTS)     # list of 20 variant names
print(hvpalenight.VARIANTS)   # list of 20 variant names

# font list
print(list(hv_BUNDLED_FONTSkeys()))
# ['jetbrains', 'sourcecodepro', 'cascadia', 'fira_code',
#  'hack', 'microsoft_sans', 'operator_mono', 'roboto']

# full reference — themes, variants, fonts, params
hvinfo()

# per-theme parameter reference
hvrosepine.help()
hvdracula.help()
hvpalenight.help()
```

---

## Themes & Variants

### Rosé Pine — 20 variants

| #   | Variant     | Style                |
| --- | ----------- | -------------------- |
| 1   | `main`      | dark original        |
| 2   | `moon`      | softer dark          |
| 3   | `dawn`      | light                |
| 4   | `midnight`  | deep dark            |
| 5   | `ember`     | warm dark            |
| 6   | `slate`     | cool grey dark       |
| 7   | `forest`    | green dark           |
| 8   | `desert`    | warm sand dark       |
| 9   | `ocean`     | deep blue dark       |
| 10  | `lavender`  | purple dark          |
| 11  | `crimson`   | red dark             |
| 12  | `teal`      | teal dark            |
| 13  | `sunset`    | orange warm dark     |
| 14  | `mono`      | monochrome dark      |
| 15  | `quartz`    | pink dark            |
| 16  | `aurora`    | northern lights dark |
| 17  | `parchment` | warm light           |
| 18  | `linen`     | soft light           |
| 19  | `neon`      | electric dark        |
| 20  | `cosmos`    | deep violet dark     |

### Dracula — 20 variants

`classic` · `soft` · `ink` · `blood` · `storm` · `toxic` · `amber` ·
`synthwave` · `volcanic` · `arctic` · `cyber` · `coffee` · `rose` ·
`void` · `galaxy` · `silver` · `jungle` · `velvet` · `neon` · `paper`

### Palenight — 20 variants

`default` · `contrast` · `midnight` · `abyss` · `noir` · `nebula` ·
`twilight` · `rose` · `dusk` · `arctic` · `steel` · `frost` · `ash` ·
`smoke` · `pebble` · `neon` · `vivid` · `day` · `lace` · `aurora`

---

## apply() — full parameter reference

```python
hvrosepine.apply(
    variant        = "moon",        # which colour palette to use
    font           = "jetbrains",   # which font to use
    font_size_base = 13,            # base font size in points
    font_weight    = "normal",      # text weight
    grid           = False,         # grid lines
    font_color     = None,          # override ALL text colour
    label_color    = None,          # override axis labels & title only
    tick_color     = None,          # override tick labels only
)
```

### variant

```python
hvrosepine.apply("main")
hvrosepine.apply("moon")
hvrosepine.apply("dawn")
hvdracula.apply("classic")
hvdracula.apply("synthwave")
hvpalenight.apply("default")
hvpalenight.apply("nebula")
```

### font

```python
hvrosepine.apply("moon", font="jetbrains")        # JetBrains Mono (default)
hvrosepine.apply("moon", font="sourcecodepro")    # Source Code Pro
hvrosepine.apply("moon", font="cascadia")         # Cascadia Code
hvrosepine.apply("moon", font="fira_code")        # Fira Code
hvrosepine.apply("moon", font="hack")             # Hack
hvrosepine.apply("moon", font="microsoft_sans")   # Microsoft Sans Serif
hvrosepine.apply("moon", font="operator_mono")    # Operator Mono
hvrosepine.apply("moon", font="roboto")           # Roboto
hvrosepine.apply("moon", font="fonts/MyFont.ttf") # your own font file
hvrosepine.apply("moon", font=None)               # Matplotlib default
```

### font_size_base

```python
hvdracula.apply("classic", font_size_base=10)   # small
hvdracula.apply("classic", font_size_base=13)   # default
hvdracula.apply("classic", font_size_base=16)   # large
# tick labels = 85% of base,  title = 115% of base
```

### font_weight

```python
hvrosepine.apply("moon", font_weight="normal")  # default
hvrosepine.apply("moon", font_weight="bold")    # bold everywhere
hvrosepine.apply("moon", font_weight="light")   # light everywhere
```

### grid

```python
hvrosepine.apply("moon", grid=False)   # off — default
hvrosepine.apply("moon", grid=True)    # both axes
hvrosepine.apply("moon", grid="x")     # vertical lines only
hvrosepine.apply("moon", grid="y")     # horizontal lines only
```

### font_color / label_color / tick_color

```python
# override ALL text at once
hvdracula.apply("classic", font_color="#ffffff")

# override specific parts independently
hvdracula.apply("classic",
    label_color = "#ff79c6",   # axis labels & title
    tick_color  = "#8be9fd",   # tick labels
)

# combine all three
hvdracula.apply("classic",
    font_color  = "#f8f8f2",
    label_color = "#ff79c6",
    tick_color  = "#8be9fd",
)
```

---

## palette()

Returns a list of **20 unique hex strings** for the given variant.

```python
pal = hvrosepine.palette("moon")
# ['#eb6f92', '#9ccfd8', '#f6c177', '#c4a7e7', ...]  — 20 colours

pal = hvdracula.palette("classic")
pal = hvpalenight.palette("nebula")

# use slices for different chart types
ax.bar(cats, vals, color=pal[:6])       # 6 bars — 6 colours
ax.plot(x, y,      color=pal[0])        # 1 line
ax.scatter(x, y,   color=pal[3])        # scatter
for i in range(4):
    ax.plot(x, data[i], color=pal[i])   # 4 lines — 4 colours
```

---

## subplots()

Applies the theme and creates the figure in one call.

```python
# basic
fig, ax = hvrosepine.subplots(variant="moon")

# with layout
fig, axes = hvdracula.subplots(2, 2, variant="classic", figsize=(12, 8))

# with all params
fig, ax = hvpalenight.subplots(
    1, 2,
    variant        = "nebula",
    font           = "fira_code",
    font_size_base = 14,
    font_weight    = "bold",
    figsize        = (12, 5),
)
```

---

## Font Guide

Font recommendations by use case:

| Use case                  | Recommended font           |
| ------------------------- | -------------------------- |
| Data science / code plots | `jetbrains` or `fira_code` |
| Academic / reports        | `sourcecodepro`            |
| Modern dashboards         | `roboto` or `cascadia`     |
| Terminal aesthetic        | `hack`                     |
| General purpose           | `jetbrains` (default)      |

```python
# check which fonts are available
print(list(hv_BUNDLED_FONTSkeys()))

# apply with font
hvrosepine.apply("moon", font="fira_code")
```

---

## Grid Control

Always start with `grid=False`, then toggle per axis:

```python
hvrosepine.apply("moon", grid=False)   # global default off

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))

ax1.grid(True)             # both axes on
ax2.grid(True, axis="y")   # horizontal only
ax3.grid(False)            # off — no call needed
```

---

## Font Styling

```python
# bold everything
hvdracula.apply("classic", font_weight="bold")

# large font
hvdracula.apply("classic", font_size_base=16)

# custom colours
hvdracula.apply("classic",
    label_color = "#ff79c6",   # axis labels & title
    tick_color  = "#8be9fd",   # tick labels
)

# all controls together
hvrosepine.apply(
    "moon",
    font           = "fira_code",
    font_size_base = 14,
    font_weight    = "bold",
    font_color     = "#e0def4",
    label_color    = "#eb6f92",
    tick_color     = "#9ccfd8",
    grid           = False,
)
```

---

## Works with Seaborn

```python
import seaborn as sns
import huevanta as hv

hvdracula.apply("classic", grid=False)
pal = hvdracula.palette("classic")

# pass palette=pal[:n]  where n = number of hue groups
sns.scatterplot(data=df, x="x",   y="y",   hue="group",  palette=pal[:3])
sns.boxplot(    data=df, x="day", y="val",               palette=pal[:4])
sns.histplot(   data=df, x="val", hue="time", kde=True,  palette=pal[:2])
sns.violinplot( data=df, x="day", y="tip",               palette=pal[:4])
sns.barplot(    data=df, x="cat", y="val",               palette=pal[:5])
```

---

## Legend Customisation

`apply()` sets global defaulhv Customise per-plot directly via Matplotlib:

```python
hvrosepine.apply("moon", grid=False)
pal = hvrosepine.palette("moon")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, np.sin(x), color=pal[0], label="sin")
ax.plot(x, np.cos(x), color=pal[1], label="cos")

ax.legend(
    loc            = "upper right",   # position
    fontsize       = 12,              # font size
    title          = "Functions",     # legend title
    title_fontsize = 13,
    facecolor      = "#282A36",       # background colour
    edgecolor      = "#ff79c6",       # border colour
    labelcolor     = "#f8f8f2",       # text colour
    framealpha     = 0.9,
    ncols          = 2,               # number of columns
)
plt.show()
```

---

## Real Example

```python
import huevanta as hv
import matplotlib.pyplot as plt
import numpy as np

# apply theme once at the top
hvrosepine.apply(
    "moon",
    font           = "jetbrains",
    font_size_base = 13,
    font_weight    = "normal",
    grid           = False,
)
pal = hvrosepine.palette("moon")

# data
tree_number = [10, 5, 15, 8, 6, 1, 13]
tree_name   = ['Orange','Banana','Litchi','Guava','Mango','Apple','Cherries']
tree_pos    = np.arange(len(tree_name))

# plot
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(tree_pos, tree_number, color=pal[:7], zorder=2)
ax.set_xticks(tree_pos)
ax.set_xticklabels(tree_name)
ax.set_title("Tree Count by Fruit")
ax.set_xlabel("Fruit")
ax.set_ylabel("Count")
ax.grid(True, axis="y")

# value labels on bars
for bar, val in zip(bars, tree_number):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.2,
            str(val), ha="center", va="bottom", fontsize=10)

plt.tight_layout()
plt.show()
```

---

## License

MIT — Jahid Hasan

```

Add fonts to the package folder (optional but recommended):

```

huevanta/
└── fonts/
├── JetBrainsMono-Regular.ttf
├── SourceCodePro-Regular.ttf
├── CascadiaCode.ttf
├── Fira Code Regular 400.ttf
├── Hack-Regular.ttf
├── Microsoft Sans Serif.ttf
├── Operator Mono Book Regular.otf
└── Roboto-Regular.ttf

````

Download sources:

- JetBrains Mono → https://github.com/JetBrains/JetBrainsMono/releases
- Source Code Pro → https://github.com/adobe-fonts/source-code-pro/releases
- Cascadia Code → https://github.com/microsoft/cascadia-code/releases
- Fira Code → https://github.com/tonsky/FiraCode/releases
- Hack → https://github.com/source-foundry/Hack/releases
- Roboto → https://fontsgoogle.com/specimen/Roboto

---

## Quick Start

```python
import huevanta as hv
import matplotlib.pyplot as plt
import numpy as np

# 1. Apply a theme ONCE at the top
hvrosepine.apply("moon")

# 2. Get the 20 accent colours
pal = hvrosepine.palette("moon")

# 3. Plot normally — theme is applied globally
x = np.linspace(0, 2 * np.pi, 100)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, np.sin(x), color=pal[0], label="sin")
ax.plot(x, np.cos(x), color=pal[1], label="cos")
ax.legend()
plt.show()
````

---

## Info & Help

```python
import huevanta as hv

# package version & author
print(hv__version__)          # 0.1
print(hv__author__)           # Jahid Hasan

# theme list
print(hv__all__)
# ['rosepine', 'dracula', 'palenight']

# variant lists per theme
print(hvrosepine.VARIANTS)    # list of 20 variant names
print(hvdracula.VARIANTS)     # list of 20 variant names
print(hvpalenight.VARIANTS)   # list of 20 variant names

# font list
print(list(hv_BUNDLED_FONTSkeys()))
# ['jetbrains', 'sourcecodepro', 'cascadia', 'fira_code',
#  'hack', 'microsoft_sans', 'operator_mono', 'roboto']

# full reference — themes, variants, fonts, params
hvinfo()

# per-theme parameter reference
hvrosepine.help()
hvdracula.help()
hvpalenight.help()
```

---

## Themes & Variants

### Rosé Pine — 20 variants

| #   | Variant     | Style                |
| --- | ----------- | -------------------- |
| 1   | `main`      | dark original        |
| 2   | `moon`      | softer dark          |
| 3   | `dawn`      | light                |
| 4   | `midnight`  | deep dark            |
| 5   | `ember`     | warm dark            |
| 6   | `slate`     | cool grey dark       |
| 7   | `forest`    | green dark           |
| 8   | `desert`    | warm sand dark       |
| 9   | `ocean`     | deep blue dark       |
| 10  | `lavender`  | purple dark          |
| 11  | `crimson`   | red dark             |
| 12  | `teal`      | teal dark            |
| 13  | `sunset`    | orange warm dark     |
| 14  | `mono`      | monochrome dark      |
| 15  | `quartz`    | pink dark            |
| 16  | `aurora`    | northern lights dark |
| 17  | `parchment` | warm light           |
| 18  | `linen`     | soft light           |
| 19  | `neon`      | electric dark        |
| 20  | `cosmos`    | deep violet dark     |

### Dracula — 20 variants

`classic` · `soft` · `ink` · `blood` · `storm` · `toxic` · `amber` ·
`synthwave` · `volcanic` · `arctic` · `cyber` · `coffee` · `rose` ·
`void` · `galaxy` · `silver` · `jungle` · `velvet` · `neon` · `paper`

### Palenight — 20 variants

`default` · `contrast` · `midnight` · `abyss` · `noir` · `nebula` ·
`twilight` · `rose` · `dusk` · `arctic` · `steel` · `frost` · `ash` ·
`smoke` · `pebble` · `neon` · `vivid` · `day` · `lace` · `aurora`

---

## apply() — full parameter reference

```python
hvrosepine.apply(
    variant        = "moon",        # which colour palette to use
    font           = "jetbrains",   # which font to use
    font_size_base = 13,            # base font size in points
    font_weight    = "normal",      # text weight
    grid           = False,         # grid lines
    font_color     = None,          # override ALL text colour
    label_color    = None,          # override axis labels & title only
    tick_color     = None,          # override tick labels only
)
```

### variant

```python
hvrosepine.apply("main")
hvrosepine.apply("moon")
hvrosepine.apply("dawn")
hvdracula.apply("classic")
hvdracula.apply("synthwave")
hvpalenight.apply("default")
hvpalenight.apply("nebula")
```

### font

```python
hvrosepine.apply("moon", font="jetbrains")        # JetBrains Mono (default)
hvrosepine.apply("moon", font="sourcecodepro")    # Source Code Pro
hvrosepine.apply("moon", font="cascadia")         # Cascadia Code
hvrosepine.apply("moon", font="fira_code")        # Fira Code
hvrosepine.apply("moon", font="hack")             # Hack
hvrosepine.apply("moon", font="microsoft_sans")   # Microsoft Sans Serif
hvrosepine.apply("moon", font="operator_mono")    # Operator Mono
hvrosepine.apply("moon", font="roboto")           # Roboto
hvrosepine.apply("moon", font="fonts/MyFont.ttf") # your own font file
hvrosepine.apply("moon", font=None)               # Matplotlib default
```

### font_size_base

```python
hvdracula.apply("classic", font_size_base=10)   # small
hvdracula.apply("classic", font_size_base=13)   # default
hvdracula.apply("classic", font_size_base=16)   # large
# tick labels = 85% of base,  title = 115% of base
```

### font_weight

```python
hvrosepine.apply("moon", font_weight="normal")  # default
hvrosepine.apply("moon", font_weight="bold")    # bold everywhere
hvrosepine.apply("moon", font_weight="light")   # light everywhere
```

### grid

```python
hvrosepine.apply("moon", grid=False)   # off — default
hvrosepine.apply("moon", grid=True)    # both axes
hvrosepine.apply("moon", grid="x")     # vertical lines only
hvrosepine.apply("moon", grid="y")     # horizontal lines only
```

### font_color / label_color / tick_color

```python
# override ALL text at once
hvdracula.apply("classic", font_color="#ffffff")

# override specific parts independently
hvdracula.apply("classic",
    label_color = "#ff79c6",   # axis labels & title
    tick_color  = "#8be9fd",   # tick labels
)

# combine all three
hvdracula.apply("classic",
    font_color  = "#f8f8f2",
    label_color = "#ff79c6",
    tick_color  = "#8be9fd",
)
```

---

## palette()

Returns a list of **20 unique hex strings** for the given variant.

```python
pal = hvrosepine.palette("moon")
# ['#eb6f92', '#9ccfd8', '#f6c177', '#c4a7e7', ...]  — 20 colours

pal = hvdracula.palette("classic")
pal = hvpalenight.palette("nebula")

# use slices for different chart types
ax.bar(cats, vals, color=pal[:6])       # 6 bars — 6 colours
ax.plot(x, y,      color=pal[0])        # 1 line
ax.scatter(x, y,   color=pal[3])        # scatter
for i in range(4):
    ax.plot(x, data[i], color=pal[i])   # 4 lines — 4 colours
```

---

## subplots()

Applies the theme and creates the figure in one call.

```python
# basic
fig, ax = hvrosepine.subplots(variant="moon")

# with layout
fig, axes = hvdracula.subplots(2, 2, variant="classic", figsize=(12, 8))

# with all params
fig, ax = hvpalenight.subplots(
    1, 2,
    variant        = "nebula",
    font           = "fira_code",
    font_size_base = 14,
    font_weight    = "bold",
    figsize        = (12, 5),
)
```

---

## Font Guide

Font recommendations by use case:

| Use case                  | Recommended font           |
| ------------------------- | -------------------------- |
| Data science / code plots | `jetbrains` or `fira_code` |
| Academic / reports        | `sourcecodepro`            |
| Modern dashboards         | `roboto` or `cascadia`     |
| Terminal aesthetic        | `hack`                     |
| General purpose           | `jetbrains` (default)      |

```python
# check which fonts are available
print(list(hv_BUNDLED_FONTSkeys()))

# apply with font
hvrosepine.apply("moon", font="fira_code")
```

---

## Grid Control

Always start with `grid=False`, then toggle per axis:

```python
hvrosepine.apply("moon", grid=False)   # global default off

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))

ax1.grid(True)             # both axes on
ax2.grid(True, axis="y")   # horizontal only
ax3.grid(False)            # off — no call needed
```

---

## Font Styling

```python
# bold everything
hvdracula.apply("classic", font_weight="bold")

# large font
hvdracula.apply("classic", font_size_base=16)

# custom colours
hvdracula.apply("classic",
    label_color = "#ff79c6",   # axis labels & title
    tick_color  = "#8be9fd",   # tick labels
)

# all controls together
hvrosepine.apply(
    "moon",
    font           = "fira_code",
    font_size_base = 14,
    font_weight    = "bold",
    font_color     = "#e0def4",
    label_color    = "#eb6f92",
    tick_color     = "#9ccfd8",
    grid           = False,
)
```

---

## Works with Seaborn

```python
import seaborn as sns
import huevanta as hv

hvdracula.apply("classic", grid=False)
pal = hvdracula.palette("classic")

# pass palette=pal[:n]  where n = number of hue groups
sns.scatterplot(data=df, x="x",   y="y",   hue="group",  palette=pal[:3])
sns.boxplot(    data=df, x="day", y="val",               palette=pal[:4])
sns.histplot(   data=df, x="val", hue="time", kde=True,  palette=pal[:2])
sns.violinplot( data=df, x="day", y="tip",               palette=pal[:4])
sns.barplot(    data=df, x="cat", y="val",               palette=pal[:5])
```

---

## Legend Customisation

`apply()` sets global defaulhv Customise per-plot directly via Matplotlib:

```python
hvrosepine.apply("moon", grid=False)
pal = hvrosepine.palette("moon")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, np.sin(x), color=pal[0], label="sin")
ax.plot(x, np.cos(x), color=pal[1], label="cos")

ax.legend(
    loc            = "upper right",   # position
    fontsize       = 12,              # font size
    title          = "Functions",     # legend title
    title_fontsize = 13,
    facecolor      = "#282A36",       # background colour
    edgecolor      = "#ff79c6",       # border colour
    labelcolor     = "#f8f8f2",       # text colour
    framealpha     = 0.9,
    ncols          = 2,               # number of columns
)
plt.show()
```

---

## Real Example

```python
import huevanta as hv
import matplotlib.pyplot as plt
import numpy as np

# apply theme once at the top
hvrosepine.apply(
    "moon",
    font           = "jetbrains",
    font_size_base = 13,
    font_weight    = "normal",
    grid           = False,
)
pal = hvrosepine.palette("moon")

# data
tree_number = [10, 5, 15, 8, 6, 1, 13]
tree_name   = ['Orange','Banana','Litchi','Guava','Mango','Apple','Cherries']
tree_pos    = np.arange(len(tree_name))

# plot
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(tree_pos, tree_number, color=pal[:7], zorder=2)
ax.set_xticks(tree_pos)
ax.set_xticklabels(tree_name)
ax.set_title("Tree Count by Fruit")
ax.set_xlabel("Fruit")
ax.set_ylabel("Count")
ax.grid(True, axis="y")

# value labels on bars
for bar, val in zip(bars, tree_number):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.2,
            str(val), ha="center", va="bottom", fontsize=10)

plt.tight_layout()
plt.show()
```

---

## License

MIT — Jahid Hasan
