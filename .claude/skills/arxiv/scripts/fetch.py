#!/usr/bin/env python3
"""Fetch an arXiv paper into the local cache and prepare it for reading.

Pipeline: normalize ID -> resolve version via API -> download LaTeX source
(e-print) -> safe-extract -> find entrypoint -> flatten \\input/\\include into
one file. Falls back to the PDF when no LaTeX source exists. Idempotent:
cached artifacts are reused, pass --force to re-download.

Examples:
    python fetch.py 2409.03108
    python fetch.py https://arxiv.org/abs/1706.03762v7
    python fetch.py 2409.03108 --pdf          # also fetch the PDF
    python fetch.py 2409.03108 --json         # machine-readable manifest

Prints a manifest of what is available: source dir, entrypoint, flattened
tex, pdf, and metadata. Feed the flattened tex (or the source dir) to
to_markdown.py, or read it directly.
"""

from __future__ import annotations

import argparse
import gzip
import io
import json
import re
import sys
import tarfile
from pathlib import Path

import arxiv_api
from common import http_get, id_with_version, normalize_arxiv_id, paper_dir, read_json, write_json

MAX_EXTRACT_BYTES = 500 * 1024 * 1024  # refuse archives that expand past 500 MB


# ---------------------------------------------------------------------------
# Download and payload detection
# ---------------------------------------------------------------------------


def download_eprint(versioned_id: str) -> bytes:
    return http_get(f"https://arxiv.org/e-print/{versioned_id}", rate_limit_key="arxiv")


def download_pdf(versioned_id: str) -> bytes:
    return http_get(f"https://arxiv.org/pdf/{versioned_id}", rate_limit_key="arxiv")


def detect_payload(data: bytes) -> str:
    """Classify an e-print payload: 'targz', 'gzip-single', 'pdf', 'tex', 'unknown'."""
    if data[:4] == b"%PDF":
        return "pdf"
    if data[:2] == b"\x1f\x8b":  # gzip magic; could wrap a tar or a lone file
        inner = gzip.decompress(data)
        if len(inner) > 262 and inner[257:262] == b"ustar":
            return "targz"
        return "gzip-single"
    if data[:257].lstrip()[:1] in (b"%", b"\\"):
        return "tex"
    return "unknown"


# ---------------------------------------------------------------------------
# Safe extraction
# ---------------------------------------------------------------------------


def safe_extract_targz(data: bytes, dest: Path) -> list[str]:
    """Extract a tar.gz, refusing path traversal, absolute paths, links, and
    absurd expansion. Returns the list of extracted relative paths."""
    dest.mkdir(parents=True, exist_ok=True)
    extracted: list[str] = []
    total = 0
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for member in tf:
            name = member.name
            if member.issym() or member.islnk():
                print(f"  skipping link in archive: {name}", file=sys.stderr)
                continue
            p = Path(name)
            if p.is_absolute() or ".." in p.parts:
                print(f"  skipping unsafe path in archive: {name}", file=sys.stderr)
                continue
            target = (dest / p).resolve()
            if not target.is_relative_to(dest.resolve()):
                print(f"  skipping escaping path in archive: {name}", file=sys.stderr)
                continue
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            if not member.isfile():
                continue
            total += member.size
            if total > MAX_EXTRACT_BYTES:
                raise RuntimeError("Archive expands beyond the safety limit; aborting.")
            target.parent.mkdir(parents=True, exist_ok=True)
            src = tf.extractfile(member)
            if src is None:
                continue
            with open(target, "wb") as out:
                out.write(src.read())
            extracted.append(str(p))
    return extracted


# ---------------------------------------------------------------------------
# Entrypoint detection and flattening
# ---------------------------------------------------------------------------

_INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")
# An unescaped % starts a LaTeX comment for the rest of the line.
_COMMENT_RE = re.compile(r"(?<!\\)%")


def _split_comment(line: str) -> tuple[str, str]:
    """Split a line into (code, comment-including-%)."""
    m = _COMMENT_RE.search(line)
    if m:
        return line[: m.start()], line[m.start():]
    return line, ""


def _count_inputs(text: str) -> int:
    return sum(len(_INPUT_RE.findall(_split_comment(line)[0])) for line in text.splitlines())


def _read_tex(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def find_entrypoint(src_dir: Path) -> Path | None:
    """Pick the main .tex file.

    Preference order: contains \\begin{document} and \\documentclass; then
    most \\input/\\include directives; then conventional names; then
    shallower paths; then size.
    """
    candidates = sorted(src_dir.rglob("*.tex"))
    if not candidates:
        return None
    scored: list[tuple[tuple, Path]] = []
    conventional = {"main.tex", "paper.tex", "ms.tex", "arxiv.tex", "manuscript.tex"}
    for path in candidates:
        text = _read_tex(path)
        has_begin_doc = "\\begin{document}" in text
        has_docclass = "\\documentclass" in text
        n_inputs = _count_inputs(text)
        is_conventional = path.name.lower() in conventional
        depth = len(path.relative_to(src_dir).parts)  # prefer shallow files
        scored.append(
            (
                (has_begin_doc, has_docclass, n_inputs, is_conventional, -depth,
                 path.stat().st_size),
                path,
            )
        )
    scored.sort(key=lambda t: t[0], reverse=True)
    best_score, best = scored[0]
    if not best_score[0]:  # nothing has \begin{document}
        print("warning: no .tex file contains \\begin{document}; "
              f"guessing {best.name}", file=sys.stderr)
    return best


def flatten(entry: Path, src_dir: Path, _seen: set | None = None) -> str:
    """Recursively inline \\input{...} and \\include{...}. Cycle-safe.

    Missing includes are left in place with a comment so nothing is silently
    dropped."""
    seen = _seen if _seen is not None else set()
    entry = entry.resolve()
    if entry in seen:
        return f"% [arxiv-skill] skipped repeated include: {entry.name}\n"
    seen.add(entry)

    def _sub(match: re.Match) -> str:
        target = match.group(1).strip()
        rel = Path(target if target.endswith(".tex") else target + ".tex")
        for candidate in (entry.parent / rel, src_dir / rel):
            if candidate.exists():
                inlined = flatten(candidate, src_dir, seen)
                return (
                    f"\n% [arxiv-skill] begin {rel}\n{inlined}\n"
                    f"% [arxiv-skill] end {rel}\n"
                )
        return f"{match.group(0)}\n% [arxiv-skill] include not found on disk: {rel}\n"

    out_lines = []
    for line in _read_tex(entry).splitlines():
        code, comment = _split_comment(line)
        out_lines.append(_INPUT_RE.sub(_sub, code) + comment)
    return "\n".join(out_lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def fetch(raw: str, *, want_pdf: bool = False, force: bool = False) -> dict:
    base, ver = normalize_arxiv_id(raw)

    # Resolve to an explicit version so reads are pinned and reproducible.
    meta = None
    if not ver or force:
        try:
            meta = arxiv_api.get_metadata(id_with_version(base, ver))
            ver = ver or meta["version"]
        except Exception as e:
            print(f"warning: metadata lookup failed ({e}); "
                  "continuing without version pinning", file=sys.stderr)
    versioned = id_with_version(base, ver)
    pdir = paper_dir(versioned)

    meta_path = pdir / "meta.json"
    if meta:
        write_json(meta_path, meta)
    elif meta_path.exists():
        meta = read_json(meta_path)
    else:
        try:
            meta = arxiv_api.get_metadata(versioned)
            write_json(meta_path, meta)
        except Exception as e:
            print(f"warning: could not fetch metadata: {e}", file=sys.stderr)

    manifest: dict = {
        "id": base,
        "version": ver,
        "versioned_id": versioned,
        "cache_dir": str(pdir),
        "title": meta["title"] if meta else None,
        "source": None,
        "entrypoint": None,
        "flattened_tex": None,
        "pdf": None,
        "notes": [],
    }

    src_dir = pdir / "src"
    raw_path = pdir / "src.tar.gz"
    flattened_path = pdir / "flattened.tex"
    pdf_path = pdir / "paper.pdf"

    # --- source ---
    need_source = force or not (src_dir.exists() and any(src_dir.iterdir()))
    if need_source:
        try:
            data = download_eprint(versioned)
            kind = detect_payload(data)
            raw_path.write_bytes(data)
            if kind == "targz":
                safe_extract_targz(data, src_dir)
            elif kind == "gzip-single":
                src_dir.mkdir(parents=True, exist_ok=True)
                (src_dir / "main.tex").write_bytes(gzip.decompress(data))
            elif kind == "tex":
                src_dir.mkdir(parents=True, exist_ok=True)
                (src_dir / "main.tex").write_bytes(data)
            elif kind == "pdf":
                pdf_path.write_bytes(data)
                manifest["notes"].append(
                    "No LaTeX source on arXiv for this paper; e-print was the PDF itself."
                )
            else:
                manifest["notes"].append(
                    f"Unrecognized e-print payload ({len(data)} bytes); kept at src.tar.gz."
                )
        except Exception as e:
            manifest["notes"].append(f"Source download failed: {e}")
    else:
        manifest["notes"].append("Reused cached source.")

    if src_dir.exists() and any(src_dir.iterdir()):
        manifest["source"] = str(src_dir)
        entry = find_entrypoint(src_dir)
        if entry:
            manifest["entrypoint"] = str(entry)
            if force or not flattened_path.exists():
                flattened_path.write_text(flatten(entry, src_dir), encoding="utf-8")
            manifest["flattened_tex"] = str(flattened_path)
        else:
            manifest["notes"].append("No .tex files found in the extracted source.")

    # --- pdf (on request, or as fallback when there is no usable source) ---
    if want_pdf or (manifest["flattened_tex"] is None and not pdf_path.exists()):
        if force or not pdf_path.exists():
            try:
                data = download_pdf(versioned)
                if data[:4] != b"%PDF":
                    raise RuntimeError("response was not a PDF (withdrawn paper?)")
                pdf_path.write_bytes(data)
            except Exception as e:
                manifest["notes"].append(f"PDF download failed: {e}")
    if pdf_path.exists():
        manifest["pdf"] = str(pdf_path)

    if manifest["flattened_tex"] is None and manifest["pdf"] is None:
        manifest["notes"].append(
            "Neither source nor PDF is available; the paper may be withdrawn. "
            "Check the abs page."
        )
    return manifest


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paper", help="arXiv ID or URL in any common form")
    p.add_argument("--pdf", action="store_true", help="Also download the PDF")
    p.add_argument("--force", action="store_true", help="Re-download even if cached")
    p.add_argument("--json", action="store_true", help="Emit the manifest as JSON")
    args = p.parse_args()

    try:
        manifest = fetch(args.paper, want_pdf=args.pdf, force=args.force)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    else:
        print(f"paper:     {manifest['versioned_id']}"
              + (f" - {manifest['title']}" if manifest["title"] else ""))
        print(f"cache:     {manifest['cache_dir']}")
        for key in ("source", "entrypoint", "flattened_tex", "pdf"):
            if manifest[key]:
                print(f"{key + ':':11s}{manifest[key]}")
        for note in manifest["notes"]:
            print(f"note:      {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
