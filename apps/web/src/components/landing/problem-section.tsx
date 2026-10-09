'use client';

import React from 'react';
import {
  FileWarning,
  CameraOff,
  History,
  ArrowRight,
  CheckCircle,
  XCircle,
  AlertCircle,
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export function ProblemSection() {
  return (
    <section
      id="problem"
      aria-label="The Construction Audit Problem"
      className="py-20 bg-surface-0 border-b border-border relative overflow-hidden"
    >
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-100 border border-border text-xs font-mono font-medium text-brand-700">
            <span>AUDIT VULNERABILITIES</span>
          </div>

          <h2 className="text-3xl sm:text-4xl font-extrabold text-brand-950 tracking-tight">
            Construction claims need more than a spreadsheet.
          </h2>

          <p className="text-base sm:text-lg text-text-secondary leading-relaxed">
            Traditional construction monitoring relies on sampled site visits, unverified photo
            attachments, and disconnected spreadsheets—leaving millions in material leakage,
            phantom milestone progress, and disputed contractor invoices undetected.
          </p>
        </div>

        {/* 3 Technical Problem Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Card 1: Unverified Progress Claims */}
          <div className="relative group p-6 rounded-2xl bg-surface-50 border border-border hover:border-brand-700/60 transition-all duration-200 shadow-sm flex flex-col justify-between">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-danger-700 bg-red-50 border border-red-200 px-2.5 py-1 rounded">
                  FAILURE MODE 01
                </span>
                <CameraOff className="w-5 h-5 text-danger-700" />
              </div>

              <h3 className="text-xl font-bold text-brand-950">
                Unverified Progress Claims
              </h3>

              <p className="text-sm text-text-secondary leading-relaxed">
                Subcontractors submit milestone clearance requests backed by recycled gallery
                photos or stock imagery. Without real-time camera capture verification, owners pay
                for uncured concrete and uninstalled structural steel.
              </p>

              {/* Technical Schematic Box */}
              <div className="p-3 rounded-lg bg-surface-0 border border-border/80 font-mono text-xs space-y-2">
                <div className="flex items-center justify-between text-danger-700">
                  <span className="flex items-center gap-1.5">
                    <XCircle className="w-3.5 h-3.5" /> Traditional Audit:
                  </span>
                  <span>Recycled Gallery File</span>
                </div>
                <div className="text-[11px] text-text-secondary pl-5">
                  Pre-existing disk upload with stripped EXIF and unverified physical location.
                </div>
                <div className="pt-1.5 border-t border-border flex items-center justify-between text-signal-teal">
                  <span className="flex items-center gap-1.5 font-semibold">
                    <CheckCircle className="w-3.5 h-3.5" /> AuditForge:
                  </span>
                  <span>Live Camera Only</span>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-border/60 text-xs text-brand-700 font-semibold flex items-center gap-1">
              <span>Tamper-evident hardware capture enforced</span>
            </div>
          </div>

          {/* Card 2: Document Reconciliation Gaps */}
          <div className="relative group p-6 rounded-2xl bg-surface-50 border border-border hover:border-brand-700/60 transition-all duration-200 shadow-sm flex flex-col justify-between">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-warning-700 bg-amber-50 border border-amber-200 px-2.5 py-1 rounded">
                  FAILURE MODE 02
                </span>
                <FileWarning className="w-5 h-5 text-warning-700" />
              </div>

              <h3 className="text-xl font-bold text-brand-950">
                Document Reconciliation Gaps
              </h3>

              <p className="text-sm text-text-secondary leading-relaxed">
                Purchase orders, paper delivery challans, and tax invoices arrive with mismatched
                units (tonnes vs bags vs m³), partial shipments, and untracked returns. Ledger
                discrepancies hide in manual comparison errors.
              </p>

              {/* Technical Schematic Box */}
              <div className="p-3 rounded-lg bg-surface-0 border border-border/80 font-mono text-xs space-y-2">
                <div className="flex items-center justify-between text-warning-700">
                  <span className="flex items-center gap-1.5">
                    <AlertCircle className="w-3.5 h-3.5" /> Traditional Audit:
                  </span>
                  <span>Sampled 3-Way Match</span>
                </div>
                <div className="text-[11px] text-text-secondary pl-5">
                  PO: 120T vs Challan: 118.5T vs Invoice: 120T billing undetected.
                </div>
                <div className="pt-1.5 border-t border-border flex items-center justify-between text-signal-teal">
                  <span className="flex items-center gap-1.5 font-semibold">
                    <CheckCircle className="w-3.5 h-3.5" /> AuditForge:
                  </span>
                  <span>Deterministic Decimal Math</span>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-border/60 text-xs text-brand-700 font-semibold flex items-center gap-1">
              <span>Automatic unit normalization & line tolerances</span>
            </div>
          </div>

          {/* Card 3: Untraceable Audit Trails */}
          <div className="relative group p-6 rounded-2xl bg-surface-50 border border-border hover:border-brand-700/60 transition-all duration-200 shadow-sm flex flex-col justify-between">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-brand-700 bg-blue-50 border border-blue-200 px-2.5 py-1 rounded">
                  FAILURE MODE 03
                </span>
                <History className="w-5 h-5 text-brand-700" />
              </div>

              <h3 className="text-xl font-bold text-brand-950">
                Untraceable Audit Trails
              </h3>

              <p className="text-sm text-text-secondary leading-relaxed">
                When cost overruns or structural defects appear months later, paper inspection slips
                and spreadsheet revisions cannot reconstruct who approved what milestone, under
                which criteria version, or backed by what evidence.
              </p>

              {/* Technical Schematic Box */}
              <div className="p-3 rounded-lg bg-surface-0 border border-border/80 font-mono text-xs space-y-2">
                <div className="flex items-center justify-between text-text-secondary">
                  <span className="flex items-center gap-1.5">
                    <XCircle className="w-3.5 h-3.5" /> Traditional Audit:
                  </span>
                  <span>Mutable Spreadsheets</span>
                </div>
                <div className="text-[11px] text-text-secondary pl-5">
                  Overwritten rows, lost original PDFs, and opaque reviewer sign-off history.
                </div>
                <div className="pt-1.5 border-t border-border flex items-center justify-between text-signal-teal">
                  <span className="flex items-center gap-1.5 font-semibold">
                    <CheckCircle className="w-3.5 h-3.5" /> AuditForge:
                  </span>
                  <span>SHA-256 Versioned Snapshots</span>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-border/60 text-xs text-brand-700 font-semibold flex items-center gap-1">
              <span>Immutable clearance certificates & eligibility gates</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
