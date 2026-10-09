'use client';

import React, { useState } from 'react';
import {
  UserCheck,
  CheckCircle2,
  AlertCircle,
  FileCheck2,
  Lock,
  ArrowRight,
  Shield,
  HelpCircle,
  XCircle,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

export function HumanReviewSection() {
  const [selectedDecision, setSelectedDecision] = useState<
    'hold' | 'evidence' | 'approve' | 'reject'
  >('hold');

  return (
    <section
      id="review"
      aria-label="Human Review and Clearance Authority"
      className="py-20 bg-surface-0 border-b border-border relative overflow-hidden"
    >
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-100 border border-border text-xs font-mono font-medium text-brand-700">
            <span>GOVERNANCE & ACCOUNTABILITY</span>
          </div>

          <h2 className="text-3xl sm:text-4xl font-extrabold text-brand-950 tracking-tight">
            AI surfaces the signal. Auditors make the decision.
          </h2>

          <p className="text-base sm:text-lg text-text-secondary leading-relaxed">
            AuditForge is decision support—not an autonomous judge or regulatory certifier. No model
            prediction can directly authorize payments, mutate ledger baselines, or release clearance
            certificates.
          </p>
        </div>

        {/* Auditor Workbench Mockup Container */}
        <div className="max-w-4xl mx-auto rounded-2xl bg-surface-50 border border-border shadow-xl overflow-hidden">
          {/* Workbench Top Bar */}
          <div className="p-4 sm:px-6 bg-brand-950 text-white flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-800 text-signal-amber border border-brand-700">
                <UserCheck className="w-5 h-5" />
              </div>
              <div>
                <span className="font-mono text-[11px] text-slate-400 block uppercase tracking-wider">
                  Auditor Clearance Gate // Milestone Review
                </span>
                <h3 className="text-sm sm:text-base font-bold text-white">
                  M-02: Level 2 Structural Columns & Core
                </h3>
              </div>
            </div>

            <div className="flex items-center gap-2 text-xs font-mono text-slate-300">
              <span className="px-2.5 py-1 rounded bg-brand-900 border border-brand-700">
                Reviewer: S. Jenkins (Lead Auditor)
              </span>
            </div>
          </div>

          <div className="p-6 sm:p-8 space-y-8">
            {/* Eligibility Prerequisites Checklist */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-brand-950">
                  Documented Eligibility Gates (RFC-FR-014)
                </span>
                <span className="text-xs font-mono text-danger-700 font-semibold">
                  1 Blocker Identified
                </span>
              </div>

              <div className="space-y-2 font-mono text-xs">
                {/* Gate 1 */}
                <div className="p-3 rounded-xl bg-surface-0 border border-border flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-signal-teal shrink-0" />
                    <span className="text-text-primary">
                      Gate 01: Live Camera Site Capture (6/6 viewpoints verified on site)
                    </span>
                  </div>
                  <Badge variant="verified">Passed</Badge>
                </div>

                {/* Gate 2 */}
                <div className="p-3 rounded-xl bg-surface-0 border border-border flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-signal-teal shrink-0" />
                    <span className="text-text-primary">
                      Gate 02: Cryptographic Payload Integrity (SHA-256 match verified)
                    </span>
                  </div>
                  <Badge variant="verified">Passed</Badge>
                </div>

                {/* Gate 3 */}
                <div className="p-3 rounded-xl bg-surface-0 border border-border flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-signal-teal shrink-0" />
                    <span className="text-text-primary">
                      Gate 03: Concrete Cube Test Strength (28-day curing certificate attached)
                    </span>
                  </div>
                  <Badge variant="verified">Passed</Badge>
                </div>

                {/* Gate 4 (Blocker) */}
                <div className="p-3 rounded-xl bg-red-50/70 border border-red-200 flex items-center justify-between gap-3 text-danger-700">
                  <div className="flex items-center gap-2.5 font-semibold">
                    <AlertCircle className="w-4 h-4 text-danger-700 shrink-0" />
                    <span>
                      Gate 04: Commercial Reconciliation (Cement Shortfall -20 Bags Credit Note Pending)
                    </span>
                  </div>
                  <span className="px-2 py-0.5 rounded bg-red-100 border border-red-300 font-bold text-[11px]">
                    Blocker
                  </span>
                </div>
              </div>
            </div>

            {/* Decision Controls */}
            <div className="space-y-3 pt-4 border-t border-border">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-brand-950 block">
                Authorized Review Actions
              </span>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                {/* Hold Action */}
                <button
                  type="button"
                  onClick={() => setSelectedDecision('hold')}
                  className={`p-3 rounded-xl border text-left font-mono text-xs transition-all ${
                    selectedDecision === 'hold'
                      ? 'bg-amber-950 text-white border-amber-800 shadow-md ring-2 ring-signal-amber'
                      : 'bg-surface-0 text-text-primary border-border hover:border-brand-700/50'
                  }`}
                >
                  <span className="font-bold block text-sm mb-1">
                    Hold Claim
                  </span>
                  <span className="text-[11px] text-slate-300 block">
                    Wait for credit note receipt
                  </span>
                </button>

                {/* Request Evidence Action */}
                <button
                  type="button"
                  onClick={() => setSelectedDecision('evidence')}
                  className={`p-3 rounded-xl border text-left font-mono text-xs transition-all ${
                    selectedDecision === 'evidence'
                      ? 'bg-brand-950 text-white border-brand-800 shadow-md ring-2 ring-signal-teal'
                      : 'bg-surface-0 text-text-primary border-border hover:border-brand-700/50'
                  }`}
                >
                  <span className="font-bold block text-sm mb-1">
                    Request Evidence
                  </span>
                  <span className="text-[11px] text-text-secondary block">
                    Ask for additional inspection
                  </span>
                </button>

                {/* Reject Action */}
                <button
                  type="button"
                  onClick={() => setSelectedDecision('reject')}
                  className={`p-3 rounded-xl border text-left font-mono text-xs transition-all ${
                    selectedDecision === 'reject'
                      ? 'bg-red-950 text-white border-red-800 shadow-md ring-2 ring-danger-700'
                      : 'bg-surface-0 text-text-primary border-border hover:border-brand-700/50'
                  }`}
                >
                  <span className="font-bold block text-sm mb-1">
                    Reject Milestone
                  </span>
                  <span className="text-[11px] text-text-secondary block">
                    Record formal rejection notice
                  </span>
                </button>

                {/* Issue Certificate Action (Blocked) */}
                <div
                  title="Issuance blocked by unresolved commercial discrepancy"
                  className="p-3 rounded-xl border border-dashed border-slate-300 bg-surface-100/60 text-slate-400 font-mono text-xs cursor-not-allowed flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center gap-1 font-bold text-sm mb-1">
                      <Lock className="w-3.5 h-3.5" />
                      Issue Certificate
                    </div>
                    <span className="text-[10px] leading-tight block">
                      Clearance Blocked by Gate 04
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Audit Event Signature & Snapshot */}
            <div className="p-4 rounded-xl bg-surface-100 border border-border font-mono text-xs flex flex-wrap items-center justify-between gap-4 text-text-secondary">
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-brand-700" />
                <span>
                  Audit Event ID: <strong className="text-text-primary">EVT-DEC-9912</strong>
                </span>
              </div>
              <div>
                <span>Timestamp: </span>
                <span className="text-text-primary font-semibold">2026-10-09 14:30:15 UTC</span>
              </div>
              <div>
                <span>Ledger Hash: </span>
                <span className="text-brand-700">sha256:7f42...10da</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
