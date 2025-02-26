import os
import logging
from typing import Optional
from api.models import CommandResponse

logger = logging.getLogger("terminal-api")

# Directory for storing generated files
FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated_files")
os.makedirs(FILES_DIR, exist_ok=True)
logger.info(f"Files directory: {FILES_DIR}")

class FileService:
    """Service for managing files"""
    
    # Add FILES_DIR as a class attribute
    FILES_DIR = FILES_DIR
    
    @staticmethod
    def create_file(content: str, filename: Optional[str] = None, extension: str = ".py") -> CommandResponse:
        """
        Create a file with the given content
        
        Args:
            content: The content to write to the file
            filename: Optional filename (without extension)
            extension: File extension (default: .py)
            
        Returns:
            CommandResponse with the result
        """
        try:
            # Clean up the content - remove any leading/trailing whitespace
            content = content.strip()
            
            # If it's a Python file, validate the syntax
            if extension == ".py":
                try:
                    # Try to compile the code to check for syntax errors
                    compile(content, "<string>", "exec")
                    logger.info("Python code validation successful")
                except SyntaxError as e:
                    logger.warning(f"Python syntax error in generated code: {str(e)}")
                    # We'll still create the file, but warn the user
                    return CommandResponse(
                        output=f"⚠️ Warning: The generated Python code contains syntax errors: {str(e)}\n"
                               f"The file will be created, but may not run correctly.",
                        status=1
                    )
            
            # Extract filename from content if not provided
            if not filename:
                # Look for a filename comment in the first 5 lines
                lines = content.split('\n')[:5]
                for line in lines:
                    if line.startswith("# filename:") or line.startswith("#filename:"):
                        filename = line.split(":", 1)[1].strip()
                        break
            
            # If still no filename, generate a random one
            if not filename:
                import uuid
                filename = f"ai_generated_{uuid.uuid4().hex[:8]}"
            
            # Ensure the filename has the correct extension
            if not filename.endswith(extension):
                filename += extension
            
            # Create the full path
            file_path = os.path.join(FILES_DIR, filename)
            
            # Write the content to the file
            with open(file_path, 'w') as f:
                f.write(content)
            
            logger.info(f"Created file: {file_path}")
            
            # For Python files, add instructions on how to run it
            if extension == ".py":
                return CommandResponse(
                    output=f"✅ File created successfully: {filename}\n\n"
                           f"You can run it with: python {file_path}",
                    status=0
                )
            else:
                return CommandResponse(
                    output=f"✅ File created successfully: {filename}\n\n"
                           f"File path: {file_path}",
                    status=0
                )
            
        except Exception as e:
            logger.error(f"Error creating file: {str(e)}", exc_info=True)
            return CommandResponse(
                output=f"❌ Error creating file: {str(e)}",
                status=1
            )
    
    @staticmethod
    def list_files(extension: Optional[str] = None) -> CommandResponse:
        """
        List all files in the generated files directory
        
        Args:
            extension: Optional file extension filter
            
        Returns:
            CommandResponse with the list of files
        """
        try:
            files = os.listdir(FILES_DIR)
            
            if extension:
                files = [f for f in files if f.endswith(extension)]
            
            if not files:
                return CommandResponse(
                    output="No files found.",
                    status=0
                )
            
            output = "📁 Generated Files:\n\n"
            for i, file in enumerate(files, 1):
                file_path = os.path.join(FILES_DIR, file)
                size = os.path.getsize(file_path)
                modified = os.path.getmtime(file_path)
                
                # Format the size
                if size < 1024:
                    size_str = f"{size} bytes"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
                
                # Format the modified time
                from datetime import datetime
                modified_str = datetime.fromtimestamp(modified).strftime("%Y-%m-%d %H:%M:%S")
                
                output += f"{i}. {file} ({size_str}, modified: {modified_str})\n"
            
            return CommandResponse(
                output=output,
                status=0
            )
            
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}", exc_info=True)
            return CommandResponse(
                output=f"❌ Error listing files: {str(e)}",
                status=1
            )
    
    @staticmethod
    def run_file(filename: str, demo_mode: bool = False) -> CommandResponse:
        """
        Run a Python file
        
        Args:
            filename: The name of the file to run
            demo_mode: Whether to run in demo mode (for interactive scripts)
            
        Returns:
            CommandResponse with the result
        """
        try:
            # Ensure the filename has the correct extension if not provided
            if not filename.endswith('.py'):
                filename += '.py'
            
            file_path = os.path.join(FILES_DIR, filename)
            
            if not os.path.exists(file_path):
                return CommandResponse(
                    output=f"Error: File not found: {filename}",
                    status=1
                )
            
            # Check if the file contains input() calls (likely interactive)
            with open(file_path, 'r') as f:
                file_content = f.read()
                is_interactive = 'input(' in file_content
            
            # Run the Python file
            import subprocess
            import sys
            
            logger.info(f"Running file: {file_path}")
            
            # Format the output
            output = f"🚀 Running {filename}...\n\n"
            
            # If the script is interactive and demo_mode is requested, run with --demo flag
            if is_interactive and demo_mode:
                output += "Running in demo mode...\n\n"
                result = subprocess.run(
                    [sys.executable, file_path, "--demo"],
                    capture_output=True,
                    text=True,
                    timeout=10  # 10 second timeout
                )
            elif is_interactive:
                # For interactive scripts without demo mode, warn the user
                return CommandResponse(
                    output=output + 
                           "⚠️ This script appears to be interactive and requires user input.\n" +
                           "It cannot be run directly from the terminal agent.\n" +
                           f"To run it manually, use: python {file_path}\n" +
                           "Or run it in demo mode with: file:run " + filename + " --demo",
                    status=0
                )
            else:
                # Run non-interactive scripts normally
                result = subprocess.run(
                    [sys.executable, file_path],
                    capture_output=True,
                    text=True,
                    timeout=10  # 10 second timeout
                )
            
            # Format the result output
            if result.returncode == 0:
                if result.stdout.strip():
                    output += f"Output:\n{result.stdout}\n"
                else:
                    output += "The script ran successfully with no output.\n"
            else:
                output += f"Error running the script:\n{result.stderr}\n"
            
            return CommandResponse(
                output=output,
                status=result.returncode
            )
            
        except subprocess.TimeoutExpired:
            return CommandResponse(
                output=f"⚠️ Script execution timed out after 10 seconds.",
                status=124
            )
        except Exception as e:
            logger.error(f"Error running file: {str(e)}", exc_info=True)
            return CommandResponse(
                output=f"❌ Error running file: {str(e)}",
                status=1
            ) 