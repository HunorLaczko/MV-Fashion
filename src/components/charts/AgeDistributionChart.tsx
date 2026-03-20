"use client";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { COLORS, CustomTooltip, useChartTheme } from "./shared";

const ageData = [
    { name: "18-24", count: 42 },
    { name: "25-34", count: 28 },
    { name: "35-44", count: 8 },
    { name: "45-54", count: 2 },
];

export function AgeDistributionChart() {
    const { mounted, gridStroke, axisStroke, cursorFill } = useChartTheme();
    if (!mounted) return <div className="w-full h-[250px]" />;

    return (
        <ResponsiveContainer width="100%" height={250}>
            <BarChart data={ageData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} vertical={false} />
                <XAxis dataKey="name" stroke={axisStroke} fontSize={12} tickLine={false} axisLine={false} dy={10} />
                <YAxis stroke={axisStroke} fontSize={12} tickLine={false} axisLine={false} dx={-10} />
                <Tooltip content={(props) => <CustomTooltip {...props} />} cursor={{ fill: cursorFill }} />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                    {ageData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Bar>
            </BarChart>
        </ResponsiveContainer>
    );
}
