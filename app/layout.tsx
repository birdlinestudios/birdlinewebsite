// The document every page shares: the fonts, the site's CSS (app/globals.css), the header, the page itself (<main>, from each
// route's page.tsx), the footer, the media lightbox, the booking modal, and the site's scripts (public/js/birdline.js), which run
// after the page is on screen. The header, footer, lightbox and modal come from content/chrome.json as the generator wrote them.
import type { Metadata, Viewport } from "next";
import Script from "next/script";
import { SpeedInsights } from "@vercel/speed-insights/next";
import { createElement } from "react";
import { chrome, type Part } from "@/lib/content";
import "./globals.css";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://birdlinestudios.com";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: "Birdline",
  openGraph: { siteName: "Birdline", type: "website", locale: "en_US" },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: "#0f1a4a",
};

// One of the shared parts, rendered as the element the generator wrote (its tag and attributes) with its HTML inside.
function Fragment({ part }: { part: Part }) {
  return createElement(part.tag, { ...part.attrs, dangerouslySetInnerHTML: { __html: part.html } });
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const c = chrome();
  return (
    <html lang="en">
      <head>
        {c.fonts.map((href) => (
          <link key={href} rel="preload" href={href} as="font" type="font/woff2" crossOrigin="anonymous" />
        ))}
      </head>
      <body>
        <div className="page">
          <Fragment part={c.topMark} />
          <Fragment part={c.header} />
          {children}
          <Fragment part={c.footer} />
          <Fragment part={c.lightbox} />
          <Fragment part={c.book} />
        </div>
        <Script src="/js/birdline.js" strategy="afterInteractive" />
        <SpeedInsights />
      </body>
    </html>
  );
}
