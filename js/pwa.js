/* Apka Eve (PWA): rejestracja service workera + przycisk instalacji. GENEROWANY przez scripts/pwa.py. */
(function () {
  var me = document.currentScript, lang = (me && me.dataset.lang) || 'pl';
  var root = me ? me.src.replace(/js\/pwa\.js(\?.*)?$/, '') : '/';
  var T = {"pl": {"install": "Zainstaluj apkę Eve", "sub": "Gry, komiksy i nowe wpisy prosto z ekranu telefonu.", "ios_t": "Eve jako apka", "ios": "Dotknij <b>Udostępnij</b> {share}, a potem <b>„Dodaj do ekranu początkowego”</b>.", "close": "Zamknij"}, "en": {"install": "Install the Eve app", "sub": "Games, comics and new posts right from your home screen.", "ios_t": "Get the Eve app", "ios": "Tap <b>Share</b> {share}, then <b>“Add to Home Screen”</b>.", "close": "Close"}, "es": {"install": "Instalar la app de Eve", "sub": "Juegos, cómics y nuevas entradas desde tu pantalla de inicio.", "ios_t": "Eve como app", "ios": "Toca <b>Compartir</b> {share} y luego <b>«Añadir a pantalla de inicio»</b>.", "close": "Cerrar"}, "pt": {"install": "Instalar o app da Eve", "sub": "Jogos, quadrinhos e novos posts direto da tela inicial.", "ios_t": "Eve como app", "ios": "Toque em <b>Compartilhar</b> {share} e depois em <b>“Adicionar à Tela de Início”</b>.", "close": "Fechar"}, "it": {"install": "Installa l’app di Eve", "sub": "Giochi, fumetti e nuovi articoli dalla schermata Home.", "ios_t": "Eve come app", "ios": "Tocca <b>Condividi</b> {share}, poi <b>«Aggiungi alla schermata Home»</b>.", "close": "Chiudi"}, "ja": {"install": "Eveアプリをインストール", "sub": "ゲーム、コミック、新着記事をホーム画面から。", "ios_t": "Eveをアプリで", "ios": "<b>共有</b> {share} をタップして<b>「ホーム画面に追加」</b>を選んでください。", "close": "閉じる"}, "zh": {"install": "安装 Eve 应用", "sub": "游戏、漫画和最新文章，从主屏幕直达。", "ios_t": "把 Eve 装成应用", "ios": "点击<b>分享</b> {share}，然后选择<b>“添加到主屏幕”</b>。", "close": "关闭"}}, t = T[lang] || T.en;
  var KEY = 'eve-pwa-dismissed', IOSKEY = 'eve-pwa-ios-hint';
  var standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  function gc(path, title) {   // zdarzenie GoatCounter (count.js ładuje się async — ponawiamy chwilę)
    var n = 0; (function go() {
      if (window.goatcounter && window.goatcounter.count) { try { window.goatcounter.count({path: path, title: title + ' (' + lang + ')', event: true}); } catch (_) {} }
      else if (n++ < 20) setTimeout(go, 500);
    })();
  }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (_) {} }

  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    addEventListener('load', function () { navigator.serviceWorker.register(root + 'sw.js', {scope: root}).catch(function () {}); });
  }
  if (standalone) {
    document.documentElement.classList.add('pwa');
    try { if (!sessionStorage.getItem('eve-pwa-launch')) { sessionStorage.setItem('eve-pwa-launch', '1'); gc('pwa-launch', 'PWA: start z ekranu telefonu'); } } catch (_) {}
    return;
  }

  var SHARE = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" style="vertical-align:-2px"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M12 15V3m0 0L8 7m4-4 4 4M6 11H5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-8a1 1 0 0 0-1-1h-1"/></svg>';
  var CSS = '.eve-pwa{position:fixed;left:50%;bottom:calc(14px + env(safe-area-inset-bottom));transform:translate(-50%,140%);z-index:998;width:min(92vw,430px);display:flex;flex-wrap:wrap;align-items:center;gap:10px 12px;padding:12px 12px 12px 14px;background:rgba(12,7,8,.96);border:1px solid rgba(201,163,91,.55);box-shadow:0 14px 50px rgba(0,0,0,.6);color:#f3ece0;font:500 13px/1.4 Inter,system-ui,sans-serif;transition:transform .45s cubic-bezier(.2,.8,.2,1);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}'
    + '.eve-pwa.on{transform:translate(-50%,0)}.eve-pwa img{width:44px;height:44px;border-radius:50%;flex:none}.eve-pwa .tx{flex:1;min-width:0;font-size:12.5px}.eve-pwa .tx b{color:#e8cf96;font-weight:500}.eve-pwa .tt{font:italic 400 17px/1.2 "Playfair Display",Georgia,serif;color:#e8cf96;margin-bottom:2px}'
    + '.eve-pwa .go{flex:none;background:#c9a35b;color:#0c0708;border:0;order:3;flex:1 1 100%;padding:12px;font:600 11px/1.2 Inter,system-ui,sans-serif;letter-spacing:.16em;text-transform:uppercase;cursor:pointer}.eve-pwa .x{flex:none;align-self:flex-start;background:none;border:0;color:#b9a89a;font-size:20px;line-height:1;padding:0 2px;cursor:pointer}'
    + '@media (prefers-reduced-motion:reduce){.eve-pwa{transition:none}}';
  function bar(inner, onGo) {
    var s = document.createElement('style'); s.textContent = CSS; document.head.appendChild(s);
    var b = document.createElement('div'); b.className = 'eve-pwa'; b.setAttribute('role', 'dialog'); b.setAttribute('aria-label', t.install);
    b.innerHTML = '<img src="' + root + 'assets/pwa/icon-192.png" alt="">' + inner + '<button class="x" type="button" aria-label="' + t.close + '">×</button>';
    document.body.appendChild(b); requestAnimationFrame(function () { requestAnimationFrame(function () { b.classList.add('on'); }); });
    var hide = function () { b.classList.remove('on'); setTimeout(function () { b.remove(); }, 500); };
    b.querySelector('.x').onclick = function () { store(KEY, '1'); gc('pwa-prompt-dismissed', 'PWA: zamknięto zachętę'); hide(); };
    if (onGo) b.querySelector('.go').onclick = function () { onGo(hide); };
    return b;
  }
  if (store(KEY)) return;

  // Android / Chrome / Edge: natywne okno instalacji
  var deferred = null;
  addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault(); deferred = e;
    if (document.querySelector('.eve-pwa')) return;
    setTimeout(function () {
      bar('<div class="tx"><div class="tt">Eve.</div>' + t.sub + '</div><button class="go" type="button">' + t.install + '</button>', function (hide) {
        if (!deferred) return hide();
        deferred.prompt();
        deferred.userChoice.then(function (c) {
          if (c.outcome === 'accepted') gc('pwa-prompt-accepted', 'PWA: zaakceptowano instalację');
          else { store(KEY, '1'); gc('pwa-prompt-declined', 'PWA: odrzucono instalację'); }
          deferred = null; hide();
        });
      });
      gc('pwa-prompt-shown', 'PWA: pokazano przycisk instalacji');
    }, 2500);
  });
  addEventListener('appinstalled', function () { store(KEY, '1'); gc('pwa-appinstalled', 'PWA: apka zainstalowana'); var b = document.querySelector('.eve-pwa'); if (b) b.remove(); });

  // iPhone / iPad w Safari: jednorazowa podpowiedź „Udostępnij → Dodaj do ekranu początkowego”
  var ua = navigator.userAgent, ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var safari = ios && /Safari/.test(ua) && !/CriOS|FxiOS|EdgiOS|OPiOS|GSA|Instagram|FBAN|FBAV/.test(ua);
  if (safari && !store(IOSKEY)) {
    setTimeout(function () {
      store(IOSKEY, '1');
      bar('<div class="tx"><div class="tt">' + t.ios_t + '</div>' + t.ios.replace('{share}', SHARE) + '</div>');
      gc('pwa-ios-hint-shown', 'PWA: pokazano podpowiedź iOS');
    }, 3500);
  }
})();
