"use client";

import Script from "next/script";
import { useEffect } from "react";

declare global {
    interface Window {
        goatcounter?: {
            count: (vars: { path: string; title: string; event: boolean }) => void;
        };
    }
}

export function GoatCounterTracker() {
    useEffect(() => {
        const handleClick = (e: MouseEvent) => {
            const target = e.target as HTMLElement | null;
            if (!target) return;

            // Try to find the closest interactive element, otherwise fall back to the raw target
            const interactiveEl = target.closest('a, button, input, select, textarea, [role="button"]') as HTMLElement | null;
            const elToTrack = interactiveEl || target;

            // Extract meaningful text or fallback to tag name/id
            const rawText = elToTrack.innerText || elToTrack.getAttribute("aria-label") || elToTrack.getAttribute("alt") || elToTrack.tagName;

            // Clean up the text for logging
            const text = rawText.substring(0, 30).trim().replace(/\s+/g, "-");

            let path = `click/${elToTrack.tagName.toLowerCase()}`;
            if (elToTrack.id) {
                path += `/#${elToTrack.id}`;
            } else if (text) {
                path += `/${text}`;
            }

            if (window.goatcounter && typeof window.goatcounter.count === "function") {
                window.goatcounter.count({
                    path: path,
                    title: `Click: ${text || elToTrack.tagName.toLowerCase()}`,
                    event: true,
                });
            }
        };

        document.addEventListener("click", handleClick);

        return () => {
            document.removeEventListener("click", handleClick);
        };
    }, []);

    return (
        <Script
            strategy="afterInteractive"
            data-goatcounter="https://mvfashion.goatcounter.com/count"
            src="//gc.zgo.at/count.js"
        />
    );
}
