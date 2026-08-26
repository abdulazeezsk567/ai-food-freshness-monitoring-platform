import React from 'react';
import { Leaf, ShieldCheck, Thermometer, Sparkles, ArrowRight, BarChart3, Users, CheckCircle2 } from 'lucide-react';

export const LandingPage = ({ onNavigate }) => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Header Nav */}
      <nav className="glass-panel border-b border-slate-800 px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <Leaf className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-extrabold text-white tracking-tight">Fresh Guard</span>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={() => onNavigate('login')}
            className="px-4 py-2 rounded-xl text-sm font-semibold text-slate-300 hover:text-white transition"
          >
            Sign In
          </button>
          <button
            onClick={() => onNavigate('register')}
            className="px-5 py-2.5 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 shadow-lg shadow-emerald-500/20 transition"
          >
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative px-6 pt-20 pb-16 text-center max-w-5xl mx-auto flex-1 flex flex-col justify-center">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass-card border border-emerald-500/30 text-emerald-400 text-xs font-semibold uppercase tracking-wider mb-6 mx-auto">
          <Sparkles className="w-4 h-4" /> Next-Generation Food Freshness Infrastructure
        </div>
        <h1 className="text-5xl sm:text-6xl font-black text-white tracking-tight leading-tight mb-6">
          AI-Powered Precision <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400">
            Food Freshness & Spoilage Intelligence
          </span>
        </h1>
        <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
          Monitor shelf life, track environmental storage metrics, optimize batch management, and prevent food spoilage across supply chains with our enterprise full-stack platform.
        </p>

        <div className="flex flex-wrap justify-center gap-4 mb-16">
          <button
            onClick={() => onNavigate('register')}
            className="flex items-center gap-2 px-7 py-3.5 rounded-2xl text-base font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 shadow-xl shadow-emerald-500/25 transition"
          >
            Launch Platform Demo <ArrowRight className="w-5 h-5" />
          </button>
          <button
            onClick={() => onNavigate('login')}
            className="flex items-center gap-2 px-7 py-3.5 rounded-2xl text-base font-bold text-slate-200 glass-card hover:bg-slate-800 transition"
          >
            Existing User Login
          </button>
        </div>

        {/* Feature Highlights Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 text-left">
          <div className="glass-card p-6 rounded-2xl">
            <ShieldCheck className="w-8 h-8 text-emerald-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Role-Based Security</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Granular access control tailored for Consumers, Retail Managers, Warehouse Operators, and Quality Inspectors.
            </p>
          </div>
          <div className="glass-card p-6 rounded-2xl">
            <Thermometer className="w-8 h-8 text-teal-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Storage Telemetry</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Real-time monitoring of temperature (°C), relative humidity, packaging types, and storage duration.
            </p>
          </div>
          <div className="glass-card p-6 rounded-2xl">
            <BarChart3 className="w-8 h-8 text-cyan-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Freshness Analytics</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Automated expiry calculation, batch status categorizations, and near-spoilage alerts.
            </p>
          </div>
          <div className="glass-card p-6 rounded-2xl">
            <Sparkles className="w-8 h-8 text-amber-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">AI Foundation</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Modular service stubs and organized datasets ready for Milestone 2 computer vision vision models.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 px-8 py-6 text-center text-xs text-slate-500">
        © 2026 Food Freshness Monitoring Platform. Built with React, FastAPI, PostgreSQL & Tailwind CSS.
      </footer>
    </div>
  );
};
