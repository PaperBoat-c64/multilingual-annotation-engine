# Lyrics Structures — Detection & Reconstruction

## Table of Contents
- [Structure Types](#structure-types)
- [Verse-Chorus Detection](#verse-chorus-detection)
- [Character Fragmentation Repair](#character-fragmentation-repair)
- [Line Break Preservation](#line-break-preservation)
- [Global Structure Patterns](#global-structure-patterns)
- [Language-Specific Patterns](#language-specific-patterns)

---

## Structure Types

### Verse-Chorus (most common)
```
[Verse 1]
Lines 1-4 (often 4 lines per verse)

[Chorus]
Lines 5-8 (repeated after each verse)

[Verse 2]
Lines 9-12

[Chorus]
Lines 13-16 (same as lines 5-8)

[Bridge]
Lines 17-20

[Chorus]
Lines 21-24
```

**Detection**: Identify blocks of text that repeat with high similarity (>85%).

### Strophic (verse-only, no chorus)
```
[Verse 1]
Lines 1-4

[Verse 2]
Lines 5-8

[Verse 3]
Lines 9-12
```
Each verse same meter, different words. Common in folk, narrative songs.

### Through-Composed
No repetition. Continuous new material. Common in art songs, avant-garde.

### Refrain (verse + short repeated line)
```
[Verse 1]
Line 1
Line 2
Line 3
Refrain line ← repeated

[Verse 2]
Line 5
Line 6
Line 7
Refrain line ← repeated
```

### Bridge-Only Sections
```
[Verse]
[Bridge] ← different melody/lyrics
[Verse]
```

### Detection Algorithm

```
1. Split lines into blocks (separated by empty lines)
2. Compare blocks for similarity (SequenceMatcher ratio)
3. If two blocks ≥ 85% similar → chorus candidates
4. First chorus occurrence defines chorus line range
5. Earlier blocks → verses
6. Shorter, unique blocks → bridge/intro/outro
```

---

## Character Fragmentation Repair

### Problem
OCR and PDF extraction often produce one character per line:

```
君
の
名
は
```

### Detection
- Consecutive lines of single non-ASCII characters
- CJK characters (U+4E00-U+9FFF, U+3040-U+30FF, U+AC00-U+D7AF)
- Run length ≥ 2 characters

### Repair
1. Detect run of single-character lines
2. Join consecutive characters into one line
3. If empty line interrupts run → check if it's intentional or noise
4. Preserve runs broken by ASCII punctuation (include punctuation in join)

### When NOT to join
- Single-character lines separated by multiple empty lines
- Stylized poetry with intentional single-character lines
- Acrostic poems where each line starts a new thought
- Single-character lines that are complete words (e.g., Chinese particles: 的, 了, 吗)

### Confidence scoring
```
Run length ≥ 4 → confidence 0.95
Run length = 3 → confidence 0.85
Run length = 2 → confidence 0.70
Char is CJK ideograph → +0.05
Char is punctuation/particle → -0.10
Surrounded by multi-char lines → +0.05
```

---

## Line Break Preservation

### Intentional breaks (KEEP)
```
I wandered lonely as a cloud      ← enjambment
That floats on high o'er vales and hills
```

### Structural breaks (KEEP)
```
[Verse 1]
...
(empty line)
[Chorus]
```

### Artifact breaks (REMOVE)
```
Single-char lines ← OCR artifact
Mid-word breaks in Latin scripts ← PDF extraction artifact
```

### Heuristics for preservation
1. **Poetic enjambment**: line ends mid-phrase without punctuation → keep break
2. **End-stopped lines**: line ends with punctuation → keep break
3. **Structural separation**: empty line between verse and chorus → keep
4. **Mid-word break**: line ends with hyphen or incomplete word → join
5. **Character isolation**: single character on own line → likely artifact

---

## Global Structure Patterns

### By Genre

| Genre | Typical Structure | Line Count |
|-------|------------------|------------|
| Pop | V-C-V-C-B-C | 24-32 |
| Rock | V-C-V-C-Solo-C | 20-28 |
| Hip-Hop | V-V-V (no chorus, hook instead) | 16-48 |
| K-Pop | V-PC-C-V-PC-C-B-C | 28-40 |
| J-Pop | V-C-V-C-B-C-outro | 24-36 |
| Ballad | V-V-C-V-C-B-C | 20-28 |
| Folk | V-V-V-V (strophic) | 16-32 |
| Musical Theater | V-C-V-C-B-C-outro | 28-40 |

### By Language

| Language | Typical Lines per Section | Notes |
|----------|--------------------------|-------|
| Chinese | 4-8 lines, often 7 or 10 chars | Character-count based meter |
| Japanese | 4-8 lines | Syllable-count (5-7-5 tradition) |
| Korean | 4-8 lines | Syllable blocks |
| English | 4 lines common, 2-8 range | Syllable-stress meter |
| Arabic | 2-8 lines, couplets common | Monorhyme traditional |
| Persian | 2 lines (couplet) or 4-8 | Ghazal: 5-15 couplets |
| Hindi/Urdu | 4-8 lines | Film songs: V-C-V-C |

---

## Language-Specific Patterns

### Chinese Lyrics
- Character-based rhythm (not syllable-based)
- Common patterns: 7-char lines (七言), 5-char lines (五言)
- Modern pop: variable length, 7-12 characters per line
- Often no explicit verse/chorus markers
- Repetition detected by character sequence similarity

### Japanese Lyrics
- Mixed kanji + kana per line
- No spaces between words
- Particle は/が/を/に often ends phrases (not lines)
- J-Pop: often through-composed or verse-chorus
- Enka: strophic with 4-line verses

### Korean Lyrics
- Hangul blocks separated by spaces (modern)
- Particles attached to nouns (은/는, 이/가, 을/를)
- K-Pop: complex structure (Verse-PreChorus-Chorus-Verse-PC-Chorus-Bridge-Chorus)
- Often has English phrases mixed in

### Arabic/Persian Lyrics
- RTL script
- Poetry-based structures (qasida, ghazal)
- Couplets common (two hemistiches per line)
- Monorhyme through entire poem
- Refrain (radif) + rhyme (qafiya) system

### Hindi/Urdu Lyrics
- Film songs: 2-3 verses with recurring chorus
- Mukhda (chorus) + Antara (verse) structure
- Often 4-6 lines per section
- Rhyme scheme preserved across verses

---

## Reconstruction Output Format

```json
{
  "structure_type": "verse-chorus",
  "sections": [
    {
      "type": "verse",
      "number": 1,
      "line_start": 1,
      "line_end": 4,
      "line_count": 4
    },
    {
      "type": "chorus",
      "number": 1,
      "line_start": 5,
      "line_end": 8,
      "line_count": 4,
      "repeats": true,
      "repetition_of": null
    }
  ],
  "repetitions": [
    {
      "section_a": {"line_start": 5, "line_end": 8},
      "section_b": {"line_start": 13, "line_end": 16},
      "similarity": 0.95,
      "is_chorus_candidate": true
    }
  ],
  "total_lines": 24,
  "non_empty_lines": 20
}
```

### Key Fields
- `structure_type`: verse-chorus, strophic, through-composed, refrain
- `sections`: ordered list of detected sections
- `repetitions`: pairs of similar blocks (for chorus identification)
- `repeats`: true if this section repeats elsewhere
- `similarity`: 0.0-1.0, how similar the two blocks are
