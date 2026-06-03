import type { NextConfig } from "next";
const nextConfig: NextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  env: {
    NEXT_PUBLIC_API_URL: "https://churchhub-api-o91c.onrender.com/api/v1",
  },
};
export default nextConfig;
