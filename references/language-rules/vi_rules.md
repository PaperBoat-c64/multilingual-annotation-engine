# Vietnamese Language Rules (vi_rules.md)

## Language Profile
- **Language**: Vietnamese (Tiếng Việt)
- **ISO 639-1**: `vi`
- **Script**: Latin (Chữ Quốc Ngữ)
- **Direction**: LTR
- **Morphological Type**: Analytic (isolating)
- **Word Order**: SVO (Subject-Verb-Object)
- **Script Family**: `latin`

## Morphology Rules

### Syllable-Level Tokenization

Vietnamese is analytic — each syllable is written as a separate word (separated by spaces). Tokenize at the syllable level:

```
Tôi yêu bạn → "I love you"
- Tôi → root: "I/me"
- yêu → root: "love"
- bạn → root: "you (friend)"
```

### Compound Words

Many Vietnamese words are disyllabic compounds. When two syllables form one semantic unit, group them:

```
máy bay → "airplane" (literally: machine-fly)
- Group as single semantic unit: máy bay
- Do NOT separate into "machine" + "fly"
```

### Classifiers (Loại Từ)

Vietnamese requires classifiers with nouns. Tag them:

| Classifier | Usage | ui_tag |
|-----------|-------|--------|
| cái | General objects | 量词 通用 (Classifier — General) |
| con | Animals | 量词 动物 (Classifier — Animals) |
| người | People | 量词 人 (Classifier — People) |
| quyển/cuốn | Books | 量词 书本 (Classifier — Books) |
| cây | Stick-like objects | 量词 条状物 (Classifier — Stick-like) |

### Tense/Aspect Markers

Vietnamese uses pre-verbal markers for tense/aspect (separate particles):

| Marker | ui_tag | Function |
|--------|--------|----------|
| đã | 完成/过去 (Completed/Past) | Past/completed action |
| đang | 进行 (Ongoing) | Action in progress |
| sẽ | 将来 (Future) | Future action |
| rồi | 已经 (Already) | Already completed |
| chưa | 尚未 (Not Yet) | Not yet |

```
Tôi đã ăn → "I ate"
- Tôi → root: "I"
- đã  → particle, ui_tag: "完成/过去 (Completed/Past)"
- ăn  → root: "eat"
```

## Sentiment & Context Rules

### Kinship-Based Pronouns

**CRITICAL**: Vietnamese uses kinship terms as personal pronouns. The choice reflects age, gender, social status, and intimacy:

| Pronoun | Literal Meaning | Usage | Social Meaning |
|---------|----------------|-------|----------------|
| anh | Older brother | Male peer/slightly older man | Respect, brotherly |
| chị | Older sister | Female peer/slightly older woman | Respect, sisterly |
| em | Younger sibling | Younger person | Affection, closeness |
| ông | Grandfather | Older man | High respect |
| bà | Grandmother | Older woman | High respect |
| chú | Uncle (younger) | Middle-aged man | Familiar respect |
| cô | Aunt | Middle-aged woman | Familiar respect |
| bạn | Friend | Same-age peer | Equal, friendly |
| tôi | I (formal) | Self-reference | Neutral/formal |
| mình | Body/self | Self-reference (intimate) | Intimate, close |
| tao | I (superior) | Self-reference (to inferior) | Superior, rough |

**Translation**: Map kinship pronouns to target-language social deixis (e.g., Japanese keigo, Chinese 您/你, French tu/vous).

### Tone Sensitivity

Vietnamese has 6 tones, marked by diacritics. Tones affect meaning:
- ngang (mid): không dấu
- huyền (low falling): dấu huyền (à)
- sắc (high rising): dấu sắc (á)
- nặng (low glottal): dấu nặng (ạ)
- hỏi (mid falling-rising): dấu hỏi (ả)
- ngã (high broken rising): dấu ngã (ã)

Tone marks MUST be preserved in the original string. In romanization, they remain part of the word.

## Romanization

- Vietnamese already uses Latin script — romanization row is typically omitted
- If IPA is requested: use IPA phonetic transcription for tones

## Translation Quality Checklist

- [ ] Syllable-level tokenization correct
- [ ] Compound words grouped as single semantic units
- [ ] Classifiers tagged correctly
- [ ] Tense/aspect markers (đã/đang/sẽ) tagged
- [ ] Kinship pronoun social meaning correctly conveyed in translation
- [ ] Tone marks preserved in original string
- [ ] Appropriate target-language social deixis matching Vietnamese kinship terms
