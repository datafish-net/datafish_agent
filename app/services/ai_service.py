import openai
import os
from typing import Dict, List
import json

class AIService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def generate_integration_code(self, source_platform: str, target_platform: str, knowledge: Dict) -> Dict:
        """Generate complete integration code using AI."""
        prompt = self._build_integration_prompt(
            source_platform,
            target_platform,
            knowledge['documentation']
        )
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert system integrator. Generate Python code for integrating between different platforms.
                        Include all necessary authentication, API calls, data transformation, and error handling.
                        Return the response as a JSON object with the following structure:
                        {
                            "auth_code": "Python code for authentication",
                            "fetch_code": "Python code to fetch data from source",
                            "transform_code": "Python code to transform data",
                            "upload_code": "Python code to upload to target",
                            "requirements": ["list of required packages"]
                        }"""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating integration code: {str(e)}")
            return {}
    
    def _build_integration_prompt(self, source_platform: str, target_platform: str, documentation: Dict) -> str:
        """Build AI prompt for code generation."""
        return f"""
        Generate Python code to integrate between {source_platform} and {target_platform}.
        
        Source Platform ({source_platform}) Documentation:
        {documentation.get(source_platform, '')}
        
        Target Platform ({target_platform}) Documentation:
        {documentation.get(target_platform, '')}
        
        Requirements:
        1. Handle authentication for both platforms
        2. Fetch data from source platform
        3. Transform data to match target platform's format
        4. Upload transformed data to target platform
        5. Include error handling and logging
        6. Use async/await for API calls
        7. Include type hints
        
        Generate complete, production-ready Python code that can be executed directly.
        """