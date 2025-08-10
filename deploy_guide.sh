#!/bin/bash

echo "🚀 VulnGPT MCP Server - Hackathon Deployment"
echo "============================================"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this from the python-fastapi directory"
    exit 1
fi

echo "📋 Choose deployment option:"
echo "1. Railway (Recommended - Free tier with GitHub)"
echo "2. Render (Free tier)"
echo "3. Heroku (Requires credit card)"
echo "4. Local testing only"

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "🚂 Railway deployment selected"
        echo "Please follow these steps:"
        echo "1. Go to https://railway.app/"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New Project'"
        echo "4. Select 'Deploy from GitHub repo'"
        echo "5. Choose your repository"
        echo "6. Railway will auto-detect Python and deploy"
        ;;
    2)
        echo "🎨 Render deployment selected"  
        echo "Please follow these steps:"
        echo "1. Go to https://render.com/"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New Web Service'"
        echo "4. Connect your GitHub repository"
        echo "5. Render will auto-deploy your Python app"
        ;;
    3)
        echo "🔮 Heroku deployment selected"
        echo "Note: Heroku requires credit card verification"
        echo "1. Go to https://heroku.com/"
        echo "2. Create account and verify with credit card"
        echo "3. Install Heroku CLI"
        echo "4. Run: heroku create your-app-name"
        echo "5. Run: git push heroku main"
        ;;
    4)
        echo "🧪 Starting local server for testing..."
        python main.py
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "📱 After deployment, test with:"
echo "curl https://your-deployed-url.com/health"
echo ""
echo "🎯 Then submit to Puch AI hackathon:"
echo "/hackathon submission add vulngpt-mcp-server https://github.com/yourusername/your-repo"
