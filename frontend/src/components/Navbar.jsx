import React from 'react'
import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-content">
        <div className="logo">
          <Link to="/" className="logo-link">DataFish</Link>
        </div>
        <div className="nav-links">
          <Link to="/features">Features</Link>
          <Link to="/about">About</Link>
          <Link to="/pricing">Pricing</Link>
        </div>
        <button className="nav-cta">Get Started Free</button>
      </div>
    </nav>
  )
} 