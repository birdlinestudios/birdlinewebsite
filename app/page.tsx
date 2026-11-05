// The homepage: content/pages/index.html, rendered inside the shared header and footer from app/layout.tsx.
import type { Metadata } from "next";
import { page } from "@/lib/content";

const home = () => page("/")!;

export function generateMetadata(): Metadata {
  const p = home();
  return { title: p.title, description: p.description };
}

export default function HomePage() {
  return <main dangerouslySetInnerHTML={{ __html: home().html }} />;
}
