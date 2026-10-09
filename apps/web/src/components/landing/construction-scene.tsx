'use client';

import React, { useState, useRef, useEffect, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useProgress, Html } from '@react-three/drei';
import type { OrbitControls as OrbitControlsImpl } from 'three-stdlib';
import {
  RotateCcw,
  Layers,
  Sparkles,
  Scan,
  Compass,
  CheckCircle2,
  AlertTriangle,
  Eye,
  Box,
} from 'lucide-react';
import { ConstructionModel, MilestoneId } from './construction-model';
import { ScenePlaceholder } from './scene-placeholder';

export interface MilestoneData {
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

export const HERO_MILESTONES: Record<MilestoneId, MilestoneData> = {
  'level-1': {
    id: 'level-1',
    label: 'Zone 01',
    tag: 'Precast Substructure',
    levelName: 'Precast Drainage & Concrete Blocks',
    elevation: 'Datum +0.00m to +1.80m',
    criterionCode: 'CRIT-FND-101',
    criterionDescription:
      'Precast concrete pipes and perimeter masonry blocks delivered and staged per site plan.',
    evidenceRef: 'EVID-FND-0912',
    status: 'verified',
    variance: '0.0% variance (verified)',
  },
  'level-2': {
    id: 'level-2',
    label: 'Zone 02',
    tag: 'Cement Intake (Active)',
    levelName: 'Palletized Cement Bags & Delivery Intake',
    elevation: 'Datum +0.00m to +2.40m',
    criterionCode: 'CRIT-MAT-204',
    criterionDescription:
      'Challan match: 50 bags OPC-53 cement palletized. Weight ticket and live camera site capture cross-referenced.',
    evidenceRef: 'EVID-LIVE-842',
    status: 'observed',
    variance: 'Shortfall anomaly (-20 bags signal)',
  },
  'level-3': {
    id: 'level-3',
    label: 'Zone 03',
    tag: 'Pipe Stacks & Dunnage',
    levelName: 'Reinforced Pipe Stacks on Timber Dunnage',
    elevation: 'Datum +0.00m to +3.20m',
    criterionCode: 'CRIT-STK-305',
    criterionDescription:
      'Industrial concrete pipe tier stacked on timber bearers. Stacking protocol checked against safety clearance limits.',
    evidenceRef: 'EVID-PIP-4103',
    status: 'warning',
    variance: 'Stack height within limits; visual inspection noted',
  },
  'level-4': {
    id: 'level-4',
    label: 'Zone 04',
    tag: 'Rigging & Equipment',
    levelName: 'Heavy Cable Reels & Site Rigging Staging',
    elevation: 'Datum +0.00m to +2.10m',
    criterionCode: 'CRIT-TLS-402',
    criterionDescription:
      'Site rigging, timber reel spools, sledgehammers, and verified hand tools cataloged for ongoing foundation pour.',
    evidenceRef: 'EVID-EQP-5520',
    status: 'observed',
    variance: 'Tool manifest logged & verified',
  },
};

/**
 * 3D Model Streaming Progress HUD
 */
function ModelProgressLoader() {
  const { progress, active } = useProgress();
  if (!active && progress === 100) return null;

  return (
    <Html center zIndexRange={[100, 0]}>
      <div className="flex flex-col items-center justify-center p-5 rounded-2xl bg-[#050505]/95 border border-emerald-500/40 shadow-2xl backdrop-blur-xl min-w-[260px] text-center select-none pointer-events-none">
        <div className="relative w-12 h-12 mb-3 flex items-center justify-center">
          <div className="w-12 h-12 rounded-full border-2 border-emerald-500/20 border-t-emerald-400 animate-spin" />
          <span className="absolute text-[11px] font-mono font-bold text-emerald-400">
            {Math.round(progress)}%
          </span>
        </div>
        <p className="text-xs font-semibold text-white tracking-wide">
          Streaming 3D Building Model
        </p>
        <p className="text-[10px] font-mono text-[#888888] mt-0.5">
          GLTF PBR Assets (43 MB)
        </p>
        <div className="w-full bg-white/10 rounded-full h-1.5 mt-3 overflow-hidden">
          <div
            className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full transition-all duration-200"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>
    </Html>
  );
}

interface ConstructionSceneProps {
  activeMilestone?: MilestoneId;
  onMilestoneChange?: (id: MilestoneId) => void;
  wireframeMode?: boolean;
  onWireframeToggle?: () => void;
  showOverlayControls?: boolean;
}

export function ConstructionScene({
  activeMilestone: externalMilestone,
  onMilestoneChange,
  wireframeMode: externalWireframe,
  onWireframeToggle,
  showOverlayControls = true,
}: ConstructionSceneProps) {
  const [internalMilestone, setInternalMilestone] = useState<MilestoneId>('level-2');
  const [internalWireframe, setInternalWireframe] = useState<boolean>(false);
  const [hasWebGL, setHasWebGL] = useState<boolean | null>(null);
  const controlsRef = useRef<OrbitControlsImpl>(null);

  const activeMilestone = externalMilestone ?? internalMilestone;
  const wireframeMode = externalWireframe ?? internalWireframe;

  const setActiveMilestone = (id: MilestoneId) => {
    if (onMilestoneChange) {
      onMilestoneChange(id);
    } else {
      setInternalMilestone(id);
    }
  };

  const toggleWireframe = () => {
    if (onWireframeToggle) {
      onWireframeToggle();
    } else {
      setInternalWireframe((prev) => !prev);
    }
  };

  // Check WebGL availability safely
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

  // If WebGL is unavailable, render fallback
  if (hasWebGL === false) {
    return <ScenePlaceholder />;
  }

  const current = HERO_MILESTONES[activeMilestone];

  return (
    <div
      role="region"
      aria-label="Interactive 3D Architectural Construction Building"
      className="relative w-full h-full overflow-hidden select-none"
    >
      {/* ---------------- 3D CANVAS LAYER ---------------- */}
      <div className="absolute inset-0 cursor-grab active:cursor-grabbing">
        <Canvas
          camera={{ position: [8.0, 5.8, 9.8], fov: 38, near: 0.1, far: 100 }}
          gl={{
            antialias: true,
            alpha: true,
            powerPreference: 'high-performance',
          }}
          dpr={[1, 1.5]}
        >
          {/* Architectural Lighting Rig */}
          <ambientLight intensity={1.5} />
          <hemisphereLight args={['#ffffff', '#0f172a', 1.0]} />
          {/* Key warm directional sunlight */}
          <directionalLight
            position={[14, 20, 16]}
            intensity={2.4}
            color="#FFFBEB"
            castShadow
          />
          {/* Subtle Emerald rim backlight */}
          <directionalLight
            position={[-12, 10, -12]}
            intensity={1.2}
            color="#10B981"
          />
          {/* Cool fill light */}
          <directionalLight
            position={[0, 12, 14]}
            intensity={0.9}
            color="#93C5FD"
          />
          <pointLight position={[3, 5, 2]} intensity={1.8} color="#E9A23B" />

          <Suspense fallback={<ModelProgressLoader />}>
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
            dampingFactor={0.06}
            minDistance={4}
            maxDistance={25}
            minPolarAngle={Math.PI / 8}
            maxPolarAngle={Math.PI / 2 - 0.05}
            target={[1.2, 0.8, 0]}
          />
        </Canvas>
      </div>

      {/* ---------------- FLOATING TECHNICAL CONTROLS HUD ---------------- */}
      {showOverlayControls && (
        <div className="absolute bottom-6 right-6 z-20 flex flex-col items-end gap-3 pointer-events-none">
          {/* Inspection Zone Selector Tabs */}
          <div className="pointer-events-auto flex items-center gap-1 p-1 rounded-xl bg-[#050505]/85 backdrop-blur-md border border-white/10 shadow-2xl">
            {(Object.keys(HERO_MILESTONES) as MilestoneId[]).map((mId) => {
              const m = HERO_MILESTONES[mId];
              const isSelected = activeMilestone === mId;
              return (
                <button
                  key={mId}
                  type="button"
                  onClick={() => setActiveMilestone(mId)}
                  aria-pressed={isSelected}
                  className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-mono transition-all ${
                    isSelected
                      ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-semibold shadow-sm'
                      : 'text-[#888888] hover:text-white hover:bg-white/5 border border-transparent'
                  }`}
                >
                  <span
                    className={`w-1.5 h-1.5 rounded-full ${
                      isSelected ? 'bg-emerald-400' : 'bg-white/30'
                    }`}
                  />
                  <span>{m.label}</span>
                </button>
              );
            })}
          </div>

          {/* Technical Viewport Action Buttons */}
          <div className="pointer-events-auto flex items-center gap-2">
            <button
              type="button"
              onClick={toggleWireframe}
              aria-label="Toggle technical wireframe blueprint mode"
              title="Toggle technical blueprint wireframe"
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono border transition-all shadow-md ${
                wireframeMode
                  ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                  : 'bg-[#050505]/85 text-[#A3A3A3] border-white/10 hover:text-white hover:border-white/25'
              }`}
            >
              <Scan className="w-3.5 h-3.5 text-emerald-400" />
              <span>Blueprint Mode</span>
            </button>

            <button
              type="button"
              onClick={handleResetCamera}
              aria-label="Reset 3D camera to default framing"
              title="Reset isometric perspective"
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#050505]/85 text-[#A3A3A3] border border-white/10 hover:text-white hover:border-white/25 text-xs font-mono transition-all shadow-md"
            >
              <RotateCcw className="w-3.5 h-3.5 text-emerald-400" />
              <span>Reset View</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
