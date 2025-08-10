"""
Ultra-simple MCP server for testing Puch AI connection
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def mcp_endpoint(request: Request):
    """Simple MCP JSON-RPC endpoint"""
    try:
        data = await request.json()
        method = data.get("method")
        request_id = data.get("id", 1)
        
        logger.info(f"Received method: {method}")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "vulngpt-mcp-server",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "validate",
                            "description": "Return phone number",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        }
                    ]
                }
            }
        
        elif method == "tools/call":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": "917305041960"}]
                }
            }
        
        else:
            return {
                "jsonrpc": "2.0", 
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": "Method not found"
                }
            }
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
