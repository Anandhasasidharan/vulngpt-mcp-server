"""
Vercel ASGI handler for FastAPI application
"""

# Import the simplified app
from app_simple import app

# Export the app for Vercel
# Vercel will use this as the ASGI application
# No need for handler functions in newer Vercel Python runtime
