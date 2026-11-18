#!/bin/bash
# Kopiuje ZBUDOWANE gry Eve (tylko dist, bez kodu źródłowego) do strony: /gry/karne/ i /gry/brawler/.
# Gry działają wtedy w apce Eve (ta sama domena) i offline po pierwszym uruchomieniu (każda ma własny sw.js
# ze scope ograniczonym do swojego folderu). Właścicielka: Gry.
#
# Użycie (z katalogu repo strony):
#   scripts/sync_games.sh            # buduje obie gry i kopiuje dist
#   scripts/sync_games.sh karne      # tylko karne   (brawler — tylko brawler)
#   NO_BUILD=1 scripts/sync_games.sh # kopiuje istniejące dist bez budowania
# Potem: git add gry && git commit && git pull --rebase && git push
# Stare adresy (wodzu2207.github.io/eve-penalty, /eve-brawler) aktualizuje osobno tools/deploy.sh w repo gry.
set -euo pipefail
SITE="$(cd "$(dirname "$0")/.." && pwd)"
PENALTY_SRC="${PENALTY_SRC:-/workspace/eve-penalty}"
BRAWLER_SRC="${BRAWLER_SRC:-/workspace/eve-brawler}"
want="${1:-all}"

sync_one() {   # $1 = katalog źródłowy gry, $2 = folder docelowy w stronie
  local src="$1" dst="$SITE/gry/$2"
  [ -f "$src/package.json" ] || { echo "brak gry w $src" >&2; exit 1; }
  if [ -z "${NO_BUILD:-}" ]; then (cd "$src" && npm run build >/dev/null); fi
  [ -f "$src/dist/index.html" ] && [ -f "$src/dist/sw.js" ] || { echo "brak $src/dist" >&2; exit 1; }
  # Strażnik: do publicznego repo idzie tylko zbudowana gra
  if [ -d "$src/dist/src" ] || [ -f "$src/dist/package.json" ] || [ -f "$src/dist/vite.config.js" ] || find "$src/dist" -name '*.map' | grep -q .; then
    echo "ODMOWA: w dist są pliki źródłowe ($src)" >&2; exit 1
  fi
  rm -rf "$dst" && mkdir -p "$dst"
  cp -a "$src/dist/." "$dst/"
  echo "gry/$2/  <- $src/dist  ($(find "$dst" -type f | wc -l) plików, $(du -sh "$dst" | cut -f1))"
}
case "$want" in
  all)     sync_one "$PENALTY_SRC" karne; sync_one "$BRAWLER_SRC" brawler ;;
  karne)   sync_one "$PENALTY_SRC" karne ;;
  brawler) sync_one "$BRAWLER_SRC" brawler ;;
  *) echo "użycie: $0 [all|karne|brawler]" >&2; exit 2 ;;
esac
