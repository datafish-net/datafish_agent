import subprocess
import shlex
import os
from api.models import CommandResponse
from core.config import COMMAND_TIMEOUT, OPENAI_MODEL
from core.security import ALLOWED_COMMANDS
from utils.helpers import get_help_text
from services.ai_service import AIService
from services.file_service import FileService

async def execute_terminal_command(command: str) -> CommandResponse:
    """
    Execute a terminal command and return the result
    
    Args:
        command: The command to execute
        
    Returns:
        CommandResponse with output and status
    """
    # Handle empty commands
    if not command:
        return CommandResponse(output="", status=0)
    
    # Handle help command
    if command == "help":
        return CommandResponse(output=get_help_text(), status=0)
    
    # Handle AI commands
    if command.startswith("ai:"):
        return await handle_ai_command(command[3:].strip())
    
    # Handle file commands
    if command.startswith("file:"):
        return await handle_file_command(command[5:].strip())
    
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
            timeout=COMMAND_TIMEOUT,
        )
        
        output = process.stdout
        if process.stderr:
            output += f"\nError: {process.stderr}"
            
        return CommandResponse(output=output, status=process.returncode)
        
    except subprocess.TimeoutExpired:
        return CommandResponse(
            output=f"Command timed out after {COMMAND_TIMEOUT} seconds",
            status=124
        )
    except Exception as e:
        return CommandResponse(
            output=f"Error executing command: {str(e)}",
            status=1
        )

async def handle_ai_command(prompt: str) -> CommandResponse:
    """
    Handle AI commands by sending them to the OpenAI API
    
    Args:
        prompt: The prompt to send to the AI model
        
    Returns:
        CommandResponse with the AI's response
    """
    # Check for empty prompt
    if not prompt:
        return CommandResponse(
            output="Error: Empty prompt. Usage: ai:<your prompt here>",
            status=1
        )
    
    # Handle code generation command
    if prompt.startswith("code:"):
        # Check if auto-run is disabled with --no-run flag
        auto_run = True
        if "--no-run" in prompt:
            auto_run = False
            prompt = prompt.replace("--no-run", "").strip()
        
        code_prompt = prompt[5:].strip()
        processing_message = "🤖 Generating Python code...\n"
        processing_message += f"Prompt: \"{code_prompt}\"\n\n"
        
        response = await AIService.generate_and_save_code(code_prompt, model=OPENAI_MODEL, auto_run=auto_run)
        
        # If successful, return the response
        if response.status == 0:
            return CommandResponse(
                output=processing_message + response.output,
                status=0
            )
        
        # If there was an error, return it
        return response
    
    # Print a message indicating that the AI is processing
    processing_message = "🤖 Processing your request...\n"
    
    # Special case for model selection
    if prompt.startswith("model:"):
        parts = prompt.split(" ", 1)
        if len(parts) < 2:
            return CommandResponse(
                output="Error: Missing prompt after model selection. Usage: ai:model:<model_name> <prompt>",
                status=1
            )
        
        model = parts[0][6:]  # Remove "model:" prefix
        user_prompt = parts[1]
        
        # Print what we're doing
        processing_message += f"Using model: {model}\n"
        processing_message += f"Prompt: \"{user_prompt}\"\n\n"
        
        response = await AIService.generate_response(user_prompt, model=model)
    else:
        # Default case - use default model
        processing_message += f"Using default model: {OPENAI_MODEL}\n"
        processing_message += f"Prompt: \"{prompt}\"\n\n"
        
        response = await AIService.generate_response(prompt)
    
    # If successful, format the output nicely
    if response.status == 0:
        # Extract just the response text (without the model info)
        ai_response = response.output
        if ai_response.startswith(f"Model: {OPENAI_MODEL}\n\n"):
            ai_response = ai_response[len(f"Model: {OPENAI_MODEL}\n\n"):]
        
        # Format the output with a nice border
        formatted_output = processing_message
        formatted_output += "┌" + "─" * 50 + "┐\n"
        
        # Split the response into lines and add borders
        for line in ai_response.split('\n'):
            # Handle long lines by wrapping them
            while len(line) > 48:
                formatted_output += "│ " + line[:48] + " │\n"
                line = line[48:]
            formatted_output += "│ " + line.ljust(48) + " │\n"
        
        formatted_output += "└" + "─" * 50 + "┘"
        
        return CommandResponse(output=formatted_output, status=0)
    
    # If there was an error, return it as is
    return response 

async def handle_file_command(command: str) -> CommandResponse:
    """
    Handle file-related commands
    
    Args:
        command: The file command to execute
        
    Returns:
        CommandResponse with the result
    """
    # Check for empty command
    if not command:
        return CommandResponse(
            output="Error: Empty file command. Available commands: create, list, view, cat, run",
            status=1
        )
    
    # Split the command into parts
    parts = command.split(" ", 1)
    action = parts[0].lower()
    
    if action == "create":
        if len(parts) < 2:
            return CommandResponse(
                output="Error: Missing file content. Usage: file:create <content>",
                status=1
            )
        return FileService.create_file(parts[1])
    
    elif action == "list":
        extension = None
        if len(parts) > 1:
            extension = parts[1]
        return FileService.list_files(extension)
    
    elif action == "view" or action == "cat":
        if len(parts) < 2:
            return CommandResponse(
                output="Error: Missing filename. Usage: file:view <filename>",
                status=1
            )
        
        filename = parts[1]
        # Ensure the filename has the correct extension if not provided
        if not any(filename.endswith(ext) for ext in ['.py', '.txt', '.md', '.json', '.csv']):
            filename += '.py'  # Default to Python extension
        
        file_path = os.path.join(FILES_DIR, filename)
        
        if not os.path.exists(file_path):
            return CommandResponse(
                output=f"Error: File not found: {filename}",
                status=1
            )
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            return CommandResponse(
                output=f"📄 {filename}:\n\n{content}",
                status=0
            )
        except Exception as e:
            return CommandResponse(
                output=f"Error reading file: {str(e)}",
                status=1
            )
    
    elif action == "run":
        if len(parts) < 2:
            return CommandResponse(
                output="Error: Missing filename. Usage: file:run <filename> [--demo]",
                status=1
            )
        
        # Check for demo mode flag
        demo_mode = False
        filename = parts[1]
        if len(parts) > 2 and "--demo" in parts[1]:
            # Handle case where filename and flag are in the same part
            filename = parts[1].replace("--demo", "").strip()
            demo_mode = True
        elif len(parts) > 2 and "--demo" in " ".join(parts[2:]):
            # Handle case where flag is a separate part
            demo_mode = True
        
        return FileService.run_file(filename, demo_mode)
    
    else:
        return CommandResponse(
            output=f"Unknown file command: {action}\nAvailable commands: create, list, view, cat, run",
            status=1
        ) 