// The <head> metadata of a page: its title and description, and the Open Graph and Twitter cards that Slack, iMessage, LinkedIn
// and X show for a shared link, and the canonical link. The card image is the page's own, drawn by the generator
// (content/pages.json names it under public/og/); the URLs are made absolute against metadataBase (app/layout.tsx), which is the
// domain the site is served from (lib/site.ts).
import type { Metadata } from "next";
import type { Page } from "@/lib/content";

export function pageMetadata(p: Page): Metadata {
  const images = p.image ? [{ url: p.image, width: 1200, height: 630, alt: p.title }] : [];
  return {
    title: p.title,
    description: p.description,
    alternates: { canonical: p.route },
    openGraph: { siteName: "Birdline", type: "website", locale: "en_US", url: p.route, title: p.title, description: p.description, images },
    twitter: { card: "summary_large_image", title: p.title, description: p.description, images: images.map((i) => i.url) },
  };
}
