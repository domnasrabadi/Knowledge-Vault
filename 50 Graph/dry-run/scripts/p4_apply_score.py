import sys, os, math, datetime, glob
sys.path.insert(0, os.path.dirname(__file__))
from common import *
C = load("claims.json"); byid = {c["id"]: c for c in C}; N = {n["id"]: n for n in load("notes.json")}
groups, rels, bad = [], [], 0
for f in sorted(glob.glob(os.path.join(ROOT, "out", "P4-*.json"))):
    k = os.path.basename(f)[3:-5]; o = read_out("P4-" + k)
    for g in o.get("groups", []): groups.append({"cluster": k, **g})
    for r in o.get("relations", []):
        if r["from"] in byid and r["to"] in byid: rels.append({"cluster": k, **r})
        else: bad += 1
seen = set(); uniq = []
for r in rels:
    key = (r["from"], r["to"], r["label"])
    if key not in seen: seen.add(key); uniq.append(r)
rels = uniq
TODAY = datetime.date(2026, 11, 16); HALF = {"durable": None, "evolving": 730, "ephemeral": 182}; Q = {"": 1.0, "1": 1.0, "2": 1.5, "3": 2.0}
def weight(c):
    n = N[c["note"]]; rt = c["referenced_time"]; start = (rt.get("start") if isinstance(rt, dict) else rt) or n["published"] or n["created"]
    parts = [int(x) for x in str(start).split("-")] + [1, 1]; d = datetime.date(parts[0], parts[1], parts[2])
    h = HALF[c["volatility"]]; decay = 1.0 if h is None else 0.5 ** (max(0, (TODAY - d).days) / h)
    return Q[n["quality"]] * decay, decay, ("published" if n["published"] else "created") if not rt else "stated"
sup = {c["id"]: {c["note"]: weight(c)[0]} for c in C}; opp = {c["id"]: {} for c in C}
for r in rels:
    a, b = byid[r["from"]], byid[r["to"]]
    if r["label"] == "refines": sup[b["id"]][a["note"]] = max(sup[b["id"]].get(a["note"], 0), 0.5 * weight(a)[0])   # QUALIFIED_SUPPORT at half weight
    if r["label"] == "contradicts":
        opp[b["id"]][a["note"]] = max(opp[b["id"]].get(a["note"], 0), weight(a)[0]); opp[a["id"]][b["note"]] = max(opp[a["id"]].get(b["note"], 0), weight(b)[0])
for c in C:
    w, decay, basis = weight(c)
    c.update(w=round(w, 3), decay=round(decay, 3), date_basis=basis, support=round(math.log(1 + sum(sup[c["id"]].values())), 3), support_groups=len(sup[c["id"]]), opposition=round(math.log(1 + sum(opp[c["id"]].values())), 3))
save("claims_scored.json", C); save("p4_relations.json", {"groups": groups, "relations": rels})
multi = [c for c in C if c["support_groups"] >= 2]
print(f"P4: {len(groups)} same-groups, {len(rels)} relations ({bad} with unknown ids)")
for r in rels: print("  ", r["cluster"], r["from"], r["label"], r["to"], r["confidence"], "| sup" if r.get("supersedes") else "|", (r.get("qualifier") or "")[:60], "||", r["reason"][:150])
print(f"claims {len(C)} | supported by >=2 groups: {len(multi)} ({len(multi)/len(C):.1%}) | contested: {sum(c['opposition']>0 for c in C)}")
for c in sorted(C, key=lambda c: -c["support"])[:8]: print("  ", c["id"], c["note"], c["volatility"], "w", c["w"], "support", c["support"], "groups", c["support_groups"], "|", c["text"][:90])
import collections
print("date basis", collections.Counter(c["date_basis"] for c in C), "| support range", min(c["support"] for c in C), max(c["support"] for c in C))
