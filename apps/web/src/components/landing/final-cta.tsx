'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowRight, ShieldCheck, Database, Lock, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function FinalCta() {
  return (
    <section
      aria-label="Call to Action"
      className="py-24 bg-brand-950 text-white relative overflow-hidden border-b border-brand-800"
    >
      {/* Background Architectural Grid Lines */}
      <div
        className="absolute inset-0 bg-dark-grid opacity-30 pointer-events-none"
        aria-hidden="true"
      />

      {/* Amber radial glow */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-signal-amber/10 blur-3xl pointer-events-none"
        aria-hidden="true"
      />

      <div className="container relative mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 text-center space-y-8">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-900 border border-brand-700/80 text-xs font-mono font-medium text-signal-amber">
          <ShieldCheck className="w-4 h-4 text-signal-amber" />
          <span>ENTERPRISE CONSTRUCTION AUDITING</span>
        </div>

        <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight text-white leading-tight">
          Make every construction claim{' '}
          <span className="text-signal-amber block sm:inline">accountable.</span>
        </h2>

        <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
          Empower project owners, lenders, and audit teams with tamper-evident live camera
          provenance, deterministic material reconciliation, and defensible clearance records.
        </p>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link href="/dashboard">
            <Button
              size="lg"
              variant="primary"
              className="gap-2.5 text-base px-8 py-6 shadow-xl shadow-amber-500/10 font-bold"
            >
              Launch AuditForge Workspace
              <ArrowRight className="h-5 w-5" />
            </Button>
          </Link>
          <Link href="/login">
            <Button
              size="lg"
              variant="outline"
              className="text-base px-8 py-6 border-slate-700 text-slate-200 hover:text-white hover:bg-slate-800/80"
            >
              Sign In to Organization
            </Button>
          </Link>
        </div>

        {/* Trust & Architecture Reassurance Strip */}
        <div className="pt-10 border-t border-brand-800/80 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-mono text-slate-400">
          <div className="flex items-center justify-center gap-2">
            <Database className="w-4 h-4 text-signal-teal" />
            <span>PostgreSQL NUMERIC Precision</span>
          </div>
          <div className="flex items-center justify-center gap-2">
            <Lock className="w-4 h-4 text-signal-amber" />
            <span>Private Object Storage Default</span>
          </div>
          <div className="flex items-center justify-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Strict Tenant Isolation</span>
          </div>
        </div>
      </div>
    </section>
  );
}
