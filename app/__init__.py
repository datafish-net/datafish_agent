from flask import Flask
from flask_cors import CORS
from flask_session import Session
from .config import Config
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables from .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, supports_credentials=True)
    Session(app)
    
    from .routes import integrations, knowledge
    app.register_blueprint(integrations.bp)
    app.register_blueprint(knowledge.bp)
    
    return app