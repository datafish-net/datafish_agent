import React from 'react'
import { Link, Outlet } from 'react-router-dom'

export default function LandingLayout() {
  return (
    <div>
      <header className="navbar">
        <div className="nav-content">
          <Link to="/" className="logo-link">
            <div className="logo">DataFish</div>
          </Link>
          <nav className="nav-links">
            <Link to="/features">Features</Link>
            <Link to="/pricing">Pricing</Link>
            <Link to="/about">About</Link>
            <Link to="/terminal" className="nav-button">Terminal</Link>
          </nav>
        </div>
      </header>
      
      <main>
        <Outlet />
      </main>
      
      <footer>
        <div className="footer-content">
          <div className="footer-logo">DataFish</div>
          <div className="footer-links">
            <div className="footer-column">
              <h4>Product</h4>
              <Link to="/features">Features</Link>
              <Link to="/pricing">Pricing</Link>
            </div>
            <div className="footer-column">
              <h4>Company</h4>
              <Link to="/about">About</Link>
            </div>
            <div className="footer-column">
              <h4>Resources</h4>
              <Link to="/terminal">Terminal</Link>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} DataFish. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
} 