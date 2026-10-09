import { cn } from '../src/lib/utils';
import { env } from '../src/lib/env';

describe('Web Foundation Smoke Tests', () => {
  it('correctly merges tailwind classes with cn utility', () => {
    const result = cn('px-2 py-1', 'bg-brand-700', { 'text-white': true });
    expect(result).toContain('px-2');
    expect(result).toContain('bg-brand-700');
    expect(result).toContain('text-white');
  });

  it('provides safe environment defaults', () => {
    expect(env.NEXT_PUBLIC_APP_URL).toBeDefined();
    expect(env.NEXT_PUBLIC_API_URL).toBeDefined();
  });
});
