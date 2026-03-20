"use client";

import { motion } from "framer-motion";
import { Users, Camera, FileJson, Layers, Image as ImageIcon, Scissors } from "lucide-react";

const features = [
    { icon: Users, title: "80 Subjects", desc: "Diverse pool of participants (50.6% male, 45.7% female) across various BMI and age distributions." },
    { icon: Scissors, title: "754 Garments", desc: "Spanning 14 distinct fashion categories, comprising single, double, and triple-layered outfits." },
    { icon: ImageIcon, title: "Paired VTON Data", desc: "Unique paired data featuring synchronized multi-view captures of worn garments with corresponding flat catalogue images." },
    { icon: Camera, title: "68 Synchronized Cameras", desc: "60 RGB global shutter and 8 Depth/4K cameras capturing real-world dynamic deformations." },
    { icon: FileJson, title: "Rich Annotations", desc: "Features precise SMPL-X fits, 3D point clouds, text descriptions, and segmentation masks." },
    { icon: Layers, title: "3,273 Sequences", desc: "Extensive multi-view video database yielding over 72.5 million high-fidelity frames." },
];

export function Features() {
    return (
        <section className="py-12 md:py-24 bg-slate-50 dark:bg-white/5 border-y border-slate-200 dark:border-white/5">
            <div className="container mx-auto px-4">
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
                    {features.map((feature, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true, margin: "-50px" }}
                            transition={{ duration: 0.5, delay: i * 0.1 }}
                            className={`flex gap-4 p-6 rounded-2xl`}
                        >
                            <div className={`flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center border bg-indigo-50 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-200 dark:border-indigo-500/20 shadow-sm dark:shadow-none`}>
                                <feature.icon className="w-6 h-6" />
                            </div>
                            <div>
                                <h3 className={`text-lg font-bold mb-2 font-display text-slate-800 dark:text-slate-200`}>{feature.title}</h3>
                                <p className="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">{feature.desc}</p>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
