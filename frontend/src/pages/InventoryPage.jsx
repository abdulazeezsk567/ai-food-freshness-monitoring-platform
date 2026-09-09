import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useNotification } from '../context/NotificationContext';
import { StatusBadge } from '../components/StatusBadge';
import { Modal } from '../components/Modal';
import { CATEGORIES, UNITS, PACKAGING_TYPES } from '../utils/constants';
import { Search, Filter, Plus, Edit2, Trash2, RefreshCw, Thermometer, Droplets, History, Sparkles } from 'lucide-react';

export const InventoryPage = ({ setActiveTab, onSelectReport }) => {
  const { user } = useAuth();
  const { addToast } = useNotification();
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  // History Modal State
  const [historyBatch, setHistoryBatch] = useState(null);
  const [historyRecords, setHistoryRecords] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  // Edit Modal State
  const [editingItem, setEditingItem] = useState(null);
  const [editForm, setEditForm] = useState({
    batch_number: '',
    quantity: 1,
    unit: 'kg',
    expiry_date: '',
    storage_temperature: 4,
    storage_humidity: 85,
    packaging_type: 'Standard Packaging'
  });

  const fetchInventory = async () => {
    setLoading(true);
    try {
      let endpoint = '/inventory?';
      if (selectedCategory) endpoint += `category=${encodeURIComponent(selectedCategory)}&`;
      if (selectedStatus) endpoint += `status=${encodeURIComponent(selectedStatus)}&`;
      if (searchQuery) endpoint += `search=${encodeURIComponent(searchQuery)}&`;
      const data = await api.get(endpoint);
      setInventory(data);
    } catch (err) {
      addToast(err.message || 'Failed to fetch inventory', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, [selectedCategory, selectedStatus, searchQuery]);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this inventory batch?')) return;
    try {
      await api.delete(`/inventory/${id}`);
      addToast('Inventory batch deleted successfully', 'success');
      fetchInventory();
    } catch (err) {
      addToast(err.message || 'Failed to delete inventory item', 'error');
    }
  };

  const handleEditOpen = (item) => {
    setEditingItem(item);
    setEditForm({
      batch_number: item.batch_number,
      quantity: item.quantity,
      unit: item.unit,
      expiry_date: item.expiry_date,
      storage_temperature: item.storage_temperature,
      storage_humidity: item.storage_humidity,
      packaging_type: item.packaging_type
    });
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/inventory/${editingItem.id}`, editForm);
      addToast('Batch details updated successfully', 'success');
      setEditingItem(null);
      fetchInventory();
    } catch (err) {
      addToast(err.message || 'Failed to update item', 'error');
    }
  };

  const handleViewHistory = async (item) => {
    setHistoryBatch(item);
    setHistoryLoading(true);
    try {
      const history = await api.get(`/freshness/inventory/${item.id}/freshness-history`);
      setHistoryRecords(history);
    } catch (err) {
      addToast(err.message || 'Failed to load freshness history', 'error');
    } finally {
      setHistoryLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-6 rounded-2xl border border-slate-800">
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight">Food Inventory Management</h2>
          <p className="text-xs text-slate-400 mt-1">Track physical batches, storage conditions, and freshness history</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchInventory}
            className="p-2.5 rounded-xl text-slate-400 hover:text-white bg-slate-800/80 hover:bg-slate-800 border border-slate-700 transition"
            title="Refresh Data"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
          <button
            onClick={() => setActiveTab('add-item')}
            className="px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 shadow-lg shadow-emerald-500/20 transition flex items-center gap-2"
          >
            <Plus className="w-4 h-4" /> Register New Item / Batch
          </button>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="glass-card p-4 rounded-2xl border border-slate-800 space-y-4">
        <div className="flex flex-col md:flex-row items-center gap-4 justify-between">
          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
            <input
              type="text"
              placeholder="Search batch or food name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl pl-10 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
            />
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto">
            <Filter className="w-4 h-4 text-slate-400" />
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="bg-slate-900/90 border border-slate-700/80 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500 transition"
            >
              <option value="">All Statuses</option>
              <option value="Fresh">Fresh</option>
              <option value="Good">Good</option>
              <option value="Acceptable">Acceptable</option>
              <option value="Near Spoilage">Near Spoilage</option>
              <option value="Spoiled">Spoiled</option>
            </select>

            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="bg-slate-900/90 border border-slate-700/80 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500 transition"
            >
              <option value="">All Categories</option>
              {CATEGORIES.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Inventory Table */}
      <div className="glass-card rounded-2xl border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-[11px] font-bold uppercase tracking-wider text-slate-400 bg-slate-900/50">
                <th className="py-4 px-4">Batch #</th>
                <th className="py-4 px-4">Food Item</th>
                <th className="py-4 px-4">Category</th>
                <th className="py-4 px-4">Quantity</th>
                <th className="py-4 px-4">Expiry Date</th>
                <th className="py-4 px-4">Storage Metrics</th>
                <th className="py-4 px-4">Freshness</th>
                <th className="py-4 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs">
              {loading ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-400">Loading inventory records...</td>
                </tr>
              ) : inventory.length > 0 ? (
                inventory.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-4 px-4 font-mono font-semibold text-emerald-400">{item.batch_number}</td>
                    <td className="py-4 px-4">
                      <div className="font-bold text-white">{item.food_item?.name || 'Item'}</div>
                      <div className="text-[10px] text-slate-400 line-clamp-1">{item.food_item?.description}</div>
                    </td>
                    <td className="py-4 px-4 text-slate-300">{item.food_item?.category}</td>
                    <td className="py-4 px-4 font-semibold text-white">{item.quantity} {item.unit}</td>
                    <td className="py-4 px-4">
                      <div className="text-slate-200 font-medium">{item.expiry_date}</div>
                      <div className="text-[10px] text-slate-400">
                        {item.days_to_expiry < 0 ? (
                          <span className="text-rose-400 font-semibold">Expired {Math.abs(item.days_to_expiry)} days ago</span>
                        ) : (
                          <span>{item.days_to_expiry} days remaining</span>
                        )}
                      </div>
                    </td>
                    <td className="py-4 px-4 text-slate-300">
                      <div className="flex items-center gap-3 text-[11px]">
                        <span className="flex items-center gap-1 text-amber-300">
                          <Thermometer className="w-3.5 h-3.5" /> {item.storage_temperature}°C
                        </span>
                        <span className="flex items-center gap-1 text-cyan-300">
                          <Droplets className="w-3.5 h-3.5" /> {item.storage_humidity}%
                        </span>
                      </div>
                      <div className="text-[10px] text-slate-400 mt-0.5">{item.packaging_type}</div>
                    </td>
                    <td className="py-4 px-4">
                      <StatusBadge status={item.status} />
                    </td>
                    <td className="py-4 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleViewHistory(item)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-purple-400 hover:bg-purple-500/10 transition"
                          title="View Freshness AI History"
                        >
                          <History className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleEditOpen(item)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 transition"
                          title="Edit Batch"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        {['ADMINISTRATOR', 'RETAIL_MANAGER', 'WAREHOUSE_OPERATOR', 'FOOD_QUALITY_INSPECTOR'].includes(user?.role) && (
                          <button
                            onClick={() => handleDelete(item.id)}
                            className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition"
                            title="Delete Batch"
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
                  <td colSpan={8} className="py-12 text-center text-slate-500">No matching inventory batches found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Freshness History Modal */}
      <Modal isOpen={!!historyBatch} onClose={() => setHistoryBatch(null)} title={`Freshness AI History — ${historyBatch?.batch_number}`}>
        <div className="space-y-4 text-xs">
          <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900 border border-slate-800">
            <div>
              <span className="font-bold text-white">{historyBatch?.food_item?.name}</span>
              <span className="text-[10px] text-slate-400 block">{historyBatch?.food_item?.category}</span>
            </div>
            <button
              onClick={() => {
                setHistoryBatch(null);
                setActiveTab('freshness-analysis');
              }}
              className="px-3 py-1.5 rounded-lg font-bold text-xs bg-purple-600 hover:bg-purple-500 text-white transition flex items-center gap-1.5"
            >
              <Sparkles className="w-3.5 h-3.5" /> Analyze Image for Batch
            </button>
          </div>

          {historyLoading ? (
            <div className="py-8 text-center text-slate-400">Loading batch freshness history...</div>
          ) : historyRecords.length > 0 ? (
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {historyRecords.map((rec) => (
                <div key={rec.id} className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/60 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <img src={rec.image_path} alt="Analysis" className="w-12 h-12 rounded-lg object-cover border border-slate-700" />
                    <div>
                      <div className="font-bold text-white">Score: {rec.freshness_score} / 100</div>
                      <div className="text-[10px] text-slate-400">{new Date(rec.created_at).toLocaleString()}</div>
                      <div className="text-[10px] text-amber-400 mt-0.5">Spoilage Prob: {(rec.spoilage_probability * 100).toFixed(1)}%</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <StatusBadge status={rec.predicted_category} />
                    <button
                      onClick={() => {
                        setHistoryBatch(null);
                        onSelectReport(rec);
                      }}
                      className="px-2.5 py-1 rounded-lg text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-200 transition"
                    >
                      Report
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="py-8 text-center text-slate-500">
              No image analysis history linked to this batch yet.
            </div>
          )}
        </div>
      </Modal>

      {/* Edit Modal */}
      <Modal isOpen={!!editingItem} onClose={() => setEditingItem(null)} title="Edit Inventory Batch">
        <form onSubmit={handleEditSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-bold text-slate-400 mb-1">Batch Number</label>
            <input
              type="text"
              value={editForm.batch_number}
              onChange={(e) => setEditForm({ ...editForm, batch_number: e.target.value })}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-400 mb-1">Quantity</label>
              <input
                type="number"
                step="0.1"
                value={editForm.quantity}
                onChange={(e) => setEditForm({ ...editForm, quantity: parseFloat(e.target.value) })}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white"
                required
              />
            </div>
            <div>
              <label className="block font-bold text-slate-400 mb-1">Unit</label>
              <select
                value={editForm.unit}
                onChange={(e) => setEditForm({ ...editForm, unit: e.target.value })}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white"
              >
                {UNITS.map(u => <option key={u} value={u}>{u}</option>)}
              </select>
            </div>
          </div>

          <div>
            <label className="block font-bold text-slate-400 mb-1">Expiry Date</label>
            <input
              type="date"
              value={editForm.expiry_date}
              onChange={(e) => setEditForm({ ...editForm, expiry_date: e.target.value })}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-400 mb-1">Storage Temp (°C)</label>
              <input
                type="number"
                step="0.1"
                value={editForm.storage_temperature}
                onChange={(e) => setEditForm({ ...editForm, storage_temperature: parseFloat(e.target.value) })}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-400 mb-1">Humidity (%)</label>
              <input
                type="number"
                step="0.1"
                value={editForm.storage_humidity}
                onChange={(e) => setEditForm({ ...editForm, storage_humidity: parseFloat(e.target.value) })}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white"
              />
            </div>
          </div>

          <div>
            <label className="block font-bold text-slate-400 mb-1">Packaging Type</label>
            <select
              value={editForm.packaging_type}
              onChange={(e) => setEditForm({ ...editForm, packaging_type: e.target.value })}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white"
            >
              {PACKAGING_TYPES.map(p => <option key={p} value={p}>{p}</option>)}
            </select>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
            <button type="button" onClick={() => setEditingItem(null)} className="px-4 py-2 rounded-xl text-slate-400 hover:text-white">Cancel</button>
            <button type="submit" className="px-5 py-2.5 rounded-xl font-bold text-white bg-emerald-600 hover:bg-emerald-500 transition">Save Changes</button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
