import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useNotification } from '../context/NotificationContext';
import { Modal } from '../components/Modal';
import { ROLES } from '../utils/constants';
import { Users, Shield, UserCheck, Edit, Trash2, CheckCircle, XCircle } from 'lucide-react';

export const UserManagementPage = () => {
  const { user: currentUser } = useAuth();
  const { addToast } = useNotification();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Edit User State
  const [editingUser, setEditingUser] = useState(null);
  const [roleInput, setRoleInput] = useState('CONSUMER');
  const [isActiveInput, setIsActiveInput] = useState(true);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const data = await api.get('/users');
      setUsers(data);
    } catch (err) {
      addToast(err.message || 'Failed to fetch users list', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleEditOpen = (u) => {
    setEditingUser(u);
    setRoleInput(u.role);
    setIsActiveInput(u.is_active);
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/users/${editingUser.id}`, {
        role: roleInput,
        is_active: isActiveInput
      });
      addToast('User permissions updated successfully', 'success');
      setEditingUser(null);
      fetchUsers();
    } catch (err) {
      addToast(err.message || 'Failed to update user', 'error');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    try {
      await api.delete(`/users/${id}`);
      addToast('User deleted successfully', 'success');
      fetchUsers();
    } catch (err) {
      addToast(err.message || 'Failed to delete user', 'error');
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
            <Users className="w-6 h-6 text-purple-400" /> User Management & RBAC Permissions
          </h2>
          <p className="text-xs text-slate-400 mt-1">Manage user roles, platform access levels, and credentials</p>
        </div>
      </div>

      <div className="glass-card rounded-2xl border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-[11px] font-bold uppercase tracking-wider text-slate-400 bg-slate-900/50">
                <th className="py-4 px-4">ID</th>
                <th className="py-4 px-4">User</th>
                <th className="py-4 px-4">Email</th>
                <th className="py-4 px-4">Assigned Role</th>
                <th className="py-4 px-4">Status</th>
                <th className="py-4 px-4">Registered Date</th>
                <th className="py-4 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs">
              {loading ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-400">Loading user accounts...</td>
                </tr>
              ) : users.length > 0 ? (
                users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-4 px-4 font-mono text-slate-400">#{u.id}</td>
                    <td className="py-4 px-4 font-bold text-white">{u.name}</td>
                    <td className="py-4 px-4 text-slate-300">{u.email}</td>
                    <td className="py-4 px-4">
                      <span className="inline-block px-2.5 py-0.5 rounded text-[10px] font-bold border bg-purple-500/10 text-purple-300 border-purple-500/20 uppercase">
                        {u.role}
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      {u.is_active ? (
                        <span className="inline-flex items-center gap-1 text-emerald-400 font-semibold">
                          <CheckCircle className="w-3.5 h-3.5" /> Active
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-rose-400 font-semibold">
                          <XCircle className="w-3.5 h-3.5" /> Inactive
                        </span>
                      )}
                    </td>
                    <td className="py-4 px-4 text-slate-400">{new Date(u.created_at).toLocaleDateString()}</td>
                    <td className="py-4 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleEditOpen(u)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-purple-400 hover:bg-purple-500/10 transition"
                          title="Edit Role"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        {currentUser?.role === 'ADMINISTRATOR' && u.id !== currentUser.id && (
                          <button
                            onClick={() => handleDelete(u.id)}
                            className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition"
                            title="Delete User"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-500">No users found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <Modal isOpen={!!editingUser} onClose={() => setEditingUser(null)} title="Update User Role & Access">
        <form onSubmit={handleEditSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-bold text-slate-400 mb-1">User Name</label>
            <input type="text" value={editingUser?.name || ''} disabled className="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-slate-400 cursor-not-allowed" />
          </div>

          <div>
            <label className="block font-bold text-slate-400 mb-1">Assigned Role</label>
            <select
              value={roleInput}
              onChange={(e) => setRoleInput(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white"
            >
              <option value={ROLES.CONSUMER}>CONSUMER</option>
              <option value={ROLES.RETAIL_MANAGER}>RETAIL_MANAGER</option>
              <option value={ROLES.WAREHOUSE_OPERATOR}>WAREHOUSE_OPERATOR</option>
              <option value={ROLES.FOOD_QUALITY_INSPECTOR}>FOOD_QUALITY_INSPECTOR</option>
              <option value={ROLES.ADMINISTRATOR}>ADMINISTRATOR</option>
            </select>
          </div>

          <div className="flex items-center gap-2 pt-2">
            <input
              type="checkbox"
              id="isActive"
              checked={isActiveInput}
              onChange={(e) => setIsActiveInput(e.target.checked)}
              className="rounded border-slate-700 bg-slate-900 text-emerald-500 focus:ring-emerald-500"
            />
            <label htmlFor="isActive" className="font-bold text-slate-300 cursor-pointer">Account Active</label>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
            <button type="button" onClick={() => setEditingUser(null)} className="px-4 py-2 text-slate-400 hover:text-white">Cancel</button>
            <button type="submit" className="px-5 py-2.5 font-bold text-white bg-purple-600 hover:bg-purple-500 rounded-xl transition">Update User</button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
