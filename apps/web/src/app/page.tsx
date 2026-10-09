import React from 'react';
import { HeroSection } from '@/components/landing/hero-section';
import { ProblemSection } from '@/components/landing/problem-section';
import { WorkflowSection } from '@/components/landing/workflow-section';
import { EvidenceSection } from '@/components/landing/evidence-section';
import { ReconciliationSection } from '@/components/landing/reconciliation-section';
import { HumanReviewSection } from '@/components/landing/human-review-section';
import { FinalCta } from '@/components/landing/final-cta';

export default function HomePage() {
  return (
    <div className="flex flex-col flex-1">
      {/* 1. Hero Section with Interactive 3D Model */}
      <HeroSection />

      {/* 2. The Construction Audit Problem */}
      <ProblemSection />

      {/* 3. 7-Stage AuditForge Workflow */}
      <WorkflowSection />

      {/* 4. Multi-Modal Evidence Intelligence Graph */}
      <EvidenceSection />

      {/* 5. Deterministic Material Reconciliation */}
      <ReconciliationSection />

      {/* 6. Human Review Authority Workbench */}
      <HumanReviewSection />

      {/* 7. Final Enterprise Call to Action */}
      <FinalCta />
    </div>
  );
}
