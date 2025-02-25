import React from 'react'
import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer>
      <div className="footer-content">
        <div className="footer-logo">DataFish</div>
        <div className="footer-links">
          <div className="footer-column">
            <h4>Product</h4>
            <Link to="/features">Features</Link>
            <Link to="/pricing">Pricing</Link>
            <Link to="/security">Security</Link>
          </div>
          <div className="footer-column">
            <h4>Company</h4>
            <Link to="/about">About</Link>
            <Link to="/careers">Careers</Link>
            <Link to="/contact">Contact</Link>
          </div>
        </div>
      </div>
      <div className="footer-bottom">
        <p>© 2024 DataFish. All rights reserved.</p>
      </div>
    </footer>
  )
} 