import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *
P = {p["id"]: p for p in load("passages.json")}
reg = load("registry.json"); byid = {e["id"]: e for e in reg}
index = {}
for e in reg:
    for nm in [e["canonical_name"]] + e["aliases"]: index.setdefault(norm(nm), e["id"])
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
claims = []
for n in load("notes.json"):
    nid = n["id"]; res = load(f"resolved_{nid}.json"); out = read_out(f"P3-{nid}")["claims"]
    st = dict(returned=len(out), kept=0, bad_passage=0, over_40_words=0, pronoun_start=0, about_unknown_id=0, about_not_in_passage_mentions=0, new_targets=0, new_targets_created=0, with_time=0, multi_passage=0)
    for c in out:
        pids = [p for p in c["passage_ids"] if p in P and P[p]["note"] == nid]
        if len(pids) != len(c["passage_ids"]): st["bad_passage"] += 1
        if not pids: continue
        if len(c["text"].split()) > 40: st["over_40_words"] += 1
        if re.match(r"^(It|They|This|These|Those|He|She|We)\b", c["text"]): st["pronoun_start"] += 1
        allowed = {m["id"] for p in pids for m in res.get(p, [])}
        about = []
        for a in c["about"]:
            if a.get("id"):
                if a["id"] not in byid: st["about_unknown_id"] += 1; continue
                if a["id"] not in allowed: st["about_not_in_passage_mentions"] += 1
                about.append(a["id"])
            elif a.get("new_name"):
                st["new_targets"] += 1; k = norm(a["new_name"])
                if k not in index:
                    kind = a.get("new_kind") or "concept"; i = f"reg:{kind}:{slug(a['new_name'])}"
                    e = {"id": i, "kind": kind, "entity_type": None, "canonical_name": a["new_name"], "aliases": [], "definition": "", "instance_of": None, "status": "approved", "review_state": "auto", "first_note": nid, "from": "P3 new target (not sent to P2 in the dry run)"}
                    reg.append(e); byid[i] = e; index[k] = i; st["new_targets_created"] += 1
                about.append(index[k])
            else: about.append(None)
        if c.get("referenced_time"): st["with_time"] += 1
        if len(pids) > 1: st["multi_passage"] += 1
        claims.append({"id": f"c{len(claims)+1:03d}", "note": nid, "text": c["text"], "qualifiers": c["qualifiers"], "passage_ids": pids, "about": about, "about_raw": c["about"], "relation_phrases": c["relation_phrases"], "referenced_time": c.get("referenced_time"), "volatility": c["volatility"], "confidence": c["confidence"]})
        st["kept"] += 1
    npass = sum(1 for p in P.values() if p["note"] == nid); cited = {p for c in claims if c["note"] == nid for p in c["passage_ids"]}
    print(nid, st, "| passages with a claim", len(cited), "of", npass)
save("claims.json", claims); save("registry.json", reg)
from collections import Counter
print("volatility", Counter(c["volatility"] for c in claims), "| registry", len(reg))
