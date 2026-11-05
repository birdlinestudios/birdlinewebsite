# Birdline website on Next.js

The Birdline Studios site (`birdlinestudios.com`) as a [Next.js](https://nextjs.org) app, ready for Vercel.

- **`app/`** — the Next.js app (App Router). `layout.tsx` is the document every page shares (fonts, header, footer, media
  lightbox, scripts); `page.tsx` is the homepage; `[...slug]/page.tsx` renders every other route from `content/`;
  `not-found.tsx` is the 404 page; `globals.css` is the site's CSS; `icon.png` / `apple-icon.png` are the favicons.
- **`content/`** — the pages as generated HTML: `pages.json` (every route with its title and description),
  `pages/*.html` (the body of each page) and `chrome.json` (header, footer, lightbox). **Generated, don't hand-edit**:
  see "Changing the content" below.
- **`public/`** — files served as they are: `img/` (447 images), `video/` (the videos; not in git, see "Videos"),
  `js/birdline.js` (the site's scripts: menus, carousels, galleries, lightbox, calculator, radio player).
- **`lib/content.ts`** — reads `content/` at build time.
- **`tools/generator/`** — the Python generator that writes `content/`, `app/globals.css`, `public/js` and `public/img`
  from `body.html`, `content.json`, `extras.py` and friends. This is the source of truth for the copy and the galleries.
- **`scripts/upload-videos.sh`** — uploads the videos to Vercel Blob for production.

Routes: `/`, `/work`, `/case-studies`, `/case-studies/<brand>` (12), `/services`, `/services/<service>` (15, plus
`/services/production-process`), `/packages`, `/about`, `/production-workspace`, `/why-us`, `/rops`. Every route is
pre-rendered to static HTML at build time; nothing runs on a server per request.

---

## 1. Run it on your Mac

You need **Node.js 20.9 or newer** (the LTS from https://nodejs.org is fine; check with `node -v`).

```bash
cd ~/Downloads/birdline-next
npm install          # once; installs Next.js and React into node_modules/
npm run dev          # the development server
```

Open **http://localhost:3000**. Every page is there, links work, and any file you change is reflected in the browser
on save. Stop the server with `Ctrl+C`.

To try the exact build Vercel will serve:

```bash
npm run build        # pre-renders all 37 pages into .next/
npm start            # serves that build at http://localhost:3000
```

`npm run build` is also the check to run before pushing: if it fails here, the Vercel deploy would fail too.

### The Vercel CLI (optional)

```bash
npm i -g vercel      # once
vercel login
vercel link          # in this folder: creates/links the Vercel project (answer the prompts; defaults are right)
vercel dev           # Vercel's local server: same as npm run dev, plus any vercel.json rewrites/redirects you add later
```

For this site `npm run dev` and `vercel dev` behave the same; the CLI is needed for the Blob upload below and for deploying
from the terminal (`vercel` = preview deployment, `vercel --prod` = production).

---

## 2. Videos

The site plays 210 self-hosted videos (about 1.4 GB). They live in `public/video/` on your Mac for local work, and are
**not** committed to git: GitHub won't take files that size and Vercel's static upload limit is 100 MB on Hobby / 1 GB on
Pro. In production they are served from a Vercel Blob store instead (or any CDN folder that holds the same file names).

`content/videos.txt` lists every file the pages need. Locally, copy them in once:

```bash
cp ~/Downloads/birdline-site-selfhosted/video/* ~/Downloads/birdline-next/public/video/
```

For production (after `vercel login` and `vercel link`):

1. In the Vercel dashboard open the project → **Storage** → **Create** → **Blob**, access **public**, and connect it to the
   project. (Or from the terminal: `vercel blob create-store birdline-video --access public`.)
2. Upload, either way:
   - in the dashboard: open the store → **Upload**, select every file in `public/video` and drop them at the top level; or
   - `npm run videos:upload` — loops over `content/videos.txt` and `vercel blob put`s each file at the top level;
     re-running only sends files that are missing.
   Each file gets a URL like `https://abc123xyz.public.blob.vercel-storage.com/ufl-radio.mp3`.
3. In the project's **Settings → Environment Variables** add `NEXT_PUBLIC_VIDEO_BASE` =
   `https://abc123xyz.public.blob.vercel-storage.com` (everything before the file name) for Production and Preview,
   then redeploy. Every `/video/<file>` reference in the pages is rewritten to that base at build time.

Without the variable the site looks for the videos in `public/video/`, which is what you want on your Mac.

**Plan:** this needs the **Pro** plan ($20/month, with $20 of usage credit included). Hobby includes 1 GB of Blob storage
and 10 GB of transfer a month and simply stops serving blobs for 30 days once either is exceeded, and it is for
non-commercial use anyway. On Pro, Blob is metered at roughly $0.023 per GB stored per month (1.4 GB ≈ 3¢) and $0.05 per
GB transferred, so a thousand visitors each watching 100 MB of video is about $5; Vercel's CDN caches public blobs up
to 512 MB each, so repeat views come from the edge. Any individual file can be up to 5 TB, so the library can grow.
If the bill ever matters, any object store with cheap egress (Cloudflare R2, Bunny) works the same way, since all the
site needs is a folder of the same file names.

---

## 3. Put it on Vercel

**Fastest: the one-shot script.** From the project folder, with `npm install` done and the videos in `public/video`:

```bash
npx vercel login            # once; opens the browser
npm run vercel:setup        # links the project (creating it in the team), creates the Blob store, uploads the videos,
                            # sets the environment variables, deploys to production and prints the live URL
```

It is safe to rerun: each step skips what already exists. `scripts/setup-vercel.sh` has the details; `SCOPE`, `PROJECT`,
`STORE` and `SITE_URL` can be overridden as environment variables. After that, every later release is `npx vercel --prod`
(or connect GitHub in the project's Git settings for push-to-deploy).

**Alternatively, deploy from GitHub.** Every push to `main` becomes the production site; every branch or pull request gets
its own preview URL to review before merging.

1. Make it a git repository and push it to a **private** GitHub repository (GitHub Desktop works; or in the terminal):
   ```bash
   cd ~/Downloads/birdline-next
   git init && git add -A && git commit -m "Birdline site on Next.js"
   gh repo create birdline-site --private --source=. --push      # or create the repo on github.com and `git remote add origin …`
   ```
   `.gitignore` already keeps `node_modules/`, `.next/`, `public/video/` and `.env*.local` out of the repository.
2. On https://vercel.com → **Add New… → Project** → import the repository. Vercel detects Next.js; keep the defaults
   (build command `next build`, output `.next`) and press **Deploy**. The first deployment is live in a couple of minutes at
   `https://<project>.vercel.app`.
3. **Settings → Environment Variables**: add `NEXT_PUBLIC_VIDEO_BASE` (see Videos) and `NEXT_PUBLIC_SITE_URL`
   (`https://birdlinestudios.com`, used for social-sharing metadata). `NEXT_PUBLIC_*` values are baked in at build time, so
   redeploy after changing one (Deployments → ⋯ → Redeploy).
4. **Settings → Domains**: add `birdlinestudios.com` and `www.birdlinestudios.com`, then set the DNS records Vercel shows
   at your registrar (an A record for the apex, a CNAME for www). Vercel issues the TLS certificate itself. Keep the old
   site up until the new one answers on the domain; the switch is just the DNS change.

**Alternative: deploy from the terminal** with the CLI: `vercel` makes a preview deployment, `vercel --prod` the
production one. The CLI respects `.gitignore`, so the videos are never uploaded as part of a deployment.

### Day to day

- Work on a branch, push, open a pull request → Vercel comments with a preview URL → merge to `main` → production.
- Rolling back is one click: Deployments → the previous one → **Promote to Production** (or **Instant Rollback**).
- The dashboard's **Analytics** tab works after `npm i @vercel/analytics` and adding `<Analytics />` to `app/layout.tsx`;
  **Speed Insights** likewise with `@vercel/speed-insights`.

---

## 4. Developing the site

### Changing the content

The copy, the case studies, the services, the packages and the galleries are written in `tools/generator/` and generated
into `content/`:

| What | Where |
| --- | --- |
| Homepage sections, header menus, footer | `tools/generator/body.html` |
| Case studies, added videos per brand, packages, team, FAQs | `tools/generator/site/extras.py` (and `content.json` for the original case-study copy) |
| Services pages | `tools/generator/site/services.py` |
| ROPS & ROCS page, Production Process page, Why Birdline page | `rops.py`, `production.py`, `why.py` |
| Styles | `tools/generator/style.css` (homepage + shared) and `site/site.css` (the other pages) |
| Scripts | `tools/generator/script.js` and `site/site.js` |
| Images | `tools/generator/assets/` (homepage, by key) and `site/img/` + `site/img_map.json` (everything else) |
| Videos | `site/video_index.tsv` (the Vimeo library) and the file-backed items in `extras.py` |

After an edit, regenerate (needs Python 3, which macOS has):

```bash
npm run content
```

That rewrites `content/`, `app/globals.css`, `public/js/birdline.js` and `public/img/`; the dev server picks the change up
immediately. Commit the generated files along with the source so Vercel builds without Python.

Editing `content/pages/*.html` directly works for a quick experiment, but the next `npm run content` overwrites it.

### Adding a video

Transcode for the web (H.264, long edge 1280, AAC audio, `-movflags +faststart`), put the `.mp4` in `public/video/`, add a
poster to `tools/generator/site/img/` + `img_map.json`, add the item to the brand's list in `extras.py` (`ADDED_WORK` or
the case's `gal`), run `npm run content`, then `npm run videos:upload` before the production deploy.

### Moving pages to React

Every page is a generated HTML fragment rendered by `app/[...slug]/page.tsx`. To rebuild one in React, add a real route
folder, e.g. `app/packages/page.tsx`: Next.js prefers it over the catch-all. The CSS classes in `app/globals.css` and the
behaviours in `public/js/birdline.js` keep working on the markup you write, so a page can move over piece by piece. Links
can stay plain `<a>` tags (the scripts re-run on each page load); switch to `next/link` once a page no longer relies on
`birdline.js` for its interactions.

### Fonts

The site loads Host Grotesk and Inter from Google Fonts, as the current site does. To self-host them (no third-party
request, no layout shift), switch `app/layout.tsx` to `next/font`:

```tsx
import { Host_Grotesk, Inter } from "next/font/google";
const display = Host_Grotesk({ subsets: ["latin"], weight: ["600", "700"] });
const text = Inter({ subsets: ["latin"], weight: ["400", "500", "600", "700"] });
// then on <html>: style={{ "--display": `${display.style.fontFamily}, system-ui, sans-serif`,
//                        "--text": `${text.style.fontFamily}, system-ui, sans-serif` } as React.CSSProperties}
// and drop the two <link> tags from <head>.
```

### Scripts

```
npm run dev            development server, http://localhost:3000
npm run build          production build (what Vercel runs)
npm start              serve the production build locally
npm run typecheck      TypeScript check
npm run content        regenerate content/, globals.css, public/js and public/img from tools/generator
npm run videos:upload  upload public/video to the project's Vercel Blob store
```
