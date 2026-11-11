// The address the site is served from, for every absolute URL in the metadata (the Open Graph cards, the canonical links), the
// sitemap and robots.txt: the domain Vercel serves production from (VERCEL_PROJECT_PRODUCTION_URL: the project's vercel.app domain
// until a custom domain is attached, then that — www.birdlinestudios.com since November 10, 2026), or NEXT_PUBLIC_SITE_URL where
// that is not set (a local build).
export const SITE_URL = process.env.VERCEL_PROJECT_PRODUCTION_URL
  ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
  : process.env.NEXT_PUBLIC_SITE_URL || "https://birdlinestudios.com";
