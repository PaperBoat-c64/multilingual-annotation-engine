# Multilingual Annotation Engine

> Transform song lyrics from **any language** into beautifully color-aligned multilingual displays — every word aligned, every color meaningful.

A lightweight, highest-quality **lyric alignment translator** built as a [Claude Code](https://claude.com/claude-code) skill. It detects the source language, cleans noisy input, reconstructs broken lyrics, then produces word-level color-aligned translations with romanization and beginner-friendly morphological breakdowns — exported as an interactive **HTML** page and a **DOCX** document.

**Primary mission**: build the highest-quality lyric alignment translator possible.

---

## ✨ Key Features

- 🌍 **Language-agnostic, 100+ languages** — any source language → any target language, across 30+ writing systems (Latin, Arabic, Hebrew, CJK, Devanagari, Cyrillic, Thai, and more). No language is treated as the "default."
- 🎯 **Word-level semantic alignment** — every word aligned one-to-one across three rows (original / romanization / translation), linked by a shared `group_id` and a persistent color.
- 🎨 **Color mapping with a persistent lexicon** — the same semantic unit gets the same color across all rows and across sessions, enforced by a SQLite-backed color engine. Three palettes: `default`, `high-contrast`, `pastel`.
- 🧠 **Three-layer dynamic routing architecture** — a lightweight Router (language + sentiment detection) feeds a per-language rule loader, which arms a Generator for deep parsing. Token-efficient and language-specific.
- ✍️ **Three-stage translation pipeline (信达雅)** — deconstruction → cross-family syntactic reordering → fluency & polish. Designed to eliminate "translationese" and literal word-for-word glossing.
- 🌗 **First-class RTL & bidirectional support** — Arabic, Hebrew, Persian, Urdu, and every other RTL script get mirrored layouts, isolated segments (`unicode-bidi: isolate`), and correct number handling.
- 📚 **Beginner-friendly morpheme glossing** — complex words are broken into roots and affixes with plain-language UI tags (e.g. "过去时 / Past") instead of academic jargon, revealed on hover/tap.
- 🧹 **Noise recovery engine** — strips timestamps, URLs, ads, copyright notices, navigation text, OCR artifacts, smart quotes, zero-width characters, and more.
- 🔧 **Lyrics reconstruction** — repairs character-level fragmentation and detects verse/chorus/bridge structure and repeated sections.
- 🔤 **Language-specific romanization** — Pinyin, Hepburn, Revised Romanization, DIN 31635, ISO 15919, RTGS, and more — never one universal system.
- 🖥️ **Three-tab HTML interface** — Annotated (color-aligned), Reading (side-by-side prose), and Vocabulary (flashcards) tabs, with an Apple Music + DeepL inspired minimal design, dark/light mode, and responsive layout.
- 📦 **Multi-format export** — polished **HTML + DOCX** by default; Markdown on demand; plus a batch runner for directories of files.
- 🔡 **No-tofu typography** — script-appropriate font stacks (Noto Sans family) with per-script sizing, line height, and RTL font-feature settings.

---

## 🏗️ Architecture

The system uses a **three-layer dynamic routing architecture** that minimizes token consumption while maximizing parsing accuracy:

```
┌─────────────────────────────────────────────────────┐
│  Layer 1: Router Agent (Pre-processing)             │
│  Language ID + Sentiment detection                  │
│  Ultra-lightweight, structured output only          │
└──────────────────────┬──────────────────────────────┘
                       │ lang_code + sentiment
                       ▼
┌─────────────────────────────────────────────────────┐
│  Layer 2: Context Retrieval (Backend Logic)         │
│  Load per-language rule documents                   │
│  e.g., ja_rules.md, fa_rules.md, ko_rules.md       │
└──────────────────────┬──────────────────────────────┘
                       │ dynamic language rules
                       ▼
┌─────────────────────────────────────────────────────┐
│  Layer 3: Generator Agent (Core Processing)         │
│  Deep parsing with color mapping + morpheme         │
│  breakdown + sentiment-aware translation            │
│  Output: structured JSON for frontend rendering     │
└─────────────────────────────────────────────────────┘
```

1. **Router** — identifies the source language (ISO 639-1) and emotional sentiment (melancholic, energetic, romantic, …) with a minimal, structured JSON output.
2. **Context Retrieval** — loads the matching per-language rule document (`ja_rules.md`, `fa_rules.md`, `ar_rules.md`, …), each containing morphology rules, UI-tag conventions, and script-specific constraints.
3. **Generator** — performs deep linguistic parsing armed with the language rules and sentiment, emitting structured JSON with color mapping, morpheme breakdowns, and tone-aware translation.

---

## ✍️ The 信达雅 Translation Pipeline

Every line passes through a mandatory three-stage pipeline (三步翻译法) — never word-for-word literal translation:

| Stage | Purpose |
|-------|---------|
| **1 · Deconstruction** | Segment agglutinative/space-free text, deconstruct affixes, restore the core syntactic frame, and identify idioms/compounds as single units. |
| **2 · Cross-family reordering** | Reconstruct every sentence into the target language's natural grammar — fix modifier position, remap SVO/SOV/VSO order, reposition adverbials. |
| **3 · Fluency & polish (信达雅)** | Fidelity (信), expressiveness (达), and elegance (雅) — the result must read as if originally authored by a native speaker. |

A mandatory 7-question native-speaker quality loop verifies meaning accuracy, natural grammar, idiomatic phrasing, emotion, and "does it sound like lyrics, not a dictionary entry?" before any line is accepted.

---

## 🚀 Quick Start

Install the skill into Claude Code and simply ask for a translation, specifying the **target language** (it is never assumed):

```
Translate this Chinese song lyric to Spanish.

<text>
月亮代表我的心
你问我爱你有多深
我爱你有几分
</text>
```

→ Generates **HTML + DOCX** with original + pinyin + **Spanish** translation, color-aligned.

```
Translate this Persian lyric to Arabic.

<text>
خداحافظ
دل من رفت و دلم را نبرد
</text>
```

→ Generates **HTML + DOCX** with original + romanization + **Arabic** (RTL) translation.

```
Clean and translate this Japanese lyric to Russian. HTML output only.

<text>
[00:23.45] 君の名は
www.lyrics-site.com
(C) 2024 Sony Music
</text>
```

→ Noise removed → HTML with original + romanization + **Russian** translation.

The target language can be given in many forms: `Translate to French`, `한국어로 번역`, `en français`, `بالعربية`, or a code like `Target: ko`. If you don't specify one, the system asks you to choose.

---

## 🧩 How It Works

1. **Route** — detect source language + sentiment.
2. **Recover noise** — strip timestamps, URLs, ads, copyright, OCR artifacts (`noise_recovery.py`).
3. **Reconstruct** — repair fragmented text and detect structure (`lyrics_reconstructor.py`).
4. **Parse & align** — language-aware tokenization, semantic segmentation, cross-language alignment.
5. **Gloss** — beginner-friendly morpheme breakdown for complex words.
6. **Color** — assign persistent colors via the SQLite lexicon (`color_engine.py`).
7. **Export** — render interactive HTML + DOCX (`output_writer.py`).

---

## 🖥️ Three-Tab Interface

| Tab | Purpose | Layout |
|-----|---------|--------|
| 📝 **Annotated** | Word-level color-aligned display | Original → romanization → translation per line; tap/click any word for a morpheme card. |
| 📖 **Reading** | Clean prose reading experience | Two-column side-by-side original + fluent idiomatic translation. |
| 📚 **Vocabulary** | Word learning with flashcards | Responsive card grid with pronunciation, meaning, POS badge, and frequency stars; sortable and searchable. |

---

## 🌐 Supported Languages

Automatic detection covers **100+ languages** across these writing systems:

| Script | Languages | Direction |
|--------|-----------|-----------|
| Arabic | Arabic, Persian, Urdu, Pashto, Kurdish, Uyghur, Sindhi, Balochi | RTL |
| Hebrew | Hebrew, Yiddish, Ladino | RTL |
| CJK | Chinese (Simplified/Traditional), Japanese, Korean | LTR |
| Devanagari | Hindi, Marathi, Nepali, Sanskrit, and more | LTR |
| Cyrillic | Russian, Ukrainian, Bulgarian, Serbian, Mongolian, and more | LTR |
| Latin | English, French, German, Spanish, Turkish, Vietnamese, Swahili, Yoruba, and 50+ more | LTR |
| Thai / Khmer / Burmese | Thai, Lao, Khmer, Burmese, Shan, Mon | LTR |
| Indic | Bengali, Tamil, Telugu, Kannada, Malayalam, Gujarati, Punjabi, Odia, Sinhala | LTR / RTL |
| Ethiopic | Amharic, Tigrinya, Ge'ez | LTR |
| … | Greek, Georgian, Armenian, Tibetan, Mongolian | LTR |

Mixed-script documents are handled per-segment with bidirectional isolation.

---

## 📁 File Structure

```
multilingual-annotation-engine/
├── SKILL.md                     # Skill definition and full processing specification
├── scripts/
│   ├── noise_recovery.py        # Detect & remove non-lyric content
│   ├── lyrics_reconstructor.py  # Repair fragmentation, detect structure
│   ├── color_engine.py          # Persistent color assignment (SQLite lexicon)
│   ├── output_writer.py         # Export to HTML / DOCX / Markdown
│   └── batch_runner.py          # Batch processing across a directory
├── assets/
│   ├── templates/lyrics.html    # Apple Music inspired three-tab template
│   └── palettes/                # default / high-contrast / pastel
└── references/                  # Detailed specifications
    ├── language-rules/          # Per-language rules (ja, ko, zh, ar, fa, …)
    ├── script-detection.md      # Writing-system identification
    ├── romanization-systems.md  # Per-language romanization standards
    ├── alignment-rules.md       # Cross-language alignment rules
    ├── rtl-layout-engine.md     # RTL layout specification
    ├── bidirectional-text.md    # BiDi rendering rules
    ├── tokenization-engine.md   # Language-aware tokenization
    ├── morphological-analysis.md
    ├── poetry-translation.md    # 信达雅 quality standard
    ├── font-system.md           # No-tofu font stacks
    └── …
```

---

## 🎯 Design Principles

1. **Translation accuracy above all** — natural, native-quality output, judged by a native speaker of the target language.
2. **Word alignment precision** — one-to-one correspondence whenever possible.
3. **Robustness against noise** — handle broken lyrics and mixed scripts without crashing.
4. **Clean reading experience** — minimal, elegant display; Apple Music + DeepL inspired.
5. **No unnecessary features** — default mode outputs only original + romanization + translation; advanced annotations are on-demand.

---

## 📄 License

Provided as-is for educational and personal use. See the repository for any additional terms.
