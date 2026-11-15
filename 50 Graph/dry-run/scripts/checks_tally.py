import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from collections import Counter
P = {p["id"]: p for p in load("passages.json")}; C = {c["id"]: c for c in load("claims.json")}
ws = lambda s: re.sub(r"\s+", " ", s).strip()
rows = []; S = load("p11_sample.json")
for nid in ["n1", "n2", "n3"]:
    res = {r["item"]: r for r in read_out(f"P11-{nid}")["results"]}
    for s in [x for x in S if x["note"] == nid]:
        r = res[s["item"]]; q = r["quote"]
        found = all(ws(part) in ws(P[s["passage"]]["text"]) for part in q.split(" ... ")) if q else None
        rows.append({**s, "verdict": r["verdict"], "quote_found": found, "multi_passage": len(C[s["claim"]]["passage_ids"]) > 1, "reason": r["reason"], "claim_text": C[s["claim"]]["text"]})
save("p11_results.json", rows)
print("P11 verdicts", Counter(r["verdict"] for r in rows), "| quote not found", sum(r["quote_found"] is False for r in rows))
print("  single-passage claims", Counter(r["verdict"] for r in rows if not r["multi_passage"]), "| multi-passage", Counter(r["verdict"] for r in rows if r["multi_passage"]))
for r in rows:
    if r["verdict"] != "supports": print("  ", r["claim"], r["passage"], "multi" if r["multi_passage"] else "single", "|", r["reason"][:230])
m = []; tot = 0
for s in load("p14_sample.json"):
    out = read_out(f"P14-{s['note']}-{s['k']}")["missed"]; tot += s["claims_citing"]
    for x in out: m.append({**s, **x, "quote_found": ws(x["quote"]) in ws(P[s["passage"]]["text"])})
save("p14_results.json", m)
core = sum(x["importance"] == "core" for x in m)
print(f"P14: 9 passages, {tot} claims cite them, {len(m)} missed ({core} core) -> recall {tot/(tot+len(m)):.2f} all, {tot/(tot+core):.2f} core only")
for x in m: print("  ", x["passage"], x["importance"], x["quote_found"], "|", x["text"][:200])
