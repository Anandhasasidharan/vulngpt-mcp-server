"""
Test the deployed Vercel server
Usage: python test_vercel.py <your-vercel-url>
Example: python test_vercel.py https://vulngpt-mcp-server.vercel.app
"""

import requests
import sys
import json

def test_vercel_deployment(base_url):
    print(f"🧪 Testing Vercel deployment at: {base_url}")
    print("=" * 60)
    
    # Remove trailing slash
    base_url = base_url.rstrip('/')
    
    # Test 1: Health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Validation endpoint with valid token
    print("\n2. Testing validation endpoint...")
    headers = {
        "Authorization": "Bearer puch_ai_token_123",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{base_url}/validate", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get("phone_number") == "917305041960":
                print("✅ Validation successful!")
                print(f"Phone: {data['phone_number']}")
            else:
                print(f"❌ Wrong phone number: {data.get('phone_number')}")
                return False
        else:
            print(f"❌ Validation failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False
    
    # Test 3: Invalid token
    print("\n3. Testing invalid token...")
    headers = {
        "Authorization": "Bearer invalid_token_xyz",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{base_url}/validate", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Invalid token properly rejected!")
        else:
            print(f"❌ Expected 401, got: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Invalid token test error: {e}")
        return False
    
    print("\n🎉 All tests passed! Your server is ready for hackathon submission!")
    print("\n📋 Next steps:")
    print(f"1. Submit to hackathon: /hackathon submission add vulngpt-mcp-server https://github.com/Anandhasasidhiran/vulngpt-mcp-server")
    print(f"2. Connect users: /mcp connect {base_url} puch_ai_token_123")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_vercel.py <vercel-url>")
        print("Example: python test_vercel.py https://vulngpt-mcp-server.vercel.app")
        sys.exit(1)
    
    url = sys.argv[1]
    test_vercel_deployment(url)
