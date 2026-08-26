export const ROLES = {
  CONSUMER: 'CONSUMER',
  RETAIL_MANAGER: 'RETAIL_MANAGER',
  WAREHOUSE_OPERATOR: 'WAREHOUSE_OPERATOR',
  FOOD_QUALITY_INSPECTOR: 'FOOD_QUALITY_INSPECTOR',
  ADMINISTRATOR: 'ADMINISTRATOR',
};

export const CATEGORIES = [
  'Fruits',
  'Vegetables',
  'Dairy Products',
  'Meat & Poultry',
  'Seafood',
  'Bakery Products',
  'Packaged Foods',
  'Beverages',
];

export const UNITS = ['kg', 'grams', 'liters', 'units', 'boxes', 'packs'];

export const PACKAGING_TYPES = [
  'Standard Packaging',
  'Vacuum Sealed',
  'Plastic Tray & Wrap',
  'Glass Bottle',
  'Wooden Crate',
  'Cardboard Box',
  'Modified Atmosphere Packaging (MAP)',
];

export const STATUS_COLORS = {
  Fresh: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
  Good: 'bg-teal-500/10 text-teal-300 border-teal-500/30',
  Acceptable: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
  'Near Spoilage': 'bg-amber-500/10 text-amber-400 border-amber-500/30',
  Spoiled: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
};
