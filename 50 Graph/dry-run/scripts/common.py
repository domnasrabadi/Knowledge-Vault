import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT = os.path.dirname(os.path.dirname(ROOT))
PROMPTS = os.path.join(os.path.dirname(ROOT), "prompts")
NOTES = [
 ("n1", "10 Sources/Articles/⭐️ LLM-as-Judge Architectures (inc. runtime judges).md"),
 ("n2", "10 Sources/Articles/⭐️ How to Use LLM-Judges Properly.md"),
 ("n3", "10 Sources/Articles/⭐️⭐️ Evals for AI Agents (Anthropic).md"),
]
PFILE = {"P1":"P1 - Mention Extraction.md","P2":"P2 - Mention Adjudication.md","P3":"P3 - Claim Extraction.md",
         "P4":"P4 - Claim Matching.md","P11":"P11 - Citation Support Judge.md","P14":"P14 - Exhaustiveness Check.md"}
def system_prompt(pid):
    t = open(os.path.join(PROMPTS, PFILE[pid])).read()
    a = t.index("## System prompt"); a = t.index("````text\n", a) + 9
    return t[a:t.index("\n````", a)]
def load(name): return json.load(open(os.path.join(ROOT, "data", name)))
def save(name, obj): json.dump(obj, open(os.path.join(ROOT, "data", name), "w"), ensure_ascii=False, indent=1)
def write_call(name, pid, user):
    p = os.path.join(ROOT, "calls", name + ".txt")
    open(p, "w").write("=== SYSTEM PROMPT ===\n" + system_prompt(pid) + "\n\n=== USER MESSAGE ===\n" + user + "\n")
    return p
def read_out(name):
    t = open(os.path.join(ROOT, "out", name + ".json")).read().strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    return json.loads(t)
def norm(s): return re.sub(r"[^\w+#]+", " ", s.lower()).strip()
