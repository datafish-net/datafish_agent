import React from 'react'

export default function Settings() {
  return (
    <div className="dashboard-page">
      <h1>Settings</h1>
      
      <div className="settings-section">
        <h2>Account Settings</h2>
        <form className="settings-form">
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input type="text" id="name" defaultValue="John Doe" />
          </div>
          
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input type="email" id="email" defaultValue="john@example.com" />
          </div>
          
          <div className="form-group">
            <label htmlFor="company">Company</label>
            <input type="text" id="company" defaultValue="Acme Inc." />
          </div>
          
          <button type="submit" className="primary-button">Save Changes</button>
        </form>
      </div>
      
      <div className="settings-section">
        <h2>API Keys</h2>
        <div className="api-key-section">
          <div className="api-key-item">
            <div className="api-key-info">
              <div className="api-key-name">Production Key</div>
              <div className="api-key-value">••••••••••••••••</div>
            </div>
            <button className="secondary-button">Reveal</button>
            <button className="secondary-button">Regenerate</button>
          </div>
          
          <div className="api-key-item">
            <div className="api-key-info">
              <div className="api-key-name">Development Key</div>
              <div className="api-key-value">••••••••••••••••</div>
            </div>
            <button className="secondary-button">Reveal</button>
            <button className="secondary-button">Regenerate</button>
          </div>
        </div>
      </div>
    </div>
  )
} 