'use client';

import React, { useState, useRef, useEffect, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import type { OrbitControls as OrbitControlsImpl } from 'three-stdlib';
import {
  RotateCcw,
  Layers,
  Sparkles,
  Maximize2,
  Scan,
  Compass,
  CheckCircle2,
  AlertTriangle,
  Eye,
} from 'lucide-react';
import { ConstructionModel, MilestoneId } from './construction-model';
import { ScenePlaceholder } from './scene-placeholder';

interface MilestoneData {
  id: MilestoneId;
  label: string;
  tag: string;
  levelName: string;
  elevation: string;
  criterionCode: string;
  criterionDescription: string;
  evidenceRef: string;
  status: 'observed' | 'verified' | 'warning';
  variance: string;
}

const MILESTONES: Record<MilestoneId, MilestoneData> = {
  'level-1': {
    id: 'level-1',
    label: 'Level 01',
    tag: 'Foundation & Basement',
    levelName: 'Substructure & Ground Slab',
    elevation: '+0.00m to +2.20m',
    criterionCode: 'CRIT-FND-101',
    criterionDescription:
      'Base raft slab poured and cured. Foundation waterproofing inspection signoff attached.',
    evidenceRef: 'EVID-FND-0912',
    status: 'verified',
    variance: '0.0% variance',
  },
  'level-2': {
    id: 'level-2',
    label: 'Level 02',
    tag: 'Columns & Core (Active)',
    levelName: 'Reinforced Columns & Shear Core',
    elevation: '+2.20m to +4.40m',
    criterionCode: 'CRIT-COL-204',
    criterionDescription:
      'Structural columns cured. Vertical plumb line within ±5mm tolerance across grid C1-D3.',
    evidenceRef: 'EVID-LIVE-842',
    status: 'observed',
    variance: 'Inconclusive rebar tie (review needed)',
  },
  'level-3': {
    id: 'level-3',
    label: 'Level 03',
    tag: 'Framing & Steel Deck',
    levelName: 'Primary Beams & Active Decking',
    elevation: '+4.40m to +6.60m',
    criterionCode: 'CRIT-FRM-305',
    criterionDescription:
      'Primary steel beams bolted to shear core. Concrete decking formwork shuttering underway.',
    evidenceRef: 'EVID-STL-4103',
    status: 'warning',
    variance: 'Cement bags delivery shortfall (-20 bags)',
  },
  'level-4': {
    id: 'level-4',
    label: 'Level 04',
    tag: 'Top Deck & Scaffolding',
    levelName: 'Perimeter Scaffolding & Rigging',
    elevation: '+6.60m to +8.80m',
    criterionCode: 'CRIT-SCF-402',
    criterionDescription:
      'Perimeter safety netting installed. Tower crane hoist clearance validated.',
    evidenceRef: 'EVID-CRN-5520',
    status: 'observed',
    variance: 'Inspection scheduled',
  },
};

export function ConstructionScene() {
  const [activeMilestone, setActiveMilestone] = useState<MilestoneId>('level-2');
  const [wireframeMode, setWireframeMode] = useState<boolean>(false);
  const [hasWebGL, setHasWebGL] = useState<boolean | null>(null);
  const controlsRef = useRef<OrbitControlsImpl>(null);

  // Check WebGL support safely
  useEffect(() => {
    try {
      const canvas = document.createElement('canvas');
      const gl =
        canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      setHasWebGL(Boolean(gl));
    } catch {
      setHasWebGL(false);
    }
  }, []);

  const handleResetCamera = () => {
    if (controlsRef.current) {
      controlsRef.current.reset();
    }
  };

  // If WebGL is unavailable, render the accessible high-fidelity fallback
  if (hasWebGL === false) {
    return <ScenePlaceholder />;
  }

  const current = MILESTONES[activeMilestone];

  return (
    <div
      role="region"
      aria-label="Interactive 3D Architectural Construction Model"
      className="relative w-full h-[520px] sm:h-[580px] lg:h-[640px] rounded-2xl overflow-hidden bg-slate-900 border border-slate-700/60 shadow-2xl flex flex-col justify-between"
    >
      {/* Background Architectural Blueprint Grid */}
      <div
        className="absolute inset-0 pointer-events-none opacity-25"
        style={{
          backgroundImage: `
            radial-gradient(circle at 1px 1px, rgba(233, 162, 59, 0.3) 1px, transparent 0),
            linear-gradient(to right, rgba(56, 189, 248, 0.08) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(56, 189, 248, 0.08) 1px, transparent 1px)
          `,
          backgroundSize: '24px 24px, 48px 48px, 48px 48px',
        }}
        aria-hidden="true"
      />

      {/* Radial lighting ambient effect */}
      <div
        className="absolute top-1/4 right-1/4 w-80 h-80 rounded-full bg-brand-600/15 blur-3xl pointer-events-none"
        aria-hidden="true"
      />

      {/* ---------------- 3D CANVAS LAYER ---------------- */}
      <div className="absolute inset-0 cursor-grab active:cursor-grabbing">
        <Canvas
          camera={{ position: [15, 12, 17], fov: 36, near: 0.1, far: 100 }}
          gl={{
            antialias: true,
            alpha: true,
            powerPreference: 'high-performance',
          }}
          dpr={[1, 1.5]}
        >
          {/* Lighting Rig */}
          <ambientLight intensity={0.9} />
          <directionalLight
            position={[12, 22, 14]}
            intensity={1.6}
            color="#FFFBEB"
          />
          <directionalLight
            position={[-12, 8, -10]}
            intensity={0.6}
            color="#93C5FD"
          />
          <pointLight position={[0, 6, 0]} intensity={0.4} color="#E9A23B" />

          <Suspense fallback={null}>
            <ConstructionModel
              activeMilestone={activeMilestone}
              wireframeMode={wireframeMode}
            />
          </Suspense>

          <OrbitControls
            ref={controlsRef}
            makeDefault
            enablePan={false}
            enableDamping
            dampingFactor={0.05}
            minDistance={11}
            maxDistance={32}
            minPolarAngle={Math.PI / 6}
            maxPolarAngle={Math.PI / 2 - 0.06}
          />
        </Canvas>
      </div>

      {/* ---------------- TOP HUD OVERLAY ---------------- */}
      <div className="relative z-10 flex flex-wrap items-center justify-between gap-3 p-4 sm:p-5 pointer-events-none">
        {/* Technical Coordinate & Site Datum Badge */}
        <div className="pointer-events-auto flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-950/85 backdrop-blur-md border border-slate-700/80 shadow-md text-slate-300 text-xs font-mono">
          <Compass className="w-3.5 h-3.5 text-signal-amber animate-spin-slow" />
          <span className="font-semibold text-white">NORTHSTAR TOWER</span>
          <span className="text-slate-500">|</span>
          <span className="text-slate-400">DATUM {current.elevation}</span>
        </div>

        {/* Viewport Control Actions */}
        <div className="pointer-events-auto flex items-center gap-2">
          {/* Wireframe / Blueprint Toggle */}
          <button
            type="button"
            onClick={() => setWireframeMode(!wireframeMode)}
            aria-label="Toggle technical wireframe blueprint mode"
            title="Toggle technical blueprint wireframe"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium font-mono border transition-all shadow-md ${
              wireframeMode
                ? 'bg-blue-600/90 text-white border-blue-400 shadow-blue-500/20'
                : 'bg-slate-950/85 text-slate-300 border-slate-700 hover:text-white hover:border-slate-500'
            }`}
          >
            <Scan className="w-3.5 h-3.5 text-blue-400" />
            <span className="hidden sm:inline">Blueprint Mode</span>
          </button>

          {/* Reset Camera View */}
          <button
            type="button"
            onClick={handleResetCamera}
            aria-label="Reset 3D camera to default isometric framing"
            title="Reset isometric perspective"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-950/85 text-slate-300 border border-slate-700 hover:text-white hover:border-slate-500 text-xs font-medium font-mono transition-all shadow-md"
          >
            <RotateCcw className="w-3.5 h-3.5 text-signal-amber" />
            <span className="hidden sm:inline">Reset View</span>
          </button>
        </div>
      </div>

      {/* ---------------- BOTTOM HUD & INSPECTION CALLOUT ---------------- */}
      <div className="relative z-10 p-4 sm:p-5 space-y-3 pointer-events-none">
        {/* Milestone Selector Tabs */}
        <div className="pointer-events-auto flex flex-wrap items-center gap-1.5 p-1.5 rounded-xl bg-slate-950/90 backdrop-blur-md border border-slate-800 shadow-xl max-w-fit">
          {(Object.keys(MILESTONES) as MilestoneId[]).map((mId) => {
            const m = MILESTONES[mId];
            const isSelected = activeMilestone === mId;
            return (
              <button
                key={mId}
                type="button"
                onClick={() => setActiveMilestone(mId)}
                aria-pressed={isSelected}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  isSelected
                    ? 'bg-signal-amber text-slate-950 font-semibold shadow-md'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/80'
                }`}
              >
                <Layers
                  className={`w-3.5 h-3.5 ${
                    isSelected ? 'text-slate-950' : 'text-slate-400'
                  }`}
                />
                <span>{m.label}</span>
                <span
                  className={`text-[10px] hidden md:inline font-mono ${
                    isSelected ? 'text-slate-800 font-bold' : 'text-slate-400'
                  }`}
                >
                  ({m.tag})
                </span>
              </button>
            );
          })}
        </div>

        {/* Detailed Inspection Criterion Callout Card */}
        <div className="pointer-events-auto max-w-lg p-3.5 sm:p-4 rounded-xl bg-slate-950/90 backdrop-blur-md border border-slate-800 text-left shadow-2xl transition-all">
          <div className="flex items-center justify-between gap-3 mb-2">
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-brand-900/90 text-signal-amber border border-brand-700 text-[11px] font-mono font-medium">
                <Sparkles className="w-3 h-3" />
                {current.criterionCode}
              </span>
              <span className="text-xs font-mono text-slate-300 font-medium">
                REF: {current.evidenceRef}
              </span>
            </div>

            {current.status === 'verified' && (
              <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-400">
                <CheckCircle2 className="w-3.5 h-3.5" />
                Verified
              </span>
            )}
            {current.status === 'observed' && (
              <span className="inline-flex items-center gap-1 text-[11px] font-medium text-signal-amber">
                <Eye className="w-3.5 h-3.5" />
                Review Required
              </span>
            )}
            {current.status === 'warning' && (
              <span className="inline-flex items-center gap-1 text-[11px] font-medium text-rose-400">
                <AlertTriangle className="w-3.5 h-3.5" />
                Discrepancy Signal
              </span>
            )}
          </div>

          <h4 className="text-xs sm:text-sm font-semibold text-white mb-1">
            {current.levelName}
          </h4>

          <p className="text-xs text-slate-300 leading-relaxed">
            {current.criterionDescription}
          </p>

          <div className="mt-2.5 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span>Variance Check: {current.variance}</span>
            <span className="text-slate-400 text-[10px]">
              *Illustrative demo fixture
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
