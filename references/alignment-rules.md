# Alignment Rules — Complete Specification

## Table of Contents
- [Rule 1: Semantic Priority](#rule-1-semantic-priority)
- [Rule 2: Morpheme Awareness](#rule-2-morpheme-awareness)
- [Rule 3: Syllable Fallback](#rule-3-syllable-fallback)
- [Rule 4: Translation Segmentation](#rule-4-translation-segmentation)
- [Rule 5: N:M Mapping](#rule-5-nm-mapping)
- [Rule 6: Implicit Components](#rule-6-implicit-components)
- [Rule 7: Idiomatic Handling](#rule-7-idiomatic-handling)
- [Rule 8: Confidence Scoring](#rule-8-confidence-scoring)
- [Rule 9: Color Persistence](#rule-9-color-persistence)
- [Rule 10: Transliteration Detection](#rule-10-transliteration-detection)
- [Rule 11: Annotation System](#rule-11-annotation-system)
- [Rule 12: Robustness Requirements](#rule-12-robustness-requirements)

---

## Rule 1: Semantic Priority

**Core principle**: Always align by meaning, never by character count or position.

### Correct
```
خدا  ↔  Khoda  ↔  再
حافظ ↔  hafez  ↔  见
```

### Incorrect
```
خ  د  ا  ح  ا  ف  ظ
K  h  o  d  a  h  a  f  e  z
```

Characters are not aligned — semantic units are. Each chunk must carry independent meaning.

---

## Rule 2: Morpheme Awareness

When a word contains multiple meaningful parts, decompose it.

### Example: متشکرم (moteshakkeram = "thank you" + "I am")

```
متشکر  ↔  moteshakker  ↔  感谢
م       ↔  am           ↔  我（语法成分）
```

The enclitic pronoun `-am` is a distinct morpheme and must be separated.

### Turkish example: geliyorum ("I am coming")
```
gel   ↔  come    ↔  来
iyor  ↔  PROG    ↔  正在
um    ↔  1SG     ↔  我
```

---

## Rule 3: Syllable Fallback

If semantic decomposition is impossible, use syllable boundaries.

### Example: سلام (salam = "hello")

```
سا  ↔  Sa
لام ↔  lam
```

Note: This is a fallback. Prefer semantic alignment whenever possible.

---

## Rule 4: Translation Segmentation

Translations should be segmented to match the granularity of the source.

### Correct
```
Khoda  ↔  再
hafez  ↔  见
```

### Incorrect
```
Khodahafez  ↔  再见
```

Unless no finer semantic alignment exists (e.g., idioms, fixed expressions).

---

## Rule 5: N:M Mapping

Support one-to-many, many-to-one, and many-to-many alignments.

### One-to-Many (Persian → English)
```
میروم  ↔  I am going
```
1 Persian word → 3 English words → group as ONE aligned unit with ONE color.

### Many-to-One (Chinese → English)
```
你  好  ↔  hello
```
2 Chinese characters → 1 English word → group together if 你好 is the minimal translatable unit.

### Rule: The minimal independently translatable unit defines the alignment group size.

---

## Rule 6: Implicit Components

Mark information that is implicit in one language but explicit in another.

### Persian: رفتم (raftam = "I went")
```
[implied: I] + رفت (go.PAST) + م (1SG)
```
The subject "I" is encoded in the verb suffix and has no independent word.

### Japanese: 食べた (tabeta = "ate")
```
[implied: I/he/she] + 食べ (eat) + た (PAST)
```
Subject is implicit. Mark as `[implied: subject]`.

### Format
```
[implied: <role>]
```

---

## Rule 7: Idiomatic Handling

Non-literal translations must be annotated.

### Persian: دلم برات تنگ شده
- Literal: "my heart has become narrow for you"
- Translation: "I miss you"

**Action**: Align as a single semantic block. Add annotation:
```
⚠ Idiomatic expression. Literal: "my heart has become narrow for you."
No word-level alignment possible. Human review recommended.
```

### Annotation format
```
[idiomatic] — confidence: <0.0-1.0>
Literal gloss: <word-by-word>
```

---

## Rule 8: Confidence Scoring

Every alignment receives a confidence score [0.0 - 1.0].

| Score | Meaning | Action |
|-------|---------|--------|
| 0.95-1.0 | Certain | No annotation needed |
| 0.85-0.94 | High confidence | Optional annotation |
| 0.70-0.84 | Moderate | ⚠ annotation recommended |
| < 0.70 | Low | ⚠ annotation required; human review |

### Scoring factors:
- Semantic transparency of the word
- Language pair distance (e.g., Persian→English harder than French→English)
- Presence of multiple possible translations
- Contextual ambiguity

---

## Rule 9: Color Persistence

Same aligned units must use identical colors across the entire document.

### Example
If `Khoda` appears 15 times in a document, ALL 15 occurrences must use the **same** color. Never randomly recolor.

### Implementation
- Maintain a global in-document color map
- Before assigning a new color, check if the word already exists in the map
- Cross-document consistency: use `scripts/color_engine.py` with SQLite persistence

---

## Rule 10: Transliteration Detection

Automatically classify each row as one of:
- `original` — source language text
- `romanization` — pronunciation guide in Latin script
- `translation` — target language translation

### Detection heuristics
1. If a Latin row contains only lowercase a-z and matches expected romanization patterns → `romanization`
2. If a Latin row contains English words, articles, natural syntax → `translation`
3. Compare word count: romanization typically matches original word count 1:1; translations may differ

### Ambiguous case
```
Line 1: خداحافظ
Line 2: Goodbye
```
Is Line 2 a very loose romanization ("Khodahafez" → "Goodbye") or a translation?

**Resolution**: If Line 2 contains English dictionary words (not transliteration patterns), classify as `translation`. Flag ambiguity if uncertain.

---

## Rule 11: Annotation System

### Annotation triggers
- Alignment confidence < 90%
- Idiomatic expressions
- Multiple valid translations
- Homographs (same spelling, different meaning)
- Missing implied components
- Ambiguous romanization

### Annotation format
```
⚠ <type>: <description>
Possible alternatives: <list>
Context: <surrounding text>
Recommendation: <action>
```

### Examples
```
⚠ Ambiguity: "شیر" could mean "milk", "lion", or "valve"
   Context: "شیر سفید" → likely "milk" (white milk) or "lion" (white lion)
   Confidence: 0.75
   Recommendation: Human review if meaning is critical
```

```
⚠ Alignment gap: "غم" (gham) aligns to both "sorrow" and "sadness"
   Selected: "sorrow" (higher register match)
   Confidence: 0.82
```

---

---

## Rule 13: Translation Word Order — Natural Native Expression

**Core principle**: Translation rows MUST use natural target-language word order. Mechanical word-by-word mapping is FORBIDDEN when it produces unnatural results.

### SOV → SVO Reordering

Hindi, Urdu, Turkish, Japanese, and Korean are SOV (Subject-Object-Verb). Chinese and English are SVO. Translation MUST reorder:

```
Hindi SOV:  मैं  तुमसे  प्यार  करता  हूँ
            I    you     love   do      am
Chinese SVO: 我    爱      你
             I    love    you
```

**Never**: "我你爱着" (mechanical). **Always**: "我爱你" (natural).

### Postposition → Preposition Conversion

Hindi/Urdu/Turkish/Japanese/Korean use postpositions (noun + particle). Chinese/English use prepositions:

```
Hindi:  बाँहों  में   →  Chinese: 在  怀抱  里
        arms    in               in  arms  inside
```

### Possessor-Noun Reordering

In Hindi/Urdu, possessors follow nouns. In Chinese, possessors precede nouns:

```
Hindi:  आँखें  मेरी   →  Chinese: 我的  眼睛
        eyes    my               my   eyes
```

### Priority Order

1. **Semantic Accuracy** — meaning must be correct
2. **Natural Native Expression** — reads like a native speaker wrote it
3. **Grammar Correctness** — follows grammatical rules of target language
4. **Alignment Consistency** — colors remain consistent across reordering
5. **Word-by-word Mapping** — lowest priority; sacrifice before 1-4

### Song Lyric Special Rules

Allowed:
- Reorder words freely for natural expression
- Merge adjacent phrases when word-by-word is unnatural
- Add implied subjects/objects that are implicit in the source
- Use idiomatic target-language expressions

Forbidden:
- Preserving source word order at the expense of naturalness
- Mechanical glosses that read like machine translation
- Grammatical annotations in translation text (use annotation layer instead)

### Implementation

Each line defines TWO orders:
1. `source_order` — for original + romanization rows (source word order)
2. `trans_order` — for translation row (natural target-language order)

Colors persist across both orders, linking each source word to its translation regardless of position.

### Validation Pass (Mandatory)

After generating translations, perform a second pass:
1. Check for mechanical word-by-word translation traces
2. Verify the translation reads naturally to a native speaker
3. Check word order is natural for the target language
4. If any issue found → regenerate translation with natural ordering
5. Only output validated translation

The engine must handle:

### Document types
- Poetry (irregular line breaks, meter constraints)
- Song lyrics (repetition, refrain, emotional language)
- Religious texts (archaic language, formulaic expressions)
- Dictionaries (word-definition pairs)
- Bilingual books (paragraph-aligned, not word-aligned)
- Subtitles (time-coded, conversational)
- OCR output (errors, missing characters, artifact text)

### Format irregularities
- Missing transliteration rows → generate auto-detected warning
- Duplicated lines → detect and deduplicate
- Mixed RTL/LTL on same line → segment by script before processing
- Malformed Unicode → attempt NFKC normalization, flag if still broken

### Degradation strategy
When unable to fully process:
1. Attempt partial alignment (align what you can)
2. Mark unaligned segments with `[unaligned]` tag
3. Generate a degradation report
4. NEVER silently skip content — always flag

---

## Related References

- **`emotion-preservation.md`** — Emotion & Style Review Pass: applies AFTER alignment to ensure translations preserve emotional fidelity, tone, and native expression. Alignment provides the structural map; emotion review ensures the translation feels human.
- **`annotation-layers.md`** — Format specs for gloss rows (word-by-word, color-aligned) vs translation rows (natural, flowing, emotionally faithful).
