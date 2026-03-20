"use client";

import { motion } from "framer-motion";
import { Terminal } from "lucide-react";

export function GetStarted() {
    return (
        <section id="code" className="py-12 md:py-24">
            <div className="container mx-auto px-4 max-w-4xl">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={{ duration: 0.6 }}
                >
                    <div className="text-center mb-8 md:mb-12">
                        <h2 className="text-3xl md:text-5xl font-bold font-[family-name:var(--font-outfit)] mb-4 md:mb-6">
                            Get Started
                        </h2>
                        <p className="text-slate-400 text-lg">
                            Download the dataset and run the initial evaluation scripts with just a few commands.
                        </p>
                    </div>

                    <div className="glass rounded-2xl overflow-hidden shadow-2xl">
                        <div className="flex items-center gap-2 px-4 py-3 bg-slate-200 dark:bg-slate-900 border-b border-slate-300 dark:border-white/10">
                            <div className="flex gap-1.5">
                                <div className="w-3 h-3 rounded-full bg-rose-500/80" />
                                <div className="w-3 h-3 rounded-full bg-amber-500/80" />
                                <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
                            </div>
                            <div className="ml-4 flex items-center gap-2 text-xs font-mono text-slate-500">
                                <Terminal className="w-3 h-3" />
                                bash
                            </div>
                        </div>

                        <div className="p-6 bg-slate-50 dark:bg-[#0d1117] overflow-x-auto text-sm font-mono leading-relaxed">
                            <pre>
                                <code className="text-slate-800 dark:text-slate-300">
                                    <span className="text-emerald-600 dark:text-emerald-400"># Clone the repository</span>{"\n"}
                                    git clone https://github.com/HunorLaczko/MV-Fashion.git{"\n"}
                                    cd MV-Fashion{"\n\n"}

                                    <span className="text-emerald-600 dark:text-emerald-400"># Install dependencies</span>{"\n"}
                                    pip install -r requirements.txt{"\n\n"}

                                    <span className="text-emerald-600 dark:text-emerald-400"># Download the sample dataset</span>{"\n"}
                                    bash scripts/download_sample.sh{"\n"}
                                </code>
                            </pre>
                        </div>
                    </div>
                </motion.div>
            </div>
        </section>
    );
}
