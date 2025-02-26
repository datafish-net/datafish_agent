import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "../../components/ui/card";
import { ScrollArea } from "../../components/ui/scroll-area";
import { Badge } from "../../components/ui/badge";
import { Separator } from "../../components/ui/separator";
import { Loader2, Terminal, Code, Copy, CheckCircle2 } from "lucide-react";

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
        <div className="min-h-screen bg-[#0f1729] text-white">
            <div className="container mx-auto py-6 px-4">
                <div className="flex justify-between items-center mb-4">
                    <div>
                        <h1 className="text-2xl font-bold tracking-tight flex items-center">
                            <Terminal className="mr-2 h-6 w-6" />
                            AI Terminal Agent
                        </h1>
                        <p className="text-muted-foreground text-sm">
                            Execute commands and interact with the AI-powered terminal
                        </p>
                    </div>
                    <Button
                        variant="outline"
                        onClick={() => navigate('/dashboard')}
                        className="text-white border-gray-700 hover:bg-gray-800"
                    >
                        Back to Dashboard
                    </Button>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2">
                        <Card className="border-gray-700 bg-[#1a2236]">
                            <CardHeader className="border-b border-gray-700 bg-[#151b2e] rounded-t-lg flex flex-row items-center justify-between p-4">
                                <div className="flex items-center">
                                    <div className="flex space-x-2 mr-4">
                                        <div className="w-3 h-3 rounded-full bg-red-500"></div>
                                        <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                                        <div className="w-3 h-3 rounded-full bg-green-500"></div>
                                    </div>
                                    <CardTitle className="text-sm font-medium">terminal</CardTitle>
                                </div>
                                <div className="flex items-center">
                                    <Badge variant="outline" className="text-xs mr-2 bg-blue-900/30 text-blue-400 border-blue-800">
                                        {isLoading ? "Processing..." : "Ready"}
                                    </Badge>
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        onClick={copyToClipboard}
                                        className="h-8 w-8 text-gray-400 hover:text-white hover:bg-gray-700"
                                    >
                                        {copied ? <CheckCircle2 className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                                    </Button>
                                </div>
                            </CardHeader>
                            <CardContent className="p-0">
                                <ScrollArea
                                    ref={terminalRef}
                                    className="h-[60vh] rounded-b-md bg-[#1a2236] p-4 font-mono text-sm"
                                >
                                    {history.length === 0 ? (
                                        <div className="text-gray-500 italic flex items-center">
                                            <Code className="mr-2 h-4 w-4" />
                                            <span>Type a command below to get started...</span>
                                        </div>
                                    ) : (
                                        <div className="space-y-2">
                                            {history.map((item, index) => (
                                                <div key={index} className="pb-2">
                                                    {item.type === 'input' ? (
                                                        <div className="flex">
                                                            <span className="text-green-500 font-semibold">$</span>
                                                            <span className="ml-2 text-blue-400">{item.content}</span>
                                                        </div>
                                                    ) : item.type === 'error' ? (
                                                        <div className="text-red-400 pl-4">{item.content}</div>
                                                    ) : (
                                                        <div className="text-gray-300 whitespace-pre-wrap pl-4 border-l border-gray-700 my-2">{item.content}</div>
                                                    )}
                                                </div>
                                            ))}
                                            {isLoading && (
                                                <div className="flex items-center text-yellow-500 animate-pulse">
                                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                                    <span>Processing command...</span>
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </ScrollArea>
                            </CardContent>
                            <CardFooter className="border-t border-gray-700 p-2">
                                <form onSubmit={handleSubmit} className="flex w-full gap-2">
                                    <div className="flex items-center text-green-500 font-mono pr-2">
                                        $
                                    </div>
                                    <Input
                                        type="text"
                                        value={input}
                                        onChange={(e) => setInput(e.target.value)}
                                        placeholder="Type your command..."
                                        disabled={isLoading}
                                        className="font-mono bg-[#151b2e] border-gray-700 text-white focus:ring-blue-500 focus:border-blue-500"
                                    />
                                    <Button
                                        type="submit"
                                        disabled={isLoading}
                                        className="bg-blue-600 hover:bg-blue-700 text-white"
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

                    <div className="lg:col-span-1">
                        <Card className="border-gray-700 bg-[#1a2236]">
                            <CardHeader className="border-b border-gray-700 bg-[#151b2e] rounded-t-lg">
                                <CardTitle className="text-lg">Command Reference</CardTitle>
                                <CardDescription className="text-gray-400">
                                    Available commands for the terminal
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="p-4 space-y-4">
                                <div>
                                    <h3 className="text-sm font-medium text-blue-400 mb-2">File System</h3>
                                    <div className="space-y-2">
                                        <div className="bg-[#151b2e] p-2 rounded border border-gray-700">
                                            <code className="text-yellow-300">ls -la</code>
                                            <p className="text-xs text-gray-400 mt-1">List all files with details</p>
                                        </div>
                                        <div className="bg-[#151b2e] p-2 rounded border border-gray-700">
                                            <code className="text-yellow-300">pwd</code>
                                            <p className="text-xs text-gray-400 mt-1">Show current directory</p>
                                        </div>
                                    </div>
                                </div>

                                <div>
                                    <h3 className="text-sm font-medium text-blue-400 mb-2">Python</h3>
                                    <div className="space-y-2">
                                        <div className="bg-[#151b2e] p-2 rounded border border-gray-700">
                                            <code className="text-yellow-300">python -c "print('Hello')"</code>
                                            <p className="text-xs text-gray-400 mt-1">Run Python code</p>
                                        </div>
                                    </div>
                                </div>

                                <div>
                                    <h3 className="text-sm font-medium text-blue-400 mb-2">Help</h3>
                                    <div className="bg-[#151b2e] p-2 rounded border border-gray-700">
                                        <code className="text-yellow-300">help</code>
                                        <p className="text-xs text-gray-400 mt-1">Show all available commands</p>
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


