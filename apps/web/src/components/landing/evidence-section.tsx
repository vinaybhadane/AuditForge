'use client';

import React, { useState } from 'react';
import {
  Camera,
  FileSpreadsheet,
  FileCheck,
  Receipt,
  AlertTriangle,
  ArrowRight,
  ShieldCheck,
  ExternalLink,
  CheckCircle,
} from 'lucide-react';
import { Badge } from '@/components/ui/badge';

interface EvidenceNode {
  id: string;
  name: string;
  type: string;
  icon: React.ComponentType<{ className?: string }>;
  tag: string;
  refCode: string;
  timestamp: string;
  sha256: string;
  summary: string;
  extractedValues: Record<string, string>;
  connectionTo: string;
}

const NODES: EvidenceNode[] = [
  {
    id: 'site-photo',
    name: 'Live Camera Capture',
    type: 'Hardware Evidence',
    icon: Camera,
    tag: 'Live Capture Stream',
    refCode: 'EVID-SITE-204',
    timestamp: '2026-10-09 10:45:12 UTC',
    sha256: 'a4b89c72e1...892e31',
    summary:
      'Live in-app camera capture of Level 2 columns along grid C1-D3. File-picker upload blocked.',
    extractedValues: {
      'Capture Modality': 'Live Camera (Rear Facing)',
      'Site Coordinates': '19.0760° N, 72.8777° E (±12m)',
      'Linked Milestone': 'M-02 (Structural Columns)',
      'VLM Observation': 'Cured concrete columns visible; vertical plumb confirmed',
    },
    connectionTo: 'Links visual curing progress directly to milestone criteria M-02',
  },
  {
    id: 'purchase-order',
    name: 'Purchase Order',
    type: 'Commercial Document',
    icon: FileSpreadsheet,
    tag: 'ERP Contract',
    refCode: 'PO-2026-881',
    timestamp: '2026-09-28 09:15:00 UTC',
    sha256: '992a831e5...c771b0',
    summary:
      'Authoritative contract ordering 1,500 bags of OPC 53 Grade Cement for structural columns.',
    extractedValues: {
      'Vendor Name': 'ACC Concrete Ltd.',
      'Material Code': 'MAT-CEM-OPC53',
      'Ordered Quantity': '1,500 Bags (75.00 Tonnes)',
      'Agreed Unit Price': '₹380.00 / Bag (excl. GST)',
    },
    connectionTo: 'Defines the contractual baseline quantity and agreed commercial pricing',
  },
  {
    id: 'delivery-challan',
    name: 'Delivery Challan',
    type: 'Logistics Document',
    icon: Receipt,
    tag: 'Gate Ingestion',
    refCode: 'DC-9941',
    timestamp: '2026-10-04 14:20:33 UTC',
    sha256: '381ef0921...aa5412',
    summary:
      'Transporter physical challan scanned on arrival at security checkpoint.',
    extractedValues: {
      'Vehicle Number': 'MH-04-AZ-8819',
      'Despatched Quantity': '1,480 Bags (74.00 Tonnes)',
      'Transporter Ref': 'BLR-LOGISTICS-41',
      'Ingestion Mode': 'Dual Camera Scanner Scan',
    },
    connectionTo: 'Records physical departure quantity from vendor manufacturing plant',
  },
  {
    id: 'goods-receipt',
    name: 'Goods Receipt Note',
    type: 'Warehouse Ledger',
    icon: FileCheck,
    tag: 'Physical Acceptance',
    refCode: 'GRV-401',
    timestamp: '2026-10-04 16:10:00 UTC',
    sha256: 'e891bca77...448102',
    summary:
      'Store In-Charge tally inspection verifying physical cement count received in storage.',
    extractedValues: {
      'Accepted Quantity': '1,480 Bags',
      'Rejected / Damaged': '0 Bags',
      'Storage Location': 'Warehouse Bay 02',
      'Verified Inspector': 'R. K. Sharma (Store In-Charge)',
    },
    connectionTo: 'Establishes verified inventory addition into project ledger',
  },
  {
    id: 'anomaly-finding',
    name: 'Calculated Finding',
    type: 'Audit Discrepancy',
    icon: AlertTriangle,
    tag: 'Rule AN-004 Signal',
    refCode: 'ANOM-004-SHORTFALL',
    timestamp: '2026-10-04 16:15:22 UTC',
    sha256: 'Derived Deterministic Rule',
    summary:
      'Automated reconciliation flags a 20-bag difference between PO commitment and received deliveries.',
    extractedValues: {
      'Rule ID': 'REC-002 / AN-004 (Delivery Variance)',
      'Ordered PO Qty': '1,500 Bags',
      'Physical Receipt Qty': '1,480 Bags',
      'Calculated Variance': '-20 Bags (Shortfall ₹7,600)',
      'Finding Status': 'Open Investigation — Action: Require Credit Note',
    },
    connectionTo: 'Prevents invoice over-billing by blocking clearance without vendor credit note',
  },
];

export function EvidenceSection() {
  const [activeNodeId, setActiveNodeId] = useState<string>('anomaly-finding');
  const activeNode = NODES.find((n) => n.id === activeNodeId) || NODES[0];
  const ActiveIcon = activeNode.icon;

  return (
    <section
      id="evidence"
      aria-label="Evidence Intelligence and Traceability"
      className="py-20 bg-surface-0 border-b border-border relative overflow-hidden"
    >
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-100 border border-border text-xs font-mono font-medium text-brand-700">
            <span>MULTI-MODAL EVIDENCE GRAPH</span>
          </div>

          <h2 className="text-3xl sm:text-4xl font-extrabold text-brand-950 tracking-tight">
            Every finding leads back to its evidence.
          </h2>

          <p className="text-base sm:text-lg text-text-secondary leading-relaxed">
            AuditForge weaves disjointed site artifacts into an immutable graph of verifiable facts.
            Select any node below to trace its cryptographic provenance and ledger impact.
          </p>
        </div>

        {/* Connected Node Graph Visualizer */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left: Interactive Node Selector Chain */}
          <div className="lg:col-span-5 space-y-3">
            <span className="text-xs font-mono uppercase tracking-wider text-text-secondary block font-semibold mb-2">
              Traceable Supply Chain & Milestone Nodes
            </span>

            {NODES.map((node, index) => {
              const Icon = node.icon;
              const isSelected = activeNodeId === node.id;
              const isFinding = node.id === 'anomaly-finding';

              return (
                <button
                  key={node.id}
                  type="button"
                  onClick={() => setActiveNodeId(node.id)}
                  aria-pressed={isSelected}
                  className={`w-full p-4 rounded-xl border text-left transition-all flex items-center justify-between group ${
                    isSelected
                      ? isFinding
                        ? 'bg-amber-950 text-white border-amber-800 shadow-md ring-2 ring-signal-amber'
                        : 'bg-brand-950 text-white border-brand-800 shadow-md ring-2 ring-signal-teal'
                      : 'bg-surface-50 text-text-primary border-border hover:border-brand-700/50 hover:bg-surface-100'
                  }`}
                >
                  <div className="flex items-center gap-3.5">
                    <div
                      className={`flex h-10 w-10 items-center justify-center rounded-lg border ${
                        isSelected
                          ? isFinding
                            ? 'bg-amber-900/80 border-amber-700 text-signal-amber'
                            : 'bg-brand-900 border-brand-700 text-signal-teal'
                          : isFinding
                          ? 'bg-amber-50 border-amber-200 text-amber-700'
                          : 'bg-surface-0 border-border text-brand-700'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                    </div>

                    <div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`font-mono text-xs font-bold ${
                            isSelected ? 'text-white' : 'text-brand-950'
                          }`}
                        >
                          {node.name}
                        </span>
                        <span
                          className={`text-[10px] font-mono px-1.5 py-0.5 rounded border ${
                            isSelected
                              ? 'bg-black/30 border-white/20 text-slate-300'
                              : 'bg-surface-0 border-border text-text-secondary'
                          }`}
                        >
                          {node.refCode}
                        </span>
                      </div>
                      <span
                        className={`text-xs block ${
                          isSelected ? 'text-slate-300' : 'text-text-secondary'
                        }`}
                      >
                        {node.tag}
                      </span>
                    </div>
                  </div>

                  <ArrowRight
                    className={`w-4 h-4 transition-transform group-hover:translate-x-1 ${
                      isSelected
                        ? isFinding
                          ? 'text-signal-amber'
                          : 'text-signal-teal'
                        : 'text-text-secondary'
                    }`}
                  />
                </button>
              );
            })}
          </div>

          {/* Right: Active Node Detail & Provenance Inspector */}
          <div className="lg:col-span-7 p-6 sm:p-7 rounded-2xl bg-surface-50 border border-border shadow-md space-y-6">
            {/* Header info */}
            <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-border">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-950 text-signal-amber shadow-sm">
                  <ActiveIcon className="h-6 w-6" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold text-brand-700">
                      {activeNode.refCode}
                    </span>
                    <Badge variant="default">{activeNode.type}</Badge>
                  </div>
                  <h3 className="text-xl font-bold text-brand-950">
                    {activeNode.name}
                  </h3>
                </div>
              </div>

              <div className="text-right font-mono text-[11px] text-text-secondary">
                <span className="block text-text-primary font-semibold">
                  Timestamp: {activeNode.timestamp}
                </span>
                <span className="text-[10px] text-slate-500">
                  SHA-256: {activeNode.sha256}
                </span>
              </div>
            </div>

            {/* Description */}
            <p className="text-sm text-text-secondary leading-relaxed">
              {activeNode.summary}
            </p>

            {/* Structured Extracted Key-Values */}
            <div className="space-y-2">
              <span className="text-xs font-mono uppercase tracking-wider text-text-secondary font-semibold block">
                Extracted Values & Verification Attributes
              </span>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {Object.entries(activeNode.extractedValues).map(([key, val]) => (
                  <div
                    key={key}
                    className="p-3 rounded-lg bg-surface-0 border border-border/80 font-mono text-xs"
                  >
                    <span className="text-[11px] text-text-secondary block">
                      {key}
                    </span>
                    <span className="font-semibold text-text-primary text-xs mt-0.5 block">
                      {val}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Graph Relationship Connection */}
            <div className="p-3.5 rounded-xl bg-blue-50/70 border border-blue-200/90 text-xs text-blue-950 flex items-start gap-2.5">
              <ShieldCheck className="w-4 h-4 text-brand-700 shrink-0 mt-0.5" />
              <div>
                <span className="font-mono font-bold text-brand-800 uppercase tracking-wider text-[11px] block">
                  Provenance Lineage:
                </span>
                <span className="text-brand-900 leading-relaxed font-medium">
                  {activeNode.connectionTo}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
