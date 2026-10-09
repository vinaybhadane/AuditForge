'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowRight, ShieldCheck } from 'lucide-react';

export function FinalCta() {
  return (
    <section
      aria-label="Call to Action"
      className="py-28 sm:py-36 bg-[#050505] text-white relative overflow-hidden border-b border-white/10"
    >
      {/* Background Architectural Grid Lines */}
      <div
        className="absolute inset-0 bg-blueprint-lines opacity-20 pointer-events-none"
        aria-hidden="true"
      />

      {/* Subtle Soft Emerald Ambient Radial Glow */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[550px] rounded-full bg-emerald-500/[0.04] blur-3xl pointer-events-none"
        aria-hidden="true"
      />

      <div className="container relative mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 text-center space-y-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/[0.04] border border-white/10 text-xs font-mono tracking-widest text-[#A3A3A3]">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          <span>ENTERPRISE CONSTRUCTION AUDITING</span>
        </div>

        {/* Large Newsreader Headline with Emerald Italic Emphasis */}
        <h2 className="font-serif text-4xl sm:text-5xl lg:text-6xl font-normal tracking-tight text-white leading-tight">
          Make every construction claim{' '}
          <span className="italic text-emerald-400 font-serif">accountable</span>.
        </h2>

        {/* Supporting Copy */}
        <p className="text-base sm:text-lg text-[#888888] max-w-2xl mx-auto leading-relaxed font-sans">
          Bring evidence, material records, and audit decisions into one traceable workflow.
        </p>

        {/* Primary Action Button */}
        <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2.5 px-8 py-3.5 rounded-full text-sm font-mono font-medium text-[#050505] bg-emerald-400 hover:bg-emerald-300 hover:shadow-xl hover:shadow-emerald-500/20 transition-all duration-200 group"
          >
            <span>Start Auditing with Confidence</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
          </Link>
        </div>

        {/* Secondary Trust Line */}
        <div className="pt-2 text-xs font-mono tracking-widest text-[#888888]">
          <span>Evidence-first. Explainable. Human-reviewed.</span>
        </div>
      </div>
    </section>
  );
}
