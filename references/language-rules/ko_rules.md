# Korean Language Rules (ko_rules.md)

## Language Profile
- **Language**: Korean (한국어)
- **ISO 639-1**: `ko`
- **Script**: Hangul (syllabic blocks) + occasional Hanja
- **Direction**: LTR
- **Morphological Type**: Agglutinative
- **Word Order**: SOV (Subject-Object-Verb)
- **Script Family**: `hangul`

## Morphology Rules

### Core Task: Separate Content Words from Function Words

Korean morpheme analysis centers on separating:
- **Content words (体词/谓词)**: Nouns, verb/adjective stems
- **Function words (助词/语尾)**: Particles, endings, suffixes

**Example**: 저는 학교에 갔습니다 (jeoneun hakgyoe gasseumnida) = "I went to school"
```
저   (jeo)     → root: "I/me" (humble)
는   (neun)    → particle, ui_tag: "主题标记 (Topic Marker)"
학교 (hakgyo)  → root: "school"
에   (e)       → particle, ui_tag: "方向/位置标记 (Directional/Locative)"
가   (ga)      → root: "go"
ㅆ    (ss)     → suffix, ui_tag: "过去时 (Past Tense)"
습니다 (seumnida) → suffix, ui_tag: "敬语 正式体 (Formal Polite)"
```

### Subject/Topic Particles

| Particle | ui_tag | Function |
|----------|--------|----------|
| 이/가 (i/ga) | 主语标记 (Subject Marker) | Marks grammatical subject |
| 은/는 (eun/neun) | 主题标记 (Topic Marker) | Marks topic/contrast |
| 을/를 (eul/reul) | 宾语标记 (Object Marker) | Marks direct object |

### Case Particles

| Particle | ui_tag | Function |
|----------|--------|----------|
| 에 (e) | 位置/方向 (Location/Direction) | At, to (static location or direction) |
| 에서 (eseo) | 动作位置 (Action Location) | At (where action occurs) |
| 에게/한테 (ege/hante) | 间接宾语 (Dative) | To (a person) |
| 의 (ui) | 所属 (Possessive) | Of / 's |
| (으)로 (euro) | 方向/手段 (Direction/Means) | Toward / by means of |
| 와/과 (wa/gwa) | 并列 (And/With) | And / with |
| 보다 (boda) | 比较 (Comparative) | Than |

### Tense Suffixes

| Suffix | ui_tag | Function |
|--------|--------|----------|
| -았/었- (-at/eot-) | 过去时 (Past Tense) | Past action |
| -겠- (-get-) | 将来/推测 (Future/Presumptive) | Future or conjecture |
| -ㄴ/는- (-n/neun-) | 现在时 定语 (Present Adnominal) | Present (modifier form) |

### Speech Level Suffixes (Honorifics)

**CRITICAL**: Korean has multiple speech levels. The level affects the entire translation tone.

| Level | Suffix | ui_tag | Translation Tone |
|-------|--------|--------|------------------|
| 합쇼체 (Formal Polite) | -습니다/ㅂ니다 | 敬语 正式体 (Formal Polite) | Formal, respectful, distant |
| 해요체 (Informal Polite) | -아요/어요 | 敬语 非正式体 (Informal Polite) | Polite but warm, conversational |
| 해체 (Informal Plain) | -아/어 | 非敬语 随意体 (Casual Intimate) | Casual, intimate, close |
| 해라체 (Formal Plain) | -ㄴ다/는다 | 非敬语 叙述体 (Plain Narrative) | Impersonal, written, declarative |
| 하게체 (Familiar) | -네 | 熟悉体 (Familiar) | Familiar but slightly formal |

### Honorific Infix (-시-)

The honorific infix elevates the subject:

```
가십니다 (gasimnida) → "goes" (honorific subject)
- 가   → root: "go"
- 시   → suffix, ui_tag: "主体敬语 (Subject Honorific)"
- ㅂ니다 → suffix, ui_tag: "敬语 正式体 (Formal Polite)"
```

## Script-Specific Constraints

### Syllabic Blocks — NEVER Split Jamo

Hangul is composed of syllabic blocks (e.g., 한 = ㅎ + ㅏ + ㄴ). The top-level `original` string MUST keep these blocks intact:

```
✅ "original": "먹었다"     (syllabic blocks intact)
❌ "original": "ㅁㅓㄱㅇㅓㅆㄷㅏ"  (jamo-level — illegible)
```

In the `morphemes` array, break into logical dictionary forms (verb stems and endings), NOT individual jamo:

```
먹었다 (meogeotda) → "ate"
- 먹  → root: "eat" (dictionary form: 먹다)
- 었  → suffix, ui_tag: "过去时 (Past)"
- 다  → suffix, ui_tag: "叙述体 (Plain Narrative)"
```

## Translation Quality Checklist

- [ ] Speech level correctly identified and reflected in translation tone
- [ ] Subject/topic/object particles correctly tagged
- [ ] Subject honorific (-시-) recognized and conveyed
- [ ] Tense suffixes correctly identified
- [ ] Syllabic blocks preserved intact in original string
- [ ] Free translation uses appropriate target-language register matching the Korean speech level
- [ ] Implicit subjects correctly inferred (Korean often drops subjects)
