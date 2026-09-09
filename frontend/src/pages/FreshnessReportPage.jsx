import React from 'react';
import { StatusBadge } from '../components/StatusBadge';
import { ArrowLeft, Printer, ShieldCheck, Sparkles, FileText, CheckCircle, AlertTriangle } from 'lucide-react';

export const FreshnessReportPage = ({ report, onBack }) => {
  if (!report) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in print:p-0">
      {/* Top Header Controls (Hidden when printing) */}
      <div className="flex items-center justify-between glass-panel p-4 rounded-2xl border border-slate-800 print:hidden">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-xs font-bold text-slate-300 hover:text-white px-3 py-2 rounded-xl bg-slate-800 transition"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Analysis
        </button>
        <button
          onClick={handlePrint}
          className="flex items-center gap-2 text-xs font-bold text-white px-4 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 shadow-lg transition"
        >
          <Printer className="w-4 h-4" /> Print / Save Report PDF
        </button>
      </div>

      {/* Formal Printable Document Card */}
      <div className="glass-card p-8 rounded-3xl border border-slate-800 space-y-8 bg-slate-900/90 text-slate-100 print:bg-white print:text-slate-900 print:shadow-none print:border-none print:p-0">
        
        {/* Document Header */}
        <div className="flex items-center justify-between border-b border-slate-800 print:border-slate-300 pb-6">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center text-white font-bold text-xl shadow-lg">
              🌿
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tight text-white print:text-slate-900">
                Fresh Guard Inspection Report
              </h1>
              <p className="text-xs text-slate-400 print:text-slate-600 font-medium">
                AI-Powered Visual Freshness Assessment Certificate
              </p>
            </div>
          </div>
          <div className="text-right text-xs text-slate-400 print:text-slate-600">
            <div>Report ID: <span className="font-mono font-bold text-white print:text-slate-900">#AN-{report.id}</span></div>
            <div>Date: <span className="font-bold text-white print:text-slate-900">{new Date(report.created_at).toLocaleString()}</span></div>
            <div>Engine Version: <span className="font-mono font-bold text-emerald-400">{report.model_version || 'v1.0.0-CV'}</span></div>
          </div>
        </div>

        {/* Target Image & Core Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
          <div className="md:col-span-5 text-center">
            <img
              src={report.image_path}
              alt="Inspected Food"
              className="max-h-64 mx-auto rounded-2xl object-cover border border-slate-700 print:border-slate-300 shadow-xl"
            />
            <span className="text-xs font-bold text-slate-400 print:text-slate-600 mt-2 block">
              Category: {report.food_category}
            </span>
          </div>

          <div className="md:col-span-7 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400 print:text-slate-600">
                Classification Status
              </span>
              <StatusBadge status={report.predicted_category} />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="glass-panel p-4 rounded-2xl border border-emerald-500/30 bg-emerald-950/20 print:bg-emerald-50 print:border-emerald-300">
                <span className="text-[10px] font-bold uppercase text-slate-400 print:text-slate-600 block">Freshness Score</span>
                <div className="text-4xl font-black text-emerald-400 print:text-emerald-700">{report.freshness_score} <span className="text-sm font-semibold">/100</span></div>
              </div>

              <div className="glass-panel p-4 rounded-2xl border border-amber-500/30 bg-amber-950/20 print:bg-amber-50 print:border-amber-300">
                <span className="text-[10px] font-bold uppercase text-slate-400 print:text-slate-600 block">Spoilage Risk</span>
                <div className="text-4xl font-black text-amber-400 print:text-amber-700">{(report.spoilage_probability * 100).toFixed(1)}%</div>
              </div>
            </div>

            <div className="glass-panel p-3 rounded-xl border border-slate-800 text-xs flex justify-between text-slate-300 print:text-slate-700">
              <span>Model Classification Confidence:</span>
              <span className="font-bold text-purple-300 print:text-purple-700">{(report.confidence * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>

        {/* Detailed Decomposition */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
          {/* Color Decomposition */}
          <div className="glass-panel p-5 rounded-2xl border border-slate-800 print:border-slate-300 space-y-3">
            <h3 className="font-bold text-white print:text-slate-900 uppercase tracking-wider">
              🎨 Color & Pigment Decomposition
            </h3>
            <div className="space-y-1.5 text-slate-300 print:text-slate-700">
              <p>• Status: <span className="font-bold text-white print:text-slate-900">{report.color_analysis?.status}</span></p>
              <p>• Browning Index (BI): <span className="font-bold text-white print:text-slate-900">{report.color_analysis?.browning_index}</span></p>
              <p>• Discoloration Area: <span className="font-bold text-white print:text-slate-900">{((report.color_analysis?.discolored_pixel_ratio || 0) * 100).toFixed(1)}%</span></p>
              {report.color_analysis?.observations?.map((obs, i) => (
                <p key={i} className="text-slate-400 print:text-slate-600">• {obs}</p>
              ))}
            </div>
          </div>

          {/* Texture Decomposition */}
          <div className="glass-panel p-5 rounded-2xl border border-slate-800 print:border-slate-300 space-y-3">
            <h3 className="font-bold text-white print:text-slate-900 uppercase tracking-wider">
              🔬 Texture & Structure Metrics
            </h3>
            <div className="space-y-1.5 text-slate-300 print:text-slate-700">
              <p>• Local Homogeneity: <span className="font-bold text-white print:text-slate-900">{report.texture_analysis?.homogeneity}</span></p>
              <p>• Gradient Variance: <span className="font-bold text-white print:text-slate-900">{report.texture_analysis?.gradient_variance}</span></p>
              {report.texture_analysis?.observations?.map((obs, i) => (
                <p key={i} className="text-slate-400 print:text-slate-600">• {obs}</p>
              ))}
            </div>
          </div>
        </div>

        {/* Spoilage Indicators Breakdown */}
        <div className="space-y-3 text-xs">
          <h3 className="font-bold text-white print:text-slate-900 uppercase tracking-wider">
            🔍 Visual Spoilage Indicators Audit
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {Object.entries(report.spoilage_indicators || {}).map(([key, ind]) => (
              <div key={key} className="glass-panel p-3.5 rounded-xl border border-slate-800 print:border-slate-300">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-white print:text-slate-900 capitalize">{key.replace('_', ' ')}</span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${ind.detected ? 'bg-rose-500/20 text-rose-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                    {ind.detected ? 'DETECTED' : 'CLEAR'}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 print:text-slate-600">{ind.evidence}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Certificate Verification Footer */}
        <div className="pt-6 border-t border-slate-800 print:border-slate-300 flex items-center justify-between text-xs text-slate-500 print:text-slate-600">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Verified by Computer Vision Engine ({report.model_version || 'v1.0.0-CV'})</span>
          </div>
          <div>Food Freshness Monitoring Platform</div>
        </div>
      </div>
    </div>
  );
};
