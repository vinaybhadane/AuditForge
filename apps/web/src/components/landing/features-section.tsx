'use client';

import React from 'react';
import {
  Camera,
  Layers,
  FileText,
  ShieldCheck,
  CheckCircle2,
  ArrowRight,
  TrendingDown,
  Hash,
  Sparkles,
} from 'lucide-react';

interface PillarCard {
  label: string;
  title: string;
  description: string;
  visual: React.ReactNode;
}

export function FeaturesSection() {
  return (
    <section
      id="features"
      aria-label="The Audit Intelligence System Four Pillars"
      className="py-24 sm:py-32 bg-[#050505] border-b border-white/10 relative overflow-hidden"
    >
      {/* Background Architectural Blueprint Grid Lines */}
      <div
        className="absolute inset-0 bg-blueprint-lines opacity-20 pointer-events-none"
        aria-hidden="true"
      />
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-emerald-500/[0.03] rounded-full blur-3xl pointer-events-none"
        aria-hidden="true"
      />

      <div className="container relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mb-16 sm:mb-20 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/[0.04] border border-white/10 text-xs font-mono tracking-widest text-[#A3A3A3]">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            <span>THE AUDIT INTELLIGENCE SYSTEM</span>
          </div>

          <h2 className="font-serif text-4xl sm:text-5xl lg:text-5.5xl font-normal tracking-tight text-white leading-[1.05]">
            From scattered records to <span className="italic text-emerald-400">defensible</span> decisions.
          </h2>

          <p className="text-base sm:text-lg text-[#888888] leading-relaxed max-w-2xl font-sans">
            Bring site evidence, construction documents, material records, and audit
            findings into one traceable verification workflow.
          </p>
        </div>

        {/* Bento Grid: Four Capability Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Card 01 — AI-Powered Site Verification (7 cols on lg) */}
          <div className="lg:col-span-7 p-6 sm:p-8 rounded-2xl bg-white/[0.025] hover:bg-white/[0.04] border border-white/10 hover:border-emerald-500/30 transition-all duration-300 flex flex-col justify-between group shadow-xl">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-[11px] tracking-wider text-emerald-400 bg-emerald-500/10 border border-emerald-500/25 px-2.5 py-1 rounded">
                  VISUAL INTELLIGENCE / 01
                </span>
                <Camera className="w-4 h-4 text-emerald-400" />
              </div>

              <h3 className="font-serif text-2xl sm:text-3xl font-medium text-white tracking-tight">
                AI-Powered Site Verification
              </h3>

              <p className="text-sm text-[#888888] leading-relaxed max-w-xl font-sans">
                Assess verified live camera site photographs against defined milestone acceptance
                criteria. Cryptographic tamper checks and vision models validate real physical
                progress before clearance.
              </p>
            </div>

            {/* Visual: Miniature Architectural Wireframe & Verification Stamp */}
            <div className="mt-8 pt-6 border-t border-white/10">
              <div className="p-4 rounded-xl bg-black/60 border border-white/10 font-mono text-xs space-y-3">
                <div className="flex items-center justify-between text-[11px] text-[#A3A3A3]">
                  <span className="flex items-center gap-1.5 text-emerald-400">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    CRIT-COL-204 · PLUMB LINE TOLERANCE
                  </span>
                  <span>SHA-256 HASH VERIFIED</span>
                </div>
                <div className="grid grid-cols-3 gap-2 text-center text-[10px]">
                  <div className="p-2 rounded bg-white/[0.03] border border-white/10">
                    <span className="text-[#888888] block">CAPTURE</span>
                    <span className="text-white font-bold">LIVE SENSOR</span>
                  </div>
                  <div className="p-2 rounded bg-white/[0.03] border border-white/10">
                    <span className="text-[#888888] block">ELEVATION</span>
                    <span className="text-white font-bold">+4.40M</span>
                  </div>
                  <div className="p-2 rounded bg-emerald-500/10 border border-emerald-500/30">
                    <span className="text-emerald-400 block">OBSERVATION</span>
                    <span className="text-emerald-300 font-bold">98.4% ALIGNED</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Card 02 — Material Reconciliation (5 cols on lg) */}
          <div className="lg:col-span-5 p-6 sm:p-8 rounded-2xl bg-white/[0.025] hover:bg-white/[0.04] border border-white/10 hover:border-emerald-500/30 transition-all duration-300 flex flex-col justify-between group shadow-xl">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-[11px] tracking-wider text-emerald-400 bg-emerald-500/10 border border-emerald-500/25 px-2.5 py-1 rounded">
                  QUANTITY ANALYSIS / 02
                </span>
                <Layers className="w-4 h-4 text-emerald-400" />
              </div>

              <h3 className="font-serif text-2xl sm:text-3xl font-medium text-white tracking-tight">
                Material Reconciliation
              </h3>

              <p className="text-sm text-[#888888] leading-relaxed font-sans">
                Compare BOQ schedules, POs, delivery challans, issues, and recorded consumption
                through deterministic decimal math. Never confuse purchased with installed.
              </p>
            </div>

            {/* Visual: Material-Flow Connecting Diagram */}
            <div className="mt-8 pt-6 border-t border-white/10">
              <div className="p-4 rounded-xl bg-black/60 border border-white/10 font-mono text-xs space-y-2.5">
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-[#A3A3A3]">PO-0842 · TMT Steel</span>
                  <span className="text-amber-400 font-bold">VARIANCE: -2.40 MT</span>
                </div>
                <div className="flex items-center gap-2 text-[10px] text-[#888888]">
                  <span>Ordered: 50.00 MT</span>
                  <span>→</span>
                  <span>Delivered: 50.00 MT</span>
                  <span>→</span>
                  <span className="text-rose-400">Issued: 47.60 MT</span>
                </div>
              </div>
            </div>
          </div>

          {/* Card 03 — Document Intelligence (5 cols on lg) */}
          <div className="lg:col-span-5 p-6 sm:p-8 rounded-2xl bg-white/[0.025] hover:bg-white/[0.04] border border-white/10 hover:border-emerald-500/30 transition-all duration-300 flex flex-col justify-between group shadow-xl">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-[11px] tracking-wider text-emerald-400 bg-emerald-500/10 border border-emerald-500/25 px-2.5 py-1 rounded">
                  DOCUMENT EXTRACTION / 03
                </span>
                <FileText className="w-4 h-4 text-emerald-400" />
              </div>

              <h3 className="font-serif text-2xl sm:text-3xl font-medium text-white tracking-tight">
                Document Intelligence
              </h3>

              <p className="text-sm text-[#888888] leading-relaxed font-sans">
                Extract line items, tax IDs, challan weight tickets, and vehicle records with source
                bounding box provenance for complete audit trail defensibility.
              </p>
            </div>

            {/* Visual: Layered Document Extraction Interface */}
            <div className="mt-8 pt-6 border-t border-white/10">
              <div className="p-3.5 rounded-xl bg-black/60 border border-white/10 font-mono text-xs space-y-2">
                <div className="flex items-center justify-between text-[11px] text-emerald-400">
                  <span>TAX INVOICE #INV-8821</span>
                  <span>OCR CONF: 99.2%</span>
                </div>
                <div className="text-[10px] text-[#A3A3A3] flex items-center justify-between border-t border-white/10 pt-1.5">
                  <span>Vendor: UltraTech Concrete</span>
                  <span>Net: $42,650.00</span>
                </div>
              </div>
            </div>
          </div>

          {/* Card 04 — Evidence-Linked Audit Reports (7 cols on lg) */}
          <div className="lg:col-span-7 p-6 sm:p-8 rounded-2xl bg-white/[0.025] hover:bg-white/[0.04] border border-white/10 hover:border-emerald-500/30 transition-all duration-300 flex flex-col justify-between group shadow-xl">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-[11px] tracking-wider text-emerald-400 bg-emerald-500/10 border border-emerald-500/25 px-2.5 py-1 rounded">
                  TRACEABLE FINDINGS / 04
                </span>
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
              </div>

              <h3 className="font-serif text-2xl sm:text-3xl font-medium text-white tracking-tight">
                Evidence-Linked Audit Reports
              </h3>

              <p className="text-sm text-[#888888] leading-relaxed max-w-xl font-sans">
                Surface findings with mathematical discrepancy proofs, AI visual confidence
                distributions, and source document links. Authoritative signoffs gate every
                clearance certificate.
              </p>
            </div>

            {/* Visual: Audit Finding Connected to Evidence References */}
            <div className="mt-8 pt-6 border-t border-white/10">
              <div className="p-4 rounded-xl bg-black/60 border border-white/10 font-mono text-xs space-y-2.5">
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-white font-semibold">FINDING #AF-4091</span>
                  <span className="text-emerald-400 font-mono">CLEARED BY HUMAN AUDITOR</span>
                </div>
                <div className="text-[11px] text-[#888888] flex flex-wrap items-center gap-3">
                  <span className="px-2 py-0.5 rounded bg-white/5 border border-white/10">REF: CH-4091</span>
                  <span className="px-2 py-0.5 rounded bg-white/5 border border-white/10">REF: IMG-842</span>
                  <span className="px-2 py-0.5 rounded bg-white/5 border border-white/10">REF: PO-842</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
