'use client';

import React from 'react';
import Link from 'next/link';
import { Shield, KeyRound, AlertCircle } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function LoginPage() {
  return (
    <div className="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-8 bg-surface-50">
      <Card className="w-full max-w-md shadow-lg border-border">
        <CardHeader className="text-center space-y-2">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-brand-950 text-signal-amber shadow-sm">
            <Shield className="h-6 w-6" />
          </div>
          <CardTitle className="text-2xl font-bold text-brand-950">
            Sign In to AuditForge
          </CardTitle>
          <CardDescription>
            Enter your organization credentials. Access is verified server-side against project memberships.
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4">
          <div className="rounded-lg border border-amber-200 bg-amber-50 p-3.5 text-xs text-amber-900 flex items-start gap-2.5">
            <AlertCircle className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Phase 01 Foundation Placeholder</p>
              <p className="mt-0.5 text-amber-800">
                Full Supabase Auth session wiring will be integrated in Phase 02 according to{' '}
                <code className="text-amber-950 font-mono">07_SECURITY_AND_ACCESS_CONTROL.md</code>.
              </p>
            </div>
          </div>

          <form onSubmit={(e) => e.preventDefault()} className="space-y-4">
            <div>
              <label
                htmlFor="email"
                className="block text-xs font-semibold uppercase tracking-wider text-text-secondary mb-1.5"
              >
                Work Email
              </label>
              <input
                id="email"
                type="email"
                disabled
                placeholder="auditor@organization.com"
                className="w-full h-10 px-3 rounded-lg border border-border bg-surface-100 text-sm text-text-primary opacity-70 cursor-not-allowed"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-xs font-semibold uppercase tracking-wider text-text-secondary mb-1.5"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                disabled
                placeholder="••••••••••••"
                className="w-full h-10 px-3 rounded-lg border border-border bg-surface-100 text-sm text-text-primary opacity-70 cursor-not-allowed"
              />
            </div>

            <Button
              type="button"
              variant="primary"
              className="w-full gap-2"
              disabled
            >
              <KeyRound className="w-4 h-4" />
              Sign In (Active in Phase 02)
            </Button>
          </form>

          <div className="pt-2 text-center">
            <Link
              href="/dashboard"
              className="text-xs text-brand-700 hover:text-brand-800 underline font-medium"
            >
              Continue to Dashboard Placeholder →
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
