## Features

- Secure execution of whitelisted terminal commands
- Input validation and sanitization
- Configurable command timeout
- Detailed error handling
- Clean API for frontend integration

## API Endpoints

### Execute Terminal Command
- **URL**: `/api/terminal`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "command": "ls -la"
  }
  ```
- **Response**:
  ```json
  {
    "output": "total 24\ndrwxr-xr-x  5 user  staff   160 Oct 15 10:30 .\n...",
    "status": 0
  }
  ```

### Root Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "message": "AI Terminal Agent API is running"
  }
  ```

## Security

The API only allows execution of a predefined set of commands for security reasons. Attempting to execute unauthorized commands will result in an error response.

## Getting Started

### Prerequisites
- Python 3.8+
- FastAPI
- Uvicorn

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```
3. Run the server:
   ```bash
   cd server
   python app.py
   ```
4. The API will be available at http://localhost:8000

## Development

### Adding New Commands

To add new allowed commands, update the `ALLOWED_COMMANDS` set in `core/security.py`.

### Configuration

Adjust timeout and other settings in `core/config.py`.

## License

[MIT License](LICENSE)

# AI Integration

The terminal agent now supports direct interaction with OpenAI models through the `ai:` command prefix.

## Setup

1. Create a `.env` file in the server directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo
   ```

2. Install the required dependencies:
   ```bash
   pip install python-dotenv aiohttp
   ```

## Usage

- Send a prompt to the default AI model:
  ```
  ai:Write a short poem about coding
  ```

- Use a specific AI model:
  ```
  ai:model:gpt-4 Explain quantum computing
  ```

The response from the AI model will be displayed in the terminal.