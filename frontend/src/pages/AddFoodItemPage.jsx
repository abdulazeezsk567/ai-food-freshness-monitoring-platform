import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useNotification } from '../context/NotificationContext';
import { CATEGORIES, UNITS, PACKAGING_TYPES } from '../utils/constants';
import { PlusCircle, ArrowRight, Package, Layers, Thermometer, Calendar } from 'lucide-react';

export const AddFoodItemPage = ({ setActiveTab }) => {
  const { addToast } = useNotification();
  const [existingItems, setExistingItems] = useState([]);
  const [createMode, setCreateMode] = useState('new'); // 'new' or 'existing'
  const [selectedFoodId, setSelectedFoodId] = useState('');

  // Form State
  const [name, setName] = useState('');
  const [category, setCategory] = useState(CATEGORIES[0]);
  const [description, setDescription] = useState('');

  const [batchNumber, setBatchNumber] = useState(`BATCH-${Date.now().toString().slice(-6)}`);
  const [quantity, setQuantity] = useState(10);
  const [unit, setUnit] = useState('kg');
  
  const todayStr = new Date().toISOString().split('T')[0];
  const nextWeekStr = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

  const [purchaseDate, setPurchaseDate] = useState(todayStr);
  const [expiryDate, setExpiryDate] = useState(nextWeekStr);

  const [temperature, setTemperature] = useState(4.0);
  const [humidity, setHumidity] = useState(85.0);
  const [packagingType, setPackagingType] = useState(PACKAGING_TYPES[0]);
  const [storageDuration, setStorageDuration] = useState(7);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const loadItems = async () => {
      try {
        const items = await api.get('/food-items');
        setExistingItems(items);
        if (items.length > 0) setSelectedFoodId(items[0].id.toString());
      } catch (err) {
        console.error('Error loading existing food items:', err);
      }
    };
    loadItems();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      let targetFoodId;
      if (createMode === 'new') {
        if (!name) {
          addToast('Please enter food product name', 'warning');
          setSubmitting(false);
          return;
        }
        const createdFood = await api.post('/food-items', {
          name,
          category,
          description,
        });
        targetFoodId = createdFood.id;
      } else {
        targetFoodId = parseInt(selectedFoodId);
      }

      await api.post('/inventory', {
        food_item_id: targetFoodId,
        batch_number: batchNumber,
        quantity: parseFloat(quantity),
        unit,
        purchase_date: purchaseDate,
        expiry_date: expiryDate,
        storage_temperature: parseFloat(temperature),
        storage_humidity: parseFloat(humidity),
        packaging_type: packagingType,
        storage_duration: parseInt(storageDuration),
      });

      addToast('Food item batch successfully registered!', 'success');
      setActiveTab('inventory');
    } catch (err) {
      addToast(err.message || 'Failed to save inventory item', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in">
      <div className="glass-panel p-6 rounded-2xl border border-slate-800">
        <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
          <PlusCircle className="w-6 h-6 text-emerald-400" /> Register Food Item & Batch Telemetry
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Complete food product details and environmental storage parameters
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Step 1: Product Selection / Creation */}
        <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Package className="w-4 h-4 text-emerald-400" /> 1. Food Product Information
            </h3>
            <div className="flex items-center gap-2 text-xs">
              <button
                type="button"
                onClick={() => setCreateMode('new')}
                className={`px-3 py-1.5 rounded-xl font-bold transition ${createMode === 'new' ? 'bg-emerald-500 text-white' : 'bg-slate-800 text-slate-400'}`}
              >
                + New Product
              </button>
              {existingItems.length > 0 && (
                <button
                  type="button"
                  onClick={() => setCreateMode('existing')}
                  className={`px-3 py-1.5 rounded-xl font-bold transition ${createMode === 'existing' ? 'bg-emerald-500 text-white' : 'bg-slate-800 text-slate-400'}`}
                >
                  Select Existing
                </button>
              )}
            </div>
          </div>

          {createMode === 'new' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="block font-bold text-slate-300 mb-1">Food Name *</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Organic Gala Apples"
                  className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white placeholder-slate-500 focus:border-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="block font-bold text-slate-300 mb-1">Category *</label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white focus:border-emerald-500"
                >
                  {CATEGORIES.map((cat) => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>

              <div className="md:col-span-2">
                <label className="block font-bold text-slate-300 mb-1">Product Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Optional details regarding variety, harvest date, or origin..."
                  className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white h-20 placeholder-slate-500 focus:border-emerald-500"
                />
              </div>
            </div>
          ) : (
            <div className="text-xs">
              <label className="block font-bold text-slate-300 mb-1">Select Registered Product</label>
              <select
                value={selectedFoodId}
                onChange={(e) => setSelectedFoodId(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white focus:border-emerald-500"
              >
                {existingItems.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.name} ({item.category})
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>

        {/* Step 2: Batch Information */}
        <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Layers className="w-4 h-4 text-teal-400" /> 2. Batch & Expiry Timeline
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div>
              <label className="block font-bold text-slate-300 mb-1">Batch Number *</label>
              <input
                type="text"
                value={batchNumber}
                onChange={(e) => setBatchNumber(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 font-mono text-emerald-400"
                required
              />
            </div>

            <div>
              <label className="block font-bold text-slate-300 mb-1">Quantity *</label>
              <input
                type="number"
                step="0.1"
                min="0.1"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white"
                required
              />
            </div>

            <div>
              <label className="block font-bold text-slate-300 mb-1">Unit *</label>
              <select
                value={unit}
                onChange={(e) => setUnit(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white"
              >
                {UNITS.map(u => <option key={u} value={u}>{u}</option>)}
              </select>
            </div>

            <div>
              <label className="block font-bold text-slate-300 mb-1">Purchase / Reception Date *</label>
              <input
                type="date"
                value={purchaseDate}
                onChange={(e) => setPurchaseDate(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white"
                required
              />
            </div>

            <div>
              <label className="block font-bold text-slate-300 mb-1">Expiration Date *</label>
              <input
                type="date"
                value={expiryDate}
                onChange={(e) => setExpiryDate(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white"
                required
              />
            </div>

            <div>
              <label className="block font-bold text-slate-300 mb-1">Storage Duration (Days)</label>
              <input
                type="number"
                value={storageDuration}
                onChange={(e) => setStorageDuration(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white"
                required
              />
            </div>
          </div>
        </div>

        {/* Step 3: Environmental Storage Parameters */}
        <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Thermometer className="w-4 h-4 text-cyan-400" /> 3. Environmental Storage Telemetry
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div>
              <label className="block font-bold text-slate-300 mb-1">Storage Temp (°C)</label>
              <input
                type="number"
                step="0.1"
                value={temperature}
                onChange={(e) => setTemperature(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white"
                required
              />
            </div>

            <div>
              <label className="block font-bold text-slate-300 mb-1">Relative Humidity (%)</label>
              <input
                type="number"
                step="0.1"
                value={humidity}
                onChange={(e) => setHumidity(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white"
                required
              />
            </div>

            <div>
              <label className="block font-bold text-slate-300 mb-1">Packaging Format</label>
              <select
                value={packagingType}
                onChange={(e) => setPackagingType(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-3 text-white"
              >
                {PACKAGING_TYPES.map(p => <option key={p} value={p}>{p}</option>)}
              </select>
            </div>
          </div>
        </div>

        {/* Save button */}
        <div className="flex items-center justify-end gap-4 pt-2">
          <button
            type="button"
            onClick={() => setActiveTab('inventory')}
            className="px-5 py-3 rounded-xl text-xs font-bold text-slate-400 hover:text-white transition"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="px-8 py-3 rounded-xl text-sm font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 shadow-xl shadow-emerald-500/20 transition flex items-center gap-2"
          >
            {submitting ? 'Saving Batch...' : 'Save to Inventory'} <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
};
