// Every page but the homepage: /work, /case-studies, /case-studies/<brand>, /services, /services/<service>, /packages, /about,
// /production-workspace, /why-us and /rops. The routes come from content/pages.json, so a page added to the generator appears here
// on the next build with no change to the app. To hand-build one page in React instead, add app/<route>/page.tsx: a real route
// folder wins over this catch-all.
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { page, pages } from "@/lib/content";

type Props = { params: Promise<{ slug: string[] }> };

export const dynamicParams = false; // only the routes in pages.json exist; anything else is a 404

export function generateStaticParams() {
  return pages()
    .filter((p) => p.route !== "/")
    .map((p) => ({ slug: p.route.slice(1).split("/") }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const p = page("/" + slug.join("/"));
  return p ? { title: p.title, description: p.description } : {};
}

export default async function SitePage({ params }: Props) {
  const { slug } = await params;
  const p = page("/" + slug.join("/"));
  if (!p) notFound();
  return <main dangerouslySetInnerHTML={{ __html: p.html }} />;
}
