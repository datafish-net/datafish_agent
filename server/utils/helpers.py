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

Example: ls -la
""" 