# 🚀 Vercel Deployment Guide for VulnGPT MCP Server

## Method 1: Vercel Web Interface (Recommended - No CLI needed)

### Step 1: Push to GitHub

1. **Create a new GitHub repository:**
   - Go to [github.com](https://github.com) and click "New repository"
   - Name it: `vulngpt-mcp-server`
   - Set it as Public
   - Don't initialize with README (we have our files)

2. **Push your code to GitHub:**
   ```powershell
   # In your current directory (D:\PROJECTS\hackton\VulnGPT\mcp-server\python-fastapi)
   git init
   git add .
   git commit -m "Initial MCP server for Puch AI hackathon"
   git branch -M main
   git remote add origin https://github.com/yourusername/vulngpt-mcp-server.git
   git push -u origin main
   ```

### Step 2: Deploy with Vercel Web Interface

1. **Go to [vercel.com](https://vercel.com)**
2. **Sign up/Login** with your GitHub account
3. **Click "New Project"**
4. **Import your GitHub repository** (`vulngpt-mcp-server`)
5. **Configure deployment:**
   - Framework Preset: **Other**
   - Root Directory: **leave blank** (use root)
   - Build Command: **leave blank**
   - Install Command: `pip install -r requirements.txt`
   - Output Directory: **leave blank**
6. **Click "Deploy"**

### Step 3: Your Server URL

After deployment (2-3 minutes), you'll get:
- **Live URL:** `https://vulngpt-mcp-server.vercel.app`
- **Dashboard:** Manage from Vercel dashboard

## Method 2: Vercel CLI (If you install Node.js)

If you want to install Node.js and use CLI:

1. **Install Node.js** from [nodejs.org](https://nodejs.org)
2. **Install Vercel CLI:**
   ```powershell
   npm install -g vercel
   ```
3. **Deploy:**
   ```powershell
   vercel --prod
   ```

## 🧪 Testing Your Deployed Server

Once deployed, test your server:

```powershell
# Test health endpoint
Invoke-WebRequest -Uri "https://vulngpt-mcp-server.vercel.app/health"

# Test validation endpoint
$headers = @{"Authorization" = "Bearer puch_ai_token_123"; "Content-Type" = "application/json"}
Invoke-WebRequest -Uri "https://vulngpt-mcp-server.vercel.app/validate" -Method POST -Headers $headers

# Expected response: {"success": true, "phone_number": "919876543210", "message": "Token validated successfully"}
```

## 🏆 Submit to Puch AI Hackathon

Once your server is live:

```bash
# Submit to hackathon
/hackathon submission add vulngpt-mcp-server https://github.com/yourusername/vulngpt-mcp-server

# Check submission
/hackathon submission list

# Share with users
/mcp connect https://vulngpt-mcp-server.vercel.app puch_ai_token_123
```

## 🔧 Troubleshooting

### Common Issues:

1. **Build fails:**
   - Check that `requirements.txt` is present
   - Ensure `vercel.json` is configured correctly

2. **Server returns 404:**
   - Verify `vercel.json` routes are correct
   - Check that `main.py` is in root directory

3. **Module import errors:**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

### Vercel Logs:
- Check deployment logs in Vercel dashboard
- Use Functions tab to see runtime logs

## 📁 Files Required for Deployment

Make sure these files are in your repository:
- ✅ `main.py` (main server code)
- ✅ `requirements.txt` (Python dependencies)
- ✅ `vercel.json` (Vercel configuration)
- ✅ `README.md` (documentation)

## 🎯 Ready for Deployment!

Your MCP server is optimized for Vercel deployment with:
- ✅ Proper Vercel configuration
- ✅ FastAPI ASGI compatibility
- ✅ Production-ready security
- ✅ All required endpoints
- ✅ Bearer token authentication

**Next:** Follow the deployment steps above! 🚀
