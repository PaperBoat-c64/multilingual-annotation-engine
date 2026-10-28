#!/usr/bin/env python3
"""
Batch Runner — Process multiple files through the annotation pipeline.

Accepts a directory of input files and coordinates batch processing
with color consistency across all files in the batch.

Usage:
    python batch_runner.py process --input <dir> --output <dir> --format html
    python batch_runner.py process --input <dir> --output <dir> --format docx --palette default
    python batch_runner.py list --input <dir>

The actual annotation logic is performed by Claude. This script handles:
- File discovery and filtering
- Batch state management
- Per-file output organization
- Cross-file color lexicon sharing
- Progress reporting
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

# Supported input extensions
SUPPORTED_EXTENSIONS = {".txt", ".md", ".markdown", ".json"}

# Language code to name mapping (for reporting)
LANG_NAMES = {
    "ar": "Arabic", "fa": "Persian", "ur": "Urdu", "ps": "Pashto",
    "he": "Hebrew", "zh": "Chinese", "ja": "Japanese", "ko": "Korean",
    "en": "English", "fr": "French", "de": "German", "it": "Italian",
    "es": "Spanish", "ru": "Russian", "tr": "Turkish", "hi": "Hindi",
}


def discover_files(input_dir: Path, extensions: set[str] = None) -> list[Path]:
    """Discover supported files in a directory (non-recursive by default)."""
    exts = extensions or SUPPORTED_EXTENSIONS
    files = []
    if not input_dir.is_dir():
        raise ValueError(f"Not a directory: {input_dir}")
    for f in sorted(input_dir.iterdir()):
        if f.is_file() and f.suffix.lower() in exts:
            files.append(f)
    return files


def build_batch_manifest(files: list[Path], output_dir: Path, fmt: str) -> dict:
    """Build a batch processing manifest."""
    manifest = {
        "batch_id": f"batch_{abs(hash(str(output_dir))) % (10 ** 8)}",
        "total_files": len(files),
        "format": fmt,
        "output_dir": str(output_dir.resolve()),
        "files": [],
    }
    for f in files:
        manifest["files"].append({
            "input": str(f.resolve()),
            "output": str((output_dir / f"{f.stem}.{fmt}").resolve()),
            "stem": f.stem,
            "extension": f.suffix,
        })
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Batch Runner for Multilingual Annotation Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    process_parser = subparsers.add_parser("process", help="Prepare batch processing manifest")
    process_parser.add_argument("--input", required=True, help="Input directory path")
    process_parser.add_argument("--output", required=True, help="Output directory path")
    process_parser.add_argument("--format", default="html",
                                choices=["html", "docx", "pdf", "markdown", "anki"],
                                help="Output format")
    process_parser.add_argument("--palette", default="default", help="Color palette name")
    process_parser.add_argument("--extensions", default=None,
                                help="Comma-separated list of extensions (e.g., '.txt,.md')")

    list_parser = subparsers.add_parser("list", help="List files in input directory")
    list_parser.add_argument("--input", required=True, help="Input directory path")
    list_parser.add_argument("--extensions", default=None, help="Filter by extensions")

    args = parser.parse_args()

    try:
        if args.command == "list":
            input_dir = Path(args.input)
            exts = set(args.extensions.split(",")) if args.extensions else None
            files = discover_files(input_dir, exts)
            result = {
                "directory": str(input_dir.resolve()),
                "file_count": len(files),
                "files": [{"name": f.name, "path": str(f.resolve())} for f in files],
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif args.command == "process":
            input_dir = Path(args.input)
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)

            exts_raw = args.extensions
            exts = set(exts_raw.split(",")) if exts_raw else None
            files = discover_files(input_dir, exts)

            if not files:
                print(json.dumps({
                    "status": "error",
                    "message": f"No supported files found in {input_dir}",
                    "supported_extensions": list(SUPPORTED_EXTENSIONS),
                }), file=sys.stderr)
                sys.exit(1)

            manifest = build_batch_manifest(files, output_dir, args.format)
            manifest["palette"] = args.palette

            # Write manifest for Claude to consume
            manifest_path = output_dir / "batch_manifest.json"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

            print(json.dumps({
                "status": "ok",
                "message": f"Batch manifest created. Process {manifest['total_files']} files with Claude using this manifest.",
                "manifest_path": str(manifest_path.resolve()),
                "file_count": manifest["total_files"],
                "output_format": args.format,
                "next_step": "Run the Multilingual Annotation Engine on each file listed in the manifest.",
            }, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
