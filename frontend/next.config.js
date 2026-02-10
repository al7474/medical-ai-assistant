/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone', // For Docker builds
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ]
  },
}

module.exports = nextConfig
