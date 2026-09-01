#!/usr/bin/env bash
# Rebuild, run the deploy checklist, then push.
#
#   ./deploy.sh            check only, never pushes
#   ./deploy.sh --push     check, then commit and push if the checks pass
#
# The checklist is the one in ~/CLAUDE.md: favicon, OG tags with an absolute
# og:image, breadcrumbs, local preview, pushed. This script enforces the parts
# a machine can check. It cannot check that you looked at the page, so it
# refuses to push until you confirm.

set -euo pipefail
cd "$(dirname "$0")"

PUSH=0
[[ "${1:-}" == "--push" ]] && PUSH=1

echo "── build ─────────────────────────────────────────"
python3 build.py --strict

echo
echo "── deploy checklist ──────────────────────────────"
fail=0
note() { printf '  %-6s %s\n' "$1" "$2"; }

pages=(index.html students.html courses/*.html)

# 0. GitHub Pages runs Jekyll, which refuses to publish any directory whose
#    name starts with "_". Without .nojekyll the whole of _kit/ 404s live and
#    the site renders unstyled, while every local check still passes.
if [[ -f .nojekyll ]]; then
  note "ok" ".nojekyll present (publishes _kit/)"
else
  note "FAIL" ".nojekyll missing — _kit/ will 404 on GitHub Pages"; fail=1
fi

# 1. custom favicon, themed, not generic
if [[ -f favicon.svg ]] && grep -q '마' favicon.svg; then
  note "ok" "custom SVG favicon"
else
  note "FAIL" "favicon.svg missing or not themed"; fail=1
fi

# 2-4. meta tags on every page, og:image absolute
for page in "${pages[@]}"; do
  for tag in 'og:title' 'og:description' 'og:image' 'og:url' 'og:type' 'twitter:card' 'twitter:image'; do
    grep -q "\"$tag\"" "$page" || { note "FAIL" "$page missing $tag"; fail=1; }
  done
  og=$(grep -o 'property="og:image" content="[^"]*"' "$page" | sed 's/.*content="//;s/"//')
  if [[ "$og" != https://* ]]; then
    note "FAIL" "$page og:image is not an absolute URL: $og"; fail=1
  fi
done
[[ $fail -eq 0 ]] && note "ok" "OG + Twitter tags on ${#pages[@]} pages, og:image absolute"

# 5. breadcrumb on every sub-page, no orphans
for page in courses/*.html; do
  grep -q 'class="breadcrumb"' "$page" || { note "FAIL" "$page has no breadcrumb"; fail=1; }
  basename_page=$(basename "$page")
  linked=0
  for source in index.html students.html courses/*.html; do
    [[ "$source" == "$page" ]] && continue
    if grep -qE "href=\"([^\"]*/)?${basename_page}([#?][^\"]*)?\"" "$source"; then
      linked=1
      break
    fi
  done
  if [[ $linked -eq 0 ]]; then
    note "FAIL" "$page is an orphan (no generated navigation links it)"; fail=1
  fi
done
[[ $fail -eq 0 ]] && note "ok" "breadcrumbs present, every course page linked from the student or instructor surface"

# 6. every local asset resolves on disk
missing=0
for page in "${pages[@]}"; do
  dir=$(dirname "$page")
  while read -r ref; do
    [[ -z "$ref" ]] && continue
    ref="${ref%%\?*}"
    [[ -f "$dir/$ref" ]] || { note "FAIL" "$page -> $ref not found"; missing=1; }
  done < <(grep -oE '(src|href)="[^":]+"' "$page" | sed 's/.*="//;s/"//' | grep -v '^#')
done
[[ $missing -eq 0 ]] && note "ok" "all local assets resolve" || fail=1

echo
if [[ $fail -ne 0 ]]; then
  echo "checklist FAILED — not pushing."
  exit 1
fi
echo "checklist passed."

if [[ $PUSH -eq 0 ]]; then
  echo
  echo "Preview locally, then push:"
  echo "  python3 -m http.server 8765   # then open http://localhost:8765/"
  echo "  ./deploy.sh --push"
  exit 0
fi

echo
read -r -p "Did you open the site locally and approve it? [y/N] " ok
[[ "$ok" == "y" || "$ok" == "Y" ]] || { echo "Not pushing. Preview first."; exit 1; }

git add -A
git commit -m "${COMMIT_MSG:-Rebuild Fall 2026 teaching site from data/}" || echo "nothing to commit"
git push
echo
echo "pushed. live shortly at:"
python3 -c "import json;print(' ', json.load(open('data/term.json'))['hqUrl'])"
