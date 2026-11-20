# -*- coding: utf-8 -*-
"""Dane treści edytowane przez panel „Eve Admin” (Gry) — pliki JSON w content/. Format: docs/admin-data-format.md.
 • content/gallery.json   — galeria (rozkładówka 'spread' + siatka 'grid'; panel dopisuje do 'grid')
 • content/posts/<slug>.json — wpisy z panelu (obok wpisów botów blog/posts/<lang>/*.md)
 • content/ads.json       — baner sponsora (gdy aktywny, zastępuje baner reklamy własnej w tych samych miejscach)
Zasada: błędny plik/wpis z panelu NIE wywraca builda — jest pomijany z ostrzeżeniem „UWAGA (content)”.
Sprawdzenie bez budowania:  python3 scripts/content.py   (kod wyjścia 1 = są błędy)"""
import os, re, sys, json, html, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
C = os.path.join(ROOT, 'content')
LANGS = ['pl', 'en', 'es', 'pt', 'it', 'ja', 'zh']
FALLBACK = ['en', 'pl']
SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
UPLOAD_RE = re.compile(r'^assets/img/uploads/[a-z0-9/-]+\.webp$')
esc = lambda s: html.escape(str(s), quote=True)
PROBLEMS = []

def warn(msg):
    PROBLEMS.append(msg); print('UWAGA (content):', msg, file=sys.stderr)

def _load(rel):
    p = os.path.join(C, rel)
    try:
        with open(p, encoding='utf-8') as f: return json.load(f)
    except FileNotFoundError: return None
    except Exception as e: warn(f'{rel}: niepoprawny JSON ({e})'); return None

def pick(d, lang):
    """Tekst w danym języku; brak -> en -> pl -> pierwszy dostępny."""
    if isinstance(d, str): return d
    if not isinstance(d, dict) or not d: return ''
    for l in [lang] + FALLBACK:
        if d.get(l): return d[l]
    return next(iter(d.values()))

def _img_ok(path, what):
    if not isinstance(path, str) or '..' in path or not path.startswith('assets/'):
        warn(f'{what}: zła ścieżka obrazka {path!r}'); return False
    if not os.path.exists(os.path.join(ROOT, path)):
        warn(f'{what}: brak pliku {path}'); return False
    return True

# ---------------- galeria ----------------
def load_gallery():
    g = _load('gallery.json')
    if g is None: sys.exit('Brak/niepoprawny content/gallery.json — galeria jest wymagana')
    out = {}
    for sec in ('spread', 'grid'):
        items = []
        for i, it in enumerate(g.get(sec, [])):
            what = f'gallery.json {sec}[{i}] ({it.get("id", "?")})'
            if it.get('hidden'): continue
            if not it.get('caption'): warn(f'{what}: brak caption'); continue
            if not (_img_ok(it.get('full'), what) and _img_ok(it.get('thumb'), what)): continue
            items.append(it)
        out[sec] = items
    return out

# ---------------- wpisy z panelu ----------------
def _excerpt(body, n=160):
    t = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', body)
    t = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', t)
    t = re.sub(r'[#>*`_]+', '', t); t = ' '.join(t.split())
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'

def load_json_posts(categories):
    """-> {lang: [dict jak parse_post()]} dla content/posts/*.json (bez szkiców)."""
    res = {l: [] for l in LANGS}
    d = os.path.join(C, 'posts')
    if not os.path.isdir(d): return res
    for f in sorted(os.listdir(d)):
        if not f.endswith('.json'): continue
        rel = 'posts/' + f; p = _load(rel)
        if p is None: continue
        slug = f[:-5]
        if p.get('slug', slug) != slug or not SLUG_RE.match(slug): warn(f'{rel}: slug musi = nazwa pliku i pasować do a-z0-9-'); continue
        if p.get('draft'): continue
        try: date = datetime.date.fromisoformat(p.get('date', ''))
        except ValueError: warn(f'{rel}: zła data {p.get("date")!r} (RRRR-MM-DD)'); continue
        cat = p.get('category')
        if cat not in categories: warn(f'{rel}: nieznana kategoria {cat!r}; dozwolone: {", ".join(categories)}'); continue
        cover = (p.get('cover') or '').strip()
        if cover and not os.path.exists(os.path.join(ROOT, 'assets/img', cover + '.webp')):
            warn(f'{rel}: cover assets/img/{cover}.webp nie istnieje'); continue
        og = ('assets/img/' + cover + '.webp' if '/' in cover else cover) if cover else 'eve-biblioteka'
        for lang, t in (p.get('i18n') or {}).items():
            if lang not in LANGS: warn(f'{rel}: nieznany język {lang}'); continue
            if not (t.get('title') and t.get('body')): warn(f'{rel} [{lang}]: wymagane title i body'); continue
            res[lang].append(dict(lang=lang, slug=slug, date=date, title=t['title'], category=cat,
                                  excerpt=t.get('excerpt') or _excerpt(t['body']), cover=cover, og_photo=og,
                                  draft=False, body=t['body'].replace('\r\n', '\n'), file=os.path.join(d, f)))
    return res

# ---------------- baner sponsora ----------------
def load_sponsor():
    a = _load('ads.json')
    s = (a or {}).get('sponsor') or {}
    if not s.get('active'): return None
    what = 'ads.json sponsor'
    if not str(s.get('link', '')).startswith('https://'): warn(f'{what}: link musi zaczynać się od https://'); return None
    if not _img_ok(s.get('image'), what): return None
    return s

def sponsor_banner(s, lang, r, kind):
    """Baner sponsora w miejscu banera reklamy własnej (ta sama ramka .hads). Style inline — bez zmian w CSS."""
    lbl = pick(s.get('label') or {}, lang) or 'Partner'
    alt = pick(s.get('alt') or {}, lang) or s.get('name', '')
    w, h = int(s.get('w', 1200)), int(s.get('h', 300))
    return (f'<aside class="hads" aria-label="{esc(lbl)}">'
            f'<a class="hads-in" href="{esc(s["link"])}" target="_blank" rel="sponsored noopener" data-ad="sponsor" data-ad-kind="{kind}"'
            f' data-goatcounter-click="sponsor-click-{kind}" data-goatcounter-title="{esc(s.get("name", "sponsor"))}"'
            f' style="display:block;padding:0;min-height:0;overflow:hidden">'
            f'<span class="hads-lbl" style="z-index:1;background:rgba(12,7,8,.7);padding:2px 6px">{esc(lbl)}</span>'
            f'<img src="{r}{esc(s["image"])}" alt="{esc(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"'
            f' style="display:block;width:100%;height:auto"></a></aside>')

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(__file__))
    from i18n import CATEGORIES
    g = load_gallery(); ps = load_json_posts(CATEGORIES); s = load_sponsor()
    print(f'galeria: spread {len(g["spread"])}, grid {len(g["grid"])}; wpisy z panelu: '
          + ', '.join(f'{l}:{len(v)}' for l, v in ps.items() if v) + f' ; sponsor: {"aktywny" if s else "brak"}')
    sys.exit(1 if PROBLEMS else 0)
