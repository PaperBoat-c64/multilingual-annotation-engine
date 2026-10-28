# Tokenization Engine — Language-Aware Segmentation

**Core principle**: The system does not assume whitespace-separated words. Tokenization adapts to the morphological and orthographic properties of each language.

## Table of Contents
- [No-Space Languages](#no-space-languages)
- [Morphological Segmentation](#morphological-segmentation)
- [Clitic Separation](#clitic-separation)
- [Compound Word Handling](#compound-word-handling)
- [Syllable-Based Segmentation](#syllable-based-segmentation)
- [Token Confidence Scoring](#token-confidence-scoring)

---

## No-Space Languages

### Chinese (中文)

**Challenge**: No spaces between words. Characters form words of 1-4+ characters.

**Strategy**: Dictionary-based + statistical word segmentation.

```
Input:     月亮代表我的心
Segmented: 月亮 / 代表 / 我 / 的 / 心
```

**Rules**:
1. Use a dictionary of common Chinese words (词)
2. Prioritize longest-match segmentation (最大匹配)
3. Single characters are only separate tokens if they have independent meaning:
   - 的 (possessive particle) → separate token
   - 了 (aspect marker) → separate token
   - 吗 (question particle) → separate token
   - 心 in 我的心 → attached to possessor unless semantically independent
4. Idioms (成语, 4 characters) → single token
5. Names (2-3 characters) → single token

### Japanese (日本語)

**Challenge**: No spaces. Mix of Kanji, Hiragana, Katakana. Particle boundaries mark word edges.

**Strategy**: Morphological segmentation at word boundaries using particle detection.

```
Input:     君の名は
Segmented: 君 / の / 名 / は
```

**Rules**:
1. Particles (助詞) are always separate tokens: は, が, を, に, へ, と, から, まで, より, で, も, の
2. Auxiliary verbs (助動詞) are separate: た, だ, です, ます, ない, たい, られる
3. Verb stems + inflections: 食べた → 食べ + た
4. Katakana loanwords → single token: コンピューター
5. Compound kanji words → single token: 学校, 日本語

### Thai (ภาษาไทย)

**Challenge**: No spaces between words. Spaces separate sentences/clauses, not words.

**Strategy**: Dictionary-based word boundary detection.

```
Input:     ฉันรักเธอ
Segmented: ฉัน / รัก / เธอ
```

**Rules**:
1. Use a Thai dictionary for longest-match segmentation
2. Honor existing spaces (sentence/clause boundaries)
3. Tone marks are part of the syllable/word — never separate

### Khmer (ភាសាខ្មែរ)

**Challenge**: No spaces between words. Spaces separate clauses.

**Strategy**: Syllable-boundary detection.

```
Input:     ខ្ញុំស្រលាញ់អ្នក
Segmented: ខ្ញុំ / ស្រលាញ់ / អ្នក
```

### Burmese (မြန်မာဘာသာ)

**Challenge**: No inter-word spaces. Syllable clusters form words.

**Strategy**: Syllable-cluster-level segmentation.

### Lao (ພາສາລາວ)

Same strategy as Thai — no spaces between words.

---

## Morphological Segmentation

### Japanese Morphological Decomposition

```
走りたくなかった
→ 走り (stem: hashiri) + たく (tai-ADV) + なかっ (nai-ADV) + た (PAST)
→ "did not want to run"
```

### Korean Eojeol Decomposition

```
먹었습니다
→ 먹 (stem: eat) + 었 (PAST) + 습니다 (formal declarative)
→ "ate" (formal)
```

Within an eojeol (어절, space-separated block), segment into morphemes:
1. Content stem
2. Derivational suffixes
3. Inflectional suffixes
4. Sentence-final endings

---

## Clitic Separation

### Arabic Proclitics and Enclitics

Arabic words can carry multiple clitics:

```
وسأكتبها
→ و (wa-, "and") + س (sa-, "will") + أ (ʾa-, 1SG) + كتب (ktb, "write") + ها (-hā, "it")
→ "and I will write it"
```

**Segmentation strategy**:
1. Separate proclitics: bi- (بِ), li- (لِ), wa- (وَ), fa- (فَ), sa- (سَ), ʾa- (أَ)
2. Separate enclitics: -hā (هَا), -hum (هُمْ), -ka (كَ), -kum (كُمْ), -ī (ِي), -nā (نَا)
3. Keep the root + pattern stem as the core token
4. Mark separated clitics with `[proclitic]` and `[enclitic]` tags

### Persian Enclitics

```
کتابم
→ کتاب (ketâb, "book") + م (-am, "my")
→ "my book"
```

Separate: -am (م), -at (ت), -ash (ش), -emân (مان), -etân (تان), -eshân (شان)
Also: râ (را, object marker), -i (ی, indefinite)

### Hebrew Prefixed Prepositions

```
ובבית
→ ו (ve-, "and") + ב (be-, "in") + בית (bayit, "house")
→ "and in the house"
```

Separate: ve- (ו), be- (ב), le- (ל), ke- (כ), mi- (מ), she- (ש), ha- (ה)

---

## Compound Word Handling

### German Compound Nouns

```
Donaudampfschifffahrtsgesellschaftskapitän
→ Donau + Dampf + Schiff + Fahrt + Gesellschaft + Kapitän
→ "Danube steamship travel company captain"
```

**Strategy**: Decompose into constituent parts. Each part is a segment. Align to multiple translation words.

### Hindi Compound Words (Sandhi)

```
रामायण
→ राम (Rāma) + अयण (ayana, "journey")
→ "Rama's journey"
```

**Strategy**: Sandhi-aware splitting. Mark sandhi boundary.

### Sanskrit Compounds

```
गुरुकुलम्
→ गुरु (guru) + कुलम् (kulam, "family/school")
→ "teacher's school"
```

Tatpurusha, karmadharaya, dvandva, bahuvrihi compounds — all decompose differently. Mark compound type in annotation.

### Finnish Compound Words

```
rautatieasema
→ rauta + tie + asema
→ "railway station"
```

---

## Syllable-Based Segmentation

### Vietnamese

Vietnamese is already space-separated at the syllable level. Each syllable is a token:

```
Tôi yêu em
→ Tôi / yêu / em
→ "I love you"
```

**Strategy**: 
1. Whitespace separation
2. Each syllable = one token
3. Compound meanings span multiple tokens — group for alignment

### Tibetan

Tibetan separates syllables with the tsheg character (་):

```
བོད་སྐད་
→ བོད (böd) + སྐད (ké)
→ "Tibetan language"
```

---

## Token Confidence Scoring

| Segmentation Type | Confidence | Notes |
|------------------|------------|-------|
| Whitespace-separated (English, French) | 0.99 | Trivial |
| Particle-separated (Japanese) | 0.95 | Particles are reliable markers |
| Clitic-separated (Arabic) | 0.90 | Some ambiguous cases (bi- vs part of root) |
| Dictionary-based (Chinese, Thai) | 0.85–0.92 | Ambiguity in dictionary boundaries |
| Compound decomposition (German, Sanskrit) | 0.80–0.88 | Compound boundary ambiguity |
| Morphological (Turkish, Finnish) | 0.82–0.90 | Suffix boundary ambiguity |
| Syllable-based (Khmer, Burmese) | 0.75–0.85 | Word boundary ambiguity |

---

## Agglutinative Language Tokenization

### Turkish

```
evlerimizden
→ ev + ler + imiz + den
→ house + PL + 1PL.POSS + ABL
→ "from our houses"
```

**Decomposition order**:
1. Stem: ev
2. Plural: -ler
3. Possessive: -imiz (1PL)
4. Case: -den (ablative)

### Finnish

```
taloissammekin
→ talo + i + ssa + mme + kin
→ house + PL + INE + 1PL.POSS + also
→ "in our houses too"
```

### Hungarian

```
házaimban
→ ház + a + i + m + ban
→ house + POSS + PL + 1SG + INE
→ "in my houses"
```

---

## Tokenization Output Format

Each token in the segmented output:

```json
{
  "text": "وسأكتبها",
  "tokens": [
    {"text": "و", "type": "proclitic", "gloss": "and"},
    {"text": "س", "type": "proclitic", "gloss": "will"},
    {"text": "أ", "type": "proclitic", "gloss": "1SG"},
    {"text": "كتب", "type": "stem", "gloss": "write"},
    {"text": "ها", "type": "enclitic", "gloss": "it"}
  ],
  "token_count": 5,
  "confidence": 0.90
}
```
