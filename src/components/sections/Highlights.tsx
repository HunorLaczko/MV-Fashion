"use client";

import { motion } from "framer-motion";
import Image from "next/image";
import { withBasePath } from "@/lib/basePath";

const highlightItems = [
    {
        title: "Diverse Poses",
        description: "Capturing a wide range of natural and complex human motions.",
        color: "from-blue-500/20 to-cyan-500/20",
        image: withBasePath('/images/highlights/multi_poses.webp')
    },
    {
        title: "Layered Outfits",
        description: "Intricate details of multi-layered clothing combinations.",
        color: "from-rose-500/20 to-orange-500/20",
        image: withBasePath('/images/highlights/multi_layers.webp')
    },
    {
        title: "Multi-view Consistency",
        description: "Synchronized capture ensuring perfect alignment across all views.",
        color: "from-emerald-500/20 to-teal-500/20",
        image: withBasePath('/images/highlights/multiview.webp')
    },
    {
        title: "Paired Data",
        description: "Catalogue domain image pairs for the multi-view recordings for VTON.",
        color: "from-purple-500/20 to-pink-500/20",
        image: withBasePath('/images/highlights/paired.webp')
    },
    {
        title: "Challenging Garments",
        description: "Includes difficult items like loose dresses and transparent fabrics.",
        color: "from-amber-500/20 to-yellow-500/20",
        image: withBasePath('/images/highlights/challenging_outfits.webp')
    },
    {
        title: "Robust Tracking",
        description: "Accurate SMPL-X fitting and tracking.",
        color: "from-indigo-500/20 to-violet-500/20",
        image: withBasePath('/images/highlights/smplx.webp')
    },
];

export function Highlights() {
    return (
        <section id="data" className="py-12 md:py-24 relative overflow-hidden">
            <div className="container mx-auto px-4 z-10 relative">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-10 md:mb-16"
                >
                    <h2 className="text-3xl md:text-5xl font-bold font-display tracking-tight text-slate-900 dark:text-white mb-6">
                        Dataset Highlights
                    </h2>
                    <p className="text-slate-600 dark:text-slate-400 text-lg max-w-2xl mx-auto">
                        Explore the diversity and quality of the captured data, designed to push the boundaries of human-centric rendering and virtual try-on.
                    </p>
                </motion.div>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
                    {highlightItems.map((item, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, scale: 0.95 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true, margin: "-100px" }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            whileHover={{ y: -5 }}
                            className="glass rounded-2xl p-6 relative group overflow-hidden border-slate-200 dark:border-white/5"
                        >
                            <div className={`absolute inset-0 bg-gradient-to-br ${item.color} opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />

                            <div className="aspect-square bg-slate-100 dark:bg-slate-900/80 rounded-xl mb-6 relative overflow-hidden flex items-center justify-center border border-slate-200 dark:border-white/10">
                                <Image
                                    src={item.image}
                                    alt={item.title}
                                    fill
                                    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                                    className="object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-300"
                                />
                            </div>

                            <h3 className="text-xl font-bold mb-3 font-display text-slate-800 dark:text-white relative z-10">
                                {item.title}
                            </h3>
                            <p className="text-slate-600 dark:text-slate-400 relative z-10 text-sm">
                                {item.description}
                            </p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
