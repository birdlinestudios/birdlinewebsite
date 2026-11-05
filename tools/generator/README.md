# The site generator

Python scripts that write the Birdline site's content from a handful of source files. From the project root:

```bash
npm run content
# = BIRDLINE_NEXT=. python3 tools/generator/site/build_site.py tools/generator/assets .generator-out
```

`build_site.py` builds the classic static site into `.generator-out/` (ignored by git; kept for reference and for the
claude.ai artifact of the design) and, because `BIRDLINE_NEXT` points at the project, also writes what the Next.js app
renders: `content/pages/*.html`, `content/pages.json`, `content/chrome.json`, `content/videos.txt`, `app/globals.css`,
`public/js/birdline.js` and `public/img/`.

| File | Holds |
| --- | --- |
| `body.html` | The homepage markup, including the header (with its menus) and the footer used on every page. Links carry `data-page="/work"` etc.; the generator turns them into routes. Images are `data-img="<key>"` → `assets/<key>.<ext>`. |
| `style.css`, `script.js` | Styles and behaviours shared by all pages (menus, marquee, calculator, in-page scrolling). |
| `assets/` | The homepage's images, by key. |
| `site/build_site.py` | The build: pages, galleries, image copying, video references, the Next.js output. |
| `site/content.json` | The original case-study copy and portfolio items pulled from the previous site. |
| `site/extras.py` | Everything written since: the Willie's Remedy, EDJY and UFL case studies, videos added per brand (`ADDED_WORK`), the Packages, the team, FAQs, the order of the case studies. |
| `site/services.py`, `rops.py`, `production.py`, `why.py` | The Services, ROPS & ROCS, Production Process and Why Birdline pages' copy. |
| `site/site.css`, `site/site.js` | Styles and behaviours of the non-homepage pages (galleries, lightbox, carousels, radio player). |
| `site/spa.js` | The hash router used only by the claude.ai artifact; not part of the Next.js site. |
| `site/img/` + `site/img_map.json` | Every image used outside the homepage, with its size. |
| `site/video_index.tsv` | The Vimeo library: id, brand folder, title, size, length. A Vimeo id with a row here plays from `/video/<id>.mp4`. |

The videos themselves are not here: the generator only references them (`content/videos.txt`), and `public/video/` holds the
files on each machine.
