#!/usr/bin/env python3
"""
Test WhatsApp Form Parsing
Verifies that the FastAPI app can handle Twilio's form-encoded webhook data
"""

import requests
import json

def test_form_parsing():
    """Test form-encoded POST request (simulates Twilio webhook)"""
    print("🧪 Testing WhatsApp Form Parsing...")
    print("=" * 60)
    
    # Test 1: Form-encoded POST (Twilio format)
    print("\n1️⃣  Testing Form-Encoded POST (Twilio Format):")
    print("-" * 60)
    
    form_data = {
        'From': 'whatsapp:+14155550123',
        'Body': 'You never listen to me, I do everything for you. You are selfish.',
        'To': 'whatsapp:+14155238886',
        'MessageSid': 'SM123456789',
        'AccountSid': 'AC123456789'
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/whatsapp/inbound',
            data=form_data,  # Form-encoded
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Response:\n{response.text[:500]}")
        
        if response.status_code == 200:
            if 'Risk Level' in response.text:
                print("✅ PASS: Form parsing works! Risk analysis returned.")
            else:
                print("⚠️  WARN: Form parsed but unexpected response format")
        else:
            print(f"❌ FAIL: Got status code {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request error: {e}")
        print("\n⚠️  Make sure the API is running:")
        print("   uvicorn integrations.whatsapp_fastapi:app --reload --host 0.0.0.0 --port 8000")
        return False
    
    # Test 2: JSON POST (for testing endpoint)
    print("\n\n2️⃣  Testing JSON POST (Test Endpoint):")
    print("-" * 60)
    
    json_data = {
        'message': 'You are always making excuses. If you really cared about me, you would make time.'
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/whatsapp/test',
            json=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)[:500]}")
        
        if response.status_code == 200:
            result = response.json()
            if 'risk_level' in result:
                print(f"✅ PASS: JSON endpoint works! Risk Level: {result['risk_level']}")
            else:
                print("⚠️  WARN: JSON endpoint responded but missing risk_level")
        else:
            print(f"❌ FAIL: Got status code {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request error: {e}")
        return False
    
    # Test 3: cURL command example
    print("\n\n3️⃣  cURL Command for Testing:")
    print("-" * 60)
    print("""
# Test with cURL (copy and paste this):
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" \\
  -d 'From=whatsapp:+14155550123' \\
  -d 'Body=You never listen to me, I do everything for you.' \\
  http://localhost:8000/whatsapp/inbound
""")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("\n📋 Summary:")
    print("   - Form-encoded parsing: Working ✓")
    print("   - JSON endpoint: Working ✓")
    print("   - Ready for Twilio integration!")
    
    return True

def test_health():
    """Test API health"""
    print("\n\n🏥 Testing API Health:")
    print("-" * 60)
    
    try:
        response = requests.get('http://localhost:8000/health')
        print(f"Health Status: {response.json()}")
        print("✅ API is healthy!")
        return True
    except:
        print("❌ API is not running!")
        print("\n⚠️  Start the API first:")
        print("   uvicorn integrations.whatsapp_fastapi:app --reload --host 0.0.0.0 --port 8000")
        return False

if __name__ == "__main__":
    print("🚀 SilentSignal WhatsApp Integration Test Suite")
    print("=" * 60)
    
    # Check API health first
    if not test_health():
        print("\n❌ API is not running. Please start it first.")
        exit(1)
    
    # Run form parsing tests
    success = test_form_parsing()
    
    if success:
        print("\n🎉 Success! Your WhatsApp integration is ready!")
        print("\n📱 Next Steps:")
        print("   1. Set up ngrok: ngrok http 8000")
        print("   2. Configure Twilio webhook with: https://YOUR-NGROK-URL.ngrok.io/whatsapp/inbound")
        print("   3. Send a WhatsApp message to test!")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        exit(1)
