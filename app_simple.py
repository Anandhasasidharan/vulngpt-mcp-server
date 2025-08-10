"""
Minimal FastAPI app for Vercel deployment
This is a simplified version to ensure compatibility with Vercel serverless functions
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

# Configure logging for Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="VulnGPT MCP Server",
    description="MCP Server for Puch AI Integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# User database with bearer tokens
USER_DATABASE = {
    "puch_ai_token_123": "917305041960",  # Your actual phone number
    "demo_token_456": "918765432109",     # Demo token
    "test_token_789": "917654321098",     # Test token
}

# Response models
class ValidationResponse(BaseModel):
    success: bool = True
    phone_number: str
    message: str = "Token validated successfully"

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str

class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    server: str = "VulnGPT MCP Server"

# Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "VulnGPT MCP Server is running",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "validate": "/validate",
            "health": "/health"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse()

def authenticate_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Authenticate bearer token"""
    token = credentials.credentials
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required"
        )
    
    if token not in USER_DATABASE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return token

@app.post("/validate", response_model=ValidationResponse)
async def validate_token(token: str = Depends(authenticate_token)):
    """
    Validate bearer token and return user's phone number
    Required endpoint for Puch AI MCP server validation
    """
    try:
        phone_number = USER_DATABASE[token]
        
        # Validate phone format (12 digits starting with 91)
        if not (phone_number.startswith("91") and len(phone_number) == 12 and phone_number[2:].isdigit()):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid phone number format in database"
            )
        
        return ValidationResponse(
            success=True,
            phone_number=phone_number,
            message="Token validated successfully"
        )
        
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found"
        )
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during validation"
        )

# MCP protocol endpoints
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

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": f"An unexpected error occurred: {str(exc)}"
        }
    )

# For Vercel deployment
handler = app

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
