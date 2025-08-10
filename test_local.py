"""
Quick test script for MCP Server validation
Run this before deploying to ensure everything works
"""

import requests
import json

def test_local_server():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing VulnGPT MCP Server locally...")
    print("="*50)
    
    # Test 1: Health check
    try:
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server not reachable: {e}")
        print("💡 Make sure to start the server first: python main.py")
        return False
    
    # Test 2: Validation endpoint
    test_tokens = {
        "puch_ai_token_123": "919876543210",
        "demo_token_456": "918765432109", 
    }
    
    for token, expected_phone in test_tokens.items():
        print(f"\n2. Testing validation with token: {token[:10]}...")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(f"{base_url}/validate", headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("phone_number") == expected_phone:
                    print(f"✅ Validation successful: {data['phone_number']}")
                else:
                    print(f"❌ Wrong phone number: {data.get('phone_number')}")
                    return False
            else:
                print(f"❌ Validation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Validation request failed: {e}")
            return False
    
    # Test 3: Invalid token
    print(f"\n3. Testing invalid token...")
    headers = {
        "Authorization": "Bearer invalid_token_12345",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{base_url}/validate", headers=headers, timeout=5)
        if response.status_code == 401:
            print("✅ Invalid token properly rejected")
        else:
            print(f"❌ Invalid token should return 401, got: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Invalid token test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Server is ready for deployment.")
    print("\n📋 Next steps:")
    print("1. Deploy to Replit, Railway, or Render")
    print("2. Update the bearer tokens in main.py with real ones")
    print("3. Test the deployed URL")
    print("4. Submit to Puch AI hackathon")
    
    return True

if __name__ == "__main__":
    test_local_server()
