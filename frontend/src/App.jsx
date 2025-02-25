import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
// Landing pages
import HomePage from './pages/landing/HomePage'
import AboutPage from './pages/landing/AboutPage'
import FeaturesPage from './pages/landing/FeaturesPage'
import PricingPage from './pages/landing/PricingPage'
// Dashboard pages
import DashboardLayout from './layouts/DashboardLayout'
import DashboardHome from './pages/dashboard/DashboardHome'
import Integrations from './pages/dashboard/Integrations'
import Settings from './pages/dashboard/Settings'
// Layouts and components
import LandingLayout from './layouts/LandingLayout'
import NotFound from './pages/NotFound'

export default function App() {
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
        
        {/* Dashboard pages */}
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<DashboardHome />} />
          <Route path="integrations" element={<Integrations />} />
          <Route path="settings" element={<Settings />} />
        </Route>
        
        {/* 404 page */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}