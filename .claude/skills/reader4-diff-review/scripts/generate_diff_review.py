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
        ("Captured", "Untouched Inbox snapshot", True),
        ("Applied", "Reviewed result present", after_exists),
        ("Filed", "Manifest path updated", status in {"filed", "archived"}),
        ("Archived", "Removed from Shortlist", status == "archived"),
    ]
    return "".join(
        f'<li class="{"done" if done else "pending"}"><b>{number:02d} · {esc(label)}</b>'
        f'<span>{esc(description)}</span></li>'
        for number, (label, description, done) in enumerate(stages, start=1)
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
    fidelity_passed = similarity >= 0.99 and status == "archived"
    fidelity_class = "passed" if fidelity_passed else "review"
    fidelity_icon = "✓" if fidelity_passed else "!"
    fidelity_title = "Fidelity gate passed" if fidelity_passed else "Fidelity review required"
    fidelity_copy = (
        "The pipeline is archived and the formatting-insensitive prose signal is at least 99%. "
        "Use the ordered evidence below to confirm the changes are expected."
        if fidelity_passed
        else "The pipeline is incomplete or the prose signal is below 99%. Inspect every body hunk before accepting this review."
    )
    source_url = safe_link(manifest.get("source_url", after_fields.get("source", "")))
    source_html = f'<a href="{esc(source_url)}">Open source</a>' if source_url else "No source URL"

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reader4 Review · {esc(title)}</title>
<style>
:root{{--ink:#152033;--muted:#64748b;--paper:#f8fafc;--card:#fff;--line:#dbe3ee;--blue:#2563eb;--green:#16805c;--red:#c2414b;--amber:#a16207;--greenbg:#edf9f4;--redbg:#fff2f3}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font:14px/1.55 Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.topbar{{height:6px;background:linear-gradient(90deg,#2563eb,#60a5fa 48%,#22c55e)}}main{{max-width:1460px;margin:auto;padding:28px}}
h1{{font-size:clamp(29px,3.2vw,42px);line-height:1.1;letter-spacing:-.035em;margin:14px 0 6px}}h2{{font-size:17px;margin:0 0 14px}}a{{color:var(--blue)}}
.receipt-label{{display:inline-flex;gap:8px;align-items:center;padding:6px 10px;border:1px solid #bfdbfe;background:#eff6ff;color:#1d4ed8;border-radius:999px;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase}}
.subtitle{{color:var(--muted);max-width:790px;margin:0}}.meta-line{{display:flex;flex-wrap:wrap;gap:8px 18px;color:var(--muted);margin-top:12px;font-size:12px}}
.shell{{display:grid;grid-template-columns:265px minmax(0,1fr);gap:22px;margin-top:26px}}aside{{position:sticky;top:18px;align-self:start}}.box{{background:var(--card);border:1px solid var(--line);border-radius:12px;box-shadow:0 8px 22px rgba(30,41,59,.05)}}
.receipt{{padding:18px}}.receipt .id{{font:11px ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--muted);overflow-wrap:anywhere}}.status{{display:flex;align-items:center;gap:9px;margin:15px 0;font-size:20px;font-weight:800}}.status.good{{color:var(--green)}}.status.risk{{color:var(--red)}}
.status i{{width:29px;height:29px;display:grid;place-items:center;border-radius:50%;font-style:normal;background:var(--greenbg)}}.status.risk i{{background:var(--redbg)}}.metric{{display:flex;justify-content:space-between;border-top:1px solid var(--line);padding:10px 0;gap:8px}}.metric span{{color:var(--muted)}}.metric b{{font-variant-numeric:tabular-nums;text-align:right}}.metric .good{{color:var(--green)}}.metric .warn{{color:var(--amber)}}.metric .risk{{color:var(--red)}}
nav{{padding:12px;margin-top:12px}}nav a{{display:block;color:var(--muted);text-decoration:none;padding:8px 10px;border-radius:7px}}nav a:hover{{background:#f1f5f9;color:var(--blue)}}
.content{{min-width:0}}.panel{{padding:20px;margin-bottom:16px}}.kicker{{color:var(--blue);font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.08em}}
.timeline{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;list-style:none;padding:0;margin:0}}.timeline li{{border-top:3px solid var(--line);padding-top:10px;color:var(--muted)}}.timeline li b{{display:block;color:inherit}}.timeline li span{{display:block;font-size:11px}}.timeline .done{{border-color:var(--green);color:var(--ink)}}
.path-grid{{display:grid;grid-template-columns:1fr 34px 1fr;gap:10px;align-items:center}}.path{{display:block;background:#f1f5f9;padding:12px;border-radius:8px;border:1px solid var(--line);overflow-wrap:anywhere;font:12px ui-monospace,SFMono-Regular,Menlo,monospace}}.arrow{{text-align:center;color:var(--blue);font-size:22px}}
.table-scroll,.diff-scroll{{overflow-x:auto}}table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}}.frontmatter th:first-child,.frontmatter td:first-child{{font-weight:750;width:120px;color:var(--ink)}}.frontmatter .changed td{{background:#f7faff}}.frontmatter .unchanged{{color:#94a3b8}}.empty{{color:var(--muted);font-style:italic}}
.hunk{{border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:12px 0;background:var(--card)}}.hunk h3{{display:flex;justify-content:space-between;gap:15px;background:#f1f5f9;padding:9px 12px;margin:0;font-size:12px;font-weight:750}}.hunk h3 span{{color:var(--muted);font-weight:600}}
.diff-table{{table-layout:fixed;min-width:760px}}.diff-table thead th{{width:50%;padding:7px 11px;font-size:10px;font-weight:800}}.diff-table thead th:first-child{{color:var(--red);background:var(--redbg)}}.diff-table thead th:last-child{{color:var(--green);background:var(--greenbg)}}.diff-table .ln{{width:42px;color:#94a3b8;text-align:right;user-select:none;background:#f8fafc}}.diff-table td{{padding:5px 8px}}.diff-table td:nth-child(2){{border-right:1px solid var(--line)}}.diff-table code{{white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}}.diff-table tr.delete td:nth-child(-n+2),.diff-table tr.replace td:nth-child(-n+2){{background:var(--redbg);color:#8f2732}}.diff-table tr.insert td:nth-child(n+3),.diff-table tr.replace td:nth-child(n+3){{background:var(--greenbg);color:#0d6547}}.diff-table tr.context{{color:#64748b}}
.no-change{{color:var(--muted);padding:18px;border:1px dashed var(--line);border-radius:10px}}.gate{{display:flex;gap:14px;align-items:center;border-left:4px solid var(--green)}}.gate.review{{border-left-color:var(--red)}}.gate-icon{{font-size:28px;color:var(--green)}}.gate.review .gate-icon{{color:var(--red)}}.gate strong{{font-size:17px}}.gate p{{margin:2px 0;color:var(--muted)}}
details summary{{cursor:pointer;color:var(--blue);font-weight:700}}.raw-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}}pre{{margin:0;padding:14px;max-height:520px;overflow:auto;background:#f8fafc;border:1px solid var(--line);border-radius:8px;white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}}.footnote{{color:var(--muted);font-size:12px;margin:14px 0 0}}
@media(max-width:900px){{main{{padding:18px}}.shell{{grid-template-columns:1fr}}aside{{position:static}}.timeline{{grid-template-columns:1fr 1fr}}.path-grid{{grid-template-columns:1fr}}.arrow{{transform:rotate(90deg)}}.raw-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="topbar"></div><main>
  <span class="receipt-label">Reader4 · Audit Ledger</span>
  <h1>{esc(title)}</h1>
  <p class="subtitle">A precise, document-first comparison of the captured Inbox note and the filed result.</p>
  <div class="meta-line"><span>Doc ID: <code>{esc(doc_id)}</code></span><span>Generated: {esc(generated_at)}</span><span>{source_html}</span></div>
  <div class="shell">
    <aside>
      <section class="box receipt" data-testid="summary">
        <div class="kicker">Reader4 receipt</div>
        <div class="status {pipeline_class}"><i>{"✓" if status == "archived" else "!"}</i>{esc(status.title())}</div>
        <div class="id">{esc(doc_id)}</div>
        <div class="metric"><span>Metadata changes</span><b>{metadata_changed}</b></div>
        <div class="metric"><span>Body hunks</span><b>{hunk_count}</b></div>
        <div class="metric"><span>Line delta</span><b>+{lines_added} / −{lines_deleted}</b></div>
        <div class="metric"><span>Prose similarity</span><b class="{similarity_class}">{similarity:.1%}</b></div>
      </section>
      <nav class="box"><a href="#pipeline">Pipeline</a><a href="#path">Path</a><a href="#metadata">Frontmatter</a><a href="#body">Body changes</a><a href="#fidelity">Fidelity gate</a><a href="#raw">Full source</a></nav>
    </aside>
    <div class="content">
      <section class="box panel" id="pipeline"><h2>Pipeline order</h2><ol class="timeline">{timeline(status, after_path.exists())}</ol></section>
      <section class="box panel" id="path"><div class="kicker">Location change</div><h2>Path {"changed" if path_changed else "unchanged"}</h2><div class="path-grid"><code class="path">{esc(old_path)}</code><div class="arrow">→</div><code class="path">{esc(after_path)}</code></div></section>
      <section class="box panel" id="metadata" data-testid="frontmatter-table"><div class="kicker">Canonical schema</div><h2>Frontmatter comparison</h2><div class="table-scroll"><table class="frontmatter"><thead><tr><th>Field</th><th>Before</th><th>After</th></tr></thead><tbody>{frontmatter_rows}</tbody></table></div></section>
      <section class="box panel" id="body" data-testid="diff-hunks"><div class="kicker">Ordered evidence</div><h2>Body changes, in source order</h2>{hunks_html}</section>
      <section class="box panel gate {fidelity_class}" id="fidelity"><div class="gate-icon">{fidelity_icon}</div><div><strong>{fidelity_title}</strong><p>{fidelity_copy}</p></div></section>
      <section class="box panel" id="raw"><details><summary>Show complete before and after Markdown</summary><div class="raw-grid"><pre>{esc(before_text)}</pre><pre>{esc(after_text)}</pre></div></details><p class="footnote">Prose similarity ignores Markdown punctuation, HTML tags, capitalization, and whitespace. It is a triage signal—not a guarantee that meaning was preserved.</p></section>
    </div>
  </div>
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
