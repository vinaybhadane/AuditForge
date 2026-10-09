'use client';

import React, { useEffect, useState } from 'react';
import { Box, Layers, Eye } from 'lucide-react';

interface ScenePlaceholderProps {
  className?: string;
}

export function ScenePlaceholder({ className = '' }: ScenePlaceholderProps) {
  const [hasWebGL, setHasWebGL] = useState<boolean | null>(null);
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    // Check WebGL availability
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      setHasWebGL(Boolean(gl));
    } catch {
      setHasWebGL(false);
    }

    // Check reduced motion preference
    if (typeof window !== 'undefined' && window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
      setReducedMotion(mediaQuery.matches);
    }
  }, []);

  return (
    <div
      role="region"
      aria-label="Interactive 3D Construction Site Scene Container"
      className={`relative w-full h-full min-h-[420px] rounded-2xl overflow-hidden bg-brand-950 border border-brand-800/60 shadow-2xl flex flex-col items-center justify-center p-8 text-center text-white ${className}`}
    >
      {/* Background Architectural Grid Pattern */}
      <div
        className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, rgba(233, 162, 59, 0.4) 1px, transparent 0), linear-gradient(to right, rgba(255, 255, 255, 0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(255, 255, 255, 0.05) 1px, transparent 1px)`,
          backgroundSize: '24px 24px, 48px 48px, 48px 48px',
        }}
        aria-hidden="true"
      />

      {/* Subtle Glow */}
      <div
        className="absolute w-96 h-96 rounded-full bg-brand-700/20 blur-3xl pointer-events-none"
        aria-hidden="true"
      />

      <div className="relative z-10 max-w-md space-y-4">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-xl bg-brand-800/80 border border-brand-700 text-signal-amber shadow-inner">
          <Layers className="h-7 w-7" />
        </div>

        <div className="space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-brand-900/80 border border-brand-700/60 text-[11px] font-medium text-signal-amber">
            <Box className="w-3.5 h-3.5" />
            <span>3D Experience Architectural Container (Phase 10 Mount)</span>
          </div>

          <h3 className="text-xl font-bold tracking-tight text-white">
            Structural Verification Stage
          </h3>

          <p className="text-sm text-slate-300 leading-relaxed">
            Multi-storey structural framing, tower crane telemetry, and physical inspection viewpoints.
          </p>
        </div>

        <div className="pt-2 flex flex-wrap items-center justify-center gap-3 text-xs text-slate-400">
          <span className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-brand-900/50 border border-brand-800">
            <Eye className="w-3.5 h-3.5 text-signal-teal" />
            WebGL: {hasWebGL === null ? 'Checking...' : hasWebGL ? 'Ready' : 'Fallback Active'}
          </span>
          <span className="px-2.5 py-1 rounded bg-brand-900/50 border border-brand-800">
            Motion: {reducedMotion ? 'Reduced' : 'Standard'}
          </span>
          <span className="px-2.5 py-1 rounded bg-brand-900/50 border border-brand-800">
            Route: Public / Only
          </span>
        </div>
      </div>
    </div>
  );
}
