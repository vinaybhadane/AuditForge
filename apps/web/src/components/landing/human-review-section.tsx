'use client';

import React, { useState } from 'react';
import {
  UserCheck,
  CheckCircle2,
  AlertTriangle,
  FileQuestion,
  ShieldCheck,
  Lock,
  ArrowRight,
  Eye,
  History,
  FileText,
} from 'lucide-react';

export function HumanReviewSection() {
  const [selectedAction, setSelectedAction] = useState<
    'approve' | 'reject' | 'request'
  >('request');
  const [reviewerNotes, setReviewerNotes] = useState<string>(
    'Reconcile weighbridge slip #841 with subcontractor batch tally before approving clearance certificate.'
  );
  const [actionSubmitted, setActionSubmitted] = useState<boolean>(false);

  return (
    <section
      id="review"
      aria-label="Human Review Authority and Decision Governance"
      className="py-24 sm:py-32 bg-[#050505] border-b border-white/10 relative overflow-hidden"
    >
      <div
        className="absolute inset-0 bg-blueprint-lines opacity-15 pointer-events-none"
        aria-hidden="true"
      />

      <div className="container relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mb-16 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/[0.04] border border-white/10 text-xs font-mono tracking-widest text-[#A3A3A3]">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            <span>TRUST THROUGH TRANSPARENCY</span>
          </div>

          <h2 className="font-serif text-4xl sm:text-5xl lg:text-5.5xl font-normal tracking-tight text-white leading-[1.05]">
            AI surfaces the signal.{' '}
            <span className="italic text-emerald-400 font-serif">Auditors make the decision</span>.
          </h2>

          <p className="text-base sm:text-lg text-[#888888] leading-relaxed max-w-2xl font-sans">
            Keep every important conclusion explainable, reviewable, and connected to the records
            that support it. AI confidence alone cannot clear a milestone or accuse a vendor.
          </p>
        </div>

        {/* ---------------- AUDITOR BENCHMARK WORKBENCH INTERFACE ---------------- */}
        <div className="max-w-5xl mx-auto rounded-2xl bg-white/[0.025] border border-white/10 shadow-2xl overflow-hidden font-mono text-xs">
          {/* Top Workbench Status Bar */}
          <div className="p-4 sm:px-6 bg-black/80 border-b border-white/10 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
                <UserCheck className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] text-[#888888] block uppercase tracking-wider">
                  AUTHORITATIVE REVIEW GATE // MILESTONE CLEARANCE
                </span>
                <span className="text-xs font-semibold text-white">
                  M-02: Structural Columns & Reinforced Core (CRIT-COL-204)
                </span>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <span className="px-2.5 py-1 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[11px]">
                SIGNAL: REVIEW REQUIRED
              </span>
              <span className="text-[#888888] text-[11px]">FINDING-AF-0921</span>
            </div>
          </div>

          {/* Workbench Body Grid */}
          <div className="p-6 sm:p-8 space-y-6">
            {/* Row 1: Evidence Links & Extracted Values */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Box A: Relevant Evidence References */}
              <div className="p-4 rounded-xl bg-black/60 border border-white/10 space-y-3">
                <span className="text-[11px] text-emerald-400 block uppercase tracking-wider font-semibold">
                  Relevant Supporting Records
                </span>
                <div className="space-y-2 text-[11px]">
                  <div className="flex items-center justify-between p-2 rounded bg-white/[0.02] border border-white/5">
                    <span className="text-white">Live Site Photo (IMG-842)</span>
                    <span className="text-emerald-400">SHA-256 MATCH</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded bg-white/[0.02] border border-white/5">
                    <span className="text-white">Vendor Invoice (INV-8821)</span>
                    <span className="text-slate-400">50.00 MT BILLED</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded bg-white/[0.02] border border-white/5">
                    <span className="text-white">Delivery Challan (CH-4091)</span>
                    <span className="text-amber-400">47.60 MT NET</span>
                  </div>
                </div>
              </div>

              {/* Box B: AI Model Observation & Calibrated Uncertainty */}
              <div className="p-4 rounded-xl bg-black/60 border border-white/10 space-y-3">
                <span className="text-[11px] text-amber-400 block uppercase tracking-wider font-semibold">
                  AI Model Observation & Confidence
                </span>
                <div className="space-y-2 text-xs font-sans text-[#A3A3A3] leading-relaxed">
                  <p>
                    <strong className="text-white font-mono text-[11px]">Vision Model: </strong>
                    Columns stripped and cured along grid C1-D3. Visual completion aligned with
                    criteria. Vertical plumb lines within tolerance.
                  </p>
                  <div className="pt-2 border-t border-white/10 flex items-center justify-between font-mono text-[11px]">
                    <span className="text-[#888888]">Calibrated Confidence: 94.2%</span>
                    <span className="text-amber-400">*Candidate Observation Only</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Row 2: Deterministic Reconciliation Math */}
            <div className="p-4 rounded-xl bg-black/60 border border-white/10 space-y-2">
              <span className="text-[11px] text-[#A3A3A3] block uppercase tracking-wider font-semibold">
                Deterministic Ledger Discrepancy Calculation
              </span>
              <div className="p-3 rounded-lg bg-white/[0.02] border border-white/10 flex flex-wrap items-center justify-between gap-4 text-xs font-mono">
                <div>
                  <span className="text-[#888888] block text-[10px]">COMMERCIAL CLAIM</span>
                  <span className="text-white font-bold">50.00 MT ($48,250.00)</span>
                </div>
                <div>
                  <span className="text-[#888888] block text-[10px]">PHYSICAL INTAKE</span>
                  <span className="text-white font-bold">47.60 MT ($45,934.00)</span>
                </div>
                <div>
                  <span className="text-[#888888] block text-[10px]">VARIANCE DISCREPANCY</span>
                  <span className="text-rose-400 font-bold">-2.40 MT ($2,316.00 unreceived)</span>
                </div>
              </div>
            </div>

            {/* Row 3: Auditor Decision Form & Notes */}
            <div className="p-5 rounded-xl bg-black/60 border border-white/10 space-y-4">
              <span className="text-[11px] text-white block uppercase tracking-wider font-semibold">
                Auditor Determination & Reviewer Notes
              </span>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setSelectedAction('request');
                    setActionSubmitted(false);
                  }}
                  className={`px-4 py-2 rounded-lg text-xs font-mono transition-all ${
                    selectedAction === 'request'
                      ? 'bg-amber-500/20 text-amber-300 border border-amber-500/50 font-bold'
                      : 'bg-white/[0.04] text-[#888888] hover:text-white border border-white/10'
                  }`}
                >
                  Request Supporting Evidence
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setSelectedAction('reject');
                    setActionSubmitted(false);
                  }}
                  className={`px-4 py-2 rounded-lg text-xs font-mono transition-all ${
                    selectedAction === 'reject'
                      ? 'bg-rose-500/20 text-rose-300 border border-rose-500/50 font-bold'
                      : 'bg-white/[0.04] text-[#888888] hover:text-white border border-white/10'
                  }`}
                >
                  Issue Discrepancy Notice
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setSelectedAction('approve');
                    setActionSubmitted(false);
                  }}
                  className={`px-4 py-2 rounded-lg text-xs font-mono transition-all ${
                    selectedAction === 'approve'
                      ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 font-bold'
                      : 'bg-white/[0.04] text-[#888888] hover:text-white border border-white/10'
                  }`}
                >
                  Approve Clearance Certificate
                </button>
              </div>

              {/* Notes Input */}
              <div>
                <label className="text-[10px] text-[#888888] block uppercase mb-1">
                  Auditor Audit Trail Commentary
                </label>
                <textarea
                  value={reviewerNotes}
                  onChange={(e) => setReviewerNotes(e.target.value)}
                  rows={2}
                  className="w-full p-3 rounded-lg bg-white/[0.03] border border-white/10 text-white font-sans text-xs focus:outline-none focus:border-emerald-500/50 resize-none"
                />
              </div>

              {/* Submit Action */}
              <div className="flex items-center justify-between pt-2">
                <span className="text-[10px] text-[#666666]">
                  Signed by: Senior Technical Auditor #AUD-409 · RBAC Gate Verified
                </span>
                <button
                  type="button"
                  onClick={() => setActionSubmitted(true)}
                  className="px-5 py-2 rounded-lg bg-emerald-400 text-[#050505] hover:bg-emerald-300 font-bold transition-all"
                >
                  {actionSubmitted ? 'Decision Recorded ✓' : 'Execute Auditor Decision'}
                </button>
              </div>

              {actionSubmitted && (
                <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-sans">
                  Decision successfully committed to audit ledger. Nonce: 0x99f821b · Timestamp: {new Date().toISOString()}
                </div>
              )}
            </div>

            {/* Decision History Trail */}
            <div className="pt-2 text-[11px] text-[#666666] flex items-center justify-between border-t border-white/10">
              <span className="flex items-center gap-1.5">
                <History className="w-3.5 h-3.5" />
                Audit Trail Nonce: 0x8a92...e109
              </span>
              <span>*Illustrative demonstration workbench interface.</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
