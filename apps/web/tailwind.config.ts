import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#050505',
          surface: 'rgba(255, 255, 255, 0.035)',
          'surface-hover': 'rgba(255, 255, 255, 0.06)',
          border: 'rgba(255, 255, 255, 0.10)',
          'border-subtle': 'rgba(255, 255, 255, 0.06)',
          text: '#EBEBEB',
          secondary: '#A3A3A3',
          muted: '#888888',
        },
        emerald: {
          DEFAULT: '#10B981',
          400: '#34D399',
          500: '#10B981',
          600: '#059669',
        },
        brand: {
          950: '#101B2D',
          800: '#1C3555',
          700: '#24527A',
          600: '#2D6FA3',
        },
        signal: {
          amber: '#F59E0B',
          teal: '#10B981',
          red: '#F87171',
        },
        surface: {
          0: '#FFFFFF',
          50: '#F7F9FC',
          100: '#EEF2F7',
        },
        border: {
          DEFAULT: '#D7DEE8',
        },
        text: {
          primary: '#172334',
          secondary: '#536276',
        },
      },
      fontFamily: {
        serif: ['Newsreader', 'Georgia', 'serif'],
        sans: [
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'sans-serif',
        ],
        mono: [
          'Space Grotesk',
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'monospace',
        ],
        grotesk: [
          'Space Grotesk',
          '-apple-system',
          'sans-serif',
        ],
      },
      transitionTimingFunction: {
        architectural: 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
    },
  },
  plugins: [],
};

export default config;
