"use client";

import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { Download, AlertCircle, ChevronDown, ChevronUp, ArrowLeft, ExternalLink } from "lucide-react";
import { useTheme } from "next-themes";
import Link from "next/link";
import { withBasePath } from "@/lib/basePath";

export default function RequestDataPage() {
    const { resolvedTheme } = useTheme();
    const embedTimeoutRef = useRef<number | null>(null);
    const [embedError, setEmbedError] = useState(false);
    const [embedLoaded, setEmbedLoaded] = useState(false);

    const formId = resolvedTheme === "dark" ? "EkPkM2" : "KY05eg";
    const tallyEmbedUrl = `https://tally.so/embed/${formId}?alignLeft=1&hideTitle=1&transparentBackground=0`;
    const tallyDirectUrl = `https://tally.so/r/${formId}`;

    useEffect(() => {
        embedTimeoutRef.current = window.setTimeout(() => {
            setEmbedError(true);
        }, 12000);

        return () => {
            if (embedTimeoutRef.current) {
                window.clearTimeout(embedTimeoutRef.current);
                embedTimeoutRef.current = null;
            }
        };
    }, [resolvedTheme]);

    return (
        <main id="main-content" className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 relative">
            {/* Background elements */}
            <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-white to-indigo-50 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20 -z-10" />
            <div
                className="absolute inset-0 bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))] mix-blend-overlay dark:mix-blend-overlay opacity-10 dark:opacity-20 -z-10"
                style={{ backgroundImage: `url(${withBasePath('/grid.svg')})` }}
            />

            <div className="max-w-3xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5 }}
                    className="mb-8"
                >
                    <Link
                        href="/"
                        className="inline-flex items-center text-slate-600 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors font-medium group"
                    >
                        <ArrowLeft className="w-4 h-4 mr-2 transition-transform group-hover:-translate-x-1" />
                        Back to Home
                    </Link>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white dark:bg-slate-900/80 backdrop-blur-sm rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800 p-6 md:p-10"
                >
                    <div className="mb-10">
                        <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-4">Request MV-Fashion Dataset</h1>
                        <p className="text-slate-600 dark:text-slate-300 text-lg">
                            Please follow the instructions below to request access to the dataset. The dataset is available for non-commercial research purposes only.
                        </p>
                    </div>

                    <div className="bg-amber-50 dark:bg-amber-900/20 rounded-xl p-6 mb-8 border border-amber-100 dark:border-amber-800">
                        <h2 className="text-xl font-semibold text-amber-900 dark:text-amber-100 mb-3 flex items-center">
                            <AlertCircle className="w-5 h-5 mr-2" />
                            Note: Dataset Release Pending
                        </h2>
                        <p className="text-slate-700 dark:text-slate-300">
                            The dataset is not available yet, but if you would like us to send you an email when it becomes available, you can submit your details now (with a dummy PDF) and we will reach out to you once we release it.
                        </p>
                    </div>

                    <div className="bg-indigo-50 dark:bg-indigo-900/20 rounded-xl p-6 mb-10 border border-indigo-100 dark:border-indigo-800">
                        <h2 className="text-xl font-semibold text-indigo-900 dark:text-indigo-100 mb-4 flex items-center">
                            <AlertCircle className="w-5 h-5 mr-2" />
                            Instructions
                        </h2>
                        <ol className="list-decimal list-inside space-y-4 text-slate-700 dark:text-slate-300">
                            <li>
                                <a
                                    href={withBasePath('/dataset_agreement.pdf')}
                                    download
                                    className="inline-flex items-center text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 font-medium font-semibold underline-offset-4 hover:underline"
                                >
                                    Download the Dataset Agreement PDF
                                    <Download className="w-4 h-4 ml-1" />
                                </a>
                            </li>
                            <li>Have a <strong>senior member</strong> of your research team (e.g., PI, Professor) sign the agreement.</li>
                            <li>Ensure you use your <strong>institutional email address</strong> in the form.</li>
                            <li>Fill out the form below and upload the signed PDF.</li>
                        </ol>
                    </div>

                    <div className="w-full overflow-visible" key={resolvedTheme ?? "light"}>
                        <iframe
                            src={tallyEmbedUrl}
                            loading="lazy"
                            width="100%"
                            height="1030"
                            style={{ border: 'none', background: 'transparent', display: 'block' }}
                            title="Request MV-Fashion Dataset"
                            onLoad={() => {
                                if (embedTimeoutRef.current) {
                                    window.clearTimeout(embedTimeoutRef.current);
                                    embedTimeoutRef.current = null;
                                }
                                setEmbedLoaded(true);
                                setEmbedError(false);
                            }}
                            onError={() => {
                                if (embedTimeoutRef.current) {
                                    window.clearTimeout(embedTimeoutRef.current);
                                    embedTimeoutRef.current = null;
                                }
                                setEmbedError(true);
                            }}
                        />

                        {embedError && !embedLoaded && (
                            <div className="rounded-xl border border-rose-300 dark:border-rose-800 bg-rose-50 dark:bg-rose-950/30 p-6 space-y-4">
                                <h3 className="text-lg font-semibold text-rose-900 dark:text-rose-200 flex items-center">
                                    <AlertCircle className="w-5 h-5 mr-2" />
                                    We couldn&apos;t load the request form
                                </h3>
                                <p className="text-sm text-slate-700 dark:text-slate-300">
                                    The embedded Tally form failed to load. This can happen due to ad/tracker blockers, strict browser privacy settings, network filtering, or temporary Tally outages.
                                </p>
                                <ul className="list-disc list-inside text-sm text-slate-700 dark:text-slate-300 space-y-1">
                                    <li>Refresh the page and wait a few seconds.</li>
                                    <li>Try opening the form directly in a new tab.</li>
                                    <li>Temporarily disable ad/tracker blocking for this site.</li>
                                    <li>Try a different browser or network.</li>
                                </ul>
                                <div className="flex flex-wrap gap-3">
                                    <a
                                        href={tallyDirectUrl}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="inline-flex items-center px-4 py-2 rounded-full bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-500"
                                    >
                                        Open form directly
                                        <ExternalLink className="w-4 h-4 ml-2" />
                                    </a>
                                    <a
                                        href="https://github.com/HunorLaczko/MV-Fashion/issues"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="inline-flex items-center px-4 py-2 rounded-full border border-slate-300 dark:border-slate-700 text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
                                    >
                                        Report issue on GitHub
                                        <ExternalLink className="w-4 h-4 ml-2" />
                                    </a>
                                </div>
                                <p className="text-xs text-slate-500 dark:text-slate-400">
                                    If none of the steps work, please contact us by opening a GitHub issue.
                                </p>
                            </div>
                        )}
                    </div>

                    <p className="mt-4 text-sm text-slate-600 dark:text-slate-400">
                        After submission, we check your request and contact you at the given email with next steps.
                    </p>

                    <PrivacyNotice />
                </motion.div>
            </div>
        </main>
    );
}

function PrivacyNotice() {
    const [expanded, setExpanded] = useState(false);

    return (
        <div className="mt-8 pt-6 border-t border-slate-200 dark:border-slate-800">
            <button
                type="button"
                className="cursor-pointer group w-full text-left"
                onClick={() => setExpanded(!expanded)}
                aria-expanded={expanded}
                aria-controls="privacy-notice-content"
            >
                <div className="flex items-start justify-between">
                    <div>
                        <h3 className="text-base font-semibold text-slate-900 dark:text-white mb-2">
                            Privacy Notice & Data Handling
                        </h3>
                        <p className="text-sm text-slate-600 dark:text-slate-400 transition-colors group-hover:text-slate-900 dark:group-hover:text-slate-300">
                            By requesting access to the MV-Fashion Dataset, you agree to the collection and processing of your personal data in accordance with the General Data Protection Regulation (GDPR).
                        </p>
                    </div>
                    <div className="ml-4 mt-1 bg-slate-100 dark:bg-slate-800 p-1.5 rounded-full text-slate-500 group-hover:text-slate-900 dark:group-hover:text-slate-300 transition-colors">
                        {expanded ? (
                            <ChevronUp className="w-4 h-4" />
                        ) : (
                            <ChevronDown className="w-4 h-4" />
                        )}
                    </div>
                </div>
            </button>

            {expanded && (
                <motion.div
                    id="privacy-notice-content"
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    className="mt-4 text-sm text-slate-600 dark:text-slate-400 space-y-3"
                >
                    <p><strong>What we collect:</strong> We collect your name, email address, institution/company, intended use case, and implicitly, your IP address (which is anonymised/truncated by default in our logs).</p>
                    <p><strong>Why we collect it:</strong> This data is processed under the lawful bases of legitimate interests (to protect the integrity of the dataset) and contractual necessity (to grant you access under the dataset&apos;s Terms of Use).</p>
                    <p><strong>How long we keep it:</strong> Your download activity logs are strictly retained for a maximum of 2 years, after which they are automatically permanently deleted. Your profile information is kept to maintain your ongoing access.</p>
                    <p><strong>Your rights:</strong> You have the right to request the anonymisation or deletion of your personal data at any time. To submit a data-subject request or ask questions about our privacy practices, please <a href="https://docs.google.com/forms/d/e/1FAIpQLSe61xL5rpH5dzGWeUE36acWp1nCrQSFHU4QOdNYQK7Ls8gzhw/viewform?usp=publish-editor" target="_blank" rel="noopener noreferrer" className="text-indigo-600 dark:text-indigo-400 hover:underline font-medium">fill out our Privacy Contact Form</a>.</p>
                </motion.div>
            )}
        </div>
    );
}
