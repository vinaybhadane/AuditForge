import React from 'react';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import { ArrowRight, CheckCircle2, Shield, FileSpreadsheet, Scale, UserCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';

// Public '/' is the ONLY route where 3D scene container is dynamically imported.
// Never import this into layouts, auth, or dashboard routes.
const ScenePlaceholder = dynamic(
  () =>
    import('@/components/landing/scene-placeholder').then(
      (mod) => mod.ScenePlaceholder
    ),
  {
    ssr: false,
    loading: () => (
      <div className="w-full min-h-[420px] rounded-2xl bg-brand-950 border border-brand-800 animate-pulse flex items-center justify-center text-slate-400 text-sm">
        Loading 3D Visual Verification Stage...
      </div>
    ),
  }
);

export default function HomePage() {
  return (
    <div className="flex flex-col flex-1">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-surface-0 to-surface-50 py-16 sm:py-24 border-b border-border">
        <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Left Content */}
            <div className="lg:col-span-7 space-y-6">
              <div className="flex flex-wrap items-center gap-2">
                <Badge variant="verified">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Deterministic Audit Platform
                </Badge>
                <Badge variant="default">Phase 01 Foundation</Badge>
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-brand-950 leading-[1.1]">
                Every Claim.{' '}
                <span className="text-brand-700 block sm:inline">
                  Verified by Evidence.
                </span>
              </h1>

              <p className="text-lg sm:text-xl text-text-secondary max-w-2xl leading-relaxed">
                AuditForge correlates live-captured site photographs, milestone acceptance criteria,
                vendor invoices, challans, and stock movements through deterministic reconciliation and
                authorized human decisions.
              </p>

              <div className="flex flex-wrap items-center gap-4 pt-2">
                <Link href="/dashboard">
                  <Button size="lg" variant="primary" className="gap-2">
                    Enter Dashboard
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
                <Link href="/login">
                  <Button size="lg" variant="outline">
                    Sign In to Organization
                  </Button>
                </Link>
              </div>

              <div className="pt-4 flex items-center gap-6 text-xs text-text-secondary border-t border-border/80">
                <div className="flex items-center gap-1.5">
                  <Shield className="w-4 h-4 text-signal-teal" />
                  <span>Tenant Isolation</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Scale className="w-4 h-4 text-signal-amber" />
                  <span>Deterministic Math</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <UserCheck className="w-4 h-4 text-brand-600" />
                  <span>Human Authority</span>
                </div>
              </div>
            </div>

            {/* Right: Client-Only 3D Scene Container */}
            <div className="lg:col-span-5 w-full">
              <ScenePlaceholder />
            </div>
          </div>
        </div>
      </section>

      {/* Workflow Strip: Capture -> Verify -> Reconcile -> Review */}
      <section className="py-12 bg-surface-0 border-b border-border">
        <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-10">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-brand-700">
              Auditing Workflow
            </h2>
            <p className="text-2xl font-bold text-brand-950 mt-1">
              From Physical Site Capture to Authorized Clearance
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Card>
              <CardHeader>
                <div className="w-8 h-8 rounded-lg bg-amber-50 text-amber-700 flex items-center justify-center text-xs font-bold mb-1">
                  01
                </div>
                <CardTitle>1. Live Capture</CardTitle>
                <CardDescription>
                  Tamper-evident in-app camera capture for site progress photos, plus dual upload/scan for vendor documents.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <div className="w-8 h-8 rounded-lg bg-blue-50 text-brand-700 flex items-center justify-center text-xs font-bold mb-1">
                  02
                </div>
                <CardTitle>2. Extraction & VLM</CardTitle>
                <CardDescription>
                  OCR document field extraction and criterion-grounded visual observations with visible uncertainty.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-700 flex items-center justify-center text-xs font-bold mb-1">
                  03
                </div>
                <CardTitle>3. Reconciliation</CardTitle>
                <CardDescription>
                  Deterministic comparison of POs, challans, receipts, ledger movements, and BOQ allowances.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <div className="w-8 h-8 rounded-lg bg-slate-100 text-slate-800 flex items-center justify-center text-xs font-bold mb-1">
                  04
                </div>
                <CardTitle>4. Human Decision</CardTitle>
                <CardDescription>
                  Clearance certificates issued only through documented eligibility checks and designated human reviewers.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>
    </div>
  );
}
