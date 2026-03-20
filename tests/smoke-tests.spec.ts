import { test, expect } from '@playwright/test';

test.describe('MV-Fashion Website Smoke Tests', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/');
    });

    test('has title and key sections', async ({ page }) => {
        // Check the main title from Hero
        await expect(page).toHaveTitle(/MV-Fashion/);

        // Check for key sections that should be present
        const sections = [
            '#main-content',
            '#data',
            '#interactive-examples',
            '#video-examples',
            '#statistics',
            '#paper'
        ];

        for (const selector of sections) {
            await expect(page.locator(selector)).toBeVisible();
        }
    });

    test('theme toggle works and persists', async ({ page }) => {
        const toggle = page.getByLabel('Toggle theme');
        await expect(toggle).toBeVisible();

        // 1. Initial State Check (defaulting to dark in layout.tsx)
        const html = page.locator('html');
        // Because defaultTheme is "dark", html should have class "dark"
        // But we allow for system preference if user settings vary.
        // Let's toggle it.

        const isDarkInitial = await html.evaluate(el => el.classList.contains('dark'));

        // 2. Click button to change theme
        await toggle.click();
        const isDarkAfterClick = await html.evaluate(el => el.classList.contains('dark'));
        expect(isDarkAfterClick).not.toBe(isDarkInitial);

        // 3. Optional: Persistence check (if localStorage is used)
        await page.reload();
        const isDarkAfterReload = await html.evaluate(el => el.classList.contains('dark'));
        expect(isDarkAfterReload).toBe(isDarkAfterClick);
    });

    test('skip navigation works', async ({ page }) => {
        await page.keyboard.press('Tab');
        const skipLink = page.getByRole('link', { name: 'Skip to main content' });
        await expect(skipLink).toBeFocused();

        await page.keyboard.press('Enter');
        // After clicking skip link, URL should have fragment OR focus should move
        await expect(page).toHaveURL(/.*#main-content/);
    });

    test('navigation to request data page', async ({ page }) => {
        await page.getByRole('link', { name: /Get Dataset/ }).click();
        await expect(page).toHaveURL(/\/request-data/);

        const heading = page.getByRole('heading', { name: 'Request MV-Fashion Dataset' });
        await expect(heading).toBeVisible();

        // Check if Tally iframe is present
        const tallyIframe = page.locator('iframe[title="Request MV-Fashion Dataset"]');
        await expect(tallyIframe).toBeVisible();
    });

    test('copy citation clipboard feedback', async ({ page }) => {
        const copyBtn = page.getByTitle('Copy to clipboard');
        await expect(copyBtn).toBeVisible();

        await copyBtn.click();
        // Check for "Copied!" text appearing (it's animated now)
        await expect(page.getByText('Copied!')).toBeVisible();

        // Check persistence after wait
        await page.waitForTimeout(2100);
        await expect(page.getByText('Copied!')).toBeHidden();
        await expect(page.getByText('Copy')).toBeVisible();
    });
});
