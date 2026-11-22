# -*- coding: utf-8 -*-
"""Warstwa PWA strony Eve (apka na telefon): manifest, service worker, ikony, strony offline, przycisk instalacji.

Wywoływane z build.py:
  pwa_head(r, lang)  -> znaczniki do <head> KAŻDEJ strony (manifest, ikony Apple, js/pwa.js). Nie usuwać z head()!
  build_pwa(ROOT, write) -> generuje manifest.webmanifest, sw.js, js/pwa.js, <lang>/offline.html, assets/pwa/*.png
Właścicielka warstwy PWA: Gry. Treści strony (wpisy, komiksy) są poza tym plikiem.
Gry w apce: /gry/karne/ i /gry/brawler/ = zbudowane dist gier, aktualizacja jednym poleceniem: scripts/sync_games.sh
  (każda gra ma własny sw.js ze scope /gry/<gra>/; SW strony nie cache'uje /gry/ i nie kasuje cache gier).
Powiadomienia push: Worker eve-push (/workspace/eve-push, prywatny). Przycisk „Włącz powiadomienia” pojawia się
  dopiero, gdy PUSH_API poniżej nie jest puste; wysyłka: node /workspace/eve-push/scripts/notify.mjs (README tam).
"""
import os, json, hashlib, html, shutil, subprocess

LANGS = ['pl', 'en', 'es', 'pt', 'it', 'ja', 'zh', 'fr', 'de']
HTML_LANG = {'pl': 'pl', 'en': 'en', 'es': 'es', 'pt': 'pt-BR', 'it': 'it', 'ja': 'ja', 'zh': 'zh-Hans', 'fr': 'fr', 'de': 'de'}
INK, GOLD, GOLD2, PAPER, BUR = '#0c0708', '#c9a35b', '#e8cf96', '#f3ece0', '#3a0b16'
ICON_SRC = 'assets/img/eve-avatar.webp'   # portret SFW (twarz) — źródło ikon apki
PWA_DIR = 'assets/pwa/'
# Powiadomienia push (Cloudflare Worker eve-push, /workspace/eve-push). PUSH_API = '' -> przycisk ukryty (flaga).
PUSH_API = 'https://eve-push.wodzu2207.workers.dev'   # Worker eve-push, wdrożony 18.11.2026
VAPID_PUBLIC_KEY = 'BHjWY6NROqFXgTK2f8eUzoBvYPcnpEugI1et9AQMxG2Ga6csvtqX9PI-omwT-d1So85VOFr2hiQazWcyt_aRj1U'   # publiczny, może być w repo
def push_cfg(): return {'api': PUSH_API.rstrip('/'), 'key': VAPID_PUBLIC_KEY} if PUSH_API else None

def pre(l): return '' if l == 'pl' else l + '/'
# Podstrona dla twórców (robi ją Strona): pl -> dla-tworcow/, inne -> <lang>/for-creators/
def path_creators(l): return 'dla-tworcow/' if l == 'pl' else f'{l}/for-creators/'

TXT = {
 'pl': dict(push_t='Nowości od Eve', push='Daj znać, gdy pojawi się nowy wpis, komiks albo gra.', push_on='Włącz powiadomienia', push_ok='Powiadomienia włączone. Do zobaczenia!', install='Zainstaluj apkę Eve', sub='Gry, komiksy i nowe wpisy prosto z ekranu telefonu.', ios_t='Eve jako apka', ios='Dotknij <b>Udostępnij</b> {share}, a potem <b>„Dodaj do ekranu początkowego”</b>.', close='Zamknij',
            off_t='Jesteś offline', off='Ta strona nie jest jeszcze zapisana w apce. Strony, które już były otwarte, działają bez internetu.', retry='Spróbuj ponownie', home='Strona główna', games='Gry działają bez internetu, jeśli choć raz otworzysz je w apce.'),
 'en': dict(push_t='News from Eve', push='Get a heads-up when a new post, comic or game drops.', push_on='Turn on notifications', push_ok='Notifications are on. See you soon!', install='Install the Eve app', sub='Games, comics and new posts right from your home screen.', ios_t='Get the Eve app', ios='Tap <b>Share</b> {share}, then <b>“Add to Home Screen”</b>.', close='Close',
            off_t='You’re offline', off='This page isn’t saved in the app yet. Pages you have already opened work without internet.', retry='Try again', home='Home', games='Games work without internet once you have opened them in the app.'),
 'es': dict(push_t='Novedades de Eve', push='Te avisamos cuando haya una entrada, un cómic o un juego nuevo.', push_on='Activar notificaciones', push_ok='Notificaciones activadas. ¡Hasta pronto!', install='Instalar la app de Eve', sub='Juegos, cómics y nuevas entradas desde tu pantalla de inicio.', ios_t='Eve como app', ios='Toca <b>Compartir</b> {share} y luego <b>«Añadir a pantalla de inicio»</b>.', close='Cerrar',
            off_t='Estás sin conexión', off='Esta página aún no está guardada en la app. Las páginas que ya abriste funcionan sin internet.', retry='Reintentar', home='Inicio', games='Los juegos funcionan sin internet si los abriste una vez en la app.'),
 'pt': dict(push_t='Novidades da Eve', push='Receba um aviso quando sair um post, quadrinho ou jogo novo.', push_on='Ativar notificações', push_ok='Notificações ativadas. Até logo!', install='Instalar o app da Eve', sub='Jogos, quadrinhos e novos posts direto da tela inicial.', ios_t='Eve como app', ios='Toque em <b>Compartilhar</b> {share} e depois em <b>“Adicionar à Tela de Início”</b>.', close='Fechar',
            off_t='Você está offline', off='Esta página ainda não foi salva no app. As páginas que você já abriu funcionam sem internet.', retry='Tentar de novo', home='Início', games='Os jogos funcionam sem internet depois de abertos uma vez no app.'),
 'it': dict(push_t='Novità da Eve', push='Ti avvisiamo quando esce un nuovo articolo, fumetto o gioco.', push_on='Attiva le notifiche', push_ok='Notifiche attive. A presto!', install='Installa l’app di Eve', sub='Giochi, fumetti e nuovi articoli dalla schermata Home.', ios_t='Eve come app', ios='Tocca <b>Condividi</b> {share}, poi <b>«Aggiungi alla schermata Home»</b>.', close='Chiudi',
            off_t='Sei offline', off='Questa pagina non è ancora salvata nell’app. Le pagine che hai già aperto funzionano senza internet.', retry='Riprova', home='Home', games='I giochi funzionano senza internet dopo averli aperti una volta nell’app.'),
 'ja': dict(push_t='Eveからのお知らせ', push='新しい記事・コミック・ゲームが公開されたらお知らせします。', push_on='通知をオンにする', push_ok='通知をオンにしました。またね！', install='Eveアプリをインストール', sub='ゲーム、コミック、新着記事をホーム画面から。', ios_t='Eveをアプリで', ios='<b>共有</b> {share} をタップして<b>「ホーム画面に追加」</b>を選んでください。', close='閉じる',
            off_t='オフラインです', off='このページはまだアプリに保存されていません。一度開いたページはオフラインでも見られます。', retry='再読み込み', home='ホーム', games='ゲームはアプリで一度開くと、インターネットなしで遊べます。'),
 'zh': dict(push_t='Eve 的新消息', push='有新文章、漫画或游戏时第一时间通知你。', push_on='开启通知', push_ok='通知已开启。回头见！', install='安装 Eve 应用', sub='游戏、漫画和最新文章，从主屏幕直达。', ios_t='把 Eve 装成应用', ios='点击<b>分享</b> {share}，然后选择<b>“添加到主屏幕”</b>。', close='关闭',
            off_t='你已离线', off='此页面尚未保存到应用中。打开过的页面可以离线浏览。', retry='重试', home='首页', games='游戏在应用中打开过一次后，即可离线游玩。'),
 'fr': dict(push_t='Nouveautés d’Eve', push='Reçois une alerte quand un nouvel article, une BD ou un jeu sort.', push_on='Activer les notifications', push_ok='Notifications activées. À bientôt !', install='Installer l’appli d’Eve', sub='Jeux, BD et nouveaux articles directement depuis ton écran d’accueil.', ios_t='L’appli Eve', ios='Touche <b>Partager</b> {share}, puis <b>« Sur l’écran d’accueil »</b>.', close='Fermer',
            off_t='Tu es hors ligne', off='Cette page n’est pas encore enregistrée dans l’appli. Les pages que tu as déjà ouvertes fonctionnent sans internet.', retry='Réessayer', home='Accueil', games='Les jeux fonctionnent sans internet une fois ouverts dans l’appli.'),
 'de': dict(push_t='Neues von Eve', push='Wir sagen dir Bescheid, wenn ein neuer Beitrag, Comic oder ein neues Spiel erscheint.', push_on='Benachrichtigungen aktivieren', push_ok='Benachrichtigungen sind aktiv. Bis bald!', install='Eve-App installieren', sub='Spiele, Comics und neue Beiträge direkt vom Home-Bildschirm.', ios_t='Eve als App', ios='Tippe auf <b>Teilen</b> {share} und dann auf <b>„Zum Home-Bildschirm“</b>.', close='Schließen',
            off_t='Du bist offline', off='Diese Seite ist noch nicht in der App gespeichert. Seiten, die du schon geöffnet hast, funktionieren ohne Internet.', retry='Erneut versuchen', home='Startseite', games='Spiele funktionieren ohne Internet, sobald du sie einmal in der App geöffnet hast.'),
}

def pwa_head(r, lang):
    """Znaczniki PWA do <head>. r = ścieżka względna do korzenia strony ('', '../', ...)."""
    return (f'<link rel="manifest" href="{r}manifest.webmanifest">'
            f'<link rel="apple-touch-icon" href="{r}{PWA_DIR}apple-touch-icon.png">'
            f'<link rel="icon" type="image/png" sizes="192x192" href="{r}{PWA_DIR}icon-192.png">'
            '<meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes">'
            '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="Eve">'
            f'<script src="{r}js/pwa.js" data-lang="{lang}" defer></script>')

# ---------- ikony ----------
def _badge_font_path():
    """Playfair Display (nagłówki strony), potem inny szeryf. Odznaka powstaje przy budowie — czcionka nie trafia do repo."""
    queries = (
        'Playfair Display:weight=700',
        'Playfair Display',
        'Cormorant Garamond:weight=700',
        'Liberation Serif:weight=700',
        'DejaVu Serif:weight=bold',
        'serif:weight=700',
    )
    if shutil.which('fc-match'):
        for q in queries:
            r = subprocess.run(['fc-match', q, '--format', '%{file}'], capture_output=True, text=True)
            path = (r.stdout or '').strip()
            if r.returncode == 0 and path and os.path.isfile(path):
                return path
    for path in (
        '/usr/share/fonts/truetype/sand-box/google/Playfair Display/PlayfairDisplay-VariableFont_wght.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
    ):
        if os.path.isfile(path):
            return path
    raise FileNotFoundError('brak czcionki szeryfowej do odznaki powiadomień (Playfair Display / serif)')

def make_badge(size, font_path):
    """Biała litera E na całkowicie przezroczystym tle. Android w badge bierze tylko kanał alfa."""
    from PIL import Image, ImageDraw, ImageFont
    S = size * 8   # supersampling — gładka alfa, RGB zawsze czysta biel
    mask = Image.new('L', (S, S), 0)
    font = ImageFont.truetype(font_path, int(S * 0.76))
    if hasattr(font, 'set_variation_by_axes'):
        try:
            font.set_variation_by_axes([700])   # Bold, czytelne w 24 dp
        except (ValueError, OSError):
            pass
    draw = ImageDraw.Draw(mask)
    bbox = draw.textbbox((0, 0), 'E', font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((S - tw) // 2 - bbox[0], (S - th) // 2 - bbox[1]), 'E', font=font, fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    return Image.merge('RGBA', (Image.new('L', (size, size), 255),) * 3 + (mask,))

def make_icons(ROOT):
    from PIL import Image, ImageDraw
    out = os.path.join(ROOT, PWA_DIR); os.makedirs(out, exist_ok=True)
    src = Image.open(os.path.join(ROOT, ICON_SRC)).convert('RGB')
    def circle_icon(size, frac, ring=True):
        S = size * 4   # supersampling dla gładkich krawędzi
        bg = Image.new('RGB', (S, S), INK)
        d = int(S * frac); off = (S - d) // 2
        face = src.resize((d, d), Image.LANCZOS)
        m = Image.new('L', (d, d), 0); ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
        bg.paste(face, (off, off), m)
        if ring:
            w = max(4, S // 90)
            ImageDraw.Draw(bg).ellipse((off - w, off - w, off + d + w, off + d + w), outline=GOLD, width=w)
        return bg.resize((size, size), Image.LANCZOS)
    circle_icon(192, .86).save(out + 'icon-192.png', optimize=True)
    circle_icon(512, .86).save(out + 'icon-512.png', optimize=True)
    circle_icon(512, .72).save(out + 'icon-maskable-512.png', optimize=True)   # bezpieczna strefa: koło 80%
    src.resize((180, 180), Image.LANCZOS).save(out + 'apple-touch-icon.png', optimize=True)   # iOS sam zaokrągla rogi
    # Odznaka powiadomień Androida (status bar): monochromatyczne E, nie portret
    font_path = _badge_font_path()
    make_badge(96, font_path).save(out + 'badge-96.png', optimize=True)
    make_badge(72, font_path).save(out + 'badge-72.png', optimize=True)

def manifest(ROOT):
    shots = []
    for i, (f, lbl) in enumerate([('screenshot-home.webp', 'Eve — home'), ('screenshot-games.webp', 'Eve — games')]):
        if os.path.exists(os.path.join(ROOT, PWA_DIR, f)):
            shots.append({'src': PWA_DIR + f, 'sizes': '780x1688', 'type': 'image/webp', 'form_factor': 'narrow', 'label': lbl})
    m = {
        'id': '/', 'name': 'Eve', 'short_name': 'Eve',
        'description': 'Eve — gotycka muza AI: blog, komiksy, gry, galeria. Blog, comics, games and gallery in 9 languages.',
        'lang': 'pl', 'dir': 'ltr', 'start_url': './?source=pwa', 'scope': './',
        'display': 'standalone', 'display_override': ['standalone', 'minimal-ui'], 'orientation': 'portrait',
        'background_color': INK, 'theme_color': INK, 'categories': ['entertainment', 'lifestyle', 'games'],
        'icons': [
            {'src': PWA_DIR + 'icon-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
            {'src': PWA_DIR + 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
            {'src': PWA_DIR + 'icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        ],
        'shortcuts': [
            {'name': 'Gry / Games', 'url': './#gry', 'icons': [{'src': PWA_DIR + 'icon-192.png', 'sizes': '192x192'}]},
            {'name': 'Komiksy / Comics', 'url': './komiks/', 'icons': [{'src': PWA_DIR + 'icon-192.png', 'sizes': '192x192'}]},
            {'name': 'Blog', 'url': './blog/', 'icons': [{'src': PWA_DIR + 'icon-192.png', 'sizes': '192x192'}]},
            {'name': 'Eve in English', 'url': './en/', 'icons': [{'src': PWA_DIR + 'icon-192.png', 'sizes': '192x192'}]},
        ],
    }
    if shots: m['screenshots'] = shots
    return json.dumps(m, ensure_ascii=False, indent=1) + '\n'

def offline_page(l):
    t, r = TXT[l], '/'   # strona offline podstawiana pod dowolny adres -> ścieżki od korzenia domeny
    return f'''<!doctype html>
<html lang="{HTML_LANG[l]}" translate="no"><head><meta charset="utf-8"><meta name="google" content="notranslate"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(t['off_t'])} · Eve</title><meta name="robots" content="noindex"><meta name="theme-color" content="{INK}">
<link rel="manifest" href="{r}manifest.webmanifest"><link rel="icon" type="image/png" href="{r}{PWA_DIR}icon-192.png">
<style>body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:{INK};color:{PAPER};font:18px/1.6 "Cormorant Garamond",Georgia,serif;text-align:center;padding:24px;box-sizing:border-box}}
main{{max-width:30rem}}img{{width:112px;height:112px;border-radius:50%;border:2px solid {GOLD};margin:0 auto 18px;display:block}}
h1{{font:italic 400 2rem "Playfair Display",Georgia,serif;color:{GOLD2};margin:0 0 .4em}}p{{margin:.6em 0}}small{{color:#b9a89a}}
.b{{display:inline-block;margin:14px 6px 0;padding:10px 20px;border:1px solid {GOLD};color:{GOLD2};text-decoration:none;font:500 .72rem Inter,system-ui,sans-serif;letter-spacing:.24em;text-transform:uppercase;background:none;cursor:pointer}}.b.f{{background:{GOLD};color:{INK}}}</style></head>
<body><main><img src="{r}{PWA_DIR}icon-192.png" alt="Eve"><h1>{html.escape(t['off_t'])}</h1><p>{html.escape(t['off'])}</p><p><small>{html.escape(t['games'])}</small></p>
<button class="b f" onclick="location.reload()">{html.escape(t['retry'])}</button><a class="b" href="{r}{pre(l)}">{html.escape(t['home'])}</a></main></body></html>
'''

def _h(ROOT, rels):
    h = hashlib.sha256()
    for rel in rels:
        p = os.path.join(ROOT, rel)
        if os.path.isfile(p): h.update(open(p, 'rb').read())
    return h.hexdigest()[:10]

SW_TEMPLATE = r'''/* Service worker strony Eve — GENEROWANY przez scripts/pwa.py (build.py). Nie edytuj ręcznie. */
const VERSION = '__VERSION__';
const SHELL = 'eve-shell-' + VERSION, PAGES = 'eve-pages-v1', IMGS = 'eve-img-v1', FONTS = 'eve-fonts-v1';
const KEEP = [SHELL, PAGES, IMGS, FONTS];
const MAX_PAGES = 60, MAX_IMGS = 150, MAX_FONTS = 40;
const BASE = new URL('./', self.location).href;               // korzeń strony (scope)
const REQUIRED = __REQUIRED__;                                 // app shell — musi się pobrać
const OPTIONAL = __OPTIONAL__;                                 // mile widziane — 404 nie psuje instalacji
const LANGS = ['en', 'es', 'pt', 'it', 'ja', 'zh', 'fr', 'de'];
const u = p => new URL(p, BASE).href;
const GAMES = new URL('gry/', BASE).pathname;                  // /gry/ — gry w apce (scripts/sync_games.sh)

self.addEventListener('install', e => e.waitUntil((async () => {
  const c = await caches.open(SHELL);
  await c.addAll(REQUIRED.map(p => new Request(u(p), {cache: 'reload'})));
  await Promise.all(OPTIONAL.map(p => fetch(u(p), {cache: 'reload'}).then(r => r.ok ? c.put(u(p), r) : null).catch(() => null)));
  await self.skipWaiting();
})()));

self.addEventListener('activate', e => e.waitUntil((async () => {
  // tylko własne cache strony — gry w /gry/ (eve-penalty-*, eve-brawler-*) mają swoje i swój SW
  for (const k of await caches.keys()) if (/^eve-(shell|pages|img|fonts)-/.test(k) && !KEEP.includes(k)) await caches.delete(k);
  if (self.registration.navigationPreload) await self.registration.navigationPreload.enable().catch(() => {});
  await self.clients.claim();
})()));

async function trim(name, max) {
  const c = await caches.open(name), keys = await c.keys();
  for (let i = 0; i < keys.length - max; i++) await c.delete(keys[i]);   // najstarsze pierwsze
}
function offlineFor(url) {
  const rel = url.href.startsWith(BASE) ? url.href.slice(BASE.length) : '';
  const l = LANGS.find(x => rel === x || rel.startsWith(x + '/'));
  return u((l ? l + '/' : '') + 'offline.html');
}
function pageKey(url) { const k = new URL(url.href); k.search = ''; k.hash = ''; return k.href; }   // bez ?utm/?source

async function htmlNetworkFirst(e) {
  const url = new URL(e.request.url);
  try {
    const r = (await e.preloadResponse) || await fetch(e.request);
    if (r && r.ok && r.type === 'basic') {
      const copy = r.clone();
      e.waitUntil(caches.open(PAGES).then(c => c.put(pageKey(url), copy)).then(() => trim(PAGES, MAX_PAGES)));
    }
    return r;
  } catch (_) {
    return (await caches.match(pageKey(url), {ignoreSearch: true})) || (await caches.match(offlineFor(url)))
        || new Response('<h1>Offline</h1>', {status: 503, headers: {'Content-Type': 'text/html; charset=utf-8'}});
  }
}
async function cacheFirst(e, name, max) {
  const hit = await caches.match(e.request);
  if (hit) return hit;
  const r = await fetch(e.request);
  if (r && (r.ok || r.type === 'opaque')) {
    const copy = r.clone();
    e.waitUntil(caches.open(name).then(c => c.put(e.request, copy)).then(() => trim(name, max)));
  }
  return r;
}
async function staleWhileRevalidate(e) {
  const hit = await caches.match(e.request);
  const net = fetch(e.request).then(r => {
    if (r && r.ok) { const copy = r.clone(); caches.open(SHELL).then(c => c.put(e.request, copy)); }
    return r;
  }).catch(() => hit);
  if (hit) { e.waitUntil(net); return hit; }
  return net;
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (/goatcounter\.com$|(^|\.)zgo\.at$/.test(url.hostname)) return;           // analityka — zawsze sieć, nigdy cache
  if (url.origin === 'https://fonts.googleapis.com' || url.origin === 'https://fonts.gstatic.com')
    return e.respondWith(cacheFirst(e, FONTS, MAX_FONTS));
  if (url.origin !== self.location.origin) return;                              // inne domeny — bez zmian
  if (url.pathname.startsWith(GAMES)) {                                         // gry mają własne SW (scope /gry/<gra>/)
    if (req.mode === 'navigate') e.respondWith(fetch(req).catch(async () => (await caches.match(offlineFor(url))) || Response.error()));
    return;                                                                     // pliki gier: bez duplikatów w cache strony
  }
  if (req.headers.has('range') || /\.(mp4|webm|mov|pdf)$/i.test(url.pathname)) return;   // filmy/PDF — sieć
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html'))
    return e.respondWith(htmlNetworkFirst(e));
  if (req.destination === 'image' || /\.(webp|jpe?g|png|gif|svg|avif|ico)$/i.test(url.pathname))
    return e.respondWith(cacheFirst(e, IMGS, MAX_IMGS));
  if (/\.(css|js|webmanifest|woff2?|ttf)$/i.test(url.pathname))
    return e.respondWith(staleWhileRevalidate(e));
});

self.addEventListener('message', e => { if (e.data === 'skipWaiting') self.skipWaiting(); });

// ---- powiadomienia push (Worker eve-push) ----
const PUSH = __PUSH__;
const SOCIAL = /^(www\.|m\.|web\.)?(facebook\.com|fb\.com|fb\.watch|instagram\.com)$/i;   // posty Eve na FB/IG (te same hosty co LINK_HOSTS w Workerze)
self.addEventListener('push', e => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (_) { d = {body: e.data ? e.data.text() : ''}; }
  const url = (() => { try { const x = new URL(d.url || BASE, BASE); return x.origin === self.location.origin || (x.protocol === 'https:' && SOCIAL.test(x.hostname)) ? x.href : BASE; } catch (_) { return BASE; } })();
  e.waitUntil(self.registration.showNotification(d.title || 'Eve', {
    body: d.body || '', icon: u('assets/pwa/icon-192.png'), badge: u('assets/pwa/badge-96.png'),
    tag: d.tag || undefined, renotify: !!d.tag, data: {url}, lang: d.lang || undefined,
  }));
});
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || BASE;
  e.waitUntil((async () => {
    if (new URL(url).origin !== self.location.origin) return self.clients.openWindow(url);   // FB/IG: aplikacja/przeglądarka, nie okno apki Eve
    const wins = await self.clients.matchAll({type: 'window', includeUncontrolled: true});
    for (const w of wins) if (w.url.split('#')[0] === url.split('#')[0] && 'focus' in w) return w.focus();
    for (const w of wins) if (w.url.startsWith(BASE) && 'navigate' in w) { try { await w.focus(); return await w.navigate(url); } catch (_) {} }
    return self.clients.openWindow(url);
  })());
});
self.addEventListener('pushsubscriptionchange', e => {
  if (!PUSH || !PUSH.api) return;
  const old = e.oldSubscription;
  e.waitUntil((async () => {
    const opts = (old && old.options) || {userVisibleOnly: true, applicationServerKey: Uint8Array.from(atob(PUSH.key.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0))};
    const sub = e.newSubscription || await self.registration.pushManager.subscribe(opts);
    await fetch(PUSH.api + '/subscribe', {method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({subscription: sub.toJSON(), old_endpoint: old && old.endpoint})});
  })().catch(() => {}));
});
'''

PWA_JS = r'''/* Apka Eve (PWA): rejestracja service workera + przycisk instalacji. GENEROWANY przez scripts/pwa.py. */
(function () {
  var me = document.currentScript, lang = (me && me.dataset.lang) || 'pl';
  var root = me ? me.src.replace(/js\/pwa\.js(\?.*)?$/, '') : '/';
  var T = __TXT__, t = T[lang] || T.en;
  var KEY = 'eve-pwa-dismissed', IOSKEY = 'eve-pwa-ios-hint';
  var standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  function gc(path, title) {   // zdarzenie GoatCounter (count.js ładuje się async — ponawiamy chwilę)
    var n = 0; (function go() {
      if (window.goatcounter && window.goatcounter.count) { try { window.goatcounter.count({path: path, title: title + ' (' + lang + ')', event: true}); } catch (_) {} }
      else if (n++ < 20) setTimeout(go, 500);
    })();
  }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (_) {} }
  function dismissed(k) {   // stary znacznik '1' wygasł — po odinstalowaniu pasek wraca od razu
    var v = store(k); if (!v || v === '1') return false;
    var ts = +v; return !!(ts && Date.now() - ts < 14 * 864e5);
  }
  function dismiss(k) { store(k, String(Date.now())); }

  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    addEventListener('load', function () { navigator.serviceWorker.register(root + 'sw.js', {scope: root}).catch(function () {}); });
  }
  if (standalone) {
    document.documentElement.classList.add('pwa');
    // gry (/gry/) w tym samym oknie apki — na iPhonie „nowa karta” = Safari, z osobną pamięcią offline
    addEventListener('DOMContentLoaded', function () {
      [].forEach.call(document.querySelectorAll('a[target="_blank"][href*="/gry/"]'), function (a) {
        try { if (new URL(a.href).origin === location.origin) a.removeAttribute('target'); } catch (_) {}
      });
    });
    try { if (!sessionStorage.getItem('eve-pwa-launch')) { sessionStorage.setItem('eve-pwa-launch', '1'); gc('pwa-launch', 'PWA: start z ekranu telefonu'); } } catch (_) {}
  }

  var SHARE = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" style="vertical-align:-2px"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M12 15V3m0 0L8 7m4-4 4 4M6 11H5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-8a1 1 0 0 0-1-1h-1"/></svg>';
  var CSS = '.eve-pwa{position:fixed;left:50%;bottom:calc(14px + env(safe-area-inset-bottom));transform:translate(-50%,140%);z-index:998;width:min(92vw,430px);display:flex;flex-wrap:wrap;align-items:center;gap:10px 12px;padding:12px 12px 12px 14px;background:rgba(12,7,8,.96);border:1px solid rgba(201,163,91,.55);box-shadow:0 14px 50px rgba(0,0,0,.6);color:#f3ece0;font:500 13px/1.4 Inter,system-ui,sans-serif;transition:transform .45s cubic-bezier(.2,.8,.2,1);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}'
    + '.eve-pwa.on{transform:translate(-50%,0)}.eve-pwa img{width:44px;height:44px;border-radius:50%;flex:none}.eve-pwa .tx{flex:1;min-width:0;font-size:12.5px}.eve-pwa .tx b{color:#e8cf96;font-weight:500}.eve-pwa .tt{font:italic 400 17px/1.2 "Playfair Display",Georgia,serif;color:#e8cf96;margin-bottom:2px}'
    + '.eve-pwa .go{flex:none;background:#c9a35b;color:#0c0708;border:0;order:3;flex:1 1 100%;padding:12px;font:600 11px/1.2 Inter,system-ui,sans-serif;letter-spacing:.16em;text-transform:uppercase;cursor:pointer}.eve-pwa .x{flex:none;align-self:flex-start;background:none;border:0;color:#b9a89a;font-size:20px;line-height:1;padding:0 2px;cursor:pointer}'
    + '@media (prefers-reduced-motion:reduce){.eve-pwa{transition:none}}';
  function bar(inner, onGo, onClose) {
    var s = document.createElement('style'); s.textContent = CSS; document.head.appendChild(s);
    var b = document.createElement('div'); b.className = 'eve-pwa'; b.setAttribute('role', 'dialog'); b.setAttribute('aria-label', t.install);
    b.innerHTML = '<img src="' + root + 'assets/pwa/icon-192.png" alt="">' + inner + '<button class="x" type="button" aria-label="' + t.close + '">×</button>';
    document.body.appendChild(b); requestAnimationFrame(function () { requestAnimationFrame(function () { b.classList.add('on'); }); });
    var hide = function () { b.classList.remove('on'); setTimeout(function () { b.remove(); }, 500); };
    b.querySelector('.x').onclick = function () { if (onClose) onClose(); else { dismiss(KEY); gc('pwa-prompt-dismissed', 'PWA: zamknięto zachętę'); } hide(); };
    if (onGo) b.querySelector('.go').onclick = function () { onGo(hide); };
    return b;
  }
  // ---- powiadomienia push: przycisk „Włącz powiadomienia” (tylko gdy PUSH_API ustawione w scripts/pwa.py) ----
  var P = __PUSH__, PKEY = 'eve-push-dismissed', iosDev = /iPhone|iPad|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var pushable = !!(P && P.api && P.key && 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window && location.protocol !== 'file:') && (!iosDev || standalone);   // iOS: tylko apka z ekranu (iOS 16.4+)
  function keyBytes(k) { var s = atob(k.replace(/-/g, '+').replace(/_/g, '/')), a = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) a[i] = s.charCodeAt(i); return a; }
  function pushSubscribe(done) {   // wołać prosto z kliknięcia (Safari wymaga gestu)
    var perm = Notification.permission === 'granted' ? Promise.resolve('granted') : Promise.resolve(Notification.requestPermission());
    perm.then(function (p) {
      if (p !== 'granted') { store(PKEY, String(Date.now())); gc('push-denied', 'Push: odmowa'); return done && done(false); }
      return navigator.serviceWorker.ready.then(function (reg) {
        return reg.pushManager.getSubscription().then(function (s) { return s || reg.pushManager.subscribe({userVisibleOnly: true, applicationServerKey: keyBytes(P.key)}); });
      }).then(function (s) {
        return fetch(P.api + '/subscribe', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({subscription: s.toJSON(), lang: lang})});
      }).then(function (r) {
        if (!r.ok) throw new Error('subscribe ' + r.status);
        store('eve-push-on', '1'); gc('push-subscribed', 'Push: włączone'); done && done(true);
      });
    }).catch(function () { done && done(false); });
  }
  if (pushable) {
    var pv = 0; try { pv = +sessionStorage.getItem('eve-pv') + 1; sessionStorage.setItem('eve-pv', String(pv)); } catch (_) {}
    addEventListener('DOMContentLoaded', function () {   // opcjonalne przyciski na stronie: <button data-eve-push hidden>
      if (Notification.permission === 'denied') return;
      navigator.serviceWorker.ready.then(function (reg) { return reg.pushManager.getSubscription(); }).then(function (s) {
        if (s) return;   // już zasubskrybowane — zostaw ukryte
        [].forEach.call(document.querySelectorAll('[data-eve-push]'), function (el) {
          el.hidden = false;
          el.addEventListener('click', function () {
            pushSubscribe(function (ok) {
              if (ok) [].forEach.call(document.querySelectorAll('[data-eve-push]'), function (b) { b.hidden = true; });
            });
          });
        });
      }).catch(function () {});
    });
    var d = +store(PKEY) || 0;
    if (Notification.permission !== 'denied' && !(d && Date.now() - d < 30 * 864e5) && (standalone || pv >= 2)) {   // w przeglądarce dopiero od 2. strony w wizycie
      setTimeout(function () {
        navigator.serviceWorker.ready.then(function (reg) { return reg.pushManager.getSubscription(); }).then(function (s) {
          if (s || document.querySelector('.eve-pwa')) return;
          bar('<div class="tx"><div class="tt">' + t.push_t + '</div>' + t.push + '</div><button class="go" type="button">' + t.push_on + '</button>', function (hide) {
            pushSubscribe(function (ok) {
              var b = document.querySelector('.eve-pwa .tx'); if (ok && b) { b.innerHTML = '<div class="tt">' + t.push_ok + '</div>'; var g = document.querySelector('.eve-pwa .go'); if (g) g.remove(); setTimeout(hide, 2500); } else hide();
            });
          }, function () { store(PKEY, String(Date.now())); gc('push-optin-closed', 'Push: zamknięto'); });
          gc('push-optin-shown', 'Push: pokazano przycisk');
        }).catch(function () {});
      }, standalone ? 4000 : 6000);
    }
  }
  function hookInstall(onClick) {   // <button data-eve-install hidden> — znacznik dodaje Strona (stopka); tu tylko pokazać / obsłużyć
    function apply() {
      [].forEach.call(document.querySelectorAll('[data-eve-install]'), function (el) {
        el.hidden = false;
        if (el.getAttribute('data-eve-install-on') === '1') return;
        el.setAttribute('data-eve-install-on', '1');
        el.addEventListener('click', function (ev) {
          ev.preventDefault();
          if (!el.getAttribute('data-goatcounter-click')) gc('pwa-install-button-click', 'PWA: kliknięto przycisk instalacji');
          onClick();
        });
      });
    }
    if (document.readyState === 'loading') addEventListener('DOMContentLoaded', apply);
    else apply();
  }
  function hideInstallHooks() {
    [].forEach.call(document.querySelectorAll('[data-eve-install]'), function (el) { el.hidden = true; });
  }

  if (standalone) return;

  // Android / Chrome / Edge: natywne okno instalacji. beforeinstallprompt leci tylko, gdy apka NIE jest zainstalowana —
  // po odinstalowaniu pasek i przycisk wracają. Zamknięcie / odmowa: 14 dni (nie blokujemy na stałe).
  var deferred = null;
  addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault(); deferred = e;
    hookInstall(function () {
      if (!deferred || typeof deferred.prompt !== 'function') return;
      deferred.prompt();
      if (deferred.userChoice) deferred.userChoice.then(function (c) {
        if (c.outcome === 'accepted') gc('pwa-prompt-accepted', 'PWA: zaakceptowano instalację');
        else { dismiss(KEY); gc('pwa-prompt-declined', 'PWA: odrzucono instalację'); }
        deferred = null;
      }).catch(function () { deferred = null; });
    });
    if (dismissed(KEY) || document.querySelector('.eve-pwa')) return;
    setTimeout(function () {
      if (!deferred || document.querySelector('.eve-pwa')) return;
      bar('<div class="tx"><div class="tt">Eve.</div>' + t.sub + '</div><button class="go" type="button">' + t.install + '</button>', function (hide) {
        if (!deferred) return hide();
        deferred.prompt();
        deferred.userChoice.then(function (c) {
          if (c.outcome === 'accepted') gc('pwa-prompt-accepted', 'PWA: zaakceptowano instalację');
          else { dismiss(KEY); gc('pwa-prompt-declined', 'PWA: odrzucono instalację'); }
          deferred = null; hide();
        });
      }, function () { dismiss(KEY); gc('pwa-prompt-dismissed', 'PWA: zamknięto zachętę'); });
      gc('pwa-prompt-shown', 'PWA: pokazano przycisk instalacji');
    }, 2500);
  });
  addEventListener('appinstalled', function () {
    deferred = null;
    hideInstallHooks();
    gc('pwa-appinstalled', 'PWA: apka zainstalowana');
    var b = document.querySelector('.eve-pwa'); if (b) b.remove();
  });

  // iPhone / iPad w Safari: podpowiedź „Udostępnij → Dodaj do ekranu początkowego”
  var ua = navigator.userAgent, ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var safari = ios && /Safari/.test(ua) && !/CriOS|FxiOS|EdgiOS|OPiOS|GSA|Instagram|FBAN|FBAV/.test(ua);
  if (safari) {
    hookInstall(function () {
      if (document.querySelector('.eve-pwa')) return;
      bar('<div class="tx"><div class="tt">' + t.ios_t + '</div>' + t.ios.replace('{share}', SHARE) + '</div>');
      gc('pwa-ios-hint-shown', 'PWA: pokazano podpowiedź iOS');
    });
    if (!dismissed(IOSKEY) && !dismissed(KEY)) {
      setTimeout(function () {
        if (document.querySelector('.eve-pwa')) return;
        dismiss(IOSKEY);
        bar('<div class="tx"><div class="tt">' + t.ios_t + '</div>' + t.ios.replace('{share}', SHARE) + '</div>', null, function () { dismiss(KEY); gc('pwa-prompt-dismissed', 'PWA: zamknięto zachętę'); });
        gc('pwa-ios-hint-shown', 'PWA: pokazano podpowiedź iOS');
      }, 3500);
    }
  }
})();
'''

def build_pwa(ROOT, write, theme=None):
    """Generuje pliki PWA. write(rel, content) — funkcja zapisu z build.py."""
    make_icons(ROOT)
    for l in LANGS: write(pre(l) + 'offline.html', offline_page(l))
    js_txt = {l: {k: TXT[l][k] for k in ('install', 'sub', 'ios_t', 'ios', 'close', 'push_t', 'push', 'push_on', 'push_ok')} for l in LANGS}
    write('js/pwa.js', PWA_JS.replace('__TXT__', json.dumps(js_txt, ensure_ascii=False)).replace('__PUSH__', json.dumps(push_cfg())))
    write('manifest.webmanifest', manifest(ROOT))
    icons = [PWA_DIR + f for f in ('icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'apple-touch-icon.png', 'badge-96.png', 'badge-72.png')]
    required = ['./'] + [pre(l) for l in LANGS if l != 'pl'] + [pre(l) + 'offline.html' for l in LANGS] \
               + ['css/eve.css'] + ([f'css/themes/{theme}.css'] if theme else []) + ['js/eve.js', 'js/pwa.js', 'js/ads.js', 'manifest.webmanifest', ICON_SRC] + icons
    optional = [path_creators(l) for l in LANGS] + ['linki/', 'komiks/', 'blog/']
    ver = _h(ROOT, [r for r in required if not r.endswith('/')] + [pre(l) + 'index.html' for l in LANGS])
    write('sw.js', SW_TEMPLATE.replace('__VERSION__', ver).replace('__REQUIRED__', json.dumps(required)).replace('__OPTIONAL__', json.dumps(optional)).replace('__PUSH__', json.dumps(push_cfg())))
