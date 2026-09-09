import React from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  LayoutDashboard, 
  Sparkles,
  Package, 
  PlusCircle, 
  Layers, 
  Users, 
  Database, 
  Settings, 
  UserCheck, 
  Cpu 
} from 'lucide-react';

export const Sidebar = ({ activeTab, setActiveTab }) => {
  const { user } = useAuth();
  const role = user?.role || 'CONSUMER';

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, roles: ['CONSUMER', 'RETAIL_MANAGER', 'WAREHOUSE_OPERATOR', 'FOOD_QUALITY_INSPECTOR', 'ADMINISTRATOR'] },
    { id: 'freshness-analysis', label: 'Freshness Analysis AI', icon: Sparkles, roles: ['CONSUMER', 'RETAIL_MANAGER', 'WAREHOUSE_OPERATOR', 'FOOD_QUALITY_INSPECTOR', 'ADMINISTRATOR'] },
    { id: 'inventory', label: 'Food Inventory', icon: Package, roles: ['CONSUMER', 'RETAIL_MANAGER', 'WAREHOUSE_OPERATOR', 'FOOD_QUALITY_INSPECTOR', 'ADMINISTRATOR'] },
    { id: 'add-item', label: 'Add Food Item', icon: PlusCircle, roles: ['CONSUMER', 'RETAIL_MANAGER', 'WAREHOUSE_OPERATOR', 'FOOD_QUALITY_INSPECTOR', 'ADMINISTRATOR'] },
    { id: 'batches', label: 'Batch Telemetry', icon: Layers, roles: ['RETAIL_MANAGER', 'WAREHOUSE_OPERATOR', 'FOOD_QUALITY_INSPECTOR', 'ADMINISTRATOR'] },
    { id: 'users', label: 'User Management', icon: Users, roles: ['ADMINISTRATOR', 'FOOD_QUALITY_INSPECTOR'] },
    { id: 'datasets', label: 'Dataset Foundation', icon: Database, roles: ['CONSUMER', 'RETAIL_MANAGER', 'WAREHOUSE_OPERATOR', 'FOOD_QUALITY_INSPECTOR', 'ADMINISTRATOR'] },
    { id: 'profile', label: 'User Profile', icon: UserCheck, roles: ['CONSUMER', 'RETAIL_MANAGER', 'WAREHOUSE_OPERATOR', 'FOOD_QUALITY_INSPECTOR', 'ADMINISTRATOR'] },
    { id: 'settings', label: 'Settings', icon: Settings, roles: ['CONSUMER', 'RETAIL_MANAGER', 'WAREHOUSE_OPERATOR', 'FOOD_QUALITY_INSPECTOR', 'ADMINISTRATOR'] },
  ];

  return (
    <aside className="w-64 glass-panel border-r border-slate-800/80 p-4 flex flex-col justify-between hidden md:flex shrink-0">
      <div className="space-y-6">
        <div className="px-3">
          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-3">Navigation Menu</p>
          <nav className="space-y-1">
            {navItems
              .filter((item) => item.roles.includes(role))
              .map((item) => {
                const Icon = item.icon;
                const isActive = activeTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => setActiveTab(item.id)}
                    className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-semibold text-sm transition-all duration-200 ${
                      isActive
                        ? 'bg-gradient-to-r from-purple-500/20 to-emerald-500/10 text-purple-300 border border-purple-500/30 shadow-md shadow-purple-500/10'
                        : 'text-slate-400 hover:text-white hover:bg-slate-800/50 border border-transparent'
                    }`}
                  >
                    <Icon className={`w-4 h-4 ${isActive ? 'text-purple-400' : 'text-slate-400'}`} />
                    {item.label}
                  </button>
                );
              })}
          </nav>
        </div>
      </div>

      <div className="p-4 rounded-xl glass-card border border-purple-500/20 bg-purple-950/20">
        <div className="flex items-center gap-2 mb-2">
          <Cpu className="w-4 h-4 text-purple-400" />
          <span className="text-xs font-bold text-purple-300">Milestone 2 Active</span>
        </div>
        <p className="text-[11px] text-slate-400 leading-snug">
          Computer vision color degradation, texture GLCM & spoilage indicator engine online.
        </p>
      </div>
    </aside>
  );
};
