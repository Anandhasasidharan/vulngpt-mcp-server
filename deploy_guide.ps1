Write-Host "🚀 VulnGPT MCP Server - Hackathon Deployment" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Error: main.py not found. Please run this from the python-fastapi directory" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Choose deployment option:" -ForegroundColor Yellow
Write-Host "1. Railway (Recommended - Free tier with GitHub)"
Write-Host "2. Render (Free tier)"  
Write-Host "3. Replit (Easiest - just copy/paste files)"
Write-Host "4. Local testing only"

$choice = Read-Host "Enter choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host "🚂 Railway deployment selected" -ForegroundColor Blue
        Write-Host "Please follow these steps:"
        Write-Host "1. Go to https://railway.app/"
        Write-Host "2. Sign in with GitHub"
        Write-Host "3. Click 'New Project'"
        Write-Host "4. Select 'Deploy from GitHub repo'"
        Write-Host "5. Choose your repository"
        Write-Host "6. Railway will auto-detect Python and deploy"
    }
    "2" {
        Write-Host "🎨 Render deployment selected" -ForegroundColor Blue
        Write-Host "Please follow these steps:"
        Write-Host "1. Go to https://render.com/"
        Write-Host "2. Sign in with GitHub"
        Write-Host "3. Click 'New Web Service'"
        Write-Host "4. Connect your GitHub repository"
        Write-Host "5. Render will auto-deploy your Python app"
    }
    "3" {
        Write-Host "📝 Replit deployment selected (Easiest option!)" -ForegroundColor Blue
        Write-Host "Please follow these steps:"
        Write-Host "1. Go to https://replit.com/"
        Write-Host "2. Click 'Create Repl'"
        Write-Host "3. Choose 'Python' template"
        Write-Host "4. Copy all files from this directory to Replit"
        Write-Host "5. Click 'Run' - Replit handles everything automatically"
        Write-Host "6. Your server URL will be: https://your-repl-name.username.repl.co"
    }
    "4" {
        Write-Host "🧪 Starting local server for testing..." -ForegroundColor Blue
        & "D:/PROJECTS/hackton/VulnGPT/venv/Scripts/python.exe" main.py
    }
    default {
        Write-Host "❌ Invalid choice" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "📱 After deployment, test with:" -ForegroundColor Yellow
Write-Host "Invoke-WebRequest -Uri `"https://your-deployed-url.com/health`" -Method GET"
Write-Host ""
Write-Host "🎯 Then submit to Puch AI hackathon:" -ForegroundColor Green  
Write-Host "/hackathon submission add vulngpt-mcp-server https://github.com/yourusername/your-repo"
