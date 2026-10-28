# Thai Language Rules (th_rules.md)

## Language Profile
- **Language**: Thai (ภาษาไทย)
- **ISO 639-1**: `th`
- **Script**: Thai
- **Direction**: LTR
- **Morphological Type**: Analytic (isolating)
- **Word Order**: SVO (Subject-Verb-Object)
- **Script Family**: `thai`

## Morphology Rules

### No Inflection — Analytical Grammar

Thai is highly analytic. Words do not inflect. Grammatical relationships are expressed through word order and particles. Most words have empty morphemes arrays (just the root).

### Politeness Particles (คำลงท้าย)

Thai has gender-specific politeness particles that end sentences. These are CRITICAL for translation tone:

| Particle | Speaker Gender | ui_tag | Register |
|----------|---------------|--------|----------|
| ครับ (khráp) | Male | 礼貌助词 (Polite Particle — Male) | Polite/Formal |
| ค่ะ (khâ) | Female | 礼貌助词 (Polite Particle — Female) | Polite/Formal |
| จ้ะ (jâ) | Female | 亲切助词 (Affectionate Particle — Female) | Casual/Warm |
| จ๊ะ (já) | Both | 随意助词 (Casual Particle) | Very Casual |
| นะ (ná) | Both | 软化助词 (Softening Particle) | Softening/Appealing |
| สิ (sì) | Both | 催促助词 (Urging Particle) | Urging/Insisting |
| ล่ะ (lâ) | Both | 提问助词 (Question Particle) | Inquiring |

```
ไปกันเถอะนะครับ (bpai gan thùh ná khráp) → "Let's go, okay?" (male speaker, soft)
- ไป    → root: "go"
- กัน   → particle, ui_tag: "一起 (Together)"
- เถอะ  → particle, ui_tag: "建议 (Suggestion)"
- นะ   → particle, ui_tag: "软化 (Softening)"
- ครับ  → particle, ui_tag: "礼貌助词 男性 (Polite — Male)"
```

### Word Boundaries

**Thai does not use spaces between words.** Spaces indicate clause/sentence boundaries. Word segmentation is inherently ambiguous:

```
ฉันกินข้าว (chǎn kin khâo) → "I eat rice"
In Thai script: ฉันกินข้าว (no internal spaces)
Segmentation: ฉัน + กิน + ข้าว (dictionary-based)
```

The system MUST use dictionary-based word segmentation. Never segment by character.

### Classifiers (ลักษณะนาม)

Thai requires classifiers with numerals. Tag them:

```
ผู้หญิงสองคน (phûu-yǐng sǎawng khon) → "two women"
- ผู้หญิง → root: "woman"
- สอง    → root: "two"
- คน     → particle, ui_tag: "量词 人 (Classifier for People)"
```

## Script-Specific Constraints

### Tone Marks

Thai is a tonal language with 5 tones. Tone marks appear above consonants:
- ่ (mái èek) — low tone
- ้ (mái thoo) — falling tone
- ๊ (mái trii) — high tone
- ๋ (mái jàt-dtà-waa) — rising tone
- No mark — mid tone (or determined by consonant class)

These MUST remain attached to their base consonant in the original string.

### Script Family

- `script_family`: `"thai"`
- Requires Thai-specific font stack (Noto Sans Thai, Sarabun, etc.)
- Special line-height consideration for tone marks and stacked vowels

## Romanization

- **Standard**: RTGS (Royal Thai General System of Transcription)
- Tones: Include tone indicators in advanced mode
- Aspiration: ph, th, kh (aspirated) vs p, t, k (unaspirated)

## Translation Quality Checklist

- [ ] Word boundaries correctly segmented (dictionary-based, not character-based)
- [ ] Politeness particles (ครับ/ค่ะ/นะ/สิ) correctly tagged with gender
- [ ] Register reflected in translation (polite vs casual vs intimate)
- [ ] Classifiers tagged and translated with correct target-language measure words
- [ ] Tone marks preserved in original string
- [ ] Implicit subjects/topics correctly inferred
