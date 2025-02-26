# Application configuration settings
import os
import logging

# Set up logger
logger = logging.getLogger("terminal-api")

# Try to read the .env file manually
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
logger.info(f"Trying to read .env file from: {env_path}")

if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
                if key == "OPENAI_API_KEY":
                    masked = value[:8] + "*" * 10 + value[-4:] if value else ""
                    logger.info(f"Loaded API key from file: {masked}")

# Get API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
masked_key = OPENAI_API_KEY[:8] + "*" * 10 + OPENAI_API_KEY[-4:] if OPENAI_API_KEY else ""
logger.info(f"Using OpenAI API key: {masked_key}")

# Timeout for command execution in seconds
COMMAND_TIMEOUT = 10

# OpenAI API settings
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
logger.info(f"Using OpenAI model: {OPENAI_MODEL}") 