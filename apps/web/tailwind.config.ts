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
        brand: {
          950: '#101B2D',
          800: '#1C3555',
          700: '#24527A',
          600: '#2D6FA3',
        },
        signal: {
          amber: '#E9A23B',
          teal: '#1C8C83',
        },
        danger: {
          700: '#B42318',
        },
        warning: {
          700: '#9A6700',
        },
        success: {
          700: '#18794E',
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
        sans: [
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'sans-serif',
        ],
        mono: [
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'Monaco',
          'Consolas',
          'Liberation Mono',
          'Courier New',
          'monospace',
        ],
      },
    },
  },
  plugins: [],
};

export default config;
