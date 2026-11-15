import re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import *
CAP = 400
tok = lambda s: len(s) // 4   # estimate: tiktoken is not installed
def blocks(lines):
    out, cur, fence = [], [], False
    for ln in lines:
        if ln.lstrip().startswith("```"): fence = not fence; cur.append(ln); continue
        if not fence and ln.strip() == "":
            if cur: out.append("\n".join(cur)); cur = []
        else: cur.append(ln)
    if cur: out.append("\n".join(cur))
    return out
def split_big(b):
    if tok(b) <= CAP or b.lstrip().startswith("```"): return [b]
    parts, cur = [], []
    for ln in b.split("\n"):
        if re.match(r"^(?:[-*+]|\d+\.)\s", ln) and cur: parts.append("\n".join(cur)); cur = []
        cur.append(ln)
    if cur: parts.append("\n".join(cur))
    if len(parts) == 1: parts = re.split(r"(?<=[.!?])\s+", b)
    return parts
def pack(bl):
    out, cur = [], []
    bl = [x for b in bl for x in split_big(b)]
    for b in bl:
        if cur and tok("\n\n".join(cur + [b])) > CAP: out.append("\n\n".join(cur)); cur = []
        cur.append(b)
    if cur: out.append("\n\n".join(cur))
    return out
allp, notes = [], []
for nid, rel in NOTES:
    t = open(os.path.join(VAULT, rel)).read()
    fm = {}
    if t.startswith("---"):
        e = t.index("\n---", 3)
        for ln in t[3:e].strip().split("\n"):
            k, _, v = ln.partition(":"); fm[k.strip()] = v.strip()
        t = t[e + 4:]
    title = re.sub(r"^[⭐️\s]+", "", os.path.basename(rel)[:-3])
    notes.append({"id": nid, "path": rel, "title": title, **{k: fm.get(k, "") for k in ["type","status","quality","published","created","author"]}})
    stack, sect, sections, fence = [], [], [], False
    for ln in t.split("\n"):
        if ln.lstrip().startswith("```"): fence = not fence
        m = None if fence else re.match(r"^(#{1,6})\s+(.*)", ln)
        if m:
            sections.append((list(stack), sect)); sect = []
            lvl = len(m.group(1)); stack = [s for s in stack if s[0] < lvl] + [(lvl, m.group(2).strip())]
        else: sect.append(ln)
    sections.append((list(stack), sect))
    i = 0
    for si, (st, lines) in enumerate(sections):
        bc = " > ".join([title] + [s[1] for s in st if s[1] != title])
        for p in pack(blocks(lines)):
            i += 1
            allp.append({"id": f"{nid}-p{i:02d}", "note": nid, "section": f"{nid}-s{si:02d}", "breadcrumb": bc, "text": p, "tokens_est": tok(p)})
save("notes.json", notes); save("passages.json", allp)
for n in notes:
    ps = [p for p in allp if p["note"] == n["id"]]
    print(n["id"], n["title"], "| passages", len(ps), "| max tok", max(p["tokens_est"] for p in ps), "| over cap", sum(p["tokens_est"] > CAP for p in ps), "| sections", len({p["section"] for p in ps}))
    user = "\n".join(f'<passage id="{p["id"]}" breadcrumb="{p["breadcrumb"]}">{p["text"]}</passage>' for p in ps) + "\n\nReturn the mentions in these passages."
    write_call(f"P1-{n['id']}", "P1", user)
