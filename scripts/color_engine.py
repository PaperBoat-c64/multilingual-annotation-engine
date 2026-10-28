#!/usr/bin/env python3
"""
Color Engine — Persistent color assignment and lexicon management.

Assigns colors to semantic units, maintains a SQLite color lexicon
for cross-session consistency, and handles color recycling when
the palette is exhausted.

Usage:
    python color_engine.py assign --data <json> --palette <name> [--db <path>]
    python color_engine.py lookup --word <text> --lang <code> [--db <path>]
    python color_engine.py stats [--db <path>]
    python color_engine.py reset --lang <code> [--db <path>]
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Optional

# Default database location
DEFAULT_DB = Path.home() / ".claude" / "skills" / "multilingual-annotation-engine" / "color_lexicon.db"

# Built-in palettes
PALETTES = {
    "default": [
        "#E74C3C", "#2ECC71", "#3498DB", "#F39C12", "#9B59B6",
        "#1ABC9C", "#E67E22", "#2980B9", "#C0392B", "#27AE60",
        "#8E44AD", "#D35400", "#16A085", "#2C3E50", "#F1C40F",
        "#7F8C8D", "#E91E63", "#00BCD4", "#FF5722", "#795548",
        "#607D8B", "#4CAF50", "#FFC107", "#2196F3", "#9C27B0",
        "#FF9800", "#009688", "#673AB7", "#CDDC39", "#03A9F4",
    ],
    "high-contrast": [
        "#000000", "#E20000", "#006400", "#0000FF", "#8B4513",
        "#FF1493", "#008080", "#FF8C00", "#4B0082", "#B22222",
        "#006400", "#000080", "#A0522D", "#C71585", "#2F4F4F",
        "#D2691E", "#800080", "#8B0000", "#004D00", "#0000CD",
        "#654321", "#DB7093", "#006666", "#CC5500", "#663399",
        "#A52A2A", "#1B5E20", "#1A237E", "#BF360C", "#4A148C",
    ],
    "pastel": [
        "#F8B4B4", "#B4E6B4", "#B4C8F8", "#F8E4B4", "#D8B4F8",
        "#B4F0E4", "#F8D0B4", "#B4D4F8", "#F0B4B4", "#B4F0B4",
        "#D0B4F0", "#F8C8B4", "#B4E8D8", "#D4D8E0", "#F8F0B4",
        "#E0D8D0", "#F8B4D0", "#B4E8F8", "#F8CCB4", "#D0C8C0",
        "#C8D0D8", "#B4F0C8", "#F8E8B4", "#B4D8F8", "#D8B4E8",
        "#F8D4B4", "#B4E8CC", "#C8B4E8", "#E8F0B4", "#B4E4F8",
    ],
}

# ANSI color-blind-friendly 15-color palette (Okabe-Ito inspired, extended)
COLORBLIND_SAFE = [
    "#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9",
    "#F0E442", "#D55E00", "#000000", "#882255", "#AA4499",
    "#332288", "#117733", "#44AA99", "#88CCEE", "#DDCC77",
]


def get_db(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Open (or create) the color lexicon database."""
    path = db_path or str(DEFAULT_DB)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lexicon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language_code TEXT NOT NULL,
            normalized_form TEXT NOT NULL,
            color_hex TEXT NOT NULL,
            frequency INTEGER DEFAULT 1,
            first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(language_code, normalized_form)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS palette_state (
            palette_name TEXT PRIMARY KEY,
            next_index INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn


def load_palette(name: str) -> list[str]:
    """Load a palette by name. Falls back to 'default' if not found."""
    return PALETTES.get(name, PALETTES["default"])


def assign_color(
    conn: sqlite3.Connection,
    word: str,
    lang: str,
    palette_name: str = "default",
) -> dict:
    """
    Assign a color to a word. Returns existing color if word is known,
    otherwise assigns the next available color from the palette.
    """
    # Normalize input
    import unicodedata
    normalized = unicodedata.normalize("NFKC", word.strip())

    # Check if already in lexicon
    cursor = conn.execute(
        "SELECT color_hex, frequency FROM lexicon WHERE language_code = ? AND normalized_form = ?",
        (lang, normalized),
    )
    row = cursor.fetchone()

    if row:
        # Word exists — increment frequency and return existing color
        conn.execute(
            "UPDATE lexicon SET frequency = frequency + 1, last_seen_at = CURRENT_TIMESTAMP WHERE language_code = ? AND normalized_form = ?",
            (lang, normalized),
        )
        conn.commit()
        return {
            "word": word,
            "normalized": normalized,
            "language": lang,
            "color": row[0],
            "frequency": row[1] + 1,
            "is_new": False,
        }

    # New word — assign next palette color
    palette = load_palette(palette_name)

    # Get current palette index
    cursor = conn.execute(
        "SELECT next_index FROM palette_state WHERE palette_name = ?", (palette_name,)
    )
    state_row = cursor.fetchone()

    if state_row is None:
        next_index = 0
        conn.execute(
            "INSERT INTO palette_state (palette_name, next_index) VALUES (?, 0)",
            (palette_name,),
        )
    else:
        next_index = state_row[0]

    # Assign color (with recycling if exhausted)
    color = palette[next_index % len(palette)]

    # Advance index
    conn.execute(
        "UPDATE palette_state SET next_index = ? WHERE palette_name = ?",
        (next_index + 1, palette_name),
    )

    # Store in lexicon
    conn.execute(
        "INSERT INTO lexicon (language_code, normalized_form, color_hex) VALUES (?, ?, ?)",
        (lang, normalized, color),
    )
    conn.commit()

    return {
        "word": word,
        "normalized": normalized,
        "language": lang,
        "color": color,
        "frequency": 1,
        "is_new": True,
    }


def assign_batch(
    conn: sqlite3.Connection,
    units: list[dict],
    palette_name: str = "default",
) -> list[dict]:
    """
    Assign colors to a batch of semantic units.

    Each unit should be:
        {"word": "...", "lang": "fa", "semantic_group_id": "..."}

    Words with the same semantic_group_id receive the same color.
    Returns the input list with "color" and "is_new" fields added.
    """
    # Group by semantic_group_id — all words in same group get same color
    group_colors: dict[str, str] = {}
    results = []

    for unit in units:
        group_id = unit.get("semantic_group_id", unit["word"])
        lang = unit.get("lang", "unknown")

        if group_id in group_colors:
            # Already assigned for this group — look up and reuse
            color_info = assign_color(conn, unit["word"], lang, palette_name)
            color_info["color"] = group_colors[group_id]
            results.append(color_info)
        else:
            # First occurrence — assign color and record for group
            color_info = assign_color(conn, unit["word"], lang, palette_name)
            group_colors[group_id] = color_info["color"]
            results.append(color_info)

    return results


def lookup_word(conn: sqlite3.Connection, word: str, lang: str) -> Optional[dict]:
    """Look up a word in the lexicon."""
    import unicodedata
    normalized = unicodedata.normalize("NFKC", word.strip())
    cursor = conn.execute(
        "SELECT color_hex, frequency, first_seen_at, last_seen_at FROM lexicon WHERE language_code = ? AND normalized_form = ?",
        (lang, normalized),
    )
    row = cursor.fetchone()
    if row:
        return {
            "word": word,
            "normalized": normalized,
            "language": lang,
            "color": row[0],
            "frequency": row[1],
            "first_seen": row[2],
            "last_seen": row[3],
        }
    return None


def get_stats(conn: sqlite3.Connection) -> dict:
    """Get lexicon statistics."""
    total = conn.execute("SELECT COUNT(*) FROM lexicon").fetchone()[0]
    by_lang = conn.execute(
        "SELECT language_code, COUNT(*), SUM(frequency) FROM lexicon GROUP BY language_code"
    ).fetchall()
    top_words = conn.execute(
        "SELECT language_code, normalized_form, color_hex, frequency FROM lexicon ORDER BY frequency DESC LIMIT 20"
    ).fetchall()
    return {
        "total_entries": total,
        "by_language": [
            {"lang": row[0], "unique_words": row[1], "total_occurrences": row[2]}
            for row in by_lang
        ],
        "top_words": [
            {"lang": row[0], "word": row[1], "color": row[2], "frequency": row[3]}
            for row in top_words
        ],
    }


def reset_language(conn: sqlite3.Connection, lang: str) -> int:
    """Reset lexicon entries for a specific language. Returns count of deleted rows."""
    cursor = conn.execute("DELETE FROM lexicon WHERE language_code = ?", (lang,))
    conn.commit()
    return cursor.rowcount


def main():
    parser = argparse.ArgumentParser(description="Color Engine for Multilingual Annotation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Assign command
    assign_parser = subparsers.add_parser("assign", help="Assign colors to semantic units")
    assign_parser.add_argument("--data", required=True, help="JSON array of semantic units")
    assign_parser.add_argument("--palette", default="default", help="Palette name")
    assign_parser.add_argument("--db", default=None, help="Database path")

    # Lookup command
    lookup_parser = subparsers.add_parser("lookup", help="Look up a word in the lexicon")
    lookup_parser.add_argument("--word", required=True, help="Word to look up")
    lookup_parser.add_argument("--lang", required=True, help="Language code")
    lookup_parser.add_argument("--db", default=None, help="Database path")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show lexicon statistics")
    stats_parser.add_argument("--db", default=None, help="Database path")

    # Reset command
    reset_parser = subparsers.add_parser("reset", help="Reset lexicon for a language")
    reset_parser.add_argument("--lang", required=True, help="Language code to reset")
    reset_parser.add_argument("--db", default=None, help="Database path")

    args = parser.parse_args()

    try:
        conn = get_db(args.db)

        if args.command == "assign":
            units = json.loads(args.data)
            results = assign_batch(conn, units, args.palette)
            print(json.dumps(results, ensure_ascii=False, indent=2))

        elif args.command == "lookup":
            result = lookup_word(conn, args.word, args.lang)
            if result:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(json.dumps({"found": False, "word": args.word, "lang": args.lang}))

        elif args.command == "stats":
            stats = get_stats(conn)
            print(json.dumps(stats, ensure_ascii=False, indent=2))

        elif args.command == "reset":
            count = reset_language(conn, args.lang)
            print(json.dumps({"deleted": count, "language": args.lang}))

    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
    finally:
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    main()
