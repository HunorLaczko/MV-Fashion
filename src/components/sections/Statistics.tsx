"use client";

import { motion } from "framer-motion";
import dynamic from 'next/dynamic';

const DynamicGarmentCategoriesChart = dynamic(() => import('@/components/charts/GarmentCategoriesChart').then(mod => mod.GarmentCategoriesChart), { ssr: false });
const DynamicAgeDistributionChart = dynamic(() => import('@/components/charts/AgeDistributionChart').then(mod => mod.AgeDistributionChart), { ssr: false });
const DynamicGenderDistributionChart = dynamic(() => import('@/components/charts/GenderDistributionChart').then(mod => mod.GenderDistributionChart), { ssr: false });
const DynamicBMIDistributionChart = dynamic(() => import('@/components/charts/BMIDistributionChart').then(mod => mod.BMIDistributionChart), { ssr: false });
const DynamicFitDistributionChart = dynamic(() => import('@/components/charts/FitDistributionChart').then(mod => mod.FitDistributionChart), { ssr: false });
const DynamicElasticityDistributionChart = dynamic(() => import('@/components/charts/ElasticityDistributionChart').then(mod => mod.ElasticityDistributionChart), { ssr: false });

export function Statistics() {
    return (
        <section id="statistics" className="py-12 md:py-24 relative overflow-hidden bg-slate-50 dark:bg-white/[0.02] border-t border-slate-200 dark:border-white/5">
            <div className="container mx-auto px-4 z-10 relative">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-10 md:mb-16"
                >
                    <h2 className="text-3xl md:text-5xl font-bold font-[family-name:var(--font-outfit)] text-slate-900 dark:text-white mb-6">
                        Dataset Statistics
                    </h2>
                    <p className="text-slate-600 dark:text-slate-400 text-lg max-w-2xl mx-auto text-balance">
                        A comprehensive breakdown of the dataset demographics and captured motion categories.
                    </p>
                </motion.div>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true, margin: "-50px" }}
                        transition={{ duration: 0.5 }}
                        className="glass rounded-3xl p-6 flex flex-col"
                    >
                        <h3 className="text-xl font-bold font-display mb-6 text-slate-800 dark:text-white text-center">
                            Garment Categories (%)
                        </h3>
                        <DynamicGarmentCategoriesChart />
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true, margin: "-50px" }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                        className="glass rounded-3xl p-6 flex flex-col"
                    >
                        <h3 className="text-xl font-bold font-display mb-6 text-slate-800 dark:text-white text-center">
                            Age Distribution
                        </h3>
                        <DynamicAgeDistributionChart />
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true, margin: "-50px" }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="glass rounded-3xl p-6 flex flex-col"
                    >
                        <h3 className="text-xl font-bold font-display mb-2 text-slate-800 dark:text-white text-center">
                            Gender
                        </h3>
                        <DynamicGenderDistributionChart />
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true, margin: "-50px" }}
                        transition={{ duration: 0.5, delay: 0.3 }}
                        className="glass rounded-3xl p-6 flex flex-col"
                    >
                        <h3 className="text-xl font-bold font-display mb-6 text-slate-800 dark:text-white text-center">
                            BMI Distribution
                        </h3>
                        <DynamicBMIDistributionChart />
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true, margin: "-50px" }}
                        transition={{ duration: 0.5, delay: 0.4 }}
                        className="glass rounded-3xl p-6 flex flex-col"
                    >
                        <h3 className="text-xl font-bold font-display mb-2 text-slate-800 dark:text-white text-center">
                            Garment Fit
                        </h3>
                        <DynamicFitDistributionChart />
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true, margin: "-50px" }}
                        transition={{ duration: 0.5, delay: 0.5 }}
                        className="glass rounded-3xl p-6 flex flex-col"
                    >
                        <h3 className="text-xl font-bold font-display mb-2 text-slate-800 dark:text-white text-center">
                            Fabric Elasticity
                        </h3>
                        <DynamicElasticityDistributionChart />
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
