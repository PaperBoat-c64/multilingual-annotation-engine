# Russian Language Rules (ru_rules.md)

## Language Profile
- **Language**: Russian (Русский)
- **ISO 639-1**: `ru`
- **Script**: Cyrillic
- **Direction**: LTR
- **Morphological Type**: Fusional
- **Word Order**: SVO (highly flexible, pragmatically driven)
- **Script Family**: `cyrillic`

## Morphology Rules

### Verb Aspect Pairs

Every Russian verb exists in an aspect pair. This is FUNDAMENTAL — mistranslating aspect changes the core meaning:

| Imperfective (IPFV) | Perfective (PFV) | Meaning |
|---------------------|-------------------|---------|
| писать (pisat') | написать (napisat') | to write |
| читать (chitat') | прочитать (prochitat') | to read |
| говорить (govorit') | сказать (skazat') | to speak/say (suppletive) |
| делать (delat') | сделать (sdelat') | to do |

**Aspect in morpheme breakdown**:

```
написал (napisal) → "he wrote (completely)"
- на  → prefix, ui_tag: "完成体 (Perfective)"
- пис → root: "write"
- а   → suffix, ui_tag: "主题元音 (Theme Vowel)"
- л   → suffix, ui_tag: "过去时 (Past Tense)"
- ∅   → 零词尾: 阳性单数 (M.SG)
```

### 6-Case System

Every noun/adjective carries case. Tag it:

| Case | Key Question | ui_tag |
|------|-------------|--------|
| Nominative | кто? что? | 主格 (Nominative) |
| Accusative | кого? что? | 宾格 (Accusative) |
| Genitive | кого? чего? | 属格 (Genitive) |
| Dative | кому? чему? | 与格 (Dative) |
| Instrumental | кем? чем? | 工具格 (Instrumental) |
| Prepositional | о ком? о чём? | 前置格 (Prepositional) |

### Gender and Number

Three genders + plural:

```
красивый / красивая / красивое / красивые
→ beautiful (M / F / N / PL)
- красив → root: "beautiful"
- ый    → suffix, ui_tag: "阳性单数 主格 (M.SG.NOM)"
- ая    → suffix, ui_tag: "阴性单数 主格 (F.SG.NOM)"
- ое    → suffix, ui_tag: "中性单数 主格 (N.SG.NOM)"
- ые    → suffix, ui_tag: "复数 主格 (PL.NOM)"
```

### Verbs of Motion

Russian has a complex system of motion verbs (unidirectional vs multidirectional). Tag the direction type:

- идти (idti) / ходить (khodit') — go (on foot)
- ехать (yekhat') / ездить (yezdit') — go (by vehicle)

## Sentiment & Context Rules

### Poetic Inversion

Russian word order is highly flexible in poetry. When word order is pragmatically marked:
- **Fronted elements**: Carry emphasis or contrast
- **Final elements**: Carry new information or focus
- **Translation**: Use target-language devices (cleft sentences, stress, topicalization) to convey the same emphasis

### Diminutives

Russian has rich diminutive morphology conveying affection, smallness, or intimacy:

| Suffix | ui_tag | Emotion |
|--------|--------|---------|
| -очк/-ечк (-ochk/-echk) | 小称/昵称 (Diminutive/Affectionate) | Affection, tenderness |
| -еньк/-оньк (-en'k/-on'k) | 小称/爱称 (Diminutive/Endearing) | Endearment |
| -ик/-чик (-ik/-chik) | 小称 (Diminutive) | Smallness |
| -ушк/-юшк (-ushk/-yushk) | 爱称 (Endearing) | Deep affection |

## Romanization

- **Standard**: ISO 9 (scientific) or BGN/PCGN (practical)
- ISO 9: щ = ŝ, ч = č, ш = š, ж = ž, ю = û, я = â
- BGN/PCGN: щ = shch, ч = ch, ш = sh, ж = zh, ю = yu, я = ya

## Translation Quality Checklist

- [ ] Aspect (IPFV/PFV) correctly identified and conveyed
- [ ] Case correctly tagged on nouns and adjectives
- [ ] Gender and number agreement correct in translation
- [ ] Poetic word order restructured naturally in target language
- [ ] Diminutive emotion preserved in free translation
- [ ] Verbs of motion directionality conveyed
- [ ] Reflexive (-ся/-сь) verbs correctly analyzed
