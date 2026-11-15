# Dry-run stand-in for "embed and cluster claims": TF-IDF cosine on words plus shared ABOUT targets (no embedding model installed).
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from collections import Counter
T = float(sys.argv[1]) if len(sys.argv) > 1 else 0.30; MAXSZ = 12
C = load("claims.json"); N = {n["id"]: n for n in load("notes.json")}
STOP = set("a an the of to in on for and or is are be as by with that this it its from at than can not but when which into their they them was were has have had do does more most less such also only should may might must will would could if then so between about each any other own one two".split())
def stem(w):
    for s in ("ations","ation","ings","ing","ies","ed","es","s"):
        if w.endswith(s) and len(w) - len(s) >= 4: return w[:-len(s)]
    return w
toks = [Counter(stem(w) for w in re.findall(r"[a-z0-9]+", c["text"].lower()) if w not in STOP) for c in C]
df = Counter(w for t in toks for w in t)
vec = [{w: (1 + math.log(f)) * math.log(len(C) / df[w]) for w, f in t.items()} for t in toks]
nrm = [math.sqrt(sum(v * v for v in x.values())) or 1 for x in vec]
def sim(i, j):
    cos = sum(v * vec[j].get(w, 0) for w, v in vec[i].items()) / (nrm[i] * nrm[j])
    a, b = set(x for x in C[i]["about"] if x), set(x for x in C[j]["about"] if x)
    return 0.8 * cos + 0.2 * (len(a & b) / max(1, len(a | b)))
pairs = sorted(((sim(i, j), i, j) for i in range(len(C)) for j in range(i + 1, len(C))), reverse=True)
par = list(range(len(C))); size = [1] * len(C)
def find(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for s, i, j in pairs:
    if s < T: break
    a, b = find(i), find(j)
    if C[i]['note'] == C[j]['note']: continue   # dry run: only cross-note similarity seeds a cluster
    if a != b and size[a] + size[b] <= MAXSZ: par[b] = a; size[a] += size[b]
cl = {}
for i in range(len(C)): cl.setdefault(find(i), []).append(i)
clusters = [v for v in cl.values() if len(v) >= 2]
multi = [v for v in clusters if len({C[i]["note"] for i in v}) >= 2]
print(f"T={T} clusters>=2: {len(clusters)} | spanning >=2 notes: {len(multi)} | claims in them: {sum(map(len, clusters))} / {sum(map(len, multi))} | max size {max(map(len, clusters))}")
if "--write" in sys.argv:
    out = []
    for k, v in enumerate(multi, 1):
        lines = []
        for i in v:
            c = C[i]; n = N[c["note"]]
            rt = c["referenced_time"]; t = (rt.get("start") if isinstance(rt, dict) else rt) or n["published"] or n["created"]
            lines.append(f'{c["id"]} | {c["text"]} | time: {t} | source: {n["title"]}')
        write_call(f"P4-k{k:02d}", "P4", "task: cluster\n\n" + "\n".join(lines) + "\n\nGroup the claims that are the same, and list the relations between the rest.")
        out.append({"cluster": f"k{k:02d}", "claims": [C[i]["id"] for i in v]})
    save("clusters.json", out)
    for o in out[:4]:
        print(o["cluster"]); [print("  ", c["id"], c["note"], c["text"][:110]) for c in C if c["id"] in o["claims"]]
