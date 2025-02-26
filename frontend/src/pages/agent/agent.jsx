import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "../../components/ui/card";
import { Loader2, Terminal, Copy, CheckCircle2 } from "lucide-react";
import "./agent.css";

function Agent() {
    const [input, setInput] = useState('');
    const [history, setHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [copied, setCopied] = useState(false);
    const terminalRef = useRef(null);
    const navigate = useNavigate();

    // Auto-scroll to bottom of terminal when history updates
    useEffect(() => {
        if (terminalRef.current) {
            terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
        }
    }, [history]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        // Add user input to history
        const userCommand = { type: 'input', content: input };
        setHistory(prev => [...prev, userCommand]);
        setIsLoading(true);

        try {
            // Call backend API
            const response = await fetch('http://localhost:8000/api/terminal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: input }),
            });

            const data = await response.json();

            // Add response to history
            const agentResponse = { type: 'output', content: data.output };
            setHistory(prev => [...prev, agentResponse]);
        } catch (error) {
            // Add error to history
            const errorResponse = {
                type: 'error',
                content: 'Error connecting to agent. Please try again.'
            };
            setHistory(prev => [...prev, errorResponse]);
            console.error('Error:', error);
        }

        setIsLoading(false);
        setInput('');
    };

    const copyToClipboard = () => {
        const text = history.map(item => {
            if (item.type === 'input') {
                return `$ ${item.content}`;
            } else {
                return item.content;
            }
        }).join('\n');

        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="agent-container">
            <div className="agent-content">
                <div className="agent-header">
                    <div>
                        <h1 className="agent-title">
                            <Terminal className="h-6 w-6" />
                            AI Terminal Agent
                        </h1>
                        <p className="agent-subtitle">
                            Execute commands and interact with the AI-powered terminal
                        </p>
                    </div>
                    <Button
                        variant="outline"
                        onClick={() => navigate('/dashboard')}
                        className="border-white hover:bg-white"
                    >
                        Back to Dashboard
                    </Button>
                </div>

                <div className="agent-grid">
                    <div>
                        <Card className="terminal-card">
                            <CardHeader className="terminal-header">
                                <CardTitle className="terminal-title">Terminal</CardTitle>
                                <div className="terminal-status">
                                    {isLoading ? "Processing..." : "Ready"}
                                </div>
                            </CardHeader>
                            <div className="terminal-actions">
                                <button
                                    onClick={copyToClipboard}
                                    className="terminal-copy-button"
                                    disabled={history.length === 0}
                                >
                                    {copied ? (
                                        <>
                                            <CheckCircle2 className="h-4 w-4" />
                                            Copied!
                                        </>
                                    ) : (
                                        <>
                                            <Copy className="h-4 w-4" />
                                            Copy
                                        </>
                                    )}
                                </button>
                            </div>
                            <CardContent>
                                <div className="terminal-content" ref={terminalRef}>
                                    {history.length === 0 ? (
                                        <div className="text-white">
                                            Type a command below to get started...
                                        </div>
                                    ) : (
                                        <div>
                                            {history.map((item, index) => (
                                                <div key={index} className="mb-2">
                                                    {item.type === 'input' ? (
                                                        <div className="terminal-command">
                                                            <span className="terminal-command-prompt">$</span>
                                                            <span className="terminal-command-text">{item.content}</span>
                                                        </div>
                                                    ) : item.type === 'error' ? (
                                                        <div className="terminal-error">{item.content}</div>
                                                    ) : (
                                                        <div className="terminal-output">{item.content}</div>
                                                    )}
                                                </div>
                                            ))}
                                            {isLoading && (
                                                <div className="terminal-loading">
                                                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                                                    <span>Processing command...</span>
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </CardContent>
                            <CardFooter className="terminal-input-container">
                                <form onSubmit={handleSubmit} className="w-full flex gap-2">
                                    <div className="terminal-prompt">
                                        $
                                    </div>
                                    <Input
                                        type="text"
                                        value={input}
                                        onChange={(e) => setInput(e.target.value)}
                                        placeholder="Type your command..."
                                        disabled={isLoading}
                                        className="terminal-input"
                                    />
                                    <Button
                                        type="submit"
                                        disabled={isLoading}
                                        className="bg-blue-600 hover:bg-blue-700"
                                    >
                                        {isLoading ? (
                                            <>
                                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                                Running
                                            </>
                                        ) : "Execute"}
                                    </Button>
                                </form>
                            </CardFooter>
                        </Card>
                    </div>

                    <div>
                        <Card className="command-card">
                            <CardHeader className="command-header">
                                <CardTitle>Command Reference</CardTitle>
                                <CardDescription>
                                    Available commands for the terminal
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="p-4 space-y-4">
                                <div className="command-section">
                                    <h3 className="command-section-title">File System</h3>
                                    <div>
                                        <div className="command-item">
                                            <code className="command-code">ls -la</code>
                                            <p className="command-description">List all files with details</p>
                                        </div>
                                        <div className="command-item">
                                            <code className="command-code">pwd</code>
                                            <p className="command-description">Show current directory</p>
                                        </div>
                                    </div>
                                </div>

                                <div className="command-section">
                                    <h3 className="command-section-title">Python</h3>
                                    <div>
                                        <div className="command-item">
                                            <code className="command-code">python -c "print('Hello')"</code>
                                            <p className="command-description">Run Python code</p>
                                        </div>
                                    </div>
                                </div>

                                <div className="command-section">
                                    <h3 className="command-section-title">Help</h3>
                                    <div className="command-item">
                                        <code className="command-code">help</code>
                                        <p className="command-description">Show all available commands</p>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Agent;


