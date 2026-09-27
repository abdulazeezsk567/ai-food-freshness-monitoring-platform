import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useNotification } from '../context/NotificationContext';
import { StatusBadge } from '../components/StatusBadge';
import { 
  Clock, 
  Calendar, 
  AlertTriangle, 
  ShieldCheck, 
  Thermometer, 
  Droplets, 
  Package, 
  Activity, 
  CheckCircle, 
  RefreshCw, 
  TrendingUp, 
  TrendingDown, 
  Minus,
  Sparkles,
  MapPin,
  FileText
} from 'lucide-react';

export const ShelfLifePage = ({ initialInventoryId = null }) => {
  const { addToast } = useNotification();
  const [inventoryList, setInventoryList] = useState([]);
  const [selectedInventoryId, setSelectedInventoryId] = useState(initialInventoryId || '');
  const [loading, setLoading] = useState(false);
  
  const [prediction, setPrediction] = useState(null);
  const [predictionHistory, setPredictionHistory] = useState([]);

  // Storage Condition Form State
  const [storageForm, setStorageForm] = useState({
    temperature: 4.0,
    humidity: 85.0,
    storage_location: 'Cold Room A',
    packaging_type: 'Standard Packaging',
    storage_condition: 'Refrigerated',
    storage_duration_days: 1,
    notes: ''
  });
  const [savingStorage, setSavingStorage] = useState(false);

  useEffect(() => {
    const loadInventory = async () => {
      try {
        const data = await api.get('/inventory');
        setInventoryList(data);
        if (!selectedInventoryId && data.length > 0) {
          setSelectedInventoryId(data[0].id);
        }
      } catch (err) {
        addToast(err.message || 'Failed to load inventory items', 'error');
      }
    };
    loadInventory();
  }, []);

  useEffect(() => {
    if (!selectedInventoryId) return;
    fetchPredictionAndStorage(selectedInventoryId);
  }, [selectedInventoryId]);

  const fetchPredictionAndStorage = async (invId) => {
    setLoading(true);
    try {
      const [predData, histData, storageData] = await Promise.all([
        api.get(`/shelf-life/${invId}`),
        api.get(`/shelf-life/${invId}/history`),
        api.get(`/storage-conditions/${invId}`)
      ]);

      setPrediction(predData);
      setPredictionHistory(histData);

      if (storageData) {
        setStorageForm({
          temperature: storageData.temperature,
          humidity: storageData.humidity,
          storage_location: storageData.storage_location,
          packaging_type: storageData.packaging_type,
          storage_condition: storageData.storage_condition,
          storage_duration_days: storageData.storage_duration_days,
          notes: storageData.notes || ''
        });
      }
    } catch (err) {
      addToast(err.message || 'Failed to fetch shelf life prediction', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleStorageSubmit = async (e) => {
    e.preventDefault();
    if (!selectedInventoryId) return;

    setSavingStorage(true);
    try {
      await api.post('/storage-conditions', {
        inventory_id: parseInt(selectedInventoryId),
        ...storageForm
      });

      addToast('Storage conditions updated! Recalculating shelf-life forecast...', 'success');

      // Re-run shelf life prediction with updated storage conditions
      const updatedPred = await api.post('/shelf-life/predict', {
        inventory_id: parseInt(selectedInventoryId)
      });

      setPrediction(updatedPred);
      const updatedHist = await api.get(`/shelf-life/${selectedInventoryId}/history`);
      setPredictionHistory(updatedHist);
    } catch (err) {
      addToast(err.message || 'Failed to update storage conditions', 'error');
    } finally {
      setSavingStorage(false);
    }
  };

  const selectedItem = inventoryList.find(i => i.id === parseInt(selectedInventoryId));

  const getRiskBadgeColor = (risk) => {
    switch (risk) {
      case 'CRITICAL': return 'bg-rose-500/20 text-rose-400 border-rose-500/40';
      case 'HIGH RISK': return 'bg-amber-500/20 text-amber-400 border-amber-500/40';
      case 'MEDIUM RISK': return 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40';
      default: return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40';
    }
  };

  const getTrendIcon = (trend) => {
    if (trend === 'Improving') return <TrendingUp className="w-4 h-4 text-emerald-400" />;
    if (trend === 'Declining') return <TrendingDown className="w-4 h-4 text-rose-400" />;
    if (trend === 'Stable') return <Minus className="w-4 h-4 text-cyan-400" />;
    return <Activity className="w-4 h-4 text-slate-400" />;
  };

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Title Banner */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
            <Clock className="w-6 h-6 text-emerald-400" /> Predictive Shelf-Life Monitoring
          </h2>
          <p className="text-xs text-slate-400 mt-1">Multi-factor expiration forecasting based on visual freshness score, storage temperature, humidity, and degradation trends</p>
        </div>
        <span className="text-xs font-bold text-emerald-300 bg-emerald-500/10 px-3 py-1.5 rounded-xl border border-emerald-500/20">
          Model: shelf-life-baseline-v1 (Active)
        </span>
      </div>

      {/* Inventory Selector Bar */}
      <div className="glass-card p-5 rounded-2xl border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="w-full md:w-auto">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1">
            Select Inventory Batch *
          </label>
          <select
            value={selectedInventoryId}
            onChange={(e) => setSelectedInventoryId(e.target.value)}
            className="w-full md:w-96 bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-white focus:border-emerald-500 font-medium"
          >
            {inventoryList.map((item) => (
              <option key={item.id} value={item.id}>
                {item.batch_number} — {item.food_item?.name} ({item.quantity} {item.unit})
              </option>
            ))}
          </select>
        </div>

        {selectedItem && (
          <div className="flex items-center gap-4 text-xs text-slate-300 bg-slate-900/60 p-3 rounded-xl border border-slate-800 w-full md:w-auto justify-between">
            <div>
              <span className="text-slate-500 block text-[10px] uppercase font-bold">Category</span>
              <span className="font-bold text-white">{selectedItem.food_item?.category}</span>
            </div>
            <div className="border-l border-slate-800 pl-4">
              <span className="text-slate-500 block text-[10px] uppercase font-bold">Current Status</span>
              <StatusBadge status={selectedItem.status} />
            </div>
          </div>
        )}
      </div>

      {loading ? (
        <div className="py-16 text-center text-slate-400 glass-card rounded-2xl border border-slate-800">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto text-emerald-400 mb-3" />
          Calculating predictive shelf-life metrics...
        </div>
      ) : prediction ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Main Forecast Metrics & Analysis */}
          <div className="lg:col-span-7 space-y-6">
            
            {/* Top Gauges Grid */}
            <div className="glass-card p-6 rounded-2xl border border-emerald-500/30 space-y-6">
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400">Shelf-Life Forecast</span>
                  <h3 className="text-xl font-black text-white">{selectedItem?.food_item?.name || 'Item'} Expiration Forecast</h3>
                </div>
                <span className={`px-3 py-1 rounded-xl text-xs font-bold border ${getRiskBadgeColor(prediction.risk_level)}`}>
                  {prediction.risk_level}
                </span>
              </div>

              {/* 4 Score Cards */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="glass-panel p-4 rounded-xl text-center border border-emerald-500/30 bg-emerald-950/20">
                  <span className="text-[10px] font-bold uppercase text-slate-400 block mb-1">Estimated Remaining</span>
                  <div className="text-3xl font-black text-emerald-400">{prediction.estimated_remaining_days} <span className="text-sm font-bold">Days</span></div>
                </div>

                <div className="glass-panel p-4 rounded-xl text-center border border-cyan-500/30 bg-cyan-950/20">
                  <span className="text-[10px] font-bold uppercase text-slate-400 block mb-1">Estimated Expiry</span>
                  <div className="text-sm font-extrabold text-cyan-300 mt-2">{prediction.estimated_expiry_date}</div>
                  <span className="text-[9px] text-slate-400 block mt-1">AI Model Estimate</span>
                </div>

                <div className="glass-panel p-4 rounded-xl text-center border border-purple-500/30 bg-purple-950/20">
                  <span className="text-[10px] font-bold uppercase text-slate-400 block mb-1">Degradation Trend</span>
                  <div className="text-xs font-extrabold text-purple-300 mt-2 flex items-center justify-center gap-1">
                    {getTrendIcon(prediction.trend)} {prediction.trend}
                  </div>
                </div>

                <div className="glass-panel p-4 rounded-xl text-center border border-amber-500/30 bg-amber-950/20">
                  <span className="text-[10px] font-bold uppercase text-slate-400 block mb-1">Model Certainty</span>
                  <div className="text-3xl font-black text-amber-300">{(prediction.confidence * 100).toFixed(0)}%</div>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-[11px] text-slate-400 leading-snug">
                ⚠️ <span className="font-semibold text-slate-300">Important Disclaimer:</span> Estimated remaining shelf life and expiry dates are AI/model-based predictions derived from input features and environmental conditions. They do not constitute guaranteed food-safety certifications.
              </div>
            </div>

            {/* Storage Impact Analysis */}
            <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3 text-xs">
              <h3 className="font-bold text-white uppercase tracking-wider flex items-center gap-2">
                🌡️ Storage Condition Impact Analysis
              </h3>
              <div className="space-y-2 text-slate-300">
                {prediction.storage_impact?.observations?.map((obs, idx) => (
                  <div key={idx} className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 text-slate-300 flex items-start gap-2">
                    <span className="text-emerald-400 font-bold">•</span>
                    <span>{obs}</span>
                  </div>
                ))}
              </div>

              {/* Factors Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 text-center text-[11px]">
                <div className="p-2 rounded-lg bg-slate-900 border border-slate-800">
                  <span className="text-slate-500 block">Temp Factor</span>
                  <span className="font-bold text-white">{prediction.storage_impact?.temperature_factor}x</span>
                </div>
                <div className="p-2 rounded-lg bg-slate-900 border border-slate-800">
                  <span className="text-slate-500 block">Humidity Factor</span>
                  <span className="font-bold text-white">{prediction.storage_impact?.humidity_factor}x</span>
                </div>
                <div className="p-2 rounded-lg bg-slate-900 border border-slate-800">
                  <span className="text-slate-500 block">Packaging Factor</span>
                  <span className="font-bold text-white">{prediction.storage_impact?.packaging_factor}x</span>
                </div>
                <div className="p-2 rounded-lg bg-slate-900 border border-slate-800">
                  <span className="text-slate-500 block">Condition Factor</span>
                  <span className="font-bold text-white">{prediction.storage_impact?.condition_factor}x</span>
                </div>
              </div>
            </div>

            {/* Storage Guidance Recommendations */}
            <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3 text-xs">
              <h3 className="font-bold text-white uppercase tracking-wider flex items-center gap-2">
                📋 Basic Storage Guidance & Action Items
              </h3>
              <div className="space-y-2">
                {prediction.storage_guidance?.map((item, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-emerald-300 flex items-center gap-2.5">
                    <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Prediction History Table */}
            <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3 text-xs">
              <h3 className="font-bold text-white uppercase tracking-wider flex items-center gap-2">
                📜 Prediction History Log
              </h3>
              <div className="space-y-2">
                {predictionHistory.length > 0 ? (
                  predictionHistory.map((p) => (
                    <div key={p.id} className="p-3 rounded-xl border border-slate-800 bg-slate-900/40 flex items-center justify-between gap-3">
                      <div>
                        <span className="font-bold text-white">{p.estimated_remaining_days} Remaining Days</span>
                        <span className="text-[10px] text-slate-400 block">Expiry: {p.estimated_expiry_date} ({new Date(p.created_at).toLocaleDateString()})</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${getRiskBadgeColor(p.risk_level)}`}>
                          {p.risk_level}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="py-6 text-center text-slate-500">No historical prediction logs recorded yet.</div>
                )}
              </div>
            </div>

          </div>

          {/* Storage Telemetry Input Form Column */}
          <div className="lg:col-span-5 space-y-6">
            <form onSubmit={handleStorageSubmit} className="glass-card p-6 rounded-2xl border border-slate-800 space-y-5">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Thermometer className="w-4 h-4 text-cyan-400" /> Log Storage Telemetry
              </h3>

              {/* Temperature */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1.5">
                  Storage Temperature (°C) *
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={storageForm.temperature}
                  onChange={(e) => setStorageForm({ ...storageForm, temperature: parseFloat(e.target.value) })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-white focus:border-emerald-500"
                  required
                />
              </div>

              {/* Humidity */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1.5">
                  Relative Humidity (%) *
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={storageForm.humidity}
                  onChange={(e) => setStorageForm({ ...storageForm, humidity: parseFloat(e.target.value) })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-white focus:border-emerald-500"
                  required
                />
              </div>

              {/* Storage Condition */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1.5">
                  Storage Condition Environment *
                </label>
                <select
                  value={storageForm.storage_condition}
                  onChange={(e) => setStorageForm({ ...storageForm, storage_condition: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-white focus:border-emerald-500"
                >
                  <option value="Refrigerated">Refrigerated Cold-Chain</option>
                  <option value="Frozen">Deep Frozen</option>
                  <option value="Room Temperature">Room Temperature</option>
                  <option value="Controlled Storage">Controlled Atmosphere Storage</option>
                  <option value="Unknown">Unknown / Ambient</option>
                </select>
              </div>

              {/* Storage Location */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1.5">
                  Storage Location
                </label>
                <input
                  type="text"
                  value={storageForm.storage_location}
                  onChange={(e) => setStorageForm({ ...storageForm, storage_location: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-white focus:border-emerald-500"
                  placeholder="e.g. Cold Vault 2"
                />
              </div>

              {/* Packaging Type */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1.5">
                  Packaging Format
                </label>
                <select
                  value={storageForm.packaging_type}
                  onChange={(e) => setStorageForm({ ...storageForm, packaging_type: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-white focus:border-emerald-500"
                >
                  <option value="Standard Packaging">Standard Packaging</option>
                  <option value="Vacuum Sealed">Vacuum Sealed</option>
                  <option value="Aseptic Packaging">Aseptic Packaging</option>
                  <option value="Modified Atmosphere Packaging (MAP)">Modified Atmosphere Packaging (MAP)</option>
                  <option value="Plastic Tray with Film">Plastic Tray with Film</option>
                  <option value="Paper Wrapping">Paper Wrapping</option>
                  <option value="Unpackaged / Loose">Unpackaged / Loose</option>
                </select>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={savingStorage}
                className="w-full py-3 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 shadow-lg shadow-emerald-500/20 transition flex items-center justify-center gap-2"
              >
                {savingStorage ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" /> Recalculating Shelf-Life...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" /> Save Telemetry & Recalculate Forecast
                  </>
                )}
              </button>
            </form>
          </div>

        </div>
      ) : (
        <div className="py-16 text-center text-slate-500 text-xs glass-card rounded-2xl border border-slate-800">
          No inventory item selected. Please choose a batch above.
        </div>
      )}
    </div>
  );
};
