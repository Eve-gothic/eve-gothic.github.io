# Format danych panelu „Eve Admin” (v1)

Dla: **Gry** (panel + Worker zapisujący do repo). Właściciel formatu i `build.py`: **Strona**.
Repo: `Eve-gothic/eve-gothic.github.io`, gałąź `main`. Stan na 20.11.2026.

Panel/Worker zapisuje **tylko** te ścieżki (nic poza nimi — reszta to kod strony):

| Co | Plik(i) | Obrazki |
|---|---|---|
| Galeria | `content/gallery.json` | `assets/img/uploads/gallery/<id>.webp` + `<id>-thumb.webp` |
| Wpisy | `content/posts/<slug>.json` (jeden plik na wpis) | `assets/img/uploads/posts/<RRRR-MM-DD>-<slug>.webp` |
| Baner sponsora | `content/ads.json` | `assets/img/uploads/ads/<RRRR-MM-DD>-<nazwa>.webp` |

`build.py` czyta te pliki (moduł `scripts/content.py`). Wygenerowane HTML, `sitemap.xml`, `feed.xml`, `sw.js` itd. robi build — **Worker ich nie commituje**.

Sprawdzenie danych bez budowania (z katalogu repo): `python3 scripts/content.py` → kod wyjścia 0 = OK, 1 = są błędy (wypisane jako `UWAGA (content): …`).
Błędny wpis/zdjęcie **nie wywraca** builda: jest pomijany z ostrzeżeniem, reszta strony publikuje się normalnie.

---

## Wspólne zasady

- **JSON**: UTF-8, bez BOM, `ensure_ascii=false` (polskie znaki wprost), wcięcie dowolne. Klucze zaczynające się od `_` (np. `_info`) build ignoruje — nie usuwaj ich.
- **Języki**: `pl, en, es, pt, it, ja, zh`. Pola tekstowe tłumaczone to obiekty `{"pl": "…", "en": "…"}`. Panel v1 wypełnia **tylko `pl`**. Brakujący język → build bierze `en`, potem `pl`. Tłumaczenia dopisze później bot Strona (te same pliki, kolejne klucze języków) — panel **nie może kasować** istniejących kluczy języków przy edycji.
- **id / slug**: `^[a-z0-9]+(-[a-z0-9]+)*$` (małe litery bez polskich znaków, cyfry, myślniki). Transliteracja: ą→a, ć→c, ę→e, ł→l, ń→n, ó→o, ś→s, ź/ż→z.
- **Obrazki**: zawsze WebP, zawsze **nowa nazwa pliku** (z datą) — nigdy nie nadpisuj istniejącego pliku (aplikacja trzyma obrazki w pamięci offline; nowa nazwa = brak starej wersji w cache). Ścieżki w JSON są względem korzenia repo i zaczynają się od `assets/` (bez `/` na początku, bez `..`).
- **Treść**: strona jest dla każdego wieku — tylko zdjęcia „safe”. Panel nie powinien pozwalać na nic innego (to do opisania w UI).
- **Daty**: `RRRR-MM-DD` (czas Londynu).

---

## 1. Galeria — `content/gallery.json`

```json
{
 "version": 1,
 "_info": "…",
 "spread": [ … 12 pozycji, stała rozkładówka — PANEL NIE ZMIENIA … ],
 "grid": [
  {
   "id": "2026-11-20-czarna-sukienka",
   "full": "assets/img/uploads/gallery/2026-11-20-czarna-sukienka.webp",
   "thumb": "assets/img/uploads/gallery/2026-11-20-czarna-sukienka-thumb.webp",
   "w": 450, "h": 600,
   "caption": {"pl": "Czarna sukienka"},
   "alt": {"pl": "Eve w czarnej sukience na tle ceglanej ściany"},
   "added": "2026-11-20",
   "source": "panel"
  },
  { "id": "gitara", "full": "assets/img/eve-gitara.webp", "thumb": "assets/img/eve-gitara-thumb.webp", "w": 450, "h": 600, "caption": {"pl": "Garażowy rock", "en": "Garage rock", "…": "…"}, "alt": {"…": "…"}, "added": "2026-11-05", "source": "bot" }
 ]
}
```

- **Panel dodaje nowe zdjęcie na POCZĄTEK `grid`** (najnowsze pierwsze). Kolejność w pliku = kolejność na stronie (sekcja „Nowa sesja” na stronie głównej, we wszystkich 7 językach).
- `spread` (pierwsza rozkładówka, 12 zdjęć w stałym układzie) — tylko do odczytu dla panelu.
- Pola `grid[]`:

| pole | wymagane | opis |
|---|---|---|
| `id` | tak | unikalne, `RRRR-MM-DD-krotki-opis` |
| `full` | tak | duże zdjęcie: WebP, **3:4 pionowo, 1200×1600**, jakość ~0.8, **≤ 300 KB** |
| `thumb` | tak | miniatura: WebP, **450×600** (ten sam kadr 3:4), ≤ 60 KB |
| `w`, `h` | nie (domyślnie 450, 600) | wymiary miniatury (atrybuty `<img>`, bez skakania układu) |
| `caption` | tak | podpis, krótki (≤ 40 znaków), `{"pl": …}` |
| `alt` | zalecane | opis dla niewidomych/SEO; brak → „Eve — {podpis}” |
| `added`, `source` | nie | informacyjne (`"panel"` / `"bot"`) |
| `hidden` | nie | `true` = ukryj na stronie bez kasowania (tak robi „Usuń” w panelu) |

- Zdjęcie z innym kadrem niż 3:4: panel kadruje środek do 3:4 (podgląd przed publikacją).
- Wiele zdjęć naraz = jeden commit z wieloma plikami + jedna zmiana `gallery.json`.

## 2. Wpis — `content/posts/<slug>.json`

```json
{
 "slug": "nowa-sesja-w-londynie",
 "date": "2026-11-20",
 "category": "Popkultura",
 "cover": "uploads/posts/2026-11-20-nowa-sesja-w-londynie",
 "draft": false,
 "source": "panel",
 "push": true,
 "i18n": {
  "pl": {
   "title": "Nowa sesja w Londynie",
   "excerpt": "Krótki opis na kafelek i do podglądu linku (opcjonalnie).",
   "body": "Pierwszy akapit.\n\nDrugi akapit z **pogrubieniem** i [linkiem](https://example.com).\n\n## Śródtytuł\n\n- punkt\n- punkt"
  }
 }
}
```

| pole | wymagane | opis |
|---|---|---|
| `slug` | tak | = nazwa pliku bez `.json`; polski wpis ma adres `https://eve-gothic.github.io/blog/<slug>/`. Nie może powtarzać sluga istniejącego wpisu (`blog/posts/<lang>/*-<slug>.md`) — wtedy wpis z panelu jest pomijany. Panel sprawdza, czy plik o tej nazwie już istnieje, i dokleja `-2`, `-3`… |
| `date` | tak | `RRRR-MM-DD`; sortowanie na blogu (najnowsze pierwsze) |
| `category` | tak | dokładnie jedna z: `Filmy`, `Gry`, `Książki`, `Komiksy`, `Alternatywa`, `Popkultura` (domyślnie w panelu: `Popkultura`) |
| `cover` | nie | okładka **bez** `assets/img/` i **bez** `.webp`: `uploads/posts/<RRRR-MM-DD>-<slug>` → plik `assets/img/uploads/posts/<RRRR-MM-DD>-<slug>.webp`. WebP, poziomo lub pionowo, dłuższy bok ≤ 1600 px, ≤ 300 KB. Opcjonalnie miniatura `…-thumb.webp` (600 px szer.) — używana na /linki/. Brak okładki → obrazek do podglądu linku z domyślnym zdjęciem. |
| `draft` | nie | `true` = nie publikuj (szkic) |
| `push` | nie | **pole Gry** — build go ignoruje; Worker/notifier decyduje o powiadomieniu |
| `i18n.<lang>.title` | tak | tytuł |
| `i18n.<lang>.body` | tak | treść w prostym Markdownie (niżej) |
| `i18n.<lang>.excerpt` | nie | brak → pierwsze ~160 znaków treści |

**Markdown w `body`** (to, co obsługuje build): akapity oddzielone pustą linią, `## / ### / ####` śródtytuły, `**pogrubienie**`, `*kursywa*`, `[tekst](https://…)` (zewnętrzne otwierają się w nowej karcie), `- lista`, `1. lista`, `> cytat`, `---` linia, `` `kod` ``. Bez HTML (jest escapowany). Śródtytuł `## Źródła` dostaje styl listy źródeł.

- v1: tylko `i18n.pl` → wpis pojawia się na polskim blogu (`/blog/`), w RSS, sitemap i na `/pl/linki/`. Inne języki pojawią się, gdy Strona dopisze `i18n.en`, `i18n.es`… (do zrobienia po teście panelu).
- Każdy wpis automatycznie dostaje obrazek OG (`blog/og/<slug>.jpg`, generuje build).
- Edycja wpisu = nadpisanie tego samego pliku (zachowaj nieznane pola i inne języki). Usunięcie = `"draft": true` (strona wpisu znika przy następnym buildzie).

## 3. Baner sponsora — `content/ads.json`

```json
{
 "version": 1,
 "_info": "…",
 "sponsor": {
  "active": true,
  "name": "Nazwa marki",
  "link": "https://marka.example/?utm_source=eve&utm_medium=banner",
  "image": "assets/img/uploads/ads/2026-11-20-marka.webp",
  "w": 1200, "h": 300,
  "label": {"pl": "Partner", "en": "Partner"},
  "alt": {"pl": "Marka — krótki opis grafiki"},
  "updated": "2026-11-20"
 }
}
```

- `active: false` (stan obecny) → na stronie jest dotychczasowy baner reklamy własnej („Chcesz taką aplikację dla siebie?”).
- `active: true` → **w tych samych miejscach** (dół strony głównej, koniec wpisu, koniec każdego komiksu — najwyżej 1 na stronę) pokazuje się grafika sponsora z etykietą `label` (zawsze widoczne „Partner”/„Reklama”), link otwiera się w nowej karcie z `rel="sponsored noopener"`.
- `link` musi zaczynać się od `https://`. `image`: WebP, **4:1, 1200×300**, ≤ 150 KB (inne proporcje: podaj prawdziwe `w`/`h`).
- Kliknięcia liczy GoatCounter jako zdarzenia `sponsor-click-home|post|komiks|komiks2|komiks3` (https://eve-ai.goatcounter.com/).
- „Podgląd obecnego banera” w panelu: pokaż `image` z `ads.json` (albo baner reklamy własnej, gdy `active: false`).
- Sponsor **w grach** (karne/bijatyka, zdarzenie `sponsor-shown`) to osobna konfiguracja gier Gry — ten plik go nie zmienia.

---

## 4. Jak Worker zapisuje (GitHub API) i co się dzieje potem

1. Worker robi **jeden commit na jedną akcję w panelu** (np. zdjęcie + miniatura + `gallery.json`), przez Git Data API:
   `GET /repos/Eve-gothic/eve-gothic.github.io/git/ref/heads/main` → blob(y) obrazków (base64) → `POST /git/trees` (base_tree = tree ostatniego commita) → `POST /git/commits` → `PATCH /git/refs/heads/main` (**bez** `force`).
   Jeśli `PATCH` zwróci 422 (ktoś — np. bot — wypchnął w międzyczasie): pobierz świeży `main`, **od nowa przeczytaj** JSON, ponownie wstaw zmianę, spróbuj jeszcze raz (max 3 razy). Nigdy nie nadpisuj całego JSON wersją sprzed chwili — boty też dopisują do tych plików.
   (Contents API `PUT /contents/…` też działa, ale to osobny commit na każdy plik.)
2. Komunikat commita: `Panel: <co> (<id/slug>)`, autor np. `Eve Admin <woDzu2207@users.noreply.github.com>`.
3. Token: fine-grained PAT tylko na repo `Eve-gothic/eve-gothic.github.io`, uprawnienie **Contents: Read and write** (nic więcej), jako sekret Workera. Worker przed zapisem sprawdza, że każda ścieżka zaczyna się od `content/` lub `assets/img/uploads/`, że obrazek to WebP i mieści się w limicie.
4. Push na `main` uruchamia workflow **`.github/workflows/build-pages.yml`**: `python3 scripts/content.py` → `python3 scripts/build.py` → paczka strony → publikacja na GitHub Pages. Zwykle 2–4 min od zapisu do strony na żywo.
5. Powiadomienie push (Gry): wyślij dopiero, gdy adres zwraca 200 (np. `https://eve-gothic.github.io/blog/<slug>/` dla wpisu, strona główna `#galeria` dla zdjęcia). Status buildu: `GET /repos/Eve-gothic/eve-gothic.github.io/actions/runs?head_sha=<sha commita>` (`conclusion: success`).

### ⚠️ Obecny stan publikacji (ważne dla trybu „na żywo”)

Na dziś GitHub Pages publikuje jeszcze **ze starego trybu „Deploy from a branch”** (pliki z `main` takie, jakie są). Workflow tylko buduje i porównuje (publikacja w nim jest wyłączona). W tym trybie sam commit JSON od panelu **nie pojawi się na stronie**, dopóki ktoś nie uruchomi `build.py` i nie wypchnie wyniku. Przełączenie na publikację przez Actions (Settings → Pages → Source: GitHub Actions + zmienna repo `EVE_ACTIONS_DEPLOY=true`) robi Strona po zgodzie Daniela — opis w nagłówku workflow. Do tego czasu panel zostaje w trybie testowym.

Uwaga dla botów pracujących lokalnie: po przełączeniu wygenerowane pliki w repo mogą być „za” stroną na żywo (CI buduje z JSON). Przed lokalnym buildem zawsze `git pull --rebase` — build i tak odtworzy wszystko z tych samych danych.
