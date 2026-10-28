# German Language Rules (de_rules.md)

## Language Profile
- **Language**: German (Deutsch)
- **ISO 639-1**: `de`
- **Script**: Latin
- **Direction**: LTR
- **Morphological Type**: Fusional
- **Word Order**: V2 (main clauses), SOV (subordinate clauses)
- **Script Family**: `latin`

## Morphology Rules

### Separable Prefix Verbs

German separable prefixes detach and move to the end of the clause. The prefix and stem form ONE word in the infinitive but split in usage:

```
ankommen → kam ... an "arrived"
- an   → prefix, ui_tag: "分离前缀 (Separable Prefix)"
- komm → root: "come"

ausgegangen → "gone out"
- aus  → prefix, ui_tag: "分离前缀 (Separable Prefix)"
- ge   → prefix, ui_tag: "过去分词标记 (Past Participle Mark)"
- gang → root: "go"
- en   → suffix, ui_tag: "动词后缀 (Verb Suffix)"
```

### Compound Noun Decomposition

German compound nouns MUST be decomposed into constituent parts:

```
Donaudampfschifffahrtsgesellschaft → "Danube steamship travel company"
- Donau      → root: "Danube (river)"
- Dampf      → root: "steam"
- Schiff     → root: "ship"
- Fahrt      → root: "travel"
- Gesellschaft → root: "company"
Note: This is ONE segment in the original row. Decompose in morphemes[].
```

### Case System (4 Cases)

| Case | Marker Examples | ui_tag |
|------|----------------|--------|
| Nominative | der, die, das, ein, eine | 主格 (Nominative) |
| Accusative | den, die, das, einen | 宾格 (Accusative) |
| Dative | dem, der, dem, einem | 与格 (Dative) |
| Genitive | des, der, des, eines | 属格 (Genitive) |

### Article Decomposition

German articles encode case, number, and gender. Tag them fully:

```
dem Mann → "to the man"
- dem  → particle, ui_tag: "定冠词 阳性单数 与格 (Def.Art M.SG.DAT)"
- Mann → root: "man"
```

## Syntax Rules

### V2 Word Order (Main Clauses)

The finite verb MUST be in second position. Translation to SVO languages requires restructuring:

```
Heute gehe ich nach Hause.
│      │    │  │
Today  go   I  home.
→ Natural English: "Today I'm going home."
```

### Verb-Final (Subordinate Clauses)

In subordinate clauses, the verb goes to the end:

```
..., weil ich nach Hause gehe.
        │            │       │
        because I    home    go
→ Natural English: "...because I'm going home."
```

### Verb Position in Translation

**CRITICAL**: Restructure German verb placement to natural target-language order:
- Main clause V2 → natural target-language SVO/SOV
- Subordinate clause SOV → natural target-language order
- Never preserve German verb position in translation

## Translation Quality Checklist

- [ ] Separable prefix verbs correctly decomposed
- [ ] Compound nouns decomposed into constituent parts
- [ ] Case (nominative/accusative/dative/genitive) correctly tagged on articles
- [ ] Gender (masculine/feminine/neuter) correctly tagged
- [ ] V2 word order restructured to natural target-language order
- [ ] Subordinate clause verb-final order restructured
- [ ] Verb position natural in target language
