import { test, expect } from '@playwright/test';

test.describe('MV-Fashion React Hydration Tests', () => {
    test('no hydration errors on home page', async ({ page }) => {
        const errors: string[] = [];
        page.on('pageerror', (err) => {
            errors.push(err.message);
        });

        page.on('console', (msg) => {
            if (msg.type() === 'error' && (msg.text().includes('hydration') || msg.text().includes('Hydration'))) {
                errors.push(msg.text());
            }
        });

        await page.goto('/');

        // Wait slightly for any delayed hydration errors
        await page.waitForTimeout(2000);

        expect(errors).toEqual([]);
    });

    test('no hydration errors on request data page', async ({ page }) => {
        const errors: string[] = [];
        page.on('pageerror', (err) => {
            errors.push(err.message);
        });

        page.on('console', (msg) => {
            if (msg.type() === 'error' && (msg.text().includes('hydration') || msg.text().includes('Hydration'))) {
                errors.push(msg.text());
            }
        });

        await page.goto('/request-data');
        await page.waitForTimeout(2000);

        expect(errors).toEqual([]);
    });
});
