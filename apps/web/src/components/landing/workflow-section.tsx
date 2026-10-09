'use client';

import React, { useState } from 'react';
import {
  Camera,
  Hash,
  FileText,
  Eye,
  Calculator,
  AlertTriangle,
  Award,
  ChevronRight,
  ShieldCheck,
  CheckCircle2,
} from 'lucide-react';
import { Badge } from '@/components/ui/badge';

interface StepDetail {
  number: string;
  title: string;
  shortDesc: string;
  icon: React.ComponentType<{ className?: string }>;
  tag: string;
  input: string;
  process: string;
  output: string;
  integrityRule: string;
}

const STEPS: StepDetail[] = [
  {
    number: '01',
    title: 'Collect Evidence',
    shortDesc: 'Live camera capture on site; dual upload/scan for documents',
    icon: Camera,
    tag: 'Hardware Ingestion',
    input: 'Live device camera stream (site photos) or PDF/image files (vendor invoices/challans)',
    process: 'Enforces live camera capture for site progress (pre-existing image uploads disabled to prove presence)',
    output: 'Encrypted object in private storage + capture metadata (timestamp, device, location)',
    integrityRule: 'Physical presence rule: Gallery uploads rejected for milestone photos.',
  },
  {
    number: '02',
    title: 'Integrity & Provenance',
    shortDesc: 'Cryptographic hashing and tamper-evident registration',
    icon: Hash,
    tag: 'Cryptographic Seal',
    input: 'Binary file payload and client telemetry payload',
    process: 'Computes immutable SHA-256 checksum; assigns unique UUID; verifies capture time within allowed window',
    output: 'Immutable evidence asset row in PostgreSQL with verified hash and tenant ownership',
    integrityRule: 'SHA-256 detects tampering relative to known hash; does not replace human review.',
  },
  {
    number: '03',
    title: 'Document Extraction',
    shortDesc: 'High-precision OCR and candidate field normalization',
    icon: FileText,
    tag: 'OCR Engine',
    input: 'Invoices, delivery challans, goods receipts, and purchase orders',
    process: 'Extracts line items, vendor names, quantities, unit prices, tax amounts, and source coordinates',
    output: 'Structured Pydantic candidate records with page spans and confidence intervals',
    integrityRule: 'Uncertain financial extractions require human confirmation before ledger calculation.',
  },
  {
    number: '04',
    title: 'Visual Assessment',
    shortDesc: 'Criterion-grounded VLM observations against milestones',
    icon: Eye,
    tag: 'VLM Adapter',
    input: 'Live-captured site photograph + versioned acceptance criteria (e.g. column curing, reinforcement)',
    process: 'Vision-Language Model compares visible features to criteria; flags visible vs obscured elements',
    output: 'Candidate visual observations with explicit uncertainty boundaries',
    integrityRule: 'One photo cannot prove internal structural quality; VLM output is review input only.',
  },
  {
    number: '05',
    title: 'Material Reconciliation',
    shortDesc: 'Deterministic ledger balance across the supply chain',
    icon: Calculator,
    tag: 'Deterministic Math',
    input: 'BOQ baseline version, PO lines, challans, store receipts, and issue vouchers',
    process: 'Executes versioned Decimal formulas: Closing Stock = Opening + Receipts - Issues + Adjustments',
    output: 'Reproducible reconciliation lines with calculated delta, unit conversions, and tolerances',
    integrityRule: 'Ordered ≠ Delivered ≠ Received ≠ Issued ≠ Consumed. Never equate ledger states.',
  },
  {
    number: '06',
    title: 'Anomaly Detection',
    shortDesc: 'Rule-based detectors flagging discrepancies and variances',
    icon: AlertTriangle,
    tag: 'Rule Engine',
    input: 'Material deltas, duplicate hashes, PO balances, and capture telemetry',
    process: 'Evaluates rules AN-001 to AN-011 (e.g. challan vs receipt variance, PO over-billing, GPS skew)',
    output: 'Categorized anomaly findings with severity ratings and explainable calculation traces',
    integrityRule: 'An anomaly is a review signal, not proof of fraud or intentional wrongdoing.',
  },
  {
    number: '07',
    title: 'Human Review & Clearance',
    shortDesc: 'Eligibility gate checks and authorized certificate issuance',
    icon: Award,
    tag: 'Human Gate',
    input: 'Auditor review decision, referenced finding resolutions, criteria snapshot',
    process: 'Verifies eligibility blockers (unresolved critical discrepancies block clearance)',
    output: 'Immutable PDF Clearance Certificate with cryptographic signature and audit trail',
    integrityRule: 'Clearance strictly requires authorized human decision. AI cannot issue certificates.',
  },
];

export function WorkflowSection() {
  const [activeStepIndex, setActiveStepIndex] = useState(0);
  const current = STEPS[activeStepIndex];
  const CurrentIcon = current.icon;

  return (
    <section
      id="workflow"
      aria-label="The AuditForge Workflow"
      className="py-20 bg-surface-50 border-b border-border relative overflow-hidden"
    >
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-100 border border-border text-xs font-mono font-medium text-brand-700">
            <span>DETERMINISTIC LIFECYCLE</span>
          </div>

          <h2 className="text-3xl sm:text-4xl font-extrabold text-brand-950 tracking-tight">
            From scattered evidence to a defensible audit trail.
          </h2>

          <p className="text-base sm:text-lg text-text-secondary leading-relaxed">
            AuditForge replaces opaque claims with a 7-stage deterministic pipeline where
            every physical site capture and commercial invoice is linked, verified, and audited.
          </p>
        </div>

        {/* 7-Step Interactive Sequence Ribbon */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2.5 mb-10">
          {STEPS.map((step, idx) => {
            const Icon = step.icon;
            const isSelected = activeStepIndex === idx;
            return (
              <button
                key={step.number}
                type="button"
                onClick={() => setActiveStepIndex(idx)}
                aria-pressed={isSelected}
                className={`p-3.5 rounded-xl text-left border transition-all flex flex-col justify-between h-32 ${
                  isSelected
                    ? 'bg-brand-950 text-white border-brand-800 shadow-lg scale-102 ring-2 ring-signal-amber'
                    : 'bg-surface-0 text-text-primary border-border hover:border-brand-700/50 hover:bg-surface-100'
                }`}
              >
                <div className="flex items-center justify-between w-full">
                  <span
                    className={`font-mono text-xs font-bold ${
                      isSelected ? 'text-signal-amber' : 'text-brand-700'
                    }`}
                  >
                    {step.number}
                  </span>
                  <Icon
                    className={`w-4 h-4 ${
                      isSelected ? 'text-signal-amber' : 'text-text-secondary'
                    }`}
                  />
                </div>

                <div className="space-y-0.5">
                  <span className="block text-xs font-bold leading-snug line-clamp-2">
                    {step.title}
                  </span>
                  <span
                    className={`block text-[10px] font-mono ${
                      isSelected ? 'text-slate-300' : 'text-text-secondary'
                    }`}
                  >
                    {step.tag}
                  </span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Active Stage Deep-Dive Specification Card */}
        <div className="p-6 sm:p-8 rounded-2xl bg-surface-0 border border-border shadow-md">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Stage Summary */}
            <div className="lg:col-span-5 space-y-4">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-950 text-signal-amber shadow-md">
                  <CurrentIcon className="h-6 w-6" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold text-brand-700">
                      STAGE {current.number} OF 07
                    </span>
                    <Badge variant="default">{current.tag}</Badge>
                  </div>
                  <h3 className="text-2xl font-bold text-brand-950">
                    {current.title}
                  </h3>
                </div>
              </div>

              <p className="text-base text-text-secondary leading-relaxed">
                {current.shortDesc}
              </p>

              {/* Product Integrity Rule Box */}
              <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200/90 text-xs text-amber-950 space-y-1">
                <div className="flex items-center gap-1.5 font-bold font-mono text-amber-800 uppercase tracking-wider text-[11px]">
                  <ShieldCheck className="w-4 h-4 text-amber-700" />
                  Product Integrity Guardrail:
                </div>
                <p className="leading-relaxed text-amber-900 font-medium">
                  {current.integrityRule}
                </p>
              </div>
            </div>

            {/* Technical I/O Pipeline Breakdown */}
            <div className="lg:col-span-7 grid grid-cols-1 gap-4 font-mono text-xs">
              {/* Input */}
              <div className="p-4 rounded-xl bg-surface-50 border border-border space-y-1">
                <span className="text-[11px] font-bold text-brand-700 uppercase tracking-wider block">
                  Input Stream / Ingestion:
                </span>
                <p className="text-text-primary font-sans text-xs sm:text-sm">
                  {current.input}
                </p>
              </div>

              {/* Processing */}
              <div className="p-4 rounded-xl bg-surface-50 border border-border space-y-1">
                <span className="text-[11px] font-bold text-signal-teal uppercase tracking-wider block">
                  Engine Execution / Transformation:
                </span>
                <p className="text-text-primary font-sans text-xs sm:text-sm">
                  {current.process}
                </p>
              </div>

              {/* Output */}
              <div className="p-4 rounded-xl bg-surface-50 border border-border space-y-1">
                <span className="text-[11px] font-bold text-brand-950 uppercase tracking-wider block">
                  Output & Authoritative Persistence:
                </span>
                <p className="text-text-primary font-sans text-xs sm:text-sm">
                  {current.output}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
