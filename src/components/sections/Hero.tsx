"use client";

import { motion } from "framer-motion";
import { Database, ArrowRight } from "lucide-react";
import Link from "next/link";
import Image from "next/image";
import { withBasePath } from "@/lib/basePath";

export function Hero() {
    return (
        <section className="relative min-h-[65vh] flex flex-col items-center justify-center overflow-hidden pt-10 md:pt-20 pb-2 md:pb-10">
            {/* Animated Background Gradient */}
            <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-white to-indigo-50 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20 z-0" />

            {/* Grid Pattern Overlay */}
            <div
                className="absolute inset-0 bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))] mix-blend-overlay dark:mix-blend-overlay opacity-10 dark:opacity-20 z-0"
                style={{ backgroundImage: `url(${withBasePath('/grid.svg')})` }}
            />

            <div className="container px-4 md:px-6 relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    className="flex flex-col items-center text-center space-y-8 max-w-5xl mx-auto"
                >
                    {/* Main Title */}
                    <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold tracking-tighter sm:text-4xl text-transparent bg-clip-text bg-gradient-to-r from-slate-900 via-slate-700 to-indigo-600 dark:from-white dark:via-slate-200 dark:to-indigo-300 drop-shadow-sm pb-2 font-display leading-tight">
                        MV-Fashion: Towards Enabling Virtual Try-On and Size Estimation with Multi-View Paired Data
                    </h1>

                    <div className="flex flex-wrap justify-center gap-x-4 gap-y-2 text-slate-700 dark:text-slate-300 mb-8 md:mb-12 text-sm sm:text-base md:text-lg">
                        <a href="https://scholar.google.com/citations?user=RfLjJigAAAAJ" target="_blank" rel="noopener noreferrer" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors cursor-pointer">Hunor Laczkó</a>
                        <span className="text-slate-400 dark:text-slate-600">•</span>
                        <a href="https://scholar.google.com/scholar?q=Libang+Jia" target="_blank" rel="noopener noreferrer" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors cursor-pointer">Libang Jia</a>
                        <span className="text-slate-400 dark:text-slate-600">•</span>
                        <a href="https://scholar.google.com/citations?user=N3fuK8UAAAAJ" target="_blank" rel="noopener noreferrer" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors cursor-pointer">Loc-Phat Truong</a>
                        <span className="text-slate-400 dark:text-slate-600">•</span>
                        <a href="https://scholar.google.com/scholar?q=Diego+Hernández" target="_blank" rel="noopener noreferrer" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors cursor-pointer">Diego Hernández</a>
                        <span className="text-slate-400 dark:text-slate-600">•</span>
                        <a href="https://scholar.google.com/citations?user=oI6AIkMAAAAJ" target="_blank" rel="noopener noreferrer" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors cursor-pointer">Sergio Escalera</a>
                        <span className="text-slate-400 dark:text-slate-600">•</span>
                        <a href="https://scholar.google.com/citations?user=Lphp7WUAAAAJ" target="_blank" rel="noopener noreferrer" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors cursor-pointer">Jordi Gonzàlez</a>
                        <span className="text-slate-400 dark:text-slate-600">•</span>
                        <a href="https://scholar.google.com/citations?user=hWMXdg4AAAAJ" target="_blank" rel="noopener noreferrer" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors cursor-pointer">Meysam Madadi</a>
                    </div>

                    <div className="flex flex-wrap justify-center gap-4">
                        {/* Primary CTA */}
                        <a
                            href="https://arxiv.org/abs/2603.08147"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="group relative inline-flex items-center justify-center px-8 py-3.5 text-base font-semibold text-white transition-all duration-200 bg-indigo-600 border border-transparent rounded-full hover:bg-indigo-500 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600"
                        >
                            Read Paper
                            <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                        </a>

                        {/* Secondary CTAs */}
                        <Link
                            href="/request-data"
                            className="inline-flex items-center justify-center px-8 py-3.5 text-base font-semibold text-slate-700 bg-white border border-slate-200 rounded-full hover:bg-slate-50 hover:border-indigo-300 dark:text-indigo-100 transition-all duration-200 dark:bg-white/5 dark:border-white/10 dark:hover:bg-white/10 dark:hover:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-200 dark:focus:ring-slate-800 shadow-sm dark:shadow-none hover:scale-105"
                        >
                            <Database className="mr-2 w-5 h-5" />
                            Get Dataset
                        </Link>

                        <a
                            href="https://github.com/HunorLaczko/MV-Fashion"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center justify-center px-8 py-3.5 text-base font-semibold text-slate-700 bg-white border border-slate-200 rounded-full hover:bg-slate-50 hover:border-indigo-300 dark:text-indigo-100 transition-all duration-200 dark:bg-white/5 dark:border-white/10 dark:hover:bg-white/10 dark:hover:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-200 dark:focus:ring-slate-800 shadow-sm dark:shadow-none hover:scale-105"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="20"
                                height="20"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                className="mr-2 w-5 h-5"
                            >
                                <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
                                <path d="M9 18c-4.51 2-5-2-7-2" />
                            </svg>
                            GitHub
                        </a>
                    </div>
                </motion.div>

                {/* Teaser Media */}
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
                    className="mt-10 sm:mt-16 md:mt-24 max-w-7xl mx-auto rounded-xl border border-slate-200 dark:border-white/10 bg-white/50 dark:bg-white/5 p-2 shadow-2xl relative overflow-hidden"
                >
                    <div className="absolute inset-x-0 bottom-0 h-[15%] bg-gradient-to-t from-slate-50/40 dark:from-slate-950/40 to-transparent z-10 pointer-events-none" />
                    <div className="flex flex-row items-center justify-between w-full rounded-lg bg-white dark:bg-black/40 overflow-hidden xl:max-h-[600px]">
                        <Image
                            src={withBasePath('/images/hero/hero_left.webp')}
                            alt="MV-Fashion Left Part"
                            width={667}
                            height={1000}
                            priority
                            className="w-1/3 h-auto object-contain"
                        />
                        <video
                            src={withBasePath('/images/hero/hero_middle.webm')}
                            autoPlay
                            loop
                            muted
                            playsInline
                            preload="metadata"
                            poster={withBasePath('/images/hero/hero_poster.webp')}
                            className="w-1/3 h-auto object-contain"
                        />
                        <Image
                            src={withBasePath('/images/hero/hero_right.webp')}
                            alt="MV-Fashion Right Part"
                            width={667}
                            height={1000}
                            priority
                            className="w-1/3 h-auto object-contain"
                        />
                    </div>
                </motion.div>
            </div>
        </section>
    );
}
