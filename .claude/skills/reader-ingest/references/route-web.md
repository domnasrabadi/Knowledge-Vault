# Route: web pages

Websites go into Reader through the API as clean HTML, after the user confirms.
If the page is really a long multi-part document (a web book, a report split over
many pages), take `route-epub-build.md` instead.

## The flow

```bash
S="/Users/domnasrabadi/Knowledge Vault/.claude/skills/reader-ingest/scripts"
cd "$BUILD"
curl -sL -A "Mozilla/5.0 (Macintosh)" -o page.html "<url>"
curl -sL -A "Mozilla/5.0 (Macintosh)" -o site.css "<main stylesheet url>"   # for chart colours
uv run --with beautifulsoup4 --with lxml python "$S/web_extract.py" audit page.html
uv run --with beautifulsoup4 --with lxml python "$S/web_extract.py" body page.html body.html
#   (purpose-written transforms for what the audit flagged: recipes below)
#   (inline SVG charts:  rasterize.py svgs page.html charts/  then swap to <img>)
python3 "$S/html_for_api.py" body.html meta.json page-api.html
python3 "$S/reader_api.py" check "<url>"
#   AskUserQuestion — then:
python3 "$S/reader_api.py" save page-api.html meta.json [--fresh-url]
```

Why each step exists:

- **`curl`, not WebFetch.** WebFetch returns prose, not markup, and times out on
  large pages. You need the DOM.
- **`audit` lists text with no `<p>` around it.** That is exactly what readability-style
  parsers strip as furniture. We upload with Reader's cleaner **off**, so the
  API route is less exposed than a Reader scrape was, but the audit is still the
  map of components that need real structure: cards, callouts, comparisons,
  tooltips. Read it; substantial entries need a transform from the recipes below.
- **`body` converts KaTeX / MathJax to `$…$`** using the TeX source, since that's
  the maths policy on every route. It reports formulas with no recoverable
  source.
- **Inline `<svg>` charts must become `<img>`**: pandoc drops raw SVG, and
  `rasterize.py svgs` resolves the site's `var(--x)` colours first, which would
  otherwise render black on black. Build the alt text from the chart's own labels.
- **`html_for_api.py`** shifts headings so no `<h1>` is left, turns `<embed>`
  into `<img>`, embeds local images, turns iframes into links, and prints the
  stats the user sees before saying yes.

`meta.json`: `title`, `authors` (site name if no person), `date`, `url`
(the article's real URL, since highlights link back to it), `description`, `tags`.

If Reader already has the article (it usually does, since that's why the user is
here), `check` will find it. Follow the replace / keep both / cancel flow in
`reader-api.md`.

## Images: classify before you decide

This is a question for the user (AskUserQuestion), not a judgement call. The right
handling differs by class, and so does the user's preference. It applies to
PDFs and long builds too.

1. **Check alt text first.** One article had 27 images and zero `alt` attributes:
   in Reader that is 27 unlabelled pictures with their content unhighlightable
   and unsearchable.
2. **Read every image**, then classify: the author's own diagrams / third-party
   screenshots they are quoting / memes / title slides. One real split was
   8 transcribe, 4 cite-and-quote, 12 memes, 3 title slides.
3. **Transcribe to real markup** (tables, lists, `<pre>`) in visually distinct
   blocks, so a transcription is never mistaken for the author's prose. Eight
   diagrams became 2 tables and 54 list items of highlightable text.
4. **Third-party screenshots** get a short attributed quote plus a description,
   not a full transcription.
5. **Account for all N** in the report, and **flag the judgement calls**. One
   slide filed as a meme carried real content; say so rather than letting it
   disappear under a rule the user set.

---

# Rescuing custom web components

`web_extract.py audit` tells you *what* is at risk. This is *how* to convert the
common shapes so their meaning survives, with BeautifulSoup.

The rule: every piece of prose ends up inside a `<p>`, and the relationship
between pieces (question ↔ critique, before ↔ after, badge ↔ label) stays legible
when all styling is gone. Assume the reader sees no CSS.

## Setup

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('page.html').read(), 'lxml')
art = soup.find('article')

def new(tag, cls=None):
    t = soup.new_tag(tag)
    if cls: t['class'] = cls
    return t

def para(text, cls=None):
    p = new('p', cls); p.string = text; return p
```

## Q/A or example card with a critique line

`<div class="card"><div class="line"><span>Q.</span> …</div><div class="feedback">…</div></div>`

Becomes a blockquote whose lines are paragraphs. Keep the marker as `<strong>` so
"Q."/"A." survives, and mark the critique visually distinct — it's commentary,
not content.

```python
def card_to_block(el):
    bq = new('blockquote', 'card')
    for label in el.select('.badge, .tier-label'):        # badges FIRST — often nested
        bq.append(para(label.get_text(' ', strip=True), 'card-label'))
    for line in el.select('.line'):
        marker = line.select_one('.qa-marker')
        mk = marker.get_text(strip=True) if marker else ''
        if marker: marker.extract()
        p = new('p')
        if mk:
            b = new('strong'); b.string = mk + ' '; p.append(b)
        p.append(line.get_text(' ', strip=True))
        bq.append(p)
    fb = el.select_one('.feedback')
    if fb:
        for sv in fb.select('svg'): sv.decompose()        # drop decorative icons
        bq.append(para('→ ' + fb.get_text(' ', strip=True), 'card-note'))
    return bq
```

**Watch the nesting order.** Badges, tier labels and captions frequently live
*inside* the card alongside the lines. A converter that only reads `.line` will
drop them silently — this bit me on a real run. Convert innermost-outward and
always diff the text content of the original element against your replacement.

## Two-column before/after comparison

Columns are a visual device; linearise them with explicit labels, since a reader
in a single-column EPUB has no other cue which side is which.

```python
for comp in art.select('.comparison'):
    wrap = new('div', 'comparison')
    if (lab := comp.select_one('.comparison-label')):
        p = new('p', 'comparison-label')
        b = new('strong'); b.string = lab.get_text(' ', strip=True); p.append(b)
        wrap.append(p)
    for col in comp.select('.comparison-col'):
        if (tag := col.select_one('.col-tag')):
            p = new('p', 'comparison-tag')
            em = new('em'); em.string = tag.get_text(' ', strip=True); p.append(em)
            wrap.append(p)
        for card in col.select('.card'):
            wrap.append(card_to_block(card))
    comp.replace_with(wrap)
```

## Badge + label pairs

`<span class="badge">T3</span><span class="label">Ready to Review</span>` →
`<p><strong>T3 — </strong>Ready to Review</p>`. Trivial, but these are often the
rubric the whole piece is built on.

## Asides / callouts

A bare `<aside>Text</aside>` has no `<p>` and gets stripped. Wrap it:

```python
for a in art.find_all('aside'):
    bq = new('blockquote', 'aside-note')
    if not a.find('p'):
        bq.append(para(a.get_text(' ', strip=True)))
    else:
        for c in list(a.children): bq.append(c.extract())
    a.replace_with(bq)
```

## Tooltips and hover definitions

Hidden popup text is real content the reader can never hover for. Inline it:

```python
for t in art.select('.tooltip-trigger'):
    pop = t.select_one('.tooltip-popup')
    definition = pop.get_text(' ', strip=True) if pop else ''
    if pop: pop.extract()
    span = new('span'); span.append(t.get_text(' ', strip=True))
    if definition:
        em = new('em'); em.string = f' ({definition})'; span.append(em)
    t.replace_with(span)
```

## Charts

Inline SVG never survives conversion; pandoc's HTML reader drops it. Rasterise
(`rasterize.py svgs`), then swap each `<svg>` for an `<img>` with alt text built
from the chart's own `<text>` labels, so the data stays searchable:

```python
img = soup.new_tag('img')
img['src'] = "data:image/png;base64," + base64.b64encode(png_bytes).decode()
img['alt'] = ("Chart: " + "; ".join(dict.fromkeys(labels)))[:480]
sv.replace_with(img)
```

CSS-driven bar charts (a `<div>` whose `width:%` *is* the bar) can't rasterise —
keep the numeric cells, hide the bar div, and tell the user the bars are gone but
the numbers are intact.

## Always finish by diffing

```python
before = set(orig_article.get_text(' ', strip=True).split())
after  = set(new_article.get_text(' ', strip=True).split())
print("words lost:", sorted(before - after)[:40])
```

Anything meaningful in that list is a component you missed.
