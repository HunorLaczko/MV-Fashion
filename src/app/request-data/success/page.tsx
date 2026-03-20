"use client";

import { motion } from "framer-motion";
import { CheckCircle, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { withBasePath } from "@/lib/basePath";

export default function SuccessPage() {
    return (
        <div className="min-h-screen py-24 px-4 sm:px-6 lg:px-8 relative flex items-center justify-center">
            {/* Background elements */}
            <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-white to-indigo-50 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20 -z-10" />
            <div
                className="absolute inset-0 bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))] mix-blend-overlay dark:mix-blend-overlay opacity-10 dark:opacity-20 -z-10"
                style={{ backgroundImage: `url(${withBasePath('/grid.svg')})` }}
            />

            <div className="max-w-md w-full mx-auto text-center">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="bg-white dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 p-8 md:p-12 relative overflow-hidden"
                >
                    <div className="absolute top-0 left-0 w-full h-2 bg-indigo-500" />

                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                        className="mx-auto w-24 h-24 bg-indigo-100 dark:bg-indigo-900/30 rounded-full flex items-center justify-center mb-8"
                    >
                        <CheckCircle className="w-12 h-12 text-indigo-600 dark:text-indigo-400" />
                    </motion.div>

                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-4">
                        Request Submitted
                    </h1>

                    <p className="text-slate-600 dark:text-slate-300 text-lg mb-8 text-balance">
                        Thank you for your interest! We&apos;ve received your data request. Since the dataset release is pending, we will notify you at your provided email address as soon as it becomes available.
                    </p>

                    <Link
                        href="/"
                        className="inline-flex items-center justify-center px-6 py-3 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-medium hover:bg-slate-800 dark:hover:bg-slate-100 transition-colors w-full sm:w-auto shadow-md"
                    >
                        <ArrowLeft className="w-5 h-5 mr-2" />
                        Return to Homepage
                    </Link>
                </motion.div>
            </div>
        </div>
    );
}
