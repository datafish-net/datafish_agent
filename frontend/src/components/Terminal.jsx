import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './Terminal.css';

const Terminal = () => {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState([]);
  const [commandHistory, setCommandHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [isLoading, setIsLoading] = useState(false);
  const outputRef = useRef(null);
  const inputRef = useRef(null);

  // Add a welcome message when the component mounts
  useEffect(() => {
    const welcomeMessage = {
      command: '',
      output: `
╭────────────────────────────────────────────────╮
│                                                │
│  Welcome to the AI Terminal Agent              │
│                                                │
│  Type 'help' to see available commands         │
│  Try 'ai:Hello, world!' to talk to the AI      │
│  Or 'ai:code:Create a simple game' to generate │
│  and run Python code                           │
│                                                │
╰────────────────────────────────────────────────╯
`,
      isError: false
    };
    setHistory([welcomeMessage]);
  }, []);

  // Auto-scroll to the bottom when history changes
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [history]);

  // Focus the input field when the component mounts
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const executeCommand = async () => {
    if (!input.trim()) return;

    // Add command to history
    const newHistoryItem = {
      command: input,
      output: '',
      isError: false,
      isLoading: true
    };

    setHistory([...history, newHistoryItem]);
    
    // Add to command history for up/down navigation
    setCommandHistory([...commandHistory, input]);
    setHistoryIndex(-1);
    
    // Clear input
    setInput('');
    
    // Set loading state
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/api/terminal', {
        command: input
      });

      // Check if this is a clear command
      if (response.data.output === "__CLEAR__") {
        // Clear the history except for the welcome message
        const welcomeMessage = history[0];
        setHistory([welcomeMessage]);
        setIsLoading(false);
        return;
      }

      // Update the history item with the response
      setHistory(prevHistory => {
        const updatedHistory = [...prevHistory];
        const lastIndex = updatedHistory.length - 1;
        
        updatedHistory[lastIndex] = {
          ...updatedHistory[lastIndex],
          output: response.data.output,
          isError: response.data.status !== 0,
          isLoading: false
        };
        
        return updatedHistory;
      });
    } catch (error) {
      console.error('Error executing command:', error);
      
      // Update the history item with the error
      setHistory(prevHistory => {
        const updatedHistory = [...prevHistory];
        const lastIndex = updatedHistory.length - 1;
        
        updatedHistory[lastIndex] = {
          ...updatedHistory[lastIndex],
          output: `Error: ${error.message}`,
          isError: true,
          isLoading: false
        };
        
        return updatedHistory;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    // Handle Enter key to execute command
    if (e.key === 'Enter') {
      executeCommand();
    }
    
    // Handle Up arrow to navigate command history
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (commandHistory.length > 0 && historyIndex < commandHistory.length - 1) {
        const newIndex = historyIndex + 1;
        setHistoryIndex(newIndex);
        setInput(commandHistory[commandHistory.length - 1 - newIndex]);
      }
    }
    
    // Handle Down arrow to navigate command history
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1;
        setHistoryIndex(newIndex);
        setInput(commandHistory[commandHistory.length - 1 - newIndex]);
      } else if (historyIndex === 0) {
        setHistoryIndex(-1);
        setInput('');
      }
    }
    
    // Handle Tab for auto-completion (basic implementation)
    if (e.key === 'Tab') {
      e.preventDefault();
      
      // Simple auto-completion for common commands
      const commonCommands = [
        'help', 'ls', 'cat', 'pwd', 'echo', 'date', 'whoami', 'clear',
        'ai:', 'ai:code:', 'ai:model:', 
        'file:list', 'file:view', 'file:run', 'file:create'
      ];
      
      for (const cmd of commonCommands) {
        if (cmd.startsWith(input) && cmd !== input) {
          setInput(cmd);
          break;
        }
      }
    }
  };

  // Format the output with syntax highlighting for code blocks
  const formatOutput = (output) => {
    if (!output) return null;
    
    // Split by code blocks
    const parts = output.split('```');
    
    return parts.map((part, index) => {
      // Even indices are regular text, odd indices are code blocks
      if (index % 2 === 0) {
        return <span key={index}>{part}</span>;
      } else {
        // This is a code block
        return (
          <pre key={index} className="code-block">
            <code>{part}</code>
          </pre>
        );
      }
    });
  };

  // Determine the CSS class for the output based on content
  const getOutputClass = (historyItem) => {
    if (historyItem.isError) return 'error-output';
    if (historyItem.command.startsWith('ai:')) return 'ai-output';
    if (historyItem.command.startsWith('file:')) return 'file-output';
    return 'command-output';
  };

  // Add a clearTerminal function
  const clearTerminal = () => {
    // Keep only the welcome message
    const welcomeMessage = history[0];
    setHistory([welcomeMessage]);
  };

  return (
    <div className="terminal-container">
      <div className="terminal-header">
        <div className="terminal-controls">
          <div className="terminal-control close"></div>
          <div className="terminal-control minimize"></div>
          <div className="terminal-control maximize"></div>
        </div>
        <div className="terminal-title">AI Terminal Agent</div>
        <div className="terminal-actions">
          <button 
            className="terminal-clear-btn" 
            onClick={clearTerminal}
            title="Clear terminal (clear)"
          >
            Clear
          </button>
        </div>
      </div>
      
      <div className="terminal-output" ref={outputRef}>
        <div className="command-history">
          {history.map((item, index) => (
            <div key={index} className="command-entry">
              {item.command && (
                <div>
                  <span className="command-prompt">$ </span>
                  <span className="command-text">{item.command}</span>
                </div>
              )}
              <div className={getOutputClass(item)}>
                {item.isLoading ? (
                  <div>Processing<span className="loading"></span></div>
                ) : (
                  formatOutput(item.output)
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className="terminal-input-container">
        <span className="terminal-prompt">$</span>
        <input
          type="text"
          className="terminal-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your command..."
          ref={inputRef}
          disabled={isLoading}
        />
        <button 
          className="terminal-button" 
          onClick={executeCommand}
          disabled={isLoading}
        >
          Execute
        </button>
      </div>
    </div>
  );
};

export default Terminal; 