#!/usr/bin/env python3
"""Search arXiv via the official API.

Examples:
    python search.py 'ti:"chain of thought" AND cat:cs.CL' --max 10
    python search.py 'au:Hinton AND cat:cs.LG' --sort submittedDate
    python search.py 'all:mamba state space' --max 5 --json
    python search.py --ids 2409.03108 1706.03762

Query syntax (see references/api-syntax.md for the full cheatsheet):
    ti: title    au: author    abs: abstract    cat: category    all: everything
    Combine with AND / OR / ANDNOT. Quote multi-word phrases.
"""

from __future__ import annotations

import argparse
import json
import sys

import arxiv_api


def format_entry(e: dict, i: int) -> str:
    authors = ", ".join(e["authors"][:6]) + (" et al." if len(e["authors"]) > 6 else "")
    cites = ""
    if "citations" in e:
        cites = (f"   citations: {e['citations']}" if e["citations"] is not None
                 else "   citations: not indexed on S2")
    lines = [
        f"[{i}] {e['title']}",
        f"    id: {e['versioned_id']}   ({e['primary_category']}, "
        f"submitted {e['published'][:10]}, updated {e['updated'][:10]}){cites}",
        f"    authors: {authors}",
    ]
    if e["journal_ref"]:
        lines.append(f"    journal: {e['journal_ref']}")
    if e["doi"]:
        lines.append(f"    doi: {e['doi']}")
    abstract = e["abstract"]
    if len(abstract) > 400:
        abstract = abstract[:400] + "..."
    lines.append(f"    abstract: {abstract}")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query", nargs="?", help="arXiv API search query")
    p.add_argument("--ids", nargs="+", help="Fetch metadata for specific IDs instead of searching")
    p.add_argument("--max", type=int, default=10, help="Max results (default 10)")
    p.add_argument("--start", type=int, default=0, help="Pagination offset")
    p.add_argument(
        "--sort",
        default="relevance",
        choices=["relevance", "lastUpdatedDate", "submittedDate"],
    )
    p.add_argument("--order", default="descending", choices=["ascending", "descending"])
    p.add_argument("--json", action="store_true", help="Emit JSON instead of readable text")
    p.add_argument(
        "--cite-counts",
        action="store_true",
        help="Attach Semantic Scholar citation counts (needs an API key; "
        "one batch request for all results)",
    )
    p.add_argument(
        "--rank-by-citations",
        action="store_true",
        help="Sort results by citation count (implies --cite-counts)",
    )
    args = p.parse_args()

    if args.rank_by_citations:
        args.cite_counts = True

    if not args.query and not args.ids:
        p.error("Provide a search query or --ids")

    try:
        result = arxiv_api.query(
            search_query=args.query,
            id_list=args.ids,
            start=args.start,
            max_results=args.max,
            sort_by=args.sort,
            sort_order=args.order,
        )
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.cite_counts and result["entries"]:
        from common import s2_api_key

        if not s2_api_key():
            print(
                "warning: --cite-counts skipped — no Semantic Scholar API key "
                "found (set S2_API_KEY or create s2_config.json in the skill "
                "root).",
                file=sys.stderr,
            )
        else:
            try:
                import s2

                counts = s2.batch_lookup([e["id"] for e in result["entries"]])
                for e in result["entries"]:
                    paper = counts.get(e["id"], {})
                    e["citations"] = paper.get("citationCount")
                if args.rank_by_citations:
                    result["entries"].sort(
                        key=lambda e: e.get("citations") or 0, reverse=True
                    )
            except Exception as e:
                print(f"warning: citation lookup failed ({e}); "
                      "showing results without counts", file=sys.stderr)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"total matches: {result['total']} (showing {len(result['entries'])}, "
              f"offset {args.start})\n")
        for i, e in enumerate(result["entries"], start=1 + args.start):
            print(format_entry(e, i))
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
