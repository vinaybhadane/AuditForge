import React from 'react';
import { cn } from '@/lib/utils';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'verified' | 'pending' | 'warning' | 'danger' | 'ai';
}

export function Badge({
  className,
  variant = 'default',
  children,
  ...props
}: BadgeProps) {
  const variantStyles = {
    default: 'bg-surface-100 text-text-secondary border-border',
    verified: 'bg-teal-50 text-signal-teal border-teal-200 font-medium',
    pending: 'bg-amber-50 text-amber-800 border-amber-200 font-medium',
    warning: 'bg-amber-100 text-warning-700 border-amber-300 font-medium',
    danger: 'bg-red-50 text-danger-700 border-red-200 font-medium',
    ai: 'bg-slate-100 text-slate-700 border-slate-300 italic',
  }[variant];

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium tabular-nums transition-colors',
        variantStyles,
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
