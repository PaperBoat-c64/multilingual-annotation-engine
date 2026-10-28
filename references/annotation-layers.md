# Annotation Layers — Format Specifications

## Table of Contents
- [IPA Transcription](#ipa-transcription)
- [Word-by-Word Gloss](#word-by-word-gloss)
- [Grammar Notes](#grammar-notes)
- [Frequency Statistics](#frequency-statistics)
- [Vocabulary List](#vocabulary-list)
- [Confidence Scores](#confidence-scores)

---

## IPA Transcription

### Format
Each word receives an IPA transcription in `/slashes/` or `[brackets]`.

### Detail level
- **Broad transcription** (`/.../`): phonemic, sufficient for language learners
- **Narrow transcription** (`[...]`): phonetic, for advanced study

### Example
```
Original:      سلام
Romanization:  salâm
IPA:           /sæˈlɒːm/
Translation:   hello
```

### Generation
Claude generates IPA directly. For common languages, Claude's IPA is generally accurate. For rare languages, flag with `⚠ IPA auto-generated, verify before use`.

### Placement
IPA appears as an optional additional row between romanization and translation.

---

## Word-by-Word Gloss

### Format
Leipzig Glossing Rules (standard in linguistics):

```
Original:      من     کتاب     را     خواندم
Gloss:         1SG    book     ACC    read.PAST.1SG
Translation:   I read the book.
```

### Abbreviations
| Abbreviation | Meaning |
|-------------|---------|
| 1SG, 2SG, 3SG | First/second/third person singular |
| 1PL, 2PL, 3PL | First/second/third person plural |
| ACC | Accusative |
| DAT | Dative |
| GEN | Genitive |
| NOM | Nominative |
| PAST | Past tense |
| PRES | Present tense |
| FUT | Future tense |
| PROG | Progressive |
| PERF | Perfect |
| SUBJ | Subjunctive |
| IMP | Imperative |
| NEG | Negation |
| PL | Plural |
| DEF | Definite |
| INDEF | Indefinite |
| POSS | Possessive |
| EZ | Ezafe (Persian) |
| COP | Copula |
| CL | Classifier (Chinese) |
| TOP | Topic marker (Japanese は, Korean 은/는) |

### When to generate
- Requested explicitly by user
- For academic/linguistic use cases
- When morphological decomposition is complex (Turkish, Japanese, Korean)

---

## Grammar Notes

### Format
Per-sentence or per-phrase grammatical explanation:

```markdown
### Grammar Note: Ezafe Construction
**دلِ من** (del-e man) = "my heart"

- `دل` (del) = heart
- `ِ ` (ezafe) = linking vowel connecting noun to modifier
- `من` (man) = I/me/my

The ezafe construction is unique to Persian and has no direct English equivalent.
It functions like "of" or the possessive "'s" but appears between the head noun
and its modifier.
```

### Trigger conditions
- Grammatical feature with no target-language equivalent
- Inflection that encodes multiple meanings
- Unusual word order
- Non-obvious agreement patterns

### Depth
- **Basic**: 2-3 sentence explanation (for learners)
- **Detailed**: Full linguistic analysis (for advanced study)

---

## Frequency Statistics

### Format
```markdown
## Vocabulary Frequency

| Rank | Word | Romanization | Meaning | Count | % of Text |
|------|------|-------------|---------|-------|-----------|
| 1 | دل | del | heart | 12 | 8.2% |
| 2 | تو | to | you | 9 | 6.1% |
| 3 | عشق | eshgh | love | 7 | 4.8% |
| ... | ... | ... | ... | ... | ... |

### Statistics
- Total words: 147
- Unique words: 89
- Type-Token Ratio: 0.61
- Hapax Legomena: 52 (words appearing only once)
```

### Generation
Use `scripts/frequency_analyzer.py` if available, or compute manually for small texts.

---

## Vocabulary List

### Format
```markdown
## Vocabulary List

### Core Vocabulary (frequency ≥ 3)
| Word | Romanization | Color | Meaning | Occurrences |
|------|-------------|-------|---------|-------------|
| دل | del | 🔴 | heart | 12 |
| خدا | khoda | 🟢 | God | 8 |
| عشق | eshgh | 🔵 | love | 7 |

### New Vocabulary (frequency = 1)
| Word | Romanization | Color | Meaning |
|------|-------------|-------|---------|
| پریشان | parishân | 🟡 | distressed |
| نسیم | nasim | 🟣 | breeze |
```

### Sorting
- Optional: sort by frequency (descending), then alphabetically
- Optional: group by semantic category (emotions, nature, actions, etc.)

---

## Confidence Scores

### Format
Displayed inline with annotations or as a separate summary table.

```markdown
## Alignment Confidence

| Segment | Alignment | Confidence | Note |
|---------|-----------|------------|------|
| غم | sorrow | 0.92 | |
| غزل | love poem | 0.76 | ⚠ Could also mean "ghazal (poetic form)" |
| شیر | milk | 0.82 | ⚠ "شیر" can also mean "lion" or "valve" |

### Overall
- **Average confidence**: 91%
- **Low-confidence segments (<85%)**: 3 out of 47
- **Unresolved**: 0
```

### Color coding
- 🟢 Green: ≥ 95%
- 🟡 Yellow: 85-94%
- 🟠 Orange: 70-84%
- 🔴 Red: < 70%
