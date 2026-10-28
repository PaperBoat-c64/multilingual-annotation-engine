# RTL Layout Engine — Complete Specification

## Table of Contents
- [Core Principles](#core-principles)
- [Direction Detection](#direction-detection)
- [CSS RTL Rules](#css-rtl-rules)
- [Component-Level Mirroring](#component-level-mirroring)
- [RTL Typography](#rtl-typography)
- [RTL Tooltip Positioning](#rtl-tooltip-positioning)
- [RTL Dictionary Cards](#rtl-dictionary-cards)
- [RTL Selection Behavior](#rtl-selection-behavior)
- [Testing Checklist](#testing-checklist)

---

## Core Principles

1. **RTL is not "LTR mirrored."** Layout direction is a first-class property, not an afterthought.
2. **Content direction drives layout direction.** If the source language is RTL, the entire display context adapts.
3. **Colors are direction-agnostic.** The color mapping system works identically in RTL and LTR.
4. **Typography is script-specific.** Arabic/Persian fonts are different from Hebrew fonts, both different from Latin.

---

## Direction Detection

The `direction` field in the JSON data contract determines layout:

```json
{
  "rows": [
    {"type": "original", "language": "ar", "direction": "rtl", "segments": [...]},
    {"type": "romanization", "language": "ar-Latn", "direction": "ltr", "segments": [...]},
    {"type": "translation", "language": "en", "direction": "ltr", "segments": [...]}
  ]
}
```

**Rules**:
- Original row uses the direction of the source language's script
- Romanization row is always LTR (Latin script)
- Translation row uses the direction of the target language

### HTML Direction Implementation

```html
<div class="row original" dir="rtl" lang="ar">
  <span class="seg">سلام</span>
</div>
<div class="row romanization" dir="ltr" lang="ar-Latn">
  <span class="seg">salâm</span>
</div>
<div class="row translation" dir="ltr" lang="en">
  <span class="seg">hello</span>
</div>
```

---

## CSS RTL Rules

### HTML `dir` Attribute Selectors

```css
/* LTR default (root) */
:root { direction: ltr; }

/* RTL overrides via html[dir] or :root[dir] */
:root[dir="rtl"],
html[dir="rtl"] {
    direction: rtl;
}

/* Row-level RTL */
.row[dir="rtl"] {
    direction: rtl;
    text-align: start;  /* Right-aligned in RTL */
}

/* Segment isolation — prevent bidi scrambling */
.row[dir="rtl"] .seg {
    unicode-bidi: isolate;
}
```

### Logical Properties (preferred over physical)

Physical properties should be replaced with logical equivalents for automatic RTL mirroring:

| Physical Property | Logical Property |
|-------------------|-----------------|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `padding-right` | `padding-inline-end` |
| `border-left` | `border-inline-start` |
| `border-right` | `border-inline-end` |
| `left` | `inset-inline-start` |
| `right` | `inset-inline-end` |
| `text-align: left` | `text-align: start` |
| `text-align: right` | `text-align: end` |
| `float: left` | `float: inline-start` |
| `float: right` | `float: inline-end` |

---

## Component-Level Mirroring

### Container
```css
.container {
    max-width: 800px;
    margin: 0 auto;  /* Centering works for both directions */
    padding: 4em 2em 6em;
}
/* RTL: container is identical — no mirroring needed for centered layout */
```

### View Mode Toggle Bar
```css
.view-mode-bar {
    display: flex;
    justify-content: center;  /* Centered — no mirroring */
}
```

Buttons use logical border-radius:
```css
.view-mode-btn:first-child { border-radius: 6px 0 0 6px; }
/* RTL: first-child is on the RIGHT side in RTL — correct! */
```

### Section Labels
```css
.section-label {
    text-align: center;  /* Centered — no mirroring */
}
```

### Row Text Alignment
```css
.row {
    text-align: center;  /* Default center for lyrics display */
}
.row[dir="rtl"] {
    /* If lyrics are not centered, use: */
    /* text-align: start;  /* Right-aligned in RTL context */
}
```

### Vocabulary Section
```css
.vocab-table th {
    text-align: start;  /* Logical property — mirrors automatically */
}
```

### Annotations
```css
.annotation-note {
    border-inline-start: 3px solid #d4a017;  /* Logical border */
    padding: 0.55em 1em;
}
```

---

## RTL Typography

### Font Stacks for RTL Scripts

```css
/* Arabic, Persian, Urdu, Pashto, Kurdish, Uyghur, Sindhi */
[lang="ar"], [lang="fa"], [lang="ur"], [lang="ps"],
[lang="ku-Arab"], [lang="ug-Arab"], [lang="sd"] {
    font-family: 'Noto Naskh Arabic', 'Scheherazade New', 'Amiri', serif;
    font-size: 1.2em;  /* Arabic needs slightly larger size for legibility */
    line-height: 2.0;  /* Extra line height for diacritics */
}

/* Hebrew, Yiddish */
[lang="he"], [lang="yi"] {
    font-family: 'Noto Sans Hebrew', 'David', 'Frank Ruhl Hofshi', serif;
}

/* Syriac */
[lang="syr"] {
    font-family: 'Noto Sans Syriac', serif;
}

/* Thaana (Dhivehi) */
[lang="dv"] {
    font-family: 'Noto Sans Thaana', serif;
}
```

### Arabic Script Typography Features

```css
[lang="ar"], [lang="fa"], [lang="ur"] {
    font-feature-settings: "calt", "liga", "rlig", "cswh", "mset";
    -webkit-font-feature-settings: "calt", "liga", "rlig", "cswh", "mset";
    letter-spacing: 0;  /* Arabic uses kashida for justification, not letter-spacing */
}
```

Arabic/Persian/Urdu must NOT use `letter-spacing` for justification — they use kashida (تطويل) elongation. For display purposes, natural letter spacing is used.

---

## RTL Tooltip Positioning

### JavaScript Positioning Logic

The tooltip uses `position: fixed` with `getBoundingClientRect()` for viewport-relative coordinates. This works for both LTR and RTL, but the positioning preferences differ:

```javascript
function positionTooltip(seg) {
    const segRect = seg.getBoundingClientRect();
    const tipRect = tooltip.getBoundingClientRect();
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const gap = 10;
    
    // Horizontal: center over the segment (works for both LTR and RTL)
    let left = segRect.left + segRect.width / 2 - tipRect.width / 2;
    
    // Prefer above
    let top = segRect.top - tipRect.height - gap;
    
    // Fallback to below
    if (top < gap) {
        top = segRect.bottom + gap;
    }
    
    // Clamp within viewport
    if (top + tipRect.height > vh - gap) {
        top = vh - tipRect.height - gap;
    }
    if (top < gap) top = gap;
    if (left < gap) left = gap;
    if (left + tipRect.width > vw - gap) left = vw - tipRect.width - gap;
    
    tooltip.style.left = left + 'px';
    tooltip.style.top = top + 'px';
}
```

**Key insight**: Because `getBoundingClientRect()` returns viewport coordinates, and tooltips use `position: fixed`, the horizontal centering logic is identical for RTL and LTR. The segment's visual position is correctly reported regardless of text direction.

### RTL Tooltip Content

Tooltip content uses LTR for pronunciation (always Latin script), but uses RTL for the original word display when the source is RTL:

```javascript
function buildTooltipHTML(info) {
    // Word in original script
    if (info.original) {
        const dir = isRTLScript(info.script) ? 'rtl' : 'ltr';
        html += `<div class="tt-word" dir="${dir}">${escapeHTML(info.original)}</div>`;
    }
    // Pronunciation always LTR (Latin script)
    if (info.pronunciation) {
        html += `<div class="tt-pronunciation">/${escapeHTML(info.pronunciation)}/</div>`;
    }
    // ...
}
```

---

## RTL Dictionary Cards

### Card Positioning

Same as tooltips — `position: fixed` with viewport clamping:

```javascript
function positionDictCard(seg) {
    const segRect = seg.getBoundingClientRect();
    const cardW = dictCard.offsetWidth || 360;
    const cardH = dictCard.offsetHeight || 300;
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const gap = 12;
    
    // Horizontal: center on word (LTR and RTL both work)
    let left = segRect.left + segRect.width / 2 - cardW / 2;
    if (left < gap) left = gap;
    if (left + cardW > vw - gap) left = vw - cardW - gap;
    
    // Vertical: prefer below
    let top = segRect.bottom + gap;
    if (top + cardH > vh - gap) {
        top = segRect.top - cardH - gap;
    }
    if (top < gap) top = gap;
    
    dictCard.style.left = left + 'px';
    dictCard.style.top = top + 'px';
}
```

### Card Content Direction

Card content inherits the direction of the word being inspected:
- RTL word → card content aligns right, RTL text flow
- LTR word → card content aligns left, LTR text flow

### Close Button Position

```css
.dict-card-close {
    position: absolute;
    inset-block-start: 0.8em;
    inset-inline-end: 0.9em;  /* Logical property: right in LTR, left in RTL */
}
```

---

## RTL Selection Behavior

### Text Selection

Browsers handle RTL text selection natively when `dir="rtl"` is set on the element. No custom cursor behavior needed.

### Selection Highlight

```css
.row[dir="rtl"] .seg::selection {
    background: rgba(0, 113, 227, 0.2);
}
```

---

## RTL Scroll Behavior

### Horizontal Scrolling

In RTL contexts, the initial scroll position is at the right edge. Browsers handle this natively.

### Scroll-Snap (if used)

```css
.scroll-container[dir="rtl"] {
    scroll-snap-type: x mandatory;  /* Still snap on x-axis */
    /* The initial snap position will be the rightmost snap point */
}
```

---

## RTL Testing Checklist

For every RTL language output, verify:

- [ ] **Text flows right-to-left**: Words appear in correct RTL order
- [ ] **Punctuation is correct**: Arabic/Hebrew punctuation marks appear in correct positions
- [ ] **Numbers are not reversed**: "123" remains "123" (not "321")
- [ ] **Latin words are not scrambled**: English words within Arabic text flow LTR
- [ ] **Tooltips appear correctly**: Positioned relative to the word, not mirrored incorrectly
- [ ] **Dictionary cards open correctly**: Positioned relative to the word
- [ ] **Section labels are readable**: Properly centered or aligned
- [ ] **Vocabulary table is readable**: Header alignment follows content direction
- [ ] **Colors apply correctly**: Color mapping works regardless of direction
- [ ] **Line breaks are preserved**: Poetic line breaks respected
- [ ] **Selection works**: Text selection follows RTL cursor behavior
- [ ] **Mobile layout works**: Single-column RTL layout on small screens
- [ ] **Font displays correct glyphs**: No tofu (□), proper Arabic shaping
- [ ] **Diacritics render correctly**: Arabic tashkil (َ ِ ُ), Hebrew niqqud
