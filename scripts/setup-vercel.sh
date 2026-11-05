#!/usr/bin/env bash
# One-shot production setup on Vercel, run from the project folder on a Mac that holds the videos in public/video:
#   1. links this folder to the project (creating it in the team if needed)
#   2. creates a public Blob store and connects it to the project
#   3. uploads every video the pages need (content/videos.txt) to the top level of the store
#   4. sets NEXT_PUBLIC_VIDEO_BASE and NEXT_PUBLIC_SITE_URL for production and preview
#   5. deploys to production and prints the live URL
# Needs: npm install done, and `npx vercel login` done once (it opens the browser). Safe to rerun: every step skips what exists.
#
#   SCOPE=<team slug or id>  PROJECT=<project name>  STORE=<blob store name>  SITE_URL=<public site url>  bash scripts/setup-vercel.sh
set -euo pipefail
cd "$(dirname "$0")/.."

SCOPE="${SCOPE:-team_BuSpFtRz63dFaW5yK4YvgvN8}"   # the Birdline team (vercel.com/birdline)
PROJECT="${PROJECT:-birdline-site}"
STORE="${STORE:-birdline-video}"
SITE_URL="${SITE_URL:-https://birdlinestudios.com}"
VC="npx --no-install vercel"

[ -d node_modules ] || { echo "Run npm install first."; exit 1; }
$VC whoami >/dev/null 2>&1 || { echo "Sign in first: npx vercel login"; exit 1; }
echo "Signed in as $($VC whoami 2>/dev/null)"

echo; echo "1/5  Linking this folder to project '$PROJECT' in '$SCOPE'"
$VC link --yes --scope "$SCOPE" --project "$PROJECT" >/dev/null
echo "     linked"

echo; echo "2/5  Blob store '$STORE'"
if $VC blob list --limit 1 >/dev/null 2>&1; then
  echo "     a store is already connected to the project"
else
  $VC blob create-store "$STORE" --access public --yes
  $VC env pull .env.local --yes >/dev/null 2>&1 || true   # the store's token for the CLI, kept out of git
fi

echo; echo "3/5  Uploading the videos (this is the slow part)"
existing=$($VC blob list --limit 1000 2>/dev/null || true)
n=0; skipped=0; missing=0; first_url=""
while IFS= read -r f; do
  [ -n "$f" ] || continue
  if [ ! -f "public/video/$f" ]; then missing=$((missing + 1)); echo "     not in public/video: $f"; continue; fi
  if printf '%s\n' "$existing" | grep -q "/$f"; then skipped=$((skipped + 1)); continue; fi
  echo "     → $f"
  out=$($VC blob put "public/video/$f" --pathname "$f" --access public --cache-control-max-age 2592000 2>&1) || { echo "$out"; exit 1; }
  [ -n "$first_url" ] || first_url=$(printf '%s' "$out" | grep -o 'https://[^ ]*vercel-storage.com/[^ ]*' | head -1 || true)
  n=$((n + 1))
done < content/videos.txt
echo "     uploaded $n, already there $skipped, missing locally $missing"
if [ -z "$first_url" ]; then
  first_url=$($VC blob list --limit 1 2>/dev/null | grep -o 'https://[^ ]*vercel-storage.com/[^ ]*' | head -1 || true)
fi
[ -n "$first_url" ] || { echo "Could not read the store's URL from the uploads; run: npx vercel blob list --limit 1"; exit 1; }
BASE="${first_url%/*}"
echo "     video base: $BASE"

echo; echo "4/5  Environment variables"
setvar() {  # name value: production + preview, added, or updated when it already exists
  for env in production preview; do
    if ! printf '%s' "$2" | $VC env add "$1" "$env" >/dev/null 2>&1; then
      printf '%s' "$2" | $VC env update "$1" "$env" --yes >/dev/null
    fi
  done
  echo "     $1 = $2"
}
setvar NEXT_PUBLIC_VIDEO_BASE "$BASE"
setvar NEXT_PUBLIC_SITE_URL "$SITE_URL"

echo; echo "5/5  Deploying to production"
$VC deploy --prod --yes
echo; echo "Done. Open a case study on the URL above and play a video; it should stream from $BASE"
