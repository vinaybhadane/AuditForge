'use client';

import React from 'react';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import {
  ArrowRight,
  Shield,
  Scale,
  UserCheck,
  ChevronDown,
  Camera,
  Layers,
  Sparkles,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ScenePlaceholder } from './scene-placeholder';

// Public '/' is the ONLY place where Three.js / R3F is dynamically loaded.
// Never import this into dashboard, auth, or shared layouts.
const DynamicConstructionScene = dynamic(
  () =>
    import('./construction-scene').then((mod) => mod.ConstructionScene),
  {
    ssr: false,
    loading: () => <ScenePlaceholder />,
  }
);

export function HeroSection() {
  return (
    <section
      id="hero"
      aria-label="Hero Introduction and Interactive 3D Model"
      className="relative overflow-hidden bg-gradient-to-b from-surface-0 via-surface-50 to-surface-100 border-b border-border py-12 lg:py-16"
    >
      {/* Background Architectural Grid Lines */}
      <div
        className="absolute inset-0 bg-blueprint-lines pointer-events-none opacity-40"
        aria-hidden="true"
      />

      <div className="container relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Top Technical Datum Bar */}
        <div className="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-border/80 text-xs font-mono text-text-secondary">
          <div className="flex items-center gap-2">
            <span className="inline-block w-2 h-2 rounded-full bg-signal-teal animate-pulse" />
            <span className="font-semibold text-text-primary">
              PLATFORM STATUS: OPERATIONAL
            </span>
            <span className="text-border">|</span>
            <span>SPEC: RFC-08/11 DETERMINISTIC ENGINE</span>
          </div>
          <div className="hidden sm:flex items-center gap-4 text-[11px]">
            <span>COORDINATES: LAT 19.0760° N, LON 72.8777° E</span>
            <span className="text-border">|</span>
            <span>DATUM: WGS84 ELEVATION +14.2M</span>
          </div>
        </div>

        {/* Split Grid: Left Copy & CTAs, Right 3D Model */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-8 items-center">
          {/* Left Column: Copy & Conversion */}
          <div className="lg:col-span-5 space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-100 border border-border text-xs font-mono font-medium text-brand-700">
              <span className="flex h-1.5 w-1.5 rounded-full bg-signal-amber" />
              AI-POWERED CONSTRUCTION AUDITING
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-5.5xl font-black tracking-tight text-brand-950 leading-[1.08]">
              Every Claim.{' '}
              <span className="text-brand-700 block">
                Verified by Evidence.
              </span>
            </h1>

            <p className="text-base sm:text-lg text-text-secondary leading-relaxed">
              Verify construction progress, reconcile material records, and uncover
              discrepancies with evidence-linked AI auditing. Designed for project owners,
              auditors, and financial institutions.
            </p>

            {/* CTAs */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <Link href="/dashboard">
                <Button size="lg" variant="primary" className="gap-2 shadow-lg shadow-brand-950/10">
                  Explore AuditForge
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <a href="#workflow">
                <Button size="lg" variant="outline" className="gap-2">
                  See How It Works
                  <ChevronDown className="h-4 w-4 text-text-secondary" />
                </Button>
              </a>
            </div>

            {/* Evidence-First Trust Strip */}
            <div className="pt-6 border-t border-border/80">
              <p className="text-xs font-mono uppercase tracking-wider text-text-secondary mb-3 font-semibold">
                Guaranteed Audit Standards
              </p>
              <div className="grid grid-cols-3 gap-3 text-xs text-text-secondary">
                <div className="flex flex-col gap-1 p-2.5 rounded-lg bg-surface-0 border border-border/70 shadow-2xs">
                  <div className="flex items-center gap-1.5 text-text-primary font-semibold">
                    <Shield className="w-3.5 h-3.5 text-signal-teal" />
                    <span>Evidence-First</span>
                  </div>
                  <span className="text-[11px] text-text-secondary leading-tight">
                    Tamper-evident live site camera frames
                  </span>
                </div>

                <div className="flex flex-col gap-1 p-2.5 rounded-lg bg-surface-0 border border-border/70 shadow-2xs">
                  <div className="flex items-center gap-1.5 text-text-primary font-semibold">
                    <Scale className="w-3.5 h-3.5 text-signal-amber" />
                    <span>Explainable</span>
                  </div>
                  <span className="text-[11px] text-text-secondary leading-tight">
                    Deterministic reproducible ledger math
                  </span>
                </div>

                <div className="flex flex-col gap-1 p-2.5 rounded-lg bg-surface-0 border border-border/70 shadow-2xs">
                  <div className="flex items-center gap-1.5 text-text-primary font-semibold">
                    <UserCheck className="w-3.5 h-3.5 text-brand-600" />
                    <span>Human Review</span>
                  </div>
                  <span className="text-[11px] text-text-secondary leading-tight">
                    Authoritative signoff gates certificates
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Interactive 3D Model Stage */}
          <div className="lg:col-span-7 w-full">
            <div className="relative">
              {/* Subtle architectural elevation dimension tag */}
              <div className="absolute -top-3 left-4 z-20 px-2 py-0.5 rounded bg-brand-950 text-signal-amber font-mono text-[10px] font-semibold tracking-wider uppercase border border-brand-800 shadow-sm">
                STRUCTURAL ELEVATION // 3D MODEL VIEWER
              </div>

              {/* Dynamic 3D Scene */}
              <DynamicConstructionScene />

              {/* Sub-scene caption */}
              <div className="mt-3 flex items-center justify-between text-xs text-text-secondary font-mono px-1">
                <span>* Drag to orbit building • Scroll to zoom • Select levels to inspect</span>
                <span className="hidden sm:inline">Demo Model: Northstar Block</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
