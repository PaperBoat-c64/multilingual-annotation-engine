#!/usr/bin/env python3
"""
Noise Recovery Engine — Detect and remove non-lyric content from raw input.

Handles:
- Timestamps (LRC, SRT, bracketed, parenthetical)
- URLs and domains
- Advertisements and promotional text
- Copyright notices
- Navigation text and breadcrumbs
- HTML/XML comments and code comments
- Metadata headers (Artist:, Album:, etc.)
- OCR noise (extra spaces, artifacts, fragmented characters)
- Empty/whitespace lines
- HTML tags and entities
- Page numbers
- Social media handles
- Smart/curly quotes → straight quotes
- Zero-width characters and BOM

Usage:
    python noise_recovery.py clean --input "raw_text" --output clean.json
    python noise_recovery.py clean --file input.txt --output clean.json
    python noise_recovery.py detect --input "raw_text"
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Optional


# ============================================================
#  Noise Pattern Definitions
# ============================================================

# Timestamps: [00:23.45], (3:15), <00:23>, {04:15}, 01:59.999
RE_TIMESTAMP = re.compile(
    r'[\[<\({]?\d{1,3}:\d{2}(?:[:.]\d{2,3})?[\]>\)} ]?'
    r'(?:\s*[-–—]\s*[\[<\({]?\d{1,3}:\d{2}(?:[:.]\d{2,3})?[\]>\)}]?)?'
)

# Lines that are ONLY a timestamp
RE_TIMESTAMP_LINE = re.compile(
    r'^\s*[\[<\({]?\d{1,3}:\d{2}(?:[:.]\d{2,3})?[\]>\)} ]?\s*$'
)

# LRC format: [mm:ss.xx]lyric text
RE_LRC_LINE = re.compile(r'^\[(\d{2}):(\d{2})\.(\d{2,3})\](.*)')

# URLs
RE_URL = re.compile(
    r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.(?:com|net|org|io|co|ly|us|me|xyz|info|biz)'
    r'(?:/[^\s]*)?',
    re.IGNORECASE,
)

# Copyright notices
RE_COPYRIGHT = re.compile(
    r'(?:ⓒ|Ⓒ|©|\(C\)|\(c\)|Copyright\s*©?|Copr\.)\s*\d{4}?\s*[^\n]*',
    re.IGNORECASE,
)
RE_ALL_RIGHTS = re.compile(r'All\s+Rights?\s+Reserved\.?', re.IGNORECASE)

# HTML/XML tags and entities
RE_HTML_TAG = re.compile(r'<[^>]+>')
RE_HTML_ENTITY = re.compile(r'&[a-zA-Z]+;|&#\d+;|&#x[0-9a-fA-F]+;')
RE_CODE_COMMENT = re.compile(
    r'^\s*(?://|#|--|/\*|\*|<!--).*$',
    re.MULTILINE,
)

# Metadata headers
RE_METADATA_LINE = re.compile(
    r'^\s*(?:Artist|Title|Album|Year|Track|Genre|Composer|Lyricist|Writer|Producer|Label|'
    r'Released?|Recorded?|Mixed?|Mastered?|Featuring?|Feat\.?|Ft\.?)\s*[:：]\s*',
    re.IGNORECASE,
)

# Page numbers
RE_PAGE_NUMBER = re.compile(
    r'^\s*(?:Page\s*\d+|\d+\s*of\s*\d+|—\s*\d+\s*—|-\s*\d+\s*-)\s*$',
    re.IGNORECASE,
)

# Social media handles
RE_SOCIAL_HANDLE = re.compile(r'@[a-zA-Z0-9_]{1,15}')
RE_HASHTAG = re.compile(r'#[a-zA-Z0-9_-￿]+')

# Ad/promotional keywords
AD_KEYWORDS = [
    r'download\s+(?:our\s+)?app',
    r'click\s+here',
    r'subscribe\s+(?:now|today)',
    r'visit\s+(?:our\s+)?(?:website|site)',
    r'follow\s+(?:us|me)\s+on',
    r'share\s+(?:this|with)',
    r'buy\s+(?:now|today|online)',
    r'premium\s+(?:access|account|member)',
    r'sign\s+up\s+(?:now|today|free)',
    r'advertisement|sponsored\s+content|promoted\s+by',
    r'ringtone|wallpaper|merch(?:andise)?',
    r'listen\s+on\s+(?:spotify|apple\s+music|youtube|amazon)',
]
RE_AD = re.compile('|'.join(AD_KEYWORDS), re.IGNORECASE)

# Navigation/breadcrumb text
NAV_PATTERNS = [
    r'^(?:back|next|previous|home|top|menu|search|browse)\s*(?:>>|→|»|>|to)?\s*$',
    r'^(?:<<|←|«|<)\s*(?:back|previous|prev)\s*$',
    r'^[A-Z][a-z]+(?:\s*[>→»]\s*[A-Z][a-z]+)+$',  # Breadcrumb: Home > Lyrics > Song
]
RE_NAV = re.compile('|'.join(NAV_PATTERNS), re.IGNORECASE)

# Empty/whitespace-only lines
RE_EMPTY_LINE = re.compile(r'^\s*$')

# Smart/curly quotes
SMART_QUOTE_MAP = {
    '‘': "'",  # ' left single
    '’': "'",  # ' right single
    '“': '"',  # " left double
    '”': '"',  # " right double
    '‚': "'",  # ‚ single low-9
    '„': '"',  # „ double low-9
    '«': '"',  # « left double angle
    '»': '"',  # » right double angle
    '‹': "'",  # ‹ single left angle
    '›': "'",  # › single right angle
}

# Zero-width and invisible characters to strip
ZERO_WIDTH_CHARS = {
    '​',  # ZERO WIDTH SPACE
    '‌',  # ZERO WIDTH NON-JOINER
    '‍',  # ZERO WIDTH JOINER
    '‎',  # LEFT-TO-RIGHT MARK
    '‏',  # RIGHT-TO-LEFT MARK
    ' ',  # LINE SEPARATOR
    ' ',  # PARAGRAPH SEPARATOR
    '‪',  # LEFT-TO-RIGHT EMBEDDING
    '‫',  # RIGHT-TO-LEFT EMBEDDING
    '‬',  # POP DIRECTIONAL FORMATTING
    '‭',  # LEFT-TO-RIGHT OVERRIDE
    '‮',  # RIGHT-TO-LEFT OVERRIDE
    '⁠',  # WORD JOINER
    '⁡',  # FUNCTION APPLICATION
    '⁢',  # INVISIBLE TIMES
    '⁣',  # INVISIBLE SEPARATOR
    '⁤',  # INVISIBLE PLUS
    '﻿',  # ZERO WIDTH NO-BREAK SPACE (BOM)
    '￾',  # BYTE ORDER MARK (reversed)
    '⁦',  # LEFT-TO-RIGHT ISOLATE
    '⁧',  # RIGHT-TO-LEFT ISOLATE
    '⁨',  # FIRST STRONG ISOLATE
    '⁩',  # POP DIRECTIONAL ISOLATE
}


def normalize_text(text: str) -> str:
    """Normalize text: NFKC, strip zero-width chars, normalize quotes."""
    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # Strip zero-width characters
    for ch in ZERO_WIDTH_CHARS:
        text = text.replace(ch, "")

    # Normalize smart quotes to straight quotes
    for smart, straight in SMART_QUOTE_MAP.items():
        text = text.replace(smart, straight)

    return text


def detect_noise_items(text: str) -> list[dict]:
    """
    Detect all noise items in text.
    Returns list of {type, text, line_number, confidence}.
    """
    items = []
    lines = text.split("\n")

    for i, line in enumerate(lines):
        line_number = i + 1
        stripped = line.strip()

        # Empty lines
        if RE_EMPTY_LINE.match(stripped):
            items.append({
                "type": "empty_line",
                "text": line,
                "line_number": line_number,
                "confidence": 1.0,
            })
            continue

        # Timestamp-only lines
        if RE_TIMESTAMP_LINE.match(stripped):
            items.append({
                "type": "timestamp_line",
                "text": stripped,
                "line_number": line_number,
                "confidence": 0.95,
            })
            continue

        # LRC timestamp prefix
        lrc_match = RE_LRC_LINE.match(stripped)
        if lrc_match:
            # Groups 1-3 capture the timestamp: mm, ss, xx
            # Build the full timestamp including brackets
            full_ts = f"[{lrc_match.group(1)}:{lrc_match.group(2)}.{lrc_match.group(3)}]"
            lyric_part = lrc_match.group(4).strip()
            if lyric_part:
                # Line has both timestamp and lyric — strip timestamp only
                items.append({
                    "type": "lrc_timestamp",
                    "text": full_ts,
                    "line_number": line_number,
                    "confidence": 0.95,
                })
            else:
                items.append({
                    "type": "timestamp_line",
                    "text": stripped,
                    "line_number": line_number,
                    "confidence": 0.95,
                })
                continue

        # URLs
        url_matches = RE_URL.findall(stripped)
        for url in url_matches:
            items.append({
                "type": "url",
                "text": url,
                "line_number": line_number,
                "confidence": 0.9,
            })

        # Copyright notices
        if RE_COPYRIGHT.search(stripped):
            items.append({
                "type": "copyright",
                "text": stripped,
                "line_number": line_number,
                "confidence": 0.9,
            })
            continue

        if RE_ALL_RIGHTS.search(stripped):
            items.append({
                "type": "copyright",
                "text": stripped,
                "line_number": line_number,
                "confidence": 0.85,
            })
            continue

        # HTML tags (lines that are mostly HTML)
        if RE_HTML_TAG.search(stripped):
            tags = RE_HTML_TAG.findall(stripped)
            # If the line is mostly HTML tags, flag it
            tag_chars = sum(len(t) for t in tags)
            if tag_chars > len(stripped) * 0.5:
                items.append({
                    "type": "html_markup",
                    "text": stripped,
                    "line_number": line_number,
                    "confidence": 0.85,
                })
                continue

        # Code comments
        if RE_CODE_COMMENT.match(stripped):
            items.append({
                "type": "code_comment",
                "text": stripped,
                "line_number": line_number,
                "confidence": 0.8,
            })
            continue

        # Metadata headers
        if RE_METADATA_LINE.match(stripped):
            items.append({
                "type": "metadata",
                "text": stripped,
                "line_number": line_number,
                "confidence": 0.85,
            })
            continue

        # Page numbers
        if RE_PAGE_NUMBER.match(stripped):
            items.append({
                "type": "page_number",
                "text": stripped,
                "line_number": line_number,
                "confidence": 0.9,
            })
            continue

        # Social media handles / hashtags (only if the line is mostly that)
        handles = RE_SOCIAL_HANDLE.findall(stripped)
        hashtags = RE_HASHTAG.findall(stripped)
        social_text = " ".join(handles + hashtags)
        if social_text and len(social_text) > len(stripped) * 0.5:
            items.append({
                "type": "social_media",
                "text": stripped,
                "line_number": line_number,
                "confidence": 0.8,
            })
            continue

        # Advertisements
        if RE_AD.search(stripped):
            items.append({
                "type": "advertisement",
                "text": stripped,
                "line_number": line_number,
                "confidence": 0.75,
            })
            continue

        # Navigation text
        if RE_NAV.match(stripped):
            items.append({
                "type": "navigation",
                "text": stripped,
                "line_number": line_number,
                "confidence": 0.8,
            })
            continue

    return items


def remove_noise(text: str) -> dict:
    """
    Remove all detected noise from text.
    Returns {"clean_text": str, "noise_items": list, "stats": dict}.
    """
    # First, normalize
    text = normalize_text(text)

    # Detect noise items
    noise_items = detect_noise_items(text)

    # Build set of line numbers to remove (or partial cleaning)
    noise_line_numbers = set()
    lrc_timestamps = {}  # line_number → timestamp_prefix

    for item in noise_items:
        if item["type"] in (
            "empty_line", "timestamp_line", "copyright", "html_markup",
            "code_comment", "metadata", "page_number", "social_media",
            "advertisement", "navigation",
        ):
            noise_line_numbers.add(item["line_number"])
        elif item["type"] == "lrc_timestamp":
            lrc_timestamps[item["line_number"]] = item["text"]
        elif item["type"] == "url":
            # URL removal is handled inline (remove the URL from the line)
            pass

    # Build clean lines
    lines = text.split("\n")
    clean_lines = []
    removed_count = 0

    for i, line in enumerate(lines):
        line_number = i + 1

        # Skip fully noisy lines
        if line_number in noise_line_numbers:
            removed_count += 1
            continue

        cleaned = line

        # Strip LRC timestamps
        if line_number in lrc_timestamps:
            ts = lrc_timestamps[line_number]
            cleaned = cleaned.replace(ts, "").strip()

        # Remove URLs inline
        cleaned = RE_URL.sub("", cleaned).strip()

        # Remove HTML tags and entities from kept lines
        cleaned = RE_HTML_TAG.sub("", cleaned)
        cleaned = RE_HTML_ENTITY.sub("", cleaned)

        # Remove social handles from kept lines
        cleaned = RE_SOCIAL_HANDLE.sub("", cleaned)
        cleaned = RE_HASHTAG.sub("", cleaned)

        # Remove inline timestamps from kept lines
        cleaned = RE_TIMESTAMP.sub("", cleaned)

        # Collapse multiple spaces
        cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()

        if cleaned:
            clean_lines.append(cleaned)

    clean_text = "\n".join(clean_lines)

    # Statistics
    stats = {
        "original_lines": len(lines),
        "clean_lines": len(clean_lines),
        "lines_removed": removed_count,
        "noise_items_detected": len(noise_items),
        "noise_by_type": {},
        "recovery_rate": round(len(clean_lines) / max(len(lines), 1) * 100, 1),
    }

    for item in noise_items:
        t = item["type"]
        stats["noise_by_type"][t] = stats["noise_by_type"].get(t, 0) + 1

    return {
        "clean_text": clean_text,
        "noise_items": noise_items,
        "stats": stats,
    }


def detect_ocr_fragmentation(text: str) -> list[dict]:
    """
    Detect lines that appear to be OCR-fragmented (single characters on their own line).
    Returns list of fragmentation candidates.
    """
    lines = text.strip().split("\n")
    candidates = []

    # Look for runs of single-character lines
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if len(line) == 1 and not line.isascii():
            # Found a single non-ASCII character — check for a run
            run_start = i
            while i < len(lines) and len(lines[i].strip()) <= 2 and lines[i].strip():
                i += 1
            run_end = i
            run_length = run_end - run_start
            if run_length >= 2:
                # Collect the run of characters
                chars = [lines[j].strip() for j in range(run_start, run_end)]
                candidates.append({
                    "type": "ocr_fragmented",
                    "line_start": run_start + 1,
                    "line_end": run_end,
                    "characters": chars,
                    "reconstructed": "".join(chars),
                    "confidence": min(0.9, 0.5 + run_length * 0.1),
                })
        else:
            i += 1

    return candidates


def main():
    parser = argparse.ArgumentParser(
        description="Noise Recovery Engine — Clean polluted lyric input"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # clean command
    clean_parser = subparsers.add_parser("clean", help="Clean noise from text")
    clean_parser.add_argument("--input", default=None, help="Raw text string")
    clean_parser.add_argument("--file", default=None, help="Input file path")
    clean_parser.add_argument("--output", required=True, help="Output JSON file path")

    # detect command
    detect_parser = subparsers.add_parser("detect", help="Detect noise items only")
    detect_parser.add_argument("--input", default=None, help="Raw text string")
    detect_parser.add_argument("--file", default=None, help="Input file path")

    # detect-ocr command
    ocr_parser = subparsers.add_parser("detect-ocr", help="Detect OCR fragmentation only")
    ocr_parser.add_argument("--input", default=None, help="Raw text string")
    ocr_parser.add_argument("--file", default=None, help="Input file path")

    args = parser.parse_args()

    try:
        # Resolve input text
        if args.file:
            text = Path(args.file).read_text(encoding="utf-8")
        elif hasattr(args, "input") and args.input:
            text = args.input
        else:
            print(json.dumps({"error": "Either --input or --file is required"}), file=sys.stderr)
            sys.exit(1)

        if args.command == "clean":
            result = remove_noise(text)
            # Also detect OCR fragmentation
            ocr_candidates = detect_ocr_fragmentation(result["clean_text"])
            result["ocr_fragments"] = ocr_candidates
            result["has_ocr_issues"] = len(ocr_candidates) > 0

            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
            print(json.dumps({
                "status": "ok",
                "output": str(output_path.resolve()),
                "stats": result["stats"],
                "ocr_fragments_found": len(ocr_candidates),
            }, ensure_ascii=False))

        elif args.command == "detect":
            noise_items = detect_noise_items(text)
            print(json.dumps({
                "noise_items": noise_items,
                "count": len(noise_items),
            }, ensure_ascii=False, indent=2))

        elif args.command == "detect-ocr":
            fragments = detect_ocr_fragmentation(text)
            print(json.dumps({
                "fragments": fragments,
                "count": len(fragments),
            }, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
