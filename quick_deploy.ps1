Write-Host "🚀 VulnGPT MCP Server - Hackathon Deployment" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green

Write-Host "`n📋 EASIEST DEPLOYMENT OPTION - REPLIT:" -ForegroundColor Yellow
Write-Host "1. Go to https://replit.com/"
Write-Host "2. Sign up/Login and click 'Create Repl'"
Write-Host "3. Choose 'Python' template"
Write-Host "4. Name it: vulngpt-mcp-server"
Write-Host "5. Copy all files from this folder to Replit"
Write-Host "6. Click the green 'Run' button"
Write-Host "7. Your server URL: https://vulngpt-mcp-server.username.repl.co"

Write-Host "`n🔄 OTHER OPTIONS:" -ForegroundColor Blue
Write-Host "- Railway: https://railway.app (deploy from GitHub)"
Write-Host "- Render: https://render.com (free tier)"

Write-Host "`n✅ AFTER DEPLOYMENT:" -ForegroundColor Green
Write-Host "1. Test: curl https://your-url.com/health"
Write-Host "2. Submit: /hackathon submission add vulngpt-mcp-server https://github.com/user/repo"
Write-Host "3. Share: /mcp connect https://your-url.com your_token"

Write-Host "`n📋 Files to copy to Replit:" -ForegroundColor Cyan
Get-ChildItem -Name
