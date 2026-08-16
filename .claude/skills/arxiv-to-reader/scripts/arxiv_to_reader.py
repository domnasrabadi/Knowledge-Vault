#!/usr/bin/env python3
"""Fetch an arXiv paper's LaTeX source, render it to Reader-optimised HTML, and save it to Readwise Reader.

Pipeline:  arXiv ID -> arxiv-skill fetch (LaTeX e-print) -> pandoc HTML
           -> post-process (headings, math, citations, figures, references)
           -> POST https://readwise.io/api/v3/save/

Stdlib only. Requires: python3, pandoc, and the arxiv-skill checkout.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

def _resolve_arxiv_skill_dir() -> Path:
    """Prefer the copy vendored beside this skill; fall back to the old checkout."""
    env = os.environ.get("ARXIV_SKILL_DIR")
    if env:
        return Path(os.path.expanduser(env))
    sibling = Path(__file__).resolve().parent.parent.parent / "arxiv"
    if (sibling / "scripts" / "fetch.py").exists():
        return sibling
    return Path(os.path.expanduser("~/Downloads/arxiv-skill"))


ARXIV_SKILL_DIR = _resolve_arxiv_skill_dir()
TOKEN_ENV_FILES = [
    Path(os.path.expanduser("~/Downloads/reader4/.env")),
    Path(os.path.expanduser("~/.config/readwise/.env")),
    Path(os.path.expanduser(
        "~/Downloads/reader4/99_archive/readwise_highlights_to_notes/.env")),
]
SAVE_URL = "https://readwise.io/api/v3/save/"
LIST_URL = "https://readwise.io/api/v3/list/"
DELETE_URL = "https://readwise.io/api/v3/delete/{}/"

# Readwise Reader's HTML cleaner strips <h1> from the body (it owns the title),
# so sections must arrive as <h2>+. This is why we shift heading levels.
MAX_IMAGE_BYTES = 900_000       # per embedded figure, after downscaling
MAX_IMAGE_WIDTH = 1200          # px; wider rasters get downscaled via sips
MAX_HTML_BYTES = 8_000_000      # total payload guard (base64 inflates ~33%)
TABLE_DPI = 200                 # render resolution for table images
TABLE_MIN_COLS = 8              # at/above this column count a table becomes an image


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def die(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def find_token() -> str:
    token = os.environ.get("READWISE_TOKEN")
    if token:
        return token.strip()
    for path in TOKEN_ENV_FILES:
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if line.startswith("READWISE_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    die(
        "no Readwise token. Set READWISE_TOKEN, or add it to "
        f"{TOKEN_ENV_FILES[0]}. Get one at https://readwise.io/access_token"
    )


def api(method: str, url: str, token: str, payload: dict | None = None) -> tuple[int, dict]:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Authorization": f"Token {token}"}
    if data:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode() or "{}"
            return resp.status, json.loads(body) if body.strip() else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except json.JSONDecodeError:
            return e.code, {"detail": body[:500]}


# --------------------------------------------------------------------------
# step 1: fetch LaTeX source via arxiv-skill
# --------------------------------------------------------------------------

def normalize_paper_id(raw: str) -> str:
    """Reduce any input form to a bare arXiv ID.

    fetch.py handles URLs, but when given one it caches under an unversioned
    directory and skips writing meta.json; passing a bare ID makes it pin the
    version and emit full metadata. So normalise here first.
    """
    scripts = ARXIV_SKILL_DIR / "scripts"
    sys.path.insert(0, str(scripts))
    try:
        from common import normalize_arxiv_id  # type: ignore
    except ImportError:
        return raw
    finally:
        sys.path.pop(0)
    try:
        base, version = normalize_arxiv_id(raw)
    except Exception:
        return raw
    return f"{base}{version}" if version else base


def fetch_paper(paper: str, force: bool) -> dict:
    script = ARXIV_SKILL_DIR / "scripts" / "fetch.py"
    if not script.exists():
        die(
            f"arxiv-skill not found at {ARXIV_SKILL_DIR}. "
            "Set ARXIV_SKILL_DIR to its location."
        )
    cmd = [sys.executable, "fetch.py", normalize_paper_id(paper), "--json"]
    if force:
        cmd.append("--force")
    proc = run(cmd, cwd=str(script.parent))
    if proc.returncode != 0:
        die(f"fetch.py failed:\n{proc.stderr.strip()}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        die(f"fetch.py returned non-JSON:\n{proc.stdout[:500]}")


# --------------------------------------------------------------------------
# step 2: LaTeX -> HTML via pandoc
# --------------------------------------------------------------------------

# Preamble constructs pandoc's LaTeX reader cannot digest. Papers that style
# themselves with tikz/soul/pgf define @-internal macros that abort the parse
# ("unexpected end of input") even though the document body is perfectly fine.
RISKY_PREAMBLE = re.compile(
    r"@"                       # any @-internal macro is TeX plumbing, never content
    r"|tikz|pgf|soul|coordinate|\\makeatletter|\\DeclareRobustCommand"
    r"|tcolorbox|\\newenvironment|\\if[a-z]*\b|\\csname",
    re.I,
)
SAFE_DEF = re.compile(
    r"^\s*\\(newcommand|renewcommand|providecommand|DeclareMathOperator|"
    r"newtheorem|def)\b"
)


def repair_body(body: str) -> str:
    """Fix body-level LaTeX that pandoc rejects but real LaTeX tolerates.

    Two cases seen in the wild:
      * \\newcolumntype defined *after* \\begin{document} — legal, but pandoc
        chokes on the #1 parameter. It is pure table-layout, meaningless in HTML.
      * an unclosed group ("{\\small" before a bibliography, never closed).
        TeX closes it implicitly at \\end{document}; pandoc reports
        "unexpected \\end" instead.
    """
    lines = body.split("\n")
    lines = [l for l in lines if not l.lstrip().startswith("\\newcolumntype")]

    depth, verbatim = 0, False
    for line in lines:
        code = []
        for i, ch in enumerate(line):
            if ch == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            code.append(ch)
        text = "".join(code)
        if re.search(r"\\begin\{(verbatim|lstlisting|minted)\}", text):
            verbatim = True
        if re.search(r"\\end\{(verbatim|lstlisting|minted)\}", text):
            verbatim = False
            continue
        if verbatim:
            continue
        text = re.sub(r"\\[{}]", "", text)      # escaped braces are literals
        depth += text.count("{") - text.count("}")

    out = "\n".join(lines)
    if depth > 0:
        out = out.replace("\\end{document}", "}" * depth + "\n\\end{document}", 1)
    return out


def sanitize_preamble(tex: str) -> str | None:
    """Rebuild the document with a minimal preamble, keeping only simple macros.

    Authors' shorthand macros (\\MET, \\argmax) are used in the body and must
    survive; the decoration machinery that breaks pandoc is dropped.
    """
    marker = r"\begin{document}"
    idx = tex.find(marker)
    if idx == -1:
        return None
    preamble, body = tex[:idx], tex[idx:]
    kept: list[str] = []
    for line in preamble.split("\n"):
        stripped = line.split("%")[0].strip()
        if not stripped or not SAFE_DEF.match(stripped):
            continue
        # Only consider self-contained one-liners — a macro whose body spans
        # lines would be truncated here and break the parse we are fixing.
        if stripped.count("{") != stripped.count("}"):
            continue
        if not RISKY_PREAMBLE.search(stripped):
            kept.append(stripped)
            continue
        # Risky body, but the macro may still be *called* from the document
        # (\MET -> \verdicttoken{MET}). Dropping it outright leaves a dangling
        # command that MathJax renders as an error, so emit a stub that just
        # passes its first argument through.
        m = re.match(
            r"\\(?:new|renew|provide)command\*?\s*\{?\\([a-zA-Z]+)\}?\s*\[(\d+)\]",
            stripped,
        )
        if m and int(m.group(2)) >= 1:
            kept.append(f"\\newcommand{{\\{m.group(1)}}}[{m.group(2)}]{{#1}}")
    header = "\\documentclass{article}\n\\usepackage{amsmath}\n\\usepackage{amssymb}\n"
    return header + "\n".join(kept) + "\n" + repair_body(body)


# --------------------------------------------------------------------------
# dense tables -> images
# --------------------------------------------------------------------------

def _brace_span(text: str, start: int) -> int:
    """Index just past the {...} group beginning at `start` (which is the '{')."""
    depth, i = 0, start
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def extract_cmd(body: str, cmd: str) -> tuple[str | None, str]:
    """Pull the first complete \\cmd{...} out of body. Returns (command, rest)."""
    needle = "\\" + cmd
    j = body.find(needle)
    if j == -1:
        return None, body
    k = body.find("{", j)
    if k == -1:
        return None, body
    end = _brace_span(body, k)
    return body[j:end], body[:j] + body[end:]


def unwrap_scale_boxes(tex: str) -> tuple[str, int]:
    """Strip \\scalebox/\\resizebox/\\adjustbox wrappers, keeping their content.

    Authors routinely shrink wide tables with \\scalebox{0.75}{\\begin{tabular}…}.
    Pandoc does not understand these commands and silently discards the whole
    group — so every table inside one vanishes from the output. Unwrapping them
    costs only the scale factor (meaningless in HTML) and saves the table.
    """
    specs = {"scalebox": 1, "resizebox": 2, "adjustbox": 1, "makebox": 1}
    count = 0
    for name, nargs in specs.items():
        pattern = re.compile(r"\\" + name + r"\s*(?=[{\[])")
        while True:
            m = pattern.search(tex)
            if not m:
                break
            i = m.end()
            ok = True
            for _ in range(nargs):           # consume the sizing arguments
                while i < len(tex) and tex[i] in " \t\n":
                    i += 1
                if i < len(tex) and tex[i] == "[":      # optional [..] arg
                    close = tex.find("]", i)
                    if close == -1:
                        ok = False
                        break
                    i = close + 1
                    while i < len(tex) and tex[i] in " \t\n":
                        i += 1
                if i >= len(tex) or tex[i] != "{":
                    ok = False
                    break
                i = _brace_span(tex, i)
            while ok and i < len(tex) and tex[i] in " \t\n":
                i += 1
            if not ok or i >= len(tex) or tex[i] != "{":
                # Can't parse this one; neutralise the command name so the
                # loop terminates, leaving the surrounding text untouched.
                tex = tex[:m.start()] + "\\relax" + tex[m.end():]
                continue
            end = _brace_span(tex, i)
            tex = tex[:m.start()] + tex[i + 1:end - 1] + tex[end:]
            count += 1
    return tex.replace("\\relax", ""), count


def table_column_count(block: str) -> int:
    """Count columns in a tabular preamble.

    The spec must be brace-matched, not read with [^}]*: the booktabs idiom
    `{@{}cccc@{}}` ends the naive match inside `@{}` and reports zero columns,
    which silently excluded most real tables from dense-table handling.
    """
    m = re.search(
        r"\\begin\{(tabular[x*]?|longtable)\}(?:\[[^\]]*\])?\s*", block)
    if not m:
        return 0
    i = m.end()
    # tabular* and tabularx take a width argument before the column spec.
    for _ in range(2 if m.group(1) in ("tabular*", "tabularx") else 1):
        while i < len(block) and block[i] in " \t\n":
            i += 1
        if i >= len(block) or block[i] != "{":
            return 0
        start, i = i, _brace_span(block, i)
    spec = block[start + 1:i - 1]
    # Drop inter-column material, which declares no column of its own.
    spec = re.sub(r"[@>!<]\s*\{(?:[^{}]|\{[^{}]*\})*\}", "", spec)
    count, j = 0, 0
    while j < len(spec):
        ch = spec[j]
        if ch in "pmbw" and j + 1 < len(spec) and spec[j + 1] == "{":
            count += 1
            j = _brace_span(spec, j + 1)
            continue
        if ch in "lcrXY":
            count += 1
        j += 1
    return count


def build_table_preamble(tex: str, src_dir: Path, texbin: str) -> str:
    """Preamble for standalone table compiles.

    Venue style files (iclr2025_conference.sty etc.) are dropped: they pull in
    fonts a minimal TeX install lacks, and contribute nothing to a table. Any
    \\usepackage naming a package that isn't installed is dropped too, since a
    missing .sty is fatal to LaTeX even in nonstopmode. Everything else is kept
    verbatim so the authors' own macros (\\mycolorbox, \\best, …) still resolve.
    """
    local_sty = {p.stem for p in src_dir.rglob("*.sty")}
    local_sty |= {p.stem for p in src_dir.rglob("*.cls")}
    pre = tex[:tex.find(r"\begin{document}")]
    env = {"PATH": f"{texbin}:/usr/bin:/bin"}
    out: list[str] = []
    for line in pre.split("\n"):
        s = line.split("%")[0].strip()
        if s.startswith("\\documentclass"):
            continue
        if s.startswith(("\\bibliography", "\\input", "\\include")):
            continue
        m = re.match(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", s)
        if m:
            names = [p.strip() for p in m.group(1).split(",") if p.strip()]
            if any(p in local_sty for p in names):
                continue
            avail = [p for p in names if subprocess.run(
                ["kpsewhich", f"{p}.sty"], capture_output=True, env=env).stdout.strip()]
            if not avail:
                continue
            if len(avail) != len(names):
                out.append("\\usepackage{" + ",".join(avail) + "}")
                continue
        out.append(line)
    return (
        "\\documentclass[preview,border=6pt,varwidth=20cm]{standalone}\n"
        "\\usepackage{booktabs,multirow,array,graphicx,xcolor,colortbl,"
        "amsmath,amssymb,adjustbox}\n"
        + "\n".join(out) + "\n"
        # Tables routinely wrap themselves in \resizebox{\columnwidth}{!}{...};
        # standalone has no page, so these lengths need real values or LaTeX
        # aborts with "Dimension too large".
        "\\setlength{\\textwidth}{20cm}\n"
        "\\setlength{\\columnwidth}{20cm}\n"
        "\\setlength{\\linewidth}{20cm}\n"
    )


def render_tables_as_images(
    tex: str, src_dir: Path, cache_dir: Path, min_cols: int, force_all: bool
) -> tuple[str, int, int]:
    """Replace dense table floats with a rendered PNG, keeping their captions.

    Dense numeric grids are unreadable and unhighlightable in Reader's column
    layout. Rendering them through real LaTeX keeps full fidelity (rules,
    colour, multirow, math) at the cost of losing selectable text — which for
    these tables was never usable anyway. Captions stay as HTML text.
    """
    texbin = str(Path(shutil.which("pdflatex")).parent)
    preamble = build_table_preamble(tex, src_dir, texbin)
    outdir = cache_dir / "tables"
    outdir.mkdir(parents=True, exist_ok=True)

    blocks = list(re.finditer(r"\\begin\{table\*?\}.*?\\end\{table\*?\}", tex, re.S))
    rendered = failed = 0
    replacements: list[tuple[int, int, str]] = []

    for n, m in enumerate(blocks, 1):
        block = m.group(0)
        cols = table_column_count(block)
        if not force_all and cols < min_cols:
            continue

        body = re.sub(r"\\begin\{table\*?\}(\[[^\]]*\])?", "", block)
        body = re.sub(r"\\end\{table\*?\}", "", body)
        caption, body = extract_cmd(body, "caption")
        label, body = extract_cmd(body, "label")
        body = body.replace("\\centering", "").strip()
        if not body:
            continue

        png = outdir / f"table{n}.png"
        if not png.exists():
            work = Path(tempfile.mkdtemp(prefix=f"tbl{n}_"))
            (work / "t.tex").write_text(
                preamble + "\\begin{document}\n" + body + "\n\\end{document}\n"
            )
            # No -halt-on-error: leftover calls to the dropped venue style
            # (\iclrfinalcopy and friends) are undefined but harmless, and
            # LaTeX still typesets the table after reporting them.
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "t.tex"],
                cwd=work, capture_output=True, text=True,
                env={"PATH": f"{texbin}:/usr/bin:/bin", "TEXINPUTS": f".:{src_dir}:"},
            )
            pdf = work / "t.pdf"
            made = False
            if pdf.exists():
                conv = subprocess.run(
                    ["pdftocairo", "-png", "-r", str(TABLE_DPI), "-singlefile",
                     str(pdf), str(work / "t")],
                    capture_output=True,
                )
                if conv.returncode == 0 and (work / "t.png").exists():
                    shutil.copy(work / "t.png", png)
                    made = True
            shutil.rmtree(work, ignore_errors=True)
            if not made:
                failed += 1
                continue

        rendered += 1
        # A figure float, not a table float: pandoc attaches \caption inside a
        # table environment to the tabular it builds, and with the tabular now
        # replaced by an image there is nothing to attach to, so the caption is
        # silently dropped. In a figure float it becomes a <figcaption>.
        parts = ["\\begin{figure}", "\\centering",
                 f"\\includegraphics[width=\\textwidth]{{{png}}}"]
        if caption:
            parts.append(caption)
        if label:
            parts.append(label)
        parts.append("\\end{figure}")
        replacements.append((m.start(), m.end(), "\n".join(parts)))

    for start, end, repl in reversed(replacements):
        tex = tex[:start] + repl + tex[end:]
    return tex, rendered, failed


def _run_pandoc(tex_path: Path, resource_dir: Path) -> tuple[str, str, int]:
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        out = Path(tmp.name)
    cmd = [
        "pandoc", "-f", "latex", "-t", "html",
        "--mathjax",                    # emits \( \) delimiters; converted below
        "--wrap=none",
        "--shift-heading-level-by=1",   # sections become <h2> so Reader keeps them
        f"--resource-path={resource_dir}",
        str(tex_path), "-o", str(out),
    ]
    proc = run(cmd)
    html = out.read_text() if out.exists() else ""
    out.unlink(missing_ok=True)
    return html, proc.stderr, proc.returncode


def latex_to_html(tex_path: Path, resource_dir: Path) -> str:
    if not shutil.which("pandoc"):
        die("pandoc not installed. `brew install pandoc`")

    html, stderr, rc = _run_pandoc(tex_path, resource_dir)

    if len(html.strip()) < 500:
        # Retry with a sanitised preamble before giving up.
        sanitized = sanitize_preamble(tex_path.read_text(errors="replace"))
        if sanitized:
            print("  pandoc choked on the preamble — retrying with it stripped …")
            tmp_tex = Path(tempfile.mkdtemp(prefix="arxiv_tex_")) / "sanitized.tex"
            tmp_tex.write_text(sanitized)
            html2, stderr2, rc2 = _run_pandoc(tmp_tex, resource_dir)
            shutil.rmtree(tmp_tex.parent, ignore_errors=True)
            if len(html2.strip()) >= 500:
                html, stderr, rc = html2, stderr2, rc2
            else:
                stderr = stderr2 or stderr

    if len(html.strip()) < 500:
        die(
            "pandoc could not convert this paper's LaTeX:\n"
            f"{stderr.strip()[:800]}\n"
            f"Fallback: read arXiv's own HTML at https://arxiv.org/html/ instead."
        )
    if stderr.strip():
        print(f"  pandoc warnings: {len(stderr.strip().splitlines())} line(s)")
    return html


# --------------------------------------------------------------------------
# step 3: post-processing
# --------------------------------------------------------------------------

def fix_headings(html: str) -> str:
    """Safety net: demote any surviving <h1> to <h2> (Reader deletes h1 in body)."""
    html = re.sub(r"<h1(\s[^>]*)?>", lambda m: f"<h2{m.group(1) or ''}>", html)
    return html.replace("</h1>", "</h2>")


def fix_math(html: str) -> str:
    """pandoc --mathjax emits \\( \\) and \\[ \\]; Reader's renderer wants $ and $$."""
    html = html.replace(r"\(", "$").replace(r"\)", "$")
    html = html.replace(r"\[", "$$").replace(r"\]", "$$")
    return html


def latex_to_text(s: str) -> str:
    """Crudely de-TeX a bibliography fragment into readable text."""
    s = re.sub(r"\\href\s*\{([^}]*)\}\s*\{((?:[^{}]|\{[^}]*\})*)\}", r"\2 <\1>", s)
    s = re.sub(r"\\(emph|textit|textbf|texttt)\s*\{([^}]*)\}", r"\2", s)
    s = s.replace("\\newblock", " ").replace("~", " ")
    s = re.sub(r"\\natexlab\s*\{[^}]*\}", "", s)
    s = re.sub(r"\\['`\"^~=.]\s*\{?([A-Za-z])\}?", r"\1", s)  # accents
    s = re.sub(r"\\[a-zA-Z]+\s*", " ", s)                      # leftover commands
    s = s.replace("{", "").replace("}", "").replace("--", "–")
    return re.sub(r"\s+", " ", s).strip(" ,.")


def parse_bibliography(src_dir: Path) -> dict[str, dict]:
    """Parse .bbl \\bibitem entries into {key: {label, text}}.

    natbib style gives us `\\bibitem[{Author et al.(2025)...}]{key}` — the part
    before the parenthesis plus the year is exactly the inline citation label.
    """
    entries: dict[str, dict] = {}
    for bbl in src_dir.rglob("*.bbl"):
        text = bbl.read_text(errors="replace")
        chunks = re.split(r"\\bibitem", text)[1:]
        for chunk in chunks:
            m = re.match(r"\s*(?:\[(.*?)\])?\s*\{([^}]+)\}", chunk, re.S)
            if not m:
                continue
            raw_label, key = m.group(1), m.group(2).strip()
            body = chunk[m.end():]
            body = body.split("\\end{thebibliography}")[0]
            label = ""
            if raw_label:
                flat = re.sub(r"\s+", " ", raw_label).replace("~", " ")
                # "Author et al.(2025)Author, Other" -> "Author et al., 2025"
                lm = re.match(r"\{?(.*?)\((\d{4}[a-z]?)\)", flat)
                if lm:
                    label = f"{latex_to_text(lm.group(1))}, {lm.group(2)}"
                else:
                    label = latex_to_text(flat)
            if not label:
                ym = re.search(r"\b(19|20)\d{2}\b", body)
                label = f"{key}" if not ym else f"{key}, {ym.group(0)}"
            entries[key] = {"label": label, "text": latex_to_text(body)}
    if not entries:
        entries = parse_bibtex(src_dir)
    return entries


def _bib_surnames(author_field: str) -> list[str]:
    names = re.split(r"\s+and\s+", author_field.strip())
    out = []
    for n in names:
        n = latex_to_text(n).strip()
        if not n:
            continue
        out.append(n.split(",")[0].strip() if "," in n else n.split()[-1])
    return out


def parse_bibtex(src_dir: Path) -> dict[str, dict]:
    """Fallback for papers that ship .bib instead of a generated .bbl.

    Without this the prose loses every inline citation and the References
    section comes out empty, because pandoc cannot resolve \\cite on its own.
    """
    entries: dict[str, dict] = {}
    for bib in src_dir.rglob("*.bib"):
        text = bib.read_text(errors="replace")
        for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
            if m.group(1).lower() in ("comment", "preamble", "string"):
                continue
            key, start = m.group(2), m.end()
            depth, i = 1, m.start()
            i = text.find("{", m.start())
            depth, j = 1, i + 1
            while j < len(text) and depth:
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                j += 1
            body = text[start:j - 1]

            def field(name: str) -> str:
                fm = re.search(
                    rf"\b{name}\s*=\s*(\{{(?:[^{{}}]|\{{[^{{}}]*\}})*\}}|\"[^\"]*\"|[^,\s]+)",
                    body, re.I | re.S,
                )
                return re.sub(r"\s+", " ", fm.group(1).strip("{}\" ")).strip() if fm else ""

            authors = _bib_surnames(field("author"))
            year = field("year")[:4]
            if len(authors) == 1:
                who = authors[0]
            elif len(authors) == 2:
                who = f"{authors[0]} and {authors[1]}"
            elif authors:
                who = f"{authors[0]} et al"
            else:
                who = key
            label = f"{who}, {year}" if year else who
            venue = field("booktitle") or field("journal") or field("publisher")
            parts = [p for p in (", ".join(authors), year,
                                 latex_to_text(field("title")),
                                 latex_to_text(venue)) if p]
            entries[key] = {"label": label, "text": ". ".join(parts)}
    return entries


def restore_citations(html: str, bib: dict[str, dict]) -> tuple[str, int]:
    """pandoc can't resolve .bbl, leaving empty <span class="citation" data-cites="...">.

    Replace each with readable inline text so the prose isn't left with silent gaps.
    """
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        keys = m.group(1).split()
        labels = [bib[k]["label"] for k in keys if k in bib]
        if not labels:
            return ""
        count += 1
        return f' <span class="cite">({"; ".join(labels)})</span>'

    html = re.sub(
        r'<span class="citation" data-cites="([^"]*)"\s*>\s*</span>', repl, html
    )
    # Drop any citation spans we couldn't resolve rather than leaving empties.
    html = re.sub(r'\s*<span class="citation"[^>]*>\s*</span>', "", html)
    return html, count


def render_references(bib: dict[str, dict], used_keys: list[str]) -> str:
    if not bib:
        return ""
    keys = [k for k in used_keys if k in bib] or list(bib)
    seen, ordered = set(), []
    for k in keys:
        if k not in seen:
            seen.add(k)
            ordered.append(k)
    ordered.sort(key=lambda k: bib[k]["label"].lower())
    items = "\n".join(f"<li>{bib[k]['text']}</li>" for k in ordered if bib[k]["text"])
    if not items:
        return ""
    return f"\n<h2>References</h2>\n<ul>\n{items}\n</ul>\n"


def image_to_data_uri(path: Path, tmpdir: Path) -> str | None:
    """Return a data: URI for an image, converting/downscaling as needed."""
    suffix = path.suffix.lower()
    work = path
    if suffix in (".pdf", ".eps", ".ps"):
        if not shutil.which("pdftocairo"):
            return None
        out_base = tmpdir / (path.name.replace(".", "_") + "_conv")
        proc = run(["pdftocairo", "-png", "-r", "150", "-singlefile",
                    str(path), str(out_base)])
        # NB: not with_suffix() — figure names like "gpt-3.5-turbo.pdf" contain
        # dots, and with_suffix would strip from the first one and miss the file.
        work = Path(str(out_base) + ".png")
        if proc.returncode != 0 or not work.exists():
            return None
        suffix = ".png"
    if not work.exists():
        return None
    data = work.read_bytes()
    # Vector plots rasterise large. Step the width down (always from the
    # original, so quality doesn't compound) until it fits, rather than
    # dropping the figure outright.
    if len(data) > MAX_IMAGE_BYTES and shutil.which("sips"):
        for width in (MAX_IMAGE_WIDTH, 900, 700, 500):
            small = tmpdir / f"{work.stem}_{width}{suffix}"
            shutil.copy(work, small)
            run(["sips", "--resampleWidth", str(width), str(small)])
            if small.exists() and small.stat().st_size <= MAX_IMAGE_BYTES:
                data = small.read_bytes()
                break
    if len(data) > MAX_IMAGE_BYTES:
        return None
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".gif": "image/gif", ".svg": "image/svg+xml"}.get(suffix)
    if not mime:
        return None
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def embed_images(html: str, src_dir: Path) -> tuple[str, int, int]:
    """Inline local figures as data URIs — Reader cannot see the local filesystem."""
    embedded = dropped = 0
    tmpdir = Path(tempfile.mkdtemp(prefix="arxiv_fig_"))

    def resolve(ref: str) -> Path | None:
        ref = ref.split("?")[0]
        cand = (src_dir / ref)
        if cand.exists():
            return cand
        # LaTeX often omits the extension. Append rather than with_suffix() so
        # names containing dots aren't truncated at the first one.
        for ext in (".png", ".jpg", ".jpeg", ".pdf", ".eps", ".gif", ".svg"):
            if Path(str(cand) + ext).exists():
                return Path(str(cand) + ext)
            if cand.suffix and cand.with_suffix(ext).exists():
                return cand.with_suffix(ext)
        matches = list(src_dir.rglob(Path(ref).name + "*"))
        return matches[0] if matches else None

    def repl(m: re.Match) -> str:
        nonlocal embedded, dropped
        # group(1) is the full src; group(2) is only the basename. Resolve on
        # the full path — rendered table images live outside the source tree
        # and are referenced absolutely, so a basename lookup never finds them.
        tag, ref = m.group(0), m.group(1)
        if ref.startswith(("http://", "https://", "data:")):
            return tag
        path = resolve(ref)
        uri = image_to_data_uri(path, tmpdir) if path else None
        if not uri:
            dropped += 1
            return ""
        embedded += 1
        return tag.replace(m.group(1), uri, 1)

    # pandoc emits both <img src> and <embed src> for graphics
    html = re.sub(r'<(?:img|embed)[^>]*src="([^"]*?([^"/]+))"[^>]*/?>', repl, html)
    shutil.rmtree(tmpdir, ignore_errors=True)
    return html, embedded, dropped


def build_header(meta: dict, abs_url: str) -> str:
    authors = ", ".join(meta.get("authors", []))
    abstract = re.sub(r"\s+", " ", meta.get("abstract", "")).strip()
    parts = [
        f'<p><em>{authors}</em> — '
        f'<a href="{abs_url}">arXiv:{meta.get("versioned_id", "")}</a></p>'
    ]
    if abstract:
        parts.append(f"<h2>Abstract</h2>\n<blockquote><p>{abstract}</p></blockquote>")
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(
        description="Render an arXiv paper to clean HTML and save it to Readwise Reader."
    )
    p.add_argument("paper", help="arXiv ID, abs/pdf URL, or DOI")
    p.add_argument("--location", default="later",
                   choices=["new", "later", "archive", "feed"])
    p.add_argument("--tags", default="arxiv",
                   help="comma-separated tags (default: arxiv)")
    p.add_argument("--no-images", action="store_true", help="skip figure embedding")
    p.add_argument("--no-refs", action="store_true", help="omit the References section")
    p.add_argument("--dry-run", action="store_true",
                   help="write HTML locally, do not upload")
    p.add_argument("--out", help="also write the final HTML to this path")
    p.add_argument("--replace", action="store_true",
                   help="if the paper is already in Reader, delete and re-save it")
    p.add_argument("--force-fetch", action="store_true",
                   help="re-download the source even if cached")
    p.add_argument("--clean-html", action="store_true",
                   help="let Reader run its readability cleaner (it deletes "
                        "reference lists and some sections; off by default)")
    p.add_argument("--tables", choices=["dense", "all", "none"], default="dense",
                   help="render tables as images: dense (default, wide grids "
                        "only), all, or none")
    p.add_argument("--table-min-cols", type=int, default=TABLE_MIN_COLS,
                   help=f"column count at which a table becomes an image "
                        f"(default {TABLE_MIN_COLS})")
    p.add_argument("--unversioned-url", action="store_true",
                   help="save under the bare abs URL instead of the versioned one "
                        "(risks reusing Reader's cached parse of that URL)")
    args = p.parse_args()

    print(f"→ fetching {args.paper} …")
    manifest = fetch_paper(args.paper, args.force_fetch)
    cache_dir = Path(manifest["cache_dir"])
    # fetch.py sometimes caches under an unversioned dir and writes no meta.json.
    # Re-fetching by the resolved versioned ID lands in the canonical versioned
    # dir with full metadata. Never fall back to a sibling version's meta.json —
    # that would attach v1's metadata to v2's text.
    if not (cache_dir / "meta.json").exists() and manifest.get("versioned_id"):
        print(f"  metadata missing — re-fetching as {manifest['versioned_id']} …")
        manifest = fetch_paper(manifest["versioned_id"], args.force_fetch)
        cache_dir = Path(manifest["cache_dir"])
    meta_path = cache_dir / "meta.json"
    if not meta_path.exists():
        die(
            f"no meta.json under {cache_dir}; the fetch looks incomplete. "
            "Retry with --force-fetch."
        )
    meta = json.loads(meta_path.read_text())
    meta.setdefault("id", manifest.get("id", ""))
    meta.setdefault("versioned_id", manifest.get("versioned_id", ""))
    meta.setdefault("title", manifest.get("title", "Untitled"))

    tex = manifest.get("flattened_tex")
    if not tex or not Path(tex).exists():
        die(
            "no LaTeX source available for this paper (source may be PDF-only). "
            "This pipeline requires LaTeX; read the PDF in Reader instead."
        )
    tex_path = Path(tex)
    # An interrupted fetch leaves a truncated flattened.tex that later runs reuse.
    if r"\end{document}" not in tex_path.read_text(errors="replace"):
        if args.force_fetch:
            die(f"{tex_path} is truncated even after a forced re-fetch.")
        print("  cached LaTeX looks truncated — re-fetching …")
        manifest = fetch_paper(meta.get("versioned_id") or args.paper, True)
        cache_dir = Path(manifest["cache_dir"])
        tex_path = Path(manifest["flattened_tex"])
    src_dir = Path(manifest.get("source") or tex_path.parent)
    abs_url = f"https://arxiv.org/abs/{meta['id']}"
    print(f"  {meta['versioned_id']} — {meta['title']}")

    unwrapped, n_boxes = unwrap_scale_boxes(tex_path.read_text(errors="replace"))
    if n_boxes:
        print(f"  unwrapped {n_boxes} scale/resize box(es) so their tables survive")
        staged = cache_dir / "unwrapped.tex"
        staged.write_text(unwrapped)
        tex_path = staged

    if args.tables != "none" and not args.no_images:
        if not shutil.which("pdflatex"):
            print("  tables: pdflatex not found — leaving tables as HTML")
        else:
            print("→ rendering dense tables as images …")
            tex_text = tex_path.read_text(errors="replace")
            new_tex, n_ok, n_bad = render_tables_as_images(
                tex_text, src_dir, cache_dir, args.table_min_cols,
                force_all=(args.tables == "all"),
            )
            print(f"  tables rendered: {n_ok}, failed: {n_bad}")
            if n_ok:
                staged = cache_dir / "with_table_images.tex"
                staged.write_text(new_tex)
                tex_path = staged

    print("→ converting LaTeX → HTML …")
    html = latex_to_html(tex_path, src_dir)

    html = fix_headings(html)
    html = fix_math(html)

    used_keys = re.findall(r'data-cites="([^"]*)"', html)
    used_keys = [k for group in used_keys for k in group.split()]
    bib = parse_bibliography(src_dir)
    html, n_cites = restore_citations(html, bib)
    print(f"  citations restored: {n_cites} (bibliography entries: {len(bib)})")

    if args.no_images:
        html = re.sub(r'<(?:img|embed)[^>]*>', "", html)
        print("  figures: skipped (--no-images)")
    else:
        html, embedded, dropped = embed_images(html, src_dir)
        print(f"  figures embedded: {embedded}, dropped: {dropped}")

    html = build_header(meta, abs_url) + html
    if not args.no_refs:
        html += render_references(bib, used_keys)

    if len(html.encode()) > MAX_HTML_BYTES:
        die(
            f"HTML is {len(html.encode()) // 1024} KB, over the "
            f"{MAX_HTML_BYTES // 1024} KB guard. Retry with --no-images."
        )
    print(f"  final HTML: {len(html.encode()) // 1024} KB")

    out_path = Path(args.out) if args.out else None
    if args.dry_run and not out_path:
        out_path = Path(tempfile.gettempdir()) / f"{meta['versioned_id']}.html"
    if out_path:
        out_path.write_text(html)
        print(f"  wrote {out_path}")

    if args.dry_run:
        print("dry run — nothing uploaded")
        return

    token = find_token()
    # Reader caches its parsed content per URL: re-saving the same URL can serve
    # the earlier parse instead of this HTML. The versioned URL is both a fresh
    # cache key and a more honest identifier of what was actually rendered.
    save_url = abs_url if args.unversioned_url else (
        f"https://arxiv.org/abs/{meta.get('versioned_id') or meta['id']}"
    )
    payload = {
        "url": save_url,
        "html": html,
        # Our HTML is already clean. Reader's cleaner strips <h1>s, trailing
        # reference lists, and occasionally whole sections, so leave it off.
        "should_clean_html": args.clean_html,
        "title": meta["title"],
        "author": ", ".join(meta.get("authors", [])),
        "summary": re.sub(r"\s+", " ", meta.get("abstract", "")).strip()[:2000],
        "published_date": meta.get("published"),
        "location": args.location,
        "category": "article",
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
        "saved_using": "arxiv-to-reader",
    }

    print(f"→ saving to Reader ({args.location}) …")
    status, body = api("POST", SAVE_URL, token, payload)

    if status == 200 and args.replace and body.get("id"):
        print(f"  already in Reader ({body['id']}) — replacing …")
        api("DELETE", DELETE_URL.format(body["id"]), token)
        status, body = api("POST", SAVE_URL, token, payload)

    if status == 201:
        print(f"✓ created: {body.get('url')}")
    elif status == 200:
        print(f"✓ already existed (content unchanged): {body.get('url')}")
        print("  use --replace to overwrite it with this render")
    else:
        die(f"save failed [{status}]: {json.dumps(body)[:500]}")

    if status in (200, 201) and body.get("id"):
        vs, vbody = api("GET", f"{LIST_URL}?id={body['id']}", token)
        if vs == 200 and vbody.get("results"):
            doc = vbody["results"][0]
            print(f"  verified: {doc.get('word_count')} words, "
                  f"location={doc.get('location')}")


if __name__ == "__main__":
    main()
