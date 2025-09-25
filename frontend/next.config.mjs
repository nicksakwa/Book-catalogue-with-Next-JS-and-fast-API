/** @type {import('next').NextConfig} */
const nextConfig = {
    // This is required for Next.js to be properly served in the Docker container
    output: 'standalone', 
};

export default nextConfig;