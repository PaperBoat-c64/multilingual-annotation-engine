# Morphological Analysis — Complex Morphology Support

## Table of Contents
- [Overview](#overview)
- [Agglutinative Languages](#agglutinative-languages)
- [Root-Pattern Morphology (Arabic)](#root-pattern-morphology-arabic)
- [Fusional Languages](#fusional-languages)
- [Analytic Languages](#analytic-languages)
- [Morphological Decomposition Format](#morphological-decomposition-format)

---

## Overview

The system identifies **stems**, **affixes**, **particles**, and **grammatical markers** for accurate segmentation and alignment. Morphological analysis depth depends on the language's morphological type.

### Morphological Typology

| Type | Languages | Strategy |
|------|-----------|----------|
| Agglutinative | Turkish, Finnish, Hungarian, Japanese, Korean, Tamil | Decompose into stem + affix chain |
| Root-Pattern | Arabic, Hebrew, Amharic | Identify triliteral root + pattern |
| Fusional | Russian, German, Sanskrit, Greek | Identify stem + inflection with multiple meanings |
| Analytic | Chinese, Vietnamese, Thai | Each morpheme is a separate word; no decomposition needed |

---

## Agglutinative Languages

### Turkish

Turkish can form extremely long words through suffixation:

```
evlerimizdekilerden
→ ev + ler + imiz + de + ki + ler + den
→ house-PL-1PL.POSS-LOC-REL-PL-ABL
→ "from those who are in our houses"
```

**Suffix inventory** (partial):
- Plural: -ler / -lar
- Cases: -(y)i (ACC), -(y)e (DAT), -de (LOC), -den (ABL), -(n)in (GEN)
- Possessives: -(i)m, -(i)n, -(s)i, -(i)miz, -(i)niz, -leri
- Tense/Aspect: -iyor (PROG), -di (PAST), -ecek (FUT), -miş (EVID), -ir (AOR)
- Person: -(i)m, -sin, — , -(i)z, -siniz, -ler
- Derivation: -ci (agent), -lik (abstract), -li (with), -siz (without), -ce (adverbial)

**Vowel Harmony**: Suffixes alternate based on stem's last vowel:
- -ler/-lar: evler (houses) vs kapılar (doors)
- -di/-dı/-dü/-du: geldi (came) vs aldı (took) vs gördü (saw) vs oldu (happened)

### Finnish

```
taloissammekinkohan
→ talo + i + ssa + mme + kin + ko + han
→ house-PL-INE-1PL.POSS-also-Q-EMPH
→ "I wonder if (we are) also in our houses"
```

**Cases** (15):
- Nominative: —
- Partitive: -a/-ä, -ta/-tä
- Genitive: -n
- Inessive: -ssa/-ssä ("in")
- Elative: -sta/-stä ("from")
- Illative: -Vn, -hVn ("into")
- Adessive: -lla/-llä ("on")
- Ablative: -lta/-ltä ("from on")
- Allative: -lle ("onto")
- Essive: -na/-nä ("as")
- Translative: -ksi ("into being")
- Abessive: -tta/-ttä ("without")
- Instructive: -n ("by means of")
- Comitative: -ne- ("with")

### Hungarian

```
házaikban
→ ház + a + i + k + ban
→ house-POSS-PL-3PL.POSS-INE
→ "in their houses"
```

**Cases** (18+):
- Nominative: —
- Accusative: -t
- Dative: -nak/-nek
- Instrumental: -val/-vel
- Inessive: -ban/-ben
- Superessive: -n/-on/-en/-ön
- Adessive: -nál/-nél
- Illative: -ba/-be
- Sublative: -ra/-re
- Allative: -hoz/-hez/-höz
- Elative: -ból/-ből
- Delative: -ról/-ről
- Ablative: -tól/-től
- Terminative: -ig
- Essive-formal: -ként
- Essive-modal: -ul/-ül
- Translative: -vá/-vé
- Causal-final: -ért

---

## Root-Pattern Morphology (Arabic)

Arabic words are built from triliteral (three-consonant) roots combined with patterns (vowel templates + affixes).

### Example: Root k-t-b (ك-ت-ب) "writing"

| Form | Word | Romanization | Meaning |
|------|------|-------------|---------|
| I (basic) | كَتَبَ | kataba | he wrote |
| II (intensive) | كَتَّبَ | kattaba | he made write |
| III (associative) | كاتَبَ | kātaba | he corresponded |
| IV (causative) | أَكْتَبَ | ʾaktaba | he dictated |
| V (reflexive of II) | تَكَتَّبَ | takattaba | he was registered |
| VI (reflexive of III) | تَكاتَبَ | takātaba | they corresponded |
| VII (passive) | اِنْكَتَبَ | inkataba | he subscribed |
| VIII (reflexive) | اِكْتَتَبَ | iktataba | he copied |
| X (requestative) | اِسْتَكْتَبَ | istaktaba | he asked to write |
| Noun of place | مَكْتَب | maktab | office / desk |
| Noun of instrument | مِكْتَاب | miktāb | typewriter |
| Active participle | كاتِب | kātib | writer |
| Passive participle | مَكْتُوب | maktūb | letter (written thing) |
| Verbal noun | كِتابَة | kitāba | writing |
| Noun | كِتاب | kitāb | book |
| Diminutive | كُتَيِّب | kutayyib | booklet |

### Detection Strategy

1. **Extract root consonants**: For each Arabic word, identify the three core consonants
2. **Identify pattern**: Map the vowel template and affixes
3. **Link root occurrences**: Words with the same root across a document receive visual linking
4. **Annotation**: For advanced mode, annotate the root and pattern:

```
كتب (kataba) — Root: ك-ت-ب, Form I, 3SG.M.PAST
كاتب (kātib) — Root: ك-ت-ب, Active Participle, "writer"
مكتب (maktab) — Root: ك-ت-ب, Noun of Place, "office"
```

### Hebrew Root-Pattern

Similar to Arabic. Example: root k-t-v (כ-ת-ב) "writing":
- כָּתַב (katav) — he wrote
- מִכְתָּב (mikhtav) — letter
- כְּתוֹבֶת (ktovet) — address
- הִכְתִּיב (hikhtiv) — he dictated

---

## Fusional Languages

### Russian

Russian inflections encode multiple grammatical categories simultaneously:

```
написал (napisal) — "he wrote"
→ на- (PFV prefix) + пис (root "write") + а (theme vowel) + л (PAST) + ∅ (MASC.SG)
```

**Aspect pairs**:
- писать (napisat', IPFV: "to be writing") ↔ написать (napisat', PFV: "to write completely")
- читать (chitat', IPFV) ↔ прочитать (prochitat', PFV)
- говорить (govorit', IPFV) ↔ сказать (skazat', PFV, suppletive)

**Case system** (6 cases):
- Nominative: кто? что?
- Accusative: кого? что?
- Genitive: кого? чего?
- Dative: кому? чему?
- Instrumental: кем? чем?
- Prepositional: о ком? о чём?

### German

```
ausgegangen — "gone out"
→ aus- (separable prefix) + ge- (past participle) + gang (root "go") + en (suffix)
```

**Compound noun decomposition**:
```
Rechtsschutzversicherungsgesellschaften
→ Recht + s + Schutz + Versicherung + s + Gesellschaft + en
→ "legal protection insurance companies"
```

### Sanskrit

Sanskrit has extremely complex fusional morphology:

```
गच्छन्ति (gacchanti) — "they go"
→ गम् (gam, root "go") → गच्छ (present stem) + अन्ति (3PL.PRES.ACT)
```

8 cases × 3 numbers × 3 genders for nominals.
Extensive sandhi (euphonic combination) at word boundaries.

---

## Analytic Languages

### Chinese

Chinese has almost no inflectional morphology. Grammatical relationships are expressed through word order and particles.

**Aspect markers** (separate tokens):
- 了 (le) — perfective
- 过 (guò) — experiential
- 着 (zhe) — durative
- 在 (zài) — progressive

**Analysis**: Each grammatical morpheme is already a separate character. No decomposition needed. Annotation identifies the grammatical function.

### Vietnamese

Similar to Chinese — no inflection. Grammatical particles are separate words.

### Thai

No inflection. Tense, number, person are inferred from context or expressed through separate particles.

---

## Morphological Decomposition Format

### Standard Output Format

```json
{
  "word": "evlerimizden",
  "language": "tr",
  "decomposition": [
    {"text": "ev", "type": "stem", "gloss": "house", "pos": "noun"},
    {"text": "ler", "type": "suffix", "gloss": "PL", "category": "number"},
    {"text": "imiz", "type": "suffix", "gloss": "1PL.POSS", "category": "possession"},
    {"text": "den", "type": "suffix", "gloss": "ABL", "category": "case"}
  ],
  "morphological_type": "agglutinative",
  "confidence": 0.94
}
```

### Root-Pattern Output Format (Arabic)

```json
{
  "word": "مكتب",
  "romanization": "maktab",
  "language": "ar",
  "root": "ك-ت-ب",
  "pattern": "mafʿal",
  "pattern_type": "noun_of_place",
  "gloss": "office / desk",
  "related_words_in_document": ["كاتب", "كتاب", "يكتب"],
  "morphological_type": "root-pattern",
  "confidence": 0.92
}
```

### Compound Decomposition Format (German)

```json
{
  "word": "Donaudampfschifffahrtsgesellschaft",
  "language": "de",
  "decomposition": [
    {"text": "Donau", "gloss": "Danube"},
    {"text": "Dampf", "gloss": "steam"},
    {"text": "Schiff", "gloss": "ship"},
    {"text": "Fahrt", "gloss": "travel"},
    {"text": "Gesellschaft", "gloss": "company"}
  ],
  "morphological_type": "compound",
  "compound_type": "determinative",
  "confidence": 0.88
}
```
