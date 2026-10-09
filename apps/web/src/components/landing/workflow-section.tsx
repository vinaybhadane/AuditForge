'use client';

import React, { useState } from 'react';
import {
  FolderGit2,
  Camera,
  Hash,
  Eye,
  FileText,
  Calculator,
  AlertTriangle,
  Award,
  CheckCircle2,
  ArrowRight,
  ShieldCheck,
  ChevronRight,
} from 'lucide-react';

interface WorkflowStage {
  id: string;
  stepNumber: string;
  title: string;
  shortDesc: string;
  category: 'FACT' | 'CALC' | 'AI_OBSERVATION' | 'DECISION';
  categoryLabel: string;
  inputs: string;
  deterministicProcess: string;
  auditableOutput: string;
  integrityRule: string;
  icon: React.ComponentType<{ className?: string }>;
}

const WORKFLOW_STAGES: WorkflowStage[] = [
  {
    id: 'stage-1',
    stepNumber: '01',
    title: 'Project Setup',
    shortDesc: 'Geofence datum, milestones, BOQ schedules, and auditor RBAC roles',
    category: 'FACT',
    categoryLabel: 'Authoritative Baseline',
    inputs: 'Project contract, approved BOQ schedule, site boundary coordinates',
    deterministicProcess: 'Initializes tenant isolation, milestone criteria specs, and auditor cryptographic keys',
    auditableOutput: 'Immutable project baseline & acceptance criteria database records',
    integrityRule: 'Baseline parameters cannot be modified without audit trail logging.',
    icon: FolderGit2,
  },
  {
    id: 'stage-2',
    stepNumber: '02',
    title: 'Evidence Collection',
    shortDesc: 'Live camera capture on site; dual upload/scan for vendor documents',
    category: 'FACT',
    categoryLabel: 'Verified Input',
    inputs: 'Live camera video/photo streams from site; digital invoices and weight challans',
    deterministicProcess: 'Enforces live camera session for site progress (pre-existing image uploads disabled to prove presence)',
    auditableOutput: 'Encrypted object in private storage + device capture telemetry',
    integrityRule: 'Physical presence rule: Gallery file uploads rejected for milestone photos.',
    icon: Camera,
  },
  {
    id: 'stage-3',
    stepNumber: '03',
    title: 'Integrity Checks',
    shortDesc: 'Cryptographic SHA-256 baseline hashing and MIME inspection',
    category: 'FACT',
    categoryLabel: 'Tamper Verification',
    inputs: 'Raw binary stream and client metadata payload',
    deterministicProcess: 'Generates immutable SHA-256 hash, validates MIME magic bytes, verifies EXIF consistency',
    auditableOutput: 'Tamper-evident ledger entry with unique UUID and hash fingerprint',
    integrityRule: 'SHA-256 detects tampering relative to known hash; does not establish original authenticity.',
    icon: Hash,
  },
  {
    id: 'stage-4',
    stepNumber: '04',
    title: 'AI-Assisted Verification',
    shortDesc: 'Vision model assessment against defined milestone criteria',
    category: 'AI_OBSERVATION',
    categoryLabel: 'AI Observation (Candidate)',
    inputs: 'Live camera capture frames + milestone acceptance criteria specs',
    deterministicProcess: 'VLM analyzes completion percentage, structural rebar ties, and shuttering status',
    auditableOutput: 'Structured candidate observation with calibrated confidence scores (never an autonomous pass)',
    integrityRule: 'AI confidence is a review signal—raw model outputs cannot issue clearance certificates.',
    icon: Eye,
  },
  {
    id: 'stage-5',
    stepNumber: '05',
    title: 'Document Extraction',
    shortDesc: 'OCR invoice/challan field extraction with source bounding boxes',
    category: 'FACT',
    categoryLabel: 'Extracted Source Fact',
    inputs: 'PDF invoices, goods receipt notes, delivery weight tickets',
    deterministicProcess: 'Extracts line items, vendor names, quantities, unit prices, tax amounts, and source pixel coordinates',
    auditableOutput: 'Normalized invoice line item entities linked to source document bounding boxes',
    integrityRule: 'Every extracted number preserves an interactive bounding box link to the original document.',
    icon: FileText,
  },
  {
    id: 'stage-6',
    stepNumber: '06',
    title: 'Material Reconciliation',
    shortDesc: 'Deterministic decimal ledger comparing PO, challan, and issues',
    category: 'CALC',
    categoryLabel: 'Calculated Variance',
    inputs: 'BOQ baseline, PO line items, delivery challans, store issue notes, recorded consumption',
    deterministicProcess: 'Calculates: Variance = Delivered - (Issued + Retained) using high-precision Decimal arithmetic',
    auditableOutput: 'Versioned material reconciliation run with reproducible variance numbers',
    integrityRule: 'Deterministic math: AI does not override arithmetic. Delivered ≠ Consumed.',
    icon: Calculator,
  },
  {
    id: 'stage-7',
    stepNumber: '07',
    title: 'Anomaly Analysis',
    shortDesc: 'Calibrated review signals flagging variance without presuming fraud',
    category: 'AI_OBSERVATION',
    categoryLabel: 'Review Signal',
    inputs: 'Calculated material variances, visual observation discrepancies, timeline delays',
    deterministicProcess: 'Correlates multi-modal signals to flag statistical anomalies and missing documentation',
    auditableOutput: 'Ranked discrepancy signals and evidence inspection packages for human auditors',
    integrityRule: 'An anomaly is a review signal—it is not proof of fraud or intentional wrongdoing.',
    icon: AlertTriangle,
  },
  {
    id: 'stage-8',
    stepNumber: '08',
    title: 'Human Auditor Decision',
    shortDesc: 'Authorized professional signoff gating milestone clearance certificates',
    category: 'DECISION',
    categoryLabel: 'Human Authority Gate',
    inputs: 'Audit summary, anomaly signals, supporting evidence references, auditor notes',
    deterministicProcess: 'Authorized human auditor evaluates signals and explicitly executes Approve, Reject, or Request Info',
    auditableOutput: 'Cryptographically signed Milestone Clearance Certificate or Discrepancy Notice',
    integrityRule: 'Non-negotiable: Certificates require documented eligibility checks and authorized human signoff.',
    icon: Award,
  },
];

export function WorkflowSection() {
  const [activeStageId, setActiveStageId] = useState<string>('stage-4');

  const activeStage =
    WORKFLOW_STAGES.find((s) => s.id === activeStageId) || WORKFLOW_STAGES[0];

  return (
    <section
      id="workflow"
      aria-label="AuditForge Verification Pipeline Workflow"
      className="py-24 sm:py-32 bg-[#050505] border-b border-white/10 relative overflow-hidden"
    >
      {/* Background Blueprint Grid */}
      <div
        className="absolute inset-0 bg-blueprint-lines opacity-15 pointer-events-none"
        aria-hidden="true"
      />

      <div className="container relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mb-16 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/[0.04] border border-white/10 text-xs font-mono tracking-widest text-[#A3A3A3]">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            <span>THE VERIFICATION PIPELINE</span>
          </div>

          <h2 className="font-serif text-4xl sm:text-5xl lg:text-5.5xl font-normal tracking-tight text-white leading-[1.05]">
            Every finding has a <span className="italic text-emerald-400 font-serif">trail</span>.
          </h2>

          <p className="text-base sm:text-lg text-[#888888] leading-relaxed max-w-2xl font-sans">
            Follow the 8-stage verification pipeline from initial project baseline to authorized
            human auditor signoff.
          </p>
        </div>

        {/* ---------------- DESKTOP HORIZONTAL TIMELINE ---------------- */}
        <div className="hidden lg:grid grid-cols-8 gap-2 p-2 rounded-2xl bg-white/[0.02] border border-white/10 mb-8 font-mono text-xs">
          {WORKFLOW_STAGES.map((stage) => {
            const isSelected = stage.id === activeStageId;
            const IconComponent = stage.icon;
            return (
              <button
                key={stage.id}
                type="button"
                onClick={() => setActiveStageId(stage.id)}
                className={`p-3 rounded-xl flex flex-col items-start text-left transition-all relative ${
                  isSelected
                    ? 'bg-white/[0.08] text-white border border-emerald-500/40 shadow-lg'
                    : 'text-[#888888] hover:text-white hover:bg-white/[0.03] border border-transparent'
                }`}
              >
                <div className="flex items-center justify-between w-full mb-2">
                  <span
                    className={`text-[10px] font-bold ${
                      isSelected ? 'text-emerald-400' : 'text-[#666666]'
                    }`}
                  >
                    {stage.stepNumber}
                  </span>
                  <IconComponent
                    className={`w-3.5 h-3.5 ${
                      isSelected ? 'text-emerald-400' : 'text-[#666666]'
                    }`}
                  />
                </div>
                <span className="text-xs font-medium line-clamp-1 leading-snug">
                  {stage.title}
                </span>
                {isSelected && (
                  <span className="absolute bottom-1 right-2 w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
                )}
              </button>
            );
          })}
        </div>

        {/* ---------------- MOBILE VERTICAL SELECTOR ---------------- */}
        <div className="lg:hidden flex overflow-x-auto gap-2 pb-4 mb-6 font-mono text-xs no-scrollbar">
          {WORKFLOW_STAGES.map((stage) => {
            const isSelected = stage.id === activeStageId;
            return (
              <button
                key={stage.id}
                type="button"
                onClick={() => setActiveStageId(stage.id)}
                className={`flex-shrink-0 px-3.5 py-2 rounded-xl transition-all ${
                  isSelected
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-semibold'
                    : 'bg-white/[0.03] text-[#888888] border border-white/10'
                }`}
              >
                {stage.stepNumber}. {stage.title}
              </button>
            );
          })}
        </div>

        {/* ---------------- ACTIVE STAGE DETAIL CARD ---------------- */}
        <div className="p-6 sm:p-10 rounded-2xl bg-white/[0.025] border border-white/10 shadow-2xl relative overflow-hidden">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-white/10">
            <div className="space-y-2">
              <div className="flex items-center gap-3">
                <span className="font-mono text-xs px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/25">
                  STAGE {activeStage.stepNumber} OF 08
                </span>
                <span className="font-mono text-xs text-[#A3A3A3] px-2.5 py-1 rounded bg-white/[0.04] border border-white/10">
                  {activeStage.categoryLabel}
                </span>
              </div>
              <h3 className="font-serif text-3xl sm:text-4xl font-normal text-white">
                {activeStage.title}
              </h3>
              <p className="text-sm sm:text-base text-[#888888] font-sans max-w-2xl">
                {activeStage.shortDesc}
              </p>
            </div>

            <div className="flex items-center gap-3">
              <button
                type="button"
                disabled={activeStageId === 'stage-1'}
                onClick={() => {
                  const idx = WORKFLOW_STAGES.findIndex((s) => s.id === activeStageId);
                  if (idx > 0) setActiveStageId(WORKFLOW_STAGES[idx - 1].id);
                }}
                className="px-3.5 py-2 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] disabled:opacity-30 border border-white/10 text-xs font-mono text-white transition-colors"
              >
                ← Previous
              </button>
              <button
                type="button"
                disabled={activeStageId === 'stage-8'}
                onClick={() => {
                  const idx = WORKFLOW_STAGES.findIndex((s) => s.id === activeStageId);
                  if (idx < WORKFLOW_STAGES.length - 1)
                    setActiveStageId(WORKFLOW_STAGES[idx + 1].id);
                }}
                className="px-3.5 py-2 rounded-lg bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/40 text-xs font-mono text-emerald-300 transition-colors"
              >
                Next Stage →
              </button>
            </div>
          </div>

          {/* Detailed Input / Execution / Output Pipeline Breakdown */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-8 font-mono text-xs">
            {/* 1. Input Source */}
            <div className="p-4 rounded-xl bg-black/60 border border-white/10 space-y-2">
              <span className="text-[11px] text-emerald-400 block uppercase tracking-wider font-semibold">
                01. Input Stream
              </span>
              <p className="text-xs text-[#EBEBEB] leading-relaxed font-sans">
                {activeStage.inputs}
              </p>
            </div>

            {/* 2. Deterministic Execution */}
            <div className="p-4 rounded-xl bg-black/60 border border-white/10 space-y-2">
              <span className="text-[11px] text-amber-400 block uppercase tracking-wider font-semibold">
                02. Pipeline Execution
              </span>
              <p className="text-xs text-[#EBEBEB] leading-relaxed font-sans">
                {activeStage.deterministicProcess}
              </p>
            </div>

            {/* 3. Auditable Output */}
            <div className="p-4 rounded-xl bg-black/60 border border-white/10 space-y-2">
              <span className="text-[11px] text-teal-400 block uppercase tracking-wider font-semibold">
                03. Auditable Record
              </span>
              <p className="text-xs text-[#EBEBEB] leading-relaxed font-sans">
                {activeStage.auditableOutput}
              </p>
            </div>
          </div>

          {/* Integrity Note Callout */}
          <div className="mt-6 p-4 rounded-xl bg-white/[0.02] border border-white/10 flex items-start gap-3 text-xs text-[#888888] font-mono">
            <ShieldCheck className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
            <span>
              <strong className="text-white">Product Integrity Rule: </strong>
              {activeStage.integrityRule}
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
