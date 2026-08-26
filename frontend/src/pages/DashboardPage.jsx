import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { StatCard } from '../components/StatCard';
import { StatusBadge } from '../components/StatusBadge';
import { 
  Package, 
  Layers, 
  Clock, 
  AlertOctagon, 
  CheckCircle2, 
  AlertTriangle, 
  Thermometer, 
  Droplets, 
  Cpu, 
  Sparkles, 
  ArrowUpRight 
} from 'lucide-react';

export const DashboardPage = ({ setActiveTab }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await api.get('/stats/dashboard');
        setStats(data);
      } catch (err) {
        console.error('Failed to load dashboard metrics:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-emerald-500" />
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-6 rounded-2xl border border-slate-800">
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight">Platform Dashboard Overview</h2>
          <p className="text-xs text-slate-400 mt-1">Real-time telemetry and inventory freshness tracking</p>
        </div>
        <button
          onClick={() => setActiveTab('add-item')}
          className="px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 shadow-lg shadow-emerald-500/20 transition self-start sm:self-auto"
        >
          + Add Food Batch
        </button>
      </div>

      {/* 6 Metric Stat Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <StatCard
          title="Total Food Items"
          value={stats?.total_food_items || 0}
          icon={Package}
          color="text-emerald-400 bg-emerald-500"
        />
        <StatCard
          title="Active Batches"
          value={stats?.active_batches || 0}
          icon={Layers}
          color="text-teal-400 bg-teal-500"
        />
        <StatCard
          title="Expiring Soon"
          value={stats?.expiring_soon || 0}
          icon={Clock}
          color="text-amber-400 bg-amber-500"
        />
        <StatCard
          title="Expired Items"
          value={stats?.expired_items || 0}
          icon={AlertOctagon}
          color="text-rose-400 bg-rose-500"
        />
        <StatCard
          title="Fresh Items"
          value={stats?.fresh_items || 0}
          icon={CheckCircle2}
          color="text-emerald-300 bg-emerald-400"
        />
        <StatCard
          title="Near Spoilage"
          value={stats?.near_spoilage || 0}
          icon={AlertTriangle}
          color="text-orange-400 bg-orange-500"
        />
      </div>

      {/* Main Grid: Storage Telemetry & AI Placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Storage Telemetry Summary */}
        <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Thermometer className="w-4 h-4 text-emerald-400" /> Facility Telemetry
            </h3>
            <span className="text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
              Live Feed
            </span>
          </div>

          <div className="grid grid-cols-2 gap-4 pt-2">
            <div className="glass-panel p-4 rounded-xl text-center">
              <Thermometer className="w-6 h-6 text-amber-400 mx-auto mb-1" />
              <div className="text-2xl font-black text-white">3.8 °C</div>
              <p className="text-[11px] text-slate-400 font-medium">Avg Temp (Target: 4°C)</p>
            </div>

            <div className="glass-panel p-4 rounded-xl text-center">
              <Droplets className="w-6 h-6 text-cyan-400 mx-auto mb-1" />
              <div className="text-2xl font-black text-white">84.2 %</div>
              <p className="text-[11px] text-slate-400 font-medium">Avg Humidity (85%)</p>
            </div>
          </div>

          <div className="text-xs text-slate-400 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
            <span className="font-semibold text-slate-200">Optimal Storage Conditions:</span> Cold storage facility metrics are within standard food safety tolerances.
          </div>
        </div>

        {/* Future AI Freshness Assessment Stub (Clearly Marked) */}
        <div className="lg:col-span-2 glass-card p-6 rounded-2xl border border-purple-500/30 bg-purple-950/10 relative overflow-hidden flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Cpu className="w-5 h-5 text-purple-400" />
                <h3 className="text-sm font-extrabold text-white uppercase tracking-wider">AI Freshness Engine</h3>
              </div>
              <span className="text-[11px] font-bold text-purple-300 bg-purple-500/20 px-2.5 py-1 rounded-full border border-purple-500/30 flex items-center gap-1">
                <Sparkles className="w-3 h-3" /> Scheduled for Milestone 2 & 3
              </span>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed mb-4">
              Future releases will process captured food images alongside storage temperature, relative humidity, packaging type, and storage duration to run real-time spoilage classification & remaining shelf-life prediction models.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="p-3 rounded-xl bg-purple-900/20 border border-purple-500/20 text-center">
                <div className="text-xs font-bold text-purple-300">Vision Analysis</div>
                <p className="text-[10px] text-slate-400 mt-1">Rotten vs Fresh Fruit/Veg Classification</p>
              </div>
              <div className="p-3 rounded-xl bg-purple-900/20 border border-purple-500/20 text-center">
                <div className="text-xs font-bold text-purple-300">Predictive Model</div>
                <p className="text-[10px] text-slate-400 mt-1">Remaining Shelf Life (Days Prediction)</p>
              </div>
              <div className="p-3 rounded-xl bg-purple-900/20 border border-purple-500/20 text-center">
                <div className="text-xs font-bold text-purple-300">Smart Advice</div>
                <p className="text-[10px] text-slate-400 mt-1">Storage Temperature Recommendations</p>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-purple-500/20 flex items-center justify-between text-xs text-purple-300/80">
            <span>Datasets initialized in <code className="text-purple-200">datasets/raw/</code></span>
            <button onClick={() => setActiveTab('datasets')} className="hover:underline flex items-center gap-1 font-semibold">
              Explore Datasets <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Inventory Overview Table */}
      <div className="glass-card rounded-2xl border border-slate-800 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-white">Recent Inventory Batches</h3>
          <button
            onClick={() => setActiveTab('inventory')}
            className="text-xs font-semibold text-emerald-400 hover:underline flex items-center gap-1"
          >
            View All Inventory ({stats?.active_batches || 0}) <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-[11px] font-bold uppercase tracking-wider text-slate-400">
                <th className="py-3 px-4">Batch Number</th>
                <th className="py-3 px-4">Food Item</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Quantity</th>
                <th className="py-3 px-4">Expiry Date</th>
                <th className="py-3 px-4">Freshness Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs">
              {stats?.recent_activity?.length > 0 ? (
                stats.recent_activity.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-3.5 px-4 font-mono text-slate-300">{item.batch_number}</td>
                    <td className="py-3.5 px-4 font-bold text-white">{item.item_name}</td>
                    <td className="py-3.5 px-4 text-slate-400">{item.category}</td>
                    <td className="py-3.5 px-4 text-slate-300 font-medium">{item.quantity}</td>
                    <td className="py-3.5 px-4 text-slate-300">{item.expiry_date}</td>
                    <td className="py-3.5 px-4">
                      <StatusBadge status={item.status} />
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-slate-500">
                    No inventory recorded yet. Add your first food batch!
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
