from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import shlex
import os
from typing import List, Dict, Any

app = FastAPI(title="AI Terminal Agent API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL (adjust if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    command: str

class CommandResponse(BaseModel):
    output: str
    status: int = 0

# Allowed commands for security
ALLOWED_COMMANDS = {
    "ls", "echo", "cat", "pwd", "date", "whoami", "uname", 
    "python", "python3", "node", "npm", "help"
}

# Custom help command
HELP_TEXT = """
Available commands:
- ls: List directory contents
- echo: Display a line of text
- cat: Concatenate files and print on the standard output
- pwd: Print working directory
- date: Print the system date and time
- whoami: Print the current user
- uname: Print system information
- python/python3: Run Python code
- node: Run JavaScript code
- npm: Node package manager
- help: Display this help message

Example: ls -la
"""

@app.post("/api/terminal", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    command = request.command.strip()
    
    # Handle empty commands
    if not command:
        return CommandResponse(output="", status=0)
    
    # Handle help command
    if command == "help":
        return CommandResponse(output=HELP_TEXT, status=0)
    
    # Parse the command to check if it's allowed
    try:
        args = shlex.split(command)
        base_command = args[0]
        
        if base_command not in ALLOWED_COMMANDS:
            return CommandResponse(
                output=f"Command not allowed: {base_command}\nType 'help' to see available commands.",
                status=1
            )
        
        # Execute the command
        process = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=10,  # Timeout after 10 seconds
        )
        
        output = process.stdout
        if process.stderr:
            output += f"\nError: {process.stderr}"
            
        return CommandResponse(output=output, status=process.returncode)
        
    except subprocess.TimeoutExpired:
        return CommandResponse(
            output="Command timed out after 10 seconds",
            status=124
        )
    except Exception as e:
        return CommandResponse(
            output=f"Error executing command: {str(e)}",
            status=1
        )

@app.get("/")
async def root():
    return {"message": "AI Terminal Agent API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 