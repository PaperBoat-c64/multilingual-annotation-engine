# Arabic Language Rules (ar_rules.md)

## Language Profile
- **Language**: Arabic (العربية)
- **ISO 639-1**: `ar`
- **Script**: Arabic
- **Direction**: RTL
- **Morphological Type**: Root-pattern (triliteral roots + patterns)
- **Word Order**: VSO (default), SVO (common in modern usage)
- **Script Family**: `arabic`

## Morphology Rules

### Root-Pattern System

Arabic words are built from triliteral (three-consonant) roots combined with patterns (vowel templates + affixes). Always identify the root:

**Example**: Root ك-ت-ب (k-t-b) "writing" — forms include:
- كَتَبَ (kataba) — he wrote
- يَكْتُبُ (yaktubu) — he writes
- كاتِب (kātib) — writer
- مَكْتَب (maktab) — office
- كِتاب (kitāb) — book
- مَكْتُوب (maktūb) — letter

### Morpheme Breakdown

```
يكتب (yaktubu) → "he writes"
- ك-ت-ب  → root: "writing (triliteral root)"
- يَـ    → prefix, ui_tag: "第三人称阳性 (3SG.M)"
- ـُ     → suffix, ui_tag: "现在时直陈式 (PRES.IND)"
```

### Verb Forms (الأوزان)

Arabic has 10+ derived verb forms. Each carries specific meaning:

| Form | Pattern | Meaning Shift |
|------|---------|---------------|
| I (basic) | فَعَلَ | Basic action |
| II (intensive) | فَعَّلَ | Intensive, causative |
| III (associative) | فاعَلَ | Associative, reciprocal |
| IV (causative) | أَفْعَلَ | Causative |
| V (reflexive of II) | تَفَعَّلَ | Reflexive |
| VI (reflexive of III) | تَفاعَلَ | Reciprocal |
| VII (passive) | اِنْفَعَلَ | Passive, resultative |
| VIII (reflexive) | اِفْتَعَلَ | Reflexive, acquisitive |
| X (requestative) | اِسْتَفْعَلَ | Requestative, estimative |

### Enclitic Pronouns (الضمائر المتصلة)

Enclitic pronouns attach to nouns, verbs, and prepositions:

| Enclitic | ui_tag | Meaning |
|----------|--------|---------|
| ـي (-ī) | 属格 1SG | my |
| ـكَ (-ka) | 属格/宾格 2SG.M | your / you (m) |
| ـكِ (-ki) | 属格/宾格 2SG.F | your / you (f) |
| ـهُ (-hu) | 属格/宾格 3SG.M | his / him |
| ـها (-hā) | 属格/宾格 3SG.F | her |
| ـنا (-nā) | 属格/宾格 1PL | our / us |
| ـكُمْ (-kum) | 属格/宾格 2PL.M | your / you (pl m) |
| ـهُمْ (-hum) | 属格/宾格 3PL.M | their / them (m) |

## Script-Specific Constraints

### Cursive Connections — NEVER Break

Arabic letters connect to form words. The top-level `original` string MUST preserve all connections:

```
✅ "original": "يكتب"        (fully connected)
❌ "original": "ي ك ت ب"      (isolated forms — illegible)
```

In `morphemes`, provide standalone forms.

### Tashkeel / Harakat (Vowel Diacritics)

- If original includes diacritics (َ ِ ُ ً ٍ ٌ ْ ّ), preserve them
- If absent, romanization MUST accurately reflect pronunciation
- Short vowels: a (ـَ), i (ـِ), u (ـُ)
- Sukun (ـْ): no vowel
- Shadda (ـّ): gemination (doubled consonant)

### RTL Direction

- `text_direction`: `"rtl"`
- Original row: `dir="rtl"`
- Romanization row: LTR
- Numbers always LTR in RTL context
- Punctuation: isolate from word text

### Fusha vs Ammiya (Register)

Distinguish between:
- **Fusha (فصحى)**: Modern Standard Arabic — formal, literary, media
- **Ammiya (عامية)**: Colloquial dialects — casual, everyday, regional

Mark the register in `usage_notes` when identifiable. Free translation tone should match the register.

## Romanization

- **Standard**: DIN 31635
- خ = ḫ (or kh), غ = ġ (or gh), ش = š (or sh)
- ع = ʿ, ء = ʾ
- Long vowels: ā (ا), ī (ي), ū (و)
- Tāʾ marbūṭa: -a / -at (context-dependent)

## Translation Quality Checklist

- [ ] Triliteral root identified where applicable
- [ ] Cursive connections preserved in original string
- [ ] Verb form correctly identified (I-X)
- [ ] Enclitic pronouns separated in morphemes
- [ ] Gender agreement correct in translation
- [ ] Fusha/Ammiya register distinction noted
- [ ] RTL direction correctly set
- [ ] Tashkeel preserved if present in source
- [ ] Natural word order in target language (VSO→SVO conversion if needed)
- [ ] Punctuation isolated from word text
