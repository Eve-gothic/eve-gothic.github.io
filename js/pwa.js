/* Apka Eve (PWA): rejestracja service workera + przycisk instalacji. GENEROWANY przez scripts/pwa.py. */
(function () {
  var me = document.currentScript, lang = (me && me.dataset.lang) || 'pl';
  var root = me ? me.src.replace(/js\/pwa\.js(\?.*)?$/, '') : '/';
  var T = {"pl": {"install": "Zainstaluj apkę Eve", "sub": "Gry, komiksy i nowe wpisy prosto z ekranu telefonu.", "ios_t": "Eve jako apka", "ios": "Dotknij <b>Udostępnij</b> {share}, a potem <b>„Dodaj do ekranu początkowego”</b>.", "close": "Zamknij", "push_t": "Nowości od Eve", "push": "Daj znać, gdy pojawi się nowy wpis, komiks albo gra.", "push_on": "Włącz powiadomienia", "push_ok": "Powiadomienia włączone. Do zobaczenia!"}, "en": {"install": "Install the Eve app", "sub": "Games, comics and new posts right from your home screen.", "ios_t": "Get the Eve app", "ios": "Tap <b>Share</b> {share}, then <b>“Add to Home Screen”</b>.", "close": "Close", "push_t": "News from Eve", "push": "Get a heads-up when a new post, comic or game drops.", "push_on": "Turn on notifications", "push_ok": "Notifications are on. See you soon!"}, "es": {"install": "Instalar la app de Eve", "sub": "Juegos, cómics y nuevas entradas desde tu pantalla de inicio.", "ios_t": "Eve como app", "ios": "Toca <b>Compartir</b> {share} y luego <b>«Añadir a pantalla de inicio»</b>.", "close": "Cerrar", "push_t": "Novedades de Eve", "push": "Te avisamos cuando haya una entrada, un cómic o un juego nuevo.", "push_on": "Activar notificaciones", "push_ok": "Notificaciones activadas. ¡Hasta pronto!"}, "pt": {"install": "Instalar o app da Eve", "sub": "Jogos, quadrinhos e novos posts direto da tela inicial.", "ios_t": "Eve como app", "ios": "Toque em <b>Compartilhar</b> {share} e depois em <b>“Adicionar à Tela de Início”</b>.", "close": "Fechar", "push_t": "Novidades da Eve", "push": "Receba um aviso quando sair um post, quadrinho ou jogo novo.", "push_on": "Ativar notificações", "push_ok": "Notificações ativadas. Até logo!"}, "it": {"install": "Installa l’app di Eve", "sub": "Giochi, fumetti e nuovi articoli dalla schermata Home.", "ios_t": "Eve come app", "ios": "Tocca <b>Condividi</b> {share}, poi <b>«Aggiungi alla schermata Home»</b>.", "close": "Chiudi", "push_t": "Novità da Eve", "push": "Ti avvisiamo quando esce un nuovo articolo, fumetto o gioco.", "push_on": "Attiva le notifiche", "push_ok": "Notifiche attive. A presto!"}, "ja": {"install": "Eveアプリをインストール", "sub": "ゲーム、コミック、新着記事をホーム画面から。", "ios_t": "Eveをアプリで", "ios": "<b>共有</b> {share} をタップして<b>「ホーム画面に追加」</b>を選んでください。", "close": "閉じる", "push_t": "Eveからのお知らせ", "push": "新しい記事・コミック・ゲームが公開されたらお知らせします。", "push_on": "通知をオンにする", "push_ok": "通知をオンにしました。またね！"}, "zh": {"install": "安装 Eve 应用", "sub": "游戏、漫画和最新文章，从主屏幕直达。", "ios_t": "把 Eve 装成应用", "ios": "点击<b>分享</b> {share}，然后选择<b>“添加到主屏幕”</b>。", "close": "关闭", "push_t": "Eve 的新消息", "push": "有新文章、漫画或游戏时第一时间通知你。", "push_on": "开启通知", "push_ok": "通知已开启。回头见！"}}, t = T[lang] || T.en;
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
  var P = {"api": "https://eve-push.wodzu2207.workers.dev", "key": "BHjWY6NROqFXgTK2f8eUzoBvYPcnpEugI1et9AQMxG2Ga6csvtqX9PI-omwT-d1So85VOFr2hiQazWcyt_aRj1U"}, PKEY = 'eve-push-dismissed', iosDev = /iPhone|iPad|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
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
