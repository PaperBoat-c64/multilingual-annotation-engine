#!/usr/bin/env python3
"""
Lyrics Reconstructor — Repair broken lyrics and detect song structure.

Handles:
- Character-level fragmentation repair (OCR/PDF extraction artifacts)
- Verse/Chorus/Bridge structure detection
- Repeated section identification (chorus detection)
- Intentional line break preservation
- Empty line normalization

Usage:
    python lyrics_reconstructor.py reconstruct --input clean.json --output reconstructed.json
    python lyrics_reconstructor.py detect-structure --input "lyric text"
    python lyrics_reconstructor.py repair --input "fragmented text"
"""

import argparse
import json
import re
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional


# ============================================================
#  Character-Level Fragmentation Repair
# ============================================================

def detect_fragmented_lines(lines: list[str]) -> list[dict]:
    """
    Detect runs of single-character lines (CJK or other scripts)
    that are likely OCR/PDF extraction artifacts.

    Returns list of {start_index, end_index, chars, reconstructed, confidence}.
    """
    fragments = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Check if this is a single non-ASCII character
        is_single_char = len(line) == 1 and not line.isascii()
        # Also check for CJK characters that might have spaces inserted
        is_spaced_cjk = bool(re.match(r'^[一-鿿぀-ゟ゠-ヿ가-힯]\s*$', line))

        if (is_single_char or is_spaced_cjk) and line:
            run_start = i
            run_chars = []

            while i < len(lines):
                curr = lines[i].strip()
                if len(curr) <= 2 and curr and not curr.isascii():
                    # Single CJK/non-ASCII char or spaced CJK
                    char = curr.replace(" ", "")
                    if char:
                        run_chars.append(char)
                    i += 1
                elif len(curr) == 0:
                    # Empty line breaks the run
                    i += 1
                    break
                elif (
                    len(curr) <= 2 and curr.isascii() and
                    i > run_start and i < len(lines) - 1 and
                    len(lines[i + 1].strip()) <= 2
                ):
                    # ASCII punctuation/symbol between single chars — include it
                    run_chars.append(curr)
                    i += 1
                else:
                    break

            run_end = i
            run_length = run_end - run_start

            if run_length >= 2 and run_chars:
                reconstructed = "".join(run_chars)
                fragments.append({
                    "type": "character_fragmentation",
                    "line_start": run_start + 1,  # 1-based
                    "line_end": run_end,          # 1-based
                    "original_chars": run_chars,
                    "reconstructed": reconstructed,
                    "original_line_count": run_length,
                    "confidence": min(0.95, 0.5 + run_length * 0.1),
                })
        else:
            i += 1

    return fragments


def repair_fragmented_text(text: str) -> dict:
    """
    Repair character-level fragmentation in text.
    Returns {repaired_text, repairs_made, details}.
    """
    lines = text.strip().split("\n")
    fragments = detect_fragmented_lines(lines)

    if not fragments:
        return {
            "repaired_text": text,
            "repairs_made": 0,
            "details": [],
        }

    # Build set of line indices to remove
    lines_to_remove = set()
    replacements = {}  # start_index → reconstructed line

    for frag in fragments:
        start_0based = frag["line_start"] - 1
        end_0based = frag["line_end"]

        # Mark all fragment lines for removal
        for j in range(start_0based, end_0based):
            lines_to_remove.add(j)

        # Store the reconstruction at the start position
        replacements[start_0based] = frag["reconstructed"]

    # Build repaired lines
    repaired_lines = []
    repairs_made = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        if i in lines_to_remove:
            # Check if this is the replacement position
            if i in replacements:
                repaired_lines.append(replacements[i])
                repairs_made += 1
            # Otherwise skip (part of a fragment run)
        elif not stripped:
            # Normalize empty lines: collapse consecutive empty lines
            if repaired_lines and repaired_lines[-1] != "":
                repaired_lines.append("")
        else:
            repaired_lines.append(stripped)

    # Remove trailing empty lines
    while repaired_lines and repaired_lines[-1] == "":
        repaired_lines.pop()

    repaired_text = "\n".join(repaired_lines)

    return {
        "repaired_text": repaired_text,
        "repairs_made": repairs_made,
        "details": fragments,
    }


# ============================================================
#  Structure Detection
# ============================================================

def compute_line_similarity(line1: str, line2: str) -> float:
    """Compute similarity ratio between two lines."""
    if not line1 or not line2:
        return 0.0
    return SequenceMatcher(None, line1.strip(), line2.strip()).ratio()


def detect_repeated_sections(
    lines: list[str],
    min_similarity: float = 0.7,
    min_section_length: int = 2,
) -> list[dict]:
    """
    Detect repeated sections (potential choruses) by comparing non-empty lines.
    Returns list of {section_a, section_b, similarity, is_chorus_candidate}.
    """
    # Group lines into blocks separated by empty lines
    blocks = []
    current_block = []
    current_start = 0

    for i, line in enumerate(lines):
        if line.strip():
            if not current_block:
                current_start = i
            current_block.append(line.strip())
        else:
            if len(current_block) >= min_section_length:
                blocks.append({
                    "start": current_start + 1,
                    "end": i,
                    "lines": list(current_block),
                    "length": len(current_block),
                })
            current_block = []

    # Don't forget the last block
    if len(current_block) >= min_section_length:
        blocks.append({
            "start": current_start + 1,
            "end": len(lines),
            "lines": list(current_block),
            "length": len(current_block),
        })

    # Compare blocks for similarity
    repetitions = []
    seen_pairs = set()

    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            if blocks[i]["length"] != blocks[j]["length"]:
                # Different length blocks — try shifted comparison
                shorter = min(blocks[i]["length"], blocks[j]["length"])
                if shorter < 2:
                    continue

                # Compare the shorter block against each window of the longer block
                a_block = blocks[i] if blocks[i]["length"] <= blocks[j]["length"] else blocks[j]
                b_block = blocks[j] if blocks[i]["length"] <= blocks[j]["length"] else blocks[i]

                best_sim = 0.0
                for offset in range(b_block["length"] - a_block["length"] + 1):
                    sims = [
                        compute_line_similarity(a_block["lines"][k], b_block["lines"][offset + k])
                        for k in range(a_block["length"])
                    ]
                    avg_sim = sum(sims) / len(sims) if sims else 0
                    best_sim = max(best_sim, avg_sim)

                if best_sim >= min_similarity:
                    pair_key = (blocks[i]["start"], blocks[j]["start"])
                    if pair_key not in seen_pairs:
                        seen_pairs.add(pair_key)
                        repetitions.append({
                            "type": "partial_repetition",
                            "section_a": {"line_start": blocks[i]["start"], "line_end": blocks[i]["end"]},
                            "section_b": {"line_start": blocks[j]["start"], "line_end": blocks[j]["end"]},
                            "similarity": round(best_sim, 3),
                            "is_chorus_candidate": best_sim >= 0.85,
                        })
            else:
                # Same length blocks — direct line-by-line comparison
                sims = [
                    compute_line_similarity(blocks[i]["lines"][k], blocks[j]["lines"][k])
                    for k in range(blocks[i]["length"])
                ]
                avg_sim = sum(sims) / len(sims) if sims else 0

                if avg_sim >= min_similarity:
                    pair_key = (blocks[i]["start"], blocks[j]["start"])
                    if pair_key not in seen_pairs:
                        seen_pairs.add(pair_key)
                        repetitions.append({
                            "type": "full_repetition" if avg_sim >= 0.9 else "partial_repetition",
                            "section_a": {"line_start": blocks[i]["start"], "line_end": blocks[i]["end"]},
                            "section_b": {"line_start": blocks[j]["start"], "line_end": blocks[j]["end"]},
                            "similarity": round(avg_sim, 3),
                            "is_chorus_candidate": avg_sim >= 0.85,
                        })

    return repetitions


def detect_lyric_structure(text: str) -> dict:
    """
    Detect the overall structure of lyrics.
    Returns {type, sections, repeated_sections, line_count}.
    """
    lines = text.strip().split("\n")
    non_empty_lines = [l for l in lines if l.strip()]

    # Detect repeated sections (potential choruses)
    repetitions = detect_repeated_sections(lines)

    # Identify chorus candidates
    chorus_candidates = [r for r in repetitions if r.get("is_chorus_candidate")]

    # Build section annotations
    sections = []
    chorus_line_ranges = set()

    for rep in chorus_candidates:
        for key in ("section_a", "section_b"):
            start = rep[key]["line_start"]
            end = rep[key]["line_end"]
            for ln in range(start, end + 1):
                chorus_line_ranges.add(ln)

    # Determine structure type
    if chorus_candidates:
        structure_type = "verse-chorus"
    elif repetitions:
        structure_type = "strophic"  # repeated verses
    else:
        structure_type = "through-composed"  # no repetition

    # Build line-to-section mapping
    line_section_map = {}
    last_section_type = None
    section_counter = {"verse": 0, "chorus": 0, "bridge": 0, "intro": 0, "outro": 0}

    for i, line in enumerate(lines):
        line_num = i + 1

        if line_num in chorus_line_ranges:
            section_type = "chorus"
        elif not line.strip():
            continue
        else:
            # Heuristic: if line is shorter than average and non-repeating, might be bridge
            avg_len = sum(len(l.strip()) for l in non_empty_lines) / max(len(non_empty_lines), 1)
            line_len = len(line.strip())

            if line_len < avg_len * 0.5 and len(non_empty_lines) > 4:
                section_type = "bridge"
            else:
                section_type = "verse"

        if section_type != last_section_type:
            if section_type not in section_counter:
                section_counter[section_type] = 0
            section_counter[section_type] += 1

            sections.append({
                "type": section_type,
                "number": section_counter[section_type],
                "line_start": line_num,
                "lines": [],
            })
            last_section_type = section_type

        if sections:
            sections[-1]["lines"].append(line_num)

    # Fill in line_end for each section
    for i, sec in enumerate(sections):
        sec["line_end"] = sec["lines"][-1]
        # Keep only line_start, line_end, type, number
        line_range = sec["lines"]
        del sec["lines"]
        sec["line_count"] = len(line_range)

    return {
        "structure_type": structure_type,
        "sections": sections,
        "repetitions": repetitions,
        "chorus_candidates": chorus_candidates,
        "total_lines": len(lines),
        "non_empty_lines": len(non_empty_lines),
    }


# ============================================================
#  Main Reconstructor
# ============================================================

def reconstruct(text: str) -> dict:
    """
    Full reconstruction pipeline:
    1. Repair character fragmentation
    2. Normalize empty lines
    3. Detect structure
    4. Return complete result
    """
    repair_result = repair_fragmented_text(text)
    clean_text = repair_result["repaired_text"]

    structure = detect_lyric_structure(clean_text)

    return {
        "original_text": text,
        "reconstructed_text": clean_text,
        "repairs": repair_result["details"],
        "repairs_made": repair_result["repairs_made"],
        "structure": structure,
        "has_fragmentation": repair_result["repairs_made"] > 0,
        "has_repetition": len(structure.get("chorus_candidates", [])) > 0,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Lyrics Reconstructor — Repair broken lyrics and detect structure"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # reconstruct command
    recon_parser = subparsers.add_parser("reconstruct", help="Full reconstruction pipeline")
    recon_parser.add_argument("--input", required=True, help="Input JSON file (from noise_recovery) or text file")
    recon_parser.add_argument("--output", required=True, help="Output JSON file path")

    # detect-structure command
    struct_parser = subparsers.add_parser("detect-structure", help="Detect lyric structure only")
    struct_parser.add_argument("--input", required=True, help="Lyric text string or file path")
    struct_parser.add_argument("--file", action="store_true", help="Treat --input as file path")

    # repair command
    repair_parser = subparsers.add_parser("repair", help="Repair character fragmentation only")
    repair_parser.add_argument("--input", required=True, help="Fragmented text string or file path")
    repair_parser.add_argument("--file", action="store_true", help="Treat --input as file path")

    args = parser.parse_args()

    try:
        if args.command == "reconstruct":
            input_path = Path(args.input)
            if not input_path.exists():
                print(json.dumps({"error": f"Input file not found: {args.input}"}), file=sys.stderr)
                sys.exit(1)

            raw = input_path.read_text(encoding="utf-8")

            # Handle JSON input from noise_recovery
            try:
                data = json.loads(raw)
                if "clean_text" in data:
                    text = data["clean_text"]
                elif "text" in data:
                    text = data["text"]
                else:
                    text = raw
            except json.JSONDecodeError:
                text = raw

            result = reconstruct(text)

            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
            print(json.dumps({
                "status": "ok",
                "output": str(output_path.resolve()),
                "repairs_made": result["repairs_made"],
                "structure_type": result["structure"]["structure_type"],
                "sections_found": len(result["structure"]["sections"]),
            }, ensure_ascii=False))

        elif args.command == "detect-structure":
            text = args.input
            if getattr(args, "file", False):
                text = Path(args.input).read_text(encoding="utf-8")

            structure = detect_lyric_structure(text)
            print(json.dumps(structure, ensure_ascii=False, indent=2))

        elif args.command == "repair":
            text = args.input
            if getattr(args, "file", False):
                text = Path(args.input).read_text(encoding="utf-8")

            result = repair_fragmented_text(text)
            print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
