# Spanish Language Rules (es_rules.md)

## Language Profile
- **Language**: Spanish (Español)
- **ISO 639-1**: `es`
- **Script**: Latin
- **Direction**: LTR
- **Morphological Type**: Fusional
- **Word Order**: SVO (flexible, with topicalization)
- **Script Family**: `latin`

## Morphology Rules

### Verb Conjugation

Spanish verbs are highly fusional — a single suffix encodes person, number, tense, aspect, and mood simultaneously. Each suffix MUST be tagged with ALL the information it encodes:

**Example**: hablábamos = "we were speaking"
```
habl   → root: "speak"
á      → suffix, ui_tag: "过去未完成时 (Imperfect Past)"
bamos  → suffix, ui_tag: "第一人称复数 (1st Person Plural)"
```

**Full conjugation info in ui_tag**: Always include person + number + tense/mood:

| Suffix Example | ui_tag |
|---------------|--------|
| -o (hablo) | 第一人称单数 现在时 (1SG.PRES) |
| -as (hablas) | 第二人称单数 现在时 (2SG.PRES) |
| -a (habla) | 第三人称单数 现在时 (3SG.PRES) |
| -amos (hablamos) | 第一人称复数 现在时 (1PL.PRES) |
| -é (hablé) | 第一人称单数 过去时 (1SG.PRET) |
| -ía (hablaba) | 第一/三人称单数 过去未完成时 (1/3SG.IMPF) |
| -ré (hablaré) | 第一人称单数 将来时 (1SG.FUT) |
| -ría (hablaría) | 第一/三人称单数 条件式 (1/3SG.COND) |
| -e (hable) | 第一/三人称单数 虚拟式现在时 (1/3SG.PRES.SUBJ) |

### Reflexive Pronouns

Reflexive pronouns (se, te, me, nos, os) MUST be treated as independent particles. Tag them with their reflexive nature:

```
me lavo → "I wash myself"
- me  → particle, ui_tag: "反身代词 第一人称 (Reflexive 1SG)"
- lav → root: "wash"
- o   → suffix, ui_tag: "第一人称单数 现在时 (1SG.PRES)"
```

### Gender Marking

Nouns and adjectives carry gender:

```
hermoso / hermosa → "beautiful (masc/fem)"
- hermos → root: "beautiful"
- o      → suffix, ui_tag: "阳性单数 (Masculine Singular)"
- a      → suffix, ui_tag: "阴性单数 (Feminine Singular)"
```

## Sentiment & Context Rules

### Diminutive Suffixes (-ito, -ita, -illo, -illa)

**CRITICAL**: Diminutives carry strong emotional weight. When encountered, the free translation MUST reflect tenderness, smallness, affection, or vulnerability:

```
poquito → "a tiny little bit" (NOT just "a little")
- poqu → root: "little"
- ito  → suffix, ui_tag: "小称/昵称 (Diminutive/Affectionate)"
```

| Diminutive | Effect on Translation |
|-----------|----------------------|
| -ito/-ita | Add tenderness, smallness, affection |
| -illo/-illa | Add casualness, slightness |
| -cito/-cita | Add extra tenderness (extended form) |

### Ser vs Estar Distinction

When translating, preserve the ser/estar distinction:
- **Ser** → permanent, essential qualities → translate with permanent-state verbs in target language
- **Estar** → temporary, conditional states → translate with temporary/conditional verbs in target language

### Subjunctive Mood

Subjunctive signals uncertainty, desire, emotion, doubt. In free translation, use target-language equivalents:
- Present subjunctive → signal uncertainty/wish
- Imperfect subjunctive → signal hypothetical/counterfactual
- Past subjunctive → signal past uncertainty/hypotheticals

## Translation Quality Checklist

- [ ] Verb conjugation correctly identified (person + number + tense + mood)
- [ ] Reflexive pronouns treated as independent particles
- [ ] Diminutive emotion preserved in free translation
- [ ] Gender agreement correct in translation (if target language has gender)
- [ ] Ser/estar distinction conveyed
- [ ] Subjunctive mood nuance preserved
- [ ] Natural SVO with appropriate topicalization
