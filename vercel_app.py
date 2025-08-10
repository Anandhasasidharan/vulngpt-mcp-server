"""
Vercel ASGI handler for FastAPI application
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from main import app
except ImportError:
    # Fallback import from parent directory
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from main import app

# Export the app for Vercel
app = app
