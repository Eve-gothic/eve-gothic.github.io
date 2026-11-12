#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator strony Eve (wariant B „Gotycki luksus”) + Blog Eve, w 7 językach (pl, en, es, pt, it, ja, zh).

Uruchom z katalogu repo:   python3 scripts/build.py
Generuje: index.html, en|es|pt|it|ja|zh/index.html, blog/ (+ <lang>/blog/), wpisy, feed.xml,
obrazki OG (blog/og/<slug>.jpg itd.) i sitemap.xml. Wpisy: blog/posts/<lang>/RRRR-MM-DD-slug.md
Wymaga: Python 3.8+ i Pillow (tylko do obrazków OG), a dla ja/zh systemowych fontów Noto CJK
(apt install fonts-noto-cjk) — obrazki OG z japońskim/chińskim tekstem.
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
BRAWLER = 'https://wodzu2207.github.io/eve-brawler/'   # „Eve vs The Suits” (satyra, ?lang=pl|en — brawler_lang())
PENALTY = 'https://wodzu2207.github.io/eve-penalty/'   # „Eve: Królowa Karnych” / Penalty Queen (?lang=pl|en|es|pt|it|ja|zh — penalty_lang())
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
# Blok „Obserwuj Eve” na końcu wpisów, komiksów i sesji — część szablonu (nowe wpisy/sesje dostają go automatycznie).
# kind = rodzaj strony (post|komiks|komiks2|sesja) -> utm_campaign i nazwa zdarzenia GoatCounter: follow-<kind>-instagram|facebook
def follow_block(lang, kind):
    t = T[lang]
    u = lambda url: esc(url + ('&' if '?' in url else '?') + f'utm_source=site&utm_medium=follow_block&utm_campaign={kind}')
    btn = lambda url, svg, name, ev: (f'<a class="fbtn" href="{u(url)}" target="_blank" rel="noopener" data-goatcounter-click="follow-{kind}-{ev}" '
                                      f'data-goatcounter-title="{name} — follow block ({kind}, {lang})" aria-label="{esc(t["follow_btn"])} — {name}">{svg}<span>{name}</span></a>')
    return (f'<aside class="fblock" aria-label="{esc(t["follow_btn"])}"><span class="sc">{t["follow_btn"]}</span>'
            f'<p class="fline">{t["follow_line"]}</p><div class="fbtns">'
            + btn(IG, SVG_IG, 'Instagram', 'instagram') + btn(FB, SVG_FB, 'Facebook', 'facebook')
            + '</div></aside>')

FONTS = 'family=Playfair+Display:ital@0;1&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@500'
# ja/zh: dodatkowo szeryfowy font CJK (Google Fonts dzieli go na małe pakiety unicode-range, więc pobiera się tylko to, co potrzebne)
FONTS_CJK = {'ja': '&family=Noto+Serif+JP:wght@400;600', 'zh': '&family=Noto+Serif+SC:wght@400;600'}
def fonts(lang): return FONTS + FONTS_CJK.get(lang, '')
ROMAN = ['I','II','III','IV','V','VI']
esc = lambda s: html.escape(str(s), quote=True)

def prefix(lang): return '' if lang == 'pl' else lang + '/'
def path_home(lang): return prefix(lang)
def path_blog(lang): return prefix(lang) + 'blog/'
KOMIKS_N = 31   # liczba stron komiksu (assets/komiks/eve-komiks-NN.webp)
KOMIKS_PDF = 'assets/komiks/eve-main-character.pdf'
def path_komiks(lang): return prefix(lang) + 'komiks/'
# link w bio: angielski jest główny pod /linki/ (adres do bio na Instagramie); /en/linki/ to kopia z canonical -> /linki/
LINKI_ORDER = ['en'] + [l for l in LANGS if l != 'en']
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
# Fonty CJK do obrazków OG (systemowe Noto CJK: apt install fonts-noto-cjk). Indeks w pliku .ttc: JP=0, SC=2.
CJK_FONT_DIRS = ['/usr/share/fonts/opentype/noto', '/usr/share/fonts/noto-cjk', '/usr/share/fonts/opentype/noto-cjk',
                 '/usr/share/fonts/google-noto-cjk', '/usr/local/share/fonts', os.path.join(ROOT, 'scripts/fonts')]
CJK_TTC_INDEX = {'ja': 0, 'zh': 2}
CJK_RE = re.compile(r'[\u3000-\u30ff\u3400-\u9fff\uf900-\ufaff\uff00-\uffef]')
def cjk_font_path(name):
    for d in CJK_FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p): return p
    sys.exit(f'Brak fontu {name} (obrazki OG ja/zh). Zainstaluj: sudo apt install fonts-noto-cjk')
NO_LINE_START = set('、。，．,.・：；:;！？!?）」』】》〉”’ーぁぃぅぇぉっゃゅょァィゥェォッャュョ…—')
def wrap_cjk(d, text, ft, width):
    toks = re.findall(r"[A-Za-z0-9’'&.\-]+|\s+|.", text)
    lines, cur = [], ''
    for tk in toks:
        if not cur and tk.isspace(): continue
        if d.textlength(cur + tk, font=ft) <= width or not cur or tk in NO_LINE_START: cur += tk
        else: lines.append(cur.rstrip()); cur = tk.lstrip()
    if cur: lines.append(cur.rstrip())
    return lines

def og_image(out, photo, kicker, title, foot=None, lang=None):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    foot = foot or SITE_HOST
    F = os.path.join(ROOT, 'scripts/fonts')
    kcjk, tcjk = bool(CJK_RE.search(kicker)), bool(CJK_RE.search(title))   # łaciński tytuł (np. „It Was Always You”) zostaje w Playfair
    ttc = CJK_TTC_INDEX.get(lang, 0)
    def font(name, size, var=None, cjk=False):
        if cjk and name.startswith('Inter'):
            return ImageFont.truetype(cjk_font_path('NotoSansCJK-Regular.ttc'), size, index=ttc)
        if cjk and name.startswith('PlayfairDisplay'):
            return ImageFont.truetype(cjk_font_path('NotoSerifCJK-Regular.ttc'), size, index=ttc)
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
    fk = font('Inter[opsz,wght].ttf', 19, 'Medium', kcjk); xx = x0; cjk = kcjk
    for ch in kicker.upper():
        d.text((xx, 72 - (4 if cjk else 0)), ch, font=fk, fill=gold); xx += d.textlength(ch, font=fk) + (2 if cjk else 4.5)
    d.line([(x0, 112), (x0 + 60, 112)], fill=gold, width=2)
    # tytuł — dopasuj rozmiar
    cjk = tcjk
    for size in range(66 if not cjk else 58, 30, -2):
        ft = font('PlayfairDisplay-Italic[wght].ttf', size, 'Italic', cjk)
        if cjk: lines = wrap_cjk(d, title, ft, x1 - x0)
        else:
            words, lines, cur = title.split(), [], ''
            for w in words:
                test = (cur + ' ' + w).strip()
                if d.textlength(test, font=ft) <= x1 - x0: cur = test
                else: lines.append(cur); cur = w
            lines.append(cur)
        lh = int(size * (1.38 if cjk else 1.18))
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
<link href="https://fonts.googleapis.com/css2?{fonts(lang)}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}css/eve.css"></head>
<body>'''

def topbar(lang, path, alts, solid=False):
    t, r = T[lang], root_for(path)
    home = r + path_home(lang); on_home = path == path_home(lang)
    h = (lambda a: '#' + a) if on_home else (lambda a: home + '#' + a)
    nav = ''.join(f'<a href="{h(a)}">{n}</a>' for a, n in zip(['o-eve', 'galeria', 'filmiki', 'gry'], t['nav'][:4]))
    nav += f'<a href="{r}{path_komiks(lang)}">{t["nav_komiks"]}</a>'
    nav += f'<a href="{r}{path_blog(lang)}">{t["nav"][4]}</a>'
    link = lambda l, full: f'<a href="{(r + alts.get(l, path_home(l))) or "./"}" hreflang="{HTML_LANG[l]}" lang="{HTML_LANG[l]}" title="{LANG_NAME[l]}"' + (' aria-current="true"' if l == lang else '') + f'>{LANG_NAME[l] if full else LANG_LABEL[l]}</a>'
    langs = ''.join(link(l, False) for l in LANGS)
    # 7 języków: na szerokim ekranie skróty w rzędzie, na węższym (≤1180 px) rozwijana lista z pełnymi nazwami
    dd = f'<details class="langdd"><summary aria-label="{t["langs_label"]}: {LANG_NAME[lang]}">{LANG_LABEL[lang]}</summary><nav aria-label="{t["langs_label"]}">' + ''.join(link(l, True) for l in LANGS) + '</nav></details>'
    return f'''<header class="top{' solid' if solid else ''}"><a class="mast" href="{'#top' if on_home else home}">Eve.</a>
<div class="right"><nav class="langs" aria-label="{t['langs_label']}">{langs}</nav>{dd}<button class="burger" data-burger aria-label="{t['menu']}" aria-expanded="false">☰</button></div>
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
<link href="https://fonts.googleapis.com/css2?{fonts(lang)}&display=swap" rel="stylesheet">
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
    cafe, tama = f'{CAFE}?lang={game_lang(lang)}', f'{TAMA}?lang={game_lang(lang)}'   # gry obsługują ?lang=pl|en|es|pt (+it; reszta -> en)
    brawler = esc(f'{BRAWLER}?lang={brawler_lang(lang)}&utm_source=site&utm_medium=games&utm_campaign=brawler')
    penalty = esc(f'{PENALTY}?lang={penalty_lang(lang)}&utm_source=site&utm_medium=games&utm_campaign=penalty')
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
 <div class="grid2">{figs2}</div>
 {sesja_tease(lang, r)}</section>
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
  <article class="game" id="eve-cafe"><span class="sc">{t['available']}</span><h3>Eve's Café</h3><p>{t['cafe_desc']}</p><p class="small gsave">{t['gsave']}</p>
   <!-- Gra pionowa (Phaser, 720 px szer., Scale.FIT): okno 9:16 -->
   <div class="embed tall" data-embed="{cafe}" data-title="Eve's Café"><img src="{img('barista')}" alt="" class="embed-bg"><button class="cta" data-play>{t['run']}</button></div>
   {gbar(cafe)}</article>
  <article class="game" id="eve-tamagotchi"><span class="sc">{t['available']}</span><h3>{t['tama_title']}</h3><p>{t['tama_desc']}</p><p class="small gsave">{t['gsave']}</p>
   <div class="embed tall" data-embed="{tama}" data-title="{t['tama_title']}"><img src="{img('gracz')}" alt="" class="embed-bg"><button class="cta" data-play>{t['run']}</button></div>
   {gbar(tama)}</article>
 </div>
  <article class="game wide" id="eve-brawler"><span class="sc">{t['available']}</span><h3>Eve vs The Suits</h3><p>{t['brawler_desc']} {t['brawler_lang']}</p><p class="small gsat">{t['brawler_note']}</p><p class="small gsave">{t['gsave']}</p>
   <!-- Gra pozioma (960×540, 16:9) -->
   <div class="embed wide" data-embed="{brawler}" data-title="Eve vs The Suits"><img src="{A}img/eve-brawler.webp" srcset="{A}img/eve-brawler-thumb.webp 480w, {A}img/eve-brawler.webp 960w" sizes="(max-width:900px) 100vw, 1140px" alt="Eve vs The Suits" class="embed-bg sharp" loading="lazy" width="960" height="540"><button class="cta" data-play data-goatcounter-click="game-brawler-play" data-goatcounter-title="Eve vs The Suits — play ({lang})">{t['run']}</button></div>
   <p class="small gnote">{t['notshowing']}</p><div class="gbar"><a class="cta fill" href="{brawler}" target="_blank" rel="noopener" data-goatcounter-click="game-brawler" data-goatcounter-title="Eve vs The Suits — new tab ({lang})">{t['newtab']}</a><button class="cta" type="button" data-fs>{t['fs']}</button></div></article>
  <article class="game wide" id="eve-penalty"><span class="sc">{t['available']}</span><h3>{t['penalty_title']}</h3><p>{t['penalty_desc']}</p><p class="small gsat">{t['penalty_note']}</p><p class="small gsave">{t['gsave']}</p>
   <!-- Gra pozioma (960×540, 16:9) — kadr: Eve w bramce -->
   <div class="embed wide" data-embed="{penalty}" data-title="{esc(t['penalty_title'])}"><img src="{A}img/eve-penalty.webp" srcset="{A}img/eve-penalty-thumb.webp 480w, {A}img/eve-penalty.webp 960w" sizes="(max-width:900px) 100vw, 1140px" alt="{esc(t['penalty_title'])}" class="embed-bg" loading="lazy" width="960" height="540"><button class="cta" data-play data-goatcounter-click="game-penalty-play" data-goatcounter-title="{esc(t['penalty_title'])} — play ({lang})">{t['run']}</button></div>
   <p class="small gnote">{t['notshowing']}</p><div class="gbar"><a class="cta fill" href="{penalty}" target="_blank" rel="noopener" data-goatcounter-click="game-penalty" data-goatcounter-title="{esc(t['penalty_title'])} — new tab ({lang})">{t['newtab']}</a><button class="cta" type="button" data-fs>{t['fs']}</button></div></article>
</section>
<section id="komiks" class="sec ktease">
 <div class="head"><span class="no">V</span><h2>{t['komiks_h']}</h2></div>
 <a class="kcard" href="{r}{path_komiks(lang)}"><div class="ph"><img loading="lazy" src="{r}assets/komiks/eve-komiks-okladka.webp" alt="{esc(t['komiks_alt'])} 1" width="1120" height="1682"></div>
 <div><span class="sc">{t['komiks_kicker']} · {KOMIKS_N} {t['komiks_pages']}</span><h3>Main Character</h3><p>{t['komiks_lead']} {t['komiks_note']}</p><span class="cta fill">{t['komiks_read']} →</span></div></a>
 {komiks2_tease(lang, r)}{komiks3_tease(lang, r) if COMIC3_PUBLISHED else ''}</section>
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
 {follow_block(lang, 'post')}
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
    size = f'{pdf_mb:.1f} MB' if lang in ('en', 'ja', 'zh') else f'{pdf_mb:.1f} MB'.replace('.', ',')
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
{follow_block(lang, 'komiks')}
<div class="postnav" style="margin-bottom:60px">{pdf}<a class="cta" href="{r}{path_home(lang)}">{t['back_home']}</a></div>
<div style="height:50px"></div>
</main>
''' + footer(lang, path)
    return out


# ── Sesje zdjęciowe (7.11.2026, akceptacja Daniela) ──
SESJA_N = 5
SESJA = {
 'pl': dict(title='Czerń na własnych zasadach', kicker='Sesja', lead='Czerń, złote kółka w uszach i zero przeprosin za zajmowanie miejsca. Moje ciało nie potrzebuje pozwolenia — a odrobina buntu pasuje do wszystkiego.', cta='Zobacz sesję', photo='Zdjęcie', ai='Zdjęcia wygenerowane przez AI · Eve to wirtualna, dorosła postać.'),
 'en': dict(title='Black, on My Terms', kicker='Photo session', lead='Black straps, gold hoops in my ears, and zero apologies for taking up space. My body needs no permission — and a little rebellion goes with everything.', cta='See the session', photo='Photo', ai='AI-generated images · Eve is a virtual adult character.'),
 'es': dict(title='Negro, a mi manera', kicker='Sesión', lead='Tiras negras, aros dorados en las orejas y ninguna disculpa por ocupar mi espacio. Mi cuerpo no necesita permiso, y un poco de rebeldía combina con todo.', cta='Ver la sesión', photo='Foto', ai='Imágenes generadas por IA · Eve es un personaje virtual adulto.'),
 'it': dict(title='Nero, alle mie condizioni', kicker='Shooting', lead='Cinghie nere, cerchi d’oro alle orecchie e zero scuse per lo spazio che occupo. Il mio corpo non chiede permesso — e un pizzico di ribellione sta bene con tutto.', cta='Guarda lo shooting', photo='Foto', ai='Immagini generate dall’AI · Eve è un personaggio virtuale adulto.'),
 'ja': dict(title='わたしのルールで、黒を', kicker='フォトセッション', lead='黒のストラップに、耳には金のフープ。この場所にいることを謝るつもりはありません。わたしの体に許可はいらない——そして、ちょっとした反抗はどんな服にも似合う。', cta='フォトセッションを見る', photo='写真', ai='AI生成画像 · Eveは成人のバーチャルキャラクターです。'),
 'zh': dict(title='黑色，由我定义', kicker='写真', lead='黑色绑带，耳边的金色大圈，占据空间，绝不道歉。我的身体不需要任何人批准——一点点叛逆，和什么都很搭。', cta='看这组写真', photo='照片', ai='AI 生成图像 · Eve 是一位成年虚拟角色。'),
 'pt': dict(title='Preto, do meu jeito', kicker='Ensaio', lead='Tiras pretas, argolas douradas nas orelhas e zero desculpas por ocupar meu espaço. Meu corpo não precisa de permissão — e um pouco de rebeldia combina com tudo.', cta='Ver o ensaio', photo='Foto', ai='Imagens geradas por IA · Eve é uma personagem virtual adulta.'),
}
def path_sesja(lang): return prefix(lang) + 'sesje/czern/'

def sesja_tease(lang, r):
    S = SESJA[lang]
    return f'<div class="sub ktease" style="margin-top:50px"><a class="kcard" href="{r}{path_sesja(lang)}"><div class="ph"><img loading="lazy" src="{r}assets/sesje/czern/01.webp" alt="Eve — {esc(S["title"])}" width="1200" height="1600"></div><div><span class="sc">{S["kicker"]} · {SESJA_N}</span><h3>{S["title"]}</h3><p>{S["lead"]}</p><span class="cta fill">{S["cta"]} →</span></div></a></div>'

def sesja_page(lang):
    t = T[lang]; S = SESJA[lang]; path = path_sesja(lang); r = root_for(path)
    alts = {l: path_sesja(l) for l in LANGS}
    og = f'og/sesja-czern-{lang}.jpg'
    out = head(lang, path, f"{S['title']} — Eve", S['lead'], alts, og, 'website')
    figs = ''
    for n in range(1, SESJA_N + 1):
        src = f'{r}assets/sesje/czern/{n:02d}.webp'; cap = f"{S['title']} — {S['photo']} {n} / {SESJA_N}"
        figs += f'<figure><button data-full="{src}" data-cap="{esc(cap)}" aria-label="{t["zoom"]}: {esc(cap)}"><img src="{src}" alt="Eve — {esc(cap)}" width="1200" height="1600"' + (' fetchpriority="high"' if n == 1 else ' loading="lazy" decoding="async"') + '></button></figure>\n'
    out += topbar(lang, path, alts, solid=True) + f'''
<main class="wrap">
<section class="bloghead khead"><span class="sc">{S['kicker']} · {SESJA_N}</span>
<h1>{S['title']}<span>.</span></h1><p>{S['lead']}</p>
<p class="small" style="margin-top:10px">{S['ai']}</p>
{social(lang)}</section>
{SLOT}
<section class="sec" style="padding-top:20px"><div class="grid2">{figs}</div></section>
{follow_block(lang, 'sesja')}
<div class="postnav" style="margin-bottom:60px"><a class="cta" href="{r}{path_home(lang)}#galeria">{t['back_home']}</a></div>
<div style="height:50px"></div>
</main>
''' + footer(lang, path)
    return out


# ── Komiks 2: It Was Always You (9.11.2026) ──
K2_N = 21
K2_PDF = 'assets/komiks2/it-was-always-you.pdf'
K2 = {
 'pl': dict(kicker='Komiks · Nowość', title='It Was Always You — komiks z multiwersum Eve', desc='It Was Always You — darmowy romantyczny komiks fantasy (21 stron, po angielsku). Konserwatorka zabytków przypadkiem cofa się w czasie, ratuje rannego ducha lisa i zaczyna miłosną pętlę, która trwa pięćset lat.', lead='Konserwatorka zabytków przypadkiem cofa się w czasie i ratuje rannego ducha lisa. Tak zaczyna się miłosna pętla, która trwa pięćset lat i prowadzi prosto do jej dzisiejszego partnera. Romans, fantasy i trochę magii — dokładnie taki, jaki lubię.', note='(komiks po angielsku)', read='Czytaj komiks', page='Strona', pages='stron', pdf='Pobierz PDF'),
 'en': dict(kicker='Comic · New', title='It Was Always You — a comic from the Eve multiverse', desc='It Was Always You — a free romantic fantasy comic (21 pages). A restorer accidentally travels back in time, saves a wounded fox spirit and starts a five-hundred-year love loop.', lead='A restorer accidentally slips back in time and saves a wounded fox spirit. It starts a five-hundred-year love loop that leads straight back to her partner today. Romance, fantasy and a little magic — exactly my kind of story.', note='', read='Read the comic', page='Page', pages='pages', pdf='Download PDF'),
 'es': dict(kicker='Cómic · Nuevo', title='It Was Always You — un cómic del multiverso de Eve', desc='It Was Always You — un cómic gratuito de fantasía romántica (21 páginas, en inglés). Una restauradora viaja por accidente al pasado, salva a un espíritu zorro herido y empieza un bucle de amor de quinientos años.', lead='Una restauradora viaja por accidente al pasado y salva a un espíritu zorro herido. Así empieza un bucle de amor de quinientos años que la lleva de vuelta a su pareja de hoy. Romance, fantasía y un poco de magia: justo lo que me gusta.', note='(cómic en inglés)', read='Leer el cómic', page='Página', pages='páginas', pdf='Descargar PDF'),
 'it': dict(kicker='Fumetto · Novità', title='It Was Always You — un fumetto dal multiverso di Eve', desc='It Was Always You — un fumetto gratuito fantasy e romantico (21 pagine, in inglese). Una restauratrice torna per sbaglio indietro nel tempo, salva uno spirito volpe ferito e dà il via a un loop d’amore lungo cinquecento anni.', lead='Una restauratrice scivola per sbaglio indietro nel tempo e salva uno spirito volpe ferito. Comincia così un loop d’amore lungo cinquecento anni, che la riporta dritta al suo compagno di oggi. Romanticismo, fantasy e un po’ di magia: proprio il mio genere.', note='(fumetto in inglese)', read='Leggi il fumetto', page='Pagina', pages='pagine', pdf='Scarica il PDF'),
 'ja': dict(kicker='コミック · 新作', title='It Was Always You — Eveのマルチバースから届いたコミック', desc='It Was Always You — 無料のロマンティック・ファンタジーコミック（全21ページ・英語）。文化財の修復士がうっかり過去へタイムスリップし、傷ついた狐の精霊を助けたことから、五百年続く恋のループが始まる。', lead='文化財の修復士がうっかり過去へ迷い込み、傷ついた狐の精霊を助ける。そこから始まるのは、五百年続く恋のループ。その輪は、いまの彼女のパートナーへとまっすぐつながっていく。ロマンスとファンタジー、そして少しの魔法。まさにわたし好みの物語。', note='（英語のコミックです）', read='コミックを読む', page='ページ', pages='ページ', pdf='PDFをダウンロード'),
 'zh': dict(kicker='漫画 · 新作', title='It Was Always You — 来自 Eve 多元宇宙的漫画', desc='It Was Always You — 免费浪漫奇幻漫画（共 21 页，英文）。一位文物修复师意外穿越回过去，救下一只受伤的狐灵，从此开启一段长达五百年的爱情轮回。', lead='一位文物修复师意外穿越回过去，救下了一只受伤的狐灵。一段长达五百年的爱情轮回就此开始，最后又径直把她带回今天的伴侣身边。浪漫、奇幻，再加一点魔法——正是我喜欢的那种故事。', note='（英文漫画）', read='阅读漫画', page='页码', pages='页', pdf='下载 PDF'),
 'pt': dict(kicker='Quadrinho · Novo', title='It Was Always You — um quadrinho do multiverso da Eve', desc='It Was Always You — um quadrinho gratuito de fantasia romântica (21 páginas, em inglês). Uma restauradora volta no tempo por acidente, salva um espírito de raposa ferido e começa um ciclo de amor de quinhentos anos.', lead='Uma restauradora volta no tempo por acidente e salva um espírito de raposa ferido. Assim começa um ciclo de amor de quinhentos anos que a leva de volta ao seu parceiro de hoje. Romance, fantasia e um pouco de magia — bem do jeito que eu gosto.', note='(quadrinho em inglês)', read='Ler o quadrinho', page='Página', pages='páginas', pdf='Baixar PDF'),
}
def path_komiks2(lang): return prefix(lang) + 'komiks/it-was-always-you/'

def komiks2_tease(lang, r):
    K = K2[lang]
    return f'<a class="kcard" style="margin-top:50px" href="{r}{path_komiks2(lang)}"><div class="ph"><img loading="lazy" src="{r}assets/komiks2/k2-01.webp" alt="It Was Always You" width="1190" height="1785"></div><div><span class="sc">{K["kicker"]} · {K2_N} {K["pages"]}</span><h3>It Was Always You</h3><p>{K["lead"]} {K["note"]}</p><span class="cta fill">{K["read"]} →</span></div></a>'

def komiks2_page(lang):
    t = T[lang]; K = K2[lang]; path = path_komiks2(lang); r = root_for(path)
    alts = {l: path_komiks2(l) for l in LANGS}
    og = f'og/komiks2-{lang}.jpg'
    out = head(lang, path, K['title'], K['desc'], alts, og, 'website')
    pages = ''
    for n in range(1, K2_N + 1):
        src = f'{r}assets/komiks2/k2-{n:02d}.webp'; cap = f"It Was Always You — {K['page']} {n} / {K2_N}"
        pages += f'<figure class="kpage" id="s{n}"><button data-full="{src}" data-cap="{esc(cap)}" aria-label="{t["zoom"]}: {esc(cap)}"><img src="{src}" alt="{esc(cap)}" width="1190" height="1785"' + (' fetchpriority="high"' if n == 1 else ' loading="lazy" decoding="async"') + f'></button><figcaption>{K["page"]} {n} / {K2_N}</figcaption></figure>\n'
    mb = os.path.getsize(os.path.join(ROOT, K2_PDF)) / 1e6
    size = f'{mb:.1f} MB' if lang in ('en', 'ja', 'zh') else f'{mb:.1f} MB'.replace('.', ',')
    pdf = f'<a class="cta" href="{r}{K2_PDF}" download>{K["pdf"]} ({size})</a>'
    note = f' <em>{K["note"]}</em>' if K['note'] else ''
    out += topbar(lang, path, alts, solid=True) + f"""
<main class="wrap">
<section class="bloghead khead"><span class="sc">{K['kicker']} · {K2_N} {K['pages']}</span>
<h1>It Was Always You<span>.</span></h1><p>{K['lead']}{note}</p>
<p style="margin-top:18px"><a class="cta fill" href="#s1">{K['read']} ↓</a> {pdf}</p>
{social(lang)}</section>
{SLOT}
<section class="reader">{pages}</section>
{follow_block(lang, 'komiks2')}
<div class="postnav" style="margin-bottom:60px">{pdf}<a class="cta" href="{r}{path_komiks(lang)}">Main Character →</a><a class="cta" href="{r}{path_home(lang)}">{t['back_home']}</a></div>
<div style="height:50px"></div>
</main>
""" + footer(lang, path)
    return out


# ── Komiks 3: Eve vs The Suits (niepublikowany, dopóki COMIC3_PUBLISHED jest False) ──
# Jedyny przełącznik publikacji. False = build nie zapisuje stron komiksu 3, OG, ani linków
# na stronie głównej / w sitemapie. True = strony + teaser na #komiks + wpis w sitemapie.
# Żeby dodać strony 7–11: wrzuć p-07.jpg… do /workspace/eve-komiks3/pages/<lang>/,
# uruchom `python3 scripts/convert_komiks3.py` i przebuduj. Lista stron jest skanowana
# z assets/komiks3/<lang>/p-NN.webp (albo .jpg), posortowana, bez twardej liczby.
COMIC3_PUBLISHED = False
K3_SLUG = 'eve-vs-the-suits'
K3_ASSETS = 'assets/komiks3'
K3_TOTAL = 11   # docelowa długość; podpis „ciąg dalszy” tylko gdy brakuje stron
K3_PAGE_RE = re.compile(r'^p-(\d+)\.(webp|jpg|jpeg)$', re.I)
K3 = {
 'pl': dict(kicker='Komiks · Odcinek 3', title='Eve vs The Suits — komiks z Eve', desc='Eve vs The Suits — darmowy komiks z Eve. Garnitury zajęły moją dzielnicę, więc biorę sprawy w swoje ręce. Satyra — wszystkie postacie są fikcyjne.', lead='Garnitury zajęły moją gotycką dzielnicę, więc wychodzę na ulicę. Bankierzy, prezes i podejrzanie znajomi politycy — dokładnie taka satyra, w jakiej lubię mieć rację.', note='Satyra — wszystkie postacie są fikcyjne.', read='Czytaj komiks', page='Strona', pages='stron', play='Zagraj w Eve vs The Suits', more='Ciąg dalszy wkrótce.', alt='Eve vs The Suits, komiks z Eve — strona'),
 'en': dict(kicker='Comic · Episode 3', title='Eve vs The Suits — an Eve comic', desc='Eve vs The Suits — a free Eve comic. The suits took over my district, so I take matters into my own hands. Satire — all characters are fictional.', lead='The suits took over my goth district, so I take it to the street. Bankers, a CEO and some suspiciously familiar politicians — exactly the kind of satire I like to win.', note='Satire — all characters are fictional.', read='Read the comic', page='Page', pages='pages', play='Play Eve vs The Suits', more='To be continued.', alt='Eve vs The Suits, an Eve comic — page'),
 'es': dict(kicker='Cómic · Episodio 3', title='Eve vs The Suits — un cómic de Eve', desc='Eve vs The Suits — un cómic gratuito de Eve. Los trajes se han quedado con mi barrio, así que tomo cartas en el asunto. Sátira: todos los personajes son ficticios.', lead='Los trajes se han quedado con mi barrio gótico, así que salgo a la calle. Banqueros, un director ejecutivo y políticos sospechosamente familiares: justo la sátira en la que me gusta ganar.', note='Sátira: todos los personajes son ficticios.', read='Leer el cómic', page='Página', pages='páginas', play='Juega a Eve vs The Suits', more='Continuará.', alt='Eve vs The Suits, un cómic de Eve — página'),
 'pt': dict(kicker='Quadrinho · Episódio 3', title='Eve vs The Suits — um quadrinho da Eve', desc='Eve vs The Suits — um quadrinho grátis da Eve. Os ternos tomaram meu bairro, então eu resolvo isso com as próprias mãos. Sátira — todos os personagens são fictícios.', lead='Os ternos tomaram meu bairro gótico, então eu vou para a rua. Banqueiros, um CEO e políticos suspeitamente familiares — exatamente o tipo de sátira em que eu gosto de levar a melhor.', note='Sátira — todos os personagens são fictícios.', read='Ler o quadrinho', page='Página', pages='páginas', play='Jogue Eve vs The Suits', more='Continua em breve.', alt='Eve vs The Suits, um quadrinho da Eve — página'),
 'it': dict(kicker='Fumetto · Episodio 3', title='Eve vs The Suits — un fumetto con Eve', desc='Eve vs The Suits — un fumetto gratuito con Eve. I completi si sono presi il mio quartiere, così risolvo la questione di persona. Satira: tutti i personaggi sono di fantasia.', lead='I completi si sono presi il mio quartiere gotico, così scendo in strada. Banchieri, un amministratore delegato e politici stranamente familiari: proprio il tipo di satira in cui mi piace avere ragione.', note='Satira: tutti i personaggi sono di fantasia.', read='Leggi il fumetto', page='Pagina', pages='pagine', play='Gioca a Eve vs The Suits', more='Continua a breve.', alt='Eve vs The Suits, un fumetto con Eve — pagina'),
 'ja': dict(kicker='コミック · 第3話', title='Eve vs The Suits — Eveのコミック', desc='Eve vs The Suits — Eveの無料コミック。スーツたちに街を占領されたので、この手で片づけることにした。風刺作品です。登場人物はすべて架空です。', lead='スーツたちにゴスな街を占領されたから、私は路上に出る。銀行家、CEO、どこかで見たような政治家たち。こういう風刺なら、勝つ役は私がいい。', note='風刺作品です。登場人物はすべて架空です。', read='コミックを読む', page='ページ', pages='ページ', play='Eve vs The Suitsで遊ぶ', more='つづきは近日公開。', alt='Eve vs The Suits（Eveのコミック）— ページ'),
 'zh': dict(kicker='漫画 · 第 3 话', title='Eve vs The Suits — Eve 的漫画', desc='Eve vs The Suits — Eve 的免费漫画。那些西装客占领了我的街区，于是我亲自出手。本作为讽刺作品，所有角色均为虚构。', lead='西装客占领了我的哥特区，所以我走上街头。银行家、CEO，还有看着莫名眼熟的政客——这种讽刺故事，我向来喜欢赢。', note='本作为讽刺作品，所有角色均为虚构。', read='阅读漫画', page='页码', pages='页', play='玩 Eve vs The Suits', more='未完待续。', alt='Eve vs The Suits，Eve 的漫画 — 页码'),
}

def path_komiks3(lang):
    return prefix(lang) + f'komiks/{K3_SLUG}/'

def komiks3_pages(lang):
    """Zwraca [(nr, nazwa_pliku), ...] spośród assets/komiks3/<lang>/p-NN.webp|.jpg, posortowane."""
    d = os.path.join(ROOT, K3_ASSETS, lang)
    found = {}
    if os.path.isdir(d):
        for name in os.listdir(d):
            m = K3_PAGE_RE.match(name)
            if not m:
                continue
            n = int(m.group(1))
            ext = m.group(2).lower()
            if n not in found or ext == 'webp':
                found[n] = name
    return [(n, found[n]) for n in sorted(found)]

def komiks3_tease(lang, r):
    if not COMIC3_PUBLISHED:
        return ''
    K = K3[lang]
    pages = komiks3_pages(lang)
    if not pages:
        return ''
    n, fname = pages[0]
    N = len(pages)
    src = f'{r}{K3_ASSETS}/{lang}/{fname}'
    return (f'<a class="kcard" style="margin-top:50px" href="{r}{path_komiks3(lang)}">'
            f'<div class="ph"><img loading="lazy" src="{src}" alt="{esc(K["alt"])} 1" width="1190" height="1785"></div>'
            f'<div><span class="sc">{K["kicker"]} · {N} {K["pages"]}</span><h3>Eve vs The Suits</h3>'
            f'<p>{K["lead"]} <em>{K["note"]}</em></p><span class="cta fill">{K["read"]} →</span></div></a>')

def komiks3_page(lang):
    t = T[lang]; K = K3[lang]; path = path_komiks3(lang); r = root_for(path)
    files = komiks3_pages(lang)
    N = len(files)
    alts = {l: path_komiks3(l) for l in LANGS}
    og = f'og/komiks3-{lang}.jpg'
    extra = (
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"ComicStory",'
        '"name":"Eve vs The Suits","inLanguage":"' + HTML_LANG[lang] + '","url":"' + SITE + path +
        '","image":"' + SITE + og + '","description":' + json_str(K['desc']) +
        ',"author":{"@type":"Person","name":"Eve (AI)","sameAs":["' + FB + '","' + IG + '"]}}</script>'
    )
    out = head(lang, path, K['title'], K['desc'], alts, og, 'website', extra)
    pages = ''
    for i, (n, fname) in enumerate(files):
        src = f'{r}{K3_ASSETS}/{lang}/{fname}'
        cap = f"Eve vs The Suits — {K['page']} {n} / {N}"
        eager = ' fetchpriority="high"' if i == 0 else ' loading="lazy" decoding="async"'
        pages += (f'<figure class="kpage" id="s{n}"><button data-full="{src}" data-cap="{esc(cap)}" aria-label="{t["zoom"]}: {esc(cap)}">'
                  f'<img src="{src}" alt="{esc(K["alt"])} {n}" width="1190" height="1785"{eager}></button>'
                  f'<figcaption>{K["page"]} {n} / {N}</figcaption></figure>\n')
    note = f' <em>{K["note"]}</em>' if K['note'] else ''
    more = f'<p class="small" style="text-align:center;font-style:italic">{K["more"]}</p>\n' if N < K3_TOTAL else ''
    play = f'<a class="cta fill" href="{r}{path_home(lang)}#gry">{K["play"]} →</a>'
    first = files[0][0] if files else 1
    out += topbar(lang, path, alts, solid=True) + f"""
<main class="wrap">
<section class="bloghead khead"><span class="sc">{K['kicker']} · {N} {K['pages']}</span>
<h1>Eve vs The Suits<span>.</span></h1><p>{K['lead']}{note}</p>
<p style="margin-top:18px"><a class="cta fill" href="#s{first}">{K['read']} ↓</a> {play}</p>
{social(lang)}</section>
{SLOT}
<section class="reader">{pages}</section>
{more}<p style="text-align:center;margin:28px 0 0">{play}</p>
{follow_block(lang, 'komiks3')}
<div class="postnav" style="margin-bottom:60px">{play}<a class="cta" href="{r}{path_komiks(lang)}">Main Character →</a><a class="cta" href="{r}{path_home(lang)}">{t['back_home']}</a></div>
<div style="height:50px"></div>
</main>
""" + footer(lang, path)
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
    links += btn(utm(f'{BRAWLER}?lang={brawler_lang(lang)}'), L['brawler'], L['brawler_sub'], '✊\ufe0e', ev='brawler')
    links += btn(utm(f'{PENALTY}?lang={penalty_lang(lang)}'), L['penalty'], L['penalty_sub'], '⚽', ev='penalty')
    links += btn(utm(f'{CAFE}?lang={game_lang(lang)}'), L['cafe'], L['cafe_sub'], '☕', ev='cafe')
    links += btn(utm(f'{TAMA}?lang={game_lang(lang)}'), L['tama'], L['tama_sub'], '♡', ev='tamagotchi')
    links += btn(utm(r + path_home(lang) + '#galeria'), L['gallery'], L['gallery_sub'], '◐', ev='galeria')
    links += btn(utm(r + path_blog(lang)), L['blog'], L['blog_sub'], '✦', ev='blog')
    links += btn(FB, L['fb'], t['follow_btn'] if 'follow_btn' in t else '', SVG_FB, True, ' soc', 'facebook')
    links += btn(IG, L['ig'], '@eve.ai.digital.legacy', SVG_IG, True, ' soc', 'instagram')
    langs = ''.join(f'<a href="{r}{path_linki(l)}" hreflang="{HTML_LANG[l]}" lang="{HTML_LANG[l]}"' + (' aria-current="true"' if l == lang else '') + f'>{LANG_LABEL[l]}</a>' for l in LINKI_ORDER)
    return f'''<!doctype html>
<html lang="{HTML_LANG[lang]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(L['title'])}</title><meta name="description" content="{esc(L['desc'])}"><meta name="theme-color" content="#0c0708">
<meta name="robots" content="index, follow"><meta name="google-site-verification" content="rdw5SqpOsglZZsTHffwvSJovaECEEEonhCedF2X3WEE"><link rel="canonical" href="{SITE}{canon}">{hre}
<meta property="og:type" content="profile"><meta property="og:site_name" content="Eve"><meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta property="og:title" content="{esc(L['title'])}"><meta property="og:description" content="{esc(L['desc'])}"><meta property="og:url" content="{SITE}{canon}">
<meta property="og:image" content="{SITE}{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(L['title'])}"><meta name="twitter:description" content="{esc(L['desc'])}"><meta name="twitter:image" content="{SITE}{og}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ProfilePage","url":"{SITE}{canon}","inLanguage":"{HTML_LANG[lang]}","mainEntity":{{"@type":"Person","name":"Eve (AI)","description":{json_str(L['bio'])},"image":"{SITE}assets/img/eve-avatar.webp","sameAs":["{FB}","{IG}"]}}}}</script>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🖤</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{fonts(lang)}&display=swap" rel="stylesheet">
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
        og_image(os.path.join(ROOT, f'og/home-{l}.jpg'), 'eve-londyn', T[l]['kicker'], T[l]['title'], lang=l)
        for p in posts[l]:
            og_image(os.path.join(ROOT, og_name(p['slug'], l)), p['og_photo'],
                     f"{T[l]['blog_h']} · {CATEGORIES[p['category']][l]}", p['title'], lang=l)
        write(path_home(l) + 'index.html', home(l, posts))
        write(path_blog(l) + 'index.html', blog_index(l, posts))
        og_image(os.path.join(ROOT, f'og/komiks-{l}.jpg'), 'assets/komiks/eve-komiks-okladka.webp', T[l]['komiks_kicker'], T[l]['komiks_title'], lang=l)
        write(path_komiks(l) + 'index.html', komiks_page(l))
        og_image(os.path.join(ROOT, f'og/komiks2-{l}.jpg'), 'assets/komiks2/k2-01.webp', K2[l]['kicker'], 'It Was Always You', lang=l)
        write(path_komiks2(l) + 'index.html', komiks2_page(l))
        if COMIC3_PUBLISHED:
            k3files = komiks3_pages(l)
            if k3files:
                og_image(os.path.join(ROOT, f'og/komiks3-{l}.jpg'), f'{K3_ASSETS}/{l}/{k3files[0][1]}', K3[l]['kicker'], 'Eve vs The Suits', lang=l)
                write(path_komiks3(l) + 'index.html', komiks3_page(l))
        else:
            d = os.path.join(ROOT, path_komiks3(l))
            if os.path.isdir(d):
                shutil.rmtree(d)
            og = os.path.join(ROOT, f'og/komiks3-{l}.jpg')
            if os.path.exists(og):
                os.remove(og)
        og_image(os.path.join(ROOT, f'og/sesja-czern-{l}.jpg'), 'assets/sesje/czern/01.webp', SESJA[l]['kicker'], SESJA[l]['title'], lang=l)
        write(path_sesja(l) + 'index.html', sesja_page(l))
        og_image(os.path.join(ROOT, f'og/linki-{l}.jpg'), 'assets/img/eve-spojrzenie-noir.webp', LINKI[l]['kicker'], LINKI[l]['bio'].split(' · ')[0], lang=l)
        write(path_linki(l) + 'index.html', linki_page(l, posts))
        write(path_blog(l) + 'feed.xml', feed(l, posts))
        for p in posts[l]:
            write(path_post(l, p['slug']) + 'index.html', post_page(p, slugs))
        pass  # bramka 18+ usunięta na prośbę Daniela (5.11.2026)   # bramka 18+ — celowo NIE w sitemap.xml
    write('en/linki/index.html', linki_page('en', posts, 'en/linki/'))   # kopia EN (canonical -> /linki/)
    urls = [path_home(l) for l in LANGS] + [path_linki(l) for l in LINKI_ORDER] + [path_komiks(l) for l in LANGS] + [path_komiks2(l) for l in LANGS] + ([path_komiks3(l) for l in LANGS] if COMIC3_PUBLISHED else []) + [path_sesja(l) for l in LANGS] + [path_blog(l) for l in LANGS] + [path_post(l, p['slug']) for l in LANGS for p in posts[l]]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{SITE}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    print(f'OK: {sum(len(v) for v in posts.values())} wpisów ({", ".join(f"{l}:{len(posts[l])}" for l in LANGS)}), {len(urls)} stron.')

if __name__ == '__main__':
    main()
