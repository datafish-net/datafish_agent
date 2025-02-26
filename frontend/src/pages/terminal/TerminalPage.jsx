import React from 'react';
import Terminal from '../../components/Terminal';
import './TerminalPage.css';

const TerminalPage = () => {
  return (
    <div className="terminal-page">
      <header className="terminal-page-header">
        <h1>AI Terminal Agent</h1>
        <p>A powerful terminal interface with AI capabilities</p>
      </header>
      
      <main className="terminal-page-main">
        <Terminal />
      </main>
      
      <footer className="terminal-page-footer">
        <p>Datafish</p>
      </footer>
    </div>
  );
};

export default TerminalPage; 