# -*- coding: utf-8 -*-
"""Reklama własna (house ads) usługi „aplikacja dla twórców” na stronie Eve (18.11.2026).
Zasada: fani Eve są najważniejsi.
 • baner: najwyżej JEDEN na stronę — strona główna (dół), koniec wpisu bloga, koniec każdego komiksu;
   NIE w galerii/sesji, NIE w środku wpisu, NIE na podstronie dla twórców, NIE na /linki/;
 • okienko (<dialog>): tylko po kliknięciu banera lub linku w stopce — nigdy samo; bez JS link prowadzi na podstronę;
 • pasek przypomnienia: tylko na stronach komiksów, po dojściu do ostatniej strony, najwyżej raz na 30 dni (localStorage);
   nie zasłania paska instalacji apki (.eve-pwa z js/pwa.js) — staje nad nim.
 • analityka: tylko kliknięcia w GoatCounter (ad-banner-click, ad-modal-more, ad-bar-click, ad-bar-close).
Teksty: scripts/ads_i18n.py. Plik js/ads.js jest GENEROWANY (build_ads_js) — zmiany wprowadzaj tutaj."""
import json, html
from ads_i18n import AD

esc = lambda s: html.escape(str(s), quote=True)

def ad_banner(lang, r, href, kind):
    """Baner HTML (stała wysokość — bez przesunięć układu). href = adres podstrony dla twórców."""
    a = AD[lang]
    return (f'<aside class="hads" aria-label="{esc(a["label"])}">'
            f'<a class="hads-in" href="{esc(href)}" data-ad="banner" data-ad-kind="{kind}">'
            f'<span class="hads-lbl">{a["label"]}</span>'
            f'<span class="hads-ph" aria-hidden="true"><img src="{r}assets/pwa/icon-192.png" alt="" width="40" height="40" loading="lazy" decoding="async"><i></i><i></i><i></i></span>'
            f'<span class="hads-tx"><b>{a["title"]}</b><span>{a["sub"]}</span></span>'
            f'<span class="hads-go">{a["cta"]} →</span></a></aside>')

def ad_script(lang, r, href):
    return f'<script src="{r}js/ads.js" data-lang="{lang}" data-url="{esc(href)}" defer></script>'

ADS_JS = r'''/* Eve — reklama własna usługi (baner -> okienko, pasek po komiksie). GENEROWANY przez scripts/ads.py. */
(function () {
  var me = document.currentScript; if (!me) return;
  var lang = me.dataset.lang || 'pl', T = __TXT__, t = T[lang] || T.en;
  var url = new URL(me.dataset.url || '/', location.href).href, KEY = 'eve-ad-bar', DAY = 864e5;
  function gc(path, title) {   // zdarzenie GoatCounter jak w js/pwa.js (count.js ładuje się async)
    var n = 0; (function go() {
      if (window.goatcounter && window.goatcounter.count) { try { window.goatcounter.count({path: path, title: title + ' — ' + location.pathname + ' (' + lang + ')', event: true}); } catch (_) {} }
      else if (n++ < 20) setTimeout(go, 500);
    })();
  }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (_) {} }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }

  // ── okienko (tylko po kliknięciu) ──
  var dlg = null, opener = null, canDialog = typeof HTMLDialogElement === 'function' && 'showModal' in HTMLDialogElement.prototype;
  function build() {
    dlg = el('dialog', 'hadm'); dlg.setAttribute('aria-labelledby', 'hadm-t'); dlg.setAttribute('aria-describedby', 'hadm-d');
    dlg.innerHTML = '<button class="hadm-x" type="button" aria-label="' + esc(t.close) + '">×</button>'
      + '<span class="hads-lbl">' + esc(t.label) + '</span><h2 id="hadm-t">' + esc(t.m_title) + '</h2>'
      + '<div id="hadm-d">' + t.m_body.map(function (s) { return '<p>' + esc(s) + '</p>'; }).join('') + '</div>'
      + '<div class="hadm-b"><a class="cta fill" href="' + esc(url) + '">' + esc(t.more) + ' →</a>'
      + '<button class="cta" type="button" data-close>' + esc(t.close) + '</button></div>';
    document.body.appendChild(dlg);
    var close = function () { dlg.close(); };
    dlg.querySelector('.hadm-x').onclick = close; dlg.querySelector('[data-close]').onclick = close;
    dlg.querySelector('.hadm-b a').addEventListener('click', function () { gc('ad-modal-more', 'House ad: okienko -> zobacz więcej'); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) close(); });   // klik w tło
    dlg.addEventListener('keydown', function (e) {   // pułapka fokusu (Tab / Shift+Tab w obrębie okienka)
      if (e.key !== 'Tab') return;
      var f = dlg.querySelectorAll('a[href],button'), first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    dlg.addEventListener('close', function () { document.documentElement.classList.remove('hadm-open'); if (opener && opener.focus) opener.focus(); });
  }
  function openModal(from) {
    if (!canDialog) return false;
    if (!dlg) build();
    if (dlg.open) return true;
    opener = from || document.activeElement;
    try { dlg.showModal(); } catch (_) { return false; }
    document.documentElement.classList.add('hadm-open');
    dlg.querySelector('.hadm-b a').focus();
    return true;
  }
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;   // nowa karta itp. = zwykły link
    var a = e.target.closest && e.target.closest('a[data-ad="banner"], footer a.forcr');
    if (!a) return;
    if (openModal(a)) {
      e.preventDefault();
      if (a.dataset.ad === 'banner') gc('ad-banner-click', 'House ad: baner (' + (a.dataset.adKind || '') + ')');
    }
  });

  // ── pasek przypomnienia: tylko komiksy, po ostatniej stronie, raz na 30 dni ──
  var imgs = document.querySelectorAll('.reader .kpage img'), lastImg = imgs[imgs.length - 1];
  var seen = +store(KEY) || 0;
  if (!lastImg || !('IntersectionObserver' in window) || Date.now() - seen < 30 * DAY) return;
  var io = new IntersectionObserver(function (en) {
    if (!en.some(function (x) { return x.isIntersecting; })) return;
    io.disconnect(); setTimeout(showBar, 700);
  }, {threshold: 0.6});
  io.observe(lastImg);
  function showBar() {
    if (document.querySelector('.hadbar')) return;
    store(KEY, String(Date.now()));
    var b = el('div', 'hadbar'); b.setAttribute('role', 'region'); b.setAttribute('aria-label', t.label);
    b.innerHTML = '<span class="hads-lbl">' + esc(t.label) + '</span><p>' + esc(t.bar) + '</p>'
      + '<a class="go" href="' + esc(url) + '">' + esc(t.bar_cta) + ' →</a><button class="x" type="button" aria-label="' + esc(t.close) + '">×</button>';
    document.body.appendChild(b);
    var place = function () {   // nad paskiem instalacji apki (.eve-pwa), jeśli jest widoczny
      var p = document.querySelector('.eve-pwa.on');
      b.style.bottom = p ? 'calc(' + (p.offsetHeight + 26) + 'px + env(safe-area-inset-bottom))' : '';
    };
    place();
    var mo = new MutationObserver(place); mo.observe(document.body, {childList: true, subtree: true, attributes: true, attributeFilter: ['class']});
    requestAnimationFrame(function () { requestAnimationFrame(function () { b.classList.add('on'); }); });
    var hide = function () { mo.disconnect(); b.classList.remove('on'); setTimeout(function () { b.remove(); }, 400); };
    b.querySelector('.x').onclick = function () { gc('ad-bar-close', 'House ad: pasek -> zamknięto'); hide(); };
    b.querySelector('.go').addEventListener('click', function (e) {
      gc('ad-bar-click', 'House ad: pasek -> klik');
      if (e.button === 0 && !e.metaKey && !e.ctrlKey && !e.shiftKey && openModal(lastImg.closest('button') || lastImg)) { e.preventDefault(); e.stopPropagation(); hide(); }
    });
  }
})();
'''

def build_ads_js(write):
    txt = {l: AD[l] for l in AD}
    write('js/ads.js', ADS_JS.replace('__TXT__', json.dumps(txt, ensure_ascii=False)))
