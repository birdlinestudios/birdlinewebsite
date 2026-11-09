// POST /api/blob/sync — copies a file from one of our own hosts into the video store under a given name.
//
// A maintenance hook, not a visitor feature: the site's videos live in the Blob store, and new web encodes are produced elsewhere
// (a Vercel Sandbox with ffmpeg, or a machine that can reach the store). This route lets that work land in the store without
// handing the store's write token around: it runs here, where BLOB_READ_WRITE_TOKEN already is.
//
//   headers: x-sync-key: <BLOB_SYNC_SECRET>      the project's env var; without it the route refuses everything
//   body:    { "src": "https://…", "name": "whoop-lewis.mp4", "contentType": "video/mp4" }
//   src must be on a Vercel Sandbox port (sb-<id>.vercel.run) or our own Blob store (a copy or a rename); anything else is refused.
//
// The deployment's own protection (Vercel Authentication) sits in front of this as well, so a caller also has to be signed in
// to the team — the Browser pane in a working session is.
import { NextResponse } from "next/server";
import { put } from "@vercel/blob";

export const runtime = "nodejs";
export const maxDuration = 60;

const ALLOWED_HOST = /(^|\.)vercel\.run$|(^|\.)vercel-sandbox\.com$|\.public\.blob\.vercel-storage\.com$/;   // a sandbox port is served at sb-<id>.vercel.run
const NAME = /^[A-Za-z0-9][A-Za-z0-9._ ()-]{0,180}\.(mp4|mov|webm|mp3|m4a|jpg|jpeg|png|webp)$/;

export async function POST(req: Request) {
  const secret = process.env.BLOB_SYNC_SECRET;
  if (!secret || req.headers.get("x-sync-key") !== secret) {
    return NextResponse.json({ ok: false, error: "Not allowed." }, { status: 401 });
  }
  let body: { src?: unknown; name?: unknown; contentType?: unknown };
  try {
    body = (await req.json()) as typeof body;
  } catch {
    return NextResponse.json({ ok: false, error: "Send JSON." }, { status: 400 });
  }
  const src = typeof body.src === "string" ? body.src : "";
  const name = typeof body.name === "string" ? body.name.trim() : "";
  const contentType = typeof body.contentType === "string" ? body.contentType : "video/mp4";
  let url: URL;
  try {
    url = new URL(src);
  } catch {
    return NextResponse.json({ ok: false, error: "src is not a URL." }, { status: 400 });
  }
  if (url.protocol !== "https:" || !ALLOWED_HOST.test(url.hostname)) {
    return NextResponse.json({ ok: false, error: "src must be on a Vercel Sandbox or the store." }, { status: 400 });
  }
  if (!NAME.test(name) || name.includes("/")) {
    return NextResponse.json({ ok: false, error: "name must be a plain file name." }, { status: 400 });
  }
  const res = await fetch(url);
  if (!res.ok || !res.body) {
    return NextResponse.json({ ok: false, error: `The source answered ${res.status}.` }, { status: 502 });
  }
  const blob = await put(name, res.body, { access: "public", addRandomSuffix: false, allowOverwrite: true, contentType });
  const size = Number(res.headers.get("content-length") || 0);
  console.log(`[blob/sync] ${name} <- ${url.hostname} (${size} bytes)`);
  return NextResponse.json({ ok: true, url: blob.url, pathname: blob.pathname, size });
}
