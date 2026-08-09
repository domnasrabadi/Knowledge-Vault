#!/usr/bin/env python3
"""Generate a standalone full-document Reader4 diff prototype."""

from __future__ import annotations

import argparse
import difflib
import html
from pathlib import Path


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def inline_diff(before: str, after: str) -> tuple[str, str]:
    if not before and not after:
        return "", ""
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


def aligned_lines(before: list[str], after: list[str]) -> tuple[str, str, int, int, int]:
    matcher = difflib.SequenceMatcher(None, before, after, autojunk=False)
    left_rows: list[str] = []
    right_rows: list[str] = []
    slots = changes = added = deleted = 0

    def row(side: str, kind: str, number: int | None, content: str, slot: int, change: int | None) -> str:
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

        changes += 1
        width = max(len(old_lines), len(new_lines))
        for offset in range(width):
            slots += 1
            old = old_lines[offset] if offset < len(old_lines) else ""
            new = new_lines[offset] if offset < len(new_lines) else ""
            old_number = i1 + offset + 1 if offset < len(old_lines) else None
            new_number = j1 + offset + 1 if offset < len(new_lines) else None
            marker = changes if offset == 0 else None
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

    return "".join(left_rows), "".join(right_rows), changes, added, deleted


def build(before_path: Path, after_path: Path) -> str:
    before_text = before_path.read_text(encoding="utf-8")
    after_text = after_path.read_text(encoding="utf-8")
    before = before_text.splitlines()
    after = after_text.splitlines()
    left, right, changes, added, deleted = aligned_lines(before, after)
    title = after_path.stem.lstrip("⭐️ ")
    similarity = difflib.SequenceMatcher(None, before_text, after_text, autojunk=False).ratio()
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
<span class="badge">Experimental · Full Document Diff</span>
<h1>{esc(title)}</h1>
<p class="sub">The complete before and after Markdown, line-aligned in two synchronized panes. Soft red/green marks changed lines; stronger inline marks isolate the exact changed characters.</p>
<div class="summary"><div class="pill">Change groups <b>{changes}</b></div><div class="pill add">Lines added <b>+{added}</b></div><div class="pill del">Lines removed <b>−{deleted}</b></div><div class="pill">Before <b>{len(before)} lines</b></div><div class="pill">After <b>{len(after)} lines</b></div><div class="pill">Raw similarity <b>{similarity:.1%}</b></div></div>
<section class="viewer" data-testid="full-document-diff">
  <div class="toolbar">
    <div class="legend"><span class="key"><i class="swatch line-old"></i>Removed/old line</span><span class="key"><i class="swatch line-new"></i>Added/new line</span><span class="key"><i class="swatch inline"></i>Exact character change</span></div>
    <div class="controls"><button id="previous" type="button">← Previous change</button><span id="position">Change 1 of {changes}</span><button id="next" type="button">Next change →</button><label><input id="sync" type="checkbox" checked> Sync vertical scroll</label></div>
  </div>
  <div class="heads"><div class="head before">Before <span>{esc(before_path.name)}</span></div><div class="head after">After <span>{esc(after_path.name)}</span></div></div>
  <div class="panes"><div class="pane before" id="before-pane" tabindex="0">{left}</div><div class="pane after" id="after-pane" tabindex="0">{right}</div></div>
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
const total={changes};let current=1;const position=document.getElementById('position');
function go(change){{if(!total)return;current=((change-1+total)%total)+1;const left=document.getElementById(`before-change-${{current}}`);const right=document.getElementById(`after-change-${{current}}`);if(left)beforePane.scrollTop=Math.max(0,left.offsetTop-beforePane.clientHeight*.35);if(right)afterPane.scrollTop=Math.max(0,right.offsetTop-afterPane.clientHeight*.35);position.textContent=`Change ${{current}} of ${{total}}`;}}
document.getElementById('previous').addEventListener('click',()=>go(current-1));
document.getElementById('next').addEventListener('click',()=>go(current+1));
if(!total){{document.getElementById('previous').disabled=true;document.getElementById('next').disabled=true;position.textContent='No changes'}}
</script></body></html>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", required=True, type=Path)
    parser.add_argument("--after", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build(args.before, args.after), encoding="utf-8")
    print(args.output.resolve())


if __name__ == "__main__":
    main()
