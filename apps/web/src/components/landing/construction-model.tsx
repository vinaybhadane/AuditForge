'use client';

import React, { useRef, useMemo } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';

export type MilestoneId = 'level-1' | 'level-2' | 'level-3' | 'level-4';

interface ConstructionModelProps {
  activeMilestone: MilestoneId;
  wireframeMode?: boolean;
}

export function ConstructionModel({
  activeMilestone,
  wireframeMode = false,
}: ConstructionModelProps) {
  const groupRef = useRef<THREE.Group>(null);

  // Gentle idle oscillation & pointer parallax
  useFrame((state) => {
    if (!groupRef.current) return;
    const t = state.clock.getElapsedTime();
    // Soft breathing motion
    groupRef.current.position.y = Math.sin(t * 0.5) * 0.04;
  });

  // Materials palette (Concrete, Steel, Highlight Amber, Blueprint Cyan, Scaffolding, Glass)
  const materials = useMemo(() => {
    return {
      concreteCured: new THREE.MeshStandardMaterial({
        color: wireframeMode ? '#1e3a5f' : '#D1D5DB', // light concrete
        roughness: 0.85,
        metalness: 0.1,
        wireframe: wireframeMode,
      }),
      concreteDark: new THREE.MeshStandardMaterial({
        color: wireframeMode ? '#1e293b' : '#9CA3AF',
        roughness: 0.9,
        metalness: 0.15,
        wireframe: wireframeMode,
      }),
      steelStructural: new THREE.MeshStandardMaterial({
        color: wireframeMode ? '#3b82f6' : '#334155', // dark industrial slate
        roughness: 0.4,
        metalness: 0.7,
        wireframe: wireframeMode,
      }),
      steelCrane: new THREE.MeshStandardMaterial({
        color: wireframeMode ? '#f59e0b' : '#D97706', // safety amber crane
        roughness: 0.4,
        metalness: 0.6,
        wireframe: wireframeMode,
      }),
      scaffoldingPipe: new THREE.MeshStandardMaterial({
        color: wireframeMode ? '#60a5fa' : '#64748B',
        roughness: 0.3,
        metalness: 0.8,
        wireframe: wireframeMode,
      }),
      safetyNetting: new THREE.MeshStandardMaterial({
        color: '#0284C7',
        transparent: true,
        opacity: wireframeMode ? 0.4 : 0.25,
        roughness: 0.9,
        wireframe: true,
      }),
      glassCladding: new THREE.MeshStandardMaterial({
        color: '#93C5FD',
        transparent: true,
        opacity: wireframeMode ? 0.3 : 0.5,
        roughness: 0.1,
        metalness: 0.9,
      }),
      rebarSteel: new THREE.MeshStandardMaterial({
        color: wireframeMode ? '#ef4444' : '#991B1B', // rust rebar red
        roughness: 0.6,
        metalness: 0.5,
      }),
      highlightAmber: new THREE.MeshStandardMaterial({
        color: '#E9A23B',
        roughness: 0.3,
        metalness: 0.4,
        emissive: new THREE.Color('#E9A23B'),
        emissiveIntensity: 0.35,
        wireframe: wireframeMode,
      }),
      highlightTeal: new THREE.MeshStandardMaterial({
        color: '#1C8C83',
        roughness: 0.3,
        metalness: 0.4,
        emissive: new THREE.Color('#1C8C83'),
        emissiveIntensity: 0.3,
        wireframe: wireframeMode,
      }),
      palletWood: new THREE.MeshStandardMaterial({
        color: wireframeMode ? '#475569' : '#B45309',
        roughness: 0.9,
      }),
      cementBags: new THREE.MeshStandardMaterial({
        color: wireframeMode ? '#64748b' : '#E5E7EB',
        roughness: 0.95,
      }),
    };
  }, [wireframeMode]);

  // Column grid specs (3 x 4 grid)
  const xPositions = useMemo(() => [-4.5, -1.5, 1.5, 4.5], []);
  const zPositions = useMemo(() => [-3, 0, 3], []);

  // Floor heights: Level 1 = 0..2.2, Level 2 = 2.2..4.4, Level 3 = 4.4..6.6, Level 4 = 6.6..8.8
  const isL1Active = activeMilestone === 'level-1';
  const isL2Active = activeMilestone === 'level-2';
  const isL3Active = activeMilestone === 'level-3';
  const isL4Active = activeMilestone === 'level-4';

  return (
    <group ref={groupRef} position={[0, -2.8, 0]}>
      {/* ---------------- GROUND PLANE & SITE GRID ---------------- */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.05, 0]}>
        <planeGeometry args={[26, 22]} />
        <meshStandardMaterial
          color={wireframeMode ? '#0f172a' : '#F1F5F9'}
          roughness={0.95}
          metalness={0.05}
        />
      </mesh>

      {/* Ground boundary lines & surveying crosshairs */}
      <gridHelper
        args={[24, 24, '#E9A23B', wireframeMode ? '#1e3a5f' : '#CBD5E1']}
        position={[0, -0.03, 0]}
      />

      {/* ---------------- LEVEL 1: FOUNDATION SLAB & BASEMENT ---------------- */}
      <group name="Level-1-Foundation">
        {/* Main Base Slab */}
        <mesh position={[0, 0.15, 0]}>
          <boxGeometry args={[11.5, 0.3, 8.5]} />
          <primitive
            object={isL1Active ? materials.highlightAmber : materials.concreteDark}
            attach="material"
          />
        </mesh>

        {/* Foundation Plinth edge */}
        <mesh position={[0, 0.35, 0]}>
          <boxGeometry args={[11, 0.1, 8]} />
          <primitive
            object={isL1Active ? materials.highlightAmber : materials.concreteCured}
            attach="material"
          />
        </mesh>

        {/* Level 1 Columns */}
        {xPositions.map((x, xi) =>
          zPositions.map((z, zi) => (
            <mesh key={`col-l1-${xi}-${zi}`} position={[x, 1.3, z]}>
              <boxGeometry args={[0.55, 1.8, 0.55]} />
              <primitive
                object={isL1Active ? materials.highlightAmber : materials.concreteCured}
                attach="material"
              />
            </mesh>
          ))
        )}

        {/* Level 1 Partially Completed Cladding (West & South Facades) */}
        {/* West Wall with Window Openings */}
        <mesh position={[-5.3, 1.3, 0]}>
          <boxGeometry args={[0.2, 1.8, 7.6]} />
          <primitive object={materials.concreteCured} attach="material" />
        </mesh>
        {/* Architectural Windows on West Wall */}
        <mesh position={[-5.32, 1.4, -1.8]}>
          <boxGeometry args={[0.25, 0.9, 1.6]} />
          <primitive object={materials.glassCladding} attach="material" />
        </mesh>
        <mesh position={[-5.32, 1.4, 1.8]}>
          <boxGeometry args={[0.25, 0.9, 1.6]} />
          <primitive object={materials.glassCladding} attach="material" />
        </mesh>

        {/* South Wall Cladding (partial) */}
        <mesh position={[0, 1.3, -3.8]}>
          <boxGeometry args={[10.6, 1.8, 0.2]} />
          <primitive object={materials.concreteCured} attach="material" />
        </mesh>

        {/* Elevator Shear Core (Central shaft running through all floors) */}
        <mesh position={[0, 4.4, 0]}>
          <boxGeometry args={[2.2, 8.6, 2.2]} />
          <primitive
            object={isL2Active ? materials.highlightAmber : materials.concreteDark}
            attach="material"
          />
        </mesh>

        {/* Level 1 Ceiling / Floor 2 Slab */}
        <mesh position={[0, 2.25, 0]}>
          <boxGeometry args={[11.2, 0.2, 8.2]} />
          <primitive
            object={isL1Active ? materials.highlightAmber : materials.concreteCured}
            attach="material"
          />
        </mesh>
      </group>

      {/* ---------------- LEVEL 2: STRUCTURAL COLUMNS & CORE (ACTIVE MILESTONE) ---------------- */}
      <group name="Level-2-Columns">
        {/* Structural Longitudinal Beams (connecting columns along X) */}
        {zPositions.map((z, zi) => (
          <mesh key={`beam-x-l2-${zi}`} position={[0, 4.3, z]}>
            <boxGeometry args={[10.5, 0.35, 0.4]} />
            <primitive
              object={isL2Active ? materials.highlightAmber : materials.steelStructural}
              attach="material"
            />
          </mesh>
        ))}

        {/* Structural Transversal Beams (connecting columns along Z) */}
        {xPositions.map((x, xi) => (
          <mesh key={`beam-z-l2-${xi}`} position={[x, 4.3, 0]}>
            <boxGeometry args={[0.4, 0.35, 7.5]} />
            <primitive
              object={isL2Active ? materials.highlightAmber : materials.steelStructural}
              attach="material"
            />
          </mesh>
        ))}

        {/* Level 2 Columns */}
        {xPositions.map((x, xi) =>
          zPositions.map((z, zi) => {
            const isTargetColumn = xi === 2 && zi === 1; // Inspected column C3
            return (
              <group key={`col-l2-${xi}-${zi}`}>
                <mesh position={[x, 3.3, z]}>
                  <boxGeometry args={[0.5, 1.9, 0.5]} />
                  <primitive
                    object={
                      isTargetColumn || isL2Active
                        ? materials.highlightAmber
                        : materials.concreteCured
                    }
                    attach="material"
                  />
                </mesh>

                {/* Inspection highlight beacon over designated column C3 */}
                {isTargetColumn && isL2Active && (
                  <mesh position={[x, 4.6, z]}>
                    <octahedronGeometry args={[0.25, 0]} />
                    <primitive object={materials.highlightAmber} attach="material" />
                  </mesh>
                )}
              </group>
            );
          })
        )}

        {/* Level 2 Floor Slab (underneath Level 3) */}
        <mesh position={[0, 4.45, 0]}>
          <boxGeometry args={[11, 0.2, 8]} />
          <primitive
            object={isL2Active ? materials.highlightAmber : materials.concreteCured}
            attach="material"
          />
        </mesh>

        {/* Milestone 2 Dimension / Datum Ring Indicator */}
        {isL2Active && (
          <mesh position={[0, 3.3, 0]} rotation={[-Math.PI / 2, 0, 0]}>
            <ringGeometry args={[6.2, 6.35, 32]} />
            <meshBasicMaterial
              color="#E9A23B"
              transparent
              opacity={0.7}
              side={THREE.DoubleSide}
            />
          </mesh>
        )}
      </group>

      {/* ---------------- LEVEL 3: ACTIVE FRAMING & STEEL DECK ---------------- */}
      <group name="Level-3-Framing">
        {/* Steel Beams Matrix */}
        {zPositions.map((z, zi) => (
          <mesh key={`beam-x-l3-${zi}`} position={[0, 6.5, z]}>
            <boxGeometry args={[10.5, 0.3, 0.35]} />
            <primitive
              object={isL3Active ? materials.highlightAmber : materials.steelStructural}
              attach="material"
            />
          </mesh>
        ))}

        {xPositions.map((x, xi) => (
          <mesh key={`beam-z-l3-${xi}`} position={[x, 6.5, 0]}>
            <boxGeometry args={[0.35, 0.3, 7.5]} />
            <primitive
              object={isL3Active ? materials.highlightAmber : materials.steelStructural}
              attach="material"
            />
          </mesh>
        ))}

        {/* Level 3 Columns (Partially exposed steel + formwork) */}
        {xPositions.map((x, xi) =>
          zPositions.map((z, zi) => (
            <group key={`col-l3-${xi}-${zi}`}>
              <mesh position={[x, 5.5, z]}>
                <boxGeometry args={[0.42, 1.9, 0.42]} />
                <primitive
                  object={isL3Active ? materials.highlightAmber : materials.steelStructural}
                  attach="material"
                />
              </mesh>

              {/* Rebar Spires projecting into next floor */}
              <mesh position={[x - 0.12, 6.75, z - 0.12]}>
                <cylinderGeometry args={[0.025, 0.025, 0.6, 6]} />
                <primitive object={materials.rebarSteel} attach="material" />
              </mesh>
              <mesh position={[x + 0.12, 6.75, z + 0.12]}>
                <cylinderGeometry args={[0.025, 0.025, 0.6, 6]} />
                <primitive object={materials.rebarSteel} attach="material" />
              </mesh>
            </group>
          ))
        )}

        {/* Level 3 Floor Deck (Corrugated Steel / Partial Concrete Pour) */}
        <mesh position={[-1.5, 6.62, 0]}>
          <boxGeometry args={[7.5, 0.15, 7.6]} />
          <primitive
            object={isL3Active ? materials.highlightAmber : materials.concreteDark}
            attach="material"
          />
        </mesh>

        {/* Active Concrete Pouring Formwork timber boundary */}
        <mesh position={[2.5, 6.7, 0]}>
          <boxGeometry args={[0.08, 0.3, 7.4]} />
          <primitive object={materials.palletWood} attach="material" />
        </mesh>
      </group>

      {/* ---------------- LEVEL 4: TOP DECK, SCAFFOLDING & CRANE ---------------- */}
      <group name="Level-4-Scaffolding">
        {/* Perimeter Scaffolding Tubes on East Face */}
        {[-3, -1, 1, 3].map((z, i) => (
          <group key={`scaff-post-${i}`} position={[5.4, 5.5, z]}>
            {/* Vertical standards */}
            <mesh>
              <cylinderGeometry args={[0.04, 0.04, 5.2, 8]} />
              <primitive
                object={isL4Active ? materials.highlightAmber : materials.scaffoldingPipe}
                attach="material"
              />
            </mesh>
            {/* Horizontal ledgers */}
            <mesh position={[0, 0.8, 0]} rotation={[Math.PI / 2, 0, 0]}>
              <cylinderGeometry args={[0.03, 0.03, 2, 8]} />
              <primitive
                object={isL4Active ? materials.highlightAmber : materials.scaffoldingPipe}
                attach="material"
              />
            </mesh>
            <mesh position={[0, -1.2, 0]} rotation={[Math.PI / 2, 0, 0]}>
              <cylinderGeometry args={[0.03, 0.03, 2, 8]} />
              <primitive
                object={isL4Active ? materials.highlightAmber : materials.scaffoldingPipe}
                attach="material"
              />
            </mesh>
          </group>
        ))}

        {/* Safety Netting Mesh along East Elevation */}
        <mesh position={[5.42, 5.5, 0]}>
          <boxGeometry args={[0.02, 4.8, 7.6]} />
          <primitive object={materials.safetyNetting} attach="material" />
        </mesh>

        {/* Perimeter Safety Railings on Top Deck */}
        <mesh position={[0, 6.95, -3.8]}>
          <boxGeometry args={[10.5, 0.04, 0.04]} />
          <primitive object={materials.scaffoldingPipe} attach="material" />
        </mesh>
        <mesh position={[0, 6.95, 3.8]}>
          <boxGeometry args={[10.5, 0.04, 0.04]} />
          <primitive object={materials.scaffoldingPipe} attach="material" />
        </mesh>
      </group>

      {/* ---------------- TOWER CRANE SILHOUETTE & RIGGING ---------------- */}
      <group name="TowerCrane" position={[-4.5, 0, -4.5]}>
        {/* Crane Foundation Plinth */}
        <mesh position={[0, 0.25, 0]}>
          <boxGeometry args={[1.6, 0.5, 1.6]} />
          <primitive object={materials.concreteDark} attach="material" />
        </mesh>

        {/* Crane Vertical Mast (Tower) */}
        <mesh position={[0, 6.2, 0]}>
          <boxGeometry args={[0.7, 11.5, 0.7]} />
          <primitive object={materials.steelCrane} attach="material" />
        </mesh>

        {/* Crane Slewing Ring & Operator Cabin */}
        <mesh position={[0, 11.8, 0]}>
          <cylinderGeometry args={[0.6, 0.6, 0.4, 12]} />
          <primitive object={materials.steelStructural} attach="material" />
        </mesh>
        <mesh position={[0.5, 12.1, 0.4]}>
          <boxGeometry args={[0.8, 0.8, 0.7]} />
          <primitive object={materials.glassCladding} attach="material" />
        </mesh>

        {/* Crane Tower Peak (A-frame Apex) */}
        <mesh position={[0, 13.2, 0]}>
          <coneGeometry args={[0.5, 2.2, 4]} />
          <primitive object={materials.steelCrane} attach="material" />
        </mesh>

        {/* Horizontal Jib (Main Boom extending over the building) */}
        <mesh position={[4.5, 12.3, 0]}>
          <boxGeometry args={[9.5, 0.4, 0.4]} />
          <primitive object={materials.steelCrane} attach="material" />
        </mesh>

        {/* Counter-Jib (Rear Boom with concrete counterweights) */}
        <mesh position={[-2.2, 12.3, 0]}>
          <boxGeometry args={[4.2, 0.4, 0.4]} />
          <primitive object={materials.steelCrane} attach="material" />
        </mesh>
        <mesh position={[-3.5, 12.1, 0]}>
          <boxGeometry args={[1.2, 0.8, 0.7]} />
          <primitive object={materials.concreteDark} attach="material" />
        </mesh>

        {/* Trolley Carriage along Main Jib */}
        <mesh position={[5.2, 12.05, 0]}>
          <boxGeometry args={[0.5, 0.15, 0.45]} />
          <primitive object={materials.steelStructural} attach="material" />
        </mesh>

        {/* Suspended Hoist Wire Rope */}
        <mesh position={[5.2, 9.8, 0]}>
          <cylinderGeometry args={[0.015, 0.015, 4.2, 4]} />
          <primitive object={materials.scaffoldingPipe} attach="material" />
        </mesh>

        {/* Hook Block & Rigging Spreader */}
        <mesh position={[5.2, 7.6, 0]}>
          <boxGeometry args={[0.3, 0.35, 0.25]} />
          <primitive
            object={isL4Active ? materials.highlightAmber : materials.steelCrane}
            attach="material"
          />
        </mesh>
      </group>

      {/* ---------------- SITE GROUND ELEMENTS (PALLETS & REBAR) ---------------- */}
      <group name="SiteGroundElements">
        {/* Stack of Cement Bags on Pallet (Zone East) */}
        <group position={[6.5, 0, -1.8]}>
          {/* Wood Pallet */}
          <mesh position={[0, 0.1, 0]}>
            <boxGeometry args={[1.4, 0.15, 1.4]} />
            <primitive object={materials.palletWood} attach="material" />
          </mesh>
          {/* Cement Bags Layer 1 */}
          <mesh position={[0, 0.28, 0]}>
            <boxGeometry args={[1.2, 0.2, 1.2]} />
            <primitive object={materials.cementBags} attach="material" />
          </mesh>
          {/* Cement Bags Layer 2 */}
          <mesh position={[0, 0.48, 0]}>
            <boxGeometry args={[1.15, 0.2, 1.15]} />
            <primitive object={materials.cementBags} attach="material" />
          </mesh>
        </group>

        {/* Stacked Steel Rebar Bundles (Zone South) */}
        <group position={[2.5, 0, 4.8]}>
          <mesh position={[0, 0.08, 0]}>
            <boxGeometry args={[4.2, 0.12, 0.8]} />
            <primitive object={materials.palletWood} attach="material" />
          </mesh>
          <mesh position={[0, 0.25, 0]} rotation={[0, 0, Math.PI / 2]}>
            <cylinderGeometry args={[0.18, 0.18, 3.8, 12]} />
            <primitive object={materials.rebarSteel} attach="material" />
          </mesh>
          <mesh position={[0, 0.45, 0]} rotation={[0, 0, Math.PI / 2]}>
            <cylinderGeometry args={[0.14, 0.14, 3.8, 12]} />
            <primitive object={materials.rebarSteel} attach="material" />
          </mesh>
        </group>
      </group>
    </group>
  );
}
