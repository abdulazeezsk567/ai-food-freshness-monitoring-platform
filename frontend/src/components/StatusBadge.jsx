import React from 'react';
import { STATUS_COLORS } from '../utils/constants';

export const StatusBadge = ({ status }) => {
  const colorClass = STATUS_COLORS[status] || 'bg-slate-800 text-slate-300 border-slate-700';

  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold border ${colorClass}`}>
      <span className="w-1.5 h-1.5 rounded-full bg-current mr-1.5 animate-pulse"></span>
      {status}
    </span>
  );
};
