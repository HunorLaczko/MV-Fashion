import dynamic from 'next/dynamic';
import { Hero } from "@/components/sections/Hero";
import { Abstract } from "@/components/sections/Abstract";
import { Highlights } from "@/components/sections/Highlights";
import { Features } from "@/components/sections/Features";
import { GetStarted } from "@/components/sections/GetStarted";
import { Citation } from "@/components/sections/Citation";
import { Team } from "@/components/sections/Team";
import { Footer } from "@/components/sections/Footer";

const InteractiveCarousel = dynamic(() => import('@/components/sections/InteractiveCarousel').then(MOD => MOD.InteractiveCarousel), {
  loading: () => <div className="h-[300px] sm:h-[400px] md:h-[500px] lg:h-[600px] flex items-center justify-center">Loading carousel...</div>,
});

const VideoCarousel = dynamic(() => import('@/components/sections/VideoCarousel').then(MOD => MOD.VideoCarousel), {
  loading: () => <div className="h-[300px] sm:h-[400px] md:h-[500px] flex items-center justify-center">Loading videos...</div>,
});

const Statistics = dynamic(() => import('@/components/sections/Statistics').then(MOD => MOD.Statistics), {
  loading: () => <div className="h-[320px] md:h-[420px] flex items-center justify-center">Loading statistics...</div>,
});

export default function Home() {
  return (
    <main id="main-content" className="flex min-h-screen flex-col w-full overflow-x-hidden relative">
      <Hero />
      <Abstract />
      <Highlights />
      <InteractiveCarousel />
      <VideoCarousel />
      <Features />
      <Statistics />
      <GetStarted />
      <Team />
      <Citation />
      <Footer />
    </main>
  );
}
