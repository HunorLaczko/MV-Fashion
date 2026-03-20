"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";
import { ChevronLeft, ChevronRight } from "lucide-react";


const CATEGORY_IMAGES: Record<string, string[]> = {
    "Outfits": [
        '/images/carousel/outfits/outfits_1.webp',
        '/images/carousel/outfits/outfits_2.webp',
        '/images/carousel/outfits/outfits_3.webp',
        '/images/carousel/outfits/outfits_4.webp',
        '/images/carousel/outfits/outfits_5.webp',
        '/images/carousel/outfits/outfits_6.webp',
        '/images/carousel/outfits/outfits_7.webp',
        '/images/carousel/outfits/outfits_8.webp',
        '/images/carousel/outfits/outfits_9.webp',
        '/images/carousel/outfits/outfits_10.webp',
    ],
    "Multiview": [
        '/images/carousel/multiview/multiview_1.webp',
        '/images/carousel/multiview/multiview_2.webp',
        '/images/carousel/multiview/multiview_3.webp',
        '/images/carousel/multiview/multiview_4.webp',
        '/images/carousel/multiview/multiview_5.webp',
        '/images/carousel/multiview/multiview_6.webp',
        '/images/carousel/multiview/multiview_7.webp',
        '/images/carousel/multiview/multiview_8.webp',
        '/images/carousel/multiview/multiview_9.webp',
        '/images/carousel/multiview/multiview_10.webp',
        '/images/carousel/multiview/multiview_11.webp',
        '/images/carousel/multiview/multiview_12.webp',
    ],
    "Poses": [
        '/images/carousel/poses/poses_1.webp',
        '/images/carousel/poses/poses_2.webp',
        '/images/carousel/poses/poses_3.webp',
        '/images/carousel/poses/poses_4.webp',
        '/images/carousel/poses/poses_5.webp',
        '/images/carousel/poses/poses_6.webp',
        '/images/carousel/poses/poses_7.webp',
        '/images/carousel/poses/poses_8.webp',
        '/images/carousel/poses/poses_9.webp',
        '/images/carousel/poses/poses_10.webp',
    ],
};

const CATEGORIES = Object.keys(CATEGORY_IMAGES);

export function InteractiveCarousel() {
    const [activeCategory, setActiveCategory] = useState(CATEGORIES[0]);
    const [currentIndex, setCurrentIndex] = useState(0);

    const images = CATEGORY_IMAGES[activeCategory] || [];

    const handleCategoryChange = (category: string) => {
        setActiveCategory(category);
        setCurrentIndex(0);
    };

    const handleNext = () => {
        setCurrentIndex((prev) => (prev + 1) % images.length);
    };

    const handlePrev = () => {
        setCurrentIndex((prev) => (prev - 1 + images.length) % images.length);
    };

    const handleDotClick = (index: number) => {
        setCurrentIndex(index);
    };

    const getOffset = (i: number) => {
        const diff = i - currentIndex;
        const len = images.length;
        if (diff > Math.floor(len / 2)) return diff - len;
        if (diff < -Math.floor(len / 2)) return diff + len;
        return diff;
    };

    return (
        <section id="interactive-examples" className="py-12 md:py-24 bg-white dark:bg-slate-900 border-y border-slate-200 dark:border-white/5 relative overflow-hidden">
            <div className="container mx-auto px-4 max-w-7xl">
                <div className="text-center mb-10">
                    <h2 className="text-3xl md:text-5xl font-bold font-display tracking-tight text-slate-900 dark:text-white mb-6">
                        Explore the Data
                    </h2>
                    <p className="text-lg text-slate-700 dark:text-slate-300 max-w-2xl mx-auto mb-8">
                        Select a category to view multi-view dynamics, outfits, and pose variations in the MV-Fashion dataset.
                    </p>

                    {/* Category Navigation */}
                    <div className="flex flex-wrap justify-center gap-2 md:gap-4">
                        {CATEGORIES.map((category) => (
                            <button
                                key={category}
                                onClick={() => handleCategoryChange(category)}
                                className={`px-4 py-2 rounded-full text-sm md:text-base font-medium transition-all duration-200 ${activeCategory === category
                                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-500/30"
                                    : "bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700"
                                    }`}
                            >
                                {category}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="relative mx-auto max-w-6xl h-[300px] sm:h-[400px] md:h-[500px] lg:h-[600px] flex items-center justify-center [perspective:1000px] mt-8">
                    <AnimatePresence mode="popLayout" initial={false}>
                        {images.map((src, i) => {
                            const offset = getOffset(i);
                            const absOffset = Math.abs(offset);
                            // Hide elements that are too far away
                            const isVisible = absOffset <= 2;

                            if (!isVisible) return null;

                            return (
                                <motion.div
                                    key={`${activeCategory}-${src}-${i}`}
                                    className={`absolute w-[80%] md:w-[65%] lg:w-[50%] h-full rounded-2xl overflow-hidden border cursor-pointer ${
                                        absOffset === 0
                                            ? "glass bg-white/10 dark:bg-slate-800/80 border-slate-200/50 dark:border-white/10 shadow-2xl"
                                            : "bg-white/20 dark:bg-slate-800 border-slate-200/30 dark:border-white/5 shadow-md dark:shadow-none"
                                    }`}
                                    initial={{ opacity: 0, scale: 0.8 }}
                                    animate={{
                                        x: `${offset * 75}%`,
                                        scale: 1 - absOffset * 0.15,
                                        zIndex: 10 - absOffset,
                                        rotateY: offset * -12,
                                        opacity: absOffset > 1.5 ? 0 : 1,
                                    }}
                                    exit={{ opacity: 0, scale: 0.8 }}
                                    transition={{
                                        type: "spring",
                                        stiffness: 250,
                                        damping: 25,
                                        mass: 1,
                                    }}
                                    style={{
                                        filter: `blur(${absOffset === 0 ? 0 : absOffset * 4}px) brightness(${1 - absOffset * 0.3})`,
                                        willChange: "transform, opacity, filter",
                                    }}
                                    onClick={() => handleDotClick(i)}
                                >
                                    <div className="relative w-full h-full p-2">
                                        <div className="relative w-full h-full rounded-xl overflow-hidden dark:bg-black/40">
                                            <Image
                                                src={src}
                                                alt={`${activeCategory} Example ${i + 1}`}
                                                fill
                                                className="object-contain"
                                                sizes="(max-width: 768px) 80vw, (max-width: 1200px) 65vw, 50vw"
                                            />
                                        </div>
                                    </div>
                                </motion.div>
                            );
                        })}
                    </AnimatePresence>

                    {/* Controls */}
                    {images.length > 1 && (
                        <>
                            <button
                                onClick={handlePrev}
                                className="absolute left-2 md:left-8 top-1/2 -translate-y-1/2 p-3 md:p-4 rounded-full bg-white/80 dark:bg-black/50 text-slate-800 dark:text-white backdrop-blur-md shadow-xl hover:bg-white dark:hover:bg-slate-800 transition-all hover:scale-110 z-20 will-change-transform"
                                aria-label="Previous image"
                            >
                                <ChevronLeft className="w-6 h-6 md:w-8 md:h-8" />
                            </button>
                            <button
                                onClick={handleNext}
                                className="absolute right-2 md:right-8 top-1/2 -translate-y-1/2 p-3 md:p-4 rounded-full bg-white/80 dark:bg-black/50 text-slate-800 dark:text-white backdrop-blur-md shadow-xl hover:bg-white dark:hover:bg-slate-800 transition-all hover:scale-110 z-20 will-change-transform"
                                aria-label="Next image"
                            >
                                <ChevronRight className="w-6 h-6 md:w-8 md:h-8" />
                            </button>
                        </>
                    )}
                </div>

                {/* Indicators */}
                {images.length > 1 && (
                    <div className="flex justify-center mt-8 relative z-10 gap-2 px-6 py-3 rounded-full mx-auto w-fit bg-slate-100/50 dark:bg-slate-800/50 backdrop-blur-md border border-slate-200/50 dark:border-white/5">
                        {images.map((_, i) => (
                            <button
                                key={i}
                                onClick={() => handleDotClick(i)}
                                className={`w-2.5 h-2.5 rounded-full transition-all ${i === currentIndex ? "bg-indigo-600 dark:bg-indigo-400 scale-125 shadow hover:scale-125" : "bg-slate-400/50 dark:bg-slate-600/50 hover:bg-slate-500/80 dark:hover:bg-slate-400/80"}`}
                                aria-label={`Go to image ${i + 1}`}
                            />
                        ))}
                    </div>
                )}
            </div>
        </section>
    );
}
