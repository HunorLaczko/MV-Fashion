"use client";

import { withBasePath } from "@/lib/basePath";
import { motion } from "framer-motion";
import Image from "next/image";

export function Abstract() {
    return (
        <section id="about" className="pt-8 md:pt-16 pb-12 md:pb-24 relative">
            <div className="container mx-auto px-4">
                <div className="grid lg:grid-cols-2 gap-8 md:gap-16 items-center">

                    <motion.div
                        initial={{ opacity: 0, x: -30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true, margin: "-100px" }}
                        transition={{ duration: 0.7 }}
                        className="space-y-6"
                    >
                        <h2 className="text-3xl md:text-5xl font-bold font-display tracking-tight text-slate-900 dark:text-white mb-6">
                            Abstract
                        </h2>
                        <p className="text-lg text-slate-700 dark:text-slate-300 leading-relaxed text-balance">
                            Existing 4D human datasets often fall short for fashion-specific research, lacking either realistic garment dynamics or task-specific annotations. To bridge this gap, we introduce <span className="text-indigo-600 dark:text-indigo-300 font-semibold">MV-Fashion</span>, a massive multi-view video dataset engineered for domain-specific fashion analysis.
                        </p>
                        <p className="text-lg text-slate-700 dark:text-slate-300 leading-relaxed text-balance">
                            MV-Fashion captures complex, real-world garment dynamics across 80 diverse subjects wearing multiple layered outfits. Crucially for Virtual Try-On (VTON) applications, it provides <span className="text-indigo-600 dark:text-indigo-300 font-semibold underline decoration-indigo-500/30 underline-offset-4">paired data</span>: synchronized multi-view captures of worn garments alongside their corresponding flat, catalogue images.
                        </p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true, margin: "-100px" }}
                        transition={{ duration: 0.7, delay: 0.2 }}
                        className="relative rounded-2xl overflow-hidden glass flex items-center justify-center bg-white dark:bg-slate-900/50 p-2 border border-slate-200 dark:border-white/10"
                    >
                        <Image
                            src={withBasePath('/images/annotations.webp')}
                            alt="MV-Fashion Annotations Overview"
                            width={1000}
                            height={500}
                            className="w-full h-auto rounded-lg object-contain bg-slate-100 dark:bg-black/40 xl:max-h-[500px]"
                        />
                    </motion.div>

                </div>
            </div>
        </section>
    );
}
