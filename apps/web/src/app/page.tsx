import React from 'react';
import { HeroSection } from '@/components/landing/hero-section';
import { FeaturesSection } from '@/components/landing/features-section';
import { WorkflowSection } from '@/components/landing/workflow-section';
import { ReconciliationSection } from '@/components/landing/reconciliation-section';
import { EvidenceSection } from '@/components/landing/evidence-section';
import { ComparisonSection } from '@/components/landing/comparison-section';
import { HumanReviewSection } from '@/components/landing/human-review-section';
import { FinalCta } from '@/components/landing/final-cta';

export default function HomePage() {
  return (
    <div className="flex flex-col flex-1 bg-[#050505] text-[#EBEBEB]">
      {/* 1. Hero Section with Full-Screen 3D Construction Building Background */}
      <HeroSection />

      {/* 2. Four Pillars of AuditForge (Bento Grid) */}
      <FeaturesSection />

      {/* 3. 8-Stage Audit Verification Workflow */}
      <WorkflowSection />

      {/* 4. Deterministic Material Reconciliation Live Data Table */}
      <ReconciliationSection />

      {/* 5. Multi-Modal Evidence Intelligence Connected Graph */}
      <EvidenceSection />

      {/* 6. Comparison: Traditional Manual vs AuditForge Assisted */}
      <ComparisonSection />

      {/* 7. Human Review Authority Workbench */}
      <HumanReviewSection />

      {/* 8. Cinematic Final Enterprise CTA */}
      <FinalCta />
    </div>
  );
}
