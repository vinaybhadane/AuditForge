'use client';

import React, { useRef, useEffect, useMemo } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { useGLTF, Html } from '@react-three/drei';
import { Sparkles, CheckCircle2, AlertTriangle, Eye } from 'lucide-react';

export type MilestoneId = 'level-1' | 'level-2' | 'level-3' | 'level-4';

interface ConstructionModelProps {
  activeMilestone: MilestoneId;
  wireframeMode?: boolean;
}

// Downloaded building model asset path
const MODEL_PATH = '/models/construction-building.glb';

interface InspectionZone {
  position: [number, number, number];
  title: string;
  code: string;
  status: 'verified' | 'observed' | 'warning';
  detail: string;
}

// Centered coordinate mapping for the 4 key building asset clusters
const INSPECTION_ZONES: Record<MilestoneId, InspectionZone> = {
  'level-1': {
    position: [6.14, 2.12, 3.47],
    title: 'Precast Substructure & Perimeter Blocks',
    code: 'CRIT-FND-101',
    status: 'verified',
    detail: 'Delivery batch confirmed',
  },
  'level-2': {
    position: [2.31, 1.88, 0.25],
    title: 'Cement Pallet Intake (Active)',
    code: 'CRIT-MAT-204',
    status: 'observed',
    detail: '50-bag lot cross-referenced',
  },
  'level-3': {
    position: [-1.98, 3.00, -2.44],
    title: 'Pipe Stacks & Timber Dunnage',
    code: 'CRIT-STK-305',
    status: 'warning',
    detail: 'Safety clearance verified',
  },
  'level-4': {
    position: [-6.14, 2.21, -3.36],
    title: 'Heavy Cable Reels & Rigging',
    code: 'CRIT-TLS-402',
    status: 'observed',
    detail: 'Equipment manifest logged',
  },
};

export function ConstructionModel({
  activeMilestone,
  wireframeMode = false,
}: ConstructionModelProps) {
  const groupRef = useRef<THREE.Group>(null);
  const { scene } = useGLTF(MODEL_PATH);

  // Center and ground the model once loaded directly without cloning
  useMemo(() => {
    scene.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(scene);
    const center = new THREE.Vector3();
    box.getCenter(center);

    // Shift scene position so that:
    // - Bottom rests on y = 0
    // - Centroid is at x = 0, z = 0
    scene.position.x = -center.x;
    scene.position.y = -box.min.y;
    scene.position.z = -center.z;
  }, [scene]);

  // Handle wireframe blueprint toggle and milestone emerald/amber highlight accents
  useEffect(() => {
    scene.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        mesh.castShadow = true;
        mesh.receiveShadow = true;

        const name = (mesh.name + ' ' + (mesh.parent?.name || '')).toLowerCase();
        let isMatch = false;

        if (
          activeMilestone === 'level-1' &&
          (name.includes('concrete') || name.includes('block') || name.includes('con_cyl'))
        ) {
          isMatch = true;
        } else if (
          activeMilestone === 'level-2' &&
          (name.includes('cement') || name.includes('pallet'))
        ) {
          isMatch = true;
        } else if (
          activeMilestone === 'level-3' &&
          (name.includes('pipe') || name.includes('plank'))
        ) {
          isMatch = true;
        } else if (
          activeMilestone === 'level-4' &&
          (name.includes('reel') ||
            name.includes('cylinder') ||
            name.includes('shovel') ||
            name.includes('hammer'))
        ) {
          isMatch = true;
        }

        const materials = Array.isArray(mesh.material)
          ? mesh.material
          : [mesh.material];

        materials.forEach((mat) => {
          if (mat instanceof THREE.MeshStandardMaterial) {
            mat.wireframe = Boolean(wireframeMode);
            if (isMatch) {
              mat.emissive = new THREE.Color('#10B981');
              mat.emissiveIntensity = 0.45;
            } else {
              mat.emissive = new THREE.Color('#000000');
              mat.emissiveIntensity = 0;
            }
            mat.needsUpdate = true;
          }
        });
      }
    });
  }, [scene, wireframeMode, activeMilestone]);

  // Subtle pointer parallax / idle floating motion
  useFrame((state) => {
    if (!groupRef.current) return;
    const t = state.clock.getElapsedTime();
    // Gentle floating breathing oscillation
    groupRef.current.position.y = Math.sin(t * 0.6) * 0.04;
  });

  const zone = INSPECTION_ZONES[activeMilestone];

  return (
    <group ref={groupRef} position={[1.2, 0, 0]}>
      {/* Centered Large-Scale Construction Building Asset */}
      <primitive object={scene} />

      {/* Architectural Ground Grid Lines */}
      <gridHelper
        args={[28, 28, '#10B981', wireframeMode ? '#047857' : '#1e293b']}
        position={[0, 0.01, 0]}
      />

      {/* Subtle Dark Ground Pad Disk */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]} receiveShadow>
        <circleGeometry args={[16, 64]} />
        <meshStandardMaterial
          color="#050505"
          roughness={0.95}
          metalness={0.1}
        />
      </mesh>

      {/* Active 3D Holographic Inspection Marker */}
      {zone && (
        <group position={zone.position}>
          {/* Ground Projection Ring */}
          <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -zone.position[1] + 0.02, 0]}>
            <ringGeometry args={[0.5, 0.65, 32]} />
            <meshBasicMaterial
              color="#10B981"
              transparent
              opacity={0.7}
              side={THREE.DoubleSide}
            />
          </mesh>

          {/* Floating UI Callout Badge */}
          <Html distanceFactor={14} center>
            <div className="pointer-events-none select-none flex flex-col items-center">
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#050505]/95 border border-emerald-500/80 shadow-2xl backdrop-blur-md text-[11px] font-mono text-white whitespace-nowrap animate-pulse">
                {zone.status === 'verified' && (
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                )}
                {zone.status === 'observed' && (
                  <Eye className="w-3.5 h-3.5 text-amber-400" />
                )}
                {zone.status === 'warning' && (
                  <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
                )}
                <span className="font-semibold text-emerald-400">{zone.code}</span>
                <span className="text-white/30">|</span>
                <span className="text-slate-200">{zone.title}</span>
              </div>
              <div className="w-0.5 h-4 bg-gradient-to-b from-emerald-500 to-transparent" />
            </div>
          </Html>
        </group>
      )}
    </group>
  );
}
