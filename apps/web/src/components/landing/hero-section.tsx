'use client';

import React, { useRef, useState, useEffect } from 'react';
import Link from 'next/link';
import {
  ArrowRight,
  ChevronDown,
  Compass,
  Play,
  Pause,
  VolumeX,
  Volume2,
  Video,
} from 'lucide-react';

export function HeroSection() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState<boolean>(true);
  const [isMuted, setIsMuted] = useState<boolean>(true);

  // Guarantee continuous looping autoplay on mount
  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.play().catch(() => {
        // Autoplay policy handled gracefully
        setIsPlaying(false);
      });
    }
  }, []);

  const togglePlayback = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
      setIsPlaying(false);
    } else {
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  const toggleMute = () => {
    if (!videoRef.current) return;
    videoRef.current.muted = !isMuted;
    setIsMuted(!isMuted);
  };

  return (
    <section
      id="hero"
      aria-label="Hero Introduction and Full-Screen Construction Video Background"
      className="relative min-h-[100svh] w-full flex flex-col justify-between pt-28 pb-8 overflow-hidden bg-[#050505]"
    >
      {/* ---------------- 1. FULL-SCREEN CONTINUOUS VIDEO BACKGROUND ---------------- */}
      <div className="absolute inset-0 z-0 overflow-hidden">
        <video
          ref={videoRef}
          autoPlay
          loop
          muted
          playsInline
          preload="auto"
          className="absolute inset-0 w-full h-full object-cover object-center scale-[1.02] filter brightness-[0.78] contrast-[1.08] transition-transform duration-1000 ease-out"
        >
          <source src="/construction.mp4" type="video/mp4" />
          <source src="/models/construction.mp4" type="video/mp4" />
          Your browser does not support HTML5 video background.
        </video>

        {/* Ambient Darkened Film Layer */}
        <div
          className="absolute inset-0 bg-[#050505]/35 pointer-events-none"
          aria-hidden="true"
        />
      </div>

      {/* ---------------- 2. DARK CINEMATIC GRADIENT OVERLAYS ---------------- */}
      {/* Left directional darkening ensures text on left is crystal clear */}
      <div
        className="absolute inset-0 z-10 pointer-events-none bg-gradient-to-r from-[#050505] via-[#050505]/85 md:via-[#050505]/70 to-[#050505]/25"
        aria-hidden="true"
      />
      {/* Top and bottom vertical blends */}
      <div
        className="absolute inset-0 z-10 pointer-events-none bg-gradient-to-b from-[#050505]/90 via-transparent to-[#050505]"
        aria-hidden="true"
      />
      <div
        className="absolute inset-0 z-10 pointer-events-none bg-gradient-to-t from-[#050505] via-transparent to-[#050505]/40"
        aria-hidden="true"
      />

      {/* ---------------- 3. SUBTLE BLUEPRINT GRID OVERLAY ---------------- */}
      <div
        className="absolute inset-0 z-10 pointer-events-none opacity-20 bg-blueprint-lines"
        aria-hidden="true"
      />

      {/* ---------------- 4. HERO CONTENT CONTAINER ---------------- */}
      <div className="container relative z-20 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 my-auto pointer-events-none">
        <div className="max-w-2xl py-8">
          {/* Technical Eyebrow */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/[0.04] border border-white/10 text-xs font-mono tracking-widest text-[#A3A3A3] mb-6 shadow-sm backdrop-blur-md">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>CONSTRUCTION INTELLIGENCE / PLATFORM 01</span>
          </div>

          {/* Main Headline with Newsreader Serif & Emerald Italic Emphasis */}
          <h1 className="font-serif text-[clamp(2.75rem,5.5vw,5.25rem)] font-normal tracking-tight text-white leading-[0.94] mb-6 drop-shadow-lg">
            Every Claim.
            <br />
            Verified by{' '}
            <span className="italic text-emerald-400 font-serif font-normal">
              Evidence
            </span>
            .
          </h1>

          {/* Supporting Editorial Copy */}
          <p className="text-base sm:text-lg text-[#A3A3A3] leading-relaxed max-w-xl mb-8 font-sans drop-shadow">
            Verify construction progress, reconcile material records, and
            investigate discrepancies through AI-powered analysis and traceable
            evidence.
          </p>

          {/* Call to Actions */}
          <div className="pointer-events-auto flex flex-wrap items-center gap-4 mb-10">
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-full text-xs sm:text-sm font-mono font-medium text-[#050505] bg-emerald-400 hover:bg-emerald-300 hover:shadow-lg hover:shadow-emerald-500/25 transition-all duration-200 group"
            >
              <span>Explore AuditForge</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
            </Link>

            <a
              href="#workflow"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-full text-xs sm:text-sm font-mono text-white bg-white/[0.05] hover:bg-white/[0.09] border border-white/15 hover:border-white/30 backdrop-blur-sm transition-all duration-200"
            >
              <span>See How It Works</span>
              <ChevronDown className="w-4 h-4 text-[#888888]" />
            </a>
          </div>

          {/* Evidence-First Trust Strip */}
          <div className="flex flex-wrap items-center gap-3 text-xs font-mono tracking-widest text-[#888888]">
            <span className="text-emerald-400/90 font-semibold">EVIDENCE-FIRST</span>
            <span className="text-white/20">·</span>
            <span>EXPLAINABLE</span>
            <span className="text-white/20">·</span>
            <span>HUMAN-REVIEWED</span>
          </div>
        </div>
      </div>

      {/* ---------------- 5. FLOATING LIVE TELEMETRY VIDEO CONTROLS ---------------- */}
      <div className="absolute bottom-20 right-6 sm:right-8 z-20 pointer-events-none hidden sm:flex flex-col items-end gap-2">
        {/* Live Video Feed Status Chip */}
        <div className="pointer-events-auto flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#050505]/85 backdrop-blur-md border border-white/10 shadow-2xl text-[11px] font-mono text-slate-300">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
          <Video className="w-3.5 h-3.5 text-emerald-400" />
          <span className="font-semibold text-white">LIVE SITE TELEMETRY</span>
          <span className="text-white/20">|</span>
          <span className="text-[#888888]">CONTINUOUS FEED</span>
        </div>

        {/* Playback Controls */}
        <div className="pointer-events-auto flex items-center gap-1.5 p-1 rounded-xl bg-[#050505]/80 backdrop-blur-md border border-white/10 shadow-xl">
          <button
            type="button"
            onClick={togglePlayback}
            aria-label={isPlaying ? 'Pause background video' : 'Play background video'}
            title={isPlaying ? 'Pause Video' : 'Play Video'}
            className="p-1.5 rounded-lg text-[#A3A3A3] hover:text-white hover:bg-white/10 transition-colors"
          >
            {isPlaying ? (
              <Pause className="w-3.5 h-3.5 text-emerald-400" />
            ) : (
              <Play className="w-3.5 h-3.5 text-white" />
            )}
          </button>

          <button
            type="button"
            onClick={toggleMute}
            aria-label={isMuted ? 'Unmute video audio' : 'Mute video audio'}
            title={isMuted ? 'Unmute' : 'Mute'}
            className="p-1.5 rounded-lg text-[#A3A3A3] hover:text-white hover:bg-white/10 transition-colors"
          >
            {isMuted ? (
              <VolumeX className="w-3.5 h-3.5 text-[#888888]" />
            ) : (
              <Volume2 className="w-3.5 h-3.5 text-emerald-400" />
            )}
          </button>
        </div>
      </div>

      {/* ---------------- 6. BOTTOM TECHNICAL STATUS STRIP ---------------- */}
      <div className="container relative z-20 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 border-t border-white/10 pt-4 flex flex-wrap items-center justify-between gap-4 text-xs font-mono text-[#888888]">
        {/* Left: Scroll indicator */}
        <a
          href="#features"
          className="pointer-events-auto inline-flex items-center gap-2 text-[#888888] hover:text-white transition-colors group"
        >
          <ChevronDown className="w-3.5 h-3.5 text-emerald-400 group-hover:translate-y-0.5 transition-transform" />
          <span>Scroll to Explore</span>
        </a>

        {/* Center: Coordinates datum */}
        <div className="hidden sm:flex items-center gap-2 text-[11px] text-[#666666]">
          <Compass className="w-3 h-3 text-emerald-400" />
          <span>DATUM: LAT 19.0760° N, LON 72.8777° E</span>
          <span className="text-white/20">|</span>
          <span>ELEVATION +14.2M</span>
        </div>

        {/* Right: Technical label */}
        <div className="text-[11px] tracking-wider text-[#888888]">
          SITE INTELLIGENCE / EVIDENCE-LED AUDITING
        </div>
      </div>
    </section>
  );
}
