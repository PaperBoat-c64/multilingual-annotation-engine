# Japanese Language Rules (ja_rules.md)

## Language Profile
- **Language**: Japanese (日本語)
- **ISO 639-1**: `ja`
- **Script**: CJK (Kanji) + Hiragana + Katakana
- **Direction**: LTR (vertical LTR also possible but not used in this system)
- **Morphological Type**: Agglutinative
- **Word Order**: SOV (Subject-Object-Verb)
- **Script Family**: `cjk`

## Morphology Rules

### Verb Decomposition

Japanese verbs agglutinate — multiple suffixes attach to a verb stem in fixed order. Decompose strictly:

```
Stem + Voice + Aspect + Polarity + Tense + Mood + Sentence-Final
```

**Example**: 食べさせられなかった (tabesaserarenakatta) = "was not made to eat"
```
食べ     (tabe)     → root: "eat"
させ     (sase)     → suffix: CAUS (使役) "make/let"
られ     (rare)     → suffix: PASS (被动) "be acted upon"
なかっ   (nakatta)  → suffix: NEG.PAST (否定过去) "did not"
```

### Te-Form (て形) Handling

When encountering te-form, the ui_tag MUST be labeled as "连接/状态 (Connective/State)":

```
食べて (tabete) → "eating / eat (connective)"
- 食べ → root: "eat"
- て  → suffix, ui_tag: "连接/状态 (Connective/State)"
```

### Desire Form (〜たい)

When encountering -tai, ui_tag MUST be labeled as "愿望/想 (Desire/Want)":

```
食べたい (tabetai) → "want to eat"
- 食べ → root: "eat"
- たい → suffix, ui_tag: "愿望/想 (Desire/Want)"
```

### Sentence-Final Particles (終助詞)

Sentence-final particles carry emotional nuance. Identify and tag them:

| Particle | ui_tag | Meaning |
|----------|--------|---------|
| ね (ne) | 确认/寻求同意 (Confirmation) | "isn't it? / right?" |
| よ (yo) | 强调/告知 (Emphasis) | "I'm telling you!" |
| わ (wa) | 感叹/柔和断言 (Soft Assertion) | "you know" (feminine) |
| かな (kana) | 疑问/不确定 (Uncertainty) | "I wonder" |
| ぞ (zo) | 强调/警告 (Strong Emphasis) | "I'm warning you!" (masculine) |
| さ (sa) | 轻松断言 (Casual Assertion) | "you know" (casual) |
| な (na) | 感叹/禁止 (Exclamation/Prohibition) | "don't!" or "how...!" |

### Copula Decomposition

```
です (desu) → polite copula
- です → particle, ui_tag: "敬体/礼貌体 (Polite Copula)"

だ (da) → plain copula
- だ → particle, ui_tag: "简体/普通体 (Plain Copula)"
```

## Sentiment & Context Rules

### Register Detection (敬体 vs 简体)

**Plain Form (简体 — Dictionary/Short Form)**:
- Verbs ending in -u, -ru, -ku, -gu, -su, -tsu, -nu, -bu, -mu
- Adjectives ending in -i (い)
- Copula: だ (da)
- **Translation tone**: Internal monologue, casual, intimate, close relationship
- **Free translation style**: Use casual register matching the target language

**Polite Form (敬体 — Desu/Masu Form)**:
- Verbs ending in -masu (ます)
- Copula: です (desu)
- **Translation tone**: Restrained, confessional, distance, respect
- **Free translation style**: Use polite/formal register matching the target language

### Implicit Subjects

Japanese frequently omits subjects. When a subject is grammatically absent but semantically present, annotate:

```
行く (iku) → "go"
- [implied: subject] — could be "I", "you", "he/she", "we", "they"
- Free translation: infer from surrounding context
```

### Honorific Prefixes (お/ご)

```
お名前 (onamae) → "name" (honorific)
- お → prefix, ui_tag: "敬语/美化语 (Honorific/Polite Prefix)"
- 名前 → root: "name"
```

## Romanization

- **Standard**: Hepburn (modified)
- ん before vowels → n' (e.g., 恋愛 → ren'ai)
- Long vowels: ō (おう), ū (うう), ā (ああ), ē (えい/ええ)
- Geminate consonants: っ → doubled consonant (e.g., がっこう → gakkō)

## Translation Quality Checklist

- [ ] Keigo (敬語) level appropriate for lyrics context
- [ ] Natural particle usage in romanization row
- [ ] Kanji/kana balance considered in original row
- [ ] Implicit subjects correctly inferred
- [ ] Sentence-final particles' emotional weight preserved in free translation
- [ ] Plain/polite register distinction reflected in translation tone
- [ ] Te-form connections properly rendered in target language
