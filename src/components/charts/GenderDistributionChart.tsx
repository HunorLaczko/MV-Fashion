"use client";
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from "recharts";
import { COLORS, CustomTooltip, useChartTheme } from "./shared";

const genderData = [
    { name: "Male", value: 50.6 },
    { name: "Female", value: 45.7 },
    { name: "Non-binary", value: 3.7 },
];

export function GenderDistributionChart() {
    const { mounted } = useChartTheme();
    if (!mounted) return <div className="w-full h-[250px]" />;

    return (
        <ResponsiveContainer width="100%" height={250}>
            <PieChart>
                <Tooltip content={(props) => <CustomTooltip {...props} isPercentage />} />
                <Pie data={genderData} cx="50%" cy="45%" innerRadius={50} outerRadius={80} paddingAngle={4} dataKey="value" stroke="none">
                    {genderData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px' }} formatter={(value) => <span className="text-slate-600 dark:text-slate-300 ml-1">{value}</span>} />
            </PieChart>
        </ResponsiveContainer>
    );
}
