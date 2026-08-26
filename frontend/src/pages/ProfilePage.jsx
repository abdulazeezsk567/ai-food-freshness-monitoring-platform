import React from 'react';
import { useAuth } from '../context/AuthContext';
import { UserCheck, Shield, Mail, Calendar, Key } from 'lucide-react';

export const ProfilePage = () => {
  const { user } = useAuth();

  const rolePermissions = {
    ADMINISTRATOR: ['Full system access', 'User management', 'Role modification', 'Platform configuration', 'All CRUD operations'],
    RETAIL_MANAGER: ['Manage store inventory & batches', 'View freshness analytics', 'Track expiry alerts', 'Register new items'],
    WAREHOUSE_OPERATOR: ['Manage warehouse inventory', 'Monitor storage conditions (Temp/Humidity)', 'View batch telemetry'],
    FOOD_QUALITY_INSPECTOR: ['Inspect food quality', 'Review freshness results', 'Audit spoilage information', 'View users list'],
    CONSUMER: ['View personal dashboard', 'Add/view personal food items', 'View freshness recommendations'],
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 animate-fade-in">
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center gap-4">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-emerald-500/20">
          {user?.name ? user.name[0].toUpperCase() : 'U'}
        </div>
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight">{user?.name}</h2>
          <p className="text-xs text-emerald-400 font-semibold">{user?.email}</p>
        </div>
      </div>

      <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Shield className="w-4 h-4 text-emerald-400" /> Account & Role Details
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="glass-panel p-4 rounded-xl">
            <span className="text-slate-400 font-medium block mb-1">User ID:</span>
            <span className="font-mono font-bold text-white">#{user?.id}</span>
          </div>

          <div className="glass-panel p-4 rounded-xl">
            <span className="text-slate-400 font-medium block mb-1">Assigned System Role:</span>
            <span className="font-bold text-emerald-400">{user?.role}</span>
          </div>
        </div>

        <div className="pt-2">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-2">Granted Role Capabilities:</span>
          <div className="space-y-2">
            {(rolePermissions[user?.role] || []).map((perm, idx) => (
              <div key={idx} className="flex items-center gap-2 text-xs text-slate-300 glass-panel p-2.5 rounded-xl border border-slate-800">
                <div className="w-2 h-2 rounded-full bg-emerald-400" />
                {perm}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
