import type { NextConfig } from "next";

// Everything the site serves is static: the pages are pre-rendered at build time from content/, the images and videos are files
// under public/. Image names stay the same when an image is replaced, so browsers keep them for an hour and then re-check
// (a cheap 304 when nothing changed); the videos under public/ are only used locally, so they can be kept longer.
const IMAGES = "public, max-age=3600, stale-while-revalidate=86400";
const VIDEOS = "public, max-age=86400, stale-while-revalidate=604800";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  async headers() {
    return [
      { source: "/img/:path*", headers: [{ key: "Cache-Control", value: IMAGES }] },
      { source: "/video/:path*", headers: [{ key: "Cache-Control", value: VIDEOS }] },
    ];
  },
};

export default nextConfig;
