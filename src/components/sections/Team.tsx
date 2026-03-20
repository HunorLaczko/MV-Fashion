"use client";

import { motion } from "framer-motion";
import { User } from "lucide-react";
import Image from "next/image";
import { useState } from "react";
import { withBasePath } from "@/lib/basePath";

interface TeamMember {
    name: string;
    link: string;
    github?: string;
    photo?: string; // local photo path or URL
}

function TeamMemberCard({ member, index }: { member: TeamMember; index: number }) {
    const [imageError, setImageError] = useState(false);

    const getPhotoUrl = (): string | null => {
        if (member.photo) {
            return member.photo;
        }

        if (member.github) {
            return `https://github.com/${member.github}.png`;
        }

        return null;
    };

    const photoUrl = getPhotoUrl();

    return (
        <motion.a
            href={member.link}
            target="_blank"
            rel="noopener noreferrer"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="flex flex-col items-center group cursor-pointer"
        >
            <div className="w-24 h-24 md:w-32 md:h-32 mb-4 rounded-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-center overflow-hidden group-hover:border-indigo-500 dark:group-hover:border-indigo-400 transition-all shadow-sm group-hover:shadow-md relative group-hover:scale-105 duration-300">
                {photoUrl && !imageError ? (
                    <Image
                        src={photoUrl}
                        alt={member.name}
                        width={128}
                        height={128}
                        className="w-full h-full object-cover"
                        onError={() => {
                            setImageError(true);
                        }}
                    />
                ) : (
                    <User className="w-10 h-10 md:w-12 md:h-12 text-slate-400 dark:text-slate-500 group-hover:text-indigo-500 dark:group-hover:text-indigo-400 transition-colors" />
                )}
            </div>
            <h3 className="text-base md:text-lg font-medium text-slate-800 dark:text-slate-200 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors text-center font-[family-name:var(--font-outfit)]">
                {member.name}
            </h3>
        </motion.a>
    );
}

export function Team() {
    const teamMembers: TeamMember[] = [
        {
            name: "Hunor Laczkó",
            link: "https://www.linkedin.com/in/hunor-laczko/",
            github: "HunorLaczko",
            photo: withBasePath('/images/team/hl.webp')
        },
        {
            name: "Libang Jia",
            link: "https://www.linkedin.com/in/libang-jia-13683b360/",
            github: "jialibang",
            photo: withBasePath('/images/team/lj.webp')
        },
        {
            name: "Loc-Phat Truong",
            link: "https://scholar.google.com/citations?user=N3fuK8UAAAAJ",
            github: "locphattruong",
        },
        {
            name: "Diego Hernández",
            link: "https://www.linkedin.com/in/diiego-h/",
            github: "Diiego-H",
        },
        {
            name: "Sergio Escalera",
            link: "https://scholar.google.com/citations?user=oI6AIkMAAAAJ",
            github: "sergio-escalera",
            photo: withBasePath('/images/team/se.webp')
        },
        {
            name: "Jordi Gonzàlez",
            link: "https://scholar.google.com/citations?user=Lphp7WUAAAAJ",
            github: "jordi-gonzalez",
            photo: withBasePath('/images/team/jg.webp')
        },
        {
            name: "Meysam Madadi",
            link: "https://scholar.google.com/citations?user=hWMXdg4AAAAJ",
            github: "meysam-madadi",
            photo: withBasePath('/images/team/mm.webp')
        }
    ];

    return (
        <section id="team" className="py-12 md:py-24 bg-white dark:bg-slate-950">
            <div className="container mx-auto px-4 max-w-6xl">
                <div className="text-center mb-12 md:mb-16 flex flex-col items-center">
                    <h2 className="text-3xl md:text-5xl font-bold font-[family-name:var(--font-outfit)] text-slate-900 dark:text-white mb-6">
                        The Team
                    </h2>
                </div>

                <div className="flex flex-wrap justify-center gap-8 md:gap-12">
                    {teamMembers.map((member, i) => (
                        <TeamMemberCard key={member.name} member={member} index={i} />
                    ))}
                </div>
            </div>
        </section>
    );
}
