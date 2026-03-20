"use client";
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from "recharts";
import { COLORS, CustomTooltip, useChartTheme } from "./shared";

const elasticityData = [
    { name: "Level 1", value: 37.9 },
    { name: "Level 2", value: 29.2 },
    { name: "Level 3", value: 25.1 },
    { name: "Level 4", value: 6.2 },
    { name: "Level 5", value: 0.5 },
];

export function ElasticityDistributionChart() {
    const { mounted } = useChartTheme();
    if (!mounted) return <div className="w-full h-[250px]" />;

    return (
        <ResponsiveContainer width="100%" height={250}>
            <PieChart>
                <Tooltip content={(props) => <CustomTooltip {...props} isPercentage />} />
                <Pie data={elasticityData} cx="50%" cy="45%" innerRadius={50} outerRadius={80} paddingAngle={4} dataKey="value" stroke="none">
                    {elasticityData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px' }} formatter={(value) => <span className="text-slate-600 dark:text-slate-300 ml-1">{value}</span>} />
            </PieChart>
        </ResponsiveContainer>
    );
}
