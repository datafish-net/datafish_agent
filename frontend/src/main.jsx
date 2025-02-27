import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'  // This is crucial!
import 'highlight.js/styles/github-dark.css'  // You can choose a different theme
import './styles/highlight.css'  // Our custom overrides

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
) 