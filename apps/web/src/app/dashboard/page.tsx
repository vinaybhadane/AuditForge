import React from 'react';
import Link from 'next/link';
import { LayoutDashboard, FolderGit2, AlertTriangle, FileText, CheckCircle2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

export default function DashboardPage() {
  return (
    <div className="flex-1 bg-surface-50 py-8">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 space-y-8">
        {/* Top Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-border">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-brand-950">
                Auditor Workspace
              </h1>
              <Badge variant="default">Phase 01 Scaffolding</Badge>
            </div>
            <p className="text-sm text-text-secondary mt-1">
              Deterministic reconciliation and evidence verification dashboard.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link href="/">
              <Button variant="outline" size="sm">
                ← Back to Landing
              </Button>
            </Link>
          </div>
        </div>

        {/* Informational Banner */}
        <div className="rounded-xl border border-brand-800/20 bg-brand-950 p-6 text-white shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="flex h-2 w-2 rounded-full bg-signal-amber animate-pulse" />
              <p className="text-xs font-semibold uppercase tracking-wider text-signal-amber">
                Project Foundation Phase
              </p>
            </div>
            <p className="text-base font-semibold text-white">
              Data workflows and live project statistics are deferred to subsequent phases.
            </p>
            <p className="text-xs text-slate-300">
              In accordance with <code className="text-signal-amber font-mono">05_UI_UX_SPECIFICATION.md</code>, no fabricated scores or synthetic business metrics are rendered as live data.
            </p>
          </div>
          <Link href="/login">
            <Button variant="secondary" size="sm" className="whitespace-nowrap">
              Review Auth Blueprint
            </Button>
          </Link>
        </div>

        {/* Real Status Cards - Clean empty/state indicators */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-text-secondary">
                Active Projects
              </CardTitle>
              <FolderGit2 className="h-4 w-4 text-brand-700" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-brand-950 tabular-nums">--</div>
              <p className="text-xs text-text-secondary mt-1">No active projects loaded</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-text-secondary">
                Milestones for Review
              </CardTitle>
              <CheckCircle2 className="h-4 w-4 text-signal-teal" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-brand-950 tabular-nums">--</div>
              <p className="text-xs text-text-secondary mt-1">Awaiting Phase 03 setup</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-text-secondary">
                Open Findings
              </CardTitle>
              <AlertTriangle className="h-4 w-4 text-warning-700" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-brand-950 tabular-nums">--</div>
              <p className="text-xs text-text-secondary mt-1">Deterministic checks unrun</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-text-secondary">
                Clearance Certificates
              </CardTitle>
              <FileText className="h-4 w-4 text-brand-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-brand-950 tabular-nums">--</div>
              <p className="text-xs text-text-secondary mt-1">Pending eligibility checks</p>
            </CardContent>
          </Card>
        </div>

        {/* Empty State Container */}
        <Card className="p-12 text-center flex flex-col items-center justify-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-surface-100 text-text-secondary mb-4">
            <LayoutDashboard className="h-6 w-6" />
          </div>
          <h3 className="text-base font-semibold text-text-primary">No Project Loaded</h3>
          <p className="text-sm text-text-secondary max-w-sm mt-1">
            Projects and evidence runs will be populated once Phase 02 (Auth/DB) and Phase 03 (Milestones/BOQ) are implemented.
          </p>
        </Card>
      </div>
    </div>
  );
}
