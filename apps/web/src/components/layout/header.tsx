'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { ShieldCheck, Menu, X, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-surface-0/95 backdrop-blur supports-[backdrop-filter]:bg-surface-0/80 transition-colors">
      <div className="container mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand Logo & Wordmark */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-950 text-white shadow-sm transition-transform group-hover:scale-105 border border-brand-800">
            <ShieldCheck className="h-5 w-5 text-signal-amber" />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-black tracking-tight text-brand-950 leading-none">
              AuditForge
            </span>
            <span className="text-[10px] font-mono uppercase tracking-wider text-text-secondary mt-0.5">
              Every Claim. Verified.
            </span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav
          aria-label="Main Navigation"
          className="hidden lg:flex items-center gap-6 text-xs font-mono font-medium text-text-secondary"
        >
          <a
            href="/#problem"
            className="hover:text-brand-950 transition-colors py-1"
          >
            01. Problems
          </a>
          <a
            href="/#workflow"
            className="hover:text-brand-950 transition-colors py-1"
          >
            02. Workflow
          </a>
          <a
            href="/#evidence"
            className="hover:text-brand-950 transition-colors py-1"
          >
            03. Evidence
          </a>
          <a
            href="/#reconciliation"
            className="hover:text-brand-950 transition-colors py-1"
          >
            04. Reconciliation
          </a>
          <a
            href="/#review"
            className="hover:text-brand-950 transition-colors py-1"
          >
            05. Human Gate
          </a>
        </nav>

        {/* Right CTA Actions */}
        <div className="hidden sm:flex items-center gap-3">
          <Link
            href="/login"
            className="text-xs font-mono font-medium text-text-secondary hover:text-brand-950 transition-colors px-2 py-1"
          >
            Sign In
          </Link>
          <Link href="/dashboard">
            <Button size="sm" variant="primary" className="gap-1.5 font-mono text-xs shadow-sm">
              <span>Open Workspace</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Button>
          </Link>
        </div>

        {/* Mobile Hamburger Toggle Button */}
        <button
          type="button"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-expanded={mobileMenuOpen}
          aria-label="Toggle navigation menu"
          className="lg:hidden p-2 rounded-lg text-text-secondary hover:text-brand-950 hover:bg-surface-100 transition-colors border border-border"
        >
          {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-b border-border bg-surface-0 px-4 pt-2 pb-6 space-y-4 shadow-xl font-mono text-xs">
          <div className="flex flex-col space-y-3 pt-2">
            <a
              href="/#problem"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 rounded-md hover:bg-surface-100 text-text-primary font-medium"
            >
              01. Problems & Failure Modes
            </a>
            <a
              href="/#workflow"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 rounded-md hover:bg-surface-100 text-text-primary font-medium"
            >
              02. 7-Stage Workflow
            </a>
            <a
              href="/#evidence"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 rounded-md hover:bg-surface-100 text-text-primary font-medium"
            >
              03. Evidence Intelligence
            </a>
            <a
              href="/#reconciliation"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 rounded-md hover:bg-surface-100 text-text-primary font-medium"
            >
              04. Material Reconciliation
            </a>
            <a
              href="/#review"
              onClick={() => setMobileMenuOpen(false)}
              className="px-3 py-2 rounded-md hover:bg-surface-100 text-text-primary font-medium"
            >
              05. Human Authority
            </a>
          </div>

          <div className="pt-3 border-t border-border flex flex-col gap-2">
            <Link
              href="/login"
              onClick={() => setMobileMenuOpen(false)}
              className="text-center py-2.5 rounded-lg border border-border text-text-primary hover:bg-surface-100 font-medium"
            >
              Sign In to Organization
            </Link>
            <Link
              href="/dashboard"
              onClick={() => setMobileMenuOpen(false)}
              className="text-center py-2.5 rounded-lg bg-brand-950 text-white font-bold hover:bg-brand-800"
            >
              Enter Dashboard
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
