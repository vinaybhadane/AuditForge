import React from 'react';
import Link from 'next/link';
import { ShieldCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function Header() {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-border bg-surface-0/95 backdrop-blur supports-[backdrop-filter]:bg-surface-0/60">
      <div className="container mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-950 text-white shadow-sm transition-transform group-hover:scale-105">
            <ShieldCheck className="h-5 w-5 text-signal-amber" />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-tight text-brand-950 leading-none">
              AuditForge
            </span>
            <span className="text-[10px] font-medium uppercase tracking-wider text-text-secondary mt-0.5">
              Evidence-First Audit
            </span>
          </div>
        </Link>

        <nav className="flex items-center gap-4 sm:gap-6">
          <Link
            href="/dashboard"
            className="text-sm font-medium text-text-secondary hover:text-text-primary transition-colors"
          >
            Dashboard
          </Link>
          <Link
            href="/login"
            className="text-sm font-medium text-text-secondary hover:text-text-primary transition-colors"
          >
            Sign In
          </Link>
          <Link href="/dashboard">
            <Button size="sm" variant="primary">
              Open Workspace
            </Button>
          </Link>
        </nav>
      </div>
    </header>
  );
}
