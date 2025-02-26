import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/landing/HomePage';
import AboutPage from './pages/landing/AboutPage';
import FeaturesPage from './pages/landing/FeaturesPage';
import PricingPage from './pages/landing/PricingPage';
import TerminalPage from './pages/terminal/TerminalPage';
import LandingLayout from './layouts/LandingLayout';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        {/* Landing pages */}
        <Route element={<LandingLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/features" element={<FeaturesPage />} />
          <Route path="/pricing" element={<PricingPage />} />
        </Route>
        
        {/* Terminal page */}
        <Route path="/terminal" element={<TerminalPage />} />
      </Routes>
    </Router>
  );
}

export default App;