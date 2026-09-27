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

Inline SVG never reaches the EPUB — pandoc's HTML reader drops it. Rasterise
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
