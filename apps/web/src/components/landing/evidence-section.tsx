'use client';

import React, { useState } from 'react';
import {
  Camera,
  FileText,
  Truck,
  FileSpreadsheet,
  BookOpen,
  AlertTriangle,
  CheckCircle2,
  ExternalLink,
  ShieldCheck,
  Hash,
} from 'lucide-react';

interface EvidenceArtifact {
  id: string;
  name: string;
  category: string;
  identifier: string;
  timestamp: string;
  hash: string;
  description: string;
  keyFields: Record<string, string>;
  icon: React.ComponentType<{ className?: string }>;
}

const EVIDENCE_ARTIFACTS: Record<string, EvidenceArtifact> = {
  photo: {
    id: 'photo',
    name: 'Site Construction Photo',
    category: 'Hardware Capture',
    identifier: 'IMG-SITE-2026-842',
    timestamp: '2026-10-09 10:45:12 UTC',
    hash: 'SHA256: 7f83b1657ff1...a93c4e',
    description: 'Live camera capture session at Level 2 structural column staging. File-picker gallery upload disabled.',
    keyFields: {
      'Capture Modality': 'Live Sensor Only',
      'Geofence': 'Lat 19.0760° N, Lon 72.8777° E',
      'Visual Criteria': 'Level 2 Columns Cured & Stripped',
      'Observation': 'Formwork removed, rebar plumb verified',
    },
    icon: Camera,
  },
  invoice: {
    id: 'invoice',
    name: 'Commercial Tax Invoice',
    category: 'Vendor Billing',
    identifier: 'INV-2026-8821',
    timestamp: '2026-10-07 14:20:00 UTC',
    hash: 'SHA256: 3c91d8e12b70...4f8190',
    description: 'Vendor commercial invoice for 50 Metric Tonnes Fe500D structural steel line items.',
    keyFields: {
      'Vendor': 'Jindal Steel & Power Ltd',
      'Billed Qty': '50.00 MT',
      'Amount': '$48,250.00 USD',
      'PO Reference': 'PO-BLD-0842',
    },
    icon: FileText,
  },
  challan: {
    id: 'challan',
    name: 'Delivery Challan & Weight Slip',
    category: 'Logistics Ticket',
    identifier: 'CH-4091 / SLIP-841',
    timestamp: '2026-10-08 08:30:15 UTC',
    hash: 'SHA256: 8a421b00e319...55c812',
    description: 'Weighbridge gate pass and delivery challan countersigned by site security clerk.',
    keyFields: {
      'Vehicle No': 'MH-04-GP-8841',
      'Gross Weight': '68.20 MT',
      'Tare Weight': '20.60 MT',
      'Net Delivered': '47.60 MT (Variance -2.40 MT)',
    },
    icon: Truck,
  },
  boq: {
    id: 'boq',
    name: 'BOQ Schedule Entry',
    category: 'Contract Baseline',
    identifier: 'BOQ-ITEM-04.22',
    timestamp: '2026-08-15 00:00:00 UTC',
    hash: 'SHA256: 1109bc489e1a...de4931',
    description: 'Approved tender bill of quantities baseline for foundation reinforcement steel.',
    keyFields: {
      'Item Code': 'BOQ-04.22-STL',
      'Tender Scope': '120.00 MT Total',
      'Approved Rate': '$965.00 / MT',
      'Tolerance Window': '±0.50 MT',
    },
    icon: FileSpreadsheet,
  },
  ledger: {
    id: 'ledger',
    name: 'Store Material Ledger',
    category: 'Inventory Record',
    identifier: 'LEDGER-WH-0912',
    timestamp: '2026-10-08 11:10:00 UTC',
    hash: 'SHA256: e8129a03bc44...9081bb',
    description: 'Site warehouse inward issue note documenting material moved to active steel-bending yard.',
    keyFields: {
      'Inward Qty': '47.60 MT Received',
      'Store Issue': '35.00 MT Issued to Subcontractor',
      'Balance On Hand': '12.60 MT Yard Staging',
      'Custodian': 'Warehouse Supv. J. Mehta',
    },
    icon: BookOpen,
  },
  finding: {
    id: 'finding',
    name: 'Audit Discrepancy Signal',
    category: 'Audit Finding',
    identifier: 'FINDING-AF-0921',
    timestamp: '2026-10-09 11:00:00 UTC',
    hash: 'SHA256: 9b9b0081ac33...7710ad',
    description: 'Discrepancy Signal: Invoice billed for 50.00 MT, but physical weighbridge confirmed only 47.60 MT received.',
    keyFields: {
      'Discrepancy': 'Shortfall of 2.40 MT ($2,316.00 unreceived)',
      'Signal Class': 'Commercial / Physical Intake Disparity',
      'Calibrated Confidence': 'High (Deterministic Arithmetic)',
      'Action Required': 'Auditor Hold on Invoice Payment Voucher',
    },
    icon: AlertTriangle,
  },
};

export function EvidenceSection() {
  const [activeArtifactId, setActiveArtifactId] = useState<string>('finding');

  const activeArtifact = EVIDENCE_ARTIFACTS[activeArtifactId];

  return (
    <section
      id="evidence"
      aria-label="Multi-Modal Evidence Intelligence Graph"
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
            <span>EVIDENCE INTELLIGENCE / LINKED GRAPH</span>
          </div>

          <h2 className="font-serif text-4xl sm:text-5xl lg:text-5.5xl font-normal tracking-tight text-white leading-[1.05]">
            An audit finding without evidence is{' '}
            <span className="italic text-emerald-400 font-serif">only a question</span>.
          </h2>

          <p className="text-base sm:text-lg text-[#888888] leading-relaxed max-w-2xl font-sans">
            Connect site photographs, commercial invoices, delivery challans, BOQ baselines,
            and warehouse ledgers to every audit finding.
          </p>
        </div>

        {/* ---------------- 6-NODE CONNECTED EVIDENCE GRID ---------------- */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-8 font-mono text-xs">
          {Object.values(EVIDENCE_ARTIFACTS).map((artifact) => {
            const isSelected = artifact.id === activeArtifactId;
            const IconComponent = artifact.icon;
            const isFinding = artifact.id === 'finding';

            return (
              <button
                key={artifact.id}
                type="button"
                onClick={() => setActiveArtifactId(artifact.id)}
                className={`p-3.5 rounded-xl text-left transition-all flex flex-col justify-between min-h-[110px] relative ${
                  isSelected
                    ? isFinding
                      ? 'bg-rose-500/15 border border-rose-500/50 shadow-lg text-white'
                      : 'bg-emerald-500/15 border border-emerald-500/50 shadow-lg text-white'
                    : 'bg-white/[0.02] border border-white/10 hover:border-white/20 text-[#888888] hover:text-white'
                }`}
              >
                <div className="flex items-center justify-between w-full">
                  <IconComponent
                    className={`w-4 h-4 ${
                      isSelected
                        ? isFinding
                          ? 'text-rose-400'
                          : 'text-emerald-400'
                        : 'text-[#666666]'
                    }`}
                  />
                  <span className="text-[10px] text-[#666666]">
                    {artifact.category}
                  </span>
                </div>

                <div>
                  <span className="text-xs font-semibold block line-clamp-1">
                    {artifact.name}
                  </span>
                  <span className="text-[10px] text-[#888888] block font-mono">
                    {artifact.identifier}
                  </span>
                </div>

                {isSelected && (
                  <span
                    className={`absolute top-2 right-2 w-1.5 h-1.5 rounded-full ${
                      isFinding ? 'bg-rose-400' : 'bg-emerald-400'
                    }`}
                  />
                )}
              </button>
            );
          })}
        </div>

        {/* ---------------- INSPECTION CARD FOR SELECTED EVIDENCE NODE ---------------- */}
        <div className="p-6 sm:p-10 rounded-2xl bg-white/[0.025] border border-white/10 shadow-2xl relative overflow-hidden font-mono text-xs">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
            <div>
              <div className="flex items-center gap-2 mb-1.5">
                <span className="px-2.5 py-0.5 rounded bg-white/5 border border-white/10 text-emerald-400 text-[11px]">
                  {activeArtifact.category.toUpperCase()}
                </span>
                <span className="text-[#888888] text-[11px]">
                  IDENTIFIER: {activeArtifact.identifier}
                </span>
              </div>
              <h3 className="font-serif text-2xl sm:text-3xl font-medium text-white font-sans">
                {activeArtifact.name}
              </h3>
            </div>

            <div className="flex items-center gap-2 text-[11px] text-[#888888]">
              <Hash className="w-3.5 h-3.5 text-emerald-400" />
              <span>{activeArtifact.hash}</span>
            </div>
          </div>

          <p className="text-sm text-[#A3A3A3] font-sans leading-relaxed py-6 border-b border-white/10">
            {activeArtifact.description}
          </p>

          {/* Key Extracted Field Values */}
          <div className="pt-6">
            <span className="text-[11px] uppercase tracking-wider text-[#888888] block mb-4 font-semibold">
              Source-Extracted Data Fields & Metadata
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {Object.entries(activeArtifact.keyFields).map(([label, val]) => (
                <div
                  key={label}
                  className="p-3.5 rounded-xl bg-black/60 border border-white/10 space-y-1"
                >
                  <span className="text-[10px] text-[#888888] block uppercase">
                    {label}
                  </span>
                  <span className="text-xs text-white font-bold block">
                    {val}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-8 pt-4 border-t border-white/5 flex items-center justify-between text-[10px] text-[#666666]">
            <span>*Synthetic demonstration data. Illustrates linked evidence topology.</span>
            <span>All values retain interactive provenance to source binary files.</span>
          </div>
        </div>
      </div>
    </section>
  );
}
