from flask import Blueprint, redirect, request, session, jsonify, url_for
import os
from app.services.auth_service import AuthService

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_service = AuthService()

@bp.route('/quickbooks')
def quickbooks_auth():
    """Redirect to QuickBooks authorization page"""
    auth_url = auth_service.get_authorization_url('quickbooks')
    return redirect(auth_url)

@bp.route('/fulfill')
def fulfill_auth():
    """Redirect to Fulfill authorization page"""
    auth_url = auth_service.get_authorization_url('fulfill')
    return redirect(auth_url)

@bp.route('/<platform>/callback')
def callback(platform):
    """Handle OAuth callback"""
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'Authorization code not provided'}), 400
    
    try:
        # Exchange code for tokens
        token_data = auth_service.handle_callback(platform, code)
        
        # Store tokens in session
        session[f'{platform}_token'] = token_data.get('access_token')
        session[f'{platform}_refresh_token'] = token_data.get('refresh_token')
        
        return jsonify({
            'message': f'Successfully authenticated with {platform}',
            'access_token': token_data.get('access_token')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/fulfill-url')
def fulfill_url():
    """Return Fulfill authorization URL"""
    auth_url = auth_service.get_authorization_url('fulfill')
    return jsonify({'auth_url': auth_url}) 