"use client";

import * as React from "react";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

export function ThemeToggle() {
    const [mounted, setMounted] = React.useState(false);
    const { setTheme, resolvedTheme } = useTheme();

    React.useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) {
        return (
            <button
                className="fixed top-4 right-4 z-40 p-2 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-800 dark:text-slate-200 opacity-0"
                aria-label="Toggle theme"
            >
                <div className="h-[1.2rem] w-[1.2rem]" />
            </button>
        );
    }

    return (
        <button
            onClick={() => setTheme(resolvedTheme === "light" ? "dark" : "light")}
            className="fixed top-4 right-4 z-40 p-2 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-800 dark:text-slate-200 hover:bg-slate-300 dark:hover:bg-slate-700 transition-colors shadow-lg border border-slate-300 dark:border-slate-700"
            aria-label="Toggle theme"
            aria-pressed={resolvedTheme === "dark"}
        >
            <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100 top-2 left-2" />
        </button>
    );
}
