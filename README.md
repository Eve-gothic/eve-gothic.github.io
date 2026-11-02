# Eve — strona multiwersum Eve

Statyczna strona (HTML/CSS/JS) o Eve, wirtualnej, wygenerowanej przez AI bohaterce gier. Hostowana na Cloudflare
(darmowy Worker ze statycznymi plikami): https://eve-gothic.wodzu2207.workers.dev/ (PL), `/en/`, `/es/`, `/pt/`.
Stara kopia na GitHub Pages (wodzu2207.github.io/eve-strona/) przekierowuje na nowy adres. Adres strony: `SITE` w `scripts/build.py`.
Deploy: `scripts/deploy_cf.py` — patrz **BLOG.md** („Hosting i deploy”).

- Projekt: wariant B „Gotycki luksus” (podglądy wszystkich wariantów: `/warianty/`).
- Strony główne, Blog Eve, RSS, obrazki OG i sitemap generuje `python3 scripts/build.py` — patrz **BLOG.md**.
- Teksty UI: `scripts/i18n.py`, style: `css/eve.css`, skrypty: `js/eve.js`, zdjęcia/wideo: `assets/`.
- Fonty do obrazków OG: `scripts/fonts/` (Playfair Display, Inter — licencja SIL OFL, `scripts/fonts/OFL.txt`).
