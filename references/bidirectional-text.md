# Bidirectional Text Support

**Core principle**: The system must correctly render bidirectional text — preventing character scrambling, handling mixed content, and using Unicode bidi-aware rendering throughout.

## Table of Contents
- [Core Concepts](#core-concepts)
- [Mixed Content Types](#mixed-content-types)
- [Bidi Isolation Strategy](#bidi-isolation-strategy)
- [Character Scrambling Prevention](#character-scrambling-prevention)
- [CSS Implementation](#css-implementation)
- [HTML Implementation](#html-implementation)
- [Testing Scenarios](#testing-scenarios)

---

## Core Concepts

### Unicode Bidirectional Algorithm (UBA)

The Unicode Bidirectional Algorithm (UAX #9) determines the visual ordering of characters in mixed-direction text. The system must respect this algorithm and not interfere with it.

### Directional Types

Every Unicode character has a bidirectional type:

| Type | Examples | Behavior |
|------|----------|----------|
| Strong LTR | Latin, Cyrillic, Greek, CJK | Push direction left-to-right |
| Strong RTL | Arabic, Hebrew, Syriac, Thaana | Push direction right-to-left |
| Weak | Numbers, currency symbols | Follow surrounding strong characters |
| Neutral | Punctuation, spaces | Inherit from surrounding context |

### Bidi Isolation

The key tool for preventing bidi scrambling is **isolation**:

- `unicode-bidi: isolate` — Creates a directional isolate: the element's content is treated as an independent bidirectional sequence
- `dir="auto"` — HTML automatic direction detection based on the first strong character
- Unicode isolates: RLI (U+2067), LRI (U+2066), FSI (U+2068), PDI (U+2069)

---

## Mixed Content Types

### Type 1: RTL Base with LTR Embedded

```
Arabic sentence with English word:
أنا love you يا حبيبي

Base direction: RTL (Arabic)
Embedded: "love you" — LTR isolate
```

**Correct rendering**: The Arabic flows RTL, "love you" is presented LTR within the RTL flow.

**Implementation**:
```html
<span dir="rtl" lang="ar">
  أنا <span dir="ltr" lang="en">love you</span> يا حبيبي
</span>
```

### Type 2: LTR Base with RTL Embedded

```
English sentence with Arabic word:
I love العربية music

Base direction: LTR (English)
Embedded: "العربية" — RTL isolate
```

**Implementation**:
```html
<span dir="ltr" lang="en">
  I love <span dir="rtl" lang="ar">العربية</span> music
</span>
```

### Type 3: Hebrew with Numbers

```
Hebrew with phone number:
הטלפון שלי הוא 055-123-4567

Base direction: RTL (Hebrew)
Embedded: "055-123-4567" — LTR (numbers always LTR)
```

**Note**: Numbers always flow LTR even in RTL context. The browser handles this automatically.

### Type 4: Urdu with URL

```
Urdu with English URL:
ویب سائٹ https://example.com/page ہے

Base direction: RTL (Urdu)
Embedded: "https://example.com/page" — LTR isolate
```

**Implementation**:
```html
<span dir="rtl" lang="ur">
  ویب سائٹ <span dir="ltr">https://example.com/page</span> ہے
</span>
```

### Type 5: Chinese + Arabic

```
Chinese sentence with Arabic name:
这是一句中文 والعربية 混合的句子

Base direction: LTR (Chinese)
Embedded: "والعربية" — RTL isolate
```

### Type 6: Japanese + English (Common in J-Pop)

```
Japanese lyric with English phrase:
君は my sunshine 僕の光

Base direction: LTR (Japanese)
Embedded: "my sunshine" — LTR (English), same direction, no isolation needed
```

---

## Bidi Isolation Strategy

### Rule 1: Every Script-Switching Token Gets Isolated

When a token changes script within a single row, wrap it in an isolate:

```html
<!-- BEFORE (may scramble): -->
<span dir="rtl">أنا love you حبيبي</span>

<!-- AFTER (correct): -->
<span dir="rtl">أنا <bdi>love you</bdi> حبيبي</span>
```

### Rule 2: Use CSS `unicode-bidi: isolate` on Segments

```css
.seg {
    unicode-bidi: isolate;
}
```

This ensures each aligned word token is directionally independent.

### Rule 3: Rows Have Explicit Direction

```html
<div class="row original" dir="rtl" lang="ar">
  <!-- segments flow RTL -->
</div>
<div class="row romanization" dir="ltr" lang="ar-Latn">
  <!-- segments flow LTR -->
</div>
<div class="row translation" dir="ltr" lang="en">
  <!-- segments flow LTR -->
</div>
```

### Rule 4: Mixed-Script Lines Use First-Strong Heuristic with Override

```python
def determine_row_direction(segments):
    """Determine the row direction based on the dominant script."""
    rtl_scripts = {'Arabic', 'Hebrew', 'Syriac', 'Thaana'}
    ltr_scripts = {'Latin', 'Cyrillic', 'Greek', 'CJK', 'Hangul'}
    
    char_count = {'rtl': 0, 'ltr': 0}
    for seg in segments:
        for ch in seg['text']:
            script = get_script_for_char(ch)
            if script in rtl_scripts:
                char_count['rtl'] += 1
            elif script in ltr_scripts:
                char_count['ltr'] += 1
    
    if char_count['rtl'] > char_count['ltr']:
        return 'rtl'
    return 'ltr'
```

---

## Character Scrambling Prevention

### Common Scrambling Scenarios

#### Scenario 1: Punctuation at Script Boundaries

```
Problem:  "hello (שלום) world" 
Displays: "hello (world)" ← SHOULD be "(שלום)"
```

**Fix**: Wrap the RTL segment in an isolate:
```html
hello <bdi>(שלום)</bdi> world
```

#### Scenario 2: RTL Word at End of LTR Line

```
Problem:  "The Arabic word is سلام."
Displays: "The Arabic word is .سلام" ← period incorrectly positioned
```

**Fix**: Ensure the period is outside the RTL isolate:
```html
The Arabic word is <span dir="rtl">سلام</span>.
```

#### Scenario 3: Nested Bidirectional Content

```
Problem:  Arabic quote containing an English quote
قال: "He said 'hello' to me"
```

**Fix**: Nested isolates:
```html
<span dir="rtl" lang="ar">
  قال: <bdi>"He said <bdi>'hello'</bdi> to me"</bdi>
</span>
```

### Prevention Checklist

For every segment that changes script direction relative to its parent:

- [ ] Wrap in `<bdi>` element or use `unicode-bidi: isolate`
- [ ] Ensure punctuation at boundaries is in the correct isolate
- [ ] Test with a bidi-aware rendering engine
- [ ] Verify numbers display correctly (never RTL)

---

## CSS Implementation

### Base Bidi Rules

```css
/* Isolate all word segments to prevent cross-word bidi effects */
.seg {
    unicode-bidi: isolate;
}

/* RTL rows: establish RTL base direction */
.row[dir="rtl"] {
    direction: rtl;
}

/* LTR rows: establish LTR base direction */
.row[dir="ltr"] {
    direction: ltr;
}

/* For mixed-content line groups, each row is independently directed */
.line-group {
    /* Parent doesn't force direction — children do */
}

/* Numbers always LTR */
.seg.number {
    direction: ltr;
    unicode-bidi: embed;
}
```

### HTML5 `<bdi>` Element

The `<bdi>` (Bidirectional Isolate) element is the HTML5 standard way to isolate bidirectional text:

```html
<p dir="rtl">
  المستخدم <bdi>john_doe</bdi> قام بتسجيل الدخول.
</p>
```

This renders as: "قام المستخدم john_doe بتسجيل الدخول" with "john_doe" in correct LTR order.

### `dir="auto"` for Dynamic Content

When the direction of content is unknown at render time:

```html
<!-- Direction determined by first strong character -->
<span dir="auto">{{ user_content }}</span>
```

The browser reads the first strong character. If it's Arabic → RTL. If it's Latin → LTR.

---

## HTML Implementation in Output

### Annotation JSON Contract — Bidi Fields

Every row MUST include:
```json
{
  "type": "original",
  "language": "ar",
  "direction": "rtl",
  "script": "Arabic",
  "segments": [...]
}
```

Every segment MAY include:
```json
{
  "text": "love",
  "direction": "ltr",
  "color": "#E74C3C",
  "group_id": "L1-W2"
}
```

If a segment has a different direction from its row, it must be isolated.

### Rendering Logic

```python
def render_segment(seg, row_direction):
    seg_dir = seg.get("direction", row_direction)
    if seg_dir != row_direction:
        # Direction mismatch — wrap in isolate
        return f'<bdi dir="{seg_dir}">{escape_html(seg["text"])}</bdi>'
    else:
        return f'<span class="seg">{escape_html(seg["text"])}</span>'
```

---

## Testing Scenarios

### Test Set 1: Basic RTL

```
Input:   سلام
Expected: Rendered RTL, "س" on the right, "م" on the left
```

### Test Set 2: RTL + LTR Mixed

```
Input:   أنا أحب coffee في الصباح
Expected: "أنا أحب" RTL, "coffee" LTR, "في الصباح" RTL
```

### Test Set 3: LTR + RTL Mixed

```
Input:   I love شاي in the morning
Expected: "I love" LTR, "شاي" RTL, "in the morning" LTR
```

### Test Set 4: Numbers in RTL

```
Input:   السعر ١٢٣ ريال
Expected: "123" displays LTR within RTL flow
```

### Test Set 5: URL in RTL

```
Input:   زوروا https://example.com/page?q=test
Expected: URL displays correctly LTR, not scrambled
```

### Test Set 6: Punctuation at Boundaries

```
Input:   "مرحبا" means "hello"
Expected: Opening quote before مر, closing quote after ا
```

### Test Set 7: Parentheses Mixed

```
Input:   The capital is (طهران) in Farsi
Expected: (طهران) displays correctly, parentheses on correct sides
```

### Test Set 8: Multiple Script Switches

```
Input:   English, 中文, العربية, and עברית in one sentence
Expected: Each script renders correctly, no scrambling
```

### Test Set 9: Lyrics with Code-Switching

```
Input (Hindi film song):
तेरी आँखों में I see my world
Expected: Hindi portion RTL, English portion LTR, correct order
```

### Test Set 10: Tooltip on RTL Word

```
Hover over:  سلام (RTL word)
Expected: Tooltip positions correctly relative to the RTL word position
```
