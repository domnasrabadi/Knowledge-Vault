#!/usr/bin/env python3
"""Generate a BibTeX entry for an arXiv paper, pinned to a specific version.

If the paper has a journal DOI, that is included so the published version can
be cited instead. The note field records exactly which arXiv version the
entry refers to, avoiding citation drift when papers are revised.

Examples:
    python bibtex.py 1706.03762
    python bibtex.py https://arxiv.org/abs/2409.03108v2
"""

from __future__ import annotations

import argparse
import re
import sys

import arxiv_api
from common import id_with_version, normalize_arxiv_id


def _key(meta: dict) -> str:
    first_author_last = meta["authors"][0].split()[-1].lower() if meta["authors"] else "anon"
    first_author_last = re.sub(r"[^a-z]", "", first_author_last) or "anon"
    year = meta["published"][:4] if meta["published"] else "0000"
    first_word = next(
        (w.lower() for w in re.findall(r"[A-Za-z]+", meta["title"]) if len(w) > 3),
        "paper",
    )
    return f"{first_author_last}{year}{first_word}"


def to_bibtex(meta: dict) -> str:
    authors = " and ".join(meta["authors"])
    year = meta["published"][:4]
    fields = [
        ("title", meta["title"]),
        ("author", authors),
        ("year", year),
        ("eprint", meta["versioned_id"]),
        ("archivePrefix", "arXiv"),
        ("primaryClass", meta["primary_category"]),
        ("url", meta["abs_url"]),
    ]
    if meta.get("doi"):
        fields.append(("doi", meta["doi"]))
    if meta.get("journal_ref"):
        fields.append(("note", f"Published as: {meta['journal_ref']}"))
    body = ",\n".join(f"  {k}={{{v}}}" for k, v in fields if v)
    return f"@misc{{{_key(meta)},\n{body}\n}}"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paper", help="arXiv ID or URL")
    args = p.parse_args()
    try:
        base, ver = normalize_arxiv_id(args.paper)
        meta = arxiv_api.get_metadata(id_with_version(base, ver))
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(to_bibtex(meta))
    return 0


if __name__ == "__main__":
    sys.exit(main())
