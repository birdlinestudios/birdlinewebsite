import type { NextConfig } from "next";

// Everything the site serves is static: the pages are pre-rendered at build time from content/, the images and videos are files
// under public/. The headers below let browsers keep those files for a day and reuse them for a week while they re-check.
const LONG = "public, max-age=86400, stale-while-revalidate=604800";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  async headers() {
    return [
      { source: "/img/:path*", headers: [{ key: "Cache-Control", value: LONG }] },
      { source: "/video/:path*", headers: [{ key: "Cache-Control", value: LONG }] },
    ];
  },
};

export default nextConfig;
