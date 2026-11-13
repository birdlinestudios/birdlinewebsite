// The document every page shares: the fonts, the site's CSS (app/globals.css), the header, the page itself (<main>, from each
// route's page.tsx), the footer, the media lightbox, the booking modal, and the site's scripts (public/js/birdline.js), which run
// after the page is on screen. The header, footer, lightbox and modal come from content/chrome.json as the generator wrote them.
import type { Metadata, Viewport } from "next";
import Script from "next/script";
import { SpeedInsights } from "@vercel/speed-insights/next";
import { GoogleAnalytics } from "@next/third-parties/google";
import { createElement } from "react";
import { chrome, type Part } from "@/lib/content";
import { SITE_URL } from "@/lib/site";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL), // every absolute URL in the metadata is made against this (lib/site.ts)
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
        {/* The Google tag for the GTM-5P37SSRM container, first in <head> as Google's install steps ask (November 10, 2026). The
            inline part is Google's own snippet, verbatim. */}
        <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-5P37SSRM" />
        <script
          dangerouslySetInnerHTML={{
            __html: "window.dataLayer = window.dataLayer || [];\nfunction gtag(){dataLayer.push(arguments);}\ngtag('js', new Date());",
          }}
        />
        {/* The Google tag for the Google Ads account (AW-18369278264), which Google Ads reads conversions through, in <head> as
            its install steps ask (November 12, 2026). Both parts are Google's own snippet, verbatim, so it repeats the dataLayer
            lines above; that is harmless. It is here as plain <script> tags because GoogleAnalytics below can only be used once
            (a second one shares its script ids and never loads) and loads after the page is interactive, not in <head>. */}
        <script async src="https://www.googletagmanager.com/gtag/js?id=AW-18369278264" />
        <script
          dangerouslySetInnerHTML={{
            __html:
              "window.dataLayer = window.dataLayer || [];\nfunction gtag(){dataLayer.push(arguments);}\ngtag('js', new Date());\n\ngtag('config', 'AW-18369278264');",
          }}
        />
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
        {/* GA4 (property 563739787) through gtag.js, wired directly rather than through the GTM container so it collects now. In-site
            navigations count as page views through the stream's enhanced measurement (page changes on history events, on by
            default). If a GA4 tag is ever added to GTM-5P37SSRM, take this out, or page views double. */}
        <GoogleAnalytics gaId="G-NYB8HESJB3" />
      </body>
    </html>
  );
}
