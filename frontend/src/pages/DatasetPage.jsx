import React from 'react';
import { Database, FolderTree, Image, CheckCircle, Sparkles, FileText } from 'lucide-react';

export const DatasetPage = () => {
  const datasets = [
    {
      title: 'Fruits Freshness Dataset',
      path: 'datasets/raw/fruits/',
      desc: 'Image dataset covering fresh and rotten apples, bananas, oranges, and strawberries.',
      classes: ['fresh_apple', 'rotten_apple', 'fresh_banana', 'rotten_banana', 'fresh_orange', 'rotten_orange'],
      color: 'border-emerald-500/30 bg-emerald-950/20 text-emerald-400'
    },
    {
      title: 'Vegetable Quality Dataset',
      path: 'datasets/raw/vegetables/',
      desc: 'High-resolution images of fresh and decaying tomatoes, cucumbers, spinach, and bell peppers.',
      classes: ['fresh_tomato', 'spoiled_tomato', 'fresh_cucumber', 'spoiled_cucumber', 'fresh_pepper', 'spoiled_pepper'],
      color: 'border-teal-500/30 bg-teal-950/20 text-teal-400'
    },
    {
      title: 'Kaggle Food Freshness Benchmark',
      path: 'datasets/raw/food_freshness/',
      desc: 'Multi-category image data annotated with environmental storage temperature and humidity metadata.',
      classes: ['fresh', 'acceptable', 'near_spoilage', 'spoiled'],
      color: 'border-amber-500/30 bg-amber-950/20 text-amber-400'
    },
    {
      title: 'Food-101 Taxonomy Dataset',
      path: 'datasets/raw/food101/',
      desc: '101,000 images across 101 food classes used for automatic product classification upon inventory scan.',
      classes: ['101 Food Categories (Bakery, Dairy, Meat, Seafood, Packaged, etc.)'],
      color: 'border-purple-500/30 bg-purple-950/20 text-purple-400'
    }
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
            <Database className="w-6 h-6 text-emerald-400" /> Dataset Integration Foundation
          </h2>
          <p className="text-xs text-slate-400 mt-1">Image collection structure and documentation prepared for Milestone 2 & 3 ML model training</p>
        </div>
        <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-3 py-1.5 rounded-xl border border-emerald-500/20">
          <Sparkles className="w-4 h-4" /> ML Pipeline Ready
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {datasets.map((ds) => (
          <div key={ds.title} className={`glass-card p-6 rounded-2xl border ${ds.color} space-y-3`}>
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <Image className="w-5 h-5" /> {ds.title}
              </h3>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">{ds.desc}</p>

            <div className="glass-panel p-2.5 rounded-xl font-mono text-[11px] text-slate-300 flex items-center gap-2">
              <FolderTree className="w-4 h-4 text-slate-500 shrink-0" />
              <span>{ds.path}</span>
            </div>

            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1.5">Targeted Classes:</span>
              <div className="flex flex-wrap gap-1.5">
                {ds.classes.map(c => (
                  <span key={c} className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-900 border border-slate-700 text-slate-300">
                    {c}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <FileText className="w-4 h-4 text-cyan-400" /> Pipeline Specifications
        </h3>
        <ul className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-300">
          <li className="glass-panel p-4 rounded-xl">
            <strong className="text-white block mb-1">1. Acquisition & Storage</strong>
            Raw images stored under <code className="text-emerald-400">datasets/raw/</code>.
          </li>
          <li className="glass-panel p-4 rounded-xl">
            <strong className="text-white block mb-1">2. Preprocessing & Split</strong>
            Image normalization and 80/10/10 split manifests saved in <code className="text-teal-400">datasets/processed/</code>.
          </li>
          <li className="glass-panel p-4 rounded-xl">
            <strong className="text-white block mb-1">3. Model Training (M2 & M3)</strong>
            Freshness scoring & shelf-life prediction models trained without modifying core REST APIs.
          </li>
        </ul>
      </div>
    </div>
  );
};
