'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Menu, X, ArrowUpRight, ShieldCheck } from 'lucide-react';

interface NavItem {
  label: string;
  href: string;
}

const NAV_ITEMS: NavItem[] = [
  { label: 'Platform', href: '#features' },
  { label: 'Capabilities', href: '#reconciliation' },
  { label: 'Methodology', href: '#workflow' },
  { label: 'Evidence Intelligence', href: '#evidence' },
];

export function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-[#050505]/85 backdrop-blur-md border-b border-white/10 py-3.5 shadow-2xl shadow-black/60'
          : 'bg-transparent border-b border-transparent py-5'
      }`}
    >
      <div className="container mx-auto flex max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Left: Brand Wordmark with Architectural Symbol */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="relative flex h-8 w-8 items-center justify-center rounded-lg bg-white/[0.04] border border-white/10 text-emerald-400 group-hover:border-emerald-500/40 transition-colors">
            {/* Architectural Isometric Diamond Icon */}
            <div className="w-3.5 h-3.5 border-2 border-emerald-400 rotate-45 group-hover:rotate-90 transition-transform duration-500 flex items-center justify-center">
              <div className="w-1 h-1 bg-emerald-400 rounded-full" />
            </div>
          </div>
          <div className="flex flex-col">
            <div className="flex items-center gap-1.5">
              <span className="font-serif text-lg tracking-tight font-bold text-white">
                AuditForge
              </span>
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400" />
            </div>
            <span className="text-[10px] font-mono tracking-wider text-[#888888] -mt-0.5">
              ARCHITECTURAL INTELLIGENCE
            </span>
          </div>
        </Link>

        {/* Center: Desktop Navigation Links with Emerald Underline Animation */}
        <nav
          aria-label="Main Navigation"
          className="hidden md:flex items-center gap-8 text-xs font-mono tracking-wider"
        >
          {NAV_ITEMS.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="relative py-1 text-[#A3A3A3] hover:text-white transition-colors duration-200 group"
            >
              <span>{item.label}</span>
              <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-emerald-400 transition-all duration-300 ease-out group-hover:w-full" />
            </a>
          ))}
        </nav>

        {/* Right: Sign In & Get Started Pill Button */}
        <div className="hidden sm:flex items-center gap-4">
          <Link
            href="/login"
            className="text-xs font-mono text-[#A3A3A3] hover:text-white transition-colors px-2 py-1"
          >
            Sign In
          </Link>
          <Link
            href="/dashboard"
            className="group relative inline-flex items-center gap-1.5 px-4 py-2 rounded-full text-xs font-mono font-medium text-white bg-white/[0.06] hover:bg-emerald-500/10 border border-white/15 hover:border-emerald-500/40 shadow-sm transition-all duration-200"
          >
            <span>Get Started</span>
            <ArrowUpRight className="w-3.5 h-3.5 text-emerald-400 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
          </Link>
        </div>

        {/* Mobile Hamburger Toggle Button */}
        <button
          type="button"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-expanded={mobileMenuOpen}
          aria-label="Toggle navigation menu"
          className="md:hidden p-2 rounded-lg text-[#A3A3A3] hover:text-white hover:bg-white/[0.05] transition-colors border border-white/10"
        >
          {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-white/10 bg-[#050505]/95 backdrop-blur-xl px-6 pt-4 pb-6 space-y-4 font-mono text-xs animate-in slide-in-from-top-2 duration-200">
          <div className="flex flex-col space-y-3 pt-2 border-b border-white/10 pb-4">
            {NAV_ITEMS.map((item) => (
              <a
                key={item.href}
                href={item.href}
                onClick={() => setMobileMenuOpen(false)}
                className="py-1 text-[#A3A3A3] hover:text-emerald-400 transition-colors flex items-center justify-between"
              >
                <span>{item.label}</span>
                <span className="text-white/20">→</span>
              </a>
            ))}
          </div>

          <div className="flex items-center justify-between pt-2">
            <Link
              href="/login"
              onClick={() => setMobileMenuOpen(false)}
              className="text-[#A3A3A3] hover:text-white py-1"
            >
              Sign In
            </Link>
            <Link
              href="/dashboard"
              onClick={() => setMobileMenuOpen(false)}
              className="inline-flex items-center gap-1 px-4 py-2 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs"
            >
              <span>Get Started</span>
              <ArrowUpRight className="w-3 h-3" />
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
