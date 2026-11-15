import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
from common import *
random.seed(11)
PS = load("passages.json"); P = {p["id"]: p for p in PS}; C = load("claims.json"); N = {n["id"]: n for n in load("notes.json")}
# P11: 15 claim-passage edges per note
sample11 = []
for nid in N:
    edges = [(c["id"], p) for c in C if c["note"] == nid for p in c["passage_ids"]]
    pick = random.sample(edges, 15); items = []
    for k, (cid, pid) in enumerate(pick, 1):
        c = [x for x in C if x["id"] == cid][0]; p = P[pid]
        items.append(f'<item n="{k}">\n<source>{N[nid]["title"]}</source>\n<breadcrumb>{p["breadcrumb"]}</breadcrumb>\n<passage>\n{p["text"]}\n</passage>\n<claim>{c["text"]}</claim>\n</item>')
        sample11.append({"note": nid, "item": k, "claim": cid, "passage": pid})
    user = ("This message contains 15 separate items. Treat each item as its own independent request: for each, decide whether the passage asserts the claim, exactly as the system prompt describes, without letting one item influence another. Return one JSON object of the form {\"results\": [ ... ]} with one result per item, in order, each carrying the item number as \"item\" followed by the fields the system prompt defines (quote, reason, verdict).\n\n" + "\n\n".join(items))
    write_call(f"P11-{nid}", "P11", user)
save("p11_sample.json", sample11)
# P14: 3 prose passages per note
sample14 = []
for nid in N:
    cand = [p for p in PS if p["note"] == nid and p["tokens_est"] >= 120 and not p["text"].lstrip().startswith("```") and not p["text"].lstrip().startswith("|")]
    for k, p in enumerate(random.sample(cand, 3), 1):
        sect = "\n\n".join(x["text"] for x in PS if x["section"] == p["section"])
        cl = "\n".join(("[cites this passage] " if p["id"] in c["passage_ids"] else "[cites another passage] ") + c["text"] for c in C if c["note"] == nid)
        user = f'<section breadcrumb="{p["breadcrumb"]}">\n{sect}\n</section>\n<passage id="{p["id"]}">\n{p["text"]}\n</passage>\n<extracted_claims>\n{cl}\n</extracted_claims>\n\nWhich claims asserted by the passage are not covered by any extracted claim?'
        write_call(f"P14-{nid}-{k}", "P14", user)
        sample14.append({"note": nid, "k": k, "passage": p["id"], "claims_citing": sum(p["id"] in c["passage_ids"] for c in C)})
save("p14_sample.json", sample14)
print(sample14); os.system(f'wc -c "{ROOT}"/calls/P11-* "{ROOT}"/calls/P14-*')
