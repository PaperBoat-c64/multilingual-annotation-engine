# Persian Language Rules (fa_rules.md)

## Language Profile
- **Language**: Persian (فارسی)
- **ISO 639-1**: `fa`
- **Script**: Arabic (Perso-Arabic variant)
- **Direction**: RTL
- **Morphological Type**: Root-pattern + some agglutination
- **Word Order**: SOV (Subject-Object-Verb)
- **Script Family**: `arabic`

## Morphology Rules

### Prefix and Root Connection — ZWNJ Awareness

Persian uses Zero-Width Non-Joiner (ZWNJ, U+200C) between certain prefixes and their stems. When present, the prefix MUST be treated as a separate morpheme:

```
نمی‌روم (nemiravam) → "I don't go"
- نمی → prefix, ui_tag: "否定 进行时 (Negation + Progressive)"
- رو  → root: "go"
- م   → suffix, ui_tag: "第一人称单数 (1SG)"
```

**Common prefixes**:
| Prefix | ui_tag |
|--------|--------|
| می (mi-) | 进行时 (Progressive/Habitual) |
| نمی (nemi-) | 否定进行时 (Negation + Progressive) |
| ب (be-) | 虚拟式/命令式 (Subjunctive/Imperative) |
| ن (na-) | 否定 (Negation) |
| هم (ham-) | 共同 (Co-) |

### Enclitic Pronouns (ضمایر متصل)

Enclitic pronouns attach to nouns, verbs, and prepositions. List them as independent suffixes with hyphen:

| Enclitic | ui_tag | Meaning |
|----------|--------|---------|
| -am (ـم) | 属格/宾格后缀 1SG (Possessive/Objective 1SG) | my / me |
| -at (ـت) | 属格/宾格后缀 2SG | your / you |
| -ash (ـش) | 属格/宾格后缀 3SG | his/her / him/her |
| -emān (ـمان) | 属格/宾格后缀 1PL | our / us |
| -etān (ـتان) | 属格/宾格后缀 2PL | your / you (pl) |
| -eshān (ـشان) | 属格/宾格后缀 3PL | their / them |

```
دلم (delam) → "my heart"
- دل → root: "heart"
- م  → suffix, ui_tag: "属格后缀 1SG (Possessive 1SG)"
```

### Ezafe Construction (اضافه)

Ezafe (-e / -ye) links nouns to modifiers. It's unwritten in Persian script but MUST be romanized:

```
دل من (del-e man) → "my heart" (literally: heart-of me)
- دل → root: "heart"
- من → root: "me/I"
Note: ezafe is implicit — romanized as "-e"
```

## Script-Specific Constraints

### Cursive Connections — NEVER Break in Original

Persian uses connected Arabic script. The top-level `original` string MUST preserve all cursive connections:

```
✅ "original": "میروم"      (fully connected)
❌ "original": "م ی ر و م"   (isolated letters — illegible)
```

In the `morphemes` array, provide unattached standalone forms of roots and affixes.

### Tashkeel / Harakat (Vowel Diacritics)

- If original text includes diacritics (َ ِ ُ), preserve them
- If absent (most Persian text), romanization MUST accurately reflect pronunciation
- Persian short vowels: a (ـَ), e (ـِ), o (ـُ)

### BiDi — Direction is RTL

- `text_direction`: `"rtl"`
- All containers must use `dir="rtl"` for the original row
- Romanization row is LTR
- Translation row direction depends on target language
- Numbers: always LTR even in RTL context
- Punctuation: isolate from word text to prevent BiDi layout misplacement

## Sentiment & Context Rules

### Poetic Vocabulary

Persian has an extensive poetic register. When poetic vocabulary appears:

- Mark elevated/poetic words with `pos: "poetic"` or `usage_notes: "poetic register"`
- Free translation should use elevated register in the target language if available
- Common poetic markers: archaic verb forms, compound metaphors, Sufi terminology

### Verb-Final Emphasis

Persian is SOV — the verb comes last. The sentence builds tension toward the verb:
- Free translation should capture this cumulative effect
- In targets that are SVO (English, Chinese, Spanish), restructure naturally

## Romanization

- **Standard**: UniPers (Universal Persian) or DMG
- Long vowels: ā (آ/ا), i (ی), u (و)
- خ = kh, غ/ق = gh, چ = ch, ژ = zh, ش = sh

## Translation Quality Checklist

- [ ] Cursive connections preserved in original string
- [ ] ZWNJ-separated prefixes treated as independent morphemes
- [ ] Enclitic pronouns correctly identified with hyphen notation
- [ ] Ezafe construction romanized correctly
- [ ] Verb-final (SOV) restructured naturally for target language
- [ ] Poetic register conveyed in free translation
- [ ] RTL direction correctly set on original row
- [ ] Punctuation isolated from word text
