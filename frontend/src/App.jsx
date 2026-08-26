import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { NotificationProvider } from './context/NotificationContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';

import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';

import { DashboardPage } from './pages/DashboardPage';
import { InventoryPage } from './pages/InventoryPage';
import { AddFoodItemPage } from './pages/AddFoodItemPage';
import { BatchManagementPage } from './pages/BatchManagementPage';
import { UserManagementPage } from './pages/UserManagementPage';
import { DatasetPage } from './pages/DatasetPage';
import { ProfilePage } from './pages/ProfilePage';
import { SettingsPage } from './pages/SettingsPage';

const AppContent = () => {
  const { user, loading } = useAuth();
  const [publicView, setPublicView] = useState('landing'); // 'landing', 'login', 'register'
  const [activeTab, setActiveTab] = useState('dashboard');

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-500" />
      </div>
    );
  }

  // Render Public Pages when not logged in
  if (!user) {
    if (publicView === 'login') return <LoginPage onNavigate={setPublicView} />;
    if (publicView === 'register') return <RegisterPage onNavigate={setPublicView} />;
    return <LandingPage onNavigate={setPublicView} />;
  }

  // Render Authenticated Dashboard Layout
  const renderAuthenticatedPage = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardPage setActiveTab={setActiveTab} />;
      case 'inventory':
        return <InventoryPage setActiveTab={setActiveTab} />;
      case 'add-item':
        return <AddFoodItemPage setActiveTab={setActiveTab} />;
      case 'batches':
        return <BatchManagementPage />;
      case 'users':
        return <UserManagementPage />;
      case 'datasets':
        return <DatasetPage />;
      case 'profile':
        return <ProfilePage />;
      case 'settings':
        return <SettingsPage />;
      default:
        return <DashboardPage setActiveTab={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <div className="flex-1 flex overflow-hidden">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        
        <main className="flex-1 p-6 md:p-8 overflow-y-auto max-w-7xl mx-auto w-full">
          {renderAuthenticatedPage()}
        </main>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <NotificationProvider>
        <AppContent />
      </NotificationProvider>
    </AuthProvider>
  );
}
