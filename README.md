# VulnGPT MCP Server

🔐 Production-ready MCP server for Puch AI Hackathon integration

## Features
- Bearer token authentication
- Phone number validation (Indian format: 919876543210)  
- Production security (CORS, rate limiting, error handling)
- Health checks and monitoring
- MCP protocol support

## Quick Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template)

## Local Testing

```bash
pip install -r requirements.txt
python main.py
```

Server runs on http://localhost:8000

## API Endpoints

- `GET /health` - Health check
- `POST /validate` - Token validation (requires Bearer token)
- `GET /docs` - API documentation

## Environment Variables

- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)

## Puch AI Integration

Connect to Puch AI:
```
/mcp connect https://your-server-url.railway.app your_bearer_token
```

## Bearer Tokens (Update for production)

```python
USER_DATABASE = {
    "your_token_here": "919876543210",
    "another_token": "918765432109",
}
```
