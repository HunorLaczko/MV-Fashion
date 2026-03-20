"use client";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

export const COLORS = ["#6366f1", "#8b5cf6", "#ec4899", "#f43f5e", "#f59e0b", "#10b981", "#3b82f6", "#14b8a6", "#8b5cf6"];

interface CustomTooltipProps {
    active?: boolean;
    payload?: ReadonlyArray<{
        name?: string;
        value?: number | string;
    }>;
    label?: string | number;
    isPercentage?: boolean;
}

export const CustomTooltip = ({ active, payload, label, isPercentage }: CustomTooltipProps) => {
    if (active && payload && payload.length) {
        return (
            <div className="glass p-3 rounded-xl border border-slate-200 dark:border-white/10 shadow-xl bg-white/90 dark:bg-slate-900/90 backdrop-blur-md">
                <p className="text-slate-900 dark:text-white font-medium mb-1">{label || payload[0].name}</p>
                <p className="text-indigo-600 dark:text-indigo-300 text-sm">
                    {isPercentage ? "Percentage" : "Count"}: <span className="font-bold text-slate-900 dark:text-white">
                        {payload[0].value}{isPercentage ? "%" : ""}
                    </span>
                </p>
            </div>
        );
    }
    return null;
};

export function useChartTheme() {
    const { resolvedTheme } = useTheme();
    const [mounted, setMounted] = useState(false);
    useEffect(() => {
        const timer = setTimeout(() => setMounted(true), 200);
        return () => clearTimeout(timer);
    }, []);

    const isDark = !mounted || resolvedTheme === "dark";
    const gridStroke = isDark ? "#ffffff10" : "#00000010";
    const axisStroke = isDark ? "#ffffff50" : "#00000050";
    const cursorFill = isDark ? "#ffffff10" : "#00000005";

    return { mounted, isDark, gridStroke, axisStroke, cursorFill };
}
