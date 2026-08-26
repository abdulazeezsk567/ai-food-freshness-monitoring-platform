import React, { useState } from 'react';
import { useNotification } from '../context/NotificationContext';
import { Settings, Bell, Shield, Database, Save } from 'lucide-react';

export const SettingsPage = () => {
  const { addToast } = useNotification();
  const [expiryWarningDays, setExpiryWarningDays] = useState(3);
  const [tempHighThreshold, setTempHighThreshold] = useState(8.0);
  const [humidityHighThreshold, setHumidityHighThreshold] = useState(90.0);
  const [enableEmailAlerts, setEnableEmailAlerts] = useState(true);

  const handleSave = (e) => {
    e.preventDefault();
    addToast('System alert preferences saved successfully', 'success');
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 animate-fade-in">
      <div className="glass-panel p-6 rounded-2xl border border-slate-800">
        <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
          <Settings className="w-6 h-6 text-emerald-400" /> Platform Settings & Threshold Configuration
        </h2>
        <p className="text-xs text-slate-400 mt-1">Configure warning limits, telemetry alerts, and environment settings</p>
      </div>

      <form onSubmit={handleSave} className="glass-card p-6 rounded-2xl border border-slate-800 space-y-5 text-xs">
        <div>
          <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
            <Bell className="w-4 h-4 text-amber-400" /> Spoilage & Expiry Warning Parameters
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block font-bold text-slate-300 mb-1">Expiring Soon Warning Threshold (Days)</label>
              <input
                type="number"
                value={expiryWarningDays}
                onChange={(e) => setExpiryWarningDays(parseInt(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white"
              />
            </div>

            <div>
              <label className="block font-bold text-slate-300 mb-1">Max Storage Temp Warning (°C)</label>
              <input
                type="number"
                step="0.5"
                value={tempHighThreshold}
                onChange={(e) => setTempHighThreshold(parseFloat(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white"
              />
            </div>

            <div>
              <label className="block font-bold text-slate-300 mb-1">Max Humidity Warning (%)</label>
              <input
                type="number"
                step="1"
                value={humidityHighThreshold}
                onChange={(e) => setHumidityHighThreshold(parseFloat(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white"
              />
            </div>

            <div className="flex items-center gap-3 pt-6">
              <input
                type="checkbox"
                id="emailAlerts"
                checked={enableEmailAlerts}
                onChange={(e) => setEnableEmailAlerts(e.target.checked)}
                className="rounded border-slate-700 bg-slate-900 text-emerald-500"
              />
              <label htmlFor="emailAlerts" className="font-bold text-slate-300 cursor-pointer">
                Enable Near-Spoilage Alerts
              </label>
            </div>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-800 flex justify-end">
          <button
            type="submit"
            className="px-6 py-3 rounded-xl font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 shadow-lg shadow-emerald-500/20 transition flex items-center gap-2"
          >
            <Save className="w-4 h-4" /> Save Settings
          </button>
        </div>
      </form>
    </div>
  );
};
