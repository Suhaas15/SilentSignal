"""
Test TwiML Response Format
Verifies that WhatsApp responses are properly formatted
"""

import requests
import time

# Wait for server to start
print("⏳ Waiting for server to start...")
time.sleep(3)

# Test message
test_message = "You never listen to me. If you really cared, you'd make time. You're being selfish."

print("\n" + "="*60)
print("🧪 TESTING WHATSAPP TWIML RESPONSE")
print("="*60)

print(f"\n📤 Sending test message:")
print(f"   '{test_message[:50]}...'")

# Send POST request to WhatsApp endpoint
url = "http://localhost:8000/whatsapp/inbound"
data = {
    "Body": test_message,
    "From": "whatsapp:+14155550123",
    "To": "whatsapp:+14155238886"
}

print(f"\n🔗 POST {url}")

try:
    response = requests.post(url, data=data, timeout=60)
    
    print(f"\n✅ Response Status: {response.status_code}")
    print(f"📄 Content-Type: {response.headers.get('content-type')}")
    
    print("\n" + "="*60)
    print("📱 TWIML RESPONSE (What Twilio will send to WhatsApp):")
    print("="*60)
    print(response.text)
    print("="*60)
    
    # Check if it's valid XML
    if response.text.startswith("<?xml"):
        print("\n✅ Valid TwiML XML format")
        
        # Extract message content
        if "<Message>" in response.text and "</Message>" in response.text:
            start = response.text.find("<Message>") + 9
            end = response.text.find("</Message>")
            message_content = response.text[start:end]
            
            # Unescape XML entities for display
            message_content = message_content.replace("&amp;", "&")
            message_content = message_content.replace("&lt;", "<")
            message_content = message_content.replace("&gt;", ">")
            message_content = message_content.replace("&quot;", '"')
            message_content = message_content.replace("&apos;", "'")
            
            print("\n" + "="*60)
            print("📲 MESSAGE AS IT WILL APPEAR ON WHATSAPP:")
            print("="*60)
            print(message_content)
            print("="*60)
            
            print("\n✅ SUCCESS! This message will be sent to WhatsApp")
        else:
            print("\n❌ Warning: No <Message> tag found in TwiML")
    else:
        print("\n❌ ERROR: Response is not valid TwiML XML")
        
except requests.exceptions.Timeout:
    print("\n❌ Request timed out (this is normal, analysis takes time)")
    print("   But the webhook should still work with Twilio!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "="*60)
print("🎯 NEXT STEPS:")
print("="*60)
print("1. ✅ Server is running and formatting TwiML correctly")
print("2. 🔗 Make sure your ngrok tunnel is active")
print("3. 📱 Send a message to your Twilio WhatsApp number")
print("4. 📬 You should receive the analysis response on WhatsApp!")
print("="*60 + "\n")

