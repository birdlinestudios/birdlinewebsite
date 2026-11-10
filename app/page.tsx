// The homepage: content/pages/index.html, rendered inside the shared header and footer from app/layout.tsx.
import type { Metadata } from "next";
import { page } from "@/lib/content";
import { pageMetadata } from "@/lib/metadata";

const home = () => page("/")!;

export function generateMetadata(): Metadata {
  return pageMetadata(home());
}

export default function HomePage() {
  return <main dangerouslySetInnerHTML={{ __html: home().html }} />;
}
