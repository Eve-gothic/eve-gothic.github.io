#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator strony Eve (wariant B „Gotycki luksus”) + Blog Eve, w 4 językach.

Uruchom z katalogu repo:   python3 scripts/build.py
Generuje: index.html, en|es|pt/index.html, blog/ (+ en|es|pt/blog/), wpisy, feed.xml,
obrazki OG (blog/og/<slug>.jpg itd.) i sitemap.xml. Wpisy: blog/posts/<lang>/RRRR-MM-DD-slug.md
Wymaga: Python 3.8+ i Pillow (tylko do obrazków OG).
"""
import os, re, sys, html, datetime, shutil
from email.utils import format_datetime
sys.path.insert(0, os.path.dirname(__file__))
from i18n import *

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# >>> JEDYNE miejsce z adresem strony (kanoniczny adres, hreflang, og:url, RSS, sitemap, przekierowanie z GH Pages).
#     Zmiana domeny = zmień SITE, uruchom build.py, commit + push (BLOG.md). Można też nadpisać: EVE_SITE=https://… python3 scripts/build.py
SITE = os.environ.get('EVE_SITE', 'https://eve-gothic.github.io').rstrip('/') + '/'
SITE_HOST = SITE.split('://', 1)[1].rstrip('/')
# Stare repo woDzu2207/eve-strona (wodzu2207.github.io/eve-strona/) zawiera już tylko strony-przekierowania na SITE.
CAFE = 'https://wodzu2207.github.io/eve-cafe/'
TAMA = 'https://wodzu2207.github.io/eve-game-public/'   # TYLKO wersja publiczna (dla wszystkich)
# Profile społecznościowe Eve (dla wszystkich) — NIE dodawać do bramki /18/
# Analityka GoatCounter (bez cookies, bez banera). Wpisz kod strony, np. 'eve-gothic' -> https://eve-gothic.goatcounter.com
# Puste = analityka wyłączona (żaden skrypt nie jest dodawany).
ANALYTICS_CODE = 'eve-ai'
def analytics():
    if not ANALYTICS_CODE: return ''
    return f'<script data-goatcounter="https://{ANALYTICS_CODE}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'

UTM = 'utm_source=instagram&utm_medium=bio&utm_campaign=linkinbio'
def utm(url):
    base, _, frag = url.partition('#')
    base += ('&' if '?' in base else '?') + UTM
    return base + ('#' + frag if frag else '')

FB = 'https://www.facebook.com/profile.php?id=61590647888748'
IG = 'https://www.instagram.com/eve.ai.digital.legacy/'
SVG_FB = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false"><path fill="currentColor" d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.68.24 2.68.24v2.97h-1.51c-1.49 0-1.96.93-1.96 1.89v2.25h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/></svg>'
SVG_IG = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16M12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63a5.86 5.86 0 0 0-2.13 1.38A5.86 5.86 0 0 0 .63 4.14C.33 4.9.13 5.78.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.3.79.72 1.46 1.38 2.13a5.86 5.86 0 0 0 2.13 1.38c.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56a5.86 5.86 0 0 0 2.13-1.38 5.86 5.86 0 0 0 1.38-2.13c.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91a5.86 5.86 0 0 0-1.38-2.13A5.86 5.86 0 0 0 19.86.63C19.1.33 18.22.13 16.95.07 15.67.01 15.26 0 12 0zm0 5.84a6.16 6.16 0 1 0 0 12.32 6.16 6.16 0 0 0 0-12.32zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.41-11.85a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88z"/></svg>'
def social(lang, cls=''):
    lbl = T[lang]['follow_btn']
    return (f'<div class="social {cls}"><span class="social-l">{lbl}</span>'
            f'<a class="sbtn" href="{FB}" target="_blank" rel="noopener" aria-label="{lbl} — Facebook">{SVG_FB}<span>Facebook</span></a>'
            f'<a class="sbtn" href="{IG}" target="_blank" rel="noopener" aria-label="{lbl} — Instagram">{SVG_IG}<span>Instagram</span></a></div>')
FONTS = 'family=Playfair+Display:ital@0;1&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@500'
ROMAN = ['I','II','III','IV','V','VI']
esc = lambda s: html.escape(str(s), quote=True)

def prefix(lang): return '' if lang == 'pl' else lang + '/'
def path_home(lang): return prefix(lang)
def path_blog(lang): return prefix(lang) + 'blog/'
KOMIKS_N = 31   # liczba stron komiksu (assets/komiks/eve-komiks-NN.webp)
KOMIKS_PDF = 'assets/komiks/eve-main-character.pdf'
def path_komiks(lang): return prefix(lang) + 'komiks/'
# link w bio: angielski jest główny pod /linki/ (adres do bio na Instagramie); /en/linki/ to kopia z canonical -> /linki/
def path_linki(lang): return {'en': 'linki/', 'pl': 'pl/linki/'}.get(lang, lang + '/linki/')
def path_post(lang, slug): return prefix(lang) + f'blog/{slug}/'
def root_for(path): return '../' * path.count('/')   # path = katalog strony względem korzenia

# ---------------- wpisy ----------------
def parse_post(fn, lang):
    raw = open(fn, encoding='utf-8').read().replace('\r\n', '\n')
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S)
    if not m: sys.exit(f'Brak front matter w {fn}')
    meta = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1); v = v.strip()
            if len(v) > 1 and v[0] == v[-1] and v[0] in '"\'': v = v[1:-1]
            meta[k.strip()] = v
    base = os.path.basename(fn)[:-3]
    mm = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)$', base)
    if not mm: sys.exit(f'Zła nazwa pliku {fn} (oczekiwano RRRR-MM-DD-slug.md)')
    for k in ('title', 'category', 'excerpt'):
        if not meta.get(k): sys.exit(f'Brak pola "{k}" w {fn}')
    if meta['category'] not in CATEGORIES: sys.exit(f'Nieznana kategoria "{meta["category"]}" w {fn}; dozwolone: {", ".join(CATEGORIES)}')
    d = datetime.date.fromisoformat(meta.get('date') or mm.group(1))
    cover = meta.get('cover', '').strip()
    if cover and not os.path.exists(os.path.join(ROOT, 'assets/img', cover + '.webp')):
        sys.exit(f'cover "{cover}" nie istnieje w assets/img/ ({fn})')
    return dict(lang=lang, slug=mm.group(2), date=d, title=meta['title'], category=meta['category'],
                excerpt=meta['excerpt'], cover=cover, og_photo=meta.get('og_photo', '').strip() or cover or 'eve-biblioteka',
                draft=meta.get('draft', '').lower() in ('true', 'yes', '1'), body=m.group(2), file=fn)

def inline(t):
    t = esc(t).replace('&#x27;', "'")
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', r'<img src="\2" alt="\1" loading="lazy">', t)
    def link(m):
        u = m.group(2); ext = u.startswith('http')
        return f'<a href="{u}"' + (' target="_blank" rel="noopener"' if ext else '') + f'>{m.group(1)}</a>'
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    return t

def markdown(md, lang):
    out, para, lst, quote = [], [], None, []
    def flush():
        nonlocal para, lst, quote
        if para: out.append('<p>' + inline(' '.join(para)) + '</p>'); para = []
        if lst: out.append(f'<{lst[0]}>' + ''.join(f'<li>{inline(i)}</li>' for i in lst[1]) + f'</{lst[0]}>'); lst = None
        if quote: out.append('<blockquote><p>' + inline(' '.join(quote)) + '</p></blockquote>'); quote = []
    for line in md.split('\n'):
        s = line.rstrip()
        if not s.strip(): flush(); continue
        h = re.match(r'^(#{2,4})\s+(.*)$', s)
        ul = re.match(r'^\s*[-*]\s+(.*)$', s); ol = re.match(r'^\s*\d+\.\s+(.*)$', s)
        if h:
            flush(); n = len(h.group(1)); txt = h.group(2).strip()
            cls = ' class="src"' if n == 2 and txt.lower() == T[lang]['sources'].lower() else ''
            out.append(f'<h{n}{cls}>{inline(txt)}</h{n}>')
        elif ul or ol:
            kind = 'ul' if ul else 'ol'
            if para or quote: flush()
            if not lst or lst[0] != kind: flush(); lst = (kind, [])
            lst[1].append((ul or ol).group(1))
        elif s.startswith('>'):
            if para or lst: flush()
            quote.append(s.lstrip('>').strip())
        elif re.match(r'^(-{3,}|\*{3,})$', s.strip()): flush(); out.append('<hr>')
        else:
            if lst or quote: flush()
            para.append(s.strip())
    flush()
    return '\n'.join(out)

def load_posts():
    posts = {l: [] for l in LANGS}
    for l in LANGS:
        d = os.path.join(ROOT, 'blog/posts', l)
        if not os.path.isdir(d): continue
        for f in sorted(os.listdir(d)):
            if f.endswith('.md'):
                p = parse_post(os.path.join(d, f), l)
                if not p['draft']: posts[l].append(p)
        posts[l].sort(key=lambda p: (p['date'], p['slug']), reverse=True)
    slugs = {l: {p['slug'] for p in posts[l]} for l in LANGS}
    for s in slugs['pl']:
        miss = [l for l in LANGS if s not in slugs[l]]
        if miss: print(f'UWAGA: wpis "{s}" nie ma wersji: {", ".join(miss)}')
    return posts, slugs

# ---------------- obrazki OG ----------------
def og_image(out, photo, kicker, title, foot=None):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    foot = foot or SITE_HOST
    F = os.path.join(ROOT, 'scripts/fonts')
    def font(name, size, var=None):
        f = ImageFont.truetype(os.path.join(F, name), size)
        if var:
            try: f.set_variation_by_name(var)
            except Exception: pass
        return f
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), '#0c0708')
    # tło: gradient bordo -> czerń
    g = Image.new('RGB', (W, H)); gd = ImageDraw.Draw(g)
    for x in range(W):
        t = x / W; c = tuple(int(a + (b - a) * t) for a, b in zip((0x3a, 0x0b, 0x16), (0x0c, 0x07, 0x08)))
        gd.line([(x, 0), (x, H)], fill=c)
    im.paste(g)
    # zdjęcie po lewej
    ph = Image.open(os.path.join(ROOT, photo) if '/' in photo else os.path.join(ROOT, 'assets/img', photo + '.webp')).convert('RGB')
    pw = 470; sc = max(pw / ph.width, H / ph.height)
    ph = ph.resize((round(ph.width * sc), round(ph.height * sc)), Image.LANCZOS)
    top = int((ph.height - H) * (0 if '/' in photo else 0.25)); left = (ph.width - pw) // 2
    im.paste(ph.crop((left, top, left + pw, top + H)), (0, 0))
    d = ImageDraw.Draw(im)
    gold, gold2, paper, mut = '#c9a35b', '#e8cf96', '#f3ece0', '#b9a89a'
    d.line([(pw, 0), (pw, H)], fill=gold, width=3)
    d.rectangle([pw + 26, 26, W - 26, H - 26], outline=(201, 163, 91), width=1)
    x0, x1 = pw + 70, W - 70
    # kicker (rozstrzelone kapitaliki)
    fk = font('Inter[opsz,wght].ttf', 19, 'Medium'); xx = x0
    for ch in kicker.upper():
        d.text((xx, 72), ch, font=fk, fill=gold); xx += d.textlength(ch, font=fk) + 4.5
    d.line([(x0, 112), (x0 + 60, 112)], fill=gold, width=2)
    # tytuł — dopasuj rozmiar
    for size in range(66, 30, -2):
        ft = font('PlayfairDisplay-Italic[wght].ttf', size, 'Italic')
        words, lines, cur = title.split(), [], ''
        for w in words:
            test = (cur + ' ' + w).strip()
            if d.textlength(test, font=ft) <= x1 - x0: cur = test
            else: lines.append(cur); cur = w
        lines.append(cur)
        lh = int(size * 1.18)
        if len(lines) * lh <= 320: break
    y = 136 + (320 - len(lines) * lh) // 2
    for ln in lines:
        d.text((x0, y), ln, font=ft, fill=paper); y += lh
    # stopka: Eve. + adres
    fm = font('PlayfairDisplay-Italic[wght].ttf', 54, 'Italic')
    d.text((x0, H - 128), 'Eve', font=fm, fill=paper)
    d.text((x0 + d.textlength('Eve', font=fm), H - 128), '.', font=fm, fill=gold)
    fu = font('Inter[opsz,wght].ttf', 17, 'Medium')
    d.text((x1 - d.textlength(foot, font=fu), H - 92), foot, font=fu, fill=mut)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, 'JPEG', quality=86, optimize=True, progressive=True)

def og_name(slug, lang): return f'blog/og/{slug}.jpg' if lang == 'pl' else f'blog/og/{slug}-{lang}.jpg'

# ---------------- szablon ----------------
def head(lang, path, title, desc, alts, og_img, og_type='website', extra='', gate=False):
    r = root_for(path)
    if gate: return head_gate(lang, path, title, desc, alts)
    links = ''.join(f'<link rel="alternate" hreflang="{HTML_LANG[l]}" href="{SITE}{p}">' for l, p in alts.items())
    if 'pl' in alts: links += f'<link rel="alternate" hreflang="x-default" href="{SITE}{alts["pl"]}">'
    return f'''<!doctype html>
<html lang="{HTML_LANG[lang]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#3a0b16">
<link rel="canonical" href="{SITE}{path}">{links}
<link rel="alternate" type="application/rss+xml" title="{esc(T[lang]['blog_h'])}" href="{SITE}{path_blog(lang)}feed.xml">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Eve"><meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">{extra}
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🖤</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FONTS}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}css/eve.css"></head>
<body>'''

def topbar(lang, path, alts, solid=False):
    t, r = T[lang], root_for(path)
    home = r + path_home(lang); on_home = path == path_home(lang)
    h = (lambda a: '#' + a) if on_home else (lambda a: home + '#' + a)
    nav = ''.join(f'<a href="{h(a)}">{n}</a>' for a, n in zip(['o-eve', 'galeria', 'filmiki', 'gry'], t['nav'][:4]))
    nav += f'<a href="{r}{path_komiks(lang)}">{t["nav_komiks"]}</a>'
    nav += f'<a href="{r}{path_blog(lang)}">{t["nav"][4]}</a>'
    langs = ''.join(f'<a href="{(r + alts.get(l, path_home(l))) or "./"}" hreflang="{HTML_LANG[l]}" lang="{HTML_LANG[l]}" title="{LANG_NAME[l]}"' + (' aria-current="true"' if l == lang else '') + f'>{LANG_LABEL[l]}</a>' for l in LANGS)
    return f'''<header class="top{' solid' if solid else ''}"><a class="mast" href="{'#top' if on_home else home}">Eve.</a>
<div class="right"><nav class="langs" aria-label="{t['langs_label']}">{langs}</nav><button class="burger" data-burger aria-label="{t['menu']}" aria-expanded="false">☰</button></div>
<nav class="menu" data-menu>{nav}</nav></header>'''

def path_gate(lang): return prefix(lang) + '18/'

def head_gate(lang, path, title, desc, alts):
    r = root_for(path)
    links = ''.join(f'<link rel="alternate" hreflang="{HTML_LANG[l]}" href="{SITE}{p}">' for l, p in alts.items())
    return f'''<!doctype html>
<html lang="{HTML_LANG[lang]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#3a0b16">
<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer">{links}
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🖤</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FONTS}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}css/eve.css"></head>
<body>'''

# Zewnętrzny link 18+ — TYLKO na stronach bramki, wstawiany przez JS po potwierdzeniu.
GATE_URL = ''  # usunięte 5.11.2026 — żadnych linków 18+

def gate_page(lang):
    t, g = T[lang], GATE[lang]; path = path_gate(lang); r = root_for(path)
    alts = {l: path_gate(l) for l in LANGS}
    home = r + path_home(lang)
    langs = ''.join(f'<a href="{r}{alts[l]}" hreflang="{HTML_LANG[l]}" lang="{HTML_LANG[l]}" title="{LANG_NAME[l]}"' + (' aria-current="true"' if l == lang else '') + f'>{LANG_LABEL[l]}</a>' for l in LANGS)
    import json
    return head(lang, path, g['title'], g['warn'], alts, None, gate=True) + f'''
<header class="top solid"><a class="mast" href="{home}">Eve.</a><div class="right"><nav class="langs" aria-label="{t['langs_label']}">{langs}</nav></div></header>
<main class="wrap"><section class="gate">
 <span class="sc">18+</span>
 <h1>{g['h']}<span>.</span></h1>
 <p class="warn">{g['warn']}</p>
 <div class="gate-btns"><button class="cta fill" type="button" id="gate-yes">{g['yes']}</button><a class="cta" id="gate-back" href="{home}">{g['back']}</a></div>
 <div id="gate-out" hidden><p class="small">{g['note']}</p></div>
</section></main>
<footer><div><span class="mast">Eve.</span><br>© <span id="y">2026</span> Daniel Wodziński · Multiwersum Eve</div><div style="max-width:52ch">{t['foot']}</div></footer>
<script>
(()=>{{const U={json.dumps(GATE_URL)},L={json.dumps(g['open'], ensure_ascii=False)};
document.getElementById('y').textContent=new Date().getFullYear();
document.getElementById('gate-back').addEventListener('click',e=>{{try{{if(document.referrer&&new URL(document.referrer).origin===location.origin&&history.length>1){{e.preventDefault();history.back()}}}}catch(_){{}}}});
document.getElementById('gate-yes').addEventListener('click',()=>{{const box=document.getElementById('gate-out');
 if(!box.querySelector('a')){{const a=document.createElement('a');a.href=U;a.rel='nofollow noopener noreferrer';a.target='_blank';a.className='cta fill';a.textContent=L;box.prepend(a)}}
 box.hidden=false;window.open(U,'_blank','noopener,noreferrer')}});}})();
</script></body></html>'''

def footer(lang, path, blog=False):
    t, r = T[lang], root_for(path)
    note = f'<br><strong>{t["ai_note"]}</strong>' if blog else ''
    return f'''<footer><div><span class="mast">Eve.</span><br>© <span id="y">2026</span> Daniel Wodziński · Multiwersum Eve</div>
{social(lang, 'foot')}<div style="max-width:52ch">{t['foot']}{note}<br><a href="{r}{path_blog(lang)}feed.xml">{t['rss']}</a> · <a href="{r}warianty/">{t['variants']}</a></div></footer>
<script src="{r}js/eve.js"></script>{analytics()}</body></html>'''

SLOT = '<div class="slot" aria-hidden="true"></div>'   # miejsce na przyszłe reklamy (bez kodu reklam)

def card(p, r, big=False):
    t = T[p['lang']]; url = r + path_post(p['lang'], p['slug'])
    ph = f'<div class="ph"><img loading="lazy" src="{r}assets/img/{p["cover"]}.webp" alt=""></div>' if p['cover'] else ''
    return f'''<a class="pcard{' big' if big else ''}" href="{url}">{ph}<div><span class="sc">{CATEGORIES[p['category']][p['lang']]} · {fmt_date(p['date'], p['lang'])}</span>
<h3>{esc(p['title'])}</h3><p>{esc(p['excerpt'])}</p><span class="more">{t['read_more']} →</span></div></a>'''

def cards(ps, r, lang='pl'):
    if not ps: return f'<p class="small">{T[lang]["no_posts"]}</p>'
    if len(ps) == 1: return f'<div class="cards">{card(ps[0], r, True)}</div>'
    return '<div class="cards">' + ''.join(card(p, r) for p in ps) + '</div>'

def home(lang, posts):
    t = T[lang]; path = path_home(lang); r = root_for(path); A = r + 'assets/'
    alts = {l: path_home(l) for l in LANGS}
    img = lambda n, full=False: f'{A}img/eve-{n}{"" if full else "-thumb"}.webp'
    out = head(lang, path, t['title'], t['desc'], alts, f'og/home-{lang}.jpg')
    figs = ''
    for k, (n, cap) in enumerate(zip(GALLERY, GAL_CAP[lang]), 1):
        figs += f'<figure class="s{k}"><button data-full="{img(n, True)}" data-cap="{esc(cap)}" aria-label="{t["zoom"]}: {esc(cap)}"><img loading="lazy" src="{img(n, True) if k in (1, 4, 11, 12) else img(n)}" alt="Eve — {esc(cap)}"></button><figcaption data-n="{k:02d}">{esc(cap)}</figcaption></figure>\n'
    vid = lambda n: f'<video muted playsinline controls loop preload="none" data-hover poster="{A}video/{n}-poster.webp"><source src="{A}video/{n}.webm" type="video/webm"><source src="{A}video/{n}.mp4" type="video/mp4">{t["novideo"]}</video>'
    figs2 = ''
    for n, cap, alt in zip(GALLERY2, GAL2_CAP[lang], GAL2_ALT[lang]):
        figs2 += f'<figure><button data-full="{img(n, True)}" data-cap="{esc(cap)}" aria-label="{t["zoom"]}: {esc(cap)}"><img loading="lazy" src="{img(n)}" alt="{esc(alt)}" width="450" height="600"></button><figcaption>{esc(cap)}</figcaption></figure>\n'
    reel = ''.join(f'<article>{vid(n)}<h3>{vt}</h3><span class="sc">{t["frame"]} {i + 1:02d}</span></article>' for i, (n, vt) in enumerate(zip(VIDEOS, t['video_titles'])))
    traits = ''.join(f'<li>{x}</li>' for x in t['traits'])
    newtab = lambda u: f'<a class="cta fill" href="{u}" target="_blank" rel="noopener">{t["newtab"]}</a>'
    cafe, tama = f'{CAFE}?lang={lang}', f'{TAMA}?lang={lang}'   # gry obsługują ?lang=pl|en|es|pt
    gbar = lambda u: f'<p class="small gnote">{t["notshowing"]}</p><div class="gbar">{newtab(u)}<button class="cta" type="button" data-fs>{t["fs"]}</button></div>'
    blog = cards(posts[lang][:3], r, lang)
    out += topbar(lang, path, alts) + f'''
<main id="top">
<section class="cover">
 <div class="cover-img"><img src="{img('londyn', True)}" alt="{t['cover_alt']}" fetchpriority="high"></div>
 <div class="cover-txt"><span class="sc">{t['kicker']}</span>
  <h1>Eve<span>.</span></h1>
  <p class="deck">{t['deck']}</p>
  <a class="cta fill" href="#galeria">{t['cta_play']}</a> <a class="cta" href="{r}{path_blog(lang)}">{t['cta_gallery']}</a>
  {social(lang, 'hero')}</div>
 <div class="issue"><span class="sc">{t['issue']}</span><b>Nº 01</b><span class="sc">{t['season']}</span></div>
</section>
{SLOT}
<div class="wrap">
<section id="o-eve" class="sec">
 <div class="head"><span class="no">I</span><h2>{t['about_h']}</h2></div>
 <div class="about">
  <div class="ph"><img loading="lazy" src="{img('biblioteka', True)}" alt="{t['about_alt']}"></div>
  <div><p class="lede">{t['about']}</p>
   <p class="quote">{t['quote']}</p>
   <ul class="traits">{traits}</ul>
   <p class="follow">{t['follow']} <a href="{r}{path_blog(lang)}">{t['blog_h']} →</a> · <a href="{r}{path_blog(lang)}feed.xml">RSS</a></p>
   {social(lang)}</div>
 </div></section>
<section id="galeria" class="sec" style="padding-top:0">
 <div class="head"><span class="no">II</span><h2>{t['gal_h']}</h2></div>
 <div class="spread">{figs}</div>
 <div class="sub"><h3>{t['gal2_h']}</h3><p class="small">{t['gal2_lead']}</p></div>
 <div class="grid2">{figs2}</div></section>
</div>
<section id="filmiki" class="film"><div class="wrap">
 <div class="head"><span class="no">III</span><h2>{t['videos_h']}</h2></div>
 <div class="reel">{reel}</div>
 <p class="small" style="margin-top:28px">{t['video_hint']}</p></div></section>
{SLOT}
<div class="wrap">
<section id="gry" class="sec">
 <div class="head"><span class="no">IV</span><h2>{t['games_h']}</h2></div>
 <p class="small" style="margin:-30px 0 40px;max-width:60ch">{t['games_lead']}</p>
 <div class="games">
  <article class="game" id="eve-cafe"><span class="sc">{t['available']}</span><h3>Eve's Café</h3><p>{t['cafe_desc']}</p>
   <!-- Gra pionowa (Phaser, 720 px szer., Scale.FIT): okno 9:16 -->
   <div class="embed tall" data-embed="{cafe}" data-title="Eve's Café"><img src="{img('barista')}" alt="" class="embed-bg"><button class="cta" data-play>{t['run']}</button></div>
   {gbar(cafe)}</article>
  <article class="game" id="eve-tamagotchi"><span class="sc">{t['available']}</span><h3>{t['tama_title']}</h3><p>{t['tama_desc']}</p>
   <div class="embed tall" data-embed="{tama}" data-title="{t['tama_title']}"><img src="{img('gracz')}" alt="" class="embed-bg"><button class="cta" data-play>{t['run']}</button></div>
   {gbar(tama)}</article>
 </div></section>
<section id="komiks" class="sec ktease">
 <div class="head"><span class="no">V</span><h2>{t['komiks_h']}</h2></div>
 <a class="kcard" href="{r}{path_komiks(lang)}"><div class="ph"><img loading="lazy" src="{r}assets/komiks/eve-komiks-okladka.webp" alt="{esc(t['komiks_alt'])} 1" width="1120" height="1682"></div>
 <div><span class="sc">{t['komiks_kicker']} · {KOMIKS_N} {t['komiks_pages']}</span><h3>Main Character</h3><p>{t['komiks_lead']} {t['komiks_note']}</p><span class="cta fill">{t['komiks_read']} →</span></div></a></section>
<section id="blog" class="sec blogsec">
 <div class="head"><span class="no">VI</span><h2>{t['blog_h']}</h2></div>
 <p class="small" style="margin:-10px 0 34px;max-width:60ch">{t['blog_lead']}</p>
 <!-- BLOG: generowane przez scripts/build.py (3 najnowsze wpisy) -->
 {blog}
 <p style="margin-top:34px"><a class="cta" href="{r}{path_blog(lang)}">{t['all_posts']} →</a></p></section>
</div>
{SLOT}
</main>
''' + footer(lang, path)
    return out

def blog_index(lang, posts):
    t = T[lang]; path = path_blog(lang); r = root_for(path)
    alts = {l: path_blog(l) for l in LANGS}
    ps = posts[lang]
    out = head(lang, path, t['blog_title'], t['blog_lead'], alts, og_name(ps[0]['slug'], lang) if ps else f'og/home-{lang}.jpg')
    out += topbar(lang, path, alts, solid=True) + f'''
<main class="wrap">
<section class="bloghead"><span class="sc">{t['kicker'].split('·')[0].strip()} · Nº 01</span>
<h1>{t['blog_h'].replace('Eve', 'Eve<span>.</span>', 1) if t['blog_h'].endswith('Eve') else t['blog_h']}</h1><p>{t['blog_lead']}</p>
<p style="margin-top:18px"><a class="rss" href="feed.xml">{t['rss']} ↗</a></p></section>
{SLOT}
<section class="blogsec sec" style="padding-top:0">{cards(ps, r, lang)}</section>
{SLOT}
<p style="margin:0 0 60px"><a class="cta" href="{r}{path_home(lang)}">{t['back_home']}</a></p>
</main>
''' + footer(lang, path, blog=True)
    return out

def post_page(p, slugs):
    lang = p['lang']; t = T[lang]; path = path_post(lang, p['slug']); r = root_for(path)
    alts = {l: path_post(l, p['slug']) for l in LANGS if p['slug'] in slugs[l]}
    extra = f'<meta property="article:published_time" content="{p["date"].isoformat()}"><meta property="article:section" content="{CATEGORIES[p["category"]][lang]}">'
    extra += f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BlogPosting","headline":{json_str(p['title'])},"datePublished":"{p['date'].isoformat()}","inLanguage":"{HTML_LANG[lang]}","image":"{SITE}{og_name(p['slug'], lang)}","author":{{"@type":"Person","name":"Eve (AI)","sameAs":["{FB}","{IG}"]}},"description":{json_str(p['excerpt'])}}}</script>'''
    out = head(lang, path, f"{p['title']} — {t['blog_h']}", p['excerpt'], alts, og_name(p['slug'], lang), 'article', extra)
    cover = f'<figure class="pcover"><img src="{r}assets/img/{p["cover"]}.webp" alt="Eve"></figure>' if p['cover'] else ''
    out += topbar(lang, path, alts, solid=True) + f'''
<main class="wrap">
<article class="post">
 <div class="meta"><a class="sc" href="{r}{path_blog(lang)}">{t['blog_h']}</a><span class="sc">{CATEGORIES[p['category']][lang]}</span><span class="sc"><time datetime="{p['date'].isoformat()}">{fmt_date(p['date'], lang)}</time></span></div>
 <h1>{esc(p['title'])}</h1>
 <p class="deck">{esc(p['excerpt'])}</p>
 {cover}
 <div class="body">
{markdown(p['body'], lang)}
 </div>
 <p class="ainote">{t['ai_note']}</p>
 <div class="postnav"><a class="cta" href="{r}{path_blog(lang)}">{t['back_blog']}</a><a class="cta" href="{r}{path_home(lang)}">{t['back_home']}</a></div>
</article>
{SLOT}
</main>
''' + footer(lang, path, blog=True)
    return out

def komiks_page(lang):
    t = T[lang]; path = path_komiks(lang); r = root_for(path)
    alts = {l: path_komiks(l) for l in LANGS}
    og = f'og/komiks-{lang}.jpg'
    extra = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ComicStory","name":"Main Character","inLanguage":"en","url":"{SITE}{path}","image":"{SITE}{og}","description":{json_str(t['komiks_desc'])},"author":{{"@type":"Person","name":"Eve (AI)","sameAs":["{FB}","{IG}"]}}}}</script>'''
    out = head(lang, path, f"{t['komiks_title']} — Eve", t['komiks_desc'], alts, og, 'website', extra)
    pages = ''
    for n in range(1, KOMIKS_N + 1):
        src = f'{r}assets/komiks/eve-komiks-{n:02d}.webp'; cap = f"Main Character — {t['komiks_page']} {n} / {KOMIKS_N}"
        pages += f'<figure class="kpage" id="s{n}"><button data-full="{src}" data-cap="{esc(cap)}" aria-label="{t["zoom"]}: {esc(cap)}"><img src="{src}" alt="{esc(t["komiks_alt"])} {n}" width="1190" height="1682"' + (' fetchpriority="high"' if n == 1 else ' loading="lazy" decoding="async"') + f'></button><figcaption>{t["komiks_page"]} {n} / {KOMIKS_N}</figcaption></figure>\n'
    pdf_mb = os.path.getsize(os.path.join(ROOT, KOMIKS_PDF)) / 1e6
    size = f'{pdf_mb:.1f} MB' if lang == 'en' else f'{pdf_mb:.1f} MB'.replace('.', ',')
    pdf = f'<a class="cta" href="{r}{KOMIKS_PDF}" download>{t["komiks_pdf"]} ({size})</a>'
    note = f' <em>{t["komiks_note"]}</em>' if t['komiks_note'] else ''
    out += topbar(lang, path, alts, solid=True) + f'''
<main class="wrap">
<section class="bloghead khead"><span class="sc">{t['komiks_kicker']} · {KOMIKS_N} {t['komiks_pages']}</span>
<h1>Main Character<span>.</span></h1><p>{t['komiks_lead']}{note}</p>
<p style="margin-top:18px"><a class="cta fill" href="#s1">{t['komiks_read']} ↓</a> {pdf}</p>
{social(lang)}</section>
{SLOT}
<section class="reader">{pages}</section>
<p class="small" style="text-align:center;font-style:italic">{t['komiks_next']}</p>
<div class="postnav" style="margin-bottom:60px">{pdf}<a class="cta" href="{r}{path_home(lang)}">{t['back_home']}</a></div>
{social(lang)}
<div style="height:50px"></div>
</main>
''' + footer(lang, path)
    return out

def linki_page(lang, posts, path=None):
    L, t = LINKI[lang], T[lang]
    path = path or path_linki(lang); r = root_for(path); canon = path_linki(lang)
    alts = {l: path_linki(l) for l in LANGS}
    hre = ''.join(f'<link rel="alternate" hreflang="{HTML_LANG[l]}" href="{SITE}{p}">' for l, p in alts.items()) + f'<link rel="alternate" hreflang="x-default" href="{SITE}{alts["en"]}">'
    og = f'og/linki-{lang}.jpg'
    p = posts[lang][0] if posts[lang] else None
    def btn(href, label, sub='', icon='', ext=False, cls='', ev=''):
        tgt = ' target="_blank" rel="noopener"' if ext else ''
        sub = f'<small>{esc(sub)}</small>' if sub else ''
        return f'<a class="lbtn{cls}" href="{esc(href)}"{tgt} data-goatcounter-click="bio-{ev}"><span class="li">{icon}</span><span class="lt">{esc(label)}{sub}</span><span class="la" aria-hidden="true">→</span></a>\n'
    links = ''
    if p:
        cv = p['cover'] and (p['cover'] + '-thumb' if os.path.exists(os.path.join(ROOT, f'assets/img/{p["cover"]}-thumb.webp')) else p['cover'])
        ph = f'<img src="{r}assets/img/{cv}.webp" alt="" width="56" height="56" loading="lazy">' if cv else '✦'
        links += btn(utm(r + path_post(lang, p['slug'])), p['title'], L['latest'], ph, cls=' feat', ev='latest-post')
    links += btn(utm(r + path_komiks(lang)), L['comic'], L['comic_sub'], '✎', ev='komiks')
    links += btn(utm(f'{CAFE}?lang={lang}'), L['cafe'], L['cafe_sub'], '☕', ev='cafe')
    links += btn(utm(f'{TAMA}?lang={lang}'), L['tama'], L['tama_sub'], '♡', ev='tamagotchi')
    links += btn(utm(r + path_home(lang) + '#galeria'), L['gallery'], L['gallery_sub'], '◐', ev='galeria')
    links += btn(utm(r + path_blog(lang)), L['blog'], L['blog_sub'], '✦', ev='blog')
    links += btn(FB, L['fb'], t['follow_btn'] if 'follow_btn' in t else '', SVG_FB, True, ' soc', 'facebook')
    links += btn(IG, L['ig'], '@eve.ai.digital.legacy', SVG_IG, True, ' soc', 'instagram')
    langs = ''.join(f'<a href="{r}{path_linki(l)}" hreflang="{HTML_LANG[l]}" lang="{HTML_LANG[l]}"' + (' aria-current="true"' if l == lang else '') + f'>{LANG_LABEL[l]}</a>' for l in ['en', 'pl', 'es', 'pt'])
    return f'''<!doctype html>
<html lang="{HTML_LANG[lang]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(L['title'])}</title><meta name="description" content="{esc(L['desc'])}"><meta name="theme-color" content="#0c0708">
<meta name="robots" content="index, follow"><link rel="canonical" href="{SITE}{canon}">{hre}
<meta property="og:type" content="profile"><meta property="og:site_name" content="Eve"><meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta property="og:title" content="{esc(L['title'])}"><meta property="og:description" content="{esc(L['desc'])}"><meta property="og:url" content="{SITE}{canon}">
<meta property="og:image" content="{SITE}{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(L['title'])}"><meta name="twitter:description" content="{esc(L['desc'])}"><meta name="twitter:image" content="{SITE}{og}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ProfilePage","url":"{SITE}{canon}","inLanguage":"{HTML_LANG[lang]}","mainEntity":{{"@type":"Person","name":"Eve (AI)","description":{json_str(L['bio'])},"image":"{SITE}assets/img/eve-avatar.webp","sameAs":["{FB}","{IG}"]}}}}</script>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🖤</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FONTS}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}css/eve.css"></head>
<body class="linki">
<main class="lbio">
<nav class="llangs" aria-label="{esc(L['langs'])}">{langs}</nav>
<header class="lhead">
<img class="lav" src="{r}assets/img/eve-avatar.webp" alt="Eve — {esc(L['ai'])}" width="240" height="240" fetchpriority="high">
<span class="sc">{esc(L['kicker'])}</span>
<h1>Eve<span>.</span></h1>
<p class="lbiot">{esc(L['bio'])}</p>
<span class="aitag">✦ {esc(L['ai'])}</span>
</header>
<nav class="llist">
{links}</nav>
<footer class="lfoot"><a href="{esc(utm(r + path_home(lang)))}">{esc(L['site'])} · {SITE_HOST}</a><br><small>{esc(t['ai_note'])}</small></footer>
</main>{analytics()}
</body></html>'''

def json_str(s):
    import json; return json.dumps(s, ensure_ascii=False)

def feed(lang, posts):
    t = T[lang]; items = ''
    for p in posts[lang][:30]:
        u = SITE + path_post(lang, p['slug'])
        dt = datetime.datetime.combine(p['date'], datetime.time(9, 0), datetime.timezone.utc)
        items += f'''<item><title>{esc(p['title'])}</title><link>{u}</link><guid isPermaLink="true">{u}</guid><pubDate>{format_datetime(dt)}</pubDate><category>{esc(CATEGORIES[p['category']][lang])}</category><description>{esc(p['excerpt'])}</description><enclosure url="{SITE}{og_name(p['slug'], lang)}" type="image/jpeg" length="{os.path.getsize(os.path.join(ROOT, og_name(p['slug'], lang)))}"/></item>\n'''
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>
<title>{esc(t['blog_title'])}</title><link>{SITE}{path_blog(lang)}</link><description>{esc(t['blog_lead'] + ' ' + t['ai_note'])}</description>
<language>{HTML_LANG[lang]}</language><atom:link href="{SITE}{path_blog(lang)}feed.xml" rel="self" type="application/rss+xml"/>
{items}</channel></rss>
'''

def write(rel, content):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    open(p, 'w', encoding='utf-8').write(content)

def main():
    posts, slugs = load_posts()
    # usuń wygenerowane strony wpisów, których już nie ma (bez ruszania blog/posts i blog/og)
    for l in LANGS:
        bd = os.path.join(ROOT, path_blog(l))
        if os.path.isdir(bd):
            for e in os.listdir(bd):
                full = os.path.join(bd, e)
                if os.path.isdir(full) and e not in ('posts', 'og') and e not in slugs[l] and os.path.exists(os.path.join(full, 'index.html')):
                    shutil.rmtree(full); print('usunięto', full)
    for l in LANGS:
        og_image(os.path.join(ROOT, f'og/home-{l}.jpg'), 'eve-londyn', T[l]['kicker'], T[l]['title'])
        for p in posts[l]:
            og_image(os.path.join(ROOT, og_name(p['slug'], l)), p['og_photo'],
                     f"{T[l]['blog_h']} · {CATEGORIES[p['category']][l]}", p['title'])
        write(path_home(l) + 'index.html', home(l, posts))
        write(path_blog(l) + 'index.html', blog_index(l, posts))
        og_image(os.path.join(ROOT, f'og/komiks-{l}.jpg'), 'assets/komiks/eve-komiks-okladka.webp', T[l]['komiks_kicker'], T[l]['komiks_title'])
        write(path_komiks(l) + 'index.html', komiks_page(l))
        og_image(os.path.join(ROOT, f'og/linki-{l}.jpg'), 'assets/img/eve-spojrzenie-noir.webp', LINKI[l]['kicker'], LINKI[l]['bio'].split(' · ')[0])
        write(path_linki(l) + 'index.html', linki_page(l, posts))
        write(path_blog(l) + 'feed.xml', feed(l, posts))
        for p in posts[l]:
            write(path_post(l, p['slug']) + 'index.html', post_page(p, slugs))
        pass  # bramka 18+ usunięta na prośbę Daniela (5.11.2026)   # bramka 18+ — celowo NIE w sitemap.xml
    write('en/linki/index.html', linki_page('en', posts, 'en/linki/'))   # kopia EN (canonical -> /linki/)
    urls = [path_home(l) for l in LANGS] + [path_linki(l) for l in ['en', 'pl', 'es', 'pt']] + [path_komiks(l) for l in LANGS] + [path_blog(l) for l in LANGS] + [path_post(l, p['slug']) for l in LANGS for p in posts[l]]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{SITE}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    print(f'OK: {sum(len(v) for v in posts.values())} wpisów ({", ".join(f"{l}:{len(posts[l])}" for l in LANGS)}), {len(urls)} stron.')

if __name__ == '__main__':
    main()
