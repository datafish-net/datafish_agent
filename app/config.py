import os

class Config:
    CORS_ORIGINS = os.environ.get('FRONTEND_URL', 'http://localhost:3000')