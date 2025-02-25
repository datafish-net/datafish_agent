from flask import Blueprint, request, redirect, url_for, session
import os
from ..services.auth_service import AuthService

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_service = AuthService()

@bp.route('/<platform>/login', methods=['GET'])
def platform_login(platform):
    """Start OAuth flow for a platform."""
    # Get OAuth URL for the platform
    auth_url = auth_service.get_auth_url(platform)
    return redirect(auth_url)

@bp.route('/<platform>/callback', methods=['GET'])
def platform_callback(platform):
    """Handle OAuth callback from platform."""
    code = request.args.get('code')
    tokens = auth_service.handle_callback(platform, code)
    # Store tokens in session or database
    session[f'{platform}_tokens'] = tokens
    return redirect('/dashboard')  # Redirect to frontend dashboard 