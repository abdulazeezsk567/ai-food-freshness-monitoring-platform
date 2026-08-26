import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Info, X } from 'lucide-react';

export const Toast = ({ toast, onClose }) => {
  const icons = {
    success: <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0" />,
    error: <XCircle className="w-5 h-5 text-rose-400 shrink-0" />,
    warning: <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />,
    info: <Info className="w-5 h-5 text-sky-400 shrink-0" />,
  };

  const borderColors = {
    success: 'border-emerald-500/40 bg-emerald-950/80',
    error: 'border-rose-500/40 bg-rose-950/80',
    warning: 'border-amber-500/40 bg-amber-950/80',
    info: 'border-sky-500/40 bg-sky-950/80',
  };

  return (
    <div className={`flex items-center gap-3 p-4 rounded-xl border glass-panel shadow-2xl transition-all duration-300 ${borderColors[toast.type] || borderColors.info}`}>
      {icons[toast.type] || icons.info}
      <p className="text-sm font-medium text-slate-100 flex-1">{toast.message}</p>
      <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
        <X className="w-4 h-4" />
      </button>
    </div>
  );
};
