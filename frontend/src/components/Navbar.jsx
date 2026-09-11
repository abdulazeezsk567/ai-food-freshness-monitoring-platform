import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Shield, LogOut, User as UserIcon, ExternalLink, Leaf } from 'lucide-react';

export const Navbar = ({ activeTab, setActiveTab }) => {
  const { user, logout } = useAuth();

  const roleColors = {
    ADMINISTRATOR: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
    RETAIL_MANAGER: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
    WAREHOUSE_OPERATOR: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
    FOOD_QUALITY_INSPECTOR: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
    CONSUMER: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
  };

  return (
    <header className="sticky top-0 z-40 w-full glass-panel border-b border-slate-800/80 px-6 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <Leaf className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight leading-none">
              Fresh Guard
            </h1>
            <p className="text-xs text-slate-400 font-medium">Food Freshness Monitoring Platform</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white bg-slate-800/60 hover:bg-slate-800 border border-slate-700 transition"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            API Swagger Docs
          </a>

          {user && (
            <div className="flex items-center gap-3 pl-3 border-l border-slate-800">
              <div 
                onClick={() => setActiveTab('profile')}
                className="flex items-center gap-2 cursor-pointer group"
              >
                <div className="w-9 h-9 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-emerald-400 group-hover:border-emerald-500/50 transition">
                  <UserIcon className="w-5 h-5" />
                </div>
                <div className="hidden sm:block text-left">
                  <div className="text-sm font-bold text-white group-hover:text-emerald-400 transition">{user.name}</div>
                  <div className={`text-[10px] font-bold px-2 py-0.5 rounded border inline-block uppercase tracking-wider ${roleColors[user.role] || 'bg-slate-800 text-slate-300'}`}>
                    {user.role}
                  </div>
                </div>
              </div>

              <button
                onClick={logout}
                title="Logout"
                className="p-2 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
