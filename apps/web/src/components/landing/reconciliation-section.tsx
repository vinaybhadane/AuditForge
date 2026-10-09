'use client';

import React, { useState } from 'react';
import {
  Scale,
  CheckCircle2,
  AlertTriangle,
  Info,
  Calculator,
  Search,
  Filter,
} from 'lucide-react';
import { Badge } from '@/components/ui/badge';

interface ReconciliationRow {
  material: string;
  code: string;
  unit: string;
  ordered: string;
  delivered: string;
  received: string;
  issued: string;
  variance: string;
  tolerance: string;
  status: 'matched' | 'discrepancy' | 'shortfall';
  statusLabel: string;
  explanation: string;
}

const RECONCILIATION_ROWS: ReconciliationRow[] = [
  {
    material: 'TMT Steel 16mm Fe500D',
    code: 'MAT-STL-16',
    unit: 'Tonnes',
    ordered: '120.00',
    delivered: '120.00',
    received: '118.50',
    issued: '110.00',
    variance: '-1.50 T',
    tolerance: '±0.50 T',
    status: 'discrepancy',
    statusLabel: 'Variance Exceeds Tolerance',
    explanation: 'Delivery challan #882 states 120.00T, but weighbridge slip #410 records 118.50T net weight.',
  },
  {
    material: 'Ready-Mix Concrete M30',
    code: 'MAT-RMC-M30',
    unit: 'm³',
    ordered: '450.00',
    delivered: '450.00',
    received: '450.00',
    issued: '442.00',
    variance: '0.00 m³',
    tolerance: '±2.00 m³',
    status: 'matched',
    statusLabel: 'Verified Match',
    explanation: 'Transit mixer batching tickets reconcile exactly with pour log and cube test records.',
  },
  {
    material: 'OPC 53 Grade Cement',
    code: 'MAT-CEM-OPC53',
    unit: 'Bags',
    ordered: '1,500',
    delivered: '1,480',
    received: '1,480',
    issued: '1,420',
    variance: '-20 Bags',
    tolerance: '0 Bags',
    status: 'shortfall',
    statusLabel: 'Delivery Shortage',
    explanation: 'PO committed 1,500 bags; transporter challan and physical store count agree at 1,480 bags.',
  },
  {
    material: 'Structural Timber Formwork',
    code: 'MAT-TMB-PLY12',
    unit: 'm²',
    ordered: '800.00',
    delivered: '800.00',
    received: '800.00',
    issued: '760.00',
    variance: '0.00 m²',
    tolerance: '±5.00 m²',
    status: 'matched',
    statusLabel: 'Verified Match',
    explanation: 'Total surface formwork area matches milestone M-02 column perimeter calculations.',
  },
];

export function ReconciliationSection() {
  const [selectedRow, setSelectedRow] = useState<ReconciliationRow>(RECONCILIATION_ROWS[0]);

  return (
    <section
      id="reconciliation"
      aria-label="Material Reconciliation"
      className="py-20 bg-surface-50 border-b border-border relative overflow-hidden"
    >
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-100 border border-border text-xs font-mono font-medium text-brand-700">
            <span>DETERMINISTIC RECONCILIATION</span>
          </div>

          <h2 className="text-3xl sm:text-4xl font-extrabold text-brand-950 tracking-tight">
            Follow the material. Find the discrepancy.
          </h2>

          <p className="text-base sm:text-lg text-text-secondary leading-relaxed">
            AuditForge compares purchase orders, delivery challans, physical store receipts, and
            approved BOQ allowances using deterministic Decimal math. Never equate ordered with
            delivered, or delivered with consumed.
          </p>
        </div>

        {/* Formula Bar Banner */}
        <div className="p-4 rounded-xl bg-brand-950 text-white mb-8 border border-brand-800 shadow-md">
          <div className="flex flex-wrap items-center justify-between gap-4 font-mono text-xs">
            <div className="flex items-center gap-2">
              <Calculator className="w-4 h-4 text-signal-amber" />
              <span className="text-signal-amber font-bold">CORE LEDGER EQUATION:</span>
              <span className="text-slate-200">
                Closing Stock = Opening Stock + Receipts - Issues + Approved Adjustments
              </span>
            </div>
            <span className="text-slate-400 text-[11px]">
              ENGINE: Python Decimal / PostgreSQL NUMERIC(20,6)
            </span>
          </div>
        </div>

        {/* Interactive Reconciliation Table Card */}
        <div className="rounded-2xl bg-surface-0 border border-border shadow-md overflow-hidden">
          {/* Table Header controls */}
          <div className="p-4 sm:px-6 border-b border-border bg-surface-50 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <Scale className="w-4 h-4 text-brand-700" />
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-brand-950">
                Project Ledger Snapshot // Period: 2026-10-01 to 2026-10-08
              </span>
            </div>
            <div className="flex items-center gap-2 text-xs font-mono text-text-secondary">
              <span className="px-2 py-0.5 rounded bg-surface-100 border border-border">
                Snapshot Hash: c3f8...991a
              </span>
              <span className="px-2 py-0.5 rounded bg-surface-100 border border-border">
                Baseline: v2.1
              </span>
            </div>
          </div>

          {/* Responsive Table Container */}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-border bg-surface-100/60 font-mono text-[11px] text-text-secondary uppercase">
                  <th className="py-3 px-4 font-semibold">Material / Code</th>
                  <th className="py-3 px-4 font-semibold">Unit</th>
                  <th className="py-3 px-4 font-semibold text-right">PO Ordered</th>
                  <th className="py-3 px-4 font-semibold text-right">Challaned</th>
                  <th className="py-3 px-4 font-semibold text-right">Store Received</th>
                  <th className="py-3 px-4 font-semibold text-right">Site Issued</th>
                  <th className="py-3 px-4 font-semibold text-right">Variance</th>
                  <th className="py-3 px-4 font-semibold">Audit Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border font-mono">
                {RECONCILIATION_ROWS.map((row) => {
                  const isSelected = selectedRow.code === row.code;
                  return (
                    <tr
                      key={row.code}
                      onClick={() => setSelectedRow(row)}
                      className={`cursor-pointer transition-colors ${
                        isSelected
                          ? 'bg-amber-50/70'
                          : 'hover:bg-surface-50'
                      }`}
                    >
                      <td className="py-3.5 px-4">
                        <div className="font-sans font-bold text-text-primary text-xs">
                          {row.material}
                        </div>
                        <span className="text-[10px] text-text-secondary">{row.code}</span>
                      </td>
                      <td className="py-3.5 px-4 text-text-secondary">{row.unit}</td>
                      <td className="py-3.5 px-4 text-right tabular-nums">{row.ordered}</td>
                      <td className="py-3.5 px-4 text-right tabular-nums">{row.delivered}</td>
                      <td className="py-3.5 px-4 text-right tabular-nums font-semibold text-text-primary">
                        {row.received}
                      </td>
                      <td className="py-3.5 px-4 text-right tabular-nums">{row.issued}</td>
                      <td
                        className={`py-3.5 px-4 text-right tabular-nums font-bold ${
                          row.status === 'matched'
                            ? 'text-signal-teal'
                            : row.status === 'discrepancy'
                            ? 'text-danger-700'
                            : 'text-warning-700'
                        }`}
                      >
                        {row.variance}
                      </td>
                      <td className="py-3.5 px-4">
                        {row.status === 'matched' && (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-emerald-50 text-success-700 border border-emerald-200 text-[11px] font-medium">
                            <CheckCircle2 className="w-3 h-3" />
                            {row.statusLabel}
                          </span>
                        )}
                        {row.status === 'discrepancy' && (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-red-50 text-danger-700 border border-red-200 text-[11px] font-medium">
                            <AlertTriangle className="w-3 h-3" />
                            {row.statusLabel}
                          </span>
                        )}
                        {row.status === 'shortfall' && (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-amber-50 text-warning-700 border border-amber-200 text-[11px] font-medium">
                            <Info className="w-3 h-3" />
                            {row.statusLabel}
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Selected Row Ledger Inspection Callout */}
          <div className="p-4 sm:p-5 bg-surface-50 border-t border-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
            <div className="flex items-start gap-2.5">
              <Info className="w-4 h-4 text-brand-700 shrink-0 mt-0.5" />
              <div>
                <span className="font-mono font-bold text-brand-950">
                  INSPECTION TRACE ({selectedRow.material}):{' '}
                </span>
                <span className="text-text-secondary">{selectedRow.explanation}</span>
              </div>
            </div>
            <div className="font-mono text-[11px] text-text-secondary shrink-0">
              Tolerance Bound: {selectedRow.tolerance}
            </div>
          </div>
        </div>

        {/* Audit Caveat Footnote */}
        <p className="mt-4 text-center text-xs text-text-secondary font-mono">
          *AuditForge calculates reproducible discrepancies. A variance indicates an anomaly signal
          requiring human investigation, not conclusive proof of theft or fraud.
        </p>
      </div>
    </section>
  );
}
