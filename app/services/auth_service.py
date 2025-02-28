from typing import Dict
import os
import requests
import uuid

class AuthService:
    def __init__(self):
        self.oauth_configs = {
            'quickbooks': {
                'auth_url': 'https://appcenter.intuit.com/connect/oauth2',
                'token_url': 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer',
                'client_id': os.environ.get('QUICKBOOKS_CLIENT_ID'),
                'client_secret': os.environ.get('QUICKBOOKS_CLIENT_SECRET'),
                'scope': 'com.intuit.quickbooks.accounting',
                'redirect_uri': 'http://localhost:5000/api/auth/quickbooks/callback'
            },
            'fulfill': {
                'auth_url': 'https://{subdomain}.fulfil.io/oauth/authorize',
                'token_url': 'https://{subdomain}.fulfil.io/oauth/token',
                'client_id': os.environ.get('FULFILL_CLIENT_ID'),
                'client_secret': os.environ.get('FULFILL_CLIENT_SECRET'),
                'scope': 'user_session,sale.channel:read',  # Update with your required scopes
                'redirect_uri': 'http://localhost:5000/api/auth/fulfill/callback',
                'subdomain': os.environ.get('FULFILL_SUBDOMAIN', 'demo')  # Replace with your customer's subdomain
            }
        }

    def get_authorization_url(self, platform):
        """Generate authorization URL for the specified platform"""
        config = self.oauth_configs[platform]
        state = str(uuid.uuid4())
        
        if platform == 'fulfill':
            auth_url = config['auth_url'].format(subdomain=config['subdomain'])
            params = {
                'client_id': config['client_id'],
                'response_type': 'code',
                'scope': config['scope'],
                'redirect_uri': config['redirect_uri'],
                'state': state,
                'access_type': 'offline_access'  # Request offline access for refresh token
            }
        else:
            auth_url = config['auth_url']
            params = {
                'client_id': config['client_id'],
                'response_type': 'code',
                'scope': config['scope'],
                'redirect_uri': config['redirect_uri'],
                'state': state
            }
        
        # Build URL with query parameters
        auth_url += '?'
        auth_url += '&'.join([f"{key}={value}" for key, value in params.items()])
        
        return auth_url

    def handle_callback(self, platform, code):
        """Exchange authorization code for access token"""
        config = self.oauth_configs[platform]
        
        if platform == 'fulfill':
            token_url = config['token_url'].format(subdomain=config['subdomain'])
            data = {
                'client_id': config['client_id'],
                'client_secret': config['client_secret'],
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': config['redirect_uri']
            }
        else:
            token_url = config['token_url']
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': config['client_id'],
                'client_secret': config['client_secret'],
                'redirect_uri': config['redirect_uri']
            }
        
        # Exchange authorization code for tokens
        response = requests.post(
            token_url,
            data=data,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get tokens: {response.text}")
            
        return response.json() 