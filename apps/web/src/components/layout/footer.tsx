'use client';

import React from 'react';
import Link from 'next/link';
import { ShieldCheck, Compass, GitBranch, Lock } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-border bg-surface-0 py-12 text-xs text-text-secondary">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
          {/* Col 1: Brand & Description */}
          <div className="md:col-span-5 space-y-3">
            <Link href="/" className="flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-950 text-white shadow-sm border border-brand-800">
                <ShieldCheck className="h-4.5 w-4.5 text-signal-amber" />
              </div>
              <span className="text-base font-black tracking-tight text-brand-950">
                AuditForge
              </span>
            </Link>
            <p className="text-xs text-text-secondary leading-relaxed max-w-sm">
              Evidence-first construction operations auditing platform. Correlating visual
              milestone evidence, vendor documents, and deterministic material reconciliation.
            </p>
            <div className="font-mono text-[11px] text-text-secondary flex items-center gap-2">
              <Compass className="w-3.5 h-3.5 text-brand-700" />
              <span>COORDINATES: LAT 19.0760° N, LON 72.8777° E</span>
            </div>
          </div>

          {/* Col 2: Architectural Specifications */}
          <div className="md:col-span-4 space-y-2 font-mono text-[11px]">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-950 block mb-2 font-sans">
              System Specifications
            </span>
            <div className="flex items-center gap-2">
              <GitBranch className="w-3.5 h-3.5 text-signal-teal" />
              <span>Spec: Multi-Modal Ingestion Pipeline</span>
            </div>
            <div className="flex items-center gap-2">
              <Lock className="w-3.5 h-3.5 text-signal-amber" />
              <span>Storage: Private Object Encryption (SHA-256)</span>
            </div>
            <div className="flex items-center gap-2 text-text-secondary">
              <span>Engine: Deterministic Decimal Math v1.0</span>
            </div>
          </div>

          {/* Col 3: Links */}
          <div className="md:col-span-3 space-y-2">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-950 block mb-2 font-sans">
              Platform Links
            </span>
            <ul className="space-y-1.5 text-xs">
              <li>
                <Link href="/dashboard" className="hover:text-brand-950 transition-colors">
                  Operational Dashboard
                </Link>
              </li>
              <li>
                <Link href="/login" className="hover:text-brand-950 transition-colors">
                  Sign In to Organization
                </Link>
              </li>
              <li>
                <a href="#workflow" className="hover:text-brand-950 transition-colors">
                  7-Stage Lifecycle
                </a>
              </li>
              <li>
                <a href="#reconciliation" className="hover:text-brand-950 transition-colors">
                  Material Reconciliation
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Disclaimer */}
        <div className="pt-8 border-t border-border/80 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-text-secondary">
          <p>© 2026 AuditForge. Every Claim. Verified by Evidence.</p>
          <p className="text-center sm:text-right max-w-xl text-[10px] text-slate-500">
            AuditForge is an evidence-first decision support system. It does not act as an autonomous
            judge, replace licensed professional engineering inspections, or provide statutory certifications.
          </p>
        </div>
      </div>
    </footer>
  );
}
