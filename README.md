# Eve — strona multiwersum Eve

Statyczna strona (HTML/CSS/JS) o Eve — gotyckiej influencerce i modelce AI (blog o alternatywie i popkulturze; przy okazji bohaterce gier). Hostowana na GitHub Pages
(repo `eve-gothic/eve-gothic.github.io`, gałąź `main`, katalog główny): https://eve-gothic.github.io/ (PL), `/en/`, `/es/`, `/pt/`, `/it/`, `/ja/`, `/zh/`.
Adres strony: `SITE` w `scripts/build.py`. Stare repo `woDzu2207/eve-strona` (wodzu2207.github.io/eve-strona/) zawiera
tylko przekierowania na nowy adres. Publikacja = build + commit + push — patrz **BLOG.md**.

- Projekt: wariant B „Gotycki luksus” (podglądy wszystkich wariantów: `/warianty/`).
- Strony główne, Blog Eve, RSS, obrazki OG i sitemap generuje `python3 scripts/build.py` — patrz **BLOG.md**.
- Teksty UI: `scripts/i18n.py`, style: `css/eve.css`, skrypty: `js/eve.js`, zdjęcia/wideo: `assets/`.
- Fonty do obrazków OG: `scripts/fonts/` (Playfair Display, Inter — licencja SIL OFL, `scripts/fonts/OFL.txt`); dla ja/zh systemowe Noto CJK (`fonts-noto-cjk`).

## Link w bio i analityka
- `/linki/` (EN, główny adres do bio), `/pl/linki/`, `/es/linki/`, `/pt/linki/`, `/it/linki/`, `/ja/linki/`, `/zh/linki/` (+ kopia `/en/linki/` z canonical → `/linki/`). Linki wewnętrzne mają UTM `utm_source=instagram&utm_medium=bio&utm_campaign=linkinbio`.
- Analityka GoatCounter (bez cookies): w `scripts/build.py` ustaw `ANALYTICS_CODE = 'kod'` (z konta https://<kod>.goatcounter.com) i przebuduj. Puste = wyłączone.
