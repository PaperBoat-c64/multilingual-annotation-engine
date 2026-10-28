# French Language Rules (fr_rules.md)

## Language Profile
- **Language**: French (Français)
- **ISO 639-1**: `fr`
- **Script**: Latin
- **Direction**: LTR
- **Morphological Type**: Fusional
- **Word Order**: SVO (with flexibility)
- **Script Family**: `latin`

## Morphology Rules

### Verb Conjugation

French verbs conjugate for person, number, tense, mood. Decompose into stem + suffix:

```
parlions → "we were speaking"
- parl → root: "speak"
- ions → suffix, ui_tag: "第一人称复数 过去未完成时 (1PL.IMPF)"
```

### Elision and Liaison

French elides vowels and links consonants. These MUST be reflected:
- In `original`: keep the contracted form (j'aime, l'amour)
- In `romanization`: show the full pronunciation
- Do NOT split elided articles/prepositions into separate words — keep as one segment

### Gender Marking

All nouns have gender (masculine/feminine). Adjectives agree:

```
beau / belle → "beautiful (m/f)"
- beau → root: "beautiful", MASC
- belle → root: "beautiful", FEM
```

### Pronominal Verbs

Reflexive/reciprocal pronouns (me, te, se, nous, vous) are separate particles:

```
je me lave → "I wash myself"
- je  → root: "I"
- me  → particle, ui_tag: "反身代词 第一人称 (Reflexive 1SG)"
- lav → root: "wash"
- e   → suffix, ui_tag: "第一人称单数 现在时 (1SG.PRES)"
```

## Sentiment & Context Rules

### Register: Tu vs Vous

The tu/vous distinction carries social meaning. Reflect in translation tone:
- **Tu**: intimate, casual, close, or condescending
- **Vous**: formal, respectful, distant, or plural
- Free translation: use target-language equivalents (e.g., in Japanese: あなた vs 貴方; in Chinese: 你 vs 您)

### Negation (ne...pas)

French negation wraps around the verb. Treat as two linked particles:

```
je ne sais pas → "I don't know"
- ne  → particle, ui_tag: "否定标记1 (Negation Part 1)"
- sais → root: "know"
- pas → particle, ui_tag: "否定标记2 (Negation Part 2)"
```

## Romanization

- French is already Latin script — romanization row is typically omitted or used for IPA
- If romanization is requested: use IPA phonetic transcription
- Nasal vowels: ɛ̃ (in), ɑ̃ (an), ɔ̃ (on), œ̃ (un)

## Translation Quality Checklist

- [ ] Elision preserved in original string
- [ ] Gender agreement correct in translation
- [ ] Tu/vous register distinction conveyed
- [ ] Pronominal verbs correctly analyzed
- [ ] Negation structure (ne...pas) mapped
- [ ] Natural elision/liaison flow in romanization
- [ ] Past participle agreement handled
