# Romanization Systems — Per-Language Standards

**Core principle**: Never use one universal romanization system. Every language uses its own established standard.

## Table of Contents
- [Arabic](#arabic)
- [Persian](#persian)
- [Urdu](#urdu)
- [Hebrew](#hebrew)
- [Chinese (Mandarin)](#chinese-mandarin)
- [Japanese](#japanese)
- [Korean](#korean)
- [Russian](#russian)
- [Hindi / Sanskrit (IAST)](#hindi--sanskrit-iast)
- [Greek](#greek)
- [Thai](#thai)
- [Tibetan](#tibetan)
- [Georgian](#georgian)
- [Armenian](#armenian)
- [Amharic / Ethiopic](#amharic--ethiopic)
- [Burmese](#burmese)
- [Khmer](#khmer)
- [Tamil / Indic (ISO 15919)](#tamil--indic-iso-15919)
- [Vietnamese](#vietnamese)
- [Turkish (Latin Script)](#turkish-latin-script)

---

## Arabic

**Default system**: DIN 31635 (Deutsche Morgenländische Gesellschaft)

| Arabic | DIN 31635 | Notes |
|--------|-----------|-------|
| ا | ā / ʾ | ā when long vowel, ʾ for hamza |
| ب | b | |
| ت | t | |
| ث | ṯ | th sound |
| ج | ǧ | also romanized as "j" |
| ح | ḥ | pharyngeal h |
| خ | ḫ | also "kh" |
| د | d | |
| ذ | ḏ | also "dh" |
| ر | r | |
| ز | z | |
| س | s | |
| ش | š | also "sh" |
| ص | ṣ | emphatic s |
| ض | ḍ | emphatic d |
| ط | ṭ | emphatic t |
| ظ | ẓ | emphatic dh |
| ع | ʿ | pharyngeal stop |
| غ | ġ | also "gh" |
| ف | f | |
| ق | q | |
| ك | k | |
| ل | l | |
| م | m | |
| ن | n | |
| ه | h | |
| و | w / ū | |
| ي | y / ī | |

**Alternative**: ALA-LC (Library of Congress) — widely used in academic libraries.

**User-friendly fallback**: When output targets learners (not academics), use simplified romanization: ṯ→th, ḫ→kh, š→sh, ġ→gh, etc. Claude should ask which style is preferred if ambiguous.

---

## Persian

**Default system**: UniPers / simplified DIN (modified for Persian phonology)

| Persian | Romanization | Notes |
|---------|-------------|-------|
| ا | â / a / e / o | â initially, a/e/o contextually |
| ب | b | |
| پ | p | |
| ت | t | |
| ث | s | Pronounced as 's' in Persian |
| ج | j | |
| چ | ch | |
| ح | h | Pronounced as 'h' in Persian |
| خ | kh | |
| د | d | |
| ذ | z | Pronounced as 'z' in Persian |
| ر | r | |
| ز | z | |
| ژ | zh | Like 's' in "measure" |
| س | s | |
| ش | sh | |
| ص | s | Pronounced as 's' in Persian |
| ض | z | Pronounced as 'z' in Persian |
| ط | t | Pronounced as 't' in Persian |
| ظ | z | Pronounced as 'z' in Persian |
| ع | ' / â | Glottal stop or vowel lengthening |
| غ | gh | |
| ف | f | |
| ق | gh / q | Same as غ in most dialects |
| ک | k | |
| گ | g | |
| ل | l | |
| م | m | |
| ن | n | |
| و | v / u / ow | v consonant, u/ow vowel |
| ه | h / e | h consonant, -eh word-final |
| ی | y / i / ey | y consonant, i/ey vowel |

**Short vowels** (usually unwritten in Persian script):
- َ (zabar) → a
- ِ (zir) → e
- ُ (pish) → o

---

## Urdu

**Default system**: ALA-LC Urdu (with retroflex and aspirated consonant marking)

Key distinctions from Persian/Arabic:
- Retroflex consonants: ٹ (ṭ), ڈ (ḍ), ڑ (ṛ)
- Aspirated series: بھ (bh), پھ (ph), تھ (th), etc.
- Nasalization: ں (̃)

---

## Hebrew

**Default system**: ISO 259 or simplified academic romanization

| Hebrew | Romanization |
|--------|-------------|
| א | ' (alef) |
| ב | b / v |
| ג | g |
| ד | d |
| ה | h |
| ו | v / o / u |
| ז | z |
| ח | ch / ḥ |
| ט | t |
| י | y / i |
| כ/ך | k / kh |
| ל | l |
| מ/ם | m |
| נ/ן | n |
| ס | s |
| ע | ' (ayin) |
| פ/ף | p / f |
| צ/ץ | tz / ts |
| ק | k / q |
| ר | r |
| ש | sh / s |
| ת | t |

---

## Chinese (Mandarin)

**Default system**: Hànyǔ Pīnyīn (汉语拼音)

Features:
- Tone marks on vowels: ā á ǎ à (1st–4th tone), a (neutral tone)
- ü for the rounded front vowel
- Apostrophe for syllable boundary when ambiguous: Xī'ān (西安) vs xiān (先)
- Standard syllable structure: Initial + Final + Tone

**Alternative**: Wade-Giles — use only if user explicitly requests it.

---

## Japanese

**Default system**: Modified Hepburn (Hebon-shiki)

| Kana | Hepburn |
|------|---------|
| し | shi |
| ち | chi |
| つ | tsu |
| ふ | fu |
| じ | ji |
| づ | zu |
| Long vowels: ō, ū (おう→ō, うう→ū) |

**Syllabic n**: ん is romanized as n before consonants (except n, m, y) and at word end; n' before vowels and y; m before b, m, p.

**Alternative**: Kunrei-shiki — use only if user explicitly requests it.

---

## Korean

**Default system**: Revised Romanization of Korean (2000)

| Hangul | RR |
|--------|----|
| ㄱ | g / k |
| ㄷ | d / t |
| ㅂ | b / p |
| ㅈ | j / ch |
| ㄹ | r / l |
| ㅅ | s / t (final) |
| ㅇ | ng (final) / silent (initial) |

Vowels: a, eo, o, u, eu, i, ae, e, oe, wi, etc.

**Alternative**: McCune-Reischauer — use only if user explicitly requests it.

---

## Russian

**Default system**: ISO 9 (GOST 7.79 System A) for scholarly, BGN/PCGN for practical

| Cyrillic | ISO 9 | Practical |
|----------|-------|-----------|
| А а | a | a |
| Б б | b | b |
| В в | v | v |
| Г г | g | g |
| Д д | d | d |
| Е е | e | e / ye |
| Ё ё | ë | yo |
| Ж ж | ž | zh |
| З з | z | z |
| И и | i | i |
| Й й | j | y |
| К к | k | k |
| Л л | l | l |
| М м | m | m |
| Н н | n | n |
| О о | o | o |
| П п | p | p |
| Р р | r | r |
| С с | s | s |
| Т т | t | t |
| У у | u | u |
| Ф ф | f | f |
| Х х | h | kh |
| Ц ц | c | ts |
| Ч ч | č | ch |
| Ш ш | š | sh |
| Щ щ | ŝ | shch |
| Ы ы | y | y |
| Э э | è | e |
| Ю ю | û | yu |
| Я я | â | ya |
| Ь ь | ' | ' (soft sign) |
| Ъ ъ | " | " (hard sign) |

---

## Hindi / Sanskrit (IAST)

**Default system**: IAST (International Alphabet of Sanskrit Transliteration)

| Devanagari | IAST | Notes |
|-----------|------|-------|
| अ | a | |
| आ | ā | |
| इ | i | |
| ई | ī | |
| उ | u | |
| ऊ | ū | |
| ऋ | ṛ | |
| ए | e | |
| ऐ | ai | |
| ओ | o | |
| औ | au | |
| क | k | |
| ख | kh | |
| ग | g | |
| घ | gh | |
| ङ | ṅ | |
| च | c | |
| छ | ch | |
| ज | j | |
| झ | jh | |
| ञ | ñ | |
| ट | ṭ | |
| ठ | ṭh | |
| ड | ḍ | |
| ढ | ḍh | |
| ण | ṇ | |
| त | t | |
| थ | th | |
| द | d | |
| ध | dh | |
| न | n | |
| प | p | |
| फ | ph | |
| ब | b | |
| भ | bh | |
| म | m | |
| य | y | |
| र | r | |
| ल | l | |
| व | v | |
| श | ś | |
| ष | ṣ | |
| स | s | |
| ह | h | |
| ं | ṃ | anusvara |
| ः | ḥ | visarga |

**Learner-friendly variant**: NLK (National Library at Kolkata) — drops diacritics, uses "sh" for ś/ṣ. Use when user is a beginner.

---

## Greek

**Default system**: ISO 843

| Greek | ISO 843 | Notes |
|-------|---------|-------|
| Α α | a | |
| Β β | v | |
| Γ γ | g | |
| Δ δ | d | |
| Ε ε | e | |
| Ζ ζ | z | |
| Η η | i | |
| Θ θ | th | |
| Ι ι | i | |
| Κ κ | k | |
| Λ λ | l | |
| Μ μ | m | |
| Ν ν | n | |
| Ξ ξ | x | |
| Ο ο | o | |
| Π π | p | |
| Ρ ρ | r | |
| Σ σ/ς | s | |
| Τ τ | t | |
| Υ υ | y | |
| Φ φ | f | |
| Χ χ | ch | |
| Ψ ψ | ps | |
| Ω ω | o | |

**Diphthongs**: αι→ai, ει→ei, οι→oi, ου→ou, αυ→av/af, ευ→ev/ef

---

## Thai

**Default system**: RTGS (Royal Thai General System of Transcription)

Features:
- No tone marks in output (tones are lexical — indicate in IPA if requested)
- Vowel length not marked in basic RTGS (marked in ISO 11940 if needed)
- Consonant distinctions simplified: ท/ธ/ถ/ฐ all → "th"

**Alternative**: ISO 11940 — use only for academic/linguistic contexts where exact reversibility is needed.

---

## Tibetan

**Default system**: Wylie transliteration (for written Tibetan)

| Tibetan | Wylie | Notes |
|---------|-------|-------|
| ཀ | k | |
| ཁ | kh | |
| ག | g | |
| ང | ng | |
| ཅ | c | |
| ཆ | ch | |
| ཇ | j | |
| ཉ | ny | |
| ཏ | t | |
| ཐ | th | |
| ད | d | |
| ན | n | |
| པ | p | |
| ཕ | ph | |
| བ | b | |
| མ | m | |
| ཙ | ts | |
| ཚ | tsh | |
| ཛ | dz | |
| ཝ | w | |

**Learner-friendly alternative**: THL Simplified Phonetic Transcription — approximates modern Lhasa pronunciation. Use for learners who need pronunciation guidance.

---

## Georgian

**Default system**: ISO 9984

| Georgian (Mkhedruli) | ISO 9984 |
|---------------------|----------|
| ა | a |
| ბ | b |
| გ | g |
| დ | d |
| ე | e |
| ვ | v |
| ზ | z |
| თ | t' |
| ი | i |
| კ | k |
| ლ | l |
| მ | m |
| ნ | n |
| ო | o |
| პ | p' |
| ჟ | ž |
| რ | r |
| ს | s |
| ტ | t |
| უ | u |
| ფ | p |
| ქ | k' |
| ღ | ḡ |
| ყ | q |
| შ | š |
| ჩ | č |
| ც | c |
| ძ | j |
| წ | c' |
| ჭ | č' |
| ხ | x |
| ჯ | ǰ |
| ჰ | h |

---

## Armenian

**Default system**: ISO 9985

| Armenian | ISO 9985 |
|----------|----------|
| Ա ա | a |
| Բ բ | b |
| Գ գ | g |
| Դ դ | d |
| Ե ե | e / ye |
| Զ զ | z |
| Է է | ē |
| Ը ը | ë |
| Թ թ | t' |
| Ժ ժ | ž |
| Ի ի | i |
| Լ լ | l |
| Խ խ | x |
| Ծ ծ | c |
| Կ կ | k |
| Հ հ | h |
| Ձ ձ | j |
| Ղ ղ | ł |
| Ճ ճ | č |
| Մ մ | m |
| Յ յ | y |
| Ն ն | n |
| Շ շ | š |
| Ո ո | o / vo |
| Չ չ | č' |
| Պ պ | p |
| Ջ ջ | ǰ |
| Ռ ռ | ṙ |
| Ս ս | s |
| Վ վ | v |
| Տ տ | t |
| Ր ր | r |
| Ց ց | c' |
| Ւ ւ | w |
| Փ փ | p' |
| Ք ք | k' |
| Օ օ | ō |
| Ֆ ֆ | f |

---

## Amharic / Ethiopic

**Default system**: ISO 233-3

| ሀ | ለ | ሐ | መ | ሠ | ረ | ሰ | ቀ |
|----|----|----|----|----|----|----|----|
| ha | la | ḥa | ma | śa | ra | sa | qa |

Each base consonant has 7 vowel forms (ä, u, i, a, e, ə, o).

**Note**: ISO 233-3 distinguishes ሀ(h), ሐ(ḥ), ኀ(ḫ) which are pronounced identically in modern Amharic. For practical use, merge to "h".

---

## Burmese

**Default system**: MLC Transcription System (Myanmar Language Commission)

| Burmese | MLC | Notes |
|---------|-----|-------|
| က | k | |
| ခ | hk | |
| ဂ | g | |
| ဃ | gh | |
| င | ng | |
| စ | s | |
| ဆ | hs | |
| ဇ | z | |
| ဈ | z | |
| ည | ny | |

MLC is the official standard used in Myanmar. Use ISO 11940 as scholarly alternative.

---

## Khmer

**Default system**: UNGEGN (United Nations Group of Experts on Geographical Names)

| Khmer | UNGEGN |
|-------|--------|
| ក | k |
| ខ | kh |
| គ | k |
| ឃ | kh |
| ង | ng |
| ច | ch |
| ឆ | chh |
| ជ | ch |
| ឈ | chh |
| ញ | nh |

**Note**: Khmer has many letters with the same romanization due to historical spelling. Clarify ambiguity in annotations when needed.

---

## Tamil / Indic (ISO 15919)

**Default system for Tamil and all Indic scripts**: ISO 15919

ISO 15919 is the unified Indic transliteration standard. It covers Devanagari, Bengali, Gurmukhi, Gujarati, Odia, Tamil, Telugu, Kannada, Malayalam, and Sinhala.

| Tamil | ISO 15919 |
|-------|-----------|
| அ | a |
| ஆ | ā |
| இ | i |
| ஈ | ī |
| உ | u |
| ஊ | ū |
| எ | e |
| ஏ | ē |
| ஐ | ai |
| ஒ | o |
| ஓ | ō |
| ஔ | au |
| க | k |
| ங | ṅ |
| ச | c |
| ஞ | ñ |
| ட | ṭ |
| ண | ṇ |
| த | t |
| ந | n |
| ப | p |
| ம | m |
| ய | y |
| ர | r |
| ல | l |
| வ | v |
| ழ | ḻ |
| ள | ḷ |
| ற | ṟ |
| ன | ṉ |

---

## Vietnamese

Vietnamese already uses Latin script (Quốc Ngữ) — no romanization needed.

However:
- **Tone marks must be preserved**: ma, mà, má, mả, mã, mạ (6 tones)
- **Diacritics must be preserved**: â, ă, ê, ô, ơ, ư
- **IPA generation** is useful for pronunciation guidance (complex vowel system, implosive consonants)

---

## Turkish (Latin Script)

Turkish already uses Latin script — no romanization needed. However:
- **IPA generation** may still be useful (Turkish orthography is largely phonemic)
- **Gloss**: Turkish agglutination should be decomposed for learners
  - "evlerimizden" → ev-ler-imiz-den (house-PL-1PL.POSS-ABL = "from our houses")

---

## Romanization System Selection Tree

```
Input Script
├── Arabic → Check language-specific characters
│   ├── Persian: UniPers / simplified DIN
│   ├── Urdu: ALA-LC Urdu
│   ├── Pashto: ALA-LC Pashto
│   ├── Kurdish: Kurdish Latin alphabet mapping
│   ├── Uyghur: Uyghur Latin alphabet (ULY)
│   └── Arabic: DIN 31635 (or ALA-LC)
├── CJK
│   ├── Chinese: Hànyǔ Pīnyīn
│   ├── Japanese: Modified Hepburn
│   └── Korean: Revised Romanization
├── Hebrew → ISO 259
├── Cyrillic → ISO 9 (scholarly) / BGN/PCGN (practical)
├── Greek → ISO 843
├── Georgian → ISO 9984
├── Armenian → ISO 9985
├── Devanagari → IAST (Sanskrit/classical) / ISO 15919 (modern)
├── Other Indic → ISO 15919
├── Thai → RTGS
├── Tibetan → Wylie (written) / THL Phonetic (pronunciation)
├── Burmese → MLC
├── Khmer → UNGEGN
├── Ethiopic → ISO 233-3
└── Latin-script (Vietnamese, Turkish, etc.) → No romanization needed; IPA on request
```
