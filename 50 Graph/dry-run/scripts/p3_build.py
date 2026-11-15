import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *
PS = load("passages.json")
for n in load("notes.json"):
    nid = n["id"]; ps = [p for p in PS if p["note"] == nid]; res = load(f"resolved_{nid}.json")
    meta = f'title: {n["title"]} | author: {n["author"] or "unknown"} | type: {n["type"]} | status: {n["status"]} | published: {n["published"] or "unknown"}'
    ml = "\n".join(f'{p["id"]}: ' + ("; ".join(f'{m["id"]} "{m["name"]}"' for m in res.get(p["id"], [])) or "none") for p in ps)
    body = "\n".join(f'<passage id="{p["id"]}" breadcrumb="{p["breadcrumb"]}">{p["text"]}</passage>' for p in ps)
    write_call(f"P3-{nid}", "P3", f"<note_metadata>\n{meta}\n</note_metadata>\n\n<mentions>\n{ml}\n</mentions>\n\n<note>\n{body}\n</note>\n\nExtract the claims this note asserts.")
    print("built P3", nid)
