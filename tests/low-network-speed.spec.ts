import { test, expect } from '@playwright/test';

test.describe('Low-speed internet load speed', () => {
    test.skip(({ browserName }) => browserName !== 'chromium', 'Network throttling uses Chromium CDP APIs.');

    test('home page remains usable on slow 3G profile', async ({ page }) => {
        const cdpSession = await page.context().newCDPSession(page);

        await cdpSession.send('Network.enable');
        await cdpSession.send('Network.setCacheDisabled', { cacheDisabled: true });
        await cdpSession.send('Network.emulateNetworkConditions', {
            offline: false,
            latency: 400,
            downloadThroughput: (500 * 1024) / 8,
            uploadThroughput: (500 * 1024) / 8,
            connectionType: 'cellular3g',
        });

        const navigationStart = Date.now();
        const response = await page.goto('/', { waitUntil: 'domcontentloaded', timeout: 60000 });
        const domReadyDurationMs = Date.now() - navigationStart;

        expect(response?.ok()).toBeTruthy();
        await expect(page.locator('#main-content')).toBeVisible({ timeout: 30000 });
        expect(domReadyDurationMs).toBeLessThan(30000);

        const navMetrics = await page.evaluate(() => {
            const entry = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming | undefined;
            return entry
                ? {
                    domContentLoadedMs: entry.domContentLoadedEventEnd,
                    loadMs: entry.loadEventEnd,
                }
                : null;
        });

        expect(navMetrics).not.toBeNull();
        expect(navMetrics?.domContentLoadedMs ?? Number.POSITIVE_INFINITY).toBeLessThan(30000);
    });
});
