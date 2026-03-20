"use client";
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from "recharts";
import { COLORS, CustomTooltip, useChartTheme } from "./shared";

const fitData = [
    { name: "Slim", value: 8.1 },
    { name: "Regular", value: 64.1 },
    { name: "Loose", value: 24.7 },
];

export function FitDistributionChart() {
    const { mounted } = useChartTheme();
    if (!mounted) return <div className="w-full h-[250px]" />;

    return (
        <ResponsiveContainer width="100%" height={250}>
            <PieChart>
                <Tooltip content={(props) => <CustomTooltip {...props} isPercentage />} />
                <Pie data={fitData} cx="50%" cy="45%" innerRadius={50} outerRadius={80} paddingAngle={4} dataKey="value" stroke="none">
                    {fitData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[(index + 3) % COLORS.length]} />
                    ))}
                </Pie>
                <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px' }} formatter={(value) => <span className="text-slate-600 dark:text-slate-300 ml-1">{value}</span>} />
            </PieChart>
        </ResponsiveContainer>
    );
}
