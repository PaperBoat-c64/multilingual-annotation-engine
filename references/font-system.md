# Font System — Script-Appropriate Typography

**Core principle**: Automatically load script-appropriate fonts. Never display missing glyphs (tofu □). Prefer Noto family coverage. Use script-aware typography.

## Table of Contents
- [Font Stack by Script](#font-stack-by-script)
- [Font Loading Strategy](#font-loading-strategy)
- [Script-Aware Typography](#script-aware-typography)
- [Glyph Fallback Chain](#glyph-fallback-chain)
- [No-Tofu Guarantee](#no-tofu-guarantee)
- [CSS Implementation](#css-implementation)

---

## Font Stack by Script

### RTL Scripts

| Script | Primary Font | Fallback 1 | Fallback 2 | Generic |
|--------|-------------|-----------|------------|---------|
| Arabic | Noto Naskh Arabic | Scheherazade New | Amiri | serif |
| Persian | Noto Naskh Arabic | Scheherazade New | IranNastaliq | serif |
| Urdu | Noto Naskh Arabic | Scheherazade New | Nafees Nastaleeq | serif |
| Hebrew | Noto Sans Hebrew | David | Frank Ruhl Hofshi | serif |
| Syriac | Noto Sans Syriac | — | — | serif |
| Thaana | Noto Sans Thaana | — | — | serif |

### CJK / East Asian

| Script | Primary Font | Fallback 1 | Fallback 2 | Generic |
|--------|-------------|-----------|------------|---------|
| Chinese (Simplified) | Noto Sans SC | Source Han Sans SC | PingFang SC | sans-serif |
| Chinese (Traditional) | Noto Sans TC | Source Han Sans TC | PingFang TC | sans-serif |
| Japanese | Noto Sans JP | Source Han Sans JP | Hiragino Sans | sans-serif |
| Korean | Noto Sans KR | Source Han Sans KR | Apple SD Gothic Neo | sans-serif |
| Hangul (monospace) | Noto Sans Mono KR | D2Coding | — | monospace |

### Indic Scripts

| Script | Primary Font | Fallback 1 | Fallback 2 | Generic |
|--------|-------------|-----------|------------|---------|
| Devanagari | Noto Sans Devanagari | Mukta | Lohit Devanagari | serif |
| Bengali | Noto Sans Bengali | Hind Siliguri | Lohit Bengali | serif |
| Gurmukhi | Noto Sans Gurmukhi | Mukta Mahee | Lohit Gurmukhi | serif |
| Gujarati | Noto Sans Gujarati | Lohit Gujarati | — | serif |
| Odia | Noto Sans Odia | Lohit Odia | — | serif |
| Tamil | Noto Sans Tamil | Lohit Tamil | — | serif |
| Telugu | Noto Sans Telugu | Lohit Telugu | — | serif |
| Kannada | Noto Sans Kannada | Lohit Kannada | — | serif |
| Malayalam | Noto Sans Malayalam | Lohit Malayalam | — | serif |
| Sinhala | Noto Sans Sinhala | — | — | serif |

### Southeast Asian

| Script | Primary Font | Fallback | Generic |
|--------|-------------|----------|---------|
| Thai | Noto Sans Thai | Sarabun | sans-serif |
| Lao | Noto Sans Lao | Phetsarath | sans-serif |
| Myanmar | Noto Sans Myanmar | Padauk | serif |
| Khmer | Noto Sans Khmer | Khmer OS | serif |

### European

| Script | Primary Font | Fallback 1 | Fallback 2 | Generic |
|--------|-------------|-----------|------------|---------|
| Latin (sans) | Noto Sans | Inter | system-ui | sans-serif |
| Latin (serif) | Noto Serif | Georgia | Times New Roman | serif |
| Cyrillic | Noto Sans | PT Sans | system-ui | sans-serif |
| Greek | Noto Sans | Gentium | system-ui | serif |
| Georgian | Noto Sans Georgian | — | — | serif |
| Armenian | Noto Sans Armenian | — | — | serif |

### Other Scripts

| Script | Primary Font | Fallback | Generic |
|--------|-------------|----------|---------|
| Ethiopic | Noto Sans Ethiopic | — | serif |
| Tibetan | Noto Sans Tibetan | Jomolhari | serif |
| Mongolian | Noto Sans Mongolian | — | serif |
| Tifinagh | Noto Sans Tifinagh | — | sans-serif |
| Cherokee | Noto Sans Cherokee | — | sans-serif |
| Canadian Aboriginal | Noto Sans Canadian Aboriginal | — | sans-serif |

### Monospace / IPA

| Use Case | Primary Font | Fallback |
|----------|-------------|----------|
| IPA transcription | Noto Sans Mono | JetBrains Mono, SF Mono |
| Code / Glosses | Noto Sans Mono | JetBrains Mono, SF Mono |

---

## Font Loading Strategy

### @font-face with Google Fonts CDN

Load fonts on-demand via Google Fonts:

```html
<!-- Arabic, Persian, Urdu -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;700&display=swap" rel="stylesheet">

<!-- CJK (subset by language) -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">

<!-- Devanagari -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&display=swap" rel="stylesheet">
```

### Conditional Loading

Only load fonts when the script is present in the content:

```javascript
function loadFontsForScripts(scripts) {
    const fontMap = {
        'Arabic': 'Noto+Naskh+Arabic',
        'Hebrew': 'Noto+Sans+Hebrew',
        'CJK': 'Noto+Sans+SC',
        'Devanagari': 'Noto+Sans+Devanagari',
        'Thai': 'Noto+Sans+Thai',
        // ...
    };
    
    for (const script of scripts) {
        if (fontMap[script]) {
            const link = document.createElement('link');
            link.href = `https://fonts.googleapis.com/css2?family=${fontMap[script]}:wght@400;500;700&display=swap`;
            link.rel = 'stylesheet';
            document.head.appendChild(link);
        }
    }
}
```

### Fallback When Offline

If Google Fonts is unavailable (offline/local context), the CSS font stacks fall back to system-installed fonts automatically.

---

## Script-Aware Typography

### Size Scaling

Some scripts need different base sizes for equivalent legibility:

| Script | Size Multiplier | Reason |
|--------|----------------|--------|
| Latin | 1.0× | Baseline |
| Arabic | 1.15× | Diacritics need height; smaller x-height |
| Persian | 1.15× | Same as Arabic |
| Urdu | 1.2× | Nastaliq style is condensed |
| Hebrew | 1.05× | Niqqud needs height |
| CJK | 1.1× | Character density needs space |
| Devanagari | 1.2× | Conjuncts need vertical space |
| Tamil | 1.1× | Rounded forms need space |
| Thai | 1.15× | Tone marks need height above |
| Khmer | 1.25× | Subscript consonants need vertical space |
| Ethiopic | 1.1× | Syllable blocks need consistent width |

### Line Height

| Script | Line Height | Reason |
|--------|------------|--------|
| Latin | 1.6–2.0 | Standard readability |
| Arabic | 2.0–2.4 | Diacritics above and below |
| CJK | 1.8–2.2 | Uniform character boxes |
| Devanagari | 2.0–2.4 | Shirorekha (headline) + diacritics |
| Thai | 2.0–2.5 | Tone marks above, vowel marks below |
| Khmer | 2.2–2.6 | Subscript characters below baseline |
| Hebrew | 1.8–2.2 | Niqqud below |

### Letter Spacing

| Script | Letter Spacing | Notes |
|--------|---------------|-------|
| Latin | -0.01em to 0.02em | Slight tightness for headings |
| Arabic | 0 (normal) | Kashida-based justification, not letter-spacing |
| CJK | 0.02em–0.05em | Characters need breathing room |
| Cyrillic | 0 (normal) | Same as Latin |

### Font Features

Enable script-specific OpenType features:

```css
/* Arabic: required ligatures, contextual alternates */
[lang="ar"], [lang="fa"], [lang="ur"] {
    font-feature-settings: "calt", "liga", "rlig", "cswh", "mset";
}

/* Latin: discretionary ligatures for elegant display */
.romanization, .translation {
    font-feature-settings: "liga", "dlig";
}

/* CJK: proportional alternate metrics */
[lang="zh"], [lang="ja"], [lang="ko"] {
    font-feature-settings: "palt";
    font-variant-east-asian: proportional-width;
}
```

---

## Glyph Fallback Chain

### How Fallback Works

When a character is not in the primary font, the browser tries each fallback in order:

```
Noto Sans SC → Source Han Sans SC → PingFang SC → sans-serif
     ↓ (glyph missing)
                  ↓
            Source Han Sans SC
                  ↓ (glyph missing)
                          ↓
                    PingFang SC
                          ↓ (glyph missing)
                                  ↓
                            sans-serif (system default)
```

### Known Coverage Gaps

| Script | Noto Covers | Potential Gaps |
|--------|-----------|----------------|
| CJK | ~45,000 characters (CJK Unified + Ext A) | Extension B–H characters (rare) |
| Arabic | Full coverage | Historical/ornamental forms |
| Devanagari | Full coverage | Rare conjuncts in Sanskrit |
| Tibetan | Full coverage | Specialized religious shorthand |
| Ethiopic | Full coverage | Historical Ge'ez variants |

When a gap is detected, the system falls back to the system's default font for that script.

---

## No-Tofu Guarantee

### Detection

The system checks for characters that fall outside all fonts in the stack. For known scripts, the Noto family provides near-complete coverage.

### Mitigation

If tofu is detected in output:
1. Check if the character falls outside Noto coverage
2. Add a more specific font that covers the character
3. If no font covers it, render as image-based glyph (last resort)
4. Flag the character in annotations

### Testing

For every supported script, test:
```
Arabic:    السلام عليكم
Hebrew:    שלום
Chinese:   你好世界
Japanese:  こんにちは世界
Korean:    안녕하세요 세계
Hindi:     नमस्ते दुनिया
Thai:      สวัสดีชาวโลก
Tamil:     வணக்கம் உலகம்
Georgian:  გამარჯობა მსოფლიო
Armenian:  Բարև աշխարհ
Amharic:   ሰላም ልዑል
Tibetan:   བཀྲ་ཤིས་བདེ་ལེགས
```

Every character in these test strings must render without tofu.

---

## CSS Implementation

### Master CSS Font Declaration

```css
/* Root: set base font */
:root {
    font-family: 'Noto Sans', 'Inter', system-ui, -apple-system, sans-serif;
}

/* RTL Scripts */
[lang="ar"], [lang="fa"], [lang="ur"], [lang="ps"],
[lang="ku-Arab"], [lang="ug-Arab"], [lang="sd"] {
    font-family: 'Noto Naskh Arabic', 'Scheherazade New', 'Amiri', serif;
    font-size: 1.15em;
    line-height: 2.2;
}

[lang="he"], [lang="yi"] {
    font-family: 'Noto Sans Hebrew', 'David', 'Frank Ruhl Hofshi', serif;
    font-size: 1.05em;
    line-height: 2.0;
}

/* CJK */
[lang="zh"], [lang="zh-Hans"] {
    font-family: 'Noto Sans SC', 'Source Han Sans SC', 'PingFang SC', sans-serif;
    font-size: 1.1em;
    line-height: 2.0;
}

[lang="zh-Hant"] {
    font-family: 'Noto Sans TC', 'Source Han Sans TC', 'PingFang TC', sans-serif;
    font-size: 1.1em;
    line-height: 2.0;
}

[lang="ja"] {
    font-family: 'Noto Sans JP', 'Source Han Sans JP', 'Hiragino Sans', sans-serif;
    font-size: 1.1em;
    line-height: 2.0;
}

[lang="ko"] {
    font-family: 'Noto Sans KR', 'Source Han Sans KR', 'Apple SD Gothic Neo', sans-serif;
    font-size: 1.1em;
    line-height: 2.0;
}

/* Indic */
[lang="hi"], [lang="mr"], [lang="ne"], [lang="sa"] {
    font-family: 'Noto Sans Devanagari', 'Mukta', serif;
    font-size: 1.2em;
    line-height: 2.2;
}

[lang="bn"] {
    font-family: 'Noto Sans Bengali', 'Hind Siliguri', serif;
    font-size: 1.2em;
    line-height: 2.2;
}

[lang="ta"] {
    font-family: 'Noto Sans Tamil', serif;
    font-size: 1.1em;
    line-height: 2.0;
}

[lang="te"] {
    font-family: 'Noto Sans Telugu', serif;
    font-size: 1.15em;
    line-height: 2.0;
}

[lang="gu"] {
    font-family: 'Noto Sans Gujarati', serif;
    font-size: 1.15em;
    line-height: 2.0;
}

[lang="pa-Guru"] {
    font-family: 'Noto Sans Gurmukhi', serif;
    font-size: 1.2em;
    line-height: 2.0;
}

[lang="si"] {
    font-family: 'Noto Sans Sinhala', serif;
    font-size: 1.2em;
    line-height: 2.2;
}

/* Southeast Asian */
[lang="th"] {
    font-family: 'Noto Sans Thai', 'Sarabun', sans-serif;
    font-size: 1.15em;
    line-height: 2.2;
}

[lang="lo"] {
    font-family: 'Noto Sans Lao', 'Phetsarath', sans-serif;
    font-size: 1.15em;
    line-height: 2.2;
}

[lang="my"] {
    font-family: 'Noto Sans Myanmar', 'Padauk', serif;
    font-size: 1.15em;
    line-height: 2.2;
}

[lang="km"] {
    font-family: 'Noto Sans Khmer', 'Khmer OS', serif;
    font-size: 1.25em;
    line-height: 2.4;
}

/* European */
[lang="el"] {
    font-family: 'Noto Sans', 'Gentium', serif;
}

[lang="ka"] {
    font-family: 'Noto Sans Georgian', serif;
    font-size: 1.1em;
}

[lang="hy"] {
    font-family: 'Noto Sans Armenian', serif;
    font-size: 1.05em;
}

[lang="ru"], [lang="uk"], [lang="bg"], [lang="sr"],
[lang="mn-Cyrl"], [lang="kk"] {
    font-family: 'Noto Sans', 'PT Sans', sans-serif;
}

/* Other */
[lang="am"], [lang="ti"] {
    font-family: 'Noto Sans Ethiopic', serif;
    font-size: 1.1em;
}

[lang="bo"], [lang="dz"] {
    font-family: 'Noto Sans Tibetan', 'Jomolhari', serif;
    font-size: 1.1em;
    line-height: 2.2;
}

[lang="mn-Mong"] {
    font-family: 'Noto Sans Mongolian', serif;
    font-size: 1.2em;
}

/* IPA and Monospace */
.row.ipa, .row.gloss {
    font-family: 'Noto Sans Mono', 'JetBrains Mono', 'SF Mono', monospace;
}
```

### RTL Font Size Adjustments

RTL scripts need slightly larger default sizes for legibility:

```css
.row[dir="rtl"] {
    font-size: 1.05em;  /* Slight boost for RTL text */
}
```

### Mobile Font Adjustments

On small screens, increase font size slightly for legibility:

```css
@media (max-width: 600px) {
    [lang="ar"], [lang="fa"], [lang="ur"] { font-size: 1.2em; }
    [lang="km"] { font-size: 1.3em; }
}
```
