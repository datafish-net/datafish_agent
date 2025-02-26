import subprocess
import shlex
from api.models import CommandResponse
from core.config import COMMAND_TIMEOUT
from core.security import ALLOWED_COMMANDS
from utils.helpers import get_help_text

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