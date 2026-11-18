#!/bin/bash
# Publikacja strony Eve + automatyczne powiadomienia push o nowych wpisach/komiksach.
#   scripts/publish.sh "Nowy wpis: tytuł"      # build -> pull --rebase -> commit -> push -> czeka na GitHub Pages -> powiadomienia
#   scripts/publish.sh --no-notify "opis"      # bez powiadomień
#   scripts/publish.sh --dry-notify "opis"     # powiadomienia tylko na sucho (pokaże, co by poszło)
# Powiadomienia wysyła /workspace/eve-push/scripts/notify_new_content.mjs (prywatne repo, poza stroną): tylko dla treści,
# których jeszcze nie ma w state/sent.json i które zwracają 200 na żywo; datowane w przyszłość czekają. Można go też puszczać osobno.
set -euo pipefail
cd "$(dirname "$0")/.."
NOTIFY=1; DRY=""
while [[ "${1:-}" == --* ]]; do case "$1" in --no-notify) NOTIFY=0;; --dry-notify) DRY="--dry";; *) echo "nieznana opcja $1" >&2; exit 2;; esac; shift; done
MSG="${1:-Publikacja $(date '+%Y-%m-%d %H:%M %Z')}"
NOTIFIER=/workspace/eve-push/scripts/notify_new_content.mjs

git checkout -- scripts/__pycache__ 2>/dev/null || true
git pull --rebase --autostash -q || { echo "pull --rebase: konflikt — rozwiąż ręcznie (zachowaj obie strony), nic nie wypchnięto" >&2; exit 1; }
python3 scripts/build.py
git checkout -- scripts/__pycache__ 2>/dev/null || true
git add -A -- . ':(exclude)scripts/__pycache__'
if git diff --cached --quiet; then
  echo "Brak zmian do wypchnięcia."
else
  git commit -q -m "$MSG"
  for i in 1 2 3; do
    git push -q && break
    [ "$i" = 3 ] && { echo "push nieudany 3 razy" >&2; exit 1; }
    git pull --rebase --autostash -q || { echo "konflikt przy ponownym pull --rebase — rozwiąż ręcznie" >&2; exit 1; }
  done
  echo "Wypchnięto: $(git log -1 --format='%h %s')"
fi
if [ "$NOTIFY" = 1 ]; then
  # GitHub Pages potrzebuje zwykle 1–3 min; notifier sam czeka (do 10 min), aż nowe adresy dadzą 200.
  node "$NOTIFIER" --site "$PWD" --wait 600 $DRY
fi
