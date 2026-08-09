#!/usr/bin/env python3
"""Create a self-contained HTML receipt for a Reader4 note review."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import html
import json
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


CANONICAL_FIELDS = [
    "type",
    "status",
    "quality",
    "topics",
    "source",
    "created",
    "published",
    "author",
    "flashcards",
    "updated",
]


def workspace_root() -> Path:
    return Path(tempfile.gettempdir()) / "reader4-diff-review"


def safe_doc_id(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-.")
    if not safe:
        raise ValueError("doc_id must contain at least one safe character")
    return safe


def review_dir(doc_id: str) -> Path:
    return workspace_root() / safe_doc_id(doc_id)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_document(text: str) -> tuple[list[tuple[str, str]], list[str]]:
    lines = text.splitlines()
    fields: list[tuple[str, str]] = []
    body_start = 0
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                body_start = index + 1
                break
            match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[index])
            if match:
                fields.append((match.group(1), match.group(2)))
    return fields, lines[body_start:]


def fields_dict(fields: list[tuple[str, str]]) -> dict[str, str]:
    return {key: value for key, value in fields}


def field_order(before: dict[str, str], after: dict[str, str]) -> list[str]:
    extras = sorted((set(before) | set(after)) - set(CANONICAL_FIELDS))
    return [key for key in CANONICAL_FIELDS if key in before or key in after] + extras


def token_similarity(before_lines: list[str], after_lines: list[str]) -> float:
    def tokens(lines: list[str]) -> list[str]:
        text_value = "\n".join(lines)
        text_value = re.sub(r"<[^>]+>", " ", text_value)
        return re.findall(r"[\w’']+", text_value.casefold(), flags=re.UNICODE)

    left = tokens(before_lines)
    right = tokens(after_lines)
    if not left and not right:
        return 1.0
    return difflib.SequenceMatcher(None, left, right, autojunk=False).ratio()


def extract_title(body: list[str], fallback: str) -> str:
    for line in body:
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return re.sub(r"[*_`]", "", match.group(1))
    return fallback


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def safe_link(value: object) -> str:
    url = str(value or "")
    parsed = urlparse(url)
    return url if parsed.scheme in {"http", "https"} and parsed.netloc else ""


def render_frontmatter(before: dict[str, str], after: dict[str, str]) -> tuple[str, int]:
    rows = []
    changed = 0
    for key in field_order(before, after):
        left = before.get(key, "")
        right = after.get(key, "")
        is_changed = left != right
        changed += int(is_changed)
        row_class = "changed" if is_changed else "unchanged"
        rows.append(
            f'<tr class="{row_class}"><th>{esc(key)}</th>'
            f'<td>{esc(left) or "<span class=empty>empty</span>"}</td>'
            f'<td>{esc(right) or "<span class=empty>empty</span>"}</td></tr>'
        )
    return "\n".join(rows), changed


def diff_hunks(before: list[str], after: list[str], context: int) -> tuple[str, int, int, int]:
    matcher = difflib.SequenceMatcher(None, before, after, autojunk=False)
    groups = list(matcher.get_grouped_opcodes(context))
    sections: list[str] = []
    added = deleted = 0

    for number, group in enumerate(groups, start=1):
        rows: list[str] = []
        old_start = group[0][1] + 1
        new_start = group[0][3] + 1
        for tag, i1, i2, j1, j2 in group:
            left = before[i1:i2]
            right = after[j1:j2]
            if tag == "equal":
                for offset, line in enumerate(left):
                    rows.append(diff_row("context", i1 + offset + 1, line, j1 + offset + 1, right[offset]))
            elif tag == "delete":
                deleted += len(left)
                for offset, line in enumerate(left):
                    rows.append(diff_row("delete", i1 + offset + 1, line, None, ""))
            elif tag == "insert":
                added += len(right)
                for offset, line in enumerate(right):
                    rows.append(diff_row("insert", None, "", j1 + offset + 1, line))
            else:
                deleted += len(left)
                added += len(right)
                width = max(len(left), len(right))
                for offset in range(width):
                    rows.append(
                        diff_row(
                            "replace",
                            i1 + offset + 1 if offset < len(left) else None,
                            left[offset] if offset < len(left) else "",
                            j1 + offset + 1 if offset < len(right) else None,
                            right[offset] if offset < len(right) else "",
                        )
                    )
        sections.append(
            f'<section class="hunk"><h3>Change {number} '
            f'<span>before L{old_start} · after L{new_start}</span></h3>'
            '<div class="diff-scroll"><table class="diff-table"><thead><tr>'
            '<th colspan="2">Before</th><th colspan="2">After</th>'
            f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>'
        )

    if not sections:
        sections.append('<div class="no-change">No body changes detected.</div>')
    return "\n".join(sections), len(groups), added, deleted


def diff_row(kind: str, old_number: int | None, old_line: str, new_number: int | None, new_line: str) -> str:
    return (
        f'<tr class="{kind}"><td class="ln">{old_number or ""}</td>'
        f'<td><code>{esc(old_line)}</code></td><td class="ln">{new_number or ""}</td>'
        f'<td><code>{esc(new_line)}</code></td></tr>'
    )


def manifest_entry(path: Path | None, doc_id: str) -> dict[str, object]:
    if path is None or not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    entry = payload.get(doc_id, {}) if isinstance(payload, dict) else {}
    return entry if isinstance(entry, dict) else {}


def timeline(status: str, after_exists: bool) -> str:
    stages = [
        ("Captured", True),
        ("Applied", after_exists),
        ("Filed", status in {"filed", "archived"}),
        ("Archived", status == "archived"),
    ]
    return "".join(
        f'<li class="{"done" if done else "pending"}"><span>{"✓" if done else "·"}</span>{esc(label)}</li>'
        for label, done in stages
    )


def build_html(
    before_path: Path,
    after_path: Path,
    old_path: str,
    doc_id: str,
    manifest: dict[str, object],
    context: int,
) -> str:
    before_text = before_path.read_text(encoding="utf-8")
    after_text = after_path.read_text(encoding="utf-8")
    before_fields_list, before_body = split_document(before_text)
    after_fields_list, after_body = split_document(after_text)
    before_fields = fields_dict(before_fields_list)
    after_fields = fields_dict(after_fields_list)
    frontmatter_rows, metadata_changed = render_frontmatter(before_fields, after_fields)
    hunks_html, hunk_count, lines_added, lines_deleted = diff_hunks(before_body, after_body, context)
    similarity = token_similarity(before_body, after_body)
    similarity_class = "good" if similarity >= 0.99 else "warn" if similarity >= 0.95 else "risk"
    status = str(manifest.get("status", "unknown"))
    title = extract_title(after_body, str(manifest.get("title", after_path.stem)))
    generated_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    path_changed = str(Path(old_path)) != str(after_path)
    pipeline_class = "good" if status == "archived" else "risk"
    source_url = safe_link(manifest.get("source_url", after_fields.get("source", "")))
    source_html = f'<a href="{esc(source_url)}">Open source</a>' if source_url else "No source URL"

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reader4 Review · {esc(title)}</title>
<style>
:root {{ color-scheme: dark; --bg:#0b1020; --panel:#121a2e; --panel2:#172139; --text:#e8edf7; --muted:#9eabc2; --line:#2b3855; --green:#57d39b; --red:#ff7d8b; --amber:#f7c76b; --blue:#77a9ff; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:linear-gradient(145deg,#0b1020,#11172a 55%,#0b1020); color:var(--text); font:14px/1.5 ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
main {{ max-width:1440px; margin:0 auto; padding:34px 28px 70px; }}
h1 {{ margin:0 0 8px; font-size:clamp(25px,3vw,40px); line-height:1.15; letter-spacing:-.025em; }}
h2 {{ margin:0 0 14px; font-size:18px; }}
h3 {{ margin:0; font-size:13px; color:var(--muted); font-weight:600; }}
h3 span {{ float:right; font-weight:500; }}
a {{ color:#9ec1ff; }}
.eyebrow {{ color:var(--blue); font-weight:750; letter-spacing:.1em; text-transform:uppercase; font-size:12px; }}
.subtitle {{ color:var(--muted); max-width:900px; }}
.meta-line {{ display:flex; flex-wrap:wrap; gap:10px 18px; color:var(--muted); margin-top:14px; }}
.cards {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; margin:26px 0; }}
.card,.panel,.hunk {{ background:rgba(18,26,46,.93); border:1px solid var(--line); border-radius:14px; box-shadow:0 14px 34px rgba(0,0,0,.18); }}
.card {{ padding:15px 17px; }}
.card b {{ display:block; font-size:23px; margin-top:3px; }}
.label {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.06em; }}
.good b,.good strong {{ color:var(--green); }} .warn b {{ color:var(--amber); }} .risk b,.risk strong {{ color:var(--red); }}
.panel {{ padding:20px; margin:14px 0; }}
.timeline {{ display:grid; grid-template-columns:repeat(4,1fr); gap:8px; list-style:none; padding:0; margin:0; }}
.timeline li {{ display:flex; align-items:center; gap:8px; color:var(--muted); border-top:2px solid var(--line); padding-top:10px; }}
.timeline li span {{ display:grid; place-items:center; width:22px; height:22px; border-radius:50%; background:var(--panel2); }}
.timeline .done {{ color:var(--text); border-color:var(--green); }} .timeline .done span {{ background:#173b35; color:var(--green); }}
.path-grid {{ display:grid; grid-template-columns:1fr 28px 1fr; gap:12px; align-items:center; }}
.path {{ background:#0c1325; border:1px solid var(--line); border-radius:10px; padding:12px; overflow-wrap:anywhere; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:12px; }}
.arrow {{ color:var(--muted); text-align:center; font-size:20px; }}
.table-scroll,.diff-scroll {{ overflow-x:auto; }}
table {{ width:100%; border-collapse:collapse; }}
th,td {{ border-bottom:1px solid var(--line); padding:9px 10px; text-align:left; vertical-align:top; }}
th {{ color:var(--muted); font-size:12px; }}
.frontmatter th:first-child {{ width:130px; color:var(--text); }}
.frontmatter tr.changed td {{ background:rgba(119,169,255,.08); }} .frontmatter tr.unchanged {{ opacity:.55; }}
.empty {{ color:var(--muted); font-style:italic; }}
.hunk {{ margin:12px 0; overflow:hidden; }} .hunk h3 {{ padding:11px 14px; background:var(--panel2); }}
.diff-table {{ table-layout:fixed; min-width:900px; }}
.diff-table th {{ width:50%; }} .diff-table .ln {{ width:48px; color:#7584a0; text-align:right; user-select:none; background:#0c1325; }}
.diff-table td {{ padding:5px 8px; }} .diff-table code {{ white-space:pre-wrap; overflow-wrap:anywhere; font:12px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace; }}
.diff-table tr.delete td:nth-child(-n+2) {{ background:rgba(255,125,139,.14); }}
.diff-table tr.insert td:nth-child(n+3) {{ background:rgba(87,211,155,.13); }}
.diff-table tr.replace td:nth-child(-n+2) {{ background:rgba(255,125,139,.14); }}
.diff-table tr.replace td:nth-child(n+3) {{ background:rgba(87,211,155,.13); }}
.diff-table tr.context {{ opacity:.68; }}
.no-change {{ color:var(--muted); padding:18px; border:1px dashed var(--line); border-radius:12px; }}
details {{ margin-top:12px; }} summary {{ cursor:pointer; color:var(--blue); }}
.raw-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:12px; }}
pre {{ margin:0; padding:14px; max-height:520px; overflow:auto; background:#0c1325; border:1px solid var(--line); border-radius:10px; white-space:pre-wrap; font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace; }}
.footnote {{ color:var(--muted); font-size:12px; margin-top:18px; }}
@media (max-width:850px) {{ main {{ padding:22px 14px 50px; }} .cards {{ grid-template-columns:1fr 1fr; }} .timeline {{ grid-template-columns:1fr 1fr; }} .path-grid {{ grid-template-columns:1fr; }} .arrow {{ transform:rotate(90deg); }} .raw-grid {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body>
<main>
  <div class="eyebrow">Reader4 review receipt</div>
  <h1>{esc(title)}</h1>
  <div class="subtitle">A deterministic comparison of the captured Inbox note and the filed result.</div>
  <div class="meta-line"><span>Doc ID: <code>{esc(doc_id)}</code></span><span>Generated: {esc(generated_at)}</span><span>{source_html}</span></div>

  <section class="cards" data-testid="summary">
    <div class="card {pipeline_class}"><span class="label">Pipeline</span><b>{esc(status.title())}</b></div>
    <div class="card"><span class="label">Metadata fields changed</span><b>{metadata_changed}</b></div>
    <div class="card"><span class="label">Ordered body hunks</span><b>{hunk_count}</b><small>+{lines_added} / −{lines_deleted} lines</small></div>
    <div class="card {similarity_class}"><span class="label">Prose similarity</span><b>{similarity:.1%}</b><small>formatting-insensitive signal</small></div>
  </section>

  <section class="panel">
    <h2>Pipeline order</h2>
    <ol class="timeline">{timeline(status, after_path.exists())}</ol>
  </section>

  <section class="panel">
    <h2>Path {"changed" if path_changed else "unchanged"}</h2>
    <div class="path-grid"><div class="path">{esc(old_path)}</div><div class="arrow">→</div><div class="path">{esc(after_path)}</div></div>
  </section>

  <section class="panel" data-testid="frontmatter-table">
    <h2>Frontmatter</h2>
    <div class="table-scroll"><table class="frontmatter"><thead><tr><th>Field</th><th>Before</th><th>After</th></tr></thead><tbody>{frontmatter_rows}</tbody></table></div>
  </section>

  <section data-testid="diff-hunks">
    <h2>Body changes, in source order</h2>
    {hunks_html}
  </section>

  <section class="panel">
    <h2>Full source check</h2>
    <details><summary>Show complete before and after Markdown</summary><div class="raw-grid"><pre>{esc(before_text)}</pre><pre>{esc(after_text)}</pre></div></details>
    <p class="footnote">Prose similarity ignores Markdown punctuation, HTML tags, capitalization, and whitespace. It is a triage signal—not a guarantee that meaning was preserved.</p>
  </section>
</main>
</body>
</html>'''


def snapshot(args: argparse.Namespace) -> int:
    note = Path(args.note).expanduser().resolve()
    if not note.is_file():
        raise FileNotFoundError(f"note not found: {note}")
    target_dir = review_dir(args.doc_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    before = target_dir / "before.md"
    metadata = target_dir / "snapshot.json"
    if before.exists() and not args.force:
        raise FileExistsError(f"snapshot already exists: {before} (use --force only if the note is untouched)")
    shutil.copy2(note, before)
    metadata.write_text(
        json.dumps(
            {
                "doc_id": args.doc_id,
                "old_path": str(note),
                "captured_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
                "sha256": sha256(before),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(before)
    return 0


def render(args: argparse.Namespace) -> int:
    target_dir = review_dir(args.doc_id)
    before = target_dir / "before.md"
    metadata_path = target_dir / "snapshot.json"
    after = Path(args.after).expanduser().resolve()
    if not before.is_file() or not metadata_path.is_file():
        raise FileNotFoundError(f"snapshot missing for doc_id {args.doc_id}")
    if not after.is_file():
        raise FileNotFoundError(f"filed note not found: {after}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if sha256(before) != metadata.get("sha256"):
        raise ValueError("before snapshot checksum mismatch; refusing to render an untrusted comparison")
    manifest_path = Path(args.manifest).expanduser().resolve() if args.manifest else None
    entry = manifest_entry(manifest_path, args.doc_id)
    output = Path(args.output).expanduser().resolve() if args.output else target_dir / "review.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    report = build_html(before, after, str(metadata.get("old_path", "")), args.doc_id, entry, args.context_lines)
    output.write_text(report, encoding="utf-8")
    print(output)
    return 0


def show_path(args: argparse.Namespace) -> int:
    print(review_dir(args.doc_id) / "review.html")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    snapshot_parser = commands.add_parser("snapshot", help="capture the untouched Inbox note")
    snapshot_parser.add_argument("--note", required=True)
    snapshot_parser.add_argument("--doc-id", required=True)
    snapshot_parser.add_argument("--force", action="store_true")
    snapshot_parser.set_defaults(func=snapshot)

    render_parser = commands.add_parser("render", help="render the before/after HTML receipt")
    render_parser.add_argument("--doc-id", required=True)
    render_parser.add_argument("--after", required=True)
    render_parser.add_argument("--manifest")
    render_parser.add_argument("--output")
    render_parser.add_argument("--context-lines", type=int, default=2)
    render_parser.set_defaults(func=render)

    path_parser = commands.add_parser("show-path", help="print the default report path")
    path_parser.add_argument("--doc-id", required=True)
    path_parser.set_defaults(func=show_path)
    return root


def main() -> int:
    args = parser().parse_args()
    if getattr(args, "context_lines", 0) < 0:
        raise ValueError("context lines cannot be negative")
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileNotFoundError, FileExistsError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)
