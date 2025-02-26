import subprocess
import shlex
from api.models import CommandResponse
from core.config import COMMAND_TIMEOUT, OPENAI_MODEL
from core.security import ALLOWED_COMMANDS
from utils.helpers import get_help_text
from services.ai_service import AIService

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