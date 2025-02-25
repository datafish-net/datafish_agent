from typing import Dict
import os
import requests

class AuthService:
    def __init__(self):
        self.oauth_configs = {
            'quickbooks': {
                'auth_url': 'https://appcenter.intuit.com/connect/oauth2',
                'token_url': 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer',
                'client_id': os.getenv('QUICKBOOKS_CLIENT_ID'),
                'client_secret': os.getenv('QUICKBOOKS_CLIENT_SECRET'),
                'scope': 'com.intuit.quickbooks.accounting',
                'redirect_uri': 'http://localhost:5000/api/auth/quickbooks/callback'
            },
            'fulfill': {
                'auth_url': 'https://fulfill.com/oauth/authorize',
                'token_url': 'https://fulfill.com/oauth/token',
                'client_id': os.getenv('FULFILL_CLIENT_ID'),
                'client_secret': os.getenv('FULFILL_CLIENT_SECRET'),
                'scope': 'read write',
                'redirect_uri': 'http://localhost:5000/api/auth/fulfill/callback'
            }
        }

    def get_auth_url(self, platform: str) -> str:
        """Generate OAuth URL for platform."""
        config = self.oauth_configs[platform]
        return f"{config['auth_url']}?client_id={config['client_id']}&response_type=code&scope={config['scope']}&redirect_uri={config['redirect_uri']}"

    def handle_callback(self, platform: str, code: str) -> Dict:
        """Exchange OAuth code for tokens."""
        config = self.oauth_configs[platform]
        
        # Exchange authorization code for tokens
        response = requests.post(
            config['token_url'],
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': config['client_id'],
                'client_secret': config['client_secret'],
                'redirect_uri': config['redirect_uri']
            },
            headers={
                'Accept': 'application/json'
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get tokens: {response.text}")
            
        return response.json() 