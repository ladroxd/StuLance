"use client";

import * as React from "react";
import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

// -------------------------------------------------------------------------
// 1. STYLES
// -------------------------------------------------------------------------
const STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

.cinematic-footer-wrapper {
  font-family: 'Plus Jakarta Sans', sans-serif;
  -webkit-font-smoothing: antialiased;

  --pill-bg-1: rgba(255,255,255,0.04);
  --pill-bg-2: rgba(255,255,255,0.01);
  --pill-shadow: rgba(0,0,0,0.5);
  --pill-highlight: rgba(255,255,255,0.08);
  --pill-inset-shadow: rgba(0,0,0,0.6);
  --pill-border: rgba(255,255,255,0.08);

  --pill-bg-1-hover: rgba(255,255,255,0.09);
  --pill-bg-2-hover: rgba(255,255,255,0.02);
  --pill-border-hover: rgba(255,255,255,0.20);
  --pill-shadow-hover: rgba(0,0,0,0.7);
  --pill-highlight-hover: rgba(255,255,255,0.18);
}

@keyframes footer-breathe {
  0% { transform: translate(-50%, -50%) scale(1); opacity: 0.6; }
  100% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }
}

@keyframes footer-scroll-marquee {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

.animate-footer-breathe {
  animation: footer-breathe 8s ease-in-out infinite alternate;
}

.animate-footer-scroll-marquee {
  animation: footer-scroll-marquee 40s linear infinite;
}

.animate-footer-heartbeat {
  animation: footer-heartbeat 2s cubic-bezier(0.25, 1, 0.5, 1) infinite;
}

.footer-bg-grid {
  background-size: 60px 60px;
  background-image:
    linear-gradient(to right, rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255,255,255,0.03) 1px, transparent 1px);
  mask-image: linear-gradient(to bottom, transparent, black 30%, black 70%, transparent);
  -webkit-mask-image: linear-gradient(to bottom, transparent, black 30%, black 70%, transparent);
}

.footer-aurora {
  background: radial-gradient(
    circle at 50% 50%,
    rgba(124,58,237,0.15) 0%,
    rgba(109,40,217,0.08) 40%,
    transparent 70%
  );
}

.footer-glass-pill {
  background: linear-gradient(145deg, var(--pill-bg-1) 0%, var(--pill-bg-2) 100%);
  box-shadow:
    0 10px 30px -10px var(--pill-shadow),
    inset 0 1px 1px var(--pill-highlight),
    inset 0 -1px 2px var(--pill-inset-shadow);
  border: 1px solid var(--pill-border);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.footer-glass-pill:hover {
  background: linear-gradient(145deg, var(--pill-bg-1-hover) 0%, var(--pill-bg-2-hover) 100%);
  border-color: var(--pill-border-hover);
  box-shadow:
    0 20px 40px -10px var(--pill-shadow-hover),
    inset 0 1px 1px var(--pill-highlight-hover);
  color: #fff;
}

.footer-giant-bg-text {
  font-size: 26vw;
  line-height: 0.75;
  font-weight: 900;
  letter-spacing: -0.05em;
  color: transparent;
  -webkit-text-stroke: 1px rgba(255,255,255,0.05);
  background: linear-gradient(180deg, rgba(255,255,255,0.10) 0%, transparent 60%);
  -webkit-background-clip: text;
  background-clip: text;
}

.footer-text-glow {
  background: linear-gradient(180deg, #f0f0f0 0%, rgba(240,240,240,0.4) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0px 0px 20px rgba(240,240,240,0.15));
}
`;

// -------------------------------------------------------------------------
// 2. MAGNETIC BUTTON
// -------------------------------------------------------------------------
const MagneticButton = React.forwardRef(({ className, children, as: Component = "button", ...props }, forwardedRef) => {
  const localRef = useRef(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const element = localRef.current;
    if (!element) return;

    const ctx = gsap.context(() => {
      const handleMouseMove = (e) => {
        const rect = element.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        gsap.to(element, { x: x * 0.4, y: y * 0.4, rotationX: -y * 0.15, rotationY: x * 0.15, scale: 1.05, ease: "power2.out", duration: 0.4 });
      };
      const handleMouseLeave = () => {
        gsap.to(element, { x: 0, y: 0, rotationX: 0, rotationY: 0, scale: 1, ease: "elastic.out(1, 0.3)", duration: 1.2 });
      };
      element.addEventListener("mousemove", handleMouseMove);
      element.addEventListener("mouseleave", handleMouseLeave);
      return () => {
        element.removeEventListener("mousemove", handleMouseMove);
        element.removeEventListener("mouseleave", handleMouseLeave);
      };
    }, element);

    return () => ctx.revert();
  }, []);

  return (
    <Component
      ref={(node) => {
        localRef.current = node;
        if (typeof forwardedRef === "function") forwardedRef(node);
        else if (forwardedRef) forwardedRef.current = node;
      }}
      className={`cursor-pointer ${className || ""}`}
      {...props}
    >
      {children}
    </Component>
  );
});
MagneticButton.displayName = "MagneticButton";

// -------------------------------------------------------------------------
// 3. MARQUEE ITEM
// -------------------------------------------------------------------------
const MarqueeItem = () => (
  <div className="flex items-center space-x-12 px-6">
    <span>Find Student Talent</span> <span className="text-purple-400/60">✦</span>
    <span>Post a Mission</span> <span className="text-purple-300/60">✦</span>
    <span>Launch Your Gig</span> <span className="text-purple-400/60">✦</span>
    <span>Hire Smart</span> <span className="text-purple-300/60">✦</span>
    <span>Built for Students</span> <span className="text-purple-400/60">✦</span>
    <span>Join the Future of Work</span> <span className="text-purple-300/60">✦</span>
  </div>
);

// -------------------------------------------------------------------------
// 4. MAIN COMPONENT
// -------------------------------------------------------------------------
export function CinematicFooter() {
  const wrapperRef = useRef(null);
  const giantTextRef = useRef(null);
  const headingRef = useRef(null);
  const linksRef = useRef(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    if (!wrapperRef.current) return;

    const ctx = gsap.context(() => {
      gsap.fromTo(
        giantTextRef.current,
        { y: "10vh", scale: 0.8, opacity: 0 },
        {
          y: "0vh", scale: 1, opacity: 1, ease: "power1.out",
          scrollTrigger: { trigger: wrapperRef.current, start: "top 80%", end: "bottom bottom", scrub: 1 },
        }
      );

      gsap.fromTo(
        [headingRef.current, linksRef.current],
        { y: 50, opacity: 0 },
        {
          y: 0, opacity: 1, stagger: 0.15, ease: "power3.out",
          scrollTrigger: { trigger: wrapperRef.current, start: "top 40%", end: "bottom bottom", scrub: 1 },
        }
      );
    }, wrapperRef);

    return () => ctx.revert();
  }, []);

  const scrollToTop = () => window.scrollTo({ top: 0, behavior: "smooth" });

  return (
    <>
      <style dangerouslySetInnerHTML={{ __html: STYLES }} />

      <div
        ref={wrapperRef}
        className="relative h-screen w-full"
        style={{ clipPath: "polygon(0% 0, 100% 0%, 100% 100%, 0 100%)" }}
      >
        <footer className="fixed bottom-0 left-0 flex h-screen w-full flex-col justify-between overflow-hidden bg-[#0a0a0a] text-[#f0f0f0] cinematic-footer-wrapper">

          {/* Aurora + Grid */}
          <div className="footer-aurora absolute left-1/2 top-1/2 h-[60vh] w-[80vw] -translate-x-1/2 -translate-y-1/2 animate-footer-breathe rounded-[50%] blur-[80px] pointer-events-none z-0" />
          <div className="footer-bg-grid absolute inset-0 z-0 pointer-events-none" />

          {/* Giant background text */}
          <div
            ref={giantTextRef}
            className="footer-giant-bg-text absolute -bottom-[5vh] left-1/2 -translate-x-1/2 whitespace-nowrap z-0 pointer-events-none select-none"
          >
            STULANCE
          </div>

          {/* Diagonal Marquee */}
          <div className="absolute top-12 left-0 w-full overflow-hidden border-y border-white/[0.07] bg-black/60 backdrop-blur-md py-4 z-10 -rotate-2 scale-110 shadow-2xl">
            <div className="flex w-max animate-footer-scroll-marquee text-xs font-bold tracking-[0.3em] text-[#888] uppercase">
              <MarqueeItem />
              <MarqueeItem />
            </div>
          </div>

          {/* Main Center Content */}
          <div className="relative z-10 flex flex-1 flex-col items-center justify-center px-6 mt-20 w-full max-w-5xl mx-auto">
            <h2
              ref={headingRef}
              className="text-5xl md:text-8xl font-black footer-text-glow tracking-tighter mb-12 text-center"
            >
              Ready to launch your career?
            </h2>

            <div ref={linksRef} className="flex flex-col items-center gap-6 w-full">
              {/* Primary pills */}
              <div className="flex flex-wrap justify-center gap-4 w-full">
                <MagneticButton as="a" href="/accounts/onboarding/" className="footer-glass-pill px-8 py-4 rounded-full text-[#f0f0f0] font-bold text-sm md:text-base flex items-center gap-3">
                  <span>↗</span><span>Get Started</span>
                </MagneticButton>
                <MagneticButton as="a" href="/missions/" className="footer-glass-pill px-8 py-4 rounded-full text-[#f0f0f0] font-bold text-sm md:text-base flex items-center gap-3">
                  <i className="bi bi-briefcase" /><span>Browse Missions</span>
                </MagneticButton>
                <MagneticButton as="a" href="/gigs/" className="footer-glass-pill px-8 py-4 rounded-full text-[#f0f0f0] font-bold text-sm md:text-base flex items-center gap-3">
                  <i className="bi bi-stars" /><span>Explore Talent</span>
                </MagneticButton>
              </div>

              {/* Secondary text links */}
              <div className="flex flex-wrap justify-center gap-2 md:gap-4 w-full mt-2">
                <MagneticButton as="a" href="/help/" className="footer-glass-pill px-4 py-2 rounded-full text-[11px]" style={{color:'#999',fontWeight:'700'}}>
                  Help
                </MagneticButton>
                <MagneticButton as="a" href="/tos/" className="footer-glass-pill px-4 py-2 rounded-full text-[11px]" style={{color:'#999',fontWeight:'700'}}>
                  Terms of Service
                </MagneticButton>
                <MagneticButton as="a" href="/contact/" className="footer-glass-pill px-4 py-2 rounded-full text-[11px]" style={{color:'#999',fontWeight:'700'}}>
                  Contact
                </MagneticButton>
                <MagneticButton as="a" href="/email-us/" className="footer-glass-pill px-4 py-2 rounded-full text-[11px]" style={{color:'#999',fontWeight:'700'}}>
                  Email Us
                </MagneticButton>
              </div>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="relative z-20 w-full pb-8 px-6 md:px-12 flex flex-row items-center justify-between gap-6">
            <div className="text-[#888] text-[10px] md:text-xs font-semibold tracking-widest uppercase">
              © 2026 StuLance. All rights reserved.
            </div>

            <MagneticButton
              as="button"
              onClick={scrollToTop}
              className="w-12 h-12 rounded-full footer-glass-pill flex items-center justify-center text-[#888] hover:text-[#f0f0f0] group order-3"
            >
              <svg className="w-5 h-5 transform group-hover:-translate-y-1.5 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
            </MagneticButton>
          </div>

        </footer>
      </div>
    </>
  );
}
