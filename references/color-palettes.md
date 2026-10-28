# Color Palettes — Configuration & Best Practices

## Table of Contents
- [Palette Philosophy](#palette-philosophy)
- [Included Palettes](#included-palettes)
- [Custom Palette Creation](#custom-palette-creation)
- [Color Accessibility](#color-accessibility)
- [Palette Selection Guide](#palette-selection-guide)

---

## Palette Philosophy

### Design goals
1. **Maximize distinguishability** — adjacent semantic units must be visually distinct
2. **Maintain readability** — colors must have sufficient contrast against white/black backgrounds
3. **Support RTL/LTR mixing** — colors should work regardless of text direction
4. **Scale gracefully** — from 5 to 50+ distinct colors per document

### Color assignment strategy
- Colors assigned **per semantic group**, not per word
- Word → lexicon lookup → reuse existing color if found
- New word → next unused palette color
- Exhaustion → recycling (colors reused for units far apart) or numeric fallback

---

## Included Palettes

### 1. Default (`default.json`)
- 30 colors, balanced for general use
- Optimized for 15-25 unique units per document (typical song/poem)
- Moderate saturation, good on white backgrounds
- File: `assets/palettes/default.json`

### 2. High Contrast (`high-contrast.json`)
- 30 colors with maximum perceptual distance
- For documents with many similar-looking units
- Higher saturation, darker tones
- Better for print
- File: `assets/palettes/high-contrast.json`

### 3. Pastel (`pastel.json`)
- 30 soft, muted colors
- Good for extended reading (less visual fatigue)
- Better for screen/digital use
- File: `assets/palettes/pastel.json`

---

## Custom Palette Creation

### JSON format
```json
{
    "name": "my-custom-palette",
    "description": "Description of this palette",
    "colors": [
        "#RRGGBB",
        "#RRGGBB",
        ...
    ],
    "metadata": {
        "colorblind_safe": false,
        "min_contrast_ratio": 4.5,
        "max_colors": 30,
        "background": "#FFFFFF"
    }
}
```

### Requirements
- Minimum 10 colors
- Recommended 20-30 colors
- Each color: valid 6-digit hex
- `min_contrast_ratio`: WCAG AA requires 4.5:1 for normal text

### Placement
Place custom palette JSON files in `assets/palettes/` and reference by filename stem:
```bash
python scripts/color_engine.py assign --data "..." --palette my-custom-palette
```

---

## Color Accessibility

### Colorblind-safe considerations

~8% of males have some form of color vision deficiency:
- **Deuteranopia** (green-blind): ~5%
- **Protanopia** (red-blind): ~2%
- **Tritanopia** (blue-blind): <1%

### Strategies for accessibility

1. **High-contrast palette**: Uses luminance differences in addition to hue
2. **Pattern overlay**: Optional `[color + pattern]` dual encoding
   - Underline style (solid, dashed, dotted, wavy)
   - Background pattern (stripes, dots, hatching)
3. **Numeric fallback**: When colors are insufficient, add numeric tags
   ```
   <1>Khoda</1> = <1>God</1>
   <2>hafez</2> = <2>再见</2>
   ```

### WCAG compliance
Target WCAG 2.1 AA:
- Normal text: contrast ratio ≥ 4.5:1
- Large text (≥18pt): contrast ratio ≥ 3:1

---

## Palette Selection Guide

| Use Case | Recommended Palette | Why |
|----------|-------------------|-----|
| Song lyrics (10-30 unique words) | Default | Balanced, good color variety |
| Long text (50+ unique words) | High Contrast | Maximizes distinguishability |
| Reading-focused material | Pastel | Less eye strain for extended reading |
| Print output | High Contrast | Colors survive CMYK conversion better |
| Screen/digital | Default or Pastel | RGB-native, good on backlit screens |
| Colorblind users | High Contrast + pattern overlay | Luminance differences help |
| Academic/formal | Default (restrained) | Less visually aggressive |
| Children's materials | Pastel | Softer, more inviting |
