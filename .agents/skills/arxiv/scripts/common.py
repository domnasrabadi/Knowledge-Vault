"""Shared helpers for the arxiv skill scripts.

Handles: arXiv ID normalization from any input form, polite HTTP with
retries and rate limiting, and the local paper cache layout.

Cache layout (one directory per paper version):
    ~/.cache/arxiv-skill/<id-with-dots-replaced>/     e.g. 2409.03108v2/
        meta.json        - metadata fetched from the arXiv API
        src.tar.gz       - raw e-print download (may actually be gzip'd tex or pdf)
        src/             - safely extracted LaTeX source
        paper.pdf        - PDF download (fallback path)
        flattened.tex    - single-file LaTeX with \\input/\\include inlined
        paper.md         - Markdown conversion
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

USER_AGENT = "arxiv-skill/1.0 (research assistant; contact: local-user)"
ARXIV_API_DELAY_SECONDS = 3.0  # arXiv asks for no more than 1 request / 3s

_last_request_time: dict[str, float] = {}

# ---------------------------------------------------------------------------
# ID normalization
# ---------------------------------------------------------------------------

# New-style IDs: 4 digits (YYMM), dot, 4-5 digits, optional version.
_NEW_ID = re.compile(r"(?P<id>\d{4}\.\d{4,5})(?P<ver>v\d+)?")
# Old-style IDs: archive(.subject)?/YYMMNNN, optional version.
_OLD_ID = re.compile(r"(?P<id>[a-z\-]+(?:\.[A-Z]{2})?/\d{7})(?P<ver>v\d+)?")


def normalize_arxiv_id(raw: str) -> tuple[str, str | None]:
    """Return (base_id, version_or_None) from any common input form.

    Accepts: bare IDs (2409.03108, 2409.03108v2, math.GT/0309136v1),
    arxiv.org URLs (/abs/, /pdf/, /html/, /src/, /e-print/, with or
    without .pdf suffix, with query strings/anchors), export.arxiv.org,
    ar5iv.org, alphaxiv.org, huggingface.co/papers, and the arXiv DOI
    form 10.48550/arXiv.XXXX.XXXXX.

    Raises ValueError if no arXiv ID can be found.
    """
    s = raw.strip()

    # DOI form
    doi = re.search(r"10\.48550/arXiv\.(\d{4}\.\d{4,5})(v\d+)?", s, re.IGNORECASE)
    if doi:
        return doi.group(1), doi.group(2)

    # Strip URL scaffolding so path-embedded IDs are found; try old-style
    # first because it is stricter about its prefix.
    for pattern in (_OLD_ID, _NEW_ID):
        m = pattern.search(s)
        if m:
            base = m.group("id")
            ver = m.group("ver")
            # Guard against matching digits inside unrelated URLs: require
            # that, if the input looks like a URL, it is an arXiv-ish host.
            if "://" in s or s.startswith("www."):
                host_ok = re.search(
                    r"(arxiv\.org|ar5iv\.(?:org|labs\.arxiv\.org)|alphaxiv\.org|"
                    r"huggingface\.co|semanticscholar\.org)",
                    s,
                    re.IGNORECASE,
                )
                if not host_ok:
                    raise ValueError(
                        f"URL does not look like an arXiv-related host: {raw!r}"
                    )
            return base, ver

    raise ValueError(f"Could not find an arXiv ID in: {raw!r}")


def id_with_version(base: str, version: str | None) -> str:
    return f"{base}{version}" if version else base


# ---------------------------------------------------------------------------
# Semantic Scholar API key (optional add-on)
# ---------------------------------------------------------------------------


def skill_root() -> Path:
    """The skill's root directory (parent of scripts/)."""
    return Path(__file__).resolve().parent.parent


def s2_api_key() -> str | None:
    """Find an optional Semantic Scholar API key.

    Order: S2_API_KEY env var, then s2_config.json in the skill root
    (format: {"api_key": "..."}). Returns None if neither is present —
    all S2 features still work keyless, just on the shared public pool.
    """
    key = os.environ.get("S2_API_KEY")
    if key:
        return key.strip()
    cfg = skill_root() / "s2_config.json"
    if cfg.exists():
        try:
            key = json.loads(cfg.read_text(encoding="utf-8")).get("api_key", "")
            return key.strip() or None
        except Exception as e:
            print(f"warning: could not parse {cfg}: {e}", file=sys.stderr)
    return None


def s2_headers() -> dict[str, str]:
    key = s2_api_key()
    return {"x-api-key": key} if key else {}


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------


def http_get(
    url: str,
    *,
    rate_limit_key: str | None = None,
    delay: float = ARXIV_API_DELAY_SECONDS,
    max_retries: int = 3,
    timeout: int = 60,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
) -> bytes:
    """GET (or POST, when data is given) with a User-Agent, per-host rate
    limiting, and retry/backoff.

    rate_limit_key groups requests that share a limit (e.g. "arxiv").
    Retries on 429/5xx and transient network errors with exponential backoff.
    """
    if rate_limit_key:
        elapsed = time.monotonic() - _last_request_time.get(rate_limit_key, 0.0)
        if elapsed < delay:
            time.sleep(delay - elapsed)

    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)

    last_err: Exception | None = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=req_headers, data=data)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
            if rate_limit_key:
                _last_request_time[rate_limit_key] = time.monotonic()
            return data
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                wait = (2**attempt) * 5
                print(f"HTTP {e.code} from {url}; retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_err = e
            if attempt < max_retries - 1:
                wait = (2**attempt) * 5
                print(f"Network error ({e}); retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError(f"Unreachable; last error: {last_err}")


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------


def cache_root() -> Path:
    root = os.environ.get("ARXIV_SKILL_CACHE")
    if root:
        return Path(root)
    return Path.home() / ".cache" / "arxiv-skill"


def paper_dir(versioned_id: str) -> Path:
    # Old-style IDs contain '/', which cannot be a directory name.
    safe = versioned_id.replace("/", "_")
    d = cache_root() / safe
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
