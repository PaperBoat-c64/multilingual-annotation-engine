# Turkish Language Rules (tr_rules.md)

## Language Profile
- **Language**: Turkish (Türkçe)
- **ISO 639-1**: `tr`
- **Script**: Latin
- **Direction**: LTR
- **Morphological Type**: Agglutinative (highly regular)
- **Word Order**: SOV (Subject-Object-Verb)
- **Script Family**: `latin`

## Morphology Rules

### Suffix Chain Decomposition

Turkish words can have extremely long suffix chains. Each suffix carries exactly one meaning. Decompose the full chain:

**Example**: evlerimizdekilerden = "from those who are in our houses"
```
ev      → root: "house"
ler     → suffix, ui_tag: "复数 (Plural)"
imiz    → suffix, ui_tag: "第一人称复数所属 (1PL.POSS)" — "our"
de      → suffix, ui_tag: "位置格 (Locative)" — "in"
ki      → suffix, ui_tag: "关系词 (Relativizer)" — "that which is"
ler     → suffix, ui_tag: "复数 (Plural)" — "those"
den     → suffix, ui_tag: "从格 (Ablative)" — "from"
```

### Vowel Harmony

Turkish suffixes alternate based on the last vowel of the stem. The system has two harmony dimensions:

**2-fold harmony (e/a)**:
- -ler/-lar (plural): ev**ler** (houses) vs kapı**lar** (doors)

**4-fold harmony (i/ı/ü/u)**:
- -di/-dı/-dü/-du (past): gel**di** (came) vs al**dı** (took) vs gör**dü** (saw) vs ol**du** (happened)

**Always check harmony when identifying suffixes.** The suffix form changes but the grammatical function is identical.

### Case Suffixes

| Suffix (harmonized) | ui_tag |
|---------------------|--------|
| -(y)i/-(y)ı/-(y)ü/-(y)u | 宾格 (Accusative) |
| -(y)e/-(y)a | 与格 (Dative) |
| -de/-da | 位置格 (Locative) |
| -den/-dan | 从格 (Ablative) |
| -(n)in/-(n)ın/-(n)ün/-(n)un | 属格 (Genitive) |

### Possessive Suffixes

| Suffix | ui_tag | Person |
|--------|--------|--------|
| -(i)m/-(ı)m/-(ü)m/-(u)m | 第一人称单数所属 (1SG.POSS) | my |
| -(i)n/-(ı)n/-(ü)n/-(u)n | 第二人称单数所属 (2SG.POSS) | your |
| -(s)i/-(s)ı/-(s)ü/-(s)u | 第三人称所属 (3SG.POSS) | his/her/its |
| -(i)miz/-(ı)mız | 第一人称复数所属 (1PL.POSS) | our |
| -(i)niz/-(ı)nız | 第二人称复数所属 (2PL.POSS) | your (pl) |
| -leri/-ları | 第三人称复数所属 (3PL.POSS) | their |

### Tense/Aspect Suffixes

| Suffix | ui_tag |
|--------|--------|
| -iyor/-ıyor/-üyor/-uyor | 现在进行时 (Present Progressive) |
| -di/-dı/-dü/-du | 确定过去时 (Definite Past) |
| -miş/-mış/-müş/-muş | 转述过去时 (Evidential/Reported Past) |
| -ecek/-acak | 将来时 (Future) |
| -ir/-ır/-ür/-ur | 广义时 (Aorist/General) |

### Evidentiality Marker (-miş)

**CRITICAL**: The -miş suffix encodes evidentiality — the speaker did NOT personally witness the event. This is a key feature of Turkish:

```
gelmiş → "apparently came / reportedly came / I hear that...came"
- gel  → root: "come"
- miş  → suffix, ui_tag: "转述过去时/间接证据 (Evidential/Reported)"
```

In free translation, use target-language devices to convey indirect evidence:
- English: "reportedly", "apparently", "I hear that..."
- Chinese: "据说", "听说"
- Japanese: "〜そうだ", "〜らしい"

## Sentiment & Context Rules

### SOV → SVO Reordering

Turkish is SOV. When translating to SVO languages (English, Chinese, Spanish), restructure naturally:

```
Ben seni seviyorum.
I   you.ACC  love.PROG.1SG
→ Natural English: "I love you" (NOT "I you love")
```

### Topic/Focus via Word Order

Turkish fronted elements carry topic/emphasis:
- **Default**: Subject-Topic first
- **Fronted object**: Object is in focus/contrast
- **Verb-final**: Default; non-final verb = marked for emphasis

## Translation Quality Checklist

- [ ] Full suffix chain decomposed with vowel harmony variants noted
- [ ] Evidentiality (-miş) correctly conveyed in translation
- [ ] SOV restructured to natural target-language word order
- [ ] Case suffixes correctly tagged
- [ ] Possessive suffixes correctly identified
- [ ] Vowel harmony variants listed in morpheme notes
- [ ] Topic/focus marking reflected in translation
