// The site's content, as tools/generator writes it into content/:
//   content/pages.json      every route with its fragment file, <title> and meta description
//   content/pages/*.html    the inner HTML of each page's <main>, links already written as routes (/work, /case-studies/ufl ...)
//   content/chrome.json     the header, footer and lightbox shared by every page, and the Google Fonts links
// Everything is read at build time (next build pre-renders every route), so nothing here runs on a request in production.
import fs from "node:fs";
import path from "node:path";

export type Page = { route: string; file: string; title: string; description: string };
export type Part = { tag: string; attrs: Record<string, string>; html: string };
export type Chrome = { fonts: string[]; topMark: Part; header: Part; footer: Part; lightbox: Part };

const CONTENT = path.join(process.cwd(), "content");
const read = (file: string) => fs.readFileSync(path.join(CONTENT, file), "utf8");

let pagesCache: Page[] | undefined;
export function pages(): Page[] {
  return (pagesCache ??= JSON.parse(read("pages.json")) as Page[]);
}

export function page(route: string): (Page & { html: string }) | null {
  const p = pages().find((x) => x.route === route);
  return p ? { ...p, html: withMedia(read(path.join("pages", p.file))) } : null;
}

let chromeCache: Chrome | undefined;
export function chrome(): Chrome {
  return (chromeCache ??= JSON.parse(read("chrome.json")) as Chrome);
}

// Videos are served from public/video/ unless NEXT_PUBLIC_VIDEO_BASE points somewhere else (a Vercel Blob store or any CDN folder
// holding the same file names), in which case every /video/<file> reference in the pages is rewritten to that base.
const VIDEO_BASE = (process.env.NEXT_PUBLIC_VIDEO_BASE || "").replace(/\/+$/, "");
export function withMedia(html: string): string {
  return VIDEO_BASE ? html.replaceAll('="/video/', `="${VIDEO_BASE}/`) : html;
}
