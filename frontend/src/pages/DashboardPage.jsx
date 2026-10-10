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
  ArrowUpRight,
  ShieldCheck,
  TrendingDown,
  Activity,
  FileSpreadsheet,
  Camera
} from 'lucide-react';

export const DashboardPage = ({ setActiveTab, onNavigateShelfLife }) => {
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

  const facility = stats?.facility_telemetry || {
    avg_temperature: 4.0,
    avg_humidity: 85.0,
    temp_alert_count: 0,
    humidity_alert_count: 0,
    active_monitored_batches: stats?.active_batches || 0
  };

  const shelfLife = stats?.shelf_life_analytics || {
    risk_distribution: { "CRITICAL": 0, "HIGH RISK": 0, "MEDIUM RISK": 0, "LOW RISK": 0 },
    avg_remaining_days: 0.0,
    total_predictions: 0
  };

  const freshness = stats?.freshness_analytics || {
    total_analyses: 0,
    avg_freshness_score: 0.0,
    classification_distribution: {}
  };

  const alerts = stats?.spoilage_alerts || [];

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-6 rounded-2xl border border-slate-800">
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
            Platform Dashboard & Analytics
          </h2>
          <p className="text-xs text-slate-400 mt-1">Real-time facility telemetry, predictive shelf-life forecasting, and visual freshness audits</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => setActiveTab('freshness-analysis')}
            className="px-4 py-2.5 rounded-xl text-xs font-bold text-slate-200 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 transition flex items-center gap-2"
          >
            <Camera className="w-4 h-4 text-purple-400" /> Freshness Scan
          </button>
          <button
            onClick={() => setActiveTab('add-item')}
            className="px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 shadow-lg shadow-emerald-500/20 transition"
          >
            + Add Food Batch
          </button>
        </div>
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
          title="Expired / Spoiled"
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

      {/* Analytics Grid: Real Telemetry, Shelf-Life Risk Distribution & CV Freshness Engine */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* 1. Real Storage Telemetry Summary */}
        <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Thermometer className="w-4 h-4 text-emerald-400" /> Facility Telemetry
            </h3>
            {facility.temp_alert_count > 0 ? (
              <span className="text-[10px] font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                {facility.temp_alert_count} Alerts
              </span>
            ) : (
              <span className="text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                Optimal
              </span>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4 pt-1">
            <div className="glass-panel p-4 rounded-xl text-center">
              <Thermometer className="w-6 h-6 text-amber-400 mx-auto mb-1" />
              <div className="text-2xl font-black text-white">{facility.avg_temperature} °C</div>
              <p className="text-[11px] text-slate-400 font-medium">Mean Storage Temp</p>
            </div>

            <div className="glass-panel p-4 rounded-xl text-center">
              <Droplets className="w-6 h-6 text-cyan-400 mx-auto mb-1" />
              <div className="text-2xl font-black text-white">{facility.avg_humidity} %</div>
              <p className="text-[11px] text-slate-400 font-medium">Mean Relative Humidity</p>
            </div>
          </div>

          <div className="text-xs text-slate-400 bg-slate-900/60 p-3 rounded-xl border border-slate-800 space-y-1">
            <div className="flex justify-between">
              <span>Monitored Batches:</span>
              <span className="font-bold text-white">{facility.active_monitored_batches} batches</span>
            </div>
            <div className="flex justify-between">
              <span>Thermal Breaches:</span>
              <span className={facility.temp_alert_count > 0 ? "font-bold text-amber-400" : "font-bold text-emerald-400"}>
                {facility.temp_alert_count} logged
              </span>
            </div>
          </div>
        </div>

        {/* 2. Shelf-Life Risk Distribution (shelf-life-baseline-v1) */}
        <div className="glass-card p-6 rounded-2xl border border-cyan-500/30 bg-cyan-950/10 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">Shelf-Life Risk Tiers</h3>
            </div>
            <span className="text-[10px] font-bold text-cyan-300 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">
              shelf-life-baseline-v1
            </span>
          </div>

          <div className="glass-panel p-3 rounded-xl flex items-center justify-between">
            <span className="text-xs text-slate-300">Mean Remaining Shelf Life:</span>
            <span className="text-lg font-black text-cyan-300">{shelfLife.avg_remaining_days} Days</span>
          </div>

          {/* 4 Risk Distribution Progress / Counters */}
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="p-2.5 rounded-lg bg-slate-900/80 border border-rose-500/30 flex justify-between items-center">
              <span className="text-rose-400 font-bold">CRITICAL:</span>
              <span className="font-black text-white">{shelfLife.risk_distribution["CRITICAL"] || 0}</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-900/80 border border-amber-500/30 flex justify-between items-center">
              <span className="text-amber-400 font-bold">HIGH RISK:</span>
              <span className="font-black text-white">{shelfLife.risk_distribution["HIGH RISK"] || 0}</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-900/80 border border-yellow-500/30 flex justify-between items-center">
              <span className="text-yellow-300 font-bold">MEDIUM:</span>
              <span className="font-black text-white">{shelfLife.risk_distribution["MEDIUM RISK"] || 0}</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-900/80 border border-emerald-500/30 flex justify-between items-center">
              <span className="text-emerald-400 font-bold">LOW RISK:</span>
              <span className="font-black text-white">{shelfLife.risk_distribution["LOW RISK"] || 0}</span>
            </div>
          </div>

          <button
            onClick={() => setActiveTab('shelf-life')}
            className="w-full py-2.5 rounded-xl text-xs font-bold text-cyan-300 bg-cyan-950/40 hover:bg-cyan-900/40 border border-cyan-500/30 transition flex items-center justify-center gap-1.5"
          >
            Launch Predictive Shelf-Life Inspector <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* 3. Computer Vision Freshness Engine Analytics */}
        <div className="glass-card p-6 rounded-2xl border border-purple-500/30 bg-purple-950/10 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-400" />
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">Vision Freshness Index</h3>
            </div>
            <span className="text-[10px] font-bold text-purple-300 bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20">
              Active CV Pipeline
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="glass-panel p-3 rounded-xl text-center">
              <span className="text-[10px] text-slate-400 font-bold uppercase block mb-1">Mean Score</span>
              <span className="text-2xl font-black text-purple-300">{freshness.avg_freshness_score} <span className="text-xs">/100</span></span>
            </div>
            <div className="glass-panel p-3 rounded-xl text-center">
              <span className="text-[10px] text-slate-400 font-bold uppercase block mb-1">Inspections</span>
              <span className="text-2xl font-black text-white">{freshness.total_analyses}</span>
            </div>
          </div>

          <div className="text-xs text-slate-300 bg-slate-900/60 p-3 rounded-xl border border-slate-800 space-y-1">
            <span className="text-slate-400 font-semibold block text-[11px] mb-1">Recent Category Distribution:</span>
            <div className="flex flex-wrap gap-1.5">
              {Object.entries(freshness.classification_distribution || {}).map(([cat, count]) => (
                <span key={cat} className="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-900/30 text-purple-300 border border-purple-500/30">
                  {cat}: {count}
                </span>
              ))}
              {Object.keys(freshness.classification_distribution || {}).length === 0 && (
                <span className="text-slate-500 text-[11px]">No image analyses recorded yet.</span>
              )}
            </div>
          </div>

          <button
            onClick={() => setActiveTab('freshness-analysis')}
            className="w-full py-2.5 rounded-xl text-xs font-bold text-purple-300 bg-purple-950/40 hover:bg-purple-900/40 border border-purple-500/30 transition flex items-center justify-center gap-1.5"
          >
            Perform Visual Freshness Inspection <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>

      </div>

      {/* Active Spoilage & Telemetry Alerts Feed */}
      <div className="glass-card rounded-2xl border border-slate-800 p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" /> Active Spoilage & Telemetry Alerts Feed
          </h3>
          <span className="text-xs text-slate-400">{alerts.length} Active Notice{alerts.length === 1 ? '' : 's'}</span>
        </div>

        {alerts.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {alerts.map((alert) => (
              <div
                key={alert.id}
                className={`p-4 rounded-xl border text-xs space-y-1.5 ${
                  alert.severity === 'critical'
                    ? 'bg-rose-950/20 border-rose-500/30 text-rose-200'
                    : 'bg-amber-950/20 border-amber-500/30 text-amber-200'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-white flex items-center gap-1">
                    {alert.severity === 'critical' ? <AlertOctagon className="w-3.5 h-3.5 text-rose-400" /> : <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />}
                    {alert.title}
                  </span>
                  <span className="font-mono text-[10px] text-slate-400">{alert.batch_number}</span>
                </div>
                <p className="text-[11px] leading-relaxed text-slate-300">{alert.message}</p>
                <div className="text-[10px] text-slate-500 pt-1">
                  Item: <span className="text-slate-300 font-medium">{alert.item_name}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="py-6 text-center text-xs text-slate-500 flex items-center justify-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" /> All physical inventory batches and cold-storage conditions are within nominal safety limits.
          </div>
        )}
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
