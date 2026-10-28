# Hindi/Urdu Language Rules (hi_rules.md)

## Language Profile
- **Language**: Hindi (हिन्दी) / Urdu (اردو)
- **ISO 639-1**: `hi` (Hindi), `ur` (Urdu)
- **Script**: Devanagari (Hindi) / Arabic (Urdu)
- **Direction**: LTR (Hindi) / RTL (Urdu)
- **Morphological Type**: Fusional + some agglutination
- **Word Order**: SOV (Subject-Object-Verb)
- **Script Family**: `devanagari` (Hindi) / `arabic` (Urdu)

## Morphology Rules

### Postposition System

Hindi/Urdu uses POSTpositions (after the noun), not prepositions. This is CRITICAL for correct word order in translation:

```
मेज़ पर (mez par) → "on the table" (literally: table on)
- मेज़ → root: "table"
- पर  → particle, ui_tag: "位置标记 (Locative Postposition)"
```

**Common postpositions**:

| Postposition | ui_tag |
|-------------|--------|
| का/की/के (kā/kī/ke) | 属格 (Genitive/Of) |
| को (ko) | 宾格/与格 (Accusative/Dative) |
| ने (ne) | 作格 (Ergative) |
| से (se) | 工具格/从格/比较 (Instrumental/Ablative/Comparative) |
| में (mẽ) | 在...里 (In) |
| पर (par) | 在...上 (On) |
| तक (tak) | 直到 (Until) |
| के लिए (ke liye) | 为了 (For) |

### Gender and Number Agreement

Nouns carry inherent gender (masculine/feminine). Adjectives and verbs agree:

```
अच्छा लड़का (acchā laṛkā) → "good boy" (M.SG)
अच्छी लड़की (acchī laṛkī) → "good girl" (F.SG)
- अच्छ/ा → root + M.SG suffix
- अच्छ/ी → root + F.SG suffix
```

### Verb Structure

Hindi/Urdu verbs: Root + Auxiliary chain. The auxiliary encodes tense, aspect, mood, gender, and number:

```
मैं जा रहा हूँ (ma͠i jā rahā hū̃) → "I am going"
- मैं (ma͠i)  → root: "I"
- जा (jā)     → root: "go"
- रहा (rahā)  → suffix, ui_tag: "进行体 阳性单数 (Progressive M.SG)"
- हूँ (hū̃)   → suffix, ui_tag: "第一人称单数 现在时 (1SG.PRES)"
```

### Persian vs Sanskrit Vocabulary Balance

Hindi/Urdu can lean toward Sanskrit-derived (तत्सम/तद्भव) or Persian/Arabic-derived vocabulary. This affects register:

- **Sanskrit-leaning (Hindi)**: Formal, literary, technical
- **Persian-leaning (Urdu)**: Poetic, formal, elevated
- **Mixed (Hindustani)**: Everyday, colloquial, Bollywood

Note the vocabulary source in `usage_notes` when it affects translation register.

## Script-Specific Constraints

### Hindi (Devanagari)

- `script_family`: `"devanagari"`
- Abugida: vowel signs (matras) MUST remain attached to consonants in original
- ा, ि, ी, ु, ू, े, ै, ो, ौ — never sever from base consonant in display
- `text_direction`: `"ltr"`

### Urdu (Arabic Script)

- `script_family`: `"arabic"`
- Cursive: preserve connections in original
- `text_direction`: `"rtl"`
- Nasta'liq font preference for traditional feel

## Translation Quality Checklist

- [ ] SOV word order restructured for target language (SVO→SOV conversion)
- [ ] Postpositions converted to prepositions in target language
- [ ] Gender agreement correct in translation
- [ ] Register (Sanskrit-leaning vs Persian-leaning) reflected in translation tone
- [ ] Ergative construction (ने) correctly interpreted
- [ ] Compound verbs (verb+verb) correctly decomposed
- [ ] Matra connections preserved (Hindi) or cursive preserved (Urdu)
