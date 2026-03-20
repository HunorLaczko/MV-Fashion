import { BASE_PATH, SITE_URL } from './basePath.generated';

export function withBasePath(path: string): string {
  if (!path) return BASE_PATH || '/';

  if (/^https?:\/\//i.test(path) || path.startsWith('//')) {
    return path;
  }

  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${BASE_PATH}${normalizedPath}`;
}

export function getSiteUrl(): string {
  return SITE_URL;
}
