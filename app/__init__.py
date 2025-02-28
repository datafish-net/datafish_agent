from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Configure session
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Initialize Flask extensions
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    from app.routes.integrations import bp as integrations_bp
    app.register_blueprint(integrations_bp, url_prefix='/api/integrations')
    
    return app