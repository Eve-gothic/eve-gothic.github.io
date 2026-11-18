/* Service worker strony Eve — GENEROWANY przez scripts/pwa.py (build.py). Nie edytuj ręcznie. */
const VERSION = '3e037b3f18';
const SHELL = 'eve-shell-' + VERSION, PAGES = 'eve-pages-v1', IMGS = 'eve-img-v1', FONTS = 'eve-fonts-v1';
const KEEP = [SHELL, PAGES, IMGS, FONTS];
const MAX_PAGES = 60, MAX_IMGS = 150, MAX_FONTS = 40;
const BASE = new URL('./', self.location).href;               // korzeń strony (scope)
const REQUIRED = ["./", "en/", "es/", "pt/", "it/", "ja/", "zh/", "offline.html", "en/offline.html", "es/offline.html", "pt/offline.html", "it/offline.html", "ja/offline.html", "zh/offline.html", "css/eve.css", "js/eve.js", "js/pwa.js", "js/ads.js", "manifest.webmanifest", "assets/img/eve-avatar.webp", "assets/pwa/icon-192.png", "assets/pwa/icon-512.png", "assets/pwa/icon-maskable-512.png", "assets/pwa/apple-touch-icon.png"];                                 // app shell — musi się pobrać
const OPTIONAL = ["dla-tworcow/", "en/for-creators/", "es/for-creators/", "pt/for-creators/", "it/for-creators/", "ja/for-creators/", "zh/for-creators/", "linki/", "komiks/", "blog/"];                                 // mile widziane — 404 nie psuje instalacji
const LANGS = ['en', 'es', 'pt', 'it', 'ja', 'zh'];
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
const PUSH = {"api": "https://eve-push.wodzu2207.workers.dev", "key": "BHjWY6NROqFXgTK2f8eUzoBvYPcnpEugI1et9AQMxG2Ga6csvtqX9PI-omwT-d1So85VOFr2hiQazWcyt_aRj1U"};
self.addEventListener('push', e => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (_) { d = {body: e.data ? e.data.text() : ''}; }
  const url = (() => { try { const x = new URL(d.url || BASE, BASE); return x.origin === self.location.origin ? x.href : BASE; } catch (_) { return BASE; } })();
  e.waitUntil(self.registration.showNotification(d.title || 'Eve', {
    body: d.body || '', icon: u('assets/pwa/icon-192.png'), badge: u('assets/pwa/icon-192.png'),
    tag: d.tag || undefined, renotify: !!d.tag, data: {url}, lang: d.lang || undefined,
  }));
});
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || BASE;
  e.waitUntil((async () => {
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
