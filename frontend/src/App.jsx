import React from 'react';
import Terminal from './components/Terminal';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Terminal Agent</h1>
        <p>A powerful terminal interface with AI capabilities</p>
      </header>
      
      <main className="app-main">
        <Terminal />
      </main>
      
      <footer className="app-footer">
        <p>Built with React, FastAPI, and OpenAI</p>
      </footer>
    </div>
  );
}

export default App;