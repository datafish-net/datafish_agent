import React from 'react'

export default function Integrations() {
  return (
    <div className="dashboard-page">
      <h1>Integrations</h1>
      <div className="page-actions">
        <button className="primary-button">Add New Integration</button>
      </div>
      
      <div className="integrations-grid">
        <div className="integration-card active">
          <div className="integration-logo slack"></div>
          <h3>Slack</h3>
          <div className="integration-status">Active</div>
          <button className="secondary-button">Configure</button>
        </div>
        
        <div className="integration-card active">
          <div className="integration-logo salesforce"></div>
          <h3>Salesforce</h3>
          <div className="integration-status">Active</div>
          <button className="secondary-button">Configure</button>
        </div>
        
        <div className="integration-card">
          <div className="integration-logo mongodb"></div>
          <h3>MongoDB</h3>
          <div className="integration-status">Inactive</div>
          <button className="secondary-button">Activate</button>
        </div>
        
        <div className="integration-card">
          <div className="integration-logo google-ads"></div>
          <h3>Google Ads</h3>
          <div className="integration-status">Inactive</div>
          <button className="secondary-button">Activate</button>
        </div>
      </div>
    </div>
  )
} 