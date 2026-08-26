import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNotification } from '../context/NotificationContext';
import { Leaf, Lock, Mail, ArrowRight, ShieldCheck, User } from 'lucide-react';

export const LoginPage = ({ onNavigate }) => {
  const { login } = useAuth();
  const { addToast } = useNotification();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      addToast('Please enter both email and password', 'warning');
      return;
    }
    setSubmitting(true);
    try {
      await login(email, password);
      addToast('Successfully signed in!', 'success');
    } catch (err) {
      addToast(err.message || 'Invalid credentials', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const demoAccounts = [
    { role: 'System Admin', email: 'admin@foodfreshness.com', pass: 'Admin123!', color: 'border-purple-500/40 text-purple-300' },
    { role: 'Retail Manager', email: 'retail@foodfreshness.com', pass: 'Manager123!', color: 'border-emerald-500/40 text-emerald-300' },
    { role: 'Food Inspector', email: 'inspector@foodfreshness.com', pass: 'Inspector123!', color: 'border-cyan-500/40 text-cyan-300' },
    { role: 'Warehouse Operator', email: 'warehouse@foodfreshness.com', pass: 'Warehouse123!', color: 'border-amber-500/40 text-amber-300' },
    { role: 'Consumer', email: 'consumer@foodfreshness.com', pass: 'Consumer123!', color: 'border-blue-500/40 text-blue-300' },
  ];

  const handleQuickLogin = (demoEmail, demoPass) => {
    setEmail(demoEmail);
    setPassword(demoPass);
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6 relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-xl shadow-emerald-500/20 mx-auto mb-4">
            <Leaf className="w-7 h-7 text-white" />
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">Sign in to Fresh Guard</h2>
          <p className="text-xs text-slate-400 mt-1">Food Freshness Monitoring Platform</p>
        </div>

        {/* Quick Demo Logins Box */}
        <div className="glass-card p-4 rounded-2xl mb-6 border border-emerald-500/20">
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 mb-2">
            <ShieldCheck className="w-4 h-4" /> Quick Demo Role Auto-Fill:
          </div>
          <div className="grid grid-cols-2 gap-2 text-left">
            {demoAccounts.map((acc) => (
              <button
                key={acc.role}
                type="button"
                onClick={() => handleQuickLogin(acc.email, acc.pass)}
                className={`p-2 rounded-xl border glass-panel text-[11px] font-semibold hover:bg-slate-800 transition ${acc.color}`}
              >
                {acc.role}
              </button>
            ))}
          </div>
        </div>

        {/* Form Card */}
        <form onSubmit={handleSubmit} className="glass-panel p-8 rounded-2xl space-y-5">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                className="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3 rounded-xl text-sm font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 shadow-lg shadow-emerald-500/20 transition flex items-center justify-center gap-2"
          >
            {submitting ? 'Authenticating...' : 'Sign In'} <ArrowRight className="w-4 h-4" />
          </button>

          <p className="text-center text-xs text-slate-400 pt-2">
            Don't have an account?{' '}
            <button
              type="button"
              onClick={() => onNavigate('register')}
              className="text-emerald-400 font-bold hover:underline"
            >
              Register here
            </button>
          </p>
        </form>
      </div>
    </div>
  );
};
