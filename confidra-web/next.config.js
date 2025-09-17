/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  },
  // Remove rewrites for now to avoid proxy issues
  // We'll handle API calls directly from the frontend
}

module.exports = nextConfig
