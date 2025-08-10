"""
Production-ready MCP Server for Puch AI Integration
FastAPI implementation with HTTPS support and validation endpoint
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import os
import logging
import uvicorn
from typing import Dict, Optional
import hashlib
import hmac
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VulnGPT MCP Server",
    description="Model Context Protocol Server for Puch AI Integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your needs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Mock user database (replace with real database in production)
# Format: {bearer_token: phone_number}
USER_DATABASE = {
    # Example tokens - replace with your actual tokens
    "puch_ai_token_123": "919876543210",
    "demo_token_456": "918765432109",
    "test_token_789": "917654321098",
}

# Environment variables
MCP_SERVER_SECRET = os.getenv("MCP_SERVER_SECRET", "your-secret-key-here")
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

# Response models
class ValidationResponse(BaseModel):
    success: bool
    phone_number: str = Field(..., pattern=r"^91\d{10}$")
    message: str = "Token validated successfully"

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str

class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    server: str = "VulnGPT MCP Server"

# Utility functions
def validate_phone_format(phone: str) -> bool:
    """Validate Indian phone number format (919876543210)"""
    return phone.startswith("91") and len(phone) == 12 and phone[2:].isdigit()

def authenticate_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Authenticate bearer token"""
    token = credentials.credentials
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if token exists in database
    if token not in USER_DATABASE:
        logger.warning(f"Invalid token attempted: {token[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token

# Routes
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint - Server information"""
    return {
        "message": "VulnGPT MCP Server is running",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "validate": "/validate",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse()

@app.post("/validate", response_model=ValidationResponse)
async def validate_token(token: str = Depends(authenticate_token)):
    """
    Validate bearer token and return user's phone number
    
    This endpoint is required by Puch AI for MCP server validation.
    Returns phone number in Indian format (919876543210).
    """
    try:
        phone_number = USER_DATABASE[token]
        
        # Validate phone format
        if not validate_phone_format(phone_number):
            logger.error(f"Invalid phone format for token {token[:10]}...: {phone_number}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid phone number format in database"
            )
        
        logger.info(f"Token validated successfully: {token[:10]}... -> {phone_number}")
        
        return ValidationResponse(
            success=True,
            phone_number=phone_number,
            message="Token validated successfully"
        )
        
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found or expired"
        )
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during validation"
        )

@app.get("/validate", response_model=ValidationResponse)
async def validate_token_get(token: str = Depends(authenticate_token)):
    """GET version of validate endpoint for testing"""
    return await validate_token(token)

# MCP Protocol endpoints (basic implementation)
@app.post("/mcp/initialize")
async def mcp_initialize():
    """MCP Protocol initialization"""
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {},
            "resources": {},
            "prompts": {}
        },
        "serverInfo": {
            "name": "vulngpt-mcp-server",
            "version": "1.0.0"
        }
    }

@app.post("/mcp/tools/list")
async def mcp_tools_list():
    """List available MCP tools"""
    return {
        "tools": [
            {
                "name": "vulnerability_scan",
                "description": "Scan code for security vulnerabilities",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repository_url": {"type": "string"},
                        "scan_type": {"type": "string", "enum": ["quick", "full"]}
                    },
                    "required": ["repository_url"]
                }
            }
        ]
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "message": f"HTTP {exc.status_code}: {exc.detail}"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )

# Create the FastAPI app instance
# This app will be imported by vercel_app.py

# For local development, uncomment the code below:
# if __name__ == "__main__":
#     import uvicorn
#     print(f"🚀 Starting VulnGPT MCP Server on {HOST}:{PORT}")
#     print(f"📋 API Documentation: http://{HOST}:{PORT}/docs")
#     print(f"🔍 Health Check: http://{HOST}:{PORT}/health")  
#     print(f"✅ Validation Endpoint: http://{HOST}:{PORT}/validate")
#     
#     uvicorn.run(
#         "main:app",
#         host=HOST,
#         port=PORT,
#         reload=True,
#         log_level="info"
#     )
