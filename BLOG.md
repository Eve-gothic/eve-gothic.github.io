# Blog Eve — jak dodać wpis (PL / EN / ES / PT)

Wszystko (strona główna w 4 językach, blog, wpisy, RSS, obrazki do Facebooka/OG, sitemap)
generuje jeden skrypt: `scripts/build.py` (Python 3.8+ i Pillow, bez innych zależności).
**Nie edytuj ręcznie wygenerowanych plików HTML** (`index.html`, `en/`, `es/`, `pt/`, `blog/*/index.html`,
`feed.xml`, `blog/og/*.jpg`, `og/*.jpg`, `sitemap.xml`): przy następnym buildzie zostaną nadpisane.
Teksty interfejsu i sekcji strony głównej są w `scripts/i18n.py`, a wygląd w `css/eve.css`.

## Struktura

```
blog/posts/pl/RRRR-MM-DD-slug.md   ← źródło wpisu (polski, domyślny)
blog/posts/en/RRRR-MM-DD-slug.md   ← ten sam slug po angielsku
blog/posts/es/RRRR-MM-DD-slug.md   ← hiszpański
blog/posts/pt/RRRR-MM-DD-slug.md   ← portugalski (neutralny, przyjazny dla Brazylii)
```

Wynik buildu:

| Co | PL | EN | ES | PT |
|---|---|---|---|---|
| Strona główna | `/` | `/en/` | `/es/` | `/pt/` |
| Lista wpisów | `/blog/` | `/en/blog/` | `/es/blog/` | `/pt/blog/` |
| Wpis | `/blog/<slug>/` | `/en/blog/<slug>/` | `/es/blog/<slug>/` | `/pt/blog/<slug>/` |
| RSS | `/blog/feed.xml` | `/en/blog/feed.xml` | `/es/blog/feed.xml` | `/pt/blog/feed.xml` |
| Obrazek OG (1200×630) | `blog/og/<slug>.jpg` | `blog/og/<slug>-en.jpg` | `blog/og/<slug>-es.jpg` | `blog/og/<slug>-pt.jpg` |

Slug bierze się z nazwy pliku (część po dacie) i **musi być identyczny we wszystkich 4 językach** —
dzięki temu działa przełącznik języków i tagi `hreflang`. Brak którejś wersji językowej = ostrzeżenie w buildzie.
Strona główna każdego języka sama pokazuje 3 najnowsze wpisy.

## Format pliku

```markdown
---
title: Tytuł wpisu
date: 2026-11-02
category: Gry
excerpt: Jedno–dwa zdania zajawki (lista wpisów, RSS, opis OG).
cover: eve-gracz
---
Pierwszy akapit (dostaje inicjał).

## Śródtytuł

Tekst z *kursywą*, **pogrubieniem** i [linkiem](https://example.com).

> Cytat

## Źródła

- [Nazwa źródła](https://adres)
```

- `category` — zawsze **polska nazwa** (także w plikach en/es/pt): `Filmy`, `Gry`, `Książki`, `Komiksy`, `Alternatywa`, `Popkultura`.
  Na stronie wyświetla się przetłumaczona.
- `cover` (opcjonalnie) — nazwa pliku z `assets/img/` bez `.webp`, np. `eve-biblioteka`, `eve-gracz`, `eve-park`.
  Używaj tylko już zweryfikowanych zdjęć z `assets/img/`. Z niej powstaje też obrazek OG.
- `og_photo` (opcjonalnie) — inne zdjęcie tylko do obrazka OG (domyślnie = `cover`, a bez `cover` = `eve-biblioteka`).
- `draft: true` (opcjonalnie) — wpis jest pomijany.
- Nagłówek sekcji źródeł musi brzmieć dokładnie: `## Źródła` (pl), `## Sources` (en), `## Fuentes` (es), `## Fontes` (pt).
- Obsługiwany Markdown: `##`/`###`, akapity, listy `-` i `1.`, `>` cytat, `*kursywa*`, `**pogrubienie**`, `[link](url)`, `` `kod` ``, `---`.

## Zasady treści

Strona jest publiczna i dla wszystkich: zero treści seksualnych. Pisz głosem Eve (pierwsza osoba,
inteligentna, dowcipna fanka gotyckiej popkultury), 500–700 słów, tylko fakty sprawdzone w ≥2 prawdziwych
źródłach, bez zmyślonych cytatów; źródła z linkami na końcu. Stopka bloga sama informuje, że Eve jest postacią AI,
a wpisy pisze AI. Nigdy nie linkuj pełnej wersji gry (`eve-game`) ani `eve-game-safe`; tamagotchi to tylko `eve-game-public`.

## Dodanie wpisu — krok po kroku

```bash
cd /workspace/eve-strona
git pull -q
SLUG=moj-nowy-wpis; D=$(date +%F)
# 1) utwórz 4 pliki (ten sam slug!):
#    blog/posts/pl/$D-$SLUG.md  blog/posts/en/$D-$SLUG.md  blog/posts/es/$D-$SLUG.md  blog/posts/pt/$D-$SLUG.md
# 2) zbuduj:
python3 scripts/build.py          # wypisuje: OK: N wpisów (pl:…, en:…, es:…, pt:…)
# 3) podgląd lokalny (opcjonalnie):
python3 -m http.server 8765       # http://localhost:8765/  i /blog/$SLUG/
# 4) opublikuj:
git add -A
git -c user.name="woDzu2207" -c user.email="woDzu2207@users.noreply.github.com" commit -qm "Blog: $SLUG"
git push -q
# 5) sprawdź po ~1 min (GitHub Pages):
for p in "" en/ es/ pt/; do for u in "$p" "${p}blog/" "${p}blog/$SLUG/" "${p}blog/feed.xml"; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' https://wodzu2207.github.io/eve-strona/$u) $u"; done; done
curl -s -o /dev/null -w '%{http_code} og\n' https://wodzu2207.github.io/eve-strona/blog/og/$SLUG.jpg
```

Obrazek do ogłoszenia na Facebooku: `blog/og/<slug>.jpg` (PL; wersje językowe z sufiksem `-en/-es/-pt`).
Facebook pobiera go automatycznie z `og:image` po wklejeniu linku do wpisu. Gdy FB pokazuje stary podgląd,
odśwież go w https://developers.facebook.com/tools/debug/ .

## Usunięcie / zmiana wpisu

Edytuj lub usuń pliki w `blog/posts/<lang>/`, uruchom `python3 scripts/build.py` (strony usuniętych wpisów
zostaną skasowane automatycznie; stare `blog/og/<slug>*.jpg` usuń ręcznie), potem commit + push jak wyżej.
