"use client";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { COLORS, CustomTooltip, useChartTheme } from "./shared";

const bmiData = [
    { name: "< 18.5", count: 12 },
    { name: "18.5-24.9", count: 55 },
    { name: "25-29.9", count: 10 },
    { name: "30+", count: 3 },
];

export function BMIDistributionChart() {
    const { mounted, gridStroke, axisStroke, cursorFill } = useChartTheme();
    if (!mounted) return <div className="w-full h-[250px]" />;

    return (
        <ResponsiveContainer width="100%" height={250}>
            <BarChart data={bmiData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} vertical={false} />
                <XAxis dataKey="name" stroke={axisStroke} fontSize={11} tickLine={false} axisLine={false} dy={10} />
                <YAxis stroke={axisStroke} fontSize={12} tickLine={false} axisLine={false} dx={-10} />
                <Tooltip content={(props) => <CustomTooltip {...props} />} cursor={{ fill: cursorFill }} />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                    {bmiData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Bar>
            </BarChart>
        </ResponsiveContainer>
    );
}
