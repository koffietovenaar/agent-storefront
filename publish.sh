#!/usr/bin/env bash
# One-shot publisher for the agent storefront.
# Prereq (owner, once): HOME=/opt/hermes-business/workspace gh auth login
#   (device-code flow in your own shell; agent PTY input does not work)
# Then run:  bash publish.sh   (safe to re-run)
set -euo pipefail
export HOME=/opt/hermes-business/workspace
export PATH=/opt/hermes-business/workspace/.npm-global/bin:$PATH
cd "$(dirname "$0")"

gh auth status >/dev/null 2>&1 || { echo "gh not authenticated — run: gh auth login"; exit 1; }

USER=$(gh api user -q .login)
REPO=agent-storefront
git add -A && git commit -m "Storefront update" 2>/dev/null || true

if ! gh repo view "$USER/$REPO" >/dev/null 2>&1; then
  gh repo create "$REPO" --public --source=. --push \
    --description "Machine-readable index of fixed-scope AI-fulfilled micro-services (escrow-only)"
else
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$USER/$REPO.git"
  git push -u origin main
fi

# Enable GitHub Pages from main branch root (idempotent)
gh api -X POST "repos/$USER/$REPO/pages" -f 'source[branch]=main' -f 'source[path]=/' 2>/dev/null \
  || gh api -X PUT "repos/$USER/$REPO/pages" -f 'source[branch]=main' -f 'source[path]=/' 2>/dev/null \
  || true
echo "Published: https://$USER.github.io/$REPO/  (Pages may take ~1 min to build)"
