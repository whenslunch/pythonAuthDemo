import os

AUTHORITY = os.getenv("AUTHORITY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SESSION_TYPE = "filesystem"
SCOPE = os.getenv("SCOPE")
ENDPOINT = os.getenv("ENDPOINT")
PREFERRED_URL_SCHEME = 'https'  # Add this line for SSL