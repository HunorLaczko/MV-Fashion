"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence, useInView } from "framer-motion";
import { ChevronLeft, ChevronRight, AlertCircle } from "lucide-react";
import { withBasePath } from "@/lib/basePath";

const VIDEOS = [
    { src: withBasePath('/images/carousel/videos/videos_1.webm'), poster: withBasePath('/images/carousel/videos/poster_1.webp') },
    { src: withBasePath('/images/carousel/videos/videos_2.webm'), poster: withBasePath('/images/carousel/videos/poster_2.webp') },
    { src: withBasePath('/images/carousel/videos/videos_3.webm'), poster: withBasePath('/images/carousel/videos/poster_3.webp') },
];

function VideoPlayer({ src, poster, onError }: { src: string, poster: string, onError: () => void }) {
    const videoRef = useRef<HTMLVideoElement>(null);
    const inView = useInView(videoRef, { margin: "100px" });
    const [hasLoaded, setHasLoaded] = useState(false);

    useEffect(() => {
        if (!videoRef.current) return;
        if (inView) {
            // Attempt to play if in view
            videoRef.current.play().catch(() => { });
        } else {
            videoRef.current.pause();
        }
    }, [inView]);

    return (
        <video
            ref={videoRef}
            src={inView ? src : undefined}
            className="w-full h-full object-contain rounded-xl pointer-events-none"
            style={{ transform: "translateZ(0)", backfaceVisibility: "hidden" }}
            muted
            loop
            playsInline
            disablePictureInPicture
            disableRemotePlayback
            poster={hasLoaded ? undefined : poster}
            onLoadedData={() => setHasLoaded(true)}
            onError={onError}
        />
    );
}

export function VideoCarousel() {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [videoErrors, setVideoErrors] = useState<Set<number>>(new Set());

    const handleVideoError = (index: number) => {
        setVideoErrors((prev) => {
            const newSet = new Set(prev);
            newSet.add(index);
            return newSet;
        });
    };

    const handleNext = () => {
        setCurrentIndex((prev) => (prev + 1) % VIDEOS.length);
    };

    const handlePrev = () => {
        setCurrentIndex((prev) => (prev - 1 + VIDEOS.length) % VIDEOS.length);
    };

    const handleDotClick = (index: number) => {
        setCurrentIndex(index);
    };

    const getOffset = (i: number) => {
        const diff = i - currentIndex;
        const len = VIDEOS.length;
        if (diff > Math.floor(len / 2)) return diff - len;
        if (diff < -Math.floor(len / 2)) return diff + len;
        return diff;
    };

    return (
        <section id="video-examples" className="py-12 md:py-24 bg-slate-50 dark:bg-slate-950 border-y border-slate-200 dark:border-white/5 relative overflow-hidden">
            <div className="container mx-auto px-4 max-w-7xl">
                <div className="text-center mb-12">
                    <h2 className="text-3xl md:text-5xl font-bold font-display tracking-tight text-slate-900 dark:text-white mb-6">
                        Multi-View Video Captures
                    </h2>
                    <p className="text-lg text-slate-700 dark:text-slate-300 max-w-2xl mx-auto">
                        Dynamic multi-view video sequences providing temporal consistency and rich spatial information.
                    </p>
                </div>

                <div className="relative mx-auto max-w-4xl h-[300px] sm:h-[400px] md:h-[500px] flex items-center justify-center [perspective:1000px]">
                    <AnimatePresence initial={false}>
                        {VIDEOS.map((video, i) => {
                            const offset = getOffset(i);
                            const absOffset = Math.abs(offset);
                            const isVisible = absOffset <= 1; // Show fewer videos to not overwhelm the browser with videos

                            if (!isVisible) return null;

                            return (
                                <motion.div
                                    key={`${video.src}-${i}`}
                                    className={`absolute w-[80%] md:w-[65%] h-full rounded-2xl overflow-hidden border cursor-pointer ${absOffset === 0
                                        ? "glass bg-white/10 dark:bg-slate-800/80 border-slate-200/50 dark:border-white/10 shadow-2xl"
                                        : "bg-white/20 dark:bg-slate-800 border-slate-200/30 dark:border-white/5 shadow-md dark:shadow-none"
                                        }`}
                                    initial={false}
                                    animate={{
                                        x: `${offset * 85}%`,
                                        scale: 1 - absOffset * 0.15,
                                        zIndex: 10 - absOffset,
                                        rotateY: offset * -10,
                                        opacity: absOffset > 1 ? 0 : 1,
                                    }}
                                    transition={{
                                        type: "spring",
                                        stiffness: 250,
                                        damping: 25,
                                        mass: 1,
                                    }}
                                    style={{
                                        filter: `brightness(${1 - absOffset * 0.5})`,
                                        willChange: "transform, opacity, filter",
                                    }}
                                    onClick={() => handleDotClick(i)}
                                >
                                    <div className="relative w-full h-full flex items-center justify-center">
                                        {videoErrors.has(i) ? (
                                            <div className="flex flex-col items-center justify-center text-slate-500">
                                                <AlertCircle className="w-12 h-12 mb-2 opacity-50" />
                                                <p className="text-sm">Video unavailable</p>
                                            </div>
                                        ) : (
                                            <VideoPlayer src={video.src} poster={video.poster} onError={() => handleVideoError(i)} />
                                        )}
                                    </div>
                                </motion.div>
                            );
                        })}
                    </AnimatePresence>

                    {/* Controls */}
                    <button
                        onClick={handlePrev}
                        className="absolute left-2 md:left-8 top-1/2 -translate-y-1/2 p-3 md:p-4 rounded-full bg-white/80 dark:bg-black/50 text-slate-800 dark:text-white backdrop-blur-md shadow-xl hover:bg-white dark:hover:bg-slate-800 transition-all hover:scale-110 z-20"
                        aria-label="Previous video"
                    >
                        <ChevronLeft className="w-6 h-6 md:w-8 md:h-8" />
                    </button>
                    <button
                        onClick={handleNext}
                        className="absolute right-2 md:right-8 top-1/2 -translate-y-1/2 p-3 md:p-4 rounded-full bg-white/80 dark:bg-black/50 text-slate-800 dark:text-white backdrop-blur-md shadow-xl hover:bg-white dark:hover:bg-slate-800 transition-all hover:scale-110 z-20"
                        aria-label="Next video"
                    >
                        <ChevronRight className="w-6 h-6 md:w-8 md:h-8" />
                    </button>
                </div>

                {/* Indicators */}
                <div className="flex justify-center mt-8 relative z-10 gap-2 px-6 py-3 rounded-full mx-auto w-fit bg-slate-100/50 dark:bg-slate-800/50 backdrop-blur-md border border-slate-200/50 dark:border-white/5">
                    {VIDEOS.map((_, i) => (
                        <button
                            key={i}
                            onClick={() => handleDotClick(i)}
                            className={`w-2.5 h-2.5 rounded-full transition-all ${i === currentIndex ? "bg-indigo-600 dark:bg-indigo-400 scale-125 shadow hover:scale-125" : "bg-slate-400/50 dark:bg-slate-600/50 hover:bg-slate-500/80 dark:hover:bg-slate-400/80"}`}
                            aria-label={`Go to video ${i + 1}`}
                        />
                    ))}
                </div>
            </div>
        </section>
    );
}
