import type { Metadata, Viewport } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";
import { GoatCounterTracker } from "@/components/ui/GoatCounterTracker";
import Script from "next/script";
import { ThemeProvider } from "@/components/ui/ThemeProvider";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { Banner } from "@/components/ui/Banner";
import { getSiteUrl, withBasePath } from "@/lib/basePath";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL(getSiteUrl()),
  title: "MV-Fashion: Towards Enabling Virtual Try-On and Size Estimation with Multi-View Paired Data",
  description: "A large-scale, multi-view video dataset engineered for domain-specific fashion analysis featuring synchronized captures of worn garments alongside corresponding flat catalogue images.",
  manifest: withBasePath("/manifest.json"),
  openGraph: {
    title: "MV-Fashion Dataset",
    description: "A large-scale, multi-view video dataset engineered for domain-specific fashion analysis featuring synchronized captures of worn garments alongside corresponding flat catalogue images.",
    images: [withBasePath('/images/og-teaser.webp')],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "MV-Fashion Dataset",
    description: "A large-scale, multi-view video dataset engineered for domain-specific fashion analysis.",
    images: [withBasePath('/images/og-teaser.webp')],
  },
}

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f8fafc" },
    { media: "(prefers-color-scheme: dark)", color: "#020617" },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.variable} ${outfit.variable} antialiased bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-50 min-h-screen selection:bg-indigo-500/30 selection:text-indigo-200 transition-colors`}
      >
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 z-[100] bg-indigo-600 text-white px-4 py-2 rounded-md font-medium">
            Skip to main content
          </a>
          <Banner />
          <ThemeToggle />
          <GoatCounterTracker />
          {children}
        </ThemeProvider>

        <Script id="json-ld" type="application/ld+json" dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org/",
            "@type": "Dataset",
            "name": "MV-Fashion Dataset",
            "description": "A large-scale, multi-view video dataset engineered for domain-specific fashion analysis featuring synchronized captures of worn garments alongside corresponding flat catalogue images.",
            "url": getSiteUrl(),
            "license": "https://arxiv.org/abs/2603.08147",
            "keywords": ["virtual try-on", "multi-view", "fashion dataset", "size estimation", "computer vision"],
            "citation": "https://arxiv.org/abs/2603.08147",
            "distribution": {
              "@type": "DataDownload",
              "contentUrl": `${getSiteUrl()}${withBasePath('/request-data/')}`,
              "encodingFormat": "text/html"
            },
            "creator": [
              {
                "@type": "Person",
                "name": "Hunor Laczkó",
                "affiliation": "Computer Vision Center"
              },
              {
                "@type": "Person",
                "name": "Libang Jia",
                "affiliation": "Computer Vision Center"
              },
              {
                "@type": "Person",
                "name": "Loc-Phat Truong",
                "affiliation": "Computer Vision Center"
              },
              {
                "@type": "Person",
                "name": "Diego Hernández",
                "affiliation": "Computer Vision Center"
              },
              {
                "@type": "Person",
                "name": "Sergio Escalera",
                "affiliation": "Computer Vision Center"
              },
              {
                "@type": "Person",
                "name": "Jordi Gonzàlez",
                "affiliation": "Computer Vision Center"
              },
              {
                "@type": "Person",
                "name": "Meysam Madadi",
                "affiliation": "Computer Vision Center"
              }
            ]
          })
        }} />
      </body>
    </html>
  );
}
