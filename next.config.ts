import type { NextConfig } from 'next';

const repository = process.env.GITHUB_REPOSITORY;
const owner = process.env.GITHUB_REPOSITORY_OWNER;
const isGitHubActions = process.env.GITHUB_ACTIONS === 'true';
const isProduction = process.env.NODE_ENV === 'production';
const explicitBasePath = process.env.NEXT_PUBLIC_BASE_PATH;

const fallbackProjectBasePath = '/MV-Fashion';

const repoName = repository?.split('/')[1] ?? '';
const isUserOrOrgPage = !!owner && repoName.toLowerCase() === `${owner.toLowerCase()}.github.io`;
const basePathFromRepository = isGitHubActions && repoName && !isUserOrOrgPage ? `/${repoName}` : '';
const basePath = explicitBasePath
  || basePathFromRepository
  || (isProduction ? fallbackProjectBasePath : '');
const siteUrl = owner ? `https://${owner}.github.io${basePath}` : 'https://hunorlaczko.github.io/MV-Fashion';

const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: true,
  basePath,
  assetPrefix: basePath || undefined,
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  images: {
    unoptimized: true,
  },
  env: {
    NEXT_PUBLIC_BASE_PATH: basePath,
    NEXT_PUBLIC_SITE_URL: siteUrl,
  },
};

export default nextConfig;
