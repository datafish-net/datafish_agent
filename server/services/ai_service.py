import os
import json
import aiohttp
import certifi
import ssl
from typing import Dict, Any, Optional, List
from api.models import CommandResponse
from core.config import OPENAI_API_KEY, OPENAI_MODEL

class AIService:
    """Service for interacting with OpenAI API"""
    
    @staticmethod
    async def generate_response(prompt: str, 
                               model: Optional[str] = None,
                               temperature: float = 0.7,
                               max_tokens: int = 1000) -> CommandResponse:
        """
        Generate a response from OpenAI API
        
        Args:
            prompt: The prompt to send to the model
            model: The model to use (defaults to config value)
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens in the response
            
        Returns:
            CommandResponse with the model's response
        """
        api_key = OPENAI_API_KEY
        masked_key = api_key[:8] + "*" * 10 + api_key[-4:] if api_key else ""
        print(f"Using API key: {masked_key}")
        
        if not api_key:
            return CommandResponse(
                output="Error: OpenAI API key not configured. Set the OPENAI_API_KEY environment variable.",
                status=1
            )
        
        model = model or OPENAI_MODEL

        try:
            # Create an SSL context using certifi's CA bundle
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
                
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                print(f"Sending request to OpenAI API with model: {model}")
                print(f"Prompt: {prompt}")
                
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"Error from OpenAI API: {error_text}")
                        return CommandResponse(
                            output=f"Error from OpenAI API (Status {response.status}): {error_text}",
                            status=1
                        )
                    
                    data = await response.json()
                    print(f"Received response from OpenAI API: {data}")
                    
                    # Extract the response text
                    response_text = data["choices"][0]["message"]["content"]
                    
                    # Include model info in the output
                    output = f"Model: {model}\n\n{response_text}"
                    
                    return CommandResponse(output=output, status=0)
                    
        except Exception as e:
            print(f"Exception in AI service: {str(e)}")
            return CommandResponse(
                output=f"Error calling OpenAI API: {str(e)}",
                status=1
            ) 

    @staticmethod
    async def generate_and_save_code(prompt: str, 
                               model: Optional[str] = None,
                               temperature: float = 0.7,
                               max_tokens: int = 2000,
                               auto_run: bool = True) -> CommandResponse:
        """
        Generate code from OpenAI API and save it to a file
        
        Args:
            prompt: The prompt to send to the model
            model: The model to use (defaults to config value)
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens in the response
            auto_run: Whether to automatically run the generated code
            
        Returns:
            CommandResponse with the result
        """
        # Enhance the prompt to ask for Python code
        enhanced_prompt = f"""
        Generate Python code for the following request. 
        Include a '# filename: appropriate_name.py' comment at the top.
        Make sure the code is complete, well-documented, and ready to run.
        Do not include markdown formatting or code block syntax (like ```python or ```).
        Just provide the raw Python code that can be directly executed.
        
        IMPORTANT: If the code requires user input, include a demo mode that runs with sample inputs
        automatically when the script is executed with a command line argument '--demo'.
        For example: if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--demo": # run with sample inputs
        
        Request: {prompt}
        """
        
        # Get the response from the AI
        response = await AIService.generate_response(enhanced_prompt, model, temperature, max_tokens)
        
        # If there was an error, return it
        if response.status != 0:
            return response
        
        # Extract just the code part
        ai_response = response.output
        if ai_response.startswith(f"Model:"):
            # Remove the model info line
            ai_response = ai_response.split("\n\n", 1)[1]
        
        # Clean up the code - remove markdown code block syntax if present
        cleaned_code = ai_response
        
        # Remove markdown code block syntax if present
        if "```python" in cleaned_code or "```" in cleaned_code:
            # Try to extract just the code between markdown code blocks
            import re
            code_block_pattern = r"```(?:python)?(.*?)```"
            code_blocks = re.findall(code_block_pattern, cleaned_code, re.DOTALL)
            
            if code_blocks:
                # Use the first code block found
                cleaned_code = code_blocks[0].strip()
            else:
                # If no code blocks found with regex, manually remove markdown syntax
                cleaned_code = cleaned_code.replace("```python", "").replace("```", "")
        
        # Create the file
        from services.file_service import FileService, FILES_DIR
        file_response = FileService.create_file(cleaned_code)
        
        # If file creation failed, return the error
        if file_response.status != 0:
            return file_response
        
        # If auto_run is enabled, run the file
        if auto_run:
            # Extract the filename from the response
            import re
            filename_match = re.search(r"File created successfully: ([\w\.-]+)", file_response.output)
            if filename_match:
                filename = filename_match.group(1)
                file_path = os.path.join(FILES_DIR, filename)
                
                # Check if the file contains input() calls (likely interactive)
                with open(file_path, 'r') as f:
                    file_content = f.read()
                    is_interactive = 'input(' in file_content
                
                # Run the file
                import subprocess
                import sys
                
                try:
                    # Create a message about running the file
                    run_message = f"\n🚀 Automatically running the file...\n\n"
                    
                    # If the script is interactive, run it with --demo flag
                    if is_interactive:
                        run_message += "Detected interactive script, running in demo mode...\n\n"
                        result = subprocess.run(
                            [sys.executable, file_path, "--demo"],
                            capture_output=True,
                            text=True,
                            timeout=10  # 10 second timeout
                        )
                    else:
                        # Run the Python file normally
                        result = subprocess.run(
                            [sys.executable, file_path],
                            capture_output=True,
                            text=True,
                            timeout=10  # 10 second timeout
                        )
                    
                    # Format the output
                    if result.returncode == 0:
                        if result.stdout.strip():
                            run_message += f"Output:\n{result.stdout}\n"
                        else:
                            run_message += "The script ran successfully with no output.\n"
                    else:
                        run_message += f"Error running the script:\n{result.stderr}\n"
                    
                    # Combine the file creation message with the run message
                    return CommandResponse(
                        output=file_response.output + run_message,
                        status=0
                    )
                    
                except subprocess.TimeoutExpired:
                    # If the script times out, it might be waiting for input
                    if is_interactive:
                        return CommandResponse(
                            output=file_response.output + 
                                   "\n⚠️ The script appears to be interactive and is waiting for user input.\n" +
                                   f"To run it manually, use: python {file_path}\n" +
                                   "Or view the code with: file:view " + filename,
                            status=0
                        )
                    else:
                        return CommandResponse(
                            output=file_response.output + "\n⚠️ Script execution timed out after 10 seconds.",
                            status=0
                        )
                except Exception as e:
                    return CommandResponse(
                        output=file_response.output + f"\n⚠️ Error running the script: {str(e)}",
                        status=0
                    )
        
        # If auto_run is disabled or we couldn't extract the filename, just return the file creation response
        return file_response 