import React from 'react';
import { cn } from '@/lib/utils';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', ...props }, ref) => {
    const variantStyles = {
      primary: 'bg-brand-700 text-white hover:bg-brand-800 active:bg-brand-950 shadow-sm',
      secondary: 'bg-surface-100 text-text-primary hover:bg-border active:bg-slate-300',
      outline: 'border border-border bg-transparent text-text-primary hover:bg-surface-100',
      danger: 'bg-danger-700 text-white hover:bg-red-800 shadow-sm',
      ghost: 'bg-transparent text-text-secondary hover:text-text-primary hover:bg-surface-100',
    }[variant];

    const sizeStyles = {
      sm: 'h-8 px-3 text-xs rounded-md',
      md: 'h-10 px-4 text-sm rounded-lg',
      lg: 'h-12 px-6 text-base rounded-lg',
    }[size];

    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-600 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 select-none',
          variantStyles,
          sizeStyles,
          className
        )}
        {...props}
      />
    );
  }
);

Button.displayName = 'Button';
