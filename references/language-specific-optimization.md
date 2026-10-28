# Language-Specific Optimization

**Core principle**: Each language has unique features that affect translation, segmentation, and alignment. The system adapts accordingly.

## Table of Contents
- [Japanese](#japanese)
- [Chinese](#chinese)
- [Korean](#korean)
- [Hindi / Urdu](#hindi--urdu)
- [Arabic](#arabic)
- [Hebrew](#hebrew)
- [Russian](#russian)
- [Turkish](#turkish)
- [Persian](#persian)
- [Thai](#thai)
- [Vietnamese](#vietnamese)
- [Finnish / Hungarian](#finnish--hungarian)
- [German](#german)

---

## Japanese

### Honorific System (敬語)

Three levels must be preserved in translation register:

| Japanese | Type | Register | English Equivalent |
|----------|------|----------|--------------------|
| 行く (iku) | Plain | Casual | "go" |
| 行きます (ikimasu) | Polite | Standard | "go" (polite context) |
| いらっしゃいます (irasshaimasu) | Honorific | Very formal | honorific verb form |

**Strategy**: 
- Map honorific level to target language register
- Eng: "go" → "go" → "proceed/depart" (ascending formality)
- Annotate keigo type in advanced mode

### Particles (助詞)

Japanese particles are crucial for meaning. They must be correctly interpreted, not skipped:

| Particle | Function | Translation Impact |
|----------|----------|-------------------|
| は (wa) | Topic | What the sentence is ABOUT |
| が (ga) | Subject | Who/what performs the action |
| を (o) | Object | What receives the action |
| に (ni) | Direction/Location/Time | "to", "at", "on" |
| へ (e) | Direction | "toward" (more poetic than に) |
| で (de) | Location/Means | "at", "by means of" |
| の (no) | Possessive/Attributive | "of", "'s" |
| も (mo) | Also/Even | "also", "even" |
| と (to) | And/With/Quotative | "and", "with", marks quotes |
| から (kara) | From/Because | "from", "because" |
| まで (made) | Until | "until" |
| より (yori) | Comparison | "more than" |

### Implied Subjects

Japanese often omits the subject. Mark for languages that require one:

```
食べた (tabeta)
→ [implied: subject] ate
→ Translation: "He ate" or "I ate" or "She ate" (depending on context)
```

### Cultural Nuance

| Concept | Meaning | Translation Note |
|---------|---------|-----------------|
| もののあはれ (mono no aware) | Pathos of impermanence | May need cultural note |
| 間 (ma) | Negative space, pause, interval | Poetic silence — preserve with line breaks |
| わびさび (wabi-sabi) | Beauty in imperfection | May need cultural note |
| こころ (kokoro) | Heart-mind-spirit (unified) | Not just "heart" — broader concept |

---

## Chinese

### Idioms (成语)

Four-character idioms are single conceptual units:

```
画蛇添足 (huà shé tiān zú)
Literal: "draw snake add feet"
Meaning: "to gild the lily" / "to overdo it"
```

**Strategy**:
- Translate the meaning naturally
- In advanced mode: include literal gloss as annotation
- Never translate character by character

### Classical References (典故)

```
沉鱼落雁 (chényú-luòyàn)
Reference: Xi Shi (西施) and Wang Zhaojun (王昭君), legendary beauties
Meaning: "devastatingly beautiful"
```

**Strategy**: Preserve the meaning, annotate the reference in advanced mode.

### Tone and Register

Chinese has distinct registers:

| Register | Example | Context |
|----------|---------|---------|
| Classical (文言) | 余, 吾, 汝 | Poetry, formal writing |
| Formal written (书面语) | 我们, 你 | Formal prose |
| Colloquial (口语) | 咱, 你 | Conversation |
| Slang (俚语) | 哥们儿, 姐们儿 | Casual/informal |

**Strategy**: Map register to target language equivalent.

### Measure Words (量词)

Chinese uses classifiers between numbers and nouns:

```
一个人 (yī gè rén) — "one person" (个 = general classifier)
一本书 (yī běn shū) — "one book" (本 = volume classifier)
一条河 (yī tiáo hé) — "one river" (条 = long/thin classifier)
```

**Strategy**: In translation, classifiers disappear (target languages don't use them). In advanced mode, annotate the classifier.

---

## Korean

### Speech Levels (말투)

Korean has a complex speech level system:

| Level | Ending | Context | English Register |
|-------|--------|---------|-----------------|
| 합쇼체 (Formal polite) | -습니다 | Broadcast, formal speech | Formal |
| 해요체 (Informal polite) | -아요/-어요 | Everyday polite | Standard |
| 해체 (Intimate) | -아/-어 | Close friends, younger | Casual |
| 해라체 (Plain) | -는다 | Writing, inner monologue | Neutral/declarative |
| 합시다체 (Formal suggestion) | -읍시다 | "Let's..." (formal) | Inclusive |
| 하소서체 (Archaic formal) | -나이다 | Historical/royal | Archaic |

**Strategy**:
- Map speech level to target language register
- Annotate level shift in advanced mode
- 해요체 → standard polite; 해체 → casual; 합쇼체 → formal

### Honorific System

| Type | Marker | Example | Effect |
|------|--------|---------|--------|
| Subject honorific | -(으)시- | 가십니다 (he goes, formal) | Elevates subject |
| Lexical honorific | 계시다 (exist, hon.) | Honorific replacement |
| Object honorific | 께 | 선생님께 (to the teacher, hon.) | Elevates object |
| Humble form | 저 (I, humble), 드리다 (give, humble) | Lowers self |

### Omitted Subjects

Like Japanese, Korean regularly omits the subject:

```
먹었어 (meogeosseo)
→ [implied: subject] ate (intimate speech level)
→ "I ate" (likely from context) or "He/she ate"
```

---

## Hindi / Urdu

### Poetic Vocabulary

Hindi/Urdu lyrics draw from two lexical registers:

| Register | Source | Flavor | Example |
|----------|--------|--------|---------|
| Tatsama | Sanskrit | Formal, literary, "pure" Hindi | हृदय (hṛdaya, heart) |
| Persian-Arabic | Persian/Arabic | Poetic, sophisticated, Urdu | दिल/دل (dil, heart) |

**Strategy**: 
- Detect the register shift
- Preserve the register flavor in translation
- Persian-Arabic words often have elevated/poetic connotations

### Bollywood Lyric Conventions

| Structure | Hindi/Urdu Name | Function |
|-----------|----------------|----------|
| Chorus | मुखड़ा/مکھڑا (mukhda) | Hook, repeated |
| Verse | अंतरा/انترا (antara) | Narrative development |
| Bridge | — | Musical transition |

**Strategy**: Mark the structural elements in output.

### Ezafe in Urdu

Urdu inherits the Persian ezafe construction:

```
دلِ بےقرار (dil-e beqarār)
→ "restless heart" (literally: "heart of restless")
```

---

## Arabic

### Root-Pattern Morphology

Track root occurrences across a document for visual linking:

Document with root ع-ش-ق (ʿ-sh-q, "love"):
- عاشق (ʿāshiq) → "lover"
- معشوق (maʿshūq) → "beloved"
- عشق (ʿishq) → "love"
- عشاق (ʿushshāq) → "lovers"

**Strategy**: Link root-related words visually (same hue family, varying saturation).

### Religious References

Arabic lyrics frequently contain Quranic allusions and Islamic phraseology:

```
يا رب (yā rabb) — "O Lord"
بسم الله (bismillāh) — "In the name of God"
الحمد لله (al-ḥamdu lillāh) — "Praise be to God"
```

**Strategy**: Preserve the religious register. Use target-language equivalents (e.g., "O Lord" not "Hey God").

### Classical (Fusha) vs Colloquial (Ammiya)

| Register | Features | Context |
|----------|----------|---------|
| Fusha (الفصحى) | Full case endings, classical vocabulary | Formal poetry, nasheed, news |
| Ammiya (العامية) | Simplified grammar, dialect vocabulary | Pop songs, conversation |

**Strategy**: Detect the register. Fusha → elevated/formal translation. Ammiya → natural/colloquial translation.

---

## Hebrew

### Biblical References

Hebrew lyrics often reference Tanakh (Hebrew Bible):

```
שיר השירים (Shir HaShirim) — "Song of Songs"
גן עדן (Gan Eden) — "Garden of Eden"
```

**Strategy**: Use established English Bible translations for recognized phrases. Preserve the biblical register.

### Modern vs Biblical Usage

| Word | Biblical | Modern Israeli |
|------|----------|---------------|
| חשמל (chashmal) | "electrum" (divine radiance, Ezekiel) | "electricity" |
| נורא (nora) | "awesome/terrible" (divine) | "very" (intensifier) |

**Strategy**: Detect from context whether the usage is biblical/liturgical or modern conversational.

---

## Russian

### Aspect Pairs

Russian verbs come in aspect pairs. The aspect choice affects meaning:

| Imperfective (несов. вид) | Perfective (сов. вид) | Meaning |
|--------------------------|----------------------|---------|
| писать (pisat') | написать (napisat') | "to write" / "to write completely" |
| читать (chitat') | прочитать (prochitat') | "to read" / "to read through" |
| видеть (videt') | увидеть (uvidet') | "to see" / "to catch sight of" |

**Strategy**: Use English aspect equivalents (progressive for imperfective, perfect for perfective) or verb choice to convey the distinction.

### Case System

6 cases with semantic roles:

| Case | Question | Semantic Role |
|------|----------|---------------|
| Nominative | кто? что? | Subject |
| Accusative | кого? что? | Direct object |
| Genitive | кого? чего? | Possession, negation, partitive |
| Dative | кому? чему? | Indirect object, recipient |
| Instrumental | кем? чем? | Means, accompaniment |
| Prepositional | о ком? о чём? | Location, topic |

### Poetic Inversion

Russian poetry uses non-standard word order for meter and emphasis:

```
Я вас любил (Pushkin)
[I] [you] [loved] — Standard: Я любил вас
```

**Strategy**: 
- Preserve natural word order in translation
- Use emphasis markers (italic, bold) to convey the emphasis of inversion
- Annotate inverted structures in advanced mode

---

## Turkish

### Agglutination Chains

Turkish can pack extensive information into a single word:

```
gidemeyebilirdim
→ gid + e + me + y + ebil + ir + di + m
→ go + ABIL + NEG + buffer + ABIL + AOR + PAST + 1SG
→ "I might not have been able to go"
```

**Strategy**: Decompose for alignment. Each suffix maps to a translation segment.

### Word Order Flexibility

Turkish is SOV with pragmatic reordering:

```
Ben seni seviyorum.  (I you love — neutral SOV)
Seni ben seviyorum.  (Emphasis on "you")
Seviyorum seni ben.  (Emphasis on "love")
```

**Strategy**: 
- Normalize to SVO for translation
- Convey emphasis through alternative means (word choice, italics)

### Vowel Harmony

Two types:
- Front/back: ev-ler (houses) vs kapı-lar (doors)
- Rounding: gör-dü (saw) vs al-dı (took)

**Strategy**: Romanization reflects vowel harmony. Annotation in advanced mode.

---

## Persian

### Poetic Metaphors

Persian poetry has a rich, conventionalized metaphor system:

| Symbol | Meaning | Example |
|--------|---------|---------|
| گل (gol, rose) | The beloved | گل من (my rose = my beloved) |
| بلبل (bolbol, nightingale) | The lover | بلبل عاشق (the loving nightingale) |
| می (mey, wine) | Spiritual ecstasy | جام می (the cup of wine = divine intoxication) |
| شمع (sham', candle) | The self-consuming lover | شمع شب (night candle) |
| پروانه (parvâne, moth) | The self-sacrificing lover | پروانه و شمع (the moth and candle) |
| زلف (zolf, lock of hair) | The beloved's captivating beauty | زلف پریشان (disheveled locks) |

**Strategy**: Preserve the metaphor system. Annotate symbolic meanings in advanced mode.

### Ezafe Construction

The ezafe (-e/-ye) links nouns to modifiers:

```
دلِ تنگ (del-e tang)
→ "narrow heart" = "constricted heart, aching heart"
```

**Strategy**: Ezafe is a linking vowel with no direct English equivalent. Translate the resulting phrase naturally.

### Classical Literary Style

Persian classical poetry (Hafez, Rumi, Saadi) uses:
- Archaic verb forms
- Specialized poetic vocabulary
- Conventional praise openings (مدح)
- Conventional closing signatures (تخلص)

**Strategy**: Preserve the elevated register. Use archaizing touches in translation (e.g., "thou" for classical, "you" for modern).

---

## Thai

### Implicit Grammar

Thai does not mark tense, number, or person grammatically:

```
ฉันรักเธอ (chan rak thoe)
[I] [love] [you]
→ Can mean: "I love you", "I loved you", "I will love you"
```

**Strategy**: Infer tense/number from context. Mark inferred information in advanced mode.

### Word Segmentation

Thai has no spaces between words:

```
ฉันรักเธอ → ฉัน / รัก / เธอ
```

**Strategy**: Use dictionary-based segmentation (see tokenization-engine.md).

### Politeness Particles

| Particle | Gender | Context |
|----------|--------|---------|
| ครับ (khrap) | Male speaker | Polite |
| ค่ะ (kha) | Female speaker | Polite |
| คะ (kha) | Female speaker | Question |
| จ๊ะ (ja) | Either | Intimate |

**Strategy**: Politeness particles are usually not translated literally. Their function is reflected in the register of the translation.

---

## Vietnamese

### Classifier System

Vietnamese uses classifiers (similar to Chinese):

| Classifier | Use |
|-----------|-----|
| con | Animals, animated objects |
| cái | Inanimate objects (general) |
| chiếc | Individual items, vehicles |
| người | People |
| quyển/cuốn | Books, volumes |
| bức | Letters, paintings, walls |
| cây | Stick-like objects, plants |

**Strategy**: Classifiers disappear in translation. Annotate in advanced mode.

### Tone-Sensitive Lexical Distinctions

Vietnamese has 6 tones that create lexical distinctions:

| Tone | Diacritic | Example | Meaning |
|------|-----------|---------|---------|
| Ngang | (none) | ma | ghost |
| Huyền | ` | mà | but |
| Sắc | ´ | má | mother |
| Hỏi | ̉ | mả | tomb |
| Ngã | ˜ | mã | horse |
| Nặng | . | mạ | rice seedling |

**Strategy**: Always preserve tone marks in text. IPA transcription includes tone numbers (1-6).

---

## Finnish / Hungarian

### Extensive Case Systems

Both languages have 15+ grammatical cases. See morphological-analysis.md for details.

### Vowel Harmony (Finnish)

| Harmony Class | Vowels | Example |
|--------------|--------|---------|
| Front | ä, ö, y | talossa → talossä |
| Back | a, o, u | talossa (in the house) |
| Neutral | e, i | Combine with either |

### Possessive Suffixes (Hungarian)

Instead of possessive pronouns, Hungarian uses suffixes:

```
házam — "my house"
házad — "your house"
háza — "his/her house"
házunk — "our house"
házatok — "your (pl) house"
házuk — "their house"
```

---

## German

### Compound Noun Decomposition

German compounds can be arbitrarily long. Decompose for alignment:

```
Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz
→ Rind + Fleisch + Etikettierung + Überwachung + Aufgabe + Übertragung + Gesetz
→ "Beef labeling monitoring task transfer law"
```

### Separable Prefix Verbs

```
aufmachen → ich mache auf (I open)
ausgehen → ich gehe aus (I go out)
```

**Strategy**: The separated prefix is a distinct token for alignment purposes.

### Modal Particles

German uses particles for nuance that have no direct translation:

| Particle | Function | Example |
|----------|----------|---------|
| doch | Contradiction / reminder | Das ist doch schön! (But it IS nice!) |
| ja | Known fact / emphasis | Das ist ja schön! (That really IS nice!) |
| mal | Softening / "just" | Komm mal her! (Come here for a sec) |
| denn | Interest / filler | Was ist denn los? (What's going on then?) |

**Strategy**: Convey the nuance through intonation or word choice. Annotate particles in advanced mode.
