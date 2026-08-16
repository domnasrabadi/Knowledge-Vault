#!/usr/bin/env python3
"""Convert a fetched paper to Markdown.

Runs fetch.py's pipeline if the paper is not cached yet, then converts:
  1. pandoc on the flattened LaTeX  ->  GitHub Markdown with $...$ math
  2. fallback: pdftotext -layout on the PDF (labeled as degraded output)
  3. last resort: the flattened .tex itself is perfectly readable

Examples:
    python to_markdown.py 2409.03108
    python to_markdown.py https://arxiv.org/abs/1706.03762 --stdout
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import fetch as fetch_mod


def pandoc_convert(flattened_tex: Path, out_md: Path) -> bool:
    if not shutil.which("pandoc"):
        print("pandoc not found on PATH", file=sys.stderr)
        return False
    cmd = [
        "pandoc",
        "-s",  # standalone: keeps title/authors/abstract as YAML frontmatter
        "-f", "latex",
        "-t", "gfm+tex_math_dollars",
        "--wrap=none",
        "--markdown-headings=atx",
        str(flattened_tex),
        "-o", str(out_md),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        print("pandoc timed out", file=sys.stderr)
        return False
    if proc.returncode != 0:
        print(f"pandoc failed:\n{proc.stderr[:2000]}", file=sys.stderr)
        return False
    # Guard against near-empty output from exotic macro-heavy papers.
    if out_md.stat().st_size < 500:
        print("pandoc produced suspiciously little output; treating as failure",
              file=sys.stderr)
        return False
    return True


def pdftotext_convert(pdf: Path, out_md: Path) -> bool:
    if not shutil.which("pdftotext"):
        print("pdftotext not found on PATH", file=sys.stderr)
        return False
    proc = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True
    )
    if proc.returncode != 0 or len(proc.stdout) < 500:
        return False
    header = (
        "> [arxiv-skill] NOTE: this is plain-text extraction from the PDF, not a\n"
        "> LaTeX conversion. Math, tables, and layout are degraded; do not trust\n"
        "> equation or table details from this file without checking the PDF.\n\n"
    )
    out_md.write_text(header + proc.stdout, encoding="utf-8")
    return True


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paper", help="arXiv ID or URL")
    p.add_argument("--force", action="store_true", help="Re-fetch and re-convert")
    p.add_argument("--stdout", action="store_true", help="Print the markdown")
    args = p.parse_args()

    manifest = fetch_mod.fetch(args.paper, force=args.force)
    cache = Path(manifest["cache_dir"])
    out_md = cache / "paper.md"

    if out_md.exists() and not args.force:
        print(f"markdown (cached): {out_md}", file=sys.stderr)
    else:
        done = False
        if manifest["flattened_tex"]:
            done = pandoc_convert(Path(manifest["flattened_tex"]), out_md)
            if done:
                print(f"converted via pandoc: {out_md}", file=sys.stderr)
        if not done and manifest["pdf"]:
            done = pdftotext_convert(Path(manifest["pdf"]), out_md)
            if done:
                print(f"converted via pdftotext (degraded): {out_md}", file=sys.stderr)
        if not done:
            if manifest["flattened_tex"]:
                print(
                    "conversion failed; read the flattened LaTeX directly, it is "
                    f"fully readable: {manifest['flattened_tex']}",
                    file=sys.stderr,
                )
                return 2
            print("no convertible artifact available", file=sys.stderr)
            for note in manifest["notes"]:
                print(f"note: {note}", file=sys.stderr)
            return 1

    if args.stdout:
        print(out_md.read_text(encoding="utf-8"))
    else:
        print(out_md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
