# General Language Rules (_general_rules.md)

## Purpose

This is the **fallback rule document** used when no language-specific rule file exists for the detected language. It provides sensible defaults that work across all human languages.

## Language Profile (To Be Filled by Router)

- **Language**: [Detected by Router]
- **ISO 639-1**: [Router output]
- **Script**: [Detected via Unicode block analysis]
- **Direction**: [Detected via script properties]
- **Morphological Type**: [To be determined by Generator]
- **Script Family**: [Detected]

## General Morphology Rules

### Determine Morphological Type

Based on the language, classify and apply the corresponding decomposition strategy:

| Type | Strategy | Key Languages |
|------|----------|---------------|
| **Agglutinative** | Decompose stem + affix chain. Each suffix is one morpheme. | Turkish, Finnish, Hungarian, Japanese, Korean, Tamil, Kazakh, Swahili |
| **Fusional** | Identify stem + inflection (one suffix may encode multiple features). | Russian, German, Sanskrit, Greek, Latin, Arabic (verb), Spanish, French, Italian |
| **Root-Pattern** | Identify triliteral root + pattern template. | Arabic, Hebrew, Amharic |
| **Analytic** | Each word is its own morpheme. No decomposition needed. | Chinese, Vietnamese, Thai, Khmer, English (mostly) |
| **Polysynthetic** | Long complex words with many morphemes. Decompose fully. | Inuktitut, Yupik, Mohawk, Navajo |

### Morpheme Tagging Conventions

When decomposing, always use these types:

| Type | Description | ui_tag Requirement |
|------|-------------|-------------------|
| `root` | Core meaning-bearing unit | `null` (no tag — roots carry meaning directly) |
| `prefix` | Morpheme before the root | Beginner-friendly grammar tag required |
| `suffix` | Morpheme after the root | Beginner-friendly grammar tag required |
| `particle` | Standalone grammatical function word | Beginner-friendly grammar tag required |

### Universal Grammar Tags

Use these beginner-friendly tags as the default set. Localize to target language as needed:

| Function | Default ui_tag (English) |
|----------|------------------------|
| Plural marking | Plural |
| Past tense | Past Tense |
| Present tense | Present Tense |
| Future tense | Future Tense |
| Progressive aspect | Ongoing (Progressive) |
| Perfective aspect | Completed (Perfective) |
| Negation | Not (Negation) |
| Question marker | Question |
| Subject marker | Subject Marker |
| Object marker | Object Marker |
| Possessive marker | Possessive Marker |
| Locative (in/at) | Location (In/At) |
| Directional (to/toward) | Direction (To/Toward) |
| Ablative (from) | Source (From) |
| Instrumental (using/with) | Means (Using/With) |
| Causative | Causing (Causative) |
| Passive voice | Passive Voice |
| Honorific | Honorific/Respect |
| Polite form | Polite Form |
| Diminutive | Diminutive (Small/Affectionate) |
| Imperative | Command (Imperative) |
| Conditional | If/When (Conditional) |
| Conjunction | And/With (Conjunction) |

## General Script Constraints

### Cursive Scripts (Arabic family)

If the script is cursive (Arabic, Syriac, Mongolian):
- **NEVER** break letter connections in the `original` string
- In `morphemes[]`, use standalone/unattached forms for clarity
- Set `text_direction` to `"rtl"` for Arabic and Hebrew scripts

### Abugidas (Devanagari, Thai, Bengali, Tamil, etc.)

If the script is an abugida:
- **NEVER** sever vowel signs (matras) from base consonants in `original`
- Logically decompose in `morphemes[]` without visual splitting
- Ensure adequate line-height for stacked diacritics

### Syllabic Blocks (Hangul)

If the script is Hangul:
- **NEVER** split syllabic blocks into individual jamo in `original`
- Decompose into dictionary forms (stems + endings) in `morphemes[]`

### Tone Marks (Chinese, Thai, Vietnamese, Yoruba)

If the language is tonal:
- Preserve all tone marks in the `original` string
- Include tone information in romanization

## General Sentiment Rules

### Emotional Tone Mapping

The Router's sentiment output guides translation tone:

| Router Sentiment | Translation Tone |
|-----------------|-----------------|
| `melancholic` | Somber, reflective, understated emotion |
| `energetic` | Dynamic, punchy, rhythmic, active |
| `romantic` | Warm, tender, emotionally expressive |
| `aggressive` | Intense, direct, sharp, confrontational |
| `tender` | Soft, gentle, intimate, careful |
| `defiant` | Bold, resolute, unapologetic, strong |
| `nostalgic` | Wistful, warm, reminiscent, bittersweet |
| `joyful` | Bright, exuberant, celebratory |

### Register Detection (Universal)

Look for register markers common across languages:
- **Formal**: Honorifics, polite particles, full grammar, no contractions
- **Casual**: Contractions, slang, sentence fragments, informal particles
- **Poetic**: Archaic forms, literary vocabulary, figurative language, meter
- **Vulgar**: Coarse vocabulary, slang, taboo words

## General Translation Checklist

- [ ] Language correctly identified via Router
- [ ] Writing system and direction correctly detected
- [ ] Morphological type correctly classified
- [ ] Morphemes decomposed according to morphological type
- [ ] UI tags are beginner-friendly (no academic jargon)
- [ ] Script constraints followed (cursive, abugida, syllabic, tonal)
- [ ] Word order restructured to natural target-language order
- [ ] Emotional sentiment preserved in translation
- [ ] Register appropriately matched
- [ ] 信达雅 (Faithfulness, Expressiveness, Elegance) verified
