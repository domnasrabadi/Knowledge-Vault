#!/usr/bin/env python3
"""Semantic Scholar lookups: citation counts, who cites a paper, what it
references, related-paper recommendations, and corpus-wide relevance search.

Examples:
    python s2.py info 2409.03108
    python s2.py citations 1706.03762 --max 20
    python s2.py references 1706.03762
    python s2.py recommend 2409.03108 --max 10
    python s2.py search "state space models" --year 2023-2025 --min-citations 50

API key (optional): set the S2_API_KEY env var, or create s2_config.json in
the skill root containing {"api_key": "..."}. Without a key everything still
works on the shared public pool, which rate-limits aggressively (429s are
normal; the script backs off and retries). A key gives a private quota and
makes `search` and batch lookups dependable.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse

from common import http_get, normalize_arxiv_id, s2_api_key, s2_headers

BASE = "https://api.semanticscholar.org/graph/v1"
REC = "https://api.semanticscholar.org/recommendations/v1"

PAPER_FIELDS = (
    "title,year,citationCount,influentialCitationCount,referenceCount,"
    "externalIds,venue,authors,abstract,tldr,isOpenAccess"
)
LIST_FIELDS = "title,year,citationCount,externalIds,venue,authors"


def _get(url: str, data: bytes | None = None) -> dict | list:
    payload = http_get(url, rate_limit_key="s2", delay=1.5,
                       headers=s2_headers(), data=data)
    return json.loads(payload)


def batch_lookup(arxiv_ids: list[str], fields: str = LIST_FIELDS) -> dict[str, dict]:
    """Look up many papers in one POST. Returns {base_arxiv_id: paper_or_{}}.

    Requires an API key in practice — callers should check s2_api_key()
    first and skip gracefully if absent. IDs may include versions; they are
    stripped, since Semantic Scholar indexes by base ID.
    """
    bases = []
    for raw in arxiv_ids:
        base, _ = normalize_arxiv_id(raw)
        bases.append(base)
    body = json.dumps({"ids": [f"arXiv:{b}" for b in bases]}).encode()
    url = f"{BASE}/paper/batch?fields={urllib.parse.quote(fields)}"
    results = _get(url, data=body)  # POST; list aligned with input, nulls for misses
    out: dict[str, dict] = {}
    for base, paper in zip(bases, results):
        out[base] = paper or {}
    return out


def relevance_search(
    query: str,
    *,
    year: str | None = None,
    min_citations: int | None = None,
    fields_of_study: str | None = None,
    limit: int = 20,
) -> list[dict]:
    params: dict[str, str] = {
        "query": query,
        "fields": LIST_FIELDS,
        "limit": str(min(limit, 100)),
    }
    if year:
        params["year"] = year  # e.g. "2023", "2023-2025", "2023-"
    if min_citations is not None:
        params["minCitationCount"] = str(min_citations)
    if fields_of_study:
        params["fieldsOfStudy"] = fields_of_study  # e.g. "Computer Science"
    url = f"{BASE}/paper/search?{urllib.parse.urlencode(params)}"
    data = _get(url)
    return data.get("data", []) if isinstance(data, dict) else []


def _brief(paper: dict) -> dict:
    ext = paper.get("externalIds") or {}
    return {
        "title": paper.get("title"),
        "year": paper.get("year"),
        "venue": paper.get("venue") or None,
        "citations": paper.get("citationCount"),
        "arxiv_id": ext.get("ArXiv"),
        "doi": ext.get("DOI"),
        "authors": [a.get("name") for a in (paper.get("authors") or [])][:8],
    }


def _print_list(items: list[dict], as_json: bool) -> None:
    if as_json:
        print(json.dumps(items, indent=2, ensure_ascii=False))
        return
    if not items:
        print("(no results)")
        return
    for i, p in enumerate(items, 1):
        authors = ", ".join(a for a in p["authors"][:4] if a)
        arxiv = f"  arXiv:{p['arxiv_id']}" if p["arxiv_id"] else ""
        venue = f"  [{p['venue']}]" if p["venue"] else ""
        print(f"[{i}] ({p['citations']} cites, {p['year']}) {p['title']}{arxiv}{venue}")
        print(f"    {authors}")


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = p.add_subparsers(dest="command", required=True)

    for name in ("info", "citations", "references", "recommend"):
        sp = sub.add_parser(name)
        sp.add_argument("paper", help="arXiv ID or URL")
        sp.add_argument("--max", type=int, default=20)
        sp.add_argument("--json", action="store_true")

    ss = sub.add_parser("search", help="Corpus-wide relevance search with filters")
    ss.add_argument("query", help="Natural-language search query")
    ss.add_argument("--year", help="Year or range: 2024, 2023-2025, 2023-")
    ss.add_argument("--min-citations", type=int, help="Minimum citation count")
    ss.add_argument("--fields-of-study", help='e.g. "Computer Science"')
    ss.add_argument("--max", type=int, default=20)
    ss.add_argument("--json", action="store_true")

    args = p.parse_args()

    if not s2_api_key() and args.command == "search":
        print("note: no API key found (env S2_API_KEY or s2_config.json in the "
              "skill root); using the shared public pool, expect throttling.",
              file=sys.stderr)

    try:
        if args.command == "search":
            raw = relevance_search(
                args.query,
                year=args.year,
                min_citations=args.min_citations,
                fields_of_study=args.fields_of_study,
                limit=args.max,
            )
            _print_list([_brief(x) for x in raw], args.json)
            return 0

        base_id, _ = normalize_arxiv_id(args.paper)
        pid = f"arXiv:{base_id}"

        if args.command == "info":
            data = _get(f"{BASE}/paper/{pid}?fields={PAPER_FIELDS}")
            if args.json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                b = _brief(data)
                print(b["title"])
                print(f"  year: {b['year']}   venue: {b['venue'] or 'n/a'}")
                print(f"  citations: {data.get('citationCount')} "
                      f"(influential: {data.get('influentialCitationCount')}), "
                      f"references: {data.get('referenceCount')}")
                tldr = (data.get("tldr") or {}).get("text")
                if tldr:
                    print(f"  tldr: {tldr}")
        elif args.command in ("citations", "references"):
            data = _get(
                f"{BASE}/paper/{pid}/{args.command}"
                f"?fields={LIST_FIELDS}&limit={min(args.max, 100)}"
            )
            key = "citingPaper" if args.command == "citations" else "citedPaper"
            items = [_brief(row[key]) for row in data.get("data", []) if row.get(key)]
            items.sort(key=lambda x: x["citations"] or 0, reverse=True)
            _print_list(items, args.json)
        else:  # recommend
            data = _get(
                f"{REC}/papers/forpaper/{pid}"
                f"?fields={LIST_FIELDS}&limit={min(args.max, 100)}"
            )
            items = [_brief(x) for x in data.get("recommendedPapers", [])]
            _print_list(items, args.json)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        print("note: the free Semantic Scholar pool rate-limits aggressively; "
              "wait a minute and retry, or add an API key (see --help).",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
