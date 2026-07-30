"use client";

import { useState } from "react";
import { X, Download, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function Banner() {
    const [isVisible, setIsVisible] = useState(true);

    if (!isVisible) return null;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="relative bg-indigo-600 text-white overflow-hidden"
            >
                <div className="container mx-auto px-4 py-3 sm:px-6 lg:px-8">
                    <div className="flex flex-wrap items-center justify-between gap-x-6 gap-y-2">
                        <div className="flex items-center gap-x-3 text-sm font-medium leading-6">
                            <Sparkles className="h-5 w-5 flex-none" aria-hidden="true" />
                            <p>
                                The dataset is available on Hugging Face!
                            </p>
                        </div>
                        <div className="flex flex-1 items-center justify-end gap-x-4">
                            <a
                                href="https://huggingface.co/datasets/MV-Fashion/MV-Fashion"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center justify-center rounded-full bg-white/20 px-3 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-white/30 transition-colors"
                            >
                                <Download className="h-4 w-4 mr-1.5" />
                                Get Dataset
                            </a>
                            <button
                                type="button"
                                className="-m-3 p-3 focus-visible:outline-offset-[-4px] hover:text-indigo-200 transition-colors"
                                onClick={() => setIsVisible(false)}
                            >
                                <span className="sr-only">Dismiss</span>
                                <X className="h-5 w-5" aria-hidden="true" />
                            </button>
                        </div>
                    </div>
                </div>
            </motion.div>
        </AnimatePresence>
    );
}
