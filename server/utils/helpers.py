def get_help_text() -> str:
    """
    Return the help text for available commands
    
    Returns:
        String containing help information
    """
    return """
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

AI Commands:
- ai:<prompt>: Send a prompt to the default AI model
- ai:model:<model_name> <prompt>: Use a specific AI model
- ai:code:<description>: Generate Python code and save to a file
- ai:code:<description> --no-run: Generate code without running it

File Commands:
- file:create <content>: Create a file with the given content
- file:list [extension]: List all generated files
- file:view <filename>: View the contents of a file
- file:run <filename> [--demo]: Run a Python file (--demo for interactive scripts)

Example: ls -la
Example: ai:Write a short poem about coding
Example: ai:code:Create a web scraper for news headlines
Example: file:list .py
Example: file:view fibonacci.py
Example: file:run calculator.py --demo
""" 