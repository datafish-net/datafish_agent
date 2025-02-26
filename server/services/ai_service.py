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