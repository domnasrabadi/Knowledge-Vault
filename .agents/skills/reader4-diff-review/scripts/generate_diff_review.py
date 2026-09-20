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


def inline_diff(before: str, after: str) -> tuple[str, str]:
    matcher = difflib.SequenceMatcher(None, before, after, autojunk=False)
    left: list[str] = []
    right: list[str] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        old = esc(before[i1:i2])
        new = esc(after[j1:j2])
        if tag == "equal":
            left.append(old)
            right.append(new)
        elif tag == "delete":
            left.append(f'<mark class="char-del">{old}</mark>')
        elif tag == "insert":
            right.append(f'<mark class="char-add">{new}</mark>')
        else:
            left.append(f'<mark class="char-del">{old}</mark>')
            right.append(f'<mark class="char-add">{new}</mark>')
    return "".join(left), "".join(right)


def full_document_diff(before: list[str], after: list[str]) -> tuple[str, str, int, int, int]:
    matcher = difflib.SequenceMatcher(None, before, after, autojunk=False)
    left_rows: list[str] = []
    right_rows: list[str] = []
    slots = change_groups = added = deleted = 0

    def row(
        side: str,
        kind: str,
        number: int | None,
        content: str,
        slot: int,
        change: int | None,
    ) -> str:
        change_attr = f' data-change="{change}"' if change is not None else ""
        anchor = f' id="{side}-change-{change}"' if change is not None else ""
        display_number = str(number) if number is not None else ""
        return (
            f'<div class="line {kind}" data-slot="{slot}"{change_attr}{anchor}>'
            f'<span class="gutter">{display_number}</span><code>{content or "&nbsp;"}</code></div>'
        )

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        old_lines = before[i1:i2]
        new_lines = after[j1:j2]
        if tag == "equal":
            for offset, old in enumerate(old_lines):
                slots += 1
                left_rows.append(row("before", "context", i1 + offset + 1, esc(old), slots, None))
                right_rows.append(row("after", "context", j1 + offset + 1, esc(new_lines[offset]), slots, None))
            continue

        change_groups += 1
        for offset in range(max(len(old_lines), len(new_lines))):
            slots += 1
            old = old_lines[offset] if offset < len(old_lines) else ""
            new = new_lines[offset] if offset < len(new_lines) else ""
            old_number = i1 + offset + 1 if offset < len(old_lines) else None
            new_number = j1 + offset + 1 if offset < len(new_lines) else None
            marker = change_groups if offset == 0 else None
            if old_number is not None and new_number is not None:
                old_html, new_html = inline_diff(old, new)
                left_kind = right_kind = "replace"
                deleted += 1
                added += 1
            elif old_number is not None:
                old_html, new_html = esc(old), ""
                left_kind, right_kind = "delete", "ghost"
                deleted += 1
            else:
                old_html, new_html = "", esc(new)
                left_kind, right_kind = "ghost", "insert"
                added += 1
            left_rows.append(row("before", left_kind, old_number, old_html, slots, marker))
            right_rows.append(row("after", right_kind, new_number, new_html, slots, marker))

    return "".join(left_rows), "".join(right_rows), change_groups, added, deleted


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
) -> str:
    before_text = before_path.read_text(encoding="utf-8")
    after_text = after_path.read_text(encoding="utf-8")
    _, before_body = split_document(before_text)
    after_fields_list, after_body = split_document(after_text)
    after_fields = fields_dict(after_fields_list)
    before_lines = before_text.splitlines()
    after_lines = after_text.splitlines()
    before_document, after_document, change_groups, lines_added, lines_deleted = full_document_diff(
        before_lines, after_lines
    )
    similarity = token_similarity(before_body, after_body)
    title = extract_title(after_body, str(manifest.get("title", after_path.stem)))
    before_head = esc(Path(old_path).name or before_path.name)
    after_head = esc(after_path.name)

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reader4 Full Document Diff · {esc(title)}</title>
<style>
:root{{--ink:#152033;--muted:#64748b;--paper:#f8fafc;--card:#fff;--line:#dbe3ee;--blue:#2563eb;--green:#16805c;--red:#c2414b;--greenbg:#e7f7ef;--redbg:#fdecef;--gutter:#f1f5f9;--row:25px}}
*{{box-sizing:border-box}}html,body{{height:100%}}body{{margin:0;background:var(--paper);color:var(--ink);font:14px/1.5 Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.topbar{{height:6px;background:linear-gradient(90deg,#2563eb,#60a5fa 48%,#22c55e)}}main{{max-width:1800px;margin:auto;padding:24px}}
.badge{{display:inline-flex;padding:6px 10px;border:1px solid #bfdbfe;background:#eff6ff;color:#1d4ed8;border-radius:999px;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase}}h1{{font-size:clamp(27px,3vw,40px);line-height:1.1;letter-spacing:-.035em;margin:13px 0 6px}}.sub{{color:var(--muted);margin:0;max-width:900px}}
.summary{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}}.pill{{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:8px 11px;color:var(--muted)}}.pill b{{color:var(--ink);margin-left:7px;font-variant-numeric:tabular-nums}}.pill.add b{{color:var(--green)}}.pill.del b{{color:var(--red)}}
.viewer{{background:var(--card);border:1px solid var(--line);border-radius:13px;box-shadow:0 10px 30px rgba(30,41,59,.08);overflow:hidden}}.toolbar{{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:11px 14px;border-bottom:1px solid var(--line);background:#fff;flex-wrap:wrap}}.legend,.controls{{display:flex;align-items:center;gap:12px;flex-wrap:wrap}}.key{{display:flex;align-items:center;gap:6px;color:var(--muted);font-size:12px}}.swatch{{width:13px;height:13px;border-radius:3px}}.swatch.line-old{{background:var(--redbg);border:1px solid #efb8c0}}.swatch.line-new{{background:var(--greenbg);border:1px solid #a9dcc6}}.swatch.inline{{background:#ef9aa7}}
button{{border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:7px;padding:7px 10px;font-weight:700;cursor:pointer}}button:hover{{border-color:#93b4ee;background:#eff6ff}}label{{color:var(--muted);font-size:12px;display:flex;align-items:center;gap:6px}}
.heads,.panes{{display:grid;grid-template-columns:1fr 1fr}}.head{{display:flex;justify-content:space-between;padding:9px 13px;font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.06em}}.head.before{{color:var(--red);background:#fff7f8;border-right:1px solid var(--line)}}.head.after{{color:var(--green);background:#f4fbf8}}.head span{{font-weight:600;color:var(--muted);text-transform:none;letter-spacing:0}}
.pane{{height:min(72vh,820px);overflow:auto;scrollbar-gutter:stable;background:#fff}}.pane.before{{border-right:1px solid var(--line)}}.line{{display:flex;min-width:max-content;height:var(--row);line-height:var(--row);border-bottom:1px solid #f1f5f9;font:12px/25px ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}}.gutter{{position:sticky;left:0;z-index:1;width:54px;min-width:54px;padding-right:11px;text-align:right;color:#94a3b8;background:var(--gutter);border-right:1px solid var(--line);user-select:none}}.line code{{padding:0 10px;white-space:pre}}
.line.delete,.line.replace{{background:var(--redbg)}}.line.insert{{background:var(--greenbg)}}.line.ghost{{background:#f8fafc}}.line.ghost code{{opacity:0}}.line[data-change] .gutter::before{{content:'●';float:left;margin-left:7px;font-size:8px;color:var(--blue)}}mark{{color:inherit;border-radius:2px;padding:1px 0}}.char-del{{background:#ef9aa7;color:#6f1520;text-decoration:line-through;text-decoration-thickness:1px}}.char-add{{background:#8ed5b7;color:#084f38}}
.footer{{display:flex;justify-content:space-between;gap:16px;padding:10px 14px;border-top:1px solid var(--line);color:var(--muted);font-size:12px}}.sync-state{{color:var(--green);font-weight:700}}
@media(max-width:900px){{main{{padding:14px}}.heads,.panes{{grid-template-columns:1fr}}.pane{{height:48vh}}.pane.before,.head.before{{border-right:0;border-bottom:1px solid var(--line)}}.toolbar{{align-items:flex-start}}}}
</style>
</head>
<body><div class="topbar"></div><main>
<span class="badge">Reader4 · Full Document Diff</span>
<h1>{esc(title)}</h1>
<p class="sub">The complete before and after Markdown, line-aligned in two synchronized panes. Soft red/green marks changed lines; stronger inline marks isolate the exact changed characters.</p>
<div class="summary"><div class="pill">Change groups <b>{change_groups}</b></div><div class="pill add">Lines added <b>+{lines_added}</b></div><div class="pill del">Lines removed <b>−{lines_deleted}</b></div><div class="pill">Before <b>{len(before_lines)} lines</b></div><div class="pill">After <b>{len(after_lines)} lines</b></div><div class="pill">Raw similarity <b>{similarity:.1%}</b></div></div>
<section class="viewer" data-testid="full-document-diff">
  <div class="toolbar">
    <div class="legend"><span class="key"><i class="swatch line-old"></i>Removed/old line</span><span class="key"><i class="swatch line-new"></i>Added/new line</span><span class="key"><i class="swatch inline"></i>Exact character change</span></div>
    <div class="controls"><button id="previous" type="button">← Previous change</button><span id="position">Change 1 of {change_groups}</span><button id="next" type="button">Next change →</button><label><input id="sync" type="checkbox" checked> Sync vertical scroll</label></div>
  </div>
  <div class="heads"><div class="head before">Before <span>{before_head}</span></div><div class="head after">After <span>{after_head}</span></div></div>
  <div class="panes"><div class="pane before" id="before-pane" tabindex="0">{before_document}</div><div class="pane after" id="after-pane" tabindex="0">{after_document}</div></div>
  <div class="footer"><span><b>Reading model:</b> every row slot corresponds across both panes; blank rows preserve insertion/deletion alignment.</span><span class="sync-state" id="sync-state">Scroll linked</span></div>
</section>
</main>
<script>
const beforePane=document.getElementById('before-pane');
const afterPane=document.getElementById('after-pane');
const syncToggle=document.getElementById('sync');
const syncState=document.getElementById('sync-state');
let syncing=false;
function mirror(source,target){{if(syncing||!syncToggle.checked)return;syncing=true;target.scrollTop=source.scrollTop;requestAnimationFrame(()=>{{syncing=false}})}}
beforePane.addEventListener('scroll',()=>mirror(beforePane,afterPane),{{passive:true}});
afterPane.addEventListener('scroll',()=>mirror(afterPane,beforePane),{{passive:true}});
syncToggle.addEventListener('change',()=>{{syncState.textContent=syncToggle.checked?'Scroll linked':'Scroll independent';syncState.style.color=syncToggle.checked?'var(--green)':'var(--muted)';if(syncToggle.checked)afterPane.scrollTop=beforePane.scrollTop}});
const total={change_groups};let current=1;const position=document.getElementById('position');
function go(change){{if(!total)return;current=((change-1+total)%total)+1;const left=document.getElementById(`before-change-${{current}}`);const right=document.getElementById(`after-change-${{current}}`);if(left)beforePane.scrollTop=Math.max(0,left.offsetTop-beforePane.clientHeight*.35);if(right)afterPane.scrollTop=Math.max(0,right.offsetTop-afterPane.clientHeight*.35);position.textContent=`Change ${{current}} of ${{total}}`;}}
document.getElementById('previous').addEventListener('click',()=>go(current-1));
document.getElementById('next').addEventListener('click',()=>go(current+1));
if(!total){{document.getElementById('previous').disabled=true;document.getElementById('next').disabled=true;position.textContent='No changes'}}
</script></body></html>'''


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
    report = build_html(before, after, str(metadata.get("old_path", "")), args.doc_id, entry)
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
    render_parser.set_defaults(func=render)

    path_parser = commands.add_parser("show-path", help="print the default report path")
    path_parser.add_argument("--doc-id", required=True)
    path_parser.set_defaults(func=show_path)
    return root


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileNotFoundError, FileExistsError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)
