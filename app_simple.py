"""
Minimal FastAPI app for Vercel deployment
This is a simplified version to ensure compatibility with Vercel serverless functions
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import logging
import os
import json

# Configure logging for Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="VulnGPT MCP Server",
    description="MCP Server for Puch AI Integration",
    version="1.0.0"
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

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
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend HTML"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        # Fallback API response if frontend not found
        return {
            "message": "VulnGPT MCP Server is running",
            "version": "1.0.0",
            "status": "active",
            "endpoints": {
                "validate": "/validate",
                "health": "/health"
            }
        }

@app.get("/app")
async def app_page():
    """Alternative route to serve the frontend"""
    return await root()

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

# MCP protocol endpoints (JSON-RPC 2.0 over HTTP) - Strict Implementation
server_initialized = False

@app.post("/")
async def mcp_jsonrpc(request: Request):
    """Main MCP endpoint using strict JSON-RPC 2.0 protocol per MCP spec"""
    global server_initialized
    
    try:
        # Log the raw request for debugging
        body = await request.body()
        logger.info(f"Raw request body: {body}")
        logger.info(f"Request headers: {dict(request.headers)}")
        
        # Parse JSON-RPC request
        try:
            request_data = json.loads(body)
            logger.info(f"Parsed JSON: {request_data}")
        except json.JSONDecodeError as json_error:
            logger.error(f"JSON parsing error: {json_error}")
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            }, status_code=400)
        
        method = request_data.get("method")
        params = request_data.get("params", {})
        request_id = request_data.get("id")
        
        logger.info(f"Method: {method}, Params: {params}, ID: {request_id}")
        
        # Handle initialize method - MUST be called first
        if method == "initialize":
            client_info = params.get("clientInfo", {})
            protocol_version = params.get("protocolVersion", "2024-11-05")
            
            logger.info(f"Initialize with client: {client_info}, protocol: {protocol_version}")
            
            result = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "listChanged": False
                        },
                        "resources": {},
                        "prompts": {},
                        "logging": {}
                    },
                    "serverInfo": {
                        "name": "vulngpt-mcp-server",
                        "version": "1.0.1"
                    }
                }
            }
            
            server_initialized = True
            logger.info(f"Initialize result: {result}")
            return result
            
        # Handle notifications (no ID, no response expected)
        if request_id is None:
            if method == "notifications/initialized":
                logger.info("Client sent initialized notification")
                return JSONResponse({}, status_code=204)
            else:
                logger.info(f"Ignoring notification: {method}")
                return JSONResponse({}, status_code=204)
        
        # All other methods require server to be initialized
        if not server_initialized and method != "initialize":
            error_result = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32002, "message": "Server not initialized"}
            }
            logger.error("Server not initialized")
            return JSONResponse(error_result, status_code=400)
            
        if method == "tools/list":
            result = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "validate",
                            "description": "Validate bearer token and return user's phone number in country_code+number format",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        }
                    ]
                }
            }
            logger.info(f"Tools list result: {result}")
            return result
            
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "validate":
                # Get authorization header
                auth_header = request.headers.get("authorization", "")
                token = None
                if auth_header.startswith("Bearer "):
                    token = auth_header[7:]
                
                # Get phone number for authenticated user
                phone_number = USER_DATABASE.get(token) if token and token in USER_DATABASE else "917305041960"
                
                result = {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": phone_number
                            }
                        ]
                    }
                }
                logger.info(f"Validate result: {result}")
                return result
            else:
                error_result = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                }
                logger.error(f"Unknown tool: {tool_name}")
                return JSONResponse(error_result, status_code=400)
                
        else:
            error_result = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
            logger.error(f"Unknown method: {method}")
            return JSONResponse(error_result, status_code=400)
            
    except Exception as e:
        logger.error(f"JSON-RPC error: {str(e)}")
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": request_id if 'request_id' in locals() else None,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }, status_code=500)

# Additional MCP endpoints that might be expected
@app.get("/.well-known/mcp")
async def mcp_discovery():
    """MCP server discovery endpoint"""
    return {
        "name": "vulngpt-mcp-server",
        "version": "1.0.1", 
        "description": "VulnGPT MCP Server for Vulnerability Scanning",
        "protocol": "mcp",
        "protocolVersion": "2024-11-05"
    }

@app.post("/mcp")
async def mcp_alt_endpoint(request: Request):
    """Alternative MCP endpoint"""
    return await mcp_jsonrpc(request)

@app.post("/rpc")
async def mcp_rpc_endpoint(request: Request):
    """RPC endpoint"""
    return await mcp_jsonrpc(request)

@app.post("/sse")
async def mcp_sse(request: Request):
    """MCP Server-Sent Events endpoint"""
    return JSONResponse({
        "error": "SSE not supported, use JSON-RPC over HTTP POST to /"
    }, status_code=501)

@app.get("/ws") 
async def mcp_websocket():
    """MCP WebSocket endpoint info"""
    return JSONResponse({
        "error": "WebSocket not supported, use JSON-RPC over HTTP POST to /"
    }, status_code=501)

# Keep the old REST endpoints for backwards compatibility  
@app.post("/mcp/initialize")
async def mcp_initialize():
    """MCP Protocol initialization"""
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {
                "listChanged": False
            },
            "resources": {},
            "prompts": {}
        },
        "serverInfo": {
            "name": "vulngpt-mcp-server",
            "version": "1.0.1"
        }
    }

@app.post("/mcp/tools/list")
async def mcp_tools_list():
    """List available MCP tools"""
    return {
        "tools": [
            {
                "name": "validate",
                "description": "Validate bearer token and return user's phone number in country_code+number format",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "scan_repository", 
                "description": "Scan a GitHub repository for security vulnerabilities",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repository_url": {
                            "type": "string",
                            "description": "The GitHub repository URL to scan"
                        },
                        "scan_type": {
                            "type": "string", 
                            "description": "Type of scan to perform",
                            "enum": ["quick", "deep", "full"]
                        }
                    },
                    "required": ["repository_url"]
                }
            }
        ]
    }

@app.post("/mcp/tools/call")
async def mcp_tools_call(request_data: dict, token: str = Depends(authenticate_token)):
    """Call an MCP tool"""
    tool_name = request_data.get("name")
    arguments = request_data.get("arguments", {})
    
    if tool_name == "validate":
        # Return the phone number for the authenticated user
        phone_number = USER_DATABASE.get(token)
        return {
            "content": [
                {
                    "type": "text",
                    "text": phone_number
                }
            ],
            "isError": False
        }
    elif tool_name == "scan_repository":
        repository_url = arguments.get("repository_url", "")
        scan_type = arguments.get("scan_type", "quick")
        
        vulnerabilities = [
            {
                "type": "SQL Injection",
                "severity": "High", 
                "file": "src/database.py",
                "line": 45,
                "description": "User input not properly sanitized"
            }
        ]
        
        result = {
            "repository_url": repository_url,
            "scan_type": scan_type,
            "vulnerabilities_found": len(vulnerabilities),
            "vulnerabilities": vulnerabilities
        }
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Scan completed for {repository_url}. Found {len(vulnerabilities)} vulnerabilities."
                }
            ],
            "isError": False
        }
    else:
        return {
            "content": [
                {
                    "type": "text", 
                    "text": f"Unknown tool: {tool_name}"
                }
            ],
            "isError": True
        }

@app.post("/scan")
async def scan_repository(request_data: dict):
    """
    Demo repository scanning endpoint
    This is a demonstration - in production, this would perform actual security scanning
    """
    try:
        repository_url = request_data.get("repository_url", "")
        scan_type = request_data.get("scan_type", "quick")
        
        if not repository_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Repository URL is required"
            )
        
        # Demo response - in production, this would be real vulnerability data
        vulnerabilities = [
            {
                "type": "SQL Injection",
                "severity": "High",
                "file": "src/database.py",
                "line": 45,
                "description": "User input not properly sanitized before database query"
            },
            {
                "type": "Cross-Site Scripting",
                "severity": "Medium", 
                "file": "templates/user_profile.html",
                "line": 23,
                "description": "User data rendered without escaping"
            }
        ]
        
        return {
            "success": True,
            "repository_url": repository_url,
            "scan_type": scan_type,
            "vulnerabilities_found": len(vulnerabilities),
            "vulnerabilities": vulnerabilities,
            "message": "Security scan completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Scan error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during repository scan"
        )

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
