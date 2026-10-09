import React from 'react';

export function Footer() {
  return (
    <footer className="border-t border-border bg-surface-0 py-8 text-center text-xs text-text-secondary">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p>© 2026 AuditForge. Every Claim. Verified by Evidence.</p>
        <p className="text-[11px] text-text-secondary/80">
          Decision support platform — not an autonomous fraud judge or engineering certification.
        </p>
      </div>
    </footer>
  );
}
