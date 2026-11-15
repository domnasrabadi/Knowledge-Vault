# usage: p2_build.py n1   -> validates P1 output, exact-matches against the Registry, writes the P2 call for the rest
import sys, os, difflib
sys.path.insert(0, os.path.dirname(__file__))
from common import *
nid = sys.argv[1]
P = {p["id"]: p for p in load("passages.json")}
note = [n for n in load("notes.json") if n["id"] == nid][0]
reg = load("registry.json") if os.path.exists(os.path.join(ROOT, "data", "registry.json")) else []
ms = read_out(f"P1-{nid}")["mentions"]
stats = dict(returned=len(ms), bad_passage=0, text_not_found=0, offset_wrong=0)
seen, uniq, per_passage = {}, [], []
for m in ms:
    p = P.get(m["passage_id"])
    if not p or p["note"] != nid: stats["bad_passage"] += 1; continue
    if m["text"] not in p["text"]: stats["text_not_found"] += 1; continue
    if p["text"][m["start"]:m["end"]] != m["text"]: stats["offset_wrong"] += 1
    k = norm(m["text"]); per_passage.append({"passage_id": p["id"], "text": m["text"], "key": k})
    if k not in seen: seen[k] = m; uniq.append((k, m, p))
index = {}
for e in reg:
    for nm in [e["canonical_name"]] + e["aliases"]: index.setdefault(norm(nm), e["id"])
exact = {k: index[k] for k, _, _ in uniq if k in index}
def sim(k, e):
    best = 0
    for nm in [e["canonical_name"]] + e["aliases"]:
        n = norm(nm); r = difflib.SequenceMatcher(None, k, n).ratio()
        a, b = set(k.split()), set(n.split()); j = len(a & b) / max(1, len(a | b))
        best = max(best, 0.6 * r + 0.4 * j)
    return best
items, todo = [], []
for k, m, p in uniq:
    if k in exact: continue
    cands = sorted(reg, key=lambda e: -sim(k, e))[:5]
    cl = "\n".join(f'- {e["id"]} | {e["kind"]} | {e["canonical_name"]} | aliases: {", ".join(e["aliases"]) or "none"} | {e["definition"]}' for e in cands) or "(the Registry has no similar entries yet)"
    todo.append({"item": len(todo) + 1, "key": k, "text": m["text"], "kind": m["kind"], "passage_id": p["id"], "candidates": [e["id"] for e in cands]})
    items.append(f'<item n="{len(todo)}">\n<mention kind="{m["kind"]}">{m["text"]}</mention>\n<source>{note["title"]}</source>\n<breadcrumb>{p["breadcrumb"]}</breadcrumb>\n<passage>\n{p["text"]}\n</passage>\n<candidates>\n{cl}\n</candidates>\n</item>')
user = ("This message contains " + str(len(todo)) + " separate items. Treat each item as its own independent request: for each, decide which Registry entry, if any, the mention refers to, exactly as the system prompt describes. Return one JSON object of the form {\"results\": [ ... ]} with one result object per item, in order, each carrying the item number as \"item\" followed by the fields the system prompt defines.\n\n" + "\n\n".join(items))
write_call(f"P2-{nid}", "P2", user)
save(f"p1_{nid}.json", {"stats": stats, "per_passage": per_passage, "exact": exact, "todo": todo})
print(nid, stats, "| unique", len(uniq), "| exact match", len(exact), "| to P2", len(todo))
