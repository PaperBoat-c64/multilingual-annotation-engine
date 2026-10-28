# Script Detection Guide

## Table of Contents
- [Writing System Identification](#writing-system-identification)
- [Directionality Detection](#directionality-detection)
- [Language Disambiguation](#language-disambiguation)
- [Romanization vs Translation Detection](#romanization-vs-translation-detection)
- [Mixed-Script Handling](#mixed-script-handling)
- [Complete Script Coverage](#complete-script-coverage)

---

## Writing System Identification

### Unicode Range Quick Reference — Full Coverage

| Script | Unicode Range(s) | Example Languages | Direction |
|--------|-----------------|-------------------|-----------|
| **RTL Scripts** | | | |
| Arabic | U+0600–U+06FF, U+0750–U+077F, U+08A0–U+08FF, U+FB50–U+FDFF, U+FE70–U+FEFF, U+1EE00–U+1EEFF | Arabic, Persian, Urdu, Pashto, Kurdish, Uyghur, Sindhi, Balochi, Kashmiri, Punjabi (Shahmukhi) | **RTL** |
| Hebrew | U+0590–U+05FF, U+FB1D–U+FB4F | Hebrew, Yiddish, Ladino, Judeo-Arabic | **RTL** |
| Syriac | U+0700–U+074F | Assyrian, Chaldean, Syriac, Turoyo | **RTL** |
| Thaana | U+0780–U+07BF | Dhivehi (Maldivian) | **RTL** |
| N'Ko | U+07C0–U+07FF | Manding (Bambara, Maninka, Dyula) | **RTL** |
| Samaritan | U+0800–U+083F | Samaritan Hebrew, Samaritan Aramaic | **RTL** |
| Mandaic | U+0840–U+085F | Mandaic | **RTL** |
| **LTR Scripts — East Asian** | | | |
| CJK Unified Ideographs | U+4E00–U+9FFF | Chinese, Japanese (Kanji), Korean (Hanja), Vietnamese (Chữ Nôm) | LTR |
| CJK Extension A | U+3400–U+4DBF | Rare CJK characters | LTR |
| CJK Extension B–H | U+20000–U+3134F | Historical/rare CJK | LTR |
| Hiragana | U+3040–U+309F | Japanese | LTR |
| Katakana | U+30A0–U+30FF | Japanese | LTR |
| Hangul Syllables | U+AC00–U+D7AF | Korean | LTR |
| Hangul Jamo | U+1100–U+11FF | Korean (archaic/compatibility) | LTR |
| Bopomofo | U+3100–U+312F | Chinese phonetic notation (Taiwan) | LTR |
| Yi | U+A000–U+A4CF | Nuosu (Yi) | LTR |
| **LTR Scripts — Indic** | | | |
| Devanagari | U+0900–U+097F | Hindi, Marathi, Nepali, Sanskrit, Maithili, Bhojpuri, Konkani, Sindhi (Devanagari) | LTR |
| Bengali | U+0980–U+09FF | Bengali, Assamese | LTR |
| Gurmukhi | U+0A00–U+0A7F | Punjabi (Gurmukhi) | LTR |
| Gujarati | U+0A80–U+0AFF | Gujarati | LTR |
| Odia | U+0B00–U+0B7F | Odia | LTR |
| Tamil | U+0B80–U+0BFF | Tamil | LTR |
| Telugu | U+0C00–U+0C7F | Telugu | LTR |
| Kannada | U+0C80–U+0CFF | Kannada | LTR |
| Malayalam | U+0D00–U+0D7F | Malayalam | LTR |
| Sinhala | U+0D80–U+0DFF | Sinhala | LTR |
| **LTR Scripts — Southeast Asian** | | | |
| Thai | U+0E00–U+0E7F | Thai, Northern Thai, Southern Thai | LTR |
| Lao | U+0E80–U+0EFF | Lao | LTR |
| Myanmar | U+1000–U+109F | Burmese, Shan, Mon, Karen | LTR |
| Khmer | U+1780–U+17FF | Khmer | LTR |
| Tai Le | U+1950–U+197F | Tai Nüa | LTR |
| Tai Tham | U+1A20–U+1AAF | Northern Thai, Tai Lü, Khün | LTR |
| **LTR Scripts — Central Asian** | | | |
| Tibetan | U+0F00–U+0FFF | Tibetan, Dzongkha, Ladakhi, Sherpa | LTR |
| Mongolian | U+1800–U+18AF | Mongolian (Traditional script), Manchu, Xibe | LTR (vertical) |
| **LTR Scripts — European** | | | |
| Cyrillic | U+0400–U+04FF, U+0500–U+052F | Russian, Ukrainian, Bulgarian, Serbian, Belarusian, Macedonian, Mongolian (Cyrillic), Kazakh, Kyrgyz, Tajik, Bashkir, Chuvash, Tatar, Udmurt, Chechen, Ossetian, Abkhaz | LTR |
| Cyrillic Supplement | U+0500–U+052F | Abkhaz, Kurdish, Chukchi | LTR |
| Latin Basic | U+0041–U+005A, U+0061–U+007A | English, French, German, Spanish, Italian, Portuguese, Turkish, Indonesian, Polish, Czech, Dutch, Swedish, Norwegian, Danish, Finnish, Hungarian, Romanian, Croatian, Slovenian, Slovak, Lithuanian, Latvian, Estonian, Albanian, Icelandic, Catalan, Galician, Welsh, Irish, Scots Gaelic, Afrikaans, Basque, Swahili, Zulu, Xhosa, Yoruba, Igbo, Hausa, Somali, Filipino, Cebuano, Javanese, Sundanese, Malagasy, Haitian Creole, Quechua, Guarani, Maori, Hawaiian, Samoan, Tongan, Fijian, and romanizations of non-Latin scripts | LTR |
| Latin Extended-A | U+0100–U+017F | Czech, Polish, Croatian, Latvian, Lithuanian, Romanian | LTR |
| Latin Extended-B | U+0180–U+024F | African languages, Vietnamese, Pinyin | LTR |
| Latin Extended Additional | U+1E00–U+1EFF | Vietnamese, transliterations of Indic scripts | LTR |
| Greek | U+0370–U+03FF, U+1F00–U+1FFF | Greek (modern + ancient), Polytonic Greek | LTR |
| Georgian | U+10A0–U+10FF, U+2D00–U+2D2F | Georgian, Mingrelian, Svan, Laz | LTR |
| Armenian | U+0530–U+058F | Armenian (modern + classical) | LTR |
| **LTR Scripts — African** | | | |
| Ethiopic | U+1200–U+137F, U+1380–U+139F, U+2D80–U+2DDF, U+AB00–U+AB2F | Amharic, Tigrinya, Ge'ez, Oromo, Somali (Ethiopic), Tigre | LTR |
| Tifinagh | U+2D30–U+2D7F | Tamazight (Berber), Tachelhit, Tarifit | LTR |
| Osmanya | U+10480–U+104AF | Somali (Osmanya script) | LTR |
| Vai | U+A500–U+A63F | Vai | LTR |
| Bamum | U+A6A0–U+A6FF | Bamum | LTR |
| **LTR Scripts — Americas** | | | |
| Cherokee | U+13A0–U+13FF | Cherokee | LTR |
| Canadian Aboriginal | U+1400–U+167F | Cree, Inuktitut, Ojibwe, Dene | LTR |
| Deseret | U+10400–U+1044F | English (Deseret alphabet) | LTR |
| **LTR Scripts — Other** | | | |
| Georgian (Mkhedruli) | U+10D0–U+10FF | Georgian | LTR |
| Glagolitic | U+2C00–U+2C5F | Old Church Slavonic | LTR |
| Coptic | U+2C80–U+2CFF | Coptic | LTR |
| Runic | U+16A0–U+16FF | Old Norse, Anglo-Saxon | LTR |
| Ogham | U+1680–U+169F | Primitive Irish | LTR (vertical) |

### Detection Algorithm

1. **Sample the text** (~100 characters if available)
2. **Identify Unicode blocks**: Count characters per block
3. **Primary classification**: If >50% of characters fall within a single script block, classify accordingly
4. **Direction assignment**: Each script has a default direction (see table above)
5. **Mixed-script handling**: Tokenize by script block; each token inherits its script's properties

---

## Directionality Detection

### Automatic Direction Assignment

Every detected script maps to a default direction:

```
Arabic, Hebrew, Syriac, Thaana, N'Ko, Samaritan, Mandaic  →  RTL
ALL OTHER SCRIPTS                                          →  LTR
```

### Override Signals

- **HTML `dir` attribute**: If input is HTML, respect existing `dir="rtl"` or `dir="ltr"`
- **Unicode Bidi Control Characters**: 
  - RLE (U+202B) / LRE (U+202A): Embedding overrides
  - RLO (U+202E) / LRO (U+202D): Direction overrides
  - RLI (U+2067) / LRI (U+2066): Isolate overrides
  - PDF (U+202C) / PDI (U+2069): Pop directional formatting
- **First strong character rule**: If >70% of text is from an RTL script → RTL

### RTL Detection Function (pseudocode)
```python
def detect_direction(text: str) -> str:
    rtl_scripts = {
        "Arabic", "Hebrew", "Syriac", "Thaana", "N'Ko",
        "Samaritan", "Mandaic",
    }
    script = identify_script(text)
    return "rtl" if script in rtl_scripts else "ltr"
```

---

## Language Disambiguation

### Arabic Script Languages

| Character | Persian | Arabic | Urdu | Pashto | Kurdish | Uyghur | Sindhi |
|-----------|---------|--------|------|--------|---------|--------|--------|
| گ (gâf) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| چ (che) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| پ (pe) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| ژ (zhe) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ک (keheh) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| ں (noon ghunna) | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| ے (bari ye) | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| ۍ (pashto ye) | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| ښ (pashto xin) | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| ێ (kurdish ye) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| ڵ (kurdish lam) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| ۆ (kurdish o) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| ﯪ (uyghur he) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| ﯬ (uyghur pe) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| ٻ (sindhi b) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| ڏ (sindhi dd) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

**Decision tree**:
1. If contains `پ چ ژ گ` → NOT Arabic (Persian, Urdu, Pashto, Kurdish, Uyghur, or Sindhi)
2. If contains `ں ے ڈ ٹ ڑ` → Urdu
3. If contains `ۍ ښ ڼ ږ` → Pashto
4. If contains `ێ ڵ ۆ ڕ` → Kurdish (Sorani)
5. If contains `ﯪ ﯬ ﯮ ﯰ` → Uyghur
6. If contains `ٻ ڏ ڳ ڪ` → Sindhi
7. If contains `ی` (U+06CC, Arabic Yeh) frequently → Persian
8. If contains `ي` (U+064A, Farsi Yeh) + no Persian letters → Arabic

### CJK Languages

| Feature | Chinese | Japanese | Korean |
|---------|---------|----------|--------|
| Kanji/Hanzi only | ✅ | ❌ (mixed) | ❌ (mostly Hangul) |
| Hiragana present | ❌ | ✅ | ❌ |
| Katakana present | ❌ | ✅ | ❌ |
| Hangul present | ❌ | ❌ | ✅ |

**Decision tree**:
1. If contains Hiragana/Katakana → Japanese
2. If contains Hangul blocks (U+AC00–U+D7AF) → Korean
3. If contains only CJK ideographs → Chinese (Simplified or Traditional)
4. Distinguish S/T Chinese: check `什么` (Simplified) vs `什麼` (Traditional)

### Indic Script Languages

| Feature | Hindi | Marathi | Nepali | Bengali | Punjabi | Gujarati | Tamil | Telugu |
|---------|-------|---------|--------|---------|---------|----------|-------|--------|
| Script | Devanagari | Devanagari | Devanagari | Bengali | Gurmukhi | Gujarati | Tamil | Telugu |
| Unique chars | ॐ, ऋ | ळ | | য়, ড়, ঢ় | ਖ਼, ਗ਼, ਜ਼ | | ஃ, ழ | ఱ |

**Decision tree**:
1. Identify script by Unicode block → script identification
2. For Devanagari: check character set differences
   - Marathi: contains ळ (retroflex L)
   - Nepali: similar to Hindi, check for ी/ि positioning differences
   - Sanskrit: contains ॐ, more conjunct consonants
3. For Gurmukhi: Punjabi if contains ਖ਼, ਗ਼, ਜ਼, ਫ਼

### Cyrillic Script Languages

| Feature | Russian | Ukrainian | Bulgarian | Serbian | Mongolian |
|---------|---------|-----------|-----------|---------|-----------|
| Ё ё | ✅ | ❌ | ❌ | ❌ | ✅ |
| Є є | ❌ | ✅ | ❌ | ❌ | ❌ |
| Ї ї | ❌ | ✅ | ❌ | ❌ | ❌ |
| Ъ ъ | ✅ | ❌ | ✅ (ъ) | ❌ | ✅ |
| Ђ ђ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Ћ ћ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Ү ү | ❌ | ❌ | ❌ | ❌ | ✅ |
| Ө ө | ❌ | ❌ | ❌ | ❌ | ✅ |

### Latin Script Languages

For Latin-script texts, use:
1. **Character frequency analysis**: Turkish has `ğ ş İ ı`, German has `ß ä ö ü`, French has `ç è é ê ë`, Vietnamese has `ă â ê ô ơ ư đ`, Polish has `ą ć ę ł ń ó ś ź ż`
2. **Common word detection**: "the" → English, "der/die/das" → German, "le/la/les" → French, "el/la/los/las" → Spanish, "bir/bu/şu" → Turkish
3. **Structural patterns**: If the text is entirely lowercase, single words → likely romanization

### Southeast Asian Scripts

| Script | Languages | Unique Features |
|--------|-----------|----------------|
| Thai | Thai | Tone marks (่ ้ ๊ ๋), no inter-word spaces |
| Lao | Lao | Similar to Thai, fewer consonants, different tone marks |
| Myanmar | Burmese, Shan, Mon | Circular shapes, stacking, kinzi (ကင္းစီး) |
| Khmer | Khmer | Subscript consonants, complex vowel positioning, no spaces |

---

## Romanization vs Translation Detection

When a Latin-script row appears alongside original script text:

### Heuristics for "is_romanization":

1. **Word count match**: Romanization typically has ~same number of tokens as original
2. **Capitalization**: Romanization is often all-lowercase
3. **No English function words**: Absence of "the", "a", "is", "of", "in", etc.
4. **Consonant-heavy patterns**: Romanized Arabic/Persian has patterns like "kh", "gh", "sh", "ch"
5. **Repeated letter patterns**: "aa", "ee", "oo" common in informal romanization
6. **Diacritic presence**: Pinyin tone marks, ISO transliteration diacritics

### Heuristics for "is_translation":

1. **Natural grammar**: Contains articles, prepositions, auxiliary verbs in target language
2. **Different word count**: Translation often has different word count than original
3. **Dictionary words**: Contains common vocabulary of the target language
4. **Sentence structure**: Subject-verb-object patterns in target language

### Edge case
```
Original:     سلام
Latin text:   Hello
```
"Hello" could be a loose romanization or a translation. Check:
- If user provided 2 rows: treat as translation
- If user provided 3 rows (original + romanization + translation): context from position

---

## Mixed-Script Handling

### Detection
Analyze text at the **token level**, not the line level:
```
ببین this is love من و تو
```
Tokens: `[ببین:fa] [this:en] [is:en] [love:en] [من:fa] [و:fa] [تو:fa]`

### Bidirectional Text
When RTL and LTR scripts mix:
```
Arabic base with English:  أنا love you  →  base dir: RTL, English runs: LTR isolate
English base with Arabic:  I love العربية  →  base dir: LTR, Arabic runs: RTL isolate
```

### Processing
1. Split line into script-homogeneous tokens
2. Assign direction per token (LTR or RTL)
3. Wrap each direction-switching token with `unicode-bidi: isolate`
4. Group contiguous same-script tokens
5. Each group inherits its script's segmentation and alignment rules
6. The entire line is a single alignment context

### Annotation
```
ℹ Mixed script detected: Persian + English
   Tokens 2-4 are embedded English — will not be romanized
   
ℹ Bidirectional text: Arabic (RTL) with English (LTR) segments
   Base direction: RTL; LTR segments isolated
```

---

## Complete Script Coverage Summary

| Category | Scripts Covered | Languages Covered |
|----------|----------------|-------------------|
| RTL | 7 (Arabic, Hebrew, Syriac, Thaana, N'Ko, Samaritan, Mandaic) | 25+ |
| CJK/East Asian | 6 (CJK, Hiragana, Katakana, Hangul, Bopomofo, Yi) | 5+ |
| Indic | 10 (Devanagari, Bengali, Gurmukhi, Gujarati, Odia, Tamil, Telugu, Kannada, Malayalam, Sinhala) | 20+ |
| Southeast Asian | 6 (Thai, Lao, Myanmar, Khmer, Tai Le, Tai Tham) | 10+ |
| European | 4 (Latin, Cyrillic, Greek, Armenian) | 80+ |
| Central Asian | 2 (Tibetan, Mongolian) | 5+ |
| African | 4 (Ethiopic, Tifinagh, Osmanya, Vai) | 15+ |
| Americas | 3 (Cherokee, Canadian Aboriginal, Deseret) | 5+ |
| Other | 4 (Georgian, Glagolitic, Coptic, Runic) | 5+ |
| **TOTAL** | **45+ scripts** | **170+ languages** |
