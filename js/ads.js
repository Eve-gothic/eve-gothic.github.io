/* Eve — reklama własna usługi (baner -> okienko, pasek po komiksie). GENEROWANY przez scripts/ads.py. */
(function () {
  var me = document.currentScript; if (!me) return;
  var lang = me.dataset.lang || 'pl', T = {"pl": {"label": "Reklama", "title": "Chcesz taką aplikację dla siebie?", "sub": "Gry, komiksy i galeria z Tobą w roli głównej.", "cta": "Sprawdź", "m_title": "Twoja aplikacja dla fanów", "m_body": ["Tę stronę Eve można zainstalować na telefonie jak aplikację, bez App Store i Google Play.", "Taką samą robimy dla Ciebie: gry z Twoją postacią, komiksy, galerię, blog i 9 języków.", "Dla marek, z którymi współpracujesz, są miejsca na sponsora i raporty z liczbami."], "more": "Zobacz więcej", "close": "Zamknij", "bar": "Podobał się komiks? Ty też możesz mieć taką aplikację z grami i komiksami o sobie.", "bar_cta": "Jak to działa"}, "en": {"label": "Ad", "title": "Want an app like this for yourself?", "sub": "Games, comics and a gallery starring you.", "cta": "Take a look", "m_title": "Your own app for your fans", "m_body": ["Eve’s site installs on a phone like an app, with no App Store or Google Play needed.", "We build the same for you: games with your character, comics, a gallery, a blog and 9 languages.", "Brands you work with get sponsor spots and reports with real numbers."], "more": "See more", "close": "Close", "bar": "Enjoyed the comic? You could have an app like this, with games and comics about you.", "bar_cta": "How it works"}, "es": {"label": "Anuncio", "title": "¿Quieres una app como esta?", "sub": "Juegos, cómics y una galería protagonizados por ti.", "cta": "Echa un vistazo", "m_title": "Tu propia app para tus fans", "m_body": ["La web de Eve se instala en el móvil como una app, sin App Store ni Google Play.", "Hacemos lo mismo para ti: juegos con tu personaje, cómics, galería, blog y 9 idiomas.", "Las marcas con las que colaboras tienen espacios de patrocinio e informes con cifras reales."], "more": "Ver más", "close": "Cerrar", "bar": "¿Te ha gustado el cómic? Tú también puedes tener una app así, con juegos y cómics sobre ti.", "bar_cta": "Cómo funciona"}, "pt": {"label": "Anúncio", "title": "Quer um app como este?", "sub": "Jogos, quadrinhos e uma galeria estrelados por você.", "cta": "Confira", "m_title": "Seu próprio app para os fãs", "m_body": ["O site da Eve se instala no celular como um app, sem App Store nem Google Play.", "Fazemos o mesmo para você: jogos com a sua personagem, quadrinhos, galeria, blog e 9 idiomas.", "As marcas com quem você trabalha ganham espaços de patrocínio e relatórios com números reais."], "more": "Ver mais", "close": "Fechar", "bar": "Gostou do quadrinho? Você também pode ter um app assim, com jogos e quadrinhos sobre você.", "bar_cta": "Como funciona"}, "it": {"label": "Pubblicità", "title": "Vuoi un’app come questa?", "sub": "Giochi, fumetti e una galleria con te protagonista.", "cta": "Scopri", "m_title": "La tua app per i fan", "m_body": ["Il sito di Eve si installa sul telefono come un’app, senza App Store né Google Play.", "Facciamo lo stesso per te: giochi con il tuo personaggio, fumetti, galleria, blog e 9 lingue.", "I brand con cui collabori hanno spazi sponsor e report con numeri reali."], "more": "Scopri di più", "close": "Chiudi", "bar": "Ti è piaciuto il fumetto? Anche tu puoi avere un’app così, con giochi e fumetti su di te.", "bar_cta": "Come funziona"}, "ja": {"label": "広告", "title": "こんなアプリを自分にも？", "sub": "あなたが主役のゲーム、コミック、ギャラリー。", "cta": "詳しく見る", "m_title": "ファンのためのあなた専用アプリ", "m_body": ["Eve のサイトは App Store や Google Play なしで、アプリのようにスマホにインストールできます。", "あなたにも同じものを作ります。あなたのキャラクターのゲーム、コミック、ギャラリー、ブログ、9 言語に対応。", "コラボ中のブランドには、スポンサー枠と実数のレポートを用意します。"], "more": "もっと見る", "close": "閉じる", "bar": "コミックはいかがでしたか？ あなたが主役のゲームとコミックのアプリも作れます。", "bar_cta": "しくみを見る"}, "zh": {"label": "广告", "title": "想要一个这样的 App 吗？", "sub": "由你主演的游戏、漫画和图库。", "cta": "看看", "m_title": "属于你的粉丝 App", "m_body": ["Eve 的网站可以像 App 一样安装到手机上，无需 App Store 或 Google Play。", "我们也能为你打造：以你为角色的游戏、漫画、图库、博客，支持 9 种语言。", "与你合作的品牌可获得赞助位和真实数据报告。"], "more": "查看更多", "close": "关闭", "bar": "喜欢这部漫画吗？你也可以拥有这样一个关于你的游戏和漫画 App。", "bar_cta": "了解方式"}, "fr": {"label": "Pub", "title": "Envie d’une appli comme celle-ci ?", "sub": "Des jeux, des BD et une galerie dont tu es la star.", "cta": "Jeter un œil", "m_title": "Ta propre appli pour tes fans", "m_body": ["Le site d’Eve s’installe sur le téléphone comme une appli, sans App Store ni Google Play.", "Nous faisons la même chose pour toi : des jeux avec ton personnage, des BD, une galerie, un blog et 9 langues.", "Les marques avec lesquelles tu travailles ont droit à des places de sponsor et à des rapports chiffrés."], "more": "En voir plus", "close": "Fermer", "bar": "Tu as aimé la BD ? Tu peux avoir une appli comme celle-ci, avec des jeux et des BD sur toi.", "bar_cta": "Comment ça marche"}, "de": {"label": "Werbung", "title": "Willst du auch so eine App?", "sub": "Spiele, Comics und eine Galerie mit dir in der Hauptrolle.", "cta": "Ansehen", "m_title": "Deine eigene App für deine Fans", "m_body": ["Eves Website lässt sich wie eine App aufs Handy installieren, ganz ohne App Store oder Google Play.", "Das Gleiche bauen wir für dich: Spiele mit deiner Figur, Comics, eine Galerie, einen Blog und 9 Sprachen.", "Marken, mit denen du arbeitest, bekommen Sponsorenplätze und Berichte mit echten Zahlen."], "more": "Mehr erfahren", "close": "Schließen", "bar": "Hat dir der Comic gefallen? Du kannst auch eine App wie diese haben, mit Spielen und Comics über dich.", "bar_cta": "So funktioniert es"}}, t = T[lang] || T.en;
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
