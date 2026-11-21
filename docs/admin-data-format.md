# Format danych panelu „Eve Admin” (v1)

Dla: **Gry** (panel + Worker zapisujący do repo). Właściciel formatu i `build.py`: **Strona**.
Repo: `Eve-gothic/eve-gothic.github.io`, gałąź `main`. Stan na 20.11.2026.

Panel/Worker zapisuje **tylko** te ścieżki (nic poza nimi — reszta to kod strony): `content/`, `assets/img/uploads/` i `assets/video/uploads/`.

| Co | Plik(i) | Obrazki |
|---|---|---|
| Galeria | `content/gallery.json` | `assets/img/uploads/gallery/<id>.webp` + `<id>-thumb.webp` |
| Wpisy | `content/posts/<slug>.json` (jeden plik na wpis) | `assets/img/uploads/posts/<RRRR-MM-DD>-<slug>.webp` |
| Baner sponsora | `content/ads.json` | `assets/img/uploads/ads/<RRRR-MM-DD>-<nazwa>.webp` |
| Filmiki | `content/videos.json` | `assets/video/uploads/<id>.mp4` + `<id>-poster.webp` |
| Opis strony głównej | `content/home.json` | — |
| Wygląd strony (motyw) | `content/theme.json` | — (skórki: `css/themes/*.css` — to kod strony, nie dla Workera) |
| Nowa sesja zdjęciowa | `content/sessions/<slug>.json` (jeden plik na sesję) | `assets/img/uploads/sessions/<slug>/<nazwa>.webp` (+ miniatury) |

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

## 4. Filmiki — `content/videos.json` + `assets/video/uploads/`

```json
{
 "version": 1,
 "_info": "…",
 "items": [
  {"id": "2026-11-20-jesienny-spacer",
   "mp4": "assets/video/uploads/2026-11-20-jesienny-spacer.mp4",
   "poster": "assets/video/uploads/2026-11-20-jesienny-spacer-poster.webp",
   "w": 720, "h": 1280, "duration": 8,
   "title": {"pl": "Jesienny spacer"}, "alt": {"pl": "Eve idzie alejką w parku"},
   "added": "2026-11-20", "source": "panel"}
 ]
}
```

- **Nowe pozycje na POCZĄTEK `items`.** Na stronie głównej (sekcja „Filmiki”, `#filmiki`, 7 języków) najpierw idą filmiki z `items` (bez `hidden`), potem dotychczasowe z `scripts/i18n.py` (`VIDEOS`). Numeracja „Kadr NN” jest ciągła.
- Pola: `id` (slug, unikalny, wymagane) · `mp4` (wymagane) · `poster` (zalecane; brak → film bez okładki) · `w`, `h` (domyślnie 720×1280; atrybuty `<video>`, 16–4096) · `duration` (sekundy, informacyjne; jeśli podane: > 0 i ≤ 20) · `title` (wymagane, `{"pl": …}`; brak języka → `en`, potem `pl`) · `alt`, `added`, `source` (informacyjne; `alt` build na razie nie wypisuje) · `hidden: true` (= ukryj, tak robi „Usuń”).
- **Plik wideo**: tylko **H.264 MP4, bez dźwięku, ≤ 20 s, ≤ 4 MB** (4 194 304 B). Okładka: **WebP ≤ 120 KB**, ta sama proporcja co film. WebM nie jest potrzebny (strona dla filmów z panelu nie dodaje `<source webm>`).
- Ścieżki: dokładnie `^assets/video/uploads/[a-z0-9-]+\.(mp4|webp)$` (mp4 → `.mp4`, poster → `.webp`), zawsze **nowa nazwa** pliku (z datą), nigdy nadpisanie.
- Build **sprawdza**: ścieżkę, istnienie pliku, limit rozmiaru, sygnaturę (MP4 = `ftyp`, WebP = `RIFF…WEBP`), że to H.264 (`avc1`/`avc3`), że nie ma ścieżki dźwięku (`soun`), `duration`, `w`/`h`, `id` (format, unikalność), `title`. Błędna pozycja jest **pominięta z ostrzeżeniem** (reszta strony się buduje) — panel powinien więc sam pilnować tych samych limitów przed zapisem, bo inaczej film „nie pojawi się” bez komunikatu w UI.
- HTML (dla orientacji): `<video muted playsinline controls loop preload="none" data-hover poster="…" width="w" height="h"><source src="…mp4" type="video/mp4">…</video><h3>tytuł</h3>`. Film ma kadr 3:4 (`object-fit: cover`) — kadr 9:16 jest przycięty z góry i dołu; poster też.
- Powiadomienie o filmie: wysyłaj po tym, jak strona główna (`https://eve-gothic.github.io/`) zawiera ścieżkę `mp4` filmu.

## 5. Opis strony głównej — `content/home.json`

```json
{
 "version": 1,
 "_info": "…",
 "i18n": {
  "pl": {"kicker": "Influencerka AI · Gotycki styl",
         "deck": "Gotycka influencerka i modelka AI. …",
         "about": "Jestem Eve — **gotycka modelka i influencerka wygenerowana przez AI**. …",
         "quote": "„Czerń nigdy nie wychodzi z mody. Ja też nie.”"}
 },
 "needs_translation": ["en", "es", "pt", "it", "ja", "zh"],
 "updated": "2026-11-20", "source": "panel"
}
```

- Cztery pola, wszystkie **zwykły tekst** (bez HTML): `kicker` (nadtytuł nad „Eve.”, ≤ 160 znaków), `deck` (podtytuł pod „Eve.”, ≤ 600), `about` (sekcja „O Eve”, ≤ 3000; `**tekst**` = pogrubienie), `quote` (cytat, ≤ 400).
- Build: dla każdego języka z `i18n` nadpisuje **tylko te pola, które są w pliku**; reszta i języki bez wpisu zostają z `scripts/i18n.py`. HTML w tekście jest **escapowany** (`&`, `<`, `>`, `"`), potem `**x**` w `about` → `<strong>x</strong>`. Puste/nie-tekstowe/za długie pole jest pomijane z ostrzeżeniem (zostaje tekst domyślny); nieznane pola i języki — ostrzeżenie.
- `kicker` wpływa też na: nagłówek bloga („Influencerka AI · Nº 01” — pierwszy człon do `·`) i obrazek OG strony głównej (`og/home-<lang>.jpg`). Meta `description` strony się **nie** zmienia (osobny tekst w kodzie).
- Panel zapisuje tylko `i18n.pl` (inne języki w pliku zostawia) i po każdej zmianie wpisuje pozostałe 6 języków do `needs_translation`. Kto przetłumaczy (Strona), dopisuje `i18n.<lang>` i usuwa język z listy. Build listy `needs_translation` nie czyta.
- Odczyt bieżącego tekstu w panelu ze strony głównej: `.cover-txt .sc` (kicker), `p.deck`, `p.lede` (about; zawiera `<strong>` → zamień na `**…**`, encje HTML na znaki), `p.quote`. Klas nie zmieniamy bez uprzedzenia. Albo — pewniej — jeśli `home.json` istnieje i ma `i18n.pl.<pole>`, użyj go; brak pola = tekst domyślny ze strony.
- Pliki bez `i18n.pl` (pusty `i18n: {}`) = brak zmian (stan początkowy).

## 6. Wygląd strony — `content/theme.json`

```json
{"version": 1, "_info": "…", "theme": "magazyn", "updated": "2026-11-20", "source": "panel"}
```

| `theme` | nazwa | wygląd | plik |
|---|---|---|---|
| `magazyn` | Magazyn (obecny, domyślny) | burgund, czerń i złoto, Playfair Display + Cormorant | — (brak zmian w HTML) |
| `neon` | Neon noc (wariant A) | czerń/fiolet, neonowy róż i cyjan, poświata, Orbitron + Rajdhani | `css/themes/neon.css` |
| `luksus` | Gotycki luksus (wariant B) | czerń i złoto zamiast burgundu, Cinzel, złote ramki | `css/themes/luksus.css` |
| `minimal` | Jasny minimal (wariant C) | biel, pastele (lawenda, brzoskwinia, mięta), DM Serif Display + DM Sans, zaokrąglenia | `css/themes/minimal.css` |
| `creator` | Instagram / creator (wariant D) | ciemne karty, gradient różowo-fioletowo-pomarańczowy, Poppins | `css/themes/creator.css` |

- Brak pliku albo nieznana wartość → `magazyn` (nieznana wartość daje ostrzeżenie). Dla `magazyn` HTML jest **bajt w bajt taki jak bez tego pliku**.
- Dla innej wartości build dodaje na **wszystkich stronach z własnym `<head>`** (strona główna, blog, wpisy, komiksy, sesje, dla twórców, /linki/): `<html … data-theme="<motyw>">`, linki do fontów motywu i `<link rel="stylesheet" href="…/css/themes/<motyw>.css">` po `css/eve.css`. Dla `magazyn` **nie ma** atrybutu `data-theme` (odstępstwo od pierwotnej prośby — inaczej wynik nie byłby identyczny; panel czyta motyw z `theme.json`, nie z HTML).
- Skórki to **sam CSS** na istniejącym HTML (te same klasy) — blog, komiksy, gry, 7 języków i PWA działają bez zmian. `offline.html` ma własny, wbudowany styl i nie zmienia wyglądu; paski/okna apki (instalacja, powiadomienia) mają własne style. Skórka jest też w pamięci offline apki (sw.js dodaje `css/themes/<motyw>.css` do app shell).
- Wszystkie 4 skórki są **gotowe** (panel może zdjąć „projekt poglądowy”). Pliki `css/themes/*.css` są generowane przez `python3 scripts/make_themes.py` z `css/eve.css` + `scripts/themes/<motyw>.css` — Worker ich nie dotyka.
- Zmiana motywu = zmiana `theme.json` (jeden commit); po buildzie zmienia się wygląd całej strony.

---

## 7. Sesje zdjęciowe — `content/sessions/<slug>.json` + `assets/img/uploads/sessions/<slug>/`

Osobna podstrona z kilkoma–kilkunastoma zdjęciami (jak istniejąca „Czerń na własnych zasadach”, `/sesje/czern/`) + duży kafel-zajawka na stronie głównej w sekcji galerii (`#galeria`, pod „Nową sesją”). Istniejąca sesja `czern` jest zaszyta w `build.py` — **nie ma pliku JSON, jej slug jest zarezerwowany** i panel jej nie edytuje.

```json
{
 "slug": "jesien-w-londynie",
 "title": {"pl": "Jesień w Londynie"},
 "kicker": {"pl": "Sesja"},
 "lead": {"pl": "Krótki opis pod tytułem i do podglądu linku (opcjonalnie)."},
 "cover": "assets/img/uploads/sessions/jesien-w-londynie/01.webp",
 "photos": [
  {"full": "assets/img/uploads/sessions/jesien-w-londynie/01.webp",
   "thumb": "assets/img/uploads/sessions/jesien-w-londynie/01-thumb.webp",
   "w": 450, "h": 600,
   "alt": {"pl": "Eve w płaszczu na moście"}},
  {"full": "assets/img/uploads/sessions/jesien-w-londynie/02.webp",
   "thumb": "assets/img/uploads/sessions/jesien-w-londynie/02-thumb.webp"}
 ],
 "added": "2026-11-21",
 "hidden": false,
 "source": "panel"
}
```

| pole | wymagane | opis |
|---|---|---|
| `slug` | tak | = nazwa pliku bez `.json`; `a-z0-9-`; **nie `czern`** (ani `index`). Panel sprawdza, czy plik już istnieje, i dokleja `-2`, `-3`… |
| `title` | tak | `{"pl": "…"}` (inne języki dopisze Strona; brak języka → `en` → `pl`). Zwykły napis też działa. Nagłówek, kafelek, `<title>`, podpisy zdjęć i obrazek OG. HTML jest escapowany (`<`, `&` bezpieczne) |
| `lead` | nie | krótki opis (1–2 zdania) pod tytułem, w zajawce i w podglądzie linku (`og:description`); brak → bez akapitu |
| `kicker` | nie | mała etykieta nad tytułem; brak → przetłumaczone „Sesja / Photo session / Sesión…” (zalecane: **nie podawać**) |
| `photos` | tak | lista 1–**20** zdjęć, kolejność w pliku = kolejność na stronie. Dalsze niż 20 są ignorowane (ostrzeżenie) |
| `photos[].full` | tak | duże zdjęcie (otwiera się po kliknięciu): WebP, zalecane **3:4 pionowo, 1200×1600**, jakość ~0.8, **≤ 300 KB** (twardy limit builda 500 KB), wymiary 200–4000 px |
| `photos[].thumb` | nie (zalecane) | miniatura do siatki: WebP **450×600**, **≤ 40 KB** (twardy limit 100 KB). Brak → siatka ładuje `full` (wolniej, ale działa) |
| `photos[].w`, `.h` | nie | ignorowane — build sam czyta wymiary z pliku (miniatury, a bez niej `full`); możesz je pominąć |
| `photos[].alt` | zalecane | opis dla niewidomych/SEO `{"pl": …}`; brak → „Eve — <tytuł> — Zdjęcie n / N” |
| `photos[].hidden` | nie | `true` = pomiń to zdjęcie |
| `cover` | nie | zdjęcie na kafel-zajawkę i obrazek OG (ścieżka jak `full`); brak → `photos[0].full` |
| `added` | zalecane | `RRRR-MM-DD`; **kolejność zajawek na głównej: najnowsze (`added` malejąco) pierwsze**, na końcu „Czerń na własnych zasadach”. Brak daty → na końcu nowych |
| `hidden` | nie | `true` = sesji **nie ma**: nie jest budowana, nie ma zajawki, nie ma w `sitemap.xml`, a wygenerowane wcześniej strony i obrazki OG są usuwane przy następnym buildzie (pliki zdjęć w repo zostają). „Usuń” w panelu = `hidden: true` |
| `source` | nie | informacyjne (`"panel"`) |

- **Ścieżki obrazków**: dokładnie `^assets/img/uploads/sessions/<a-z0-9->/<a-z0-9->.webp$` (pierwszy człon = folder sesji; zalecane `<slug>`; pliki `NN.webp` i `NN-thumb.webp`), zawsze **nowa nazwa** (nie nadpisuj istniejącego pliku — zob. „Wspólne zasady”). Bez `/` na początku i bez `..`.
- **Kolejność zapisu**: **jeden commit** z wszystkimi zdjęciami i miniaturami **oraz** plikiem JSON (Git Data API: bloby → drzewo → commit → ref, jak w pkt 8). Wiele zdjęć naraz = jeden commit. Nie commituj JSON-a wcześniej niż zdjęć (w jednym commicie kolejność nie ma znaczenia).
- **Co buduje build** dla każdej sesji, we wszystkich 7 językach (adres jak `czern`: `/sesje/<slug>/`, `/en/sesje/<slug>/`, `/es/…`, `/pt/…`, `/it/…`, `/ja/…`, `/zh/…`): stronę z siatką 4 kolumny (2 na telefonie) i powiększaniem po kliknięciu, `canonical` + `hreflang`, `og:image` `og/sesja-<slug>-<język>.jpg` (okładka + tytuł; generowany przez build), wpis w `sitemap.xml`, `pwa_head`, blok „Obserwuj Eve” i zajawkę na stronie głównej. Aplikacja offline: zdjęcia trafiają do pamięci podręcznej przy pierwszym obejrzeniu (jak zdjęcia sesji `czern`; nie są w paczce startowej).
- **Błędy** (nie wywracają builda; `python3 scripts/content.py` pokazuje je jako `UWAGA (content): …`, kod wyjścia 1): zły/zepsuty JSON, slug ≠ nazwa pliku / zły znak / `czern`, brak `title`, zła data `added`, brak `photos` → **cała sesja pominięta**. Zdjęcie z błędną ścieżką, brakujące, za duże, nie-WebP albo o wymiarach poza 200–4000 px → **pominięte samo zdjęcie** (sesja się publikuje z pozostałymi, jeśli zostało ≥ 1). Błędna `cover` → sesja pominięta.
- Powiadomienie push: po tym, jak `https://eve-gothic.github.io/sesje/<slug>/` zwraca 200 (np. „Nowa sesja: <tytuł>”).
- Strona jest dla każdego wieku — tylko zdjęcia „safe” (zob. „Wspólne zasady”).

---

## 8. Jak Worker zapisuje (GitHub API) i co się dzieje potem

1. Worker robi **jeden commit na jedną akcję w panelu** (np. zdjęcie + miniatura + `gallery.json`), przez Git Data API:
   `GET /repos/Eve-gothic/eve-gothic.github.io/git/ref/heads/main` → blob(y) obrazków (base64) → `POST /git/trees` (base_tree = tree ostatniego commita) → `POST /git/commits` → `PATCH /git/refs/heads/main` (**bez** `force`).
   Jeśli `PATCH` zwróci 422 (ktoś — np. bot — wypchnął w międzyczasie): pobierz świeży `main`, **od nowa przeczytaj** JSON, ponownie wstaw zmianę, spróbuj jeszcze raz (max 3 razy). Nigdy nie nadpisuj całego JSON wersją sprzed chwili — boty też dopisują do tych plików.
   (Contents API `PUT /contents/…` też działa, ale to osobny commit na każdy plik.)
2. Komunikat commita: `Panel: <co> (<id/slug>)`, autor np. `Eve Admin <woDzu2207@users.noreply.github.com>`.
3. Token: fine-grained PAT tylko na repo `Eve-gothic/eve-gothic.github.io`, uprawnienie **Contents: Read and write** (nic więcej), jako sekret Workera. Worker przed zapisem sprawdza, że każda ścieżka zaczyna się od `content/`, `assets/img/uploads/` lub `assets/video/uploads/`, że obrazek to WebP (a film H.264 MP4 bez dźwięku) i mieści się w limicie.
4. Push na `main` uruchamia workflow **`.github/workflows/build-pages.yml`**: `python3 scripts/content.py` → `python3 scripts/build.py` → paczka strony (bez `.git`, `.github` i `docs/`) → publikacja na GitHub Pages. Zwykle 2–4 min od zapisu do strony na żywo.
5. Powiadomienie push (Gry): wyślij dopiero, gdy adres zwraca 200 (np. `https://eve-gothic.github.io/blog/<slug>/` dla wpisu, strona główna `#galeria` dla zdjęcia). Status buildu: `GET /repos/Eve-gothic/eve-gothic.github.io/actions/runs?head_sha=<sha commita>` (`conclusion: success`).

### ⚠️ Obecny stan publikacji (ważne dla trybu „na żywo”)

Na dziś GitHub Pages publikuje jeszcze **ze starego trybu „Deploy from a branch”** (pliki z `main` takie, jakie są). Workflow tylko buduje i porównuje (publikacja w nim jest wyłączona). W tym trybie sam commit JSON od panelu **nie pojawi się na stronie**, dopóki ktoś nie uruchomi `build.py` i nie wypchnie wyniku. Przełączenie na publikację przez Actions (Settings → Pages → Source: GitHub Actions + zmienna repo `EVE_ACTIONS_DEPLOY=true`) robi Strona po zgodzie Daniela — opis w nagłówku workflow. Do tego czasu panel zostaje w trybie testowym.

Weryfikacja 20.11.2026: build w CI (run 44726488969) daje pliki **identyczne** z repo (jedyna różnica: `scripts/__pycache__/*.pyc`, których CI celowo nie publikuje — to nie część strony). Przełączenie jest więc bezpieczne technicznie; czeka tylko na zgodę Daniela.

Uwaga dla botów pracujących lokalnie: po przełączeniu wygenerowane pliki w repo mogą być „za” stroną na żywo (CI buduje z JSON). Przed lokalnym buildem zawsze `git pull --rebase` — build i tak odtworzy wszystko z tych samych danych.
