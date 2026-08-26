import React from 'react';

export const StatCard = ({ title, value, icon: Icon, color, trend }) => {
  return (
    <div className="glass-card p-6 rounded-2xl transition-all duration-300 relative overflow-hidden group">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">{title}</p>
          <h3 className="text-3xl font-extrabold text-white tracking-tight">{value}</h3>
          {trend && (
            <p className="text-xs font-medium text-slate-400 mt-2 flex items-center gap-1">
              <span className="text-emerald-400 font-semibold">{trend}</span> vs last period
            </p>
          )}
        </div>
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${color} bg-opacity-10 border border-current/20 group-hover:scale-110 transition-transform`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
      <div className="absolute -bottom-8 -right-8 w-24 h-24 rounded-full bg-emerald-500/5 blur-2xl group-hover:bg-emerald-500/10 transition-all pointer-events-none" />
    </div>
  );
};
