"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function Citation() {
    const [copied, setCopied] = useState(false);

    const bibtex = `@InProceedings{Laczko_2026_CVPR,
    author    = {Laczk\'o, Hunor and Jia, Libang and Truong, Loc-Phat and Hern\'andez, Diego and Escalera, Sergio and Gonzalez, Jordi and Madadi, Meysam},
    title     = {MV-Fashion: Towards Enabling Virtual Try-On and Size Estimation with Multi-View Paired Data},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    month     = {June},
    year      = {2026},
    pages     = {42810-42823}
}`;

    const copyToClipboard = () => {
        navigator.clipboard.writeText(bibtex);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <section id="paper" className="py-12 md:py-24 bg-slate-50 dark:bg-[#050B14] border-y border-slate-200 dark:border-white/5">
            <div className="container mx-auto px-4 max-w-4xl">
                <div className="text-center mb-8 md:mb-12">
                    <h2 className="text-3xl md:text-5xl font-bold font-[family-name:var(--font-outfit)] text-slate-900 dark:text-white mb-4 md:mb-6">
                        Citation
                    </h2>
                    <p className="text-slate-600 dark:text-slate-400 text-lg">
                        If you find our work useful in your research, please consider citing:
                    </p>
                </div>

                <div className="relative group">
                    <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/5 to-purple-500/5 dark:from-indigo-500/10 dark:to-purple-500/10 rounded-2xl blur-xl transition-all duration-500 group-hover:scale-105 opacity-50" />
                    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-2xl relative">
                        <button
                            onClick={copyToClipboard}
                            className="absolute top-4 right-4 text-slate-500 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 dark:text-slate-400 dark:hover:text-white transition-colors dark:bg-slate-800/50 dark:hover:bg-slate-800 p-2 rounded-lg flex items-center justify-center text-sm min-w-[80px] h-[36px]"
                            title="Copy to clipboard"
                        >
                            <AnimatePresence mode="wait">
                                {copied ? (
                                    <motion.div
                                        key="check"
                                        initial={{ opacity: 0, scale: 0.8 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        exit={{ opacity: 0, scale: 0.8 }}
                                        transition={{ duration: 0.15 }}
                                        className="flex items-center gap-2"
                                    >
                                        <Check className="w-4 h-4 text-emerald-500 dark:text-emerald-400" />
                                        <span className="text-emerald-500 dark:text-emerald-400 font-medium">Copied!</span>
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        key="copy"
                                        initial={{ opacity: 0, scale: 0.8 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        exit={{ opacity: 0, scale: 0.8 }}
                                        transition={{ duration: 0.15 }}
                                        className="flex items-center gap-2"
                                    >
                                        <Copy className="w-4 h-4" />
                                        <span>Copy</span>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </button>
                        <pre className="p-6 md:p-8 text-slate-800 dark:text-slate-300 text-sm overflow-x-auto">
                            <code>{bibtex}</code>
                        </pre>
                    </div>
                </div>
            </div>
        </section>
    );
}
