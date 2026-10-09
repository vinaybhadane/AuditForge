'use client';

import React from 'react';
import Link from 'next/link';
import { Compass, ShieldCheck, GitBranch, ArrowUpRight } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-white/10 bg-[#050505] py-14 text-xs text-[#888888] font-mono">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 space-y-10">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-10 items-start">
          {/* Col 1: Brand & Purpose */}
          <div className="md:col-span-5 space-y-4">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white/[0.04] border border-white/10 text-emerald-400 group-hover:border-emerald-500/40 transition-colors">
                <div className="w-3.5 h-3.5 border-2 border-emerald-400 rotate-45 flex items-center justify-center">
                  <div className="w-1 h-1 bg-emerald-400 rounded-full" />
                </div>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="font-serif text-lg tracking-tight font-bold text-white">
                  AuditForge
                </span>
                <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400" />
              </div>
            </Link>

            <p className="text-xs text-[#888888] leading-relaxed max-w-sm font-sans">
              Evidence-first construction operations and intelligence platform. Correlating
              visual milestone evidence, vendor documents, and deterministic material reconciliation.
            </p>

            <div className="text-[11px] text-[#A3A3A3] flex items-center gap-2 pt-1">
              <Compass className="w-3.5 h-3.5 text-emerald-400" />
              <span>COORDINATES: LAT 19.0760° N, LON 72.8777° E</span>
              <span className="text-white/20">|</span>
              <span>DATUM: WGS84</span>
            </div>
          </div>

          {/* Col 2: System Specifications */}
          <div className="md:col-span-4 space-y-3">
            <span className="text-[11px] font-mono uppercase tracking-widest text-white/90 block mb-3 font-semibold">
              System Specifications
            </span>
            <div className="space-y-2 text-[11px] text-[#888888]">
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                <span>Engine: Deterministic Decimal Math RFC-08/11</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-white/30" />
                <span>Hashing: SHA-256 Tamper Verification Chain</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-white/30" />
                <span>Decision Control: Authorized Human Signoff Gate</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-white/30" />
                <span>Storage: Private Object Encryption (Tenant-Isolated)</span>
              </div>
            </div>
          </div>

          {/* Col 3: Platform Links */}
          <div className="md:col-span-3 space-y-3">
            <span className="text-[11px] font-mono uppercase tracking-widest text-white/90 block mb-3 font-semibold">
              Platform Links
            </span>
            <ul className="space-y-2 text-xs">
              <li>
                <Link
                  href="/dashboard"
                  className="hover:text-emerald-400 text-[#A3A3A3] transition-colors inline-flex items-center gap-1 group"
                >
                  <span>Auditor Workspace</span>
                  <ArrowUpRight className="w-3 h-3 text-white/30 group-hover:text-emerald-400 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                </Link>
              </li>
              <li>
                <Link
                  href="/login"
                  className="hover:text-emerald-400 text-[#A3A3A3] transition-colors inline-flex items-center gap-1 group"
                >
                  <span>Client Sign In</span>
                  <ArrowUpRight className="w-3 h-3 text-white/30 group-hover:text-emerald-400 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                </Link>
              </li>
              <li>
                <a
                  href="#workflow"
                  className="hover:text-emerald-400 text-[#A3A3A3] transition-colors"
                >
                  Verification Pipeline
                </a>
              </li>
              <li>
                <a
                  href="#reconciliation"
                  className="hover:text-emerald-400 text-[#A3A3A3] transition-colors"
                >
                  Material Reconciliation
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Legal & Provenance */}
        <div className="pt-8 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-[#888888]">
          <p>© {new Date().getFullYear()} AuditForge Inc. All rights reserved. Every claim. Verified by evidence.</p>
          <div className="flex items-center gap-4 text-white/50">
            <span>Decision Support System</span>
            <span>•</span>
            <span>Non-Autonomous Final Judgment</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
