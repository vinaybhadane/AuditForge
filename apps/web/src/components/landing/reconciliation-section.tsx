'use client';

import React, { useState } from 'react';
import {
  Scale,
  CheckCircle2,
  AlertTriangle,
  FileQuestion,
  HelpCircle,
  ArrowRight,
  Info,
} from 'lucide-react';

interface MaterialAuditRow {
  id: string;
  material: string;
  code: string;
  unit: string;
  ordered: string;
  delivered: string;
  issued: string;
  recordedReturn: string;
  calculatedVariance: string;
  status: 'reconciled' | 'review' | 'missing';
  statusLabel: string;
  sourceRefs: string;
  varianceNote: string;
}

const SAMPLE_RECONCILIATION_DATA: MaterialAuditRow[] = [
  {
    id: 'row-1',
    material: 'TMT Structural Steel Fe500D (16mm)',
    code: 'MAT-STL-16',
    unit: 'Metric Tonnes',
    ordered: '120.00',
    delivered: '120.00',
    issued: '118.50',
    recordedReturn: '0.00',
    calculatedVariance: '+1.50 MT',
    status: 'review',
    statusLabel: 'Requires Review',
    sourceRefs: 'PO-9918 · CH-4402 · SLIP-841',
    varianceNote: 'Delivery ticket matches 120 MT, but site intake weightbridge recorded 118.50 MT. Unloading variance under investigation.',
  },
  {
    id: 'row-2',
    material: 'Ready-Mix Concrete Grade M35',
    code: 'MAT-RMC-35',
    unit: 'Cubic Meters (m³)',
    ordered: '450.00',
    delivered: '450.00',
    issued: '448.00',
    recordedReturn: '2.00',
    calculatedVariance: '0.00 m³',
    status: 'reconciled',
    statusLabel: 'Reconciled',
    sourceRefs: 'PO-9870 · CH-4389 · CUBE-104',
    varianceNote: '10 transit mixer challans match batching slips. Cube testing reports within structural tolerance.',
  },
  {
    id: 'row-3',
    material: 'OPC 53 Grade Cement (50kg Bags)',
    code: 'MAT-CEM-53',
    unit: 'Bags',
    ordered: '1,200',
    delivered: '1,150',
    issued: '1,100',
    recordedReturn: '0',
    calculatedVariance: '-50 Bags',
    status: 'review',
    statusLabel: 'Requires Review',
    sourceRefs: 'PO-9821 · CH-4301 · STORE-89',
    varianceNote: 'Shortfall anomaly detected: Challan #4301 notes 1,200 bags, warehouse tally signed for 1,150 bags.',
  },
  {
    id: 'row-4',
    material: 'High-Density Precast Drainage Pipes',
    code: 'MAT-PIP-600',
    unit: 'Units (R.M.)',
    ordered: '340.00',
    delivered: '340.00',
    issued: '340.00',
    recordedReturn: '0.00',
    calculatedVariance: '0.00 R.M.',
    status: 'reconciled',
    statusLabel: 'Reconciled',
    sourceRefs: 'PO-9799 · CH-4290 · EVID-PIPE',
    varianceNote: 'Delivered and installed on foundation drainage grid. Physical live capture verified by vision model.',
  },
  {
    id: 'row-5',
    material: 'Post-Tensioning High-Tensile Strands',
    code: 'MAT-PTS-12',
    unit: 'Coils',
    ordered: '25.00',
    delivered: '25.00',
    issued: '20.00',
    recordedReturn: '0.00',
    calculatedVariance: '-5.00 Coils',
    status: 'missing',
    statusLabel: 'Supporting Record Missing',
    sourceRefs: 'PO-9750 · [CHALLAN MISSING]',
    varianceNote: 'Vendor invoice submitted for payment, but gate delivery receipt ticket is missing from evidence register.',
  },
];

export function ReconciliationSection() {
  const [selectedRowId, setSelectedRowId] = useState<string>('row-3');

  const selectedRow =
    SAMPLE_RECONCILIATION_DATA.find((r) => r.id === selectedRowId) ||
    SAMPLE_RECONCILIATION_DATA[0];

  return (
    <section
      id="reconciliation"
      aria-label="Material Reconciliation Live Demonstration"
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
            <span>MATERIAL INTELLIGENCE / LIVE DEMONSTRATION</span>
          </div>

          <h2 className="font-serif text-4xl sm:text-5xl lg:text-5.5xl font-normal tracking-tight text-white leading-[1.05]">
            Follow the material.{' '}
            <span className="italic text-emerald-400 font-serif">Find the discrepancy</span>.
          </h2>

          <p className="text-base sm:text-lg text-[#888888] leading-relaxed max-w-2xl font-sans">
            Compare quantities across records and trace each variance to its supporting
            documentation. Decimal arithmetic is deterministic and reproducible.
          </p>
        </div>

        {/* Status Legend */}
        <div className="flex flex-wrap items-center gap-6 mb-6 text-xs font-mono">
          <div className="flex items-center gap-2 text-emerald-400">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            <span>Reconciled</span>
          </div>
          <div className="flex items-center gap-2 text-amber-400">
            <span className="w-2 h-2 rounded-full bg-amber-400" />
            <span>Requires Review</span>
          </div>
          <div className="flex items-center gap-2 text-rose-400">
            <span className="w-2 h-2 rounded-full bg-rose-400" />
            <span>Supporting Record Missing</span>
          </div>
        </div>

        {/* ---------------- DATA VISUALIZATION TABLE ---------------- */}
        <div className="rounded-2xl border border-white/10 bg-white/[0.02] shadow-2xl overflow-hidden mb-8">
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs border-collapse">
              <thead>
                <tr className="border-b border-white/10 bg-black/60 text-[#888888] uppercase tracking-wider text-[11px]">
                  <th className="py-4 px-5 font-medium">Material & Code</th>
                  <th className="py-4 px-4 font-medium text-right">Ordered</th>
                  <th className="py-4 px-4 font-medium text-right">Delivered</th>
                  <th className="py-4 px-4 font-medium text-right">Issued</th>
                  <th className="py-4 px-4 font-medium text-right">Return</th>
                  <th className="py-4 px-4 font-medium text-right">Calculated Variance</th>
                  <th className="py-4 px-5 font-medium text-center">Review Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {SAMPLE_RECONCILIATION_DATA.map((row) => {
                  const isSelected = row.id === selectedRowId;
                  return (
                    <tr
                      key={row.id}
                      onClick={() => setSelectedRowId(row.id)}
                      className={`cursor-pointer transition-colors ${
                        isSelected
                          ? 'bg-white/[0.06] border-l-2 border-l-emerald-400'
                          : 'hover:bg-white/[0.025]'
                      }`}
                    >
                      <td className="py-4 px-5">
                        <div className="font-semibold text-white">{row.material}</div>
                        <div className="text-[10px] text-[#888888]">{row.code} ({row.unit})</div>
                      </td>
                      <td className="py-4 px-4 text-right text-slate-300 tabular-nums">
                        {row.ordered}
                      </td>
                      <td className="py-4 px-4 text-right text-slate-300 tabular-nums">
                        {row.delivered}
                      </td>
                      <td className="py-4 px-4 text-right text-slate-300 tabular-nums">
                        {row.issued}
                      </td>
                      <td className="py-4 px-4 text-right text-slate-300 tabular-nums">
                        {row.recordedReturn}
                      </td>
                      <td className="py-4 px-4 text-right font-bold tabular-nums">
                        <span
                          className={
                            row.calculatedVariance === '0.00 m³' ||
                            row.calculatedVariance === '0.00 R.M.'
                              ? 'text-emerald-400'
                              : 'text-amber-400'
                          }
                        >
                          {row.calculatedVariance}
                        </span>
                      </td>
                      <td className="py-4 px-5 text-center">
                        {row.status === 'reconciled' && (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[11px]">
                            <CheckCircle2 className="w-3 h-3" />
                            {row.statusLabel}
                          </span>
                        )}
                        {row.status === 'review' && (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/30 text-[11px]">
                            <AlertTriangle className="w-3 h-3" />
                            {row.statusLabel}
                          </span>
                        )}
                        {row.status === 'missing' && (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/30 text-[11px]">
                            <FileQuestion className="w-3 h-3" />
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
        </div>

        {/* ---------------- INSPECTABLE FORMULA & SOURCE PROVENANCE ---------------- */}
        <div className="p-6 rounded-2xl bg-white/[0.025] border border-white/10 font-mono text-xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-white/10">
            <div className="flex items-center gap-2 text-emerald-400">
              <Scale className="w-4 h-4" />
              <span className="font-bold">PROVENANCE INSPECTION: {selectedRow.material}</span>
            </div>
            <div className="text-[11px] text-[#A3A3A3]">
              AUDIT TRAIL: {selectedRow.sourceRefs}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-sans">
            <div>
              <span className="text-[#888888] font-mono text-[11px] block uppercase mb-1">
                Auditor Variance Explanation
              </span>
              <p className="text-white leading-relaxed">{selectedRow.varianceNote}</p>
            </div>
            <div>
              <span className="text-[#888888] font-mono text-[11px] block uppercase mb-1">
                Deterministic Calculation Formula
              </span>
              <p className="text-emerald-300 font-mono text-[11px] bg-black/60 p-2.5 rounded-lg border border-white/10">
                Variance = Delivered ({selectedRow.delivered}) - [Issued ({selectedRow.issued}) + Returned ({selectedRow.recordedReturn})]
              </p>
            </div>
          </div>

          <div className="text-[10px] text-[#666666] pt-1 border-t border-white/5 flex items-center justify-between font-mono">
            <span>*Illustrative demonstration fixture. Calculations use high-precision Python Decimal & Postgres NUMERIC.</span>
            <span>A calculated variance is an audit signal, not proof of fraud.</span>
          </div>
        </div>
      </div>
    </section>
  );
}
