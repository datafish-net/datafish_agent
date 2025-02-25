import React from 'react'

export default function DashboardHome() {
  return (
    <div className="dashboard-page">
      <h1>Dashboard</h1>
      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>Active Integrations</h3>
          <div className="stat-value">12</div>
        </div>
        <div className="stat-card">
          <h3>Data Transfers</h3>
          <div className="stat-value">1.4M</div>
        </div>
        <div className="stat-card">
          <h3>API Calls</h3>
          <div className="stat-value">8.2K</div>
        </div>
      </div>
      
      <div className="recent-activity">
        <h2>Recent Activity</h2>
        <div className="activity-list">
          <div className="activity-item">
            <div className="activity-icon">🔄</div>
            <div className="activity-details">
              <div className="activity-title">Salesforce integration updated</div>
              <div className="activity-time">2 hours ago</div>
            </div>
          </div>
          <div className="activity-item">
            <div className="activity-icon">✅</div>
            <div className="activity-details">
              <div className="activity-title">MongoDB sync completed</div>
              <div className="activity-time">Yesterday</div>
            </div>
          </div>
          <div className="activity-item">
            <div className="activity-icon">🔔</div>
            <div className="activity-details">
              <div className="activity-title">New API key generated</div>
              <div className="activity-time">2 days ago</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 