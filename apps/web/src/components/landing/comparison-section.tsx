'use client';

import React from 'react';
import { CheckCircle2, ArrowRight, Minus } from 'lucide-react';

interface ComparisonRow {
  activity: string;
  traditional: string;
  auditforge: string;
}

const COMPARISON_ROWS: ComparisonRow[] = [
  {
    activity: 'Collecting supporting records',
    traditional:
      'Paper binders, emailed gallery attachments, and physical delivery challan copies manually gathered across site offices.',
    auditforge:
      'Tamper-evident live camera session on site to enforce freshness; unified digital intake for vendor PDFs and challans.',
  },
  {
    activity: 'Extracting document details',
    traditional:
      'Manual line-by-line typing into accounting software; vulnerable to transcription oversights and overlooked items.',
    auditforge:
      'OCR document intelligence extracts line items, quantities, and vendor details with source bounding-box provenance.',
  },
  {
    activity: 'Comparing material quantities',
    traditional:
      'Ad-hoc spreadsheet formulas comparing purchase orders and invoice claims; purchased often equated with consumed.',
    auditforge:
      'Deterministic decimal reconciliation ledger comparing PO, challan, store issue, and recorded consumption.',
  },
  {
    activity: 'Tracing discrepancies to evidence',
    traditional:
      'Chasing paper challans and cross-checking conflicting notes; difficult to establish physical delivery vs. billing claims.',
    auditforge:
      'Direct bidirectional links between calculated variances, invoice line items, and weighbridge gate tickets.',
  },
  {
    activity: 'Recording auditor decisions',
    traditional:
      'Manual stamp on paper voucher or untracked email approval; absence of an auditable clearance log.',
    auditforge:
      'Authorized human signoff workflow recording rationale, reviewed evidence, and timestamped decision history.',
  },
];

export function ComparisonSection() {
  return (
    <section
      id="comparison"
      aria-label="Manual Workflow vs AuditForge Assisted Workflow Comparison"
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
            <span>OPERATIONAL METHODOLOGY</span>
          </div>

          <h2 className="font-serif text-4xl sm:text-5xl lg:text-5.5xl font-normal tracking-tight text-white leading-[1.05]">
            Engineered for <span className="italic text-emerald-400 font-serif">accountability</span> at scale.
          </h2>

          <p className="text-base sm:text-lg text-[#888888] leading-relaxed max-w-2xl font-sans">
            A clear comparison of traditional construction audit workflows versus the
            evidence-linked AuditForge system.
          </p>
        </div>

        {/* ---------------- COMPARISON TABLE ---------------- */}
        <div className="rounded-2xl border border-white/10 bg-white/[0.02] shadow-2xl overflow-hidden font-mono text-xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-white/10 bg-black/70 text-[#888888] text-[11px] uppercase tracking-wider">
                  <th className="py-5 px-6 font-medium w-1/4">Review Activity</th>
                  <th className="py-5 px-6 font-medium w-3/8 text-slate-400">
                    Traditional Manual Workflow
                  </th>
                  <th className="py-5 px-6 font-medium w-3/8 text-emerald-400">
                    AuditForge-Assisted Workflow
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 font-sans">
                {COMPARISON_ROWS.map((row, i) => (
                  <tr
                    key={row.activity}
                    className="hover:bg-white/[0.025] transition-colors"
                  >
                    <td className="py-5 px-6 font-mono text-xs font-semibold text-white">
                      {row.activity}
                    </td>
                    <td className="py-5 px-6 text-xs text-[#888888] leading-relaxed">
                      {row.traditional}
                    </td>
                    <td className="py-5 px-6 text-xs text-slate-200 leading-relaxed bg-emerald-500/[0.02]">
                      <div className="flex items-start gap-2">
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                        <span>{row.auditforge}</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-6 text-[11px] text-[#666666] font-mono">
          *Comparison reflects standard architectural auditing methodologies. AuditForge delivers
          decision support without replacing statutory professional engineering signoff.
        </div>
      </div>
    </section>
  );
}
