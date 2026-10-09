import type { Metadata } from 'next';
import { Inter, Newsreader, Space_Grotesk } from 'next/font/google';
import '@/styles/globals.css';
import { Header } from '@/components/layout/header';
import { Footer } from '@/components/layout/footer';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const newsreader = Newsreader({
  subsets: ['latin'],
  style: ['normal', 'italic'],
  variable: '--font-newsreader',
  display: 'swap',
});

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-space-grotesk',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'AuditForge — Every Claim. Verified by Evidence.',
  description:
    'Evidence-first construction operations auditing platform. Correlating visual milestone evidence, vendor documents, and deterministic material reconciliation.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${newsreader.variable} ${spaceGrotesk.variable} dark`}
    >
      <body className="min-h-screen flex flex-col bg-[#050505] text-[#EBEBEB] antialiased font-sans selection:bg-emerald-500/30 selection:text-emerald-300">
        <Header />
        <main className="flex-1 flex flex-col">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
