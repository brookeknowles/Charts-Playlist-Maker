"""Flask configuration."""
import os

TESTING = True
DEBUG = False
FLASK_ENV = 'development'
SECRET_KEY = "brooke's super secret key"

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', None)
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', None)
