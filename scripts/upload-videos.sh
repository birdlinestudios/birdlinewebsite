#!/usr/bin/env bash
# Uploads the site's videos (every file listed in content/videos.txt that exists in public/video) to the project's Vercel Blob store,
# at the top level, so NEXT_PUBLIC_VIDEO_BASE is the store's own URL, https://<store>.public.blob.vercel-storage.com
#
# Before running: npm i -g vercel; vercel login; vercel link (in this folder); a Blob store connected to the project
# (Vercel dashboard → Storage → Create → Blob, or: vercel blob create-store birdline-video --access public).
# Re-running only re-uploads files that are missing from the store or changed in size.
set -euo pipefail
cd "$(dirname "$0")/.."

command -v vercel >/dev/null || { echo "Install the Vercel CLI first (npm install adds it to node_modules; or npm i -g vercel)"; exit 1; }
[ -f content/videos.txt ] || { echo "content/videos.txt is missing: run npm run content"; exit 1; }

echo "Listing what the store already holds..."
existing=$(vercel blob list --limit 1000 2>/dev/null || true)

n=0; skipped=0; missing=0
while IFS= read -r f; do
  [ -n "$f" ] || continue
  if [ ! -f "public/video/$f" ]; then missing=$((missing + 1)); continue; fi
  if printf '%s\n' "$existing" | grep -q "/$f"; then skipped=$((skipped + 1)); continue; fi
  echo "→ $f"
  vercel blob put "public/video/$f" --pathname "$f" --access public --cache-control-max-age 2592000
  n=$((n + 1))
done < content/videos.txt

echo
echo "uploaded $n, already there $skipped, not in public/video $missing"
echo "Set NEXT_PUBLIC_VIDEO_BASE to the store's public URL (a printed URL above, without the file name)."
