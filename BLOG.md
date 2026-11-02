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
# 4) commit + push (GitHub = źródło; kopia GitHub Pages tylko przekierowuje):
git add -A
git -c user.name="woDzu2207" -c user.email="woDzu2207@users.noreply.github.com" commit -qm "Blog: $SLUG"
git push -q
# 5) deploy na Cloudflare — patrz „Hosting i deploy” niżej (automatycznie po pushu, jeśli jest sekret CLOUDFLARE_API_TOKEN;
#    inaczej tryb MCP w 3 krokach)
# 6) sprawdź (od razu po deployu):
B=https://eve-gothic.wodzu2207.workers.dev
for p in "" en/ es/ pt/; do for u in "$p" "${p}blog/" "${p}blog/$SLUG/" "${p}blog/feed.xml" "${p}18/"; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' $B/$u) $u"; done; done
curl -s -o /dev/null -w '%{http_code} og\n' $B/blog/og/$SLUG.jpg
curl -s -o /dev/null -w '%{http_code} sitemap\n' $B/sitemap.xml
curl -s $B/blog/$SLUG/ | grep -o '/eve-strona/' | wc -l    # ma być 0
```

Obrazek do ogłoszenia na Facebooku: `blog/og/<slug>.jpg` (PL; wersje językowe z sufiksem `-en/-es/-pt`).
Facebook pobiera go automatycznie z `og:image` po wklejeniu linku do wpisu. Gdy FB pokazuje stary podgląd,
odśwież go w https://developers.facebook.com/tools/debug/ .

## Usunięcie / zmiana wpisu

Edytuj lub usuń pliki w `blog/posts/<lang>/`, uruchom `python3 scripts/build.py` (strony usuniętych wpisów
zostaną skasowane automatycznie; stare `blog/og/<slug>*.jpg` usuń ręcznie), potem commit + push jak wyżej.

## Bramka 18+ (`/18/`, `/en/18/`, `/es/18/`, `/pt/18/`)

Generowana przez ten sam `python3 scripts/build.py` (teksty: `GATE` w `scripts/i18n.py`, adres docelowy:
`GATE_URL` w `scripts/build.py`). Tylko tekst — bez zdjęć, reklam i slotów; `noindex,nofollow`; nie ma jej w `sitemap.xml`.
Zewnętrzny link pojawia się/otwiera dopiero po kliknięciu „Mam 18 lat — przejdź” (wstawiany przez JS,
`rel="nofollow noopener noreferrer"`). Adresu docelowego **nie wpisuj** w żadnej innej stronie, stopce, sitemap ani OG —
pozostałe strony mają tylko mały link „18+” w stopce, prowadzący do bramki w danym języku.

## Hosting i deploy

- **Adres główny:** https://eve-gothic.wodzu2207.workers.dev/ — Cloudflare Worker `eve-gothic` (same pliki statyczne,
  darmowy plan) na koncie wodzinski.d@gmail.com. Adres jest w JEDNYM miejscu: `SITE` w `scripts/build.py`
  (canonical, hreflang, og:url, og:image, RSS, sitemap, stopka obrazków OG, przekierowanie z GitHub Pages).
  Zmiana domeny (np. na `eve-gothic.pages.dev` albo własną): zmień `SITE`, `python3 scripts/build.py`, commit, deploy.
- **GitHub Pages** (https://wodzu2207.github.io/eve-strona/) dalej działa, ale każda generowana strona ma w `<head>`
  skrypt, który TYLKO na hoście `*.github.io` robi `location.replace` + meta refresh na ten sam adres pod `SITE`.
  Canonical wskazuje nowy adres. Na Cloudflare skrypt nic nie robi.
- **Bramka 18+** (`/18/`, `/en|es|pt/18/`): `noindex,nofollow`, celowo poza `sitemap.xml` — tak ma zostać.
- Na Cloudflare trafia wszystko z repo poza: `.git`, `.github`, `scripts/`, `blog/posts/` (źródła .md), `*.md`.

### Deploy A — automatyczny (GitHub Actions), po jednorazowej konfiguracji

`.github/workflows/cloudflare.yml` po każdym pushu na `main` uruchamia `python3 scripts/deploy_cf.py deploy`.
Wymaga sekretu repo **`CLOUDFLARE_API_TOKEN`** (token z https://dash.cloudflare.com/profile/api-tokens, szablon
„Edit Cloudflare Workers” / uprawnienie Account → Workers Scripts → Edit). Bez sekretu job jest pomijany.
Ręcznie z tokenem: `CLOUDFLARE_API_TOKEN=… python3 scripts/deploy_cf.py deploy`. Wysyłane są tylko zmienione pliki.

### Deploy B — agent przez MCP Cloudflare (`user-Cloudflare` → `execute`), bez tokena na dysku

```bash
python3 scripts/deploy_cf.py manifest        # -> /tmp/eve-cf/manifest.json
```
1. MCP `execute` (wklej manifest):
   `POST /accounts/${accountId}/workers/scripts/eve-gothic/assets-upload-session` z body `{manifest}` → zwróć `result.jwt`, `result.buckets`.
2. Jeśli `buckets` nie jest puste: `python3 scripts/deploy_cf.py upload '<jwt>' '<buckets-json>'` → wypisuje completion JWT
   (gdy `buckets` puste, completion JWT = `jwt` z kroku 1).
3. MCP `execute`: `PUT /accounts/${accountId}/workers/scripts/eve-gothic` z FormData `metadata` =
   `{"compatibility_date":"2026-10-01","assets":{"jwt":"<completion JWT>","config":{"html_handling":"auto-trailing-slash","not_found_handling":"none"}}}`
   (typ `application/json`). Potem sprawdź URL-e z kroku 6 wyżej.

