import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useNotification } from '../context/NotificationContext';
import { StatusBadge } from '../components/StatusBadge';
import { CATEGORIES } from '../utils/constants';
import { 
  Upload, 
  Image as ImageIcon, 
  Sparkles, 
  AlertTriangle, 
  CheckCircle2, 
  RefreshCw, 
  FileText, 
  Layers, 
  ShieldCheck, 
  Eye, 
  Trash2,
  PieChart,
  Check
} from 'lucide-react';

const SAMPLE_IMAGES = [
  {
    id: 'apple',
    name: 'Fresh Gala Apple',
    category: 'Fruits',
    badge: 'Fresh Target',
    badgeColor: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    url: '/sample_images/sample_fresh_apple.jpg',
    filename: 'fresh_gala_apple.jpg'
  },
  {
    id: 'avocado',
    name: 'Fresh Hass Avocado',
    category: 'Fruits',
    badge: 'Fresh Target',
    badgeColor: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    url: '/sample_images/sample_fresh_avocado.jpg',
    filename: 'fresh_hass_avocado.jpg'
  },
  {
    id: 'spoiled',
    name: 'Spoiled Produce (Browning/Mold)',
    category: 'Fruits',
    badge: 'Spoilage Target',
    badgeColor: 'bg-rose-500/20 text-rose-400 border-rose-500/30',
    url: '/sample_images/sample_spoiled_produce.jpg',
    filename: 'spoiled_produce.jpg'
  },
  {
    id: 'spinach',
    name: 'Fresh Spinach Leaves',
    category: 'Vegetables',
    badge: 'Fresh Target',
    badgeColor: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    url: '/sample_images/sample_fresh_spinach.jpg',
    filename: 'fresh_spinach_leaves.jpg'
  }
];

export const FreshnessAnalysisPage = ({ setActiveTab, onSelectReport }) => {
  const { addToast } = useNotification();
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [foodCategory, setFoodCategory] = useState('Fruits');
  const [selectedInventoryId, setSelectedInventoryId] = useState('');
  const [inventoryList, setInventoryList] = useState([]);
  
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [pastResults, setPastResults] = useState([]);
  const [activeSampleId, setActiveSampleId] = useState(null);

  useEffect(() => {
    const loadInventoryAndHistory = async () => {
      try {
        const [invData, resultsData] = await Promise.all([
          api.get('/inventory'),
          api.get('/freshness/results')
        ]);
        setInventoryList(invData);
        setPastResults(resultsData);
      } catch (err) {
        console.error('Error loading initial data:', err);
      }
    };
    loadInventoryAndHistory();
  }, []);

  const handleFileSelect = (file) => {
    if (!file) return;
    const allowed = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!allowed.includes(file.type)) {
      addToast('Unsupported file type. Please upload a JPG, PNG, or WEBP image.', 'error');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      addToast('File size exceeds 10MB limit.', 'error');
      return;
    }
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
    setActiveSampleId(null);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const loadSampleImage = async (sample) => {
    try {
      const res = await fetch(sample.url);
      const blob = await res.blob();
      const file = new File([blob], sample.filename, { type: 'image/jpeg' });
      
      setSelectedFile(file);
      setPreviewUrl(sample.url);
      setFoodCategory(sample.category);
      setResult(null);
      setActiveSampleId(sample.id);
      addToast(`Loaded preset sample: ${sample.name}`, 'info');
    } catch (err) {
      addToast('Failed to load sample image.', 'error');
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      addToast('Please select an image or click a 1-click sample food image.', 'warning');
      return;
    }

    setAnalyzing(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('food_category', foodCategory);
      if (selectedInventoryId) {
        formData.append('inventory_id', selectedInventoryId);
      }

      // Perform analysis request
      const token = localStorage.getItem('token');
      const response = await fetch('/api/freshness/analyze', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Analysis request failed.');
      }

      setResult(data);
      addToast('Food freshness analysis completed!', 'success');
      
      // Refresh past results list
      const updatedResults = await api.get('/freshness/results');
      setPastResults(updatedResults);
    } catch (err) {
      addToast(err.message || 'Analysis failed. Please try another image.', 'error');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setActiveSampleId(null);
  };

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Page Title Banner */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-purple-400" /> AI Food Image Analysis & Freshness Assessment
          </h2>
          <p className="text-xs text-slate-400 mt-1">Computer vision color degradation, texture variance, and spoilage indicator detection</p>
        </div>
        <span className="text-xs font-bold text-purple-300 bg-purple-500/10 px-3 py-1.5 rounded-xl border border-purple-500/20">
          Model: v1.0.0-CV (Active)
        </span>
      </div>

      {/* 1-Click Sample Test Food Images Bar */}
      <div className="glass-card p-5 rounded-2xl border border-slate-800 space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            📸 Quick 1-Click Sample Food Images to Identify Freshness
          </span>
          <span className="text-[10px] text-slate-400">Click any preset image to analyze instantly</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {SAMPLE_IMAGES.map((sample) => {
            const isSelected = activeSampleId === sample.id;
            return (
              <div
                key={sample.id}
                onClick={() => loadSampleImage(sample)}
                className={`glass-panel p-3 rounded-xl border cursor-pointer transition-all duration-200 flex flex-col items-center text-center space-y-2 group ${
                  isSelected
                    ? 'border-purple-500 bg-purple-950/30 ring-2 ring-purple-500/40'
                    : 'border-slate-800 hover:border-purple-500/40 bg-slate-900/40'
                }`}
              >
                <div className="relative w-full h-24 rounded-lg overflow-hidden border border-slate-700">
                  <img
                    src={sample.url}
                    alt={sample.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  {isSelected && (
                    <div className="absolute top-1.5 right-1.5 w-5 h-5 rounded-full bg-purple-500 text-white flex items-center justify-center shadow">
                      <Check className="w-3.5 h-3.5" />
                    </div>
                  )}
                </div>
                <div className="w-full">
                  <span className="text-xs font-bold text-white block truncate">{sample.name}</span>
                  <span className={`text-[9px] font-bold px-2 py-0.5 rounded border inline-block mt-1 ${sample.badgeColor}`}>
                    {sample.badge}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Upload & Form Column */}
        <div className="lg:col-span-5 space-y-6">
          <form onSubmit={handleAnalyze} className="glass-card p-6 rounded-2xl border border-slate-800 space-y-5">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Upload className="w-4 h-4 text-emerald-400" /> Upload or Selected Image
            </h3>

            {/* Dropzone */}
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-2xl p-6 text-center transition cursor-pointer relative overflow-hidden ${
                previewUrl ? 'border-emerald-500/50 bg-slate-900/60' : 'border-slate-700 hover:border-emerald-500/50 bg-slate-900/30'
              }`}
            >
              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
                className="absolute inset-0 opacity-0 cursor-pointer z-10"
              />

              {previewUrl ? (
                <div className="space-y-3">
                  <img
                    src={previewUrl}
                    alt="Food preview"
                    className="max-h-56 mx-auto rounded-xl object-contain border border-slate-700 shadow-md"
                  />
                  <p className="text-xs font-semibold text-emerald-400">{selectedFile?.name}</p>
                  <p className="text-[10px] text-slate-400">Click or drag a new image to replace</p>
                </div>
              ) : (
                <div className="space-y-3 py-4">
                  <div className="w-12 h-12 rounded-2xl bg-slate-800 text-emerald-400 flex items-center justify-center mx-auto border border-slate-700">
                    <ImageIcon className="w-6 h-6" />
                  </div>
                  <div>
                    <p className="text-xs font-bold text-white">Drag & drop your food image here</p>
                    <p className="text-[11px] text-slate-400 mt-1">Supports JPG, PNG, WEBP (Max 10MB)</p>
                  </div>
                </div>
              )}
            </div>

            {/* Food Category Selector */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1.5">Food Category *</label>
              <select
                value={foodCategory}
                onChange={(e) => setFoodCategory(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-white focus:border-emerald-500"
              >
                {CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            {/* Optional Inventory Batch Linker */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1.5">Link to Inventory Batch (Optional)</label>
              <select
                value={selectedInventoryId}
                onChange={(e) => setSelectedInventoryId(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-white focus:border-emerald-500"
              >
                <option value="">-- Standalone Analysis (No Batch Link) --</option>
                {inventoryList.map((inv) => (
                  <option key={inv.id} value={inv.id}>
                    {inv.batch_number} - {inv.food_item?.name} ({inv.quantity} {inv.unit})
                  </option>
                ))}
              </select>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-3 pt-2">
              {selectedFile && (
                <button
                  type="button"
                  onClick={handleReset}
                  className="px-4 py-3 rounded-xl text-xs font-bold text-slate-400 hover:text-white bg-slate-800 transition"
                >
                  Clear
                </button>
              )}
              <button
                type="submit"
                disabled={analyzing || !selectedFile}
                className={`flex-1 py-3 rounded-xl text-xs font-bold text-white transition flex items-center justify-center gap-2 shadow-lg ${
                  analyzing || !selectedFile
                    ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                    : 'bg-gradient-to-r from-purple-600 to-emerald-600 hover:from-purple-500 hover:to-emerald-500 shadow-purple-500/20'
                }`}
              >
                {analyzing ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" /> Analyzing Image Pixels...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" /> Run Freshness Analysis
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Results Column */}
        <div className="lg:col-span-7 space-y-6">
          {result ? (
            <div className="glass-card p-6 rounded-2xl border border-purple-500/30 space-y-6 animate-fade-in">
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-purple-400">Analysis Result</span>
                  <h3 className="text-xl font-extrabold text-white">{result.food_category} Assessment</h3>
                </div>
                <StatusBadge status={result.predicted_category} />
              </div>

              {/* Top Score Gauge Cards Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="glass-panel p-4 rounded-xl text-center border border-emerald-500/30 bg-emerald-950/20">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Freshness Score</span>
                  <div className="text-3xl font-black text-emerald-400">{result.freshness_score} / 100</div>
                  <span className="text-[10px] text-slate-400 mt-1 block">AI composite score</span>
                </div>

                <div className="glass-panel p-4 rounded-xl text-center border border-purple-500/30 bg-purple-950/20">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Model Confidence</span>
                  <div className="text-3xl font-black text-purple-300">{(result.confidence * 100).toFixed(1)}%</div>
                  <span className="text-[10px] text-slate-400 mt-1 block">Classification certainty</span>
                </div>

                <div className="glass-panel p-4 rounded-xl text-center border border-amber-500/30 bg-amber-950/20">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Spoilage Probability</span>
                  <div className="text-3xl font-black text-amber-400">{(result.spoilage_probability * 100).toFixed(1)}%</div>
                  <span className="text-[10px] text-slate-400 mt-1 block">P(Near Spoilage + Spoiled)</span>
                </div>
              </div>

              {/* Color Analysis */}
              <div className="glass-panel p-4 rounded-xl border border-slate-800 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-white uppercase tracking-wider flex items-center gap-2">
                    🎨 Color & Browning Analysis
                  </span>
                  <span className="text-amber-400 font-semibold">
                    Score: {(result.color_analysis.color_degradation_score * 100).toFixed(0)}% Degradation
                  </span>
                </div>
                <div className="text-slate-300 space-y-1 pl-2 border-l-2 border-amber-500/40">
                  <p>• Browning Index: <span className="font-bold text-white">{result.color_analysis.browning_index}</span></p>
                  <p>• Discolored Area: <span className="font-bold text-white">{(result.color_analysis.discolored_pixel_ratio * 100).toFixed(1)}%</span> of surface</p>
                  {result.color_analysis.observations?.map((obs, idx) => (
                    <p key={idx} className="text-slate-400">• {obs}</p>
                  ))}
                </div>
              </div>

              {/* Texture Analysis */}
              <div className="glass-panel p-4 rounded-xl border border-slate-800 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-white uppercase tracking-wider flex items-center gap-2">
                    🔬 Surface Texture Analysis
                  </span>
                  <span className="text-cyan-400 font-semibold">
                    Score: {(result.texture_analysis.texture_score * 100).toFixed(0)}% Roughness
                  </span>
                </div>
                <div className="text-slate-300 space-y-1 pl-2 border-l-2 border-cyan-500/40">
                  <p>• Local Homogeneity: <span className="font-bold text-white">{result.texture_analysis.homogeneity}</span></p>
                  <p>• Gradient Variance: <span className="font-bold text-white">{result.texture_analysis.gradient_variance}</span></p>
                  {result.texture_analysis.observations?.map((obs, idx) => (
                    <p key={idx} className="text-slate-400">• {obs}</p>
                  ))}
                </div>
              </div>

              {/* Spoilage Indicators */}
              <div className="glass-panel p-4 rounded-xl border border-slate-800 space-y-3 text-xs">
                <span className="font-bold text-white uppercase tracking-wider block">
                  🔍 Visual Spoilage Indicators
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {Object.entries(result.spoilage_indicators || {}).map(([key, ind]) => (
                    <div key={key} className={`p-3 rounded-xl border ${ind.detected ? 'border-rose-500/40 bg-rose-950/20' : 'border-slate-800 bg-slate-900/40'}`}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-bold text-white capitalize">{key.replace('_', ' ')}</span>
                        {ind.detected ? (
                          <span className="text-[10px] font-bold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded">Detected</span>
                        ) : (
                          <span className="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">Clear</span>
                        )}
                      </div>
                      <p className="text-[11px] text-slate-400 leading-snug">{ind.evidence}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-2">
                <button
                  onClick={() => onSelectReport(result)}
                  className="px-5 py-2.5 rounded-xl font-bold text-xs text-white bg-purple-600 hover:bg-purple-500 transition flex items-center gap-2"
                >
                  <FileText className="w-4 h-4" /> View Formal Inspection Report
                </button>
                <button
                  onClick={handleReset}
                  className="px-4 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:text-white bg-slate-800 transition"
                >
                  Analyze Another Image
                </button>
              </div>
            </div>
          ) : (
            /* Recent History List */
            <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <PieChart className="w-4 h-4 text-emerald-400" /> Recent Image Analysis History
              </h3>

              <div className="space-y-3">
                {pastResults.length > 0 ? (
                  pastResults.slice(0, 5).map((r) => (
                    <div key={r.id} className="glass-panel p-4 rounded-xl border border-slate-800 flex items-center justify-between gap-4 hover:border-purple-500/40 transition">
                      <div className="flex items-center gap-3">
                        <img
                          src={r.image_path}
                          alt="Analyzed food"
                          className="w-12 h-12 rounded-lg object-cover border border-slate-700"
                        />
                        <div>
                          <div className="font-bold text-white text-xs">{r.food_category} Assessment</div>
                          <div className="text-[10px] text-slate-400">{new Date(r.created_at).toLocaleString()}</div>
                        </div>
                      </div>

                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <div className="text-xs font-black text-emerald-400">{r.freshness_score} / 100</div>
                          <div className="text-[10px] text-slate-400">Score</div>
                        </div>
                        <StatusBadge status={r.predicted_category} />
                        <button
                          onClick={() => onSelectReport(r)}
                          className="p-2 rounded-lg text-slate-400 hover:text-purple-400 hover:bg-purple-500/10 transition"
                          title="View Report"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="py-12 text-center text-slate-500 text-xs">
                    No image analysis records yet. Click a sample food image above or upload an image!
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
