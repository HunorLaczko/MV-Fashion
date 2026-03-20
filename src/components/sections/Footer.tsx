export function Footer() {
    return (
        <footer className="py-8 md:py-12 bg-white dark:bg-slate-950 border-t border-slate-200 dark:border-white/10">
            <div className="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4 md:gap-6">

                <div className="text-slate-600 dark:text-slate-400 text-sm">
                    &copy; {new Date().getFullYear()} MV-Fashion Project. All rights reserved.
                </div>

                <div className="flex gap-6 text-sm font-medium text-slate-600 dark:text-slate-400">
                    <a href="https://github.com/HunorLaczko/MV-Fashion" target="_blank" rel="noopener noreferrer" className="hover:text-slate-900 dark:hover:text-white transition-colors">GitHub</a>
                    <a href="https://arxiv.org/abs/2603.08147" target="_blank" rel="noopener noreferrer" className="hover:text-slate-900 dark:hover:text-white transition-colors">ArXiv</a>
                    <a href="https://github.com/HunorLaczko/MV-Fashion/issues" target="_blank" rel="noopener noreferrer" className="hover:text-slate-900 dark:hover:text-white transition-colors">Contact</a>
                </div>

            </div>
        </footer>
    );
}
