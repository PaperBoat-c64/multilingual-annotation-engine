---
name: multilingual-annotation-engine
description: Transform lyrics into color-aligned multilingual translations with automatic language detection, romanization, semantic alignment, interactive word-level tooltips, and export to HTML + DOCX. Three-tab interface: annotated (color-aligned), reading (side-by-side), vocabulary (word cards). Apple Music + DeepL inspired minimal design. Use when the user wants lyric translation, multilingual annotation, romanization, transliteration, color-coded translation, semantic alignment, or interactive reading of foreign text.
---

# Multilingual Lyrics Translation Engine

## Overview

A lightweight, highest-quality lyric alignment translator. Transform song lyrics from any language into beautifully aligned multilingual displays — every word aligned, every color meaningful.

**Primary mission**: Build the highest-quality lyric alignment translator possible.

**Core principles**: Translation accuracy above all. Word alignment precision. Robustness against noise. Clean reading experience. No unnecessary features.

---

## Dynamic Routing Architecture

The system uses a **three-layer dynamic routing architecture** (Dynamic Routing & On-demand Loading) to minimize token consumption while maximizing parsing accuracy:

```
┌─────────────────────────────────────────────────────┐
│  Layer 1: Router Agent (Pre-processing)             │
│  Language ID + Sentiment detection                  │
│  Ultra-lightweight, structured output only          │
└──────────────────────┬──────────────────────────────┘
                       │ lang_code + sentiment
                       ▼
┌─────────────────────────────────────────────────────┐
│  Layer 2: Context Retrieval (Backend Logic)         │
│  Load per-language rule documents                   │
│  e.g., ja_rules.md, fa_rules.md, ko_rules.md       │
└──────────────────────┬──────────────────────────────┘
                       │ dynamic language rules
                       ▼
┌─────────────────────────────────────────────────────┐
│  Layer 3: Generator Agent (Core Processing)         │
│  Deep parsing with color mapping + morpheme         │
│  breakdown + sentiment-aware translation            │
│  Output: structured JSON for frontend rendering     │
└─────────────────────────────────────────────────────┘
```

### Layer 1: Router Agent (Pre-processing)

**Purpose**: Quick, low-token, structured classification. The Router ONLY identifies language and sentiment — no parsing, no translation.

**Router System Prompt**:

> You are a highly efficient linguistic router. Your sole purpose is to analyze the provided lyrics, identify the primary language, and determine the emotional sentiment.
>
> **Task:**
> 1. Identify the language using ISO 639-1 code (e.g., "ja" for Japanese, "fa" for Persian, "es" for Spanish).
> 2. Identify the primary emotional sentiment/vibe of the text (e.g., melancholic, energetic, romantic, aggressive, tender, defiant, nostalgic).
>
> **Rules:**
> - Output strictly in JSON format.
> - Do not provide any explanations, notes, or conversational text.
>
> **Output Format:**
> ```json
> {
>   "lang_code": "ja",
>   "sentiment": "melancholic"
> }
> ```

The Router's `sentiment` output feeds directly into Layer 3's `{{USER_SENTIMENT}}` parameter, ensuring the translation tone matches the song's emotional register. The Router runs as the **first step of every pipeline execution** — before noise recovery, before anything else.

### Layer 2: Context Retrieval (Backend Logic)

Based on the Router's `lang_code` output, load the corresponding **per-language rule document** from `references/language-rules/`. These documents contain:

- **Morphology rules**: How to decompose words in this language (agglutinative, fusional, analytic, root-pattern)
- **UI tag conventions**: Language-appropriate beginner-friendly grammar tags (e.g., "过去时" instead of "PST", "主语标记" instead of "NOM")
- **Sentiment & context rules**: How register, politeness levels, and formality affect translation tone
- **Script-specific constraints**: Cursive connections, syllabic blocks, abugida handling, BiDi considerations

**Available rule documents**:

| Language | Rule Document | Key Features |
|----------|--------------|--------------|
| Japanese | `ja_rules.md` | Agglutinative, te-form, sentence-final particles (ね/よ/わ), plain/polite register |
| Korean | `ko_rules.md` | Agglutinative, speech levels (합쇼체/해요체/해체), subject/object particles, tense suffixes |
| Chinese | `zh_rules.md` | Analytic, aspect markers (了/过/着), 成语, register (口语/书面语), measure words |
| Arabic | `ar_rules.md` | Root-pattern (triliteral), cursive connections, Tashkeel/Harakat, RTL, enclitic pronouns |
| Persian | `fa_rules.md` | Root-pattern, ezafe construction, ZWNJ, RTL, poetic vocabulary |
| Spanish | `es_rules.md` | Fusional, verb conjugation (person+number+tense), diminutives (-ito/-ita), reflexive pronouns |
| French | `fr_rules.md` | Fusional, elision/liaison, gender agreement, register levels |
| German | `de_rules.md` | Fusional, separable prefixes, compound noun decomposition, V2 word order |
| Russian | `ru_rules.md` | Fusional, aspect pairs (IPFV/PFV), 6-case system, poetic inversion |
| Turkish | `tr_rules.md` | Agglutinative, vowel harmony, SOV word order, evidentiality marker (-miş) |
| Hindi/Urdu | `hi_rules.md` | SOV, postpositions, gender agreement, Sanskrit/Persian vocabulary balance |
| Thai | `th_rules.md` | Analytic, politeness particles (ครับ/ค่ะ), register, dictionary-based segmentation |
| Vietnamese | `vi_rules.md` | Analytic, classifiers, kinship-based pronouns, tone sensitivity |

If no rule document exists for the detected language, use `references/language-rules/_general_rules.md` as fallback. All rule documents follow a consistent structure so the Generator can consume them uniformly.

### Layer 3: Generator Agent (Core Processing)

**Purpose**: Execute deep linguistic parsing with the full context of language-specific rules. The Generator carries the general annotation instructions and the dynamically loaded per-language rules, producing structured JSON with color mapping, morpheme breakdown, and sentiment-aware translation.

The Generator's system prompt is constructed by injecting the language rules and sentiment:

```
You are an expert linguistic processor and lyric annotator designed to help
language beginners. You will receive a snippet of lyrics in a foreign language.

Your goal is to parse the text into a highly structured JSON format, mapping
original words to their romanization, free translation, and simplified
morphological breakdown.

Context & Rules:
1. Dynamic Language Rules: Pay strict attention to the following
   language-specific guidelines for translation and emotion handling:
   <language_rules>
   {{DYNAMIC_LANGUAGE_RULES}}
   </language_rules>

2. Sentiment Awareness: Adapt your translation tone based on the target
   sentiment: [ {{USER_SENTIMENT}} ].

3. Beginner-Friendly Glossing (Simplified Leipzig):
   - Break down complex words into roots (词根) and affixes (词缀).
   - Translate linguistic jargon into beginner-friendly UI tags
     (e.g., instead of "ACC", use "宾语目标"; instead of "PST", use "过去时").
   - Detailed rules in Step 5b: Morpheme Breakdown.

4. Color Mapping: Assign a hex color code to each word block. Ensure the
   color perfectly matches between the original word, its romanization,
   and its specific translation. Use a harmonious, modern color palette
   suitable for UI design.

5. JSON Structure Requirement: Return ONLY valid JSON. No markdown formatting
   blocks (like ```json), no intro, no outro.

6. Three-Stage Translation Pipeline (三步翻译法): Execute the following
   mandatory pipeline for EVERY line of translation. Never skip a stage.
   Never perform word-for-word literal translation (字对字直译).

   **Stage 1 — 文本解构与纠错 (Deconstruction & Segmentation)**:
   - If the source text has missing spaces, OCR粘连, or agglutinative
     writing (e.g. Arabic/Hebrew/Thai without spaces, Japanese without
     word boundaries), perform precise word segmentation first.
   - Deconstruct prefixed prepositions, suffixed possessive pronouns,
     agglutinative morphemes, definite articles, and inflectional
     changes. Restore the core syntactic frame.
   - Identify idioms, fixed expressions, and compounds — treat them as
     single semantic units, not literal word sums.

   **Stage 2 — 跨语系语法重构 (Cross-Family Syntactic Reordering)**:
   🔴 NO LITERAL TRANSLATION. Reconstruct every sentence according to
   the target language's natural grammar:
   - **Modifier Position Adjustment**: If the source language places
     modifiers after the head (e.g. Hebrew/Arabic/French adjective or
     possessive post-position: `noun + שלי/de/du`), restructure to the
     target language's natural modifier order (e.g. Chinese/Japanese
     "modifier + noun", English pre-modification).
   - **SVO/SOV/VSO Mapping**: When switching between SVO (主谓宾), SOV
     (主宾谓), and VSO (谓主宾) language families, completely reorder
     constituents to match the target language's natural syntax.
     Eliminate any residual source-language syntactic inversion.
   - **Preposition & Adverbial Placement**: Reposition post-positional
     phrases, temporal/locative adverbials to the most natural position
     in the target language. Never preserve source adverbial order at
     the expense of naturalness.

   **Stage 3 — 信达雅润色 (Fluency & Polish)**:
   - **信 (Fidelity)**: Precisely convey the source text's surface
     semantics, deep metaphors, and emotional tone.
   - **达 (Expressiveness)**: Completely eliminate "translationese"
     (翻译腔). Ensure the output flows naturally with coherent logic
     conforming to target-language conventions.
   - **雅 (Elegance)**: Match the optimal lexical richness and
     sentence-level rhythm appropriate for the context (poetry/literary/
     formal/colloquial/technical). The translation must read as if
     originally authored in the target language by a native speaker.

   **Self-Correction Loop**: After Stage 3, verify the output against
   all three criteria. If any criterion is not met, return to Stage 2
   and re-generate. Only proceed when all three stages pass.

   **Universal Quality Rules**:
   - **Proper nouns**: Use established conventional translations.
     Retain original or append parenthetical pronunciation when needed.
   - **Idioms & Proverbs**: Prioritize semantic equivalence (意译优先,
     神似为主). Find functionally equivalent idioms in the target
     language. Never translate idioms literally word-for-word.
   - **Format preservation**: Strictly preserve the original paragraph
     structure, punctuation rhythm, and typographic style.
```

---

## GLOBAL LANGUAGE OPTIMIZATION LAYER

The system is truly **language-agnostic**. It does not optimize primarily for English, Chinese, Japanese, or Korean. The architecture supports **any human language** equally.

### Architecture Mandates

1. **No language is primary.** Every language receives equal architectural treatment.
2. **Script-first design.** Features are organized by writing system properties, not by language popularity.
3. **Direction-neutral.** LTR and RTL are first-class citizens. No direction is the "default."
4. **Typography-aware.** Every script receives its own font stack, sizing, and spacing rules.
5. **Morphology-respecting.** Tokenization adapts to the morphological type of each language.

---

## Priority Order

1. **Translation Accuracy** — Natural, native-quality translation. Never mechanical gloss. 信达雅 (Faithfulness, Expressiveness, Elegance) for every language.
2. **Word Alignment Accuracy** — Every word aligned. One-to-one correspondence whenever possible.
3. **Robustness** — Handle noisy input, broken lyrics, mixed scripts. Never crash silently.
4. **Reading Experience** — Clean, minimal, elegant display. Apple Music + DeepL inspired.
5. **Performance** — Fast processing. Lightweight output. Vanilla frontend.

---

## Target Language Configuration

**The target language is USER-CONFIGURABLE.** Never assume a default target language. The system translates from **any source language → any target language** with equal quality. No target language is privileged or default.

### Detecting the Target Language

Parse the user's request for target language signals:

| User says | Target Language | Language Code |
|-----------|----------------|---------------|
| "translate to Spanish" | Spanish | `es` |
| "French translation" | French | `fr` |
| "in Arabic" | Arabic | `ar` |
| "translate to Japanese" | Japanese | `ja` |
| "Russian output" | Russian | `ru` |
| "한국어로 번역" | Korean | `ko` |
| "auf Deutsch" | German | `de` |
| "en français" | French | `fr` |
| "中文翻译" | Chinese | `zh` |
| "بالعربية" | Arabic | `ar` |

**Parsing rules**:
1. Check for "to <language>", "in <language>", "into <language>" patterns
2. Check for target language names written in their native script (中文, 日本語, 한국어, العربية, فارسی, etc.)
3. Check for ISO language codes (en, es, fr, de, ja, ko, zh, ar, ru, etc.)
4. If the target language IS the source language → error: "Cannot translate to the same language. Please specify a different target language."
5. If the user specifies "English" → respect it (English IS a valid target language, but it is ONE of many equally valid choices, never the default)

### When Target Language is NOT Specified

**DO NOT assume any language (including English).** Prompt the user:

> "What target language would you like the translation in? (e.g., Spanish, Arabic, Japanese, French, Russian, Korean, Hindi, German, etc.)"

Never default to any language silently. The user must explicitly choose the target language.

### All Languages Are Valid Targets

ALL 100+ languages in the Supported Languages table are valid both as source AND as target. The system provides equal quality for every target language:

- **Right-to-left targets**: Arabic, Hebrew, Persian, Urdu, Pashto, Uyghur, etc. — use `dir="rtl"` layout, RTL typography
- **CJK targets**: Chinese, Japanese, Korean — use CJK fonts and typography
- **Indic targets**: Hindi, Bengali, Tamil, Telugu, etc. — use Indic fonts and typography
- **European targets**: English, Spanish, French, German, Russian, etc.
- **Southeast Asian targets**: Thai, Vietnamese, Khmer, Burmese, etc.
- **African targets**: Amharic, Swahili, Yoruba, Zulu, etc.
- **Turkic targets**: Turkish, Kazakh, Uyghur, Uzbek, etc.

### Pipeline Configuration for Target Language

Once the target language is determined, the entire pipeline is configured around it:

1. **Translation engine**: Produce natural, native-quality output in the target language
2. **Font loading**: Load script-appropriate fonts for the target language's writing system
3. **Direction**: Set `dir="rtl"` in output if target language is RTL (Arabic, Hebrew, etc.)
4. **Typography**: Apply script-appropriate sizing and spacing for the target language
5. **Quality standards**: Apply 信达雅 criteria from the perspective of a native target-language speaker
6. **Language-specific optimization**: Apply target-language conventions (see Target Language Quality Pipeline)

---

## Script Detection

Automatically detect Language, Writing System, and Directionality for every input.
Supports 30+ writing systems (Latin, Arabic, Hebrew, CJK, Devanagari, Cyrillic, Thai,
and more). See the Supported Languages table below for the full matrix with directionality.

Detection: Unicode block analysis → script-specific disambiguation → direction assignment.
Mixed-script text handled per-token.

Full reference: `references/script-detection.md`

---

## RIGHT-TO-LEFT SUPPORT (Mandatory)

Full RTL support for Arabic, Hebrew, Urdu, Persian, Pashto, Sindhi, Kurdish, Uyghur,
Dhivehi, and all other RTL scripts. Automatically mirrors layout, tooltip positioning,
and color mapping via `dir="rtl"`.

Full reference: `references/rtl-layout-engine.md`

---

## Bidirectional Text Support

Mixed-content text (Arabic+English, Hebrew+Numbers, Chinese+Arabic) handled via
`unicode-bidi: isolate` on every segment. Numbers always LTR regardless of parent.

Full reference: `references/bidirectional-text.md`

---

## Romanization Standards

Uses language-specific standards — never one universal system: Pinyin (CN), Hepburn (JP),
Revised Romanization (KR), DIN 31635 (AR), ISO 15919 (Indic), RTGS (TH), Wylie (Tibetan),
and more. Full reference with alternatives: `references/romanization-systems.md`

---

## Tokenization Engine

Language-aware tokenization — never assumes whitespace-separated words. CJK: word
segmentation. Japanese/Korean: morphological. Arabic: clitic separation. Agglutinative
languages: stem+affix decomposition. Thai/Khmer/Burmese: dictionary-based.

Full reference: `references/tokenization-engine.md`

---

## Morphological Analysis

Supports complex morphology: agglutination (Turkish, Finnish, Hungarian), root-pattern
(Arabic), fusional (Russian, German, Sanskrit). Identifies stems, affixes, particles,
and grammatical markers for alignment.

Full reference: `references/morphological-analysis.md`

---

## Poetry-Aware Translation

Lyrics are not ordinary text. The translation preserves:

- **Mood**: Emotional tone (longing, joy, melancholy, defiance)
- **Imagery**: Visual and sensory metaphors in the target language
- **Metaphor**: Cultural metaphor mapping (not literal rendering)
- **Poetic Rhythm**: Syllable count and natural cadence in target language
- **Narrative Voice**: First-person intimacy, third-person distance, register
- **Cultural Symbolism**: Culturally-loaded terms with explanatory alternatives

### Translation Quality: 信达雅 (Faithfulness, Expressiveness, Elegance)

Every translation must satisfy three criteria, applied through the mandatory
**Three-Stage Translation Pipeline (三步翻译法)** defined in Layer 3 above:

1. **信 (Xìn) — Faithfulness** (Stage 1 output): Accurate to the source meaning. No fabrication. All deconstructed morphemes correctly mapped.
2. **达 (Dá) — Expressiveness** (Stage 2 output): Reads naturally to a native speaker. No translationese. Syntactic reordering complete — the target-language native word order drives the segment arrangement.
3. **雅 (Yǎ) — Elegance** (Stage 3 output): Appropriate register and poetic quality. Beautiful to read. Reads as if originally authored in the target language.

This standard applies to **ALL languages equally**, not only Chinese.

**Core Anti-Pattern**: Word-for-word literal translation (字对字直译) is the
root cause of all translationese. The three-stage pipeline is designed to
eliminate it: deconstruct (Stage 1) → reorder (Stage 2) → polish (Stage 3).

Full reference: `references/poetry-translation.md`

---

## Target Language Quality Pipeline

**All quality checks MUST be performed in the target language.** The translation is evaluated from the perspective of a native speaker of the target language — never from the source language perspective.

### Native-Speaker Validation Standard

The final output must satisfy a native speaker of the target language. This means:

1. **Naturalness**: A native speaker should not be able to tell it's a translation. It should read as if originally written in the target language.
2. **Idiomatic correctness**: Collocations, phrases, and expressions must be authentic to the target language.
3. **Register appropriateness**: The formality level must match what a native speaker would use in the given context (song lyrics, poetry, etc.).
4. **Cultural resonance**: References, metaphors, and imagery should resonate with the target culture. When source-cultural elements are preserved, they should be framed naturally in the target language.
5. **No calques**: Never calque (loan-translate) source-language structures that sound unnatural in the target language.

### Mandatory Quality Verification Loop

**Before finalizing any translation**, run the following quality verification. This is NOT optional — every translation must pass all checks before being accepted.

Ask these 7 questions for EVERY line of the translation:

| # | Question | What to Check |
|---|----------|---------------|
| 1 | **Is the meaning accurate?** | Does the translation faithfully convey the source meaning? No omissions, no additions, no distortions. |
| 2 | **Is the grammar natural?** | 🔴 **Word order FIRST**: Are the segments in natural target-language order? (SOV→SVO, postpositions→prepositions, modifier-before-head, etc.) Then check agreement, tense, aspect, function words. No source-language grammar leaking through. |
| 3 | **Would a native speaker actually say this?** | Read it aloud (mentally). Does it sound like something a native speaker would spontaneously produce — not a translation? |
| 4 | **Is there a more idiomatic expression?** | Could a fixed phrase, collocation, or idiom in the target language express this more naturally? |
| 5 | **Is there a fixed phrase that should be used?** | For common expressions (greetings, emotions, transitions), is there a conventional phrase in the target language that should replace a literal rendering? |
| 6 | **Does the translation preserve the emotion?** | Is the emotional tone (longing, joy, melancholy, defiance, tenderness) preserved? Does it hit with the same emotional weight? |
| 7 | **Does it sound like lyrics rather than a dictionary entry?** | Is it poetic, rhythmic, singable? Or does it read like a textbook gloss? Lyrics have cadence, compression, and musicality. |

#### The Loop

```
1. Translate the line
2. Ask all 7 questions
3. If ANY answer is "No" → revise the translation → go back to step 2
4. Only when ALL 7 answers are "Yes" → the translation is accepted
5. Move to the next line
```

**Repeat until all checks pass.** A translation is not complete until every line gets a "Yes" on all 7 questions. If a line requires 3 revisions, do 3 revisions. If it requires 5, do 5. Never settle for "close enough."

#### Target-Language Convention Check

In addition to the 7 questions above, verify against target-language-specific conventions:
- [ ] RTL languages: Is the text direction correct? Are numbers and embedded LTR text handled?
- [ ] CJK languages: Is the character choice appropriate (Simplified vs Traditional Chinese, Kanji vs Kana balance)?
- [ ] Gender-marking languages (Arabic, Hebrew, French, Spanish, Russian, Hindi, etc.): Is gender agreement correct?
- [ ] Honorific languages (Japanese, Korean, Javanese, etc.): Is the politeness level appropriate for lyrics?
- [ ] Tone languages (Chinese, Thai, Vietnamese, Yoruba, etc.): Are tonal patterns euphonic?
- [ ] Case-marking languages (Russian, German, Arabic, Turkish, etc.): Are cases used correctly?
- [ ] Agglutinative languages (Turkish, Finnish, Hungarian, Korean, etc.): Is the morphology natural?

#### Correction Procedure

When any check fails:
1. Identify which of the 7 questions returned "No" (may be multiple)
2. Diagnose the root cause — is it a word choice issue, a grammar issue, or a phrasing issue?
3. Re-generate the translation addressing the specific failures
4. Re-verify ALL 7 questions (not just the ones that failed — a fix can break something else)
5. Continue until all 7 pass

### Target-Language-Specific Optimization

Just as the source language receives optimization, the **target language** must receive equal optimization:

| Target Language | Optimization Required |
|----------------|----------------------|
| **Japanese** | Appropriate keigo level, natural particle usage, kanji/kana balance for lyrics |
| **Chinese** | Natural 口语/书面语 register, correct 成语 usage if elevated, measure words |
| **Korean** | Appropriate speech level (합쇼체/해요체/해체), natural particle usage, spacing rules |
| **Arabic** | Natural Fusha/Ammiya register choice, correct gender agreement, natural word order |
| **Persian** | Natural ezafe construction, appropriate poetic vocabulary, correct verb-final placement |
| **Hindi/Urdu** | Natural gender agreement, appropriate Sanskrit/Persian vocabulary balance, natural SOV order |
| **Russian** | Correct aspect pairs, natural case usage, natural word order (not forced SVO) |
| **Turkish** | Natural agglutination, vowel harmony, natural SOV with appropriate deviations |
| **French** | Natural elision and liaison flow, appropriate register, correct gender agreement |
| **Spanish** | Natural subjunctive usage, correct ser/estar distinction, natural pronoun placement |
| **German** | Natural verb position (V2 in main clauses, verb-final in subordinate), correct case and gender |
| **Thai** | Natural particle usage (ครับ/ค่ะ/นะ/สิ), natural word boundaries, appropriate register |
| **Vietnamese** | Natural classifier usage, correct tone-sensitivity, natural pronoun system (kinship-based) |
| **Swahili** | Natural noun class agreement, natural verb extensions, appropriate Bantu word order |

### Anti-Pattern: Source-Language Contamination

❌ **German source → English target**: "I have myself the lyrics annotated" (calque of "Ich habe mir...")
✅ **German source → English target**: "I annotated the lyrics"

❌ **Japanese source → Spanish target**: Subject-object-verb order preserved
✅ **Japanese source → Spanish target**: Natural SVO with implied subject marked

❌ **Arabic source → French target**: Literal rendering of إضافة (iḍāfa) as "le X de le Y"
✅ **Arabic source → French target**: Natural French genitive construction

❌ **Chinese source → Russian target**: Preserving Chinese topic-comment structure
✅ **Chinese source → Russian target**: Natural Russian subject-predicate structure with correct cases

❌ **Hindi (SOV+postpositions) → Chinese (SVO+prepositions)**: Preserving Hindi word order
```
अब यहाँ से कहाँ जाएँ हम
→ ❌ 此刻 这里 从 何方 去 我们  (word-by-word gloss, unintelligible)
→ ✅ 此刻我们从这里去往何方    (natural Chinese SVO order)
```
✅ **Hindi source → Chinese target**: Segments reordered to natural Chinese syntax — SOV→SVO, postpositions→prepositions, modifier-before-head

> **CRITICAL RULE**: The translation row's `segments` array MUST be ordered by target-language syntax, NOT source-language word order. This means the same color appears in different positions across rows. The `group_id` links semantics; the array position controls reading order. **If concatenating the translation segments produces unnatural word order, the segment ordering is WRONG — fix it, regardless of how it affects cross-row visual alignment.**

---

## Language-Specific Optimization

Per-language optimization for Japanese (keigo, particles, implied subjects), Chinese
(成语, register, measure words), Korean (speech levels, honorifics), Hindi/Urdu
(Persian vs Sanskrit vocabulary), Arabic (root patterns, Fusha/Ammiya), Russian
(aspect pairs, cases, poetic inversion), Turkish (agglutination, vowel harmony),
Persian (ezafe, poetic metaphors), Thai (implicit grammar, particles), Vietnamese
(classifiers, tones), and all other supported languages.

Full reference: `references/language-specific-optimization.md`

---

## Font System

Script-appropriate font stacks for all 30+ writing systems (Noto Sans family primary,
script-specific fallbacks). No tofu (□) guarantee. Script-aware sizing, line height,
and RTL font-feature-settings. Fully implemented in the HTML template and DOCX output.

Full reference: `references/font-system.md`

---

## Language Robustness Test

The system successfully processes lyrics from:

- Japanese songs (J-Pop, Enka, Anime)
- Arabic nasheeds and pop songs
- Hindi film songs (Bollywood)
- Russian rock and pop songs
- Hebrew folk and contemporary songs
- Turkish pop and arabesk songs
- Persian poetry songs and traditional music
- Uyghur music
- Mongolian songs (Cyrillic + Traditional script)
- Thai pop and luk thung
- Vietnamese pop and folk songs
- Korean K-Pop and ballads
- Mixed-language songs (code-switching lyrics)

Quality target remains **consistent regardless of language**.

---

## Mandatory Output Structure

Every lyric annotation produces exactly three rows per line:

```
Original Lyrics        →  source script, bold, largest
Romanization / Transliteration  →  Latin script, italic, medium
Translation            →  target language, flowing natural expression
```

## Word Alignment

Every word must be aligned across all three rows:

- **One-to-one correspondence** whenever possible
- Original ↔ Romanization ↔ Translation maintain strict alignment
- N:M mappings only when linguistically unavoidable (idioms, compounds)
- Every alignment unit receives a unique `group_id`

## Color Mapping

Aligned words share identical colors across all rows:

```
original word ─── color #E74C3C
romanization  ─── color #E74C3C
translation   ─── color #E74C3C
```

- Same semantic unit → same color across ALL rows
- Repeated vocabulary → reuse the EXACT same color globally
- Colors are persistent via SQLite lexicon (`scripts/color_engine.py`)

## Quick Start

```
Translate this Chinese song lyric to Spanish.

<text>
月亮代表我的心
你问我爱你有多深
我爱你有几分
</text>
```
→ Generates HTML + DOCX with original + pinyin + **Spanish** translation, color-aligned.

```
Translate this Persian lyric to Arabic.

<text>
خداحافظ
دل من رفت و دلم را نبرد
</text>
```
→ Generates HTML + DOCX with original + romanization + **Arabic** (RTL) translation.

```
Clean and translate this Japanese lyric to Russian. HTML output only.

<text>
[00:23.45] 君の名は
www.lyrics-site.com
(C) 2024 Sony Music
</text>
```
→ Noise removed → HTML with original + romanization + **Russian** translation.

**Specifying target languages**: Always include the target language in your request. Examples:
- `Translate to French` / `French translation` / `en français`
- `Translate to Korean` / `한국어로 번역` / `Target: ko`
- `Translate to Hindi` / `हिंदी में अनुवाद`
- `Translate to Arabic` / `بالعربية` / `Target: ar`
- If no target language is specified, the system will ask you to choose one.

## Pipeline Workflow

Execute these steps in order. Claude handles reasoning (detection, segmentation, alignment, glossing). Scripts handle deterministic operations (noise removal, color assignment, file export).

### Step 0: Routing (Language ID + Sentiment)

**Always run first, before noise recovery.** Execute the Router Agent:

1. Identify the source language (ISO 639-1 code)
2. Identify the primary emotional sentiment (melancholic, energetic, romantic, aggressive, tender, defiant, nostalgic)

This is a lightweight classification step — no parsing, no translation. The sentiment output feeds into the Generator's `{{USER_SENTIMENT}}` parameter for tone-aware translation.

**Output format**:
```json
{"lang_code": "ja", "sentiment": "melancholic"}
```

### Step 0.5: Context Retrieval

Based on the Router's `lang_code`, load the corresponding per-language rule document from `references/language-rules/`:

1. Check if a language-specific rule document exists (e.g., `ja_rules.md`, `fa_rules.md`)
2. If yes → load it as `{{DYNAMIC_LANGUAGE_RULES}}`
3. If no → load `references/language-rules/_general_rules.md` as fallback
4. The loaded rules are injected into the Generator Agent's system prompt

This step ensures every language receives its own morphological rules, UI tag conventions, and script-specific constraints.

### Step 1: Noise Recovery Engine

**Always run first.** Automatically detect and remove noise from input:

| Noise Type | Examples | Detection |
|-----------|----------|-----------|
| Timestamps | `[00:23.45]`, `(3:15)`, `01:59` | Regex patterns |
| URLs | `www.lyrics.com`, `https://...` | URL pattern matching |
| Advertisements | "Download our app", "Click here" | Keyword matching |
| Copyright notices | `(C) 2024 Sony`, `Ⓒ All Rights Reserved` | Pattern + keyword |
| Navigation text | "Back to top", "Next →", breadcrumbs | Structural patterns |
| Comments | `<!-- HTML comments -->`, `// code comments` | Comment syntax |
| Metadata headers | "Artist:", "Album:", "Year:" | Key-value patterns |
| OCR noise | `君 の 名 は` → extra spaces, artifacts | Character distribution |
| Empty/whitespace lines | Blank lines between content | Trim check |
| HTML tags/entities | `<br>`, `<div>`, `&nbsp;` | Tag/entity patterns |
| Page numbers | "Page 3", "— 42 —" | Number patterns |
| Social media handles | `@username`, `#hashtag` | @/# prefix |
| Curly quotes/smart quotes | `"`, `"` | Unicode normalization |
| Zero-width characters | `​`, `‌`, `﻿` | Unicode stripping |

Use `scripts/noise_recovery.py` for deterministic noise removal:
```bash
python scripts/noise_recovery.py clean --input <raw_text> --output clean.json
```

The script returns detected noise items + clean text. Claude reviews borderline cases (text that might be lyrics or might be noise).

### Step 2: Lyrics Reconstruction

After noise removal, repair broken lyrics:

**Character-level fragmentation** (common in OCR/PDF extraction):
```
君
の
名
は
→ 君の名は
```

**Detection heuristics**:
- Consecutive single-character lines → join
- CJK characters isolated on their own line → join with neighbors
- Lines shorter than 2 characters surrounded by similarly short lines → join

**Structure detection**:
- Identify verse/chorus/bridge patterns
- Detect repeated sections (chorus detection by similarity)
- Preserve intentional line breaks (poetic enjambment)
- Mark detected sections in output JSON

Use `scripts/lyrics_reconstructor.py`:
```bash
python scripts/lyrics_reconstructor.py reconstruct --input clean.json --output reconstructed.json
```

### Step 3: Input Parsing

- Determine if input is single-language or multilingual (multiple rows)
- If multilingual: identify which row is original, romanization, translation
- Detect input format (plain text, markdown, file path)
- Preserve lyric structure (verses, chorus, bridge)
- **Extract target language**: Parse the user's request for the target language (see Target Language Configuration). The target language governs every subsequent step. If not specified, prompt the user before proceeding.
- **Validate target language**: Confirm it is a supported language. If the target language is the same as the source language, prompt the user for a different target.

### Step 4: Language Detection

- Identify writing system from 30+ supported scripts (see Script Detection section)
- Determine specific language from script-specific character features
- Detect directionality (LTR / RTL) automatically — never assume
- For Latin rows: distinguish romanization from actual translation
- Support 100+ languages across all major writing systems
- **Always** output: language code, script name, direction

See `references/script-detection.md`

### Step 5: Auto-Generation

**Target language is now known** (from Step 2). Configure the generation pipeline for this specific target language.

**Always generate (Default Mode)**:
- **Translation**: into the user-specified target language. Natural, human-quality, native expression. Must read as if originally written in the target language. Must satisfy 信达雅 (Faithfulness, Expressiveness, Elegance) as judged by a native speaker of the target language. Never expose literal/machine-translation intermediates.
- **Romanization/Transliteration**: For non-Latin scripts, auto-generate using the **language-specific standard system** (Pinyin for CN, Hepburn for JP, Revised Romanization for KR, DIN 31635 for AR, ISO 15919 for Indic, etc.) Never use a universal romanization system.

**Target-language quality review** (mandatory — always applies):
- After generating translations, perform a quality review pass **in the target language**
- Verify from the perspective of a native speaker of the target language
- Check: naturalness, idiomatic correctness, register appropriateness, cultural resonance
- Verify: mood preserved, imagery intact, metaphor correctly mapped, poetic rhythm natural in the target language
- For lyrics: preserve singability in the target language (syllable count, stress pattern, natural cadence)
- Apply both source-language optimizations AND target-language optimizations (see Target Language Quality Pipeline)
- Reject any output that reads like a translation — it must read like it was originally written in the target language

**Advanced Mode only** (on explicit user request):
- **Cultural notes**: relevant context for idioms, cultural references
- **Etymology**: word origins and historical development
- **Grammar notes**: morphological breakdown, syntax explanation
- **IPA**: phonetic transcription
- **Word-by-word gloss**: Leipzig-style linguistic glossing

Default Mode outputs ONLY: Original + Romanization + Translation. No explanations, no annotations, no commentary.

### Step 6: Semantic Segmentation

Split each row into minimal alignable semantic units using **language-aware tokenization**:

- **Chinese**: word-level (dictionary-based segmentation, not character-level unless independent meaning)
- **Japanese**: morpheme-level (morphological segmentation at word boundaries)
- **Korean**: morpheme-level within eojeol blocks
- **Arabic/Persian/Urdu**: morpheme-level where meaningful (clitic separation), otherwise word-level
- **Turkish/Finnish/Hungarian**: morpheme-level for agglutinative structures
- **European languages**: word-level with phrasal verb and compound noun awareness
- **Indic languages**: word-level with sandhi and compound awareness
- **Thai/Khmer**: word-level (dictionary-based segmentation)
- **Vietnamese**: syllable-level (each syllable is a token)
- Mark segmentation confidence per unit

See `references/tokenization-engine.md`

### Step 6b: Beginner-Friendly Glossing (Simplified Leipzig)

**Purpose**: Make morphological analysis accessible to language learners by breaking complex words into roots and affixes with plain-language UI tags instead of academic linguistic jargon.

This step runs **in Default Mode** for every word. Unlike the full Advanced Mode annotation, this produces a lightweight, beginner-oriented breakdown embedded directly in each word block.

#### Morpheme Types

| Type | Description | Example |
|------|-------------|---------|
| `root` | The core meaning-bearing unit (词根) | 食べ (eat), katab- (write) |
| `prefix` | Morpheme before the root (前缀) | お- (honorific), re- (again) |
| `suffix` | Morpheme after the root (后缀) | -た (PAST), -iendo (GERUND) |
| `particle` | Grammatical function word (助词/小品词) | を (OBJ), が (SUBJ), 이/가 (NOM) |

#### UI Tag Convention: Plain Language Over Jargon

**Never** use academic linguistic abbreviations in UI tags. Always translate to beginner-friendly descriptions:

| ❌ Academic Jargon | ✅ Beginner-Friendly UI Tag |
|-------------------|---------------------------|
| ACC (Accusative) | 宾语标记 / Object Marker |
| NOM (Nominative) | 主语标记 / Subject Marker |
| PST (Past Tense) | 过去时 / Past |
| PROG (Progressive) | 进行时 / Ongoing |
| 1SG (1st Person Singular) | 第一人称单数 / I/Me |
| GEN (Genitive) | 所属格 / Possessive |
| DAT (Dative) | 间接宾语 / To/For |
| PASS (Passive) | 被动语态 / Passive Voice |
| CAUS (Causative) | 使役 / Causative |
| HON (Honorific) | 敬语 / Honorific |
| POL (Polite) | 礼貌体 / Polite Form |
| NEG (Negation) | 否定 / Not |
| PL (Plural) | 复数 / Plural |
| IMP (Imperative) | 命令式 / Command |
| COND (Conditional) | 条件 / If/When |
| POT (Potential) | 可能态 / Can/ Able to |
| VOL (Volitional) | 意向形 / Let's |

**UI tags MUST be provided in both English AND the user's interface language** (default: bilingual English + target language). The exact localization is determined by the target language context:

- If the target language is Chinese → UI tags in Chinese (e.g., "过去时", "主语标记")
- If the target language is Japanese → UI tags in Japanese (e.g., "過去形", "主語マーカー")
- If the target language is Arabic → UI tags in Arabic (e.g., "الماضي", "علامة الفاعل")
- For other target languages → UI tags in English (e.g., "Past Tense", "Subject Marker")

#### Morpheme Output Format

Each word in the JSON output contains a `morphemes` array:

```json
{
  "original": "食べた",
  "romanization": "tabeta",
  "color_hex": "#E74C3C",
  "translation": "ate",
  "morphemes": [
    {
      "text": "食べ",
      "type": "root",
      "ui_tag": null,
      "meaning": "eat"
    },
    {
      "text": "た",
      "type": "suffix",
      "ui_tag": "过去时 / Past",
      "meaning": "action completed"
    }
  ]
}
```

**Rules for morpheme breakdown**:

1. **Roots never get a ui_tag** (`ui_tag: null`) — they carry meaning directly
2. **Affixes and particles always get a ui_tag** — explaining their grammatical function
3. **The `meaning` field is required** for every morpheme — it explains what that piece contributes
4. **The top-level `original` string must remain intact** — never visually break cursive connections, syllabic blocks, or abugida ligatures (see Complex Script Rules)

#### Language-Specific Glossing Examples

**Japanese (Agglutinative)**:
```json
// 食べさせられなかった (tabesaserarenakatta) = "was not made to eat"
"morphemes": [
  {"text": "食べ", "type": "root", "ui_tag": null, "meaning": "eat"},
  {"text": "させ", "type": "suffix", "ui_tag": "使役 / Causative", "meaning": "make/let"},
  {"text": "られ", "type": "suffix", "ui_tag": "被动 / Passive", "meaning": "be acted upon"},
  {"text": "なかった", "type": "suffix", "ui_tag": "否定过去 / Neg.Past", "meaning": "did not"}
]
```

**Spanish (Fusional)**:
```json
// hablábamos = "we were speaking"
"morphemes": [
  {"text": "habl", "type": "root", "ui_tag": null, "meaning": "speak"},
  {"text": "á", "type": "suffix", "ui_tag": "过去未完成时 / Imperfect Past", "meaning": "ongoing in past"},
  {"text": "bamos", "type": "suffix", "ui_tag": "第一人称复数 / 1st Pl.", "meaning": "we"}
]
```

**Turkish (Agglutinative)**:
```json
// evlerimizden = "from our houses"
"morphemes": [
  {"text": "ev", "type": "root", "ui_tag": null, "meaning": "house"},
  {"text": "ler", "type": "suffix", "ui_tag": "复数 / Plural", "meaning": "more than one"},
  {"text": "imiz", "type": "suffix", "ui_tag": "第一人称复数所属 / Our", "meaning": "belonging to us"},
  {"text": "den", "type": "suffix", "ui_tag": "从格 / Ablative", "meaning": "from"}
]
```

**Arabic (Root-Pattern)**:
```json
// يكتب (yaktubu) = "he writes"
"morphemes": [
  {"text": "ك-ت-ب", "type": "root", "ui_tag": null, "meaning": "writing (triliteral root)"},
  {"text": "يَـ", "type": "prefix", "ui_tag": "第三人称阳性 / 3SG.M", "meaning": "he"},
  {"text": "ـُ", "type": "suffix", "ui_tag": "现在时直陈式 / PRES.IND", "meaning": "ongoing action"}
]
```

**Korean (Agglutinative + Syllabic Blocks)**:
```json
// 먹었다 (meogeotda) = "ate"
"morphemes": [
  {"text": "먹", "type": "root", "ui_tag": null, "meaning": "eat"},
  {"text": "었", "type": "suffix", "ui_tag": "过去时 / Past", "meaning": "action completed"},
  {"text": "다", "type": "suffix", "ui_tag": "基本形 / Dictionary Form", "meaning": "statement ending"}
]
```

### Step 7: Cross-Language Alignment

Core alignment rules (apply in priority order):

1. **Semantic Priority**: Always align by meaning, never by character count.
2. **Morpheme Awareness**: Split compound words and agglutinative structures.
3. **Syllable Fallback**: If semantic decomposition is impossible, use syllable boundaries.
4. **One-to-One Priority**: Prefer 1:1 alignment. N:M only when linguistically unavoidable.
5. **Implicit Components**: Mark implied elements with `[implied: ...]`.
6. **Idiomatic Handling**: Non-literal translations annotated as `[idiomatic]`.
7. **Confidence Scoring**: Assign [0-1] per alignment. < 0.9 → flag for review.
8. **Natural Word Order** 🔴: Translation row segments MUST be in natural target-language word order. Never preserve source word order at the expense of naturalness. **This is the #1 cause of translationese.**

   **How it works**: The `segments` array order controls reading order. Each segment's `group_id` links it to the corresponding source word. The same `group_id` (and color) appears in different array positions across original and translation rows — this is CORRECT behavior.

   ```
   Hindi original row segments (SOV order):
     ["अब", "यहाँ", "से", "कहाँ", "जाएँ", "हम"]

   Chinese translation row segments (SVO order):
     ["此刻", "我们", "从", "这里", "去往", "何方"]
     ↑ same group_ids as above, DIFFERENT array order
   ```

   **Verification**: Concatenate the translation segments. If the result doesn't read like natural target-language text, the order is WRONG. Fix the segment order, not the translation text. The color alignment will still work — colors follow `group_id`, not array position.

Full rules: `references/alignment-rules.md`

### Step 7b: Complex Scripts & BiDi Handling (Mandatory)

**CRITICAL**: When the source or target language uses a complex script (Arabic, Persian, Devanagari, Korean Hangul, Thai, etc.), the following hard constraints apply. Violating these rules causes visual corruption, character disconnection, and BiDi layout breakage.

#### Rule 1: Cursive/Connected Scripts (Arabic, Persian, Urdu, Sindhi, Uyghur)

**NEVER break cursive connections in the top-level `original` string.** Arabic script letters connect to form words; breaking these connections produces isolated letter forms that are illegible.

```
✅ CORRECT: "original": "يكتب"     (fully connected word form)
❌ WRONG:    "original": "ي ك ت ب"  (isolated letters — illegible)
```

**Morpheme breakdown**: In the `morphemes` array, provide the unattached, standalone forms of roots and affixes:

```json
// يكتب (yaktubu) = "he writes" — original kept intact
{
  "original": "يكتب",
  "morphemes": [
    {"text": "كتب", "type": "root", "meaning": "write (triliteral root ك-ت-ب)"},
    {"text": "يـ", "type": "prefix", "ui_tag": "第三人称阳性 / 3SG.M", "meaning": "he"},
    {"text": "ـُ", "type": "suffix", "ui_tag": "现在时 / PRES", "meaning": "ongoing action"}
  ]
}
```

**Persian-specific**: Prefixes like می (mi-) are often separated by Zero-Width Non-Joiner (ZWNJ). Detect and treat as independent prefix:
```
نی‌میروم → می‌ + رو + م → "mi-" (prefix, PROG) + "row" (root, go) + "-am" (suffix, 1SG)
```

**Enclitic pronouns** (Arabic/Persian: -am, -at, -hu, -ha): List in morphemes with hyphen prefix, tag as "属格/宾格后缀 / Possessive/Object Suffix".

**Tashkeel/Harakat**: If the original text includes diacritical marks (َ ِ ُ), preserve them in the original string. If absent, romanization must accurately reflect the correct pronunciation.

#### Rule 2: Abugidas (Devanagari, Sanskrit, Hindi, Thai, Bengali, Tamil, etc.)

**Do NOT visually sever matras (vowel signs) from base consonants in the top-level `original`.** In Devanagari, vowel signs (ा, ि, ी, ु, ू, े, ै, ो, ौ) must remain attached to their consonant:

```
✅ CORRECT: "original": "मैं"      (vowel sign ै attached to म)
❌ WRONG:    "original": "म ैं"    (severed vowel sign — corruption)
```

**Morpheme breakdown**: Show the base consonant and the applied grammar rule logically:

```json
// लड़कियाँ (laRkiyā̃) = "girls"
{
  "original": "लड़कियाँ",
  "morphemes": [
    {"text": "लड़की", "type": "root", "meaning": "girl"},
    {"text": "याँ", "type": "suffix", "ui_tag": "阴性复数 / Fem.PL", "meaning": "feminine plural marker"}
  ]
}
```

#### Rule 3: Syllabic Blocks (Korean Hangul)

**Keep syllabic blocks intact in the `original` string.** Hangul characters compose into syllable blocks (e.g., 한, 글). Never split individual jamo (ㅎ, ㅏ, ㄴ) in the display text:

```
✅ CORRECT: "original": "먹었다"   (two syllabic blocks)
❌ WRONG:    "original": "ㅁㅓㄱㅇㅓㅆㄷㅏ"  (jamo-level — illegible)
```

**Morpheme breakdown**: Break into logical dictionary forms (verb stems and endings), NOT individual jamo:

```json
// 먹었다 (meogeotda) = "ate"
{
  "original": "먹었다",
  "morphemes": [
    {"text": "먹", "type": "root", "meaning": "eat (dictionary form: 먹다)"},
    {"text": "었", "type": "suffix", "ui_tag": "过去时 / Past", "meaning": "past tense marker"},
    {"text": "다", "type": "suffix", "ui_tag": "叙述体 / Declarative", "meaning": "statement ending"}
  ]
}
```

#### Rule 4: Punctuation Isolation

**Ensure no leading or trailing punctuation is attached to words in the JSON.** BiDi layout algorithms misplace punctuation when it's attached to mixed-direction text:

```
✅ CORRECT: "text": "سلام"     (no punctuation attached)
❌ WRONG:    "text": "سلام."   (period attached — will misplace in RTL context)
```

Punctuation should be either:
- Omitted from word segments (preferred for lyrics)
- Placed in its own dedicated segment with its own `group_id`

#### Rule 5: BiDi Isolation in Output JSON

Every output JSON MUST include `text_direction` and `script_family` at the top level:

```json
{
  "verse_id": "v_01",
  "text_direction": "rtl",
  "script_family": "arabic",
  ...
}
```

| `script_family` Value | Used For |
|----------------------|----------|
| `"arabic"` | Arabic, Persian, Urdu, Pashto, Kurdish, Uyghur |
| `"hebrew"` | Hebrew, Yiddish |
| `"devanagari"` | Hindi, Marathi, Nepali, Sanskrit |
| `"hangul"` | Korean |
| `"cjk"` | Chinese, Japanese |
| `"thai"` | Thai, Lao |
| `"latin"` | English, Spanish, French, all Latin-script languages |
| `"cyrillic"` | Russian, Ukrainian, Bulgarian, Mongolian |
| `"bengali"` | Bengali, Assamese |
| `"tamil"` | Tamil |
| `"telugu"` | Telugu |
| `"greek"` | Greek |
| `"georgian"` | Georgian |
| `"armenian"` | Armenian |
| `"ethiopic"` | Amharic, Tigrinya |

This enables the frontend to:
1. Load the correct font stack for the script family
2. Set `dir="rtl"` or `dir="ltr"` on the container
3. Apply script-appropriate line-height, sizing, and spacing

### Step 8: Color Mapping

Assign colors to aligned semantic units:

- Same semantic unit → same color across ALL rows (original, romanization, translation)
- Repeated vocabulary → reuse the EXACT same color globally
- New vocabulary → assign next available color from active palette
- Color exhaustion (>30 unique units): enable recycling

Use `scripts/color_engine.py` for persistent color assignment:
```bash
python scripts/color_engine.py assign --data "<aligned_units_json>" --palette default
```

Claude handles semantic grouping; the script enforces deterministic color consistency via SQLite lexicon.

### Step 9: Annotation Generation (Advanced Mode Only)

Only when user explicitly requests advanced features:

- **Grammar notes**: morphological breakdown for inflected forms
- **Cultural context**: relevant background for idioms and references
- **Etymology**: word origin and historical development
- **IPA**: per-word phonetic transcription
- **Vocabulary list**: unique words with frequency

See `references/annotation-layers.md`

### Step 10: Export Rendering

**Pre-Export Validation (MANDATORY — run BEFORE calling output_writer.py):**

Before exporting, validate the annotation JSON against these checks. If ANY check fails, fix the data and re-validate. Do NOT proceed to export with failures.

| # | Check | How to Verify | Severity |
|---|-------|---------------|----------|
| 1 | **Every vocab item has `meaning`** | `all(v.get("meaning") for v in data["vocabulary"])` | 🔴 BLOCKING |
| 2 | **Every row has `direction`** | `all(r.get("direction") in ("ltr","rtl") for r in data["rows"])` | 🔴 BLOCKING |
| 3 | **Every segment has `group_id`** | `all(s.get("group_id") for r in data["rows"] for s in r["segments"])` | 🔴 BLOCKING |
| 4 | **Every segment has `color`** | `all(s.get("color") for r in data["rows"] for s in r["segments"])` | 🔴 BLOCKING |
| 5 | **Same `group_id` → same `color`** across all rows | Group segments by group_id, verify all have identical color | 🟡 WARNING |
| 6 | **No empty-segment text in rows** | `all(s.get("text") for r in data["rows"] for s in r["segments"])` | 🟡 WARNING |

**Check #1 is the most common failure.** The vocabulary `meaning` field is rendered directly in the HTML table's Meaning column. A missing `meaning` produces an empty table cell visible to the user. Always build a complete word→meaning mapping for every unique source word before finalizing the JSON.

**Default output** (always generate both):

```bash
python scripts/output_writer.py render --format html --data "<annotated_json>" --output document.html
python scripts/output_writer.py render --format docx --data "<annotated_json>" --output document.docx
```

**On-demand only** (generate ONLY when user explicitly requests):

```bash
python scripts/output_writer.py render --format markdown --data "<annotated_json>" --output document.md
```

#### Step 10: Export Design

All visual design (layout, typography, spacing, tooltip behavior, interactions,
dark/light mode, responsive breakpoints, RTL layout, font stacks) is implemented
in `assets/templates/lyrics.html` (Apple Music inspired, clean opaque surfaces —
no frosted glass, no blur). The DOCX output uses python-docx with matching
typographic scale.

**Three-Tab Interface** (HTML output):

| Tab | Purpose | Layout |
|-----|---------|--------|
| 📝 **Annotated** | Word-level color-aligned display | Strict vertical: original → romanization → translation per line. Segments are inline colored tokens. Tap/click for dictionary cards. |
| 📖 **Reading** | Clean prose reading experience | Two-column side-by-side: original text (left) + idiomatic translation (right). Line-by-line paired reading. The translation column uses the per-line `free_translation` — a fluent, native-quality rendering matched to the lyrics' emotion (信达雅), never the word-aligned gloss. No segment colors — pure text. |
| 📚 **Vocabulary** | Word learning with flashcards | Responsive card grid. Each card shows: word (colored), pronunciation, meaning, POS badge, frequency stars. Click to expand for lemma, etymology, usage notes. Sort by frequency or alphabetical. Search/filter. |

#### Step 10a: Annotation JSON Data Contract

The JSON passed to `output_writer.py` MUST satisfy these mandatory rules:

1. **Top-level fields**: `verse_id`, `text_direction`, `script_family` — all required
2. **Every original row**: `free_translation` — the fluent, idiomatic, emotion-matched translation of that line, shown in the Reading tab. Must read as if originally authored in the target language by a native speaker (信达雅). It is allowed — and encouraged — to differ from the word-aligned `translation` row: the Reading tab shows the natural rendering, never the gloss.
3. **Every row**: `"direction": "ltr"` or `"rtl"` — never omit
4. **Every segment**: `text`, `color`, `group_id` — all required; `morphemes` array recommended for all non-analytic languages
5. **Every morpheme** (when present): `text`, `type` (root/prefix/suffix/particle), `ui_tag` (null for roots, beginner-friendly description for affixes/particles), `meaning` — all required
6. **Same semantic unit** = same `group_id` across ALL rows (original, romanization, translation)
7. **Translation row segment order**: natural target-language word order, not source order
8. **Every vocabulary item**: `word`, `romanization`, `meaning`, `color`, `frequency` — all required
9. **`meaning` in vocabulary is NOT optional** — rendered directly in the HTML Meaning column

**Full Enhanced Structure** (with morpheme breakdown):

```json
{
  "verse_id": "v_01",
  "text_direction": "rtl",
  "script_family": "arabic",
  "free_translation": "在夜的寂静中，屋子发出了呼喊。",
  "metadata": {
    "source_language": "ar",
    "target_language": "zh",
    "title": "Sample Line",
    "sentiment": "melancholic",
    "structure": {
      "sections": [{"type": "verse", "lines": [1]}]
    }
  },
  "rows": [
    {
      "type": "original",
      "language": "ar",
      "direction": "rtl",
      "free_translation": "他正在写。",
      "segments": [
        {
          "text": "يكتب",
          "color": "#E74C3C",
          "group_id": "L1-W1",
          "morphemes": [
            {"text": "كتب", "type": "root", "ui_tag": null, "meaning": "write (triliteral root ك-ت-ب)"},
            {"text": "يـ", "type": "prefix", "ui_tag": "第三人称阳性 / 3SG.M", "meaning": "he"},
            {"text": "ـُ", "type": "suffix", "ui_tag": "现在时 / PRES", "meaning": "ongoing action"}
          ]
        }
      ]
    },
    {
      "type": "romanization",
      "language": "ar-Latn",
      "direction": "ltr",
      "segments": [
        {
          "text": "yaktubu",
          "color": "#E74C3C",
          "group_id": "L1-W1"
        }
      ]
    },
    {
      "type": "translation",
      "language": "zh",
      "direction": "ltr",
      "segments": [
        {
          "text": "他正在写",
          "color": "#E74C3C",
          "group_id": "L1-W1"
        }
      ]
    }
  ],
  "vocabulary": [
    {
      "word": "يكتب",
      "romanization": "yaktubu",
      "meaning": "他正在写",
      "color": "#E74C3C",
      "frequency": 1,
      "root": "ك-ت-ب",
      "pos": "verb"
    }
  ]
}
```

**Segment field reference**:

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `text` | ✅ | string | Display text for this segment |
| `color` | ✅ | string | Hex color (uppercase, e.g., `#E74C3C`) |
| `group_id` | ✅ | string | Links semantic units across rows |
| `morphemes` | Recommended | array | Morpheme breakdown for non-analytic languages |
| `morphemes[].text` | ✅ (if morphemes present) | string | The morpheme text (standalone form for connected scripts) |
| `morphemes[].type` | ✅ (if morphemes present) | string | One of: `root`, `prefix`, `suffix`, `particle` |
| `morphemes[].ui_tag` | ✅ (if morphemes present) | string or null | Beginner-friendly grammar label; `null` for roots |
| `morphemes[].meaning` | ✅ (if morphemes present) | string | What this morpheme contributes to the word meaning |
| `pronunciation` | Optional | string | Phonetic transcription |
| `pos` | Optional | string | Part of speech (noun, verb, adj, etc.) |
| `lemma` | Optional | string | Dictionary form |
| `meanings` | Optional | array | Multiple translation options |
| `examples` | Optional | array | Usage examples |
| `synonyms` | Optional | array | Related words |
| `etymology` | Optional | string | Word origin |
| `usage_notes` | Optional | string | Register, dialect, context notes |
| `collocations` | Optional | array | Common word combinations |
| `grammar` | Optional | string | Grammatical function description |

### Step 10b: UI Mapping & Frontend Integration

The JSON output is designed for **direct binding to frontend components** — every field maps to a specific UI element. This section describes how the data structure connects to the HTML template (`assets/templates/lyrics.html`).

#### Mitigating Cognitive Overload

Language learners experience **attentional blink** when too much information is visible simultaneously. The UI mapping follows a progressive disclosure strategy:

1. **First glance** → `free_translation` (Reading tab): A clean, flowing, idiomatic sentence — the natural rendering of the line, matched to the lyrics' emotional register. The user immediately grasps the full meaning without any word-by-word gloss or visual noise.

2. **Word-by-word reading** → `words[]` array: Maps to `.word-block` containers. Each word block displays original + romanization + translation inline, color-linked. The user scans naturally without clicking.

3. **On-demand deep dive** → `morphemes[]` array: **Hidden by default.** Only revealed on hover/click. A tooltip/popover renders the morpheme breakdown with `ui_tag` and `meaning`. This prevents beginners from being overwhelmed by grammar details during initial reading.

```
┌─────────────────────────────────────────────┐
│  free_translation: "在夜的寂静中..."        │  ← Always visible
├─────────────────────────────────────────────┤
│  [يكتب]    [رسالة]    [طويلة]               │  ← words[] array
│  yaktubu   risālatan  ṭawīlatan              │     color-aligned
│  他正在写   一封信     长长的                  │
│    ↑ hover to expand                         │
│  ┌─────────────────────┐                    │  ← morphemes[]
│  │ كتب  → root: write  │                    │     on-demand
│  │ يـ   → 3SG.M: he    │                    │     popover
│  │ ـُ   → PRES: ongoing │                    │
│  └─────────────────────┘                    │
└─────────────────────────────────────────────┘
```

#### BiDi Layout Strategy

When `text_direction` is `"rtl"`, the rendering engine MUST:

1. **Set `dir="rtl"`** on the line container (`.line-group`) so word blocks flow right-to-left
2. **Each vertical word block internally** stays in its natural reading order:
   - Original (RTL) — reads right-to-left within the block
   - Romanization (LTR) — reads left-to-right
   - Translation (LTR for most target languages) — reads left-to-right
3. **Use `unicode-bidi: isolate`** on EVERY segment to prevent directionality leakage between adjacent blocks
4. **Flex/Grid adapts automatically**: The line container uses `display: flex` with `flex-direction: row`. When `dir="rtl"`, the browser automatically reverses the visual order — no CSS changes needed. Each `.word-block` maintains its internal vertical stacking.

```
RTL Line Container (dir="rtl"):
┌──────────┐ ┌──────────┐ ┌──────────┐
│  طويلة   │ │  رسالة   │ │  يكتب    │  ← Original (RTL, right-to-left)
│ ṭawīlatan│ │ risālatan│ │ yaktubu  │  ← Romanization (LTR)
│ 长长的    │ │ 一封信    │ │ 他正在写  │  ← Translation (LTR)
└──────────┘ └──────────┘ └──────────┘
  word 3       word 2       word 1
  (rightmost)               (leftmost)
```

#### Hitbox Optimization for Complex Scripts

Devanagari, Korean Hangul, Thai, and other compact scripts have uneven character heights. Tiny or irregular hitboxes cause frustrating mis-taps:

- **Minimum padding**: Each `.word-block` must have `padding: 0.25em 0.4em` minimum
- **Minimum line-height**: `line-height: 2.0` for complex scripts (Arabic, Devanagari, Thai, Hangul)
- **Regular rectangular hitbox**: Never let the clickable area hug character edges — use uniform block dimensions
- **Touch target minimum**: 44×44px on mobile for any interactive word block

#### On-Demand Morpheme Expansion (Interaction Design)

Morphemes are revealed progressively to avoid overwhelming beginners:

1. **Default state**: Only the original word, romanization, and translation are visible
2. **Hover (desktop) / Tap (mobile)**: A popover/tooltip appears above the word block
3. **Popover content**: 
   - Morpheme breakdown in visual tree (root → prefix → suffix → particle)
   - Each morpheme with its `ui_tag` badge and `meaning`
   - Root highlighted differently from affixes
4. **Dismiss**: Click away, tap elsewhere, or press Escape
5. **Visual indicator**: A subtle dotted underline or small "⊕" icon indicates expandable words

The HTML template (`assets/templates/lyrics.html`) implements this with CSS `:hover` and JavaScript click handlers. Words without morphemes (analytic languages or simple words) show no expansion indicator.

### Step 11: Summary

After processing, generate a brief summary. The summary always includes both source and target language details:

```markdown
## Summary
- Source Language: Japanese (CJK, LTR) | Target: Arabic (Arabic script, RTL)
- Writing System: Japanese (Kanji + Kana) | Script: CJK + Hiragana + Katakana
- Romanization: Hepburn | Translation Quality: 信达雅 verified (native Arabic speaker standard)
- Total Semantic Units: 47 | Unique Vocabulary: 32
- Average Alignment Confidence: 94%
- Noise Items Removed: 5 | Structure: Verse-Chorus
```

Another example — Persian → Spanish:

```markdown
## Summary
- Source Language: Persian (Arabic script, RTL) | Target: Spanish (Latin, LTR)
- Writing System: Persian (Arabic script) | Script: Arabic
- Romanization: UniPers | Translation Quality: 信达雅 verified (native Spanish speaker standard)
- Total Semantic Units: 52 | Unique Vocabulary: 38
- Average Alignment Confidence: 92%
- Noise Items Removed: 2 | Structure: Ghazal (couplets)
```

**The summary must always name the target language and confirm that quality was verified from a native speaker's perspective of that target language.**

## Default Mode vs Advanced Mode

### Default Mode (Always)

Output ONLY:
- Original Lyrics
- Romanization / Transliteration
- Translation

No explanations. No grammar notes. No commentary. Just the aligned lyrics.

### Advanced Mode (On Demand Only)

Available on explicit request:
- **Grammar**: morphological breakdown, syntax notes
- **Culture**: cultural context, idiom explanations
- **Etymology**: word origins, historical development
- **Annotations**: alignment confidence flags, ambiguity notes
- **IPA**: phonetic transcription
- **Vocabulary list**: frequency-sorted word index

Activation phrases: "add grammar notes", "explain the culture", "show etymology", "add annotations", "include IPA", "vocabulary list".

## Script Reference

| Script | Purpose | Call When |
|--------|---------|-----------|
| `scripts/noise_recovery.py` | Noise detection and removal | Every task (Step 0) |
| `scripts/lyrics_reconstructor.py` | Repair broken lyrics, detect structure | Every task (Step 1) |
| `scripts/color_engine.py` | Color assignment + persistent lexicon | Every alignment task |
| `scripts/output_writer.py` | Export to HTML + DOCX (default); MD (on-demand) | Every task |
| `scripts/batch_runner.py` | Batch processing manifest | Multiple files |

## Supported Languages (100+)

| Script | Languages | Direction |
|--------|-----------|-----------|
| Arabic | Arabic, Persian, Urdu, Pashto, Kurdish, Uyghur, Sindhi, Balochi | RTL |
| Hebrew | Hebrew, Yiddish, Ladino | RTL |
| Syriac | Assyrian, Chaldean | RTL |
| CJK | Chinese (Simplified/Traditional), Japanese, Korean | LTR |
| Devanagari | Hindi, Marathi, Nepali, Sanskrit, Maithili, Bhojpuri, Konkani | LTR |
| Cypriot | Cyrillic, Russian, Ukrainian, Bulgarian, Serbian, Mongolian, Kazakh, Kyrgyz, Tajik, Belarusian, Macedonian | LTR |
| Latin | English, French, German, Italian, Spanish, Portuguese, Turkish, Vietnamese, Indonesian, Malay, Polish, Czech, Dutch, Swedish, Norwegian, Danish, Finnish, Hungarian, Romanian, Croatian, Slovenian, Slovak, Lithuanian, Latvian, Estonian, Albanian, Icelandic, Catalan, Galician, Basque, Welsh, Irish, Scots Gaelic, Afrikaans, Swahili, Zulu, Xhosa, Yoruba, Igbo, Hausa, Somali, Filipino, Cebuano, Javanese, Sundanese, Malagasy, Haitian Creole, Quechua, Guarani, Maori, Hawaiian, Samoan, Tongan, Fijian | LTR |
| Greek | Greek (modern + ancient) | LTR |
| Georgian | Georgian, Mingrelian | LTR |
| Armenian | Armenian (modern + classical) | LTR |
| Thai | Thai, Lao, Northern Thai | LTR |
| Khmer | Khmer | LTR |
| Burmese | Burmese, Shan, Mon | LTR |
| Bengali | Bengali, Assamese | LTR |
| Tamil | Tamil | LTR |
| Telugu | Telugu | LTR |
| Kannada | Kannada | LTR |
| Malayalam | Malayalam | LTR |
| Gujarati | Gujarati | LTR |
| Punjabi | Punjabi (Gurmukhi + Shahmukhi) | LTR / RTL |
| Odia | Odia | LTR |
| Sinhala | Sinhala | LTR |
| Tibetan | Tibetan, Dzongkha | LTR |
| Mongolian | Mongolian (Cyrillic + Traditional script) | LTR |
| Ethiopic | Amharic, Tigrinya, Ge'ez | LTR |
| Mixed | Documents containing multiple scripts | Per-segment |

Automatic language detection covers all listed languages.

## Coding Standards

- Python scripts use `#!/usr/bin/env python3` shebang
- Scripts handle errors gracefully — return structured error JSON, never crash silently
- Color values stored as hex strings (uppercase, e.g., `#E74C3C`)
- JSON is the interchange format between Claude reasoning and Python scripts
- Unicode normalization: all text NFKC-normalized before processing
- RTL text: explicitly tagged with `"direction": "rtl"` in intermediate JSON — NEVER assumed
- Bidi isolation: mixed-script segments wrapped with `unicode-bidi: isolate`
- Every row in JSON data contract MUST include `"direction"` field
- Every vocabulary item MUST include `"meaning"` field (rendered in HTML vocab table — if missing, the Meaning column is blank)
- Before calling `output_writer.py`, run the Pre-Export Validation checklist (Step 10) — block on any 🔴 failure

## References

### Core Specifications
- `references/script-detection.md` — Writing system identification for 100+ languages with directionality
- `references/romanization-systems.md` — Per-language romanization standards (never universal)
- `references/alignment-rules.md` — Complete alignment rules including N:M mappings
- `references/color-palettes.md` — Palette customization guide
- `references/annotation-layers.md` — IPA, gloss, grammar notes formats
- `references/noise-patterns.md` — Noise detection patterns and recovery strategies
- `references/lyrics-structures.md` — Lyrics structure detection and reconstruction
- `references/rtl-layout-engine.md` — Full RTL layout engine specification
- `references/bidirectional-text.md` — Bidirectional text rendering rules
- `references/tokenization-engine.md` — Language-aware tokenization strategies
- `references/morphological-analysis.md` — Complex morphology support
- `references/poetry-translation.md` — Poetry-aware translation: 信达雅 quality standard
- `references/language-specific-optimization.md` — Per-language optimization rules
- `references/font-system.md` — Script-appropriate font loading and typography

### Dynamic Language Rules (Layer 2 — Context Retrieval)
- `references/language-rules/_general_rules.md` — Fallback rules for any language
- `references/language-rules/ja_rules.md` — Japanese: agglutinative, te-form, particles, keigo
- `references/language-rules/ko_rules.md` — Korean: agglutinative, speech levels, particles
- `references/language-rules/zh_rules.md` — Chinese: analytic, aspect markers, 成语, register
- `references/language-rules/ar_rules.md` — Arabic: root-pattern, cursive, Tashkeel, RTL
- `references/language-rules/fa_rules.md` — Persian: root-pattern, ezafe, ZWNJ, RTL
- `references/language-rules/es_rules.md` — Spanish: fusional, diminutives, reflexive pronouns
- `references/language-rules/fr_rules.md` — French: fusional, elision/liaison, gender
- `references/language-rules/de_rules.md` — German: fusional, separable prefixes, V2 order
- `references/language-rules/ru_rules.md` — Russian: fusional, aspect pairs, 6-case system
- `references/language-rules/tr_rules.md` — Turkish: agglutinative, vowel harmony, evidentiality
- `references/language-rules/hi_rules.md` — Hindi/Urdu: SOV, postpositions, gender
- `references/language-rules/th_rules.md` — Thai: analytic, politeness particles, segmentation
- `references/language-rules/vi_rules.md` — Vietnamese: analytic, classifiers, kinship pronouns

### Assets
- `assets/palettes/` — JSON palette configuration files
- `assets/templates/lyrics.html` — Apple Music inspired HTML template with three-tab interface
