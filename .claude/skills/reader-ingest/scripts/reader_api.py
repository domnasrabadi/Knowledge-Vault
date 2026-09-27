#!/usr/bin/env python3
"""Everything that talks to Readwise Reader, for every API route.

    reader_api.py check  <url> [<url> ...] [--title "..."] [--full-sync]
    reader_api.py save   page.html meta.json [--location later] [--tags a,b] [--fresh-url]
    reader_api.py verify <doc-id> page.html [--probe "..."]
    reader_api.py delete <doc-id> --yes [--yes-lose-highlights]

Stdlib only. Token: $READWISE_TOKEN, else ~/Downloads/reader4/.env.

The order is the safety mechanism, and the skill must follow it:

  check   -> is this source already in Reader, and how many highlights does it hold?
  (ask)   -> the user confirms the upload, and decides about any existing copy
  save    -> upload; --fresh-url when a copy exists (see below). Verifies itself.
  delete  -> the OLD copy, only after the new one verified, only if the user said so

Three Reader behaviours this works around (all observed, none documented):
  1. Re-saving a URL Reader already has can return 200 "exists" and IGNORE the
     new HTML, or return 201 and create a silent duplicate. Hence --fresh-url,
     which saves under a distinct URL. arXiv avoids it with versioned URLs.
  2. Reader caches its parse per URL, so delete-then-resave can serve the old one.
  3. Deleting a document deletes its highlights. Hence the highlight count up
     front, and --yes-lose-highlights.

The list endpoint has no URL filter and allows 20 calls/minute, so the library
is cached at ~/.cache/reader-ingest/ and refreshed incrementally (updatedAfter).
First run pages the whole library once; later checks cost a call or two.
"""
import os, re, sys, json, time, datetime, pathlib, urllib.parse, urllib.request, urllib.error

SAVE_URL = 'https://readwise.io/api/v3/save/'
LIST_URL = 'https://readwise.io/api/v3/list/'
DELETE_URL = 'https://readwise.io/api/v3/delete/{}/'
CACHE = pathlib.Path(os.path.expanduser('~/.cache/reader-ingest/library.json'))
TOKEN_ENV_FILES = [pathlib.Path(os.path.expanduser(p)) for p in (
    '~/Downloads/reader4/.env', '~/.config/readwise/.env')]
DOC_CATEGORIES = ('article', 'pdf', 'epub')   # where a duplicate of our sources can live
TRACKING = re.compile(r'^(utm_\w+|ref|source|fbclid|gclid|mc_\w+|reader-ingest)$')


# ---------------------------------------------------------------- plumbing

def die(msg):
    print(f'error: {msg}', file=sys.stderr)
    sys.exit(1)


def find_token():
    if os.environ.get('READWISE_TOKEN'):
        return os.environ['READWISE_TOKEN'].strip()
    for p in TOKEN_ENV_FILES:
        if p.exists():
            for line in p.read_text().splitlines():
                if line.strip().startswith('READWISE_TOKEN='):
                    return line.split('=', 1)[1].strip().strip('"\'')
    die(f'no Readwise token: set READWISE_TOKEN or add it to {TOKEN_ENV_FILES[0]}')


def api(method, url, token, payload=None, retries=4):
    """One call, with Retry-After honoured on 429 (list allows 20/min)."""
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {'Authorization': f'Token {token}'}
    if data:
        headers['Content-Type'] = 'application/json'
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read().decode() or '{}'
                return r.status, (json.loads(body) if body.strip() else {})
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries:
                wait = int(e.headers.get('Retry-After') or 30) + 1
                print(f'  rate-limited; waiting {wait}s …', file=sys.stderr)
                time.sleep(wait)
                continue
            body = e.read().decode()
            try:
                return e.code, json.loads(body)
            except json.JSONDecodeError:
                return e.code, {'detail': body[:500]}


def norm_url(u):
    """Comparable form of a URL. arXiv collapses to its paper id across abs/pdf/versions."""
    if not u:
        return ''
    m = re.search(r'arxiv\.org/(?:abs|pdf|html)/([0-9]{4}\.[0-9]{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/[0-9]{7})', u)
    if m:
        return f'arxiv:{m.group(1)}'
    p = urllib.parse.urlsplit(u.strip())
    host = p.netloc.lower().removeprefix('www.')
    query = urllib.parse.urlencode([(k, v) for k, v in urllib.parse.parse_qsl(p.query)
                                    if not TRACKING.match(k)])
    path = p.path.rstrip('/') or '/'
    return f'{host}{path}' + (f'?{query}' if query else '')


def norm_title(t):
    return ' '.join(re.sub(r'[^\w\s]', ' ', (t or '').lower()).split())


# ---------------------------------------------------------------- library cache

def sync(token, full=False):
    """Refresh the cached index of documents and highlight counts."""
    cache = {} if full or not CACHE.exists() else json.loads(CACHE.read_text())
    docs = cache.get('docs', {})
    hl = cache.get('highlights', {})          # highlight id -> parent doc id
    since = cache.get('synced_at')
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()

    def pages(params):
        cursor, n = None, 0
        while True:
            q = dict(params, **({'pageCursor': cursor} if cursor else {}))
            status, body = api('GET', LIST_URL + '?' + urllib.parse.urlencode(q), token)
            if status != 200:
                die(f'list failed [{status}]: {json.dumps(body)[:300]}')
            n += 1
            yield from body.get('results', [])
            cursor = body.get('nextPageCursor')
            if not cursor:
                return

    base = {'updatedAfter': since} if since else {}
    print(f"  syncing Reader library ({'incremental since ' + since[:19] if since else 'first full pass — may take a few minutes'}) …",
          file=sys.stderr)
    for cat in DOC_CATEGORIES:
        for d in pages(dict(base, category=cat)):
            docs[d['id']] = {k: d.get(k) for k in ('title', 'source_url', 'url', 'category', 'location', 'word_count')}
    for h in pages(dict(base, category='highlight')):
        if h.get('parent_id'):
            hl[h['id']] = h['parent_id']

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps({'synced_at': started, 'docs': docs, 'highlights': hl}))
    return docs, hl


def highlight_count(hl, doc_id):
    return sum(1 for parent in hl.values() if parent == doc_id)


# ---------------------------------------------------------------- commands

def cmd_check(args):
    urls = [a for a in args if not a.startswith('--')]
    title = args[args.index('--title') + 1] if '--title' in args else None
    if title in urls:
        urls.remove(title)
    token = find_token()
    docs, hl = sync(token, full='--full-sync' in args)

    wanted = {norm_url(u) for u in urls if u}
    wanted_title = norm_title(title) if title else None
    matches = []
    for doc_id, d in docs.items():
        if (norm_url(d.get('source_url')) in wanted or norm_url(d.get('url')) in wanted
                or (wanted_title and norm_title(d.get('title')) == wanted_title)):
            matches.append((doc_id, d))

    # Incremental sync never learns about deletions. Confirm each match still exists.
    live = []
    for doc_id, d in matches:
        status, body = api('GET', f'{LIST_URL}?id={doc_id}', token)
        if status == 200 and body.get('results'):
            live.append((doc_id, d))
        else:
            docs.pop(doc_id, None)
    if len(live) != len(matches):
        cache = json.loads(CACHE.read_text())
        cache['docs'] = docs
        CACHE.write_text(json.dumps(cache))

    if not live:
        print('NOT IN READER — safe to save normally.')
        return
    print(f'ALREADY IN READER — {len(live)} existing cop{"y" if len(live) == 1 else "ies"}:')
    for doc_id, d in live:
        n = highlight_count(hl, doc_id)
        print(f"  {doc_id}  {d.get('category')}/{d.get('location')}  {d.get('word_count') or '?'} words  "
              f"{n} highlight{'s' if n != 1 else ''}  — {d.get('title')}")
        print(f"      {d.get('source_url')}")
    print('Ask the user: replace (save with --fresh-url, verify, then delete the old copy), '
          'keep both (save with --fresh-url), or cancel. Deleting the old copy deletes its highlights.')


def cmd_save(args):
    pos = [a for a in args if not a.startswith('--')]
    html_path, meta_path = pathlib.Path(pos[0]), pathlib.Path(pos[1])
    opt = lambda k, d=None: args[args.index(k) + 1] if k in args else d
    meta = json.loads(meta_path.read_text())
    html = html_path.read_text()

    url = meta['url']
    if '--fresh-url' in args:
        # A distinct URL is a fresh cache key: Reader neither ignores the new HTML
        # nor serves its cached parse. The query param is harmless on click-through.
        stamp = datetime.date.today().strftime('%Y%m%d')
        url += ('&' if '?' in url else '?') + f'reader-ingest={stamp}'

    tags = [t for t in (meta.get('tags') or []) + (opt('--tags', '') or '').split(',') if t.strip()]
    summary = meta.get('description') or re.sub(r'<[^>]+>', ' ', meta.get('abstract') or '')
    payload = {
        'url': url,
        'html': html,
        # Our HTML is already clean. Reader's cleaner deletes body <h1>s, trailing
        # reference lists and occasionally whole sections — it stays off. With it
        # off, the API requires title and author.
        'should_clean_html': False,
        'title': meta['title'],
        'author': ', '.join(meta.get('authors', [])) or meta.get('venue') or 'Unknown',
        'summary': ' '.join(summary.split())[:2000],
        'location': opt('--location', 'later'),
        'category': 'article',
        'tags': sorted(set(t.strip() for t in tags)),
        'saved_using': 'reader-ingest',
    }
    if re.match(r'^\d{4}-\d{2}-\d{2}', str(meta.get('date', ''))):
        payload['published_date'] = str(meta['date'])[:10]
    if meta.get('cover_url'):
        payload['image_url'] = meta['cover_url']

    token = find_token()
    print(f"→ saving to Reader ({payload['location']}) as {url} …")
    status, body = api('POST', SAVE_URL, token, payload)
    if status == 200:
        print(f"! Reader already had this URL and KEPT ITS OLD COPY — the new HTML was ignored.\n"
              f"  existing: {body.get('url')}\n  re-run with --fresh-url")
        sys.exit(3)
    if status != 201:
        die(f'save failed [{status}]: {json.dumps(body)[:500]}')
    print(f"✓ created {body.get('id')}: {body.get('url')}")
    verify(token, body['id'], html, [])


def verify(token, doc_id, local_html, probes):
    """Compare what Reader STORED against what we sent. Reader is the ground truth."""
    for attempt in range(4):
        status, body = api('GET', f'{LIST_URL}?id={doc_id}&withHtmlContent=true', token)
        doc = (body.get('results') or [None])[0] if status == 200 else None
        if doc and doc.get('html_content'):
            break
        time.sleep(5)   # Reader parses asynchronously; the first read can be empty
    else:
        print(f'  ! could not read back {doc_id} yet — verify later with: reader_api.py verify {doc_id} <page.html>')
        return False

    stored = doc['html_content']
    def counts(h):
        return {t: len(re.findall(rf'<{t}[\s>]', h)) for t in ('h1', 'h2', 'h3', 'p', 'table', 'pre', 'img', 'embed')}
    def words(h):
        return len(re.sub(r'<[^>]+>', ' ', h).split())
    sent, kept = counts(local_html), counts(stored)
    w_sent, w_kept = words(local_html), words(stored)

    print(f'  verify: {w_kept:,} words stored of {w_sent:,} sent '
          f'({100 * w_kept // max(w_sent, 1)}%); Reader reports {doc.get("word_count")}')
    for t in ('h2', 'h3', 'table', 'pre', 'img'):
        flag = '' if kept[t] >= sent[t] else '   <-- LOST'
        print(f'    {t:6} sent {sent[t]:>4}  stored {kept[t]:>4}{flag}')
    problems = [t for t in ('h2', 'h3', 'table', 'pre', 'img') if kept[t] < sent[t]]
    if w_kept < w_sent * 0.97:
        problems.append('words')
    flat = ' '.join(re.sub(r'<[^>]+>', ' ', stored).split())
    missing = [p for p in probes if ' '.join(p.split()) not in flat]
    for p in missing:
        print(f'    MISSING probe: {p[:70]}')
    ok = not problems and not missing
    print('  ✓ verified — Reader kept everything' if ok else f'  ! Reader dropped content: {problems + (["probes"] if missing else [])}')
    return ok


def cmd_verify(args):
    pos = [a for a in args if not a.startswith('--')]
    probes = [args[i + 1] for i, a in enumerate(args) if a == '--probe']
    pos = [p for p in pos if p not in probes]
    ok = verify(find_token(), pos[0], pathlib.Path(pos[1]).read_text(), probes)
    sys.exit(0 if ok else 1)


def cmd_delete(args):
    doc_id = next(a for a in args if not a.startswith('--'))
    token = find_token()
    hl = json.loads(CACHE.read_text()).get('highlights', {}) if CACHE.exists() else {}
    n = highlight_count(hl, doc_id)
    print(f'{doc_id}: {n} highlight(s) in the cached index')
    if '--yes' not in args:
        die('refusing to delete without --yes (the user must have agreed in chat)')
    if n and '--yes-lose-highlights' not in args:
        die(f'this document has {n} highlight(s), which deleting destroys. '
            'Pass --yes-lose-highlights only if the user explicitly accepted that.')
    status, body = api('DELETE', DELETE_URL.format(doc_id), token)
    if status not in (200, 204):
        die(f'delete failed [{status}]: {json.dumps(body)[:300]}')
    print(f'✓ deleted {doc_id}')


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ('check', 'save', 'verify', 'delete'):
        print(__doc__)
        sys.exit(2)
    {'check': cmd_check, 'save': cmd_save, 'verify': cmd_verify, 'delete': cmd_delete}[sys.argv[1]](sys.argv[2:])
