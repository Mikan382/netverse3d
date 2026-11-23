const roomMode =
  process.env.NEXT_PUBLIC_ROOM ?? (process.env.NODE_ENV === 'development' ? 'fake' : '');

const nextConfig = {
  env: { NEXT_PUBLIC_ROOM: roomMode },
  output: 'export',
  reactStrictMode: true,
  images: { unoptimized: true },
  ...(process.env.NODE_ENV === 'development'
    ? {
        rewrites: async () => [
          {
            source: '/api/identity/:path*',
            destination: `http://127.0.0.1:${process.env.GATEWAY_PORT ?? '58080'}/api/identity/:path*`,
          },
        ],
      }
    : {}),
};

export default nextConfig;
