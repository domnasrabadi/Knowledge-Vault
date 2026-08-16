"""Thin client for the arXiv Atom API (export.arxiv.org/api/query).

Shared by search.py, fetch.py, and bibtex.py. Stdlib only.
"""

from __future__ import annotations

import urllib.parse
import xml.etree.ElementTree as ET

from common import http_get

API_URL = "https://export.arxiv.org/api/query"

_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}


def _text(elem, path: str) -> str:
    node = elem.find(path, _NS)
    return (node.text or "").strip() if node is not None else ""


def _parse_entry(entry) -> dict:
    # entry <id> looks like http://arxiv.org/abs/2409.03108v2
    raw_id = _text(entry, "atom:id")
    versioned = raw_id.rsplit("/abs/", 1)[-1] if "/abs/" in raw_id else raw_id
    base, _, ver = versioned.partition("v")
    authors = [
        (a.findtext("atom:name", default="", namespaces=_NS) or "").strip()
        for a in entry.findall("atom:author", _NS)
    ]
    categories = [
        c.get("term", "") for c in entry.findall("atom:category", _NS) if c.get("term")
    ]
    pdf_link = ""
    for link in entry.findall("atom:link", _NS):
        if link.get("title") == "pdf" or link.get("type") == "application/pdf":
            pdf_link = link.get("href", "")
    return {
        "id": base,
        "version": f"v{ver}" if ver else None,
        "versioned_id": versioned,
        "title": " ".join(_text(entry, "atom:title").split()),
        "authors": [a for a in authors if a],
        "abstract": " ".join(_text(entry, "atom:summary").split()),
        "published": _text(entry, "atom:published"),
        "updated": _text(entry, "atom:updated"),
        "primary_category": (
            entry.find("arxiv:primary_category", _NS).get("term", "")
            if entry.find("arxiv:primary_category", _NS) is not None
            else (categories[0] if categories else "")
        ),
        "categories": categories,
        "doi": _text(entry, "arxiv:doi"),
        "journal_ref": _text(entry, "arxiv:journal_ref"),
        "comment": _text(entry, "arxiv:comment"),
        "abs_url": f"https://arxiv.org/abs/{versioned}",
        "pdf_url": pdf_link or f"https://arxiv.org/pdf/{versioned}",
    }


def query(
    search_query: str | None = None,
    id_list: list[str] | None = None,
    start: int = 0,
    max_results: int = 10,
    sort_by: str = "relevance",  # relevance | lastUpdatedDate | submittedDate
    sort_order: str = "descending",
) -> dict:
    """Run one arXiv API query. Returns {"total": int, "entries": [...]}.

    A returned entry whose title is "Error" indicates a malformed query;
    we surface that as a ValueError so callers do not mistake it for a paper.
    """
    params: dict[str, str] = {
        "start": str(start),
        "max_results": str(max_results),
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    if search_query:
        params["search_query"] = search_query
    if id_list:
        params["id_list"] = ",".join(id_list)
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"
    xml_bytes = http_get(url, rate_limit_key="arxiv")
    root = ET.fromstring(xml_bytes)
    total = _text(root, "opensearch:totalResults")
    entries = [_parse_entry(e) for e in root.findall("atom:entry", _NS)]
    if len(entries) == 1 and entries[0]["title"] == "Error":
        raise ValueError(f"arXiv API rejected the query: {entries[0]['abstract']}")
    return {"total": int(total) if total.isdigit() else len(entries), "entries": entries}


def get_metadata(versioned_or_base_id: str) -> dict:
    """Fetch metadata for a single paper by ID (with or without version)."""
    result = query(id_list=[versioned_or_base_id], max_results=1)
    if not result["entries"]:
        raise LookupError(f"No arXiv record found for {versioned_or_base_id!r}")
    return result["entries"][0]
