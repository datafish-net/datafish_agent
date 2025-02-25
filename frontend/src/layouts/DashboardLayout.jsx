import React from 'react'
import { Outlet, Link } from 'react-router-dom'

export default function DashboardLayout() {
  return (
    <div className="dashboard-layout">
      <header className="dashboard-header">
        <div className="dashboard-logo">
          <Link to="/">DataFish</Link>
        </div>
        <div className="user-menu">
          <span className="user-name">John Doe</span>
          <div className="avatar">JD</div>
        </div>
      </header>
      
      <div className="dashboard-container">
        <aside className="dashboard-sidebar">
          <nav className="dashboard-nav">
            <Link to="/dashboard" className="nav-item">
              <span className="nav-icon">📊</span>
              <span>Dashboard</span>
            </Link>
            <Link to="/dashboard/integrations" className="nav-item">
              <span className="nav-icon">🔄</span>
              <span>Integrations</span>
            </Link>
            <Link to="/dashboard/settings" className="nav-item">
              <span className="nav-icon">⚙️</span>
              <span>Settings</span>
            </Link>
          </nav>
        </aside>
        
        <main className="dashboard-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
} 