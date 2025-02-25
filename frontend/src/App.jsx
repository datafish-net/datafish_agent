import './App.css'

export default function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-content">
          <div className="logo">DataFish</div>
          <div className="nav-links">
            <a href="#features">Features</a>
            <a href="#about">About</a>
            <a href="#pricing">Pricing</a>
          </div>
          <button className="nav-cta">Get Started Free</button>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-content">
          <div className="hero-text">
            <h1>Integrate any software in minutes with no code</h1>
            <p className="hero-subtitle">Let DataFish handle your integrations while you focus on what matters!!!</p>
            <div className="hero-cta">
              <button className="primary-button">Start free with email</button>
              <button className="secondary-button">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" alt="Google logo"/>
                Start free with Google
              </button>
            </div>
          </div>
          <div className="integration-diagram">
            <div className="center-hub">
              <div className="hub-text">DataFish</div>
            </div>
            <div className="integration-apps">
              <div className="app-icon slack"></div>
              <div className="app-icon salesforce"></div>
              <div className="app-icon google-ads"></div>
              <div className="app-icon oracle"></div>
              <div className="app-icon s3"></div>
              <div className="app-icon facebook"></div>
              <div className="app-icon mongodb"></div>
              <div className="app-icon wordpress"></div>
              <div className="app-icon trello"></div>
              <div className="app-icon quickbooks"></div>
            </div>
          </div>
        </div>
      </section>

      <section className="features" id="features">
        <div className="section-content">
          <div className="section-header">
            <h2>Easy automation for every business</h2>
            <p>Connect your apps in just a few clicks</p>
          </div>
          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>Easy setup</h3>
              <p>Point, click, connect. No coding or technical skills needed.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔄</div>
              <h3>Works with everything</h3>
              <p>Connect any app or API. New integrations added every day.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Always reliable</h3>
              <p>Real-time monitoring ensures your workflows never miss a beat.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="section-content">
          <h2>Start automating today</h2>
          <p>Join thousands of companies using DataFish to power their integrations</p>
          <button className="primary-button">Get Started Free</button>
        </div>
      </section>

      <footer>
        <div className="footer-content">
          <div className="footer-logo">DataFish</div>
          <div className="footer-links">
            <div className="footer-column">
              <h4>Product</h4>
              <a href="#features">Features</a>
              <a href="#pricing">Pricing</a>
              <a href="#security">Security</a>
            </div>
            <div className="footer-column">
              <h4>Company</h4>
              <a href="#about">About</a>
              <a href="#careers">Careers</a>
              <a href="#contact">Contact</a>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2024 DataFish. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}