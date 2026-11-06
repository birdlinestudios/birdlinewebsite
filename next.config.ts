import type { NextConfig } from "next";

// Everything the site serves is static: the pages are pre-rendered at build time from content/, the images and videos are files
// under public/. Every image name carries its content hash (the generator renames them, and the pages point at the hashed
// names), so a replaced image is a new address and the files can be cached for good. The videos under public/ are only used
// locally; in production they come from the Blob store.
const IMAGES = "public, max-age=31536000, immutable";
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
