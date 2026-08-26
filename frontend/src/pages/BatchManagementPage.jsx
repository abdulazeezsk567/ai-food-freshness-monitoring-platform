import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';
import { Layers, Thermometer, Droplets, Box, Clock, ShieldCheck } from 'lucide-react';

export const BatchManagementPage = () => {
  const [batches, setBatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadBatches = async () => {
      try {
        const data = await api.get('/inventory');
        setBatches(data);
      } catch (err) {
        console.error('Failed to load batch telemetry:', err);
      } finally {
        setLoading(false);
      }
    };
    loadBatches();
  }, []);

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
            <Layers className="w-6 h-6 text-teal-400" /> Batch Telemetry & Storage Telematics
          </h2>
          <p className="text-xs text-slate-400 mt-1">Environmental telemetry monitoring and cold-chain compliance</p>
        </div>
        <div className="flex items-center gap-2 text-xs font-semibold text-teal-400 bg-teal-500/10 px-3 py-1.5 rounded-xl border border-teal-500/20">
          <ShieldCheck className="w-4 h-4" /> Cold Chain Verified
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
          <div className="col-span-full py-12 text-center text-slate-400">Loading batch telematics...</div>
        ) : batches.length > 0 ? (
          batches.map((b) => (
            <div key={b.id} className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4 hover:border-teal-500/30 transition">
              <div className="flex items-center justify-between">
                <span className="font-mono text-sm font-bold text-teal-400">{b.batch_number}</span>
                <StatusBadge status={b.status} />
              </div>

              <div>
                <h3 className="text-lg font-bold text-white">{b.food_item?.name}</h3>
                <p className="text-xs text-slate-400">{b.food_item?.category}</p>
              </div>

              <div className="grid grid-cols-2 gap-3 pt-2">
                <div className="glass-panel p-3 rounded-xl">
                  <div className="flex items-center gap-1.5 text-xs text-amber-400 font-semibold mb-1">
                    <Thermometer className="w-4 h-4" /> Temperature
                  </div>
                  <div className="text-xl font-extrabold text-white">{b.storage_temperature} °C</div>
                </div>

                <div className="glass-panel p-3 rounded-xl">
                  <div className="flex items-center gap-1.5 text-xs text-cyan-400 font-semibold mb-1">
                    <Droplets className="w-4 h-4" /> Humidity
                  </div>
                  <div className="text-xl font-extrabold text-white">{b.storage_humidity} %</div>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800 text-xs text-slate-400 space-y-1.5">
                <div className="flex justify-between">
                  <span>Packaging:</span>
                  <span className="font-medium text-slate-200">{b.packaging_type}</span>
                </div>
                <div className="flex justify-between">
                  <span>Storage Duration:</span>
                  <span className="font-medium text-slate-200">{b.storage_duration} days</span>
                </div>
                <div className="flex justify-between">
                  <span>Expiry Date:</span>
                  <span className="font-medium text-slate-200">{b.expiry_date}</span>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full py-12 text-center text-slate-500">No active batches recorded.</div>
        )}
      </div>
    </div>
  );
};
