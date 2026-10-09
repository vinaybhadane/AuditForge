import { z } from 'zod';

const envSchema = z.object({
  NEXT_PUBLIC_APP_URL: z.string().url().default('http://localhost:3000'),
  NEXT_PUBLIC_SUPABASE_URL: z.string().default('https://YOUR_PROJECT.supabase.co'),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().default('YOUR_PUBLIC_ANON_KEY'),
  NEXT_PUBLIC_API_URL: z.string().default('http://localhost:8000/api/v1'),
});

const parsed = envSchema.safeParse({
  NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
  NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
  NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
});

if (!parsed.success) {
  console.warn('⚠️ Frontend environment variable validation warning:', parsed.error.format());
}

export const env = parsed.success
  ? parsed.data
  : {
      NEXT_PUBLIC_APP_URL: 'http://localhost:3000',
      NEXT_PUBLIC_SUPABASE_URL: 'https://YOUR_PROJECT.supabase.co',
      NEXT_PUBLIC_SUPABASE_ANON_KEY: 'YOUR_PUBLIC_ANON_KEY',
      NEXT_PUBLIC_API_URL: 'http://localhost:8000/api/v1',
    };
