// /sitemap.xml: every page the generator wrote (content/pages.json), for Search Console. No lastmod: every deploy rebuilds every
// page, so a build time would say nothing about when a page's content changed.
import type { MetadataRoute } from "next";
import { pages } from "@/lib/content";
import { SITE_URL } from "@/lib/site";

const priority = (route: string) =>
  route === "/" ? 1 : /^\/(work|case-studies|services|packages)/.test(route) ? 0.8 : /^\/(privacy|terms|support|data-deletion)$/.test(route) ? 0.3 : 0.6;

export default function sitemap(): MetadataRoute.Sitemap {
  return pages().map((p) => ({
    url: new URL(p.route, SITE_URL).href,
    changeFrequency: p.route.startsWith("/blog/") ? "monthly" : "weekly",
    priority: priority(p.route),
  }));
}
