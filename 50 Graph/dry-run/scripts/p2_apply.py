# usage: p2_apply.py n1  -> applies P2 results to the Registry using the spec's thresholds
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *
nid = sys.argv[1]
d = load(f"p1_{nid}.json")
reg = load("registry.json") if os.path.exists(os.path.join(ROOT, "data", "registry.json")) else []
byid = {e["id"]: e for e in reg}
review = load("review.json") if os.path.exists(os.path.join(ROOT, "data", "review.json")) else []
res = {r["item"]: r for r in read_out(f"P2-{nid}")["results"]}
link = dict(d["exact"]); log = []; c = dict(auto_link=0, provisional=0, new=0, missing=0, bad_target=0)
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def create(name, kind, etype, definition, inst, src):
    i = f"reg:{kind}:{slug(name)}"
    if i in byid: return i
    e = {"id": i, "kind": kind, "entity_type": etype, "canonical_name": name, "aliases": [], "definition": definition or "", "instance_of": inst, "status": "approved", "review_state": "auto", "first_note": nid}
    reg.append(e); byid[i] = e; return i
for t in d["todo"]:
    r = res.get(t["item"])
    if not r: c["missing"] += 1; continue
    dec, conf, tgt = r["decision"], r["confidence"], r.get("target_id")
    if dec == "match" and tgt not in t["candidates"]: c["bad_target"] += 1; dec = "new"
    if dec == "match" and conf >= 0.85:
        link[t["key"]] = tgt; c["auto_link"] += 1
        if norm(t["text"]) not in [norm(x) for x in [byid[tgt]["canonical_name"]] + byid[tgt]["aliases"]]: byid[tgt]["aliases"].append(t["text"])
    elif (dec == "match" and conf >= 0.60) or (dec == "unsure" and tgt in t["candidates"]):
        link[t["key"]] = tgt; c["provisional"] += 1
        review.append({"type": "mention-link", "note": nid, "mention": t["text"], "target": tgt, "decision": dec, "confidence": conf, "reason": r["reason"]})
    else:
        name = r.get("new_name") or t["text"]
        i = create(name, r["kind"], r.get("entity_type"), r.get("new_definition"), r.get("instance_of"), nid)
        if norm(t["text"]) != norm(byid[i]["canonical_name"]) and t["text"] not in byid[i]["aliases"]: byid[i]["aliases"].append(t["text"])
        link[t["key"]] = i; c["new"] += 1
        if dec == "unsure": review.append({"type": "mention-unsure", "note": nid, "mention": t["text"], "target": i, "decision": dec, "confidence": conf, "reason": r["reason"]})
    log.append({"mention": t["text"], "decision": r["decision"], "confidence": conf, "target": link[t["key"]], "reason": r["reason"]})
resolved = {}
for m in d["per_passage"]:
    if m["key"] in link:
        resolved.setdefault(m["passage_id"], [])
        if link[m["key"]] not in [x["id"] for x in resolved[m["passage_id"]]]:
            resolved[m["passage_id"]].append({"id": link[m["key"]], "name": byid[link[m["key"]]]["canonical_name"]})
save("registry.json", reg); save("review.json", review); save(f"resolved_{nid}.json", resolved); save(f"p2_log_{nid}.json", log)
print(nid, c, "| exact", len(d["exact"]), "| registry size", len(reg), "| review items", len(review))
