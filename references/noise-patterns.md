# Noise Patterns — Detection & Recovery

## Table of Contents
- [Timestamp Patterns](#timestamp-patterns)
- [URL & Domain Patterns](#url--domain-patterns)
- [Copyright & Legal Notices](#copyright--legal-notices)
- [Metadata Headers](#metadata-headers)
- [Advertisement Patterns](#advertisement-patterns)
- [Navigation & UI Text](#navigation--ui-text)
- [OCR Artifacts](#ocr-artifacts)
- [HTML & Markup Noise](#html--markup-noise)
- [Social Media Noise](#social-media-noise)
- [Recovery Strategy](#recovery-strategy)

---

## Timestamp Patterns

### LRC Format (most common in lyrics)
```
[00:23.45]Lyric text here
[01:15.00]Another line
```
- Pattern: `[mm:ss.xx]` or `[mm:ss.xxx]`
- Timestamp is at line start
- LRC may also have: `<mm:ss.xx>`, `{mm:ss.xx}`

### SRT/Subtitle Format
```
1
00:00:23,450 --> 00:00:26,780
Lyric text here
```
- Number + time range + text
- Time format: `HH:MM:SS,mmm`

### Inline Timestamps
```
(3:15) 君の名は
01:59 让我爱你
```
- Timestamp embedded within lyric text
- Usually at line start, sometimes inline

### Detection Strategy
1. Check if line starts with timestamp pattern → strip prefix
2. If entire line is a timestamp → remove line
3. If timestamp is inline → remove timestamp portion, keep text

---

## URL & Domain Patterns

### Common Patterns
```
https://www.lyrics-site.com/song/123
www.azlyrics.com
lyricsmode.com/artist/song
```

### Lyrics Site Domains (known noise sources)
- azlyrics.com, genius.com, musixmatch.com
- lyricstranslate.com, lyricsmode.com, metrolyrics.com
- j-lyric.net, uta-net.com (Japanese)
- mojim.com (Chinese)

### Detection Strategy
1. URL with protocol → always noise
2. Bare domain → check if it's a known lyrics site
3. Domain followed by path → likely noise
4. Edge case: artist names that look like domains → flag for Claude review

---

## Copyright & Legal Notices

### Patterns
```
© 2024 Sony Music Entertainment
(C) Warner Music Group
Ⓒ All Rights Reserved
Copyright Universal Music
Copr. 2023
```

### Additional Legal Text
```
All Rights Reserved. Unauthorized reproduction is prohibited.
Lyrics licensed by Music Publisher
Used by permission. All rights reserved.
```

### Detection Strategy
1. Lines containing ©, Ⓒ, (C), Copyright → always noise
2. "All Rights Reserved" → always noise
3. Lines about licensing/usage rights → noise
4. Edge case: "rights" in lyric context ("you have the rights to my heart") → Claude review

---

## Metadata Headers

### Common Headers
```
Artist: 周杰伦
Title: 七里香
Album: 依然范特西
Year: 2006
Track: 3
Genre: Pop
Composer: Jay Chou
Lyricist: Fang Wenshan
Producer: Jay Chou
Label: JVR Music
Released: September 5, 2006
Feat.: 费玉清
```

### Detection Strategy
1. Line matches `Key: Value` pattern with known keys → noise
2. Keys in English, Chinese, Japanese, Korean, etc.
3. Multiple metadata lines in sequence → remove entire block
4. Edge case: "Title:" or "Name:" in dialog lyrics → Claude review

---

## Advertisement Patterns

### Common Ads in Lyrics Sites
```
Download our app for offline lyrics!
Click here to listen on Spotify
Subscribe now for ad-free experience
Visit our website for more lyrics
Follow us on Instagram @lyricsdaily
Share this lyric with friends!
Buy this song on iTunes
Premium members get HD lyrics
```

### Ringtone/Merch Promotions
```
Get this ringtone! Text SONG to 12345
Buy official merch at store.artist.com
Wallpaper available at fan-site.com
```

### Detection Strategy
1. Imperative verbs (download, click, subscribe, visit, buy, get, follow, share) + service name → noise
2. Promotional language + URL → noise
3. Ringtone codes (Text XXXX to NNNNN) → noise
4. Edge case: "follow" in lyric context ("follow me", "follow your heart") → Claude review

---

## Navigation & UI Text

### Patterns
```
Back to top ↑
Next →
← Previous
Home > Lyrics > Artist > Song
Search results for "lyric query"
Browse by artist
Related lyrics:
You might also like:
```

### Detection Strategy
1. Single word + arrow symbol → noise
2. Breadcrumb paths (Text > Text > Text) → noise
3. UI labels (Search, Browse, Related, Next, Previous) → noise
4. Edge case: arrows/directions in lyric context → Claude review

---

## OCR Artifacts

### Character Fragmentation
```
君
の
名
は
```
→ Each character extracted as a separate text block

### Space Insertion
```
君 の 名 は
```
→ Spaces inserted between every character

### Recognition Errors
```
曰 (sun) instead of 日 (day)
己 (self) instead of 已 (already)
```
→ Similar-looking characters confused

### Mixed Encoding Artifacts
```
å››å­£ (garbled UTF-8 interpreted as Latin-1)
```
→ Encoding mismatch produces mojibake

### Detection Strategy
1. Consecutive single-character non-Latin lines → fragmentation, join them
2. Abnormally many spaces between CJK characters → strip extra spaces
3. Lines with mostly replacement characters (�) → flag for manual review
4. Mojibake patterns → attempt encoding recovery or flag

---

## HTML & Markup Noise

### HTML Tags
```html
<br>, <br/>, <br />
<div class="lyric">, </div>
<span>, <p>, <a href="...">
```

### HTML Entities
```
&nbsp; &amp; &lt; &gt; &quot; &apos;
&#9733; &#x2605;
```

### Code Comments
```
<!-- lyrics start -->
/* chorus */
// verse 1
# bridge section
```

### Inline Styles
```
<span style="color: red">lyric</span>
<div id="chorus">
```

### Detection Strategy
1. Strip all HTML tags → keep text content
2. Decode HTML entities → convert to characters
3. Remove lines that are purely markup/comments
4. Lines that are >50% markup by character count → remove

---

## Social Media Noise

### Patterns
```
@lyrics_share
#ThrowbackThursday
#music
Follow @artistname
```

### Detection Strategy
1. @handle at end or beginning of lyric line → strip handle
2. Line consisting only of handles and hashtags → remove
3. Hashtags in lyric context ("#blessed", "#love") → Claude review

---

## Recovery Strategy

### Pipeline Order
1. **Normalize** — NFKC normalization, strip zero-width chars, normalize quotes
2. **Remove structural noise** — empty lines, markup, comments, metadata
3. **Remove content noise** — URLs, ads, copyright, social media
4. **Clean remaining** — strip timestamps, decode entities
5. **Reconstruct** — join fragmented characters, normalize spacing
6. **Validate** — check that cleaned text is plausible lyrics

### Confidence Levels
| Confidence | Action |
|-----------|--------|
| 0.95-1.0 | Automatic removal |
| 0.80-0.94 | Remove, flag for info |
| 0.60-0.79 | Flag for Claude review |
| < 0.60 | Keep, mark as uncertain |

### Handling Ambiguous Cases
When noise detection is uncertain:
1. Flag the item with confidence score
2. Present both options (keep vs remove) to Claude
3. Claude makes final decision based on context
4. Never silently remove low-confidence matches

### Safety Rules
- **Never** remove content that could be lyrics
- **Always** err on the side of keeping text
- When in doubt, flag for Claude review
- If >30% of input is classified as noise → likely a systemic issue, stop and report
