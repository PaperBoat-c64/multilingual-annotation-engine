# Chinese Language Rules (zh_rules.md)

## Language Profile
- **Language**: Chinese (中文)
- **ISO 639-1**: `zh`
- **Script**: CJK — Hanzi (Chinese characters)
- **Direction**: LTR (historically also vertical RTL)
- **Morphological Type**: Analytic (isolating)
- **Word Order**: SVO (Subject-Verb-Object)
- **Script Family**: `cjk`

## Morphology Rules

### No Inflection — Analytical Grammar

Chinese has almost no inflectional morphology. Grammatical relationships are expressed through word order and separate particles. Most words have **empty morphemes arrays** (just the root):

```
我爱你 (wǒ ài nǐ) → "I love you"
- 我 → root: "I/me"     (morphemes: [])
- 爱 → root: "love"     (morphemes: [])
- 你 → root: "you"      (morphemes: [])
```

### Aspect Markers (Separate Particles)

Chinese marks aspect with post-verbal particles. These ARE separate words/segments:

| Marker | ui_tag | Function |
|--------|--------|----------|
| 了 (le) | 完成体 (Perfective) | Completed action |
| 过 (guò) | 经历体 (Experiential) | Past experience |
| 着 (zhe) | 持续体 (Durative) | Ongoing action/state |
| 在 (zài) | 进行体 (Progressive) | Action in progress |

```
我吃了 (wǒ chī le) → "I ate"
- 我 → root: "I/me"
- 吃 → root: "eat"
- 了 → particle, ui_tag: "完成体 (Perfective)"
```

### Structural Particles

| Particle | ui_tag | Function |
|----------|--------|----------|
| 的 (de) | 定语标记 (Attributive) | Possession / modification |
| 地 (de) | 状语标记 (Adverbial) | Adverbial modification |
| 得 (de) | 补语标记 (Complement) | Degree / result complement |
| 把 (bǎ) | 处置式 (Disposal) | Object preposing for affectedness |
| 被 (bèi) | 被动标记 (Passive) | Passive voice |
| 吗 (ma) | 疑问标记 (Question) | Yes/no question |
| 呢 (ne) | 语气助词 (Modal Particle) | Continuation / follow-up |
| 吧 (ba) | 建议助词 (Suggestion) | Suggestion / softening |

### Measure Words (量词)

Measure words are required between numerals/demonstratives and nouns. Tag them:

```
一本书 (yī běn shū) → "one book"
- 一   → root: "one"
- 本   → particle, ui_tag: "量词 (Measure Word for books)"
- 书   → root: "book"
```

## Sentiment & Context Rules

### Register: 口语 vs 书面语

**口语 (Spoken/Colloquial Register)**:
- Shorter sentences, more particles (啊, 吧, 呢, 嘛)
- More subject omission
- **Translation tone**: Conversational, direct, intimate

**书面语 (Written/Literary Register)**:
- More four-character idioms (成语), classical expressions
- Fuller syntax, less particle use
- **Translation tone**: Elevated, literary, formal

### 成语 (Four-Character Idioms)

When a 成语 appears, treat it as a single semantic unit (no internal segmentation):

```
一见钟情 (yī jiàn zhōng qíng) → "love at first sight"
- Treat as single unit: group_id covers all four characters
- Annotation: [idiomatic] Classical idiom. Literal: "one look, deep feeling"
```

### Simplified vs Traditional Detection

- Detect script variant: `zh-Hans` (Simplified) or `zh-Hant` (Traditional)
- Set in `metadata.language` accordingly
- Romanization: same Pinyin system for both

## Romanization

- **Standard**: Hanyu Pinyin (with tone marks)
- Tone marks: ̄ (1st), ˊ (2nd), ˇ (3rd), ˋ (4th), no mark (neutral)
- Word segmentation: Pinyin words separated by spaces
- Proper names: capitalize first letter

## Translation Quality Checklist

- [ ] Word-level segmentation correct (dictionary-based, not character-level)
- [ ] Aspect markers (了/过/着/在) correctly tagged
- [ ] Structural particles (的/地/得) correctly tagged
- [ ] 成语 treated as single unit with idiomatic annotation
- [ ] Register (口语/书面语) detected and matching in translation
- [ ] Simplified/Traditional variant correctly identified
- [ ] Measure words tagged
- [ ] Subject omission handled correctly in translation
