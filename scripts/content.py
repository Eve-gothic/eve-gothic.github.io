# -*- coding: utf-8 -*-
"""Dane treści edytowane przez panel „Eve Admin” (Gry) — pliki JSON w content/. Format: docs/admin-data-format.md.
 • content/gallery.json   — galeria (rozkładówka 'spread' + siatka 'grid'; panel dopisuje do 'grid')
 • content/posts/<slug>.json — wpisy z panelu (obok wpisów botów blog/posts/<lang>/*.md)
 • content/ads.json       — baner sponsora (gdy aktywny, zastępuje baner reklamy własnej w tych samych miejscach)
 • content/videos.json    — filmiki z panelu (przed filmikami z i18n.py VIDEOS) + assets/video/uploads/
 • content/home.json      — teksty strony głównej (kicker, deck, about, quote) nadpisujące i18n.py
 • content/theme.json     — wygląd strony: magazyn (domyślny) | neon | luksus | minimal | creator (css/themes/<nazwa>.css)
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

# ---------------- filmiki z panelu ----------------
VIDEO_RE = re.compile(r'^assets/video/uploads/[a-z0-9-]+\.(mp4|webp)$')
VIDEO_MAX_BYTES, POSTER_MAX_BYTES, VIDEO_MAX_SEC = 4 * 1024 * 1024, 120 * 1024, 20

def _video_file_ok(path, ext, what, max_bytes):
    """Ścieżka (tylko assets/video/uploads/…), istnienie, limit rozmiaru i sygnatura pliku."""
    if not isinstance(path, str) or not VIDEO_RE.match(path) or not path.endswith('.' + ext):
        warn(f'{what}: zła ścieżka {path!r} (oczekiwano assets/video/uploads/<a-z0-9->.{ext})'); return None
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full): warn(f'{what}: brak pliku {path}'); return None
    n = os.path.getsize(full)
    if n > max_bytes: warn(f'{what}: {path} ma {n // 1024} KB — limit {max_bytes // 1024} KB'); return None
    with open(full, 'rb') as f: data = f.read()
    if ext == 'webp':
        if not (data[:4] == b'RIFF' and data[8:12] == b'WEBP'): warn(f'{what}: {path} to nie WebP'); return None
    else:
        if data[4:8] != b'ftyp': warn(f'{what}: {path} to nie MP4'); return None
        if b'avc1' not in data and b'avc3' not in data: warn(f'{what}: {path} nie jest H.264'); return None
        if b'soun' in data: warn(f'{what}: {path} ma ścieżkę dźwięku (dozwolone tylko filmy bez dźwięku)'); return None
    return True

def load_videos():
    """-> lista pozycji z content/videos.json (kolejność jak w pliku; bez hidden i bez błędnych)."""
    v = _load('videos.json')
    if v is None: return []
    if not isinstance(v, dict): warn('videos.json: oczekiwano obiektu {"items": [...]}'); return []
    items, seen = [], set()
    if not isinstance(v.get('items', []), list): warn('videos.json: "items" musi być listą'); return []
    for i, it in enumerate(v.get('items', [])):
        if not isinstance(it, dict): warn(f'videos.json items[{i}]: pozycja musi być obiektem'); continue
        what = f'videos.json items[{i}] ({it.get("id", "?")})'
        if it.get('hidden'): continue
        vid = it.get('id')
        if not isinstance(vid, str) or not SLUG_RE.match(vid): warn(f'{what}: id musi pasować do a-z0-9-'); continue
        if vid in seen: warn(f'{what}: powtórzone id'); continue
        title = it.get('title')
        if not isinstance(title, dict) or not any(isinstance(x, str) and x.strip() for x in title.values()): warn(f'{what}: brak title'); continue
        if not _video_file_ok(it.get('mp4'), 'mp4', what, VIDEO_MAX_BYTES): continue
        if it.get('poster') is not None and not _video_file_ok(it.get('poster'), 'webp', what, POSTER_MAX_BYTES): continue
        try: w, h = int(it.get('w', 720)), int(it.get('h', 1280))
        except (TypeError, ValueError): warn(f'{what}: w/h muszą być liczbami'); continue
        if not (16 <= w <= 4096 and 16 <= h <= 4096): warn(f'{what}: w/h poza zakresem 16–4096'); continue
        dur = it.get('duration')
        if dur is not None and not (isinstance(dur, (int, float)) and 0 < dur <= VIDEO_MAX_SEC): warn(f'{what}: duration musi być 1–{VIDEO_MAX_SEC} s'); continue
        seen.add(vid); items.append(dict(it, w=w, h=h))
    return items

def video_article(it, lang, r, novideo, n_label):
    """<article> filmiku z panelu (bez <source webm>); n_label = „Kadr 03”."""
    poster = f' poster="{r}{esc(it["poster"])}"' if it.get('poster') else ''
    title = esc(pick(it['title'], lang))
    return (f'<article><video muted playsinline controls loop preload="none" data-hover{poster} width="{it["w"]}" height="{it["h"]}">'
            f'<source src="{r}{esc(it["mp4"])}" type="video/mp4">{novideo}</video><h3>{title}</h3><span class="sc">{n_label}</span></article>')

# ---------------- opis strony głównej ----------------
HOME_KEYS = {'kicker': 160, 'deck': 600, 'about': 3000, 'quote': 400}   # pole -> maks. długość

def load_home():
    """-> {lang: {pole: tekst}} z content/home.json (i18n). Teksty zwykłe (bez HTML); ostrzeżenie i pominięcie błędnych pól."""
    h = _load('home.json')
    out = {}
    if h is None: return out
    if not isinstance(h, dict): warn('home.json: oczekiwano obiektu {"i18n": {...}}'); return out
    if not isinstance(h.get('i18n', {}), dict): warn('home.json: "i18n" musi być obiektem'); return out
    for lang, d in (h.get('i18n') or {}).items():
        if lang not in LANGS: warn(f'home.json: nieznany język {lang}'); continue
        if not isinstance(d, dict): warn(f'home.json [{lang}]: musi być obiektem'); continue
        for k, v in d.items():
            if k.startswith('_'): continue
            if k not in HOME_KEYS: warn(f'home.json [{lang}]: nieznane pole {k!r} (dozwolone: {", ".join(HOME_KEYS)})'); continue
            if not isinstance(v, str) or not v.strip(): warn(f'home.json [{lang}] {k}: pusty lub nie-tekst'); continue
            if len(v) > HOME_KEYS[k]: warn(f'home.json [{lang}] {k}: {len(v)} znaków — limit {HOME_KEYS[k]}'); continue
            out.setdefault(lang, {})[k] = v.strip()
    return out

def _plain(s):
    return html.escape(s, quote=True).replace('&#x27;', "'")

def apply_home(T, home):
    """Nadpisuje T[lang][kicker|deck|about|quote] tekstami z panelu. Escape HTML, potem **x** -> <strong>x</strong> (tylko w about)."""
    for lang, d in home.items():
        if lang not in T: continue
        for k, v in d.items():
            t = _plain(v)
            if k == 'about': t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t, flags=re.S)
            T[lang][k] = t
    return T

def og_plain(s):
    """Tekst do obrazka OG (kicker) — bez encji HTML."""
    return html.unescape(s)

# ---------------- wygląd strony ----------------
THEMES = ('magazyn', 'neon', 'luksus', 'minimal', 'creator')
DEFAULT_THEME = 'magazyn'

def load_theme():
    t = _load('theme.json')
    if t is None: return DEFAULT_THEME
    name = t.get('theme') if isinstance(t, dict) else None
    if name not in THEMES:
        warn(f'theme.json: nieznany motyw {name!r}; dozwolone: {", ".join(THEMES)} — używam „{DEFAULT_THEME}”'); return DEFAULT_THEME
    if not os.path.isfile(os.path.join(ROOT, 'css', 'themes', name + '.css')) and name != DEFAULT_THEME:
        warn(f'theme.json: brak css/themes/{name}.css — używam „{DEFAULT_THEME}”'); return DEFAULT_THEME
    return name


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(__file__))
    from i18n import CATEGORIES
    g = load_gallery(); ps = load_json_posts(CATEGORIES); s = load_sponsor()
    vs = load_videos(); hm = load_home(); th = load_theme()
    print(f'galeria: spread {len(g["spread"])}, grid {len(g["grid"])}; wpisy z panelu: '
          + ', '.join(f'{l}:{len(v)}' for l, v in ps.items() if v) + f' ; sponsor: {"aktywny" if s else "brak"}'
          + f' ; filmiki z panelu: {len(vs)} ; opis głównej: {",".join(hm) or "domyślny"} ; wygląd: {th}')
    sys.exit(1 if PROBLEMS else 0)
