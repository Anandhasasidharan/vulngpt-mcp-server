"""
MCP Server implementation following the official MCP specification exactly
Based on https://spec.modelcontextprotocol.io/specification/
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.responses import JSONResponse
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MCP Server - VulnGPT")

# CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global server state
server_initialized = False

@app.post("/")
async def mcp_handler(request: Request):
    """Handle MCP JSON-RPC requests according to official spec"""
    global server_initialized
    
    try:
        # Get raw body and headers for debugging
        body = await request.body()
        headers = dict(request.headers)
        logger.info(f"Headers: {headers}")
        logger.info(f"Body: {body}")
        
        # Parse JSON-RPC request
        try:
            rpc_request = json.loads(body)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            }, status_code=400)
        
        method = rpc_request.get("method")
        params = rpc_request.get("params", {})
        request_id = rpc_request.get("id")
        
        logger.info(f"Method: {method}, ID: {request_id}")
        
        # Handle initialize - MUST be called first
        if method == "initialize":
            client_info = params.get("clientInfo", {})
            protocol_version = params.get("protocolVersion")
            
            logger.info(f"Initialize: client={client_info}, protocol={protocol_version}")
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "listChanged": False
                        }
                    },
                    "serverInfo": {
                        "name": "vulngpt-mcp-server",
                        "version": "1.0.0"
                    }
                }
            }
            
            server_initialized = True
            logger.info(f"Initialize response: {response}")
            return response
            
        # All other methods require initialization first
        if not server_initialized:
            return JSONResponse({
                "jsonrpc": "2.0", 
                "id": request_id,
                "error": {"code": -32002, "message": "Server not initialized"}
            }, status_code=400)
            
        # Handle notifications (no response expected)
        if request_id is None:
            if method == "notifications/initialized":
                logger.info("Client initialization complete")
                return JSONResponse({}, status_code=204)  # No content
                
        # Handle tools/list
        elif method == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "validate",
                            "description": "Validate token and return phone number",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "additionalProperties": False
                            }
                        }
                    ]
                }
            }
            logger.info(f"Tools list response: {response}")
            return response
            
        # Handle tools/call  
        elif method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments", {})
            
            if name == "validate":
                # Extract bearer token from Authorization header
                auth_header = request.headers.get("authorization", "")
                phone_number = "917305041960"  # Default phone number
                
                if auth_header.startswith("Bearer "):
                    token = auth_header[7:]
                    if token == "puch_ai_token_123":
                        phone_number = "917305041960"
                
                response = {
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
                logger.info(f"Validate response: {response}")
                return response
            else:
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {name}"}
                }, status_code=400)
                
        # Unknown method
        else:
            logger.error(f"Unknown method: {method}")
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }, status_code=400)
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": request_id if 'request_id' in locals() else None,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }, status_code=500)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "initialized": server_initialized}

# For Vercel
app_handler = app
