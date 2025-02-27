import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Bot, User, Loader } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';
import './ChatbotPage.css';

const ChatbotPage = () => {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content: 'Hi there! I\'m your AI assistant. I can help you with tasks like generating code, answering questions, or running simple commands. What would you like to do today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message to chat
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    
    // Clear input and set loading state
    setInput('');
    setIsLoading(true);

    try {
      // Prepare the command - prefix with ai: to use the AI service
      const command = `ai:${input}`;
      
      // Call backend API
      const response = await axios.post('http://localhost:8000/api/terminal', {
        command: command
      });

      // Add bot response to chat
      const botMessage = { 
        role: 'bot', 
        content: response.data.output,
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to chat
      const errorMessage = { 
        role: 'bot', 
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAction = (action) => {
    switch(action) {
      case 'generate-code':
        setInput('Create a simple Python calculator');
        break;
      case 'explain-code':
        setInput('Explain how a binary search algorithm works');
        break;
      case 'data-analysis':
        setInput('How can I analyze CSV data with Python?');
        break;
      case 'web-dev':
        setInput('Create a simple HTML page with a form');
        break;
      default:
        break;
    }
  };

  // Custom components for ReactMarkdown
  const MarkdownComponents = {
    // Override code block rendering
    code({ node, inline, className, children, ...props }) {
      const match = /language-(\w+)/.exec(className || '');
      return !inline && match ? (
        <div className="code-block">
          <div className="code-language">{match[1]}</div>
          <pre>
            <code className={className} {...props}>
              {children}
            </code>
          </pre>
        </div>
      ) : (
        <code className={className} {...props}>
          {children}
        </code>
      );
    },
    // Override pre rendering to avoid duplicate pre tags
    pre({ children }) {
      return <>{children}</>;
    }
  };

  return (
    <div className="chatbot-page">
      <header className="chatbot-header">
        <div className="chatbot-title">
          <Bot size={24} />
          <h1>AI Assistant</h1>
        </div>
        <p>Ask me anything or let me help you with coding tasks</p>
      </header>

      <main className="chatbot-main">
        <div className="chat-container">
          <div className="messages-container">
            {messages.map((message, index) => (
              <div 
                key={index} 
                className={`message ${message.role === 'user' ? 'user-message' : 'bot-message'} ${message.isError ? 'error-message' : ''}`}
              >
                <div className="message-avatar">
                  {message.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                </div>
                <div className="message-content">
                  {message.role === 'user' ? (
                    message.content
                  ) : (
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      rehypePlugins={[rehypeRaw, rehypeHighlight]}
                      components={MarkdownComponents}
                    >
                      {message.content}
                    </ReactMarkdown>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message bot-message">
                <div className="message-avatar">
                  <Bot size={20} />
                </div>
                <div className="message-content loading">
                  <Loader size={20} className="spinner" />
                  Thinking...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="quick-actions">
            <button onClick={() => handleQuickAction('generate-code')}>Generate Code</button>
            <button onClick={() => handleQuickAction('explain-code')}>Explain Code</button>
            <button onClick={() => handleQuickAction('data-analysis')}>Data Analysis</button>
            <button onClick={() => handleQuickAction('web-dev')}>Web Development</button>
          </div>

          <form className="input-container" onSubmit={handleSubmit}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message here..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading || !input.trim()}>
              <Send size={20} />
            </button>
          </form>
        </div>
      </main>

      <footer className="chatbot-footer">
        <p>Powered by AI Terminal Agent</p>
      </footer>
    </div>
  );
};

export default ChatbotPage; 