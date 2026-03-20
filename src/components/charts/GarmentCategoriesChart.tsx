"use client";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { COLORS, CustomTooltip, useChartTheme } from "./shared";

const garmentData = [
    { name: "Shirt/Blouse", value: 38.3 },
    { name: "Pants", value: 21.2 },
    { name: "Shorts", value: 11.7 },
    { name: "Dress", value: 5.2 },
    { name: "Jacket", value: 5.1 },
    { name: "Jeans", value: 4.8 },
    { name: "Skirt", value: 4.5 },
    { name: "Sweater", value: 3.2 },
    { name: "Other", value: 6.0 }
];

export function GarmentCategoriesChart() {
    const { mounted, gridStroke, axisStroke, cursorFill } = useChartTheme();
    if (!mounted) return <div className="w-full h-[250px]" />;

    return (
        <ResponsiveContainer width="100%" height={250}>
            <BarChart data={garmentData} layout="vertical" margin={{ top: 0, right: 30, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} horizontal={true} vertical={false} />
                <XAxis type="number" stroke={axisStroke} fontSize={11} tickLine={false} axisLine={false} />
                <YAxis dataKey="name" type="category" stroke={axisStroke} fontSize={11} tickLine={false} axisLine={false} width={80} />
                <Tooltip content={(props) => <CustomTooltip {...props} isPercentage />} cursor={{ fill: cursorFill }} />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                    {garmentData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Bar>
            </BarChart>
        </ResponsiveContainer>
    );
}
