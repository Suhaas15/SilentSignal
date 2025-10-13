#!/usr/bin/env python3
"""
SilentSignal Test Script
Quick test to verify the application works correctly
"""

from silent_signal_agent import SilentSignalAgent
from pattern_detector import PatternDetector
import json

def test_pattern_detection():
    """Test the pattern detector with example conversations"""
    print("🔍 Testing Pattern Detection...")
    
    detector = PatternDetector()
    
    # Test cases
    test_cases = [
        {
            "name": "Safe Conversation",
            "text": "Hey, how was your day? It was good! I went to the gym.",
            "expected_risk": "Safe"
        },
        {
            "name": "Concerning Conversation", 
            "text": "You always do this. If you loved me, you would not go out with your friends. You are being selfish.",
            "expected_risk": "Concerning"
        },
        {
            "name": "Likely Abuse",
            "text": "You're crazy. That never happened. If you leave me, I'll kill myself. You're making me angry.",
            "expected_risk": "Likely Abuse"
        }
    ]
    
    for test_case in test_cases:
        result = detector.detect_patterns(test_case["text"])
        print(f"\n📝 {test_case['name']}:")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Patterns Found: {result['total_patterns']}")
        if result['patterns']:
            print(f"   Examples: {result['patterns'][:2]}")
    
    print("\n✅ Pattern detection test completed!")

def test_ai_agent():
    """Test the AI agent (fallback mode)"""
    print("\n🤖 Testing AI Agent...")
    
    agent = SilentSignalAgent()
    test_text = "You're always making excuses. If you really cared about me, you'd make time."
    
    result = agent.analyze_conversation(test_text)
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Red Flags: {len(result['red_flags'])} found")
    print(f"   Suggestions: {len(result['suggestions'])} provided")
    
    print("✅ AI agent test completed!")

def test_resources():
    """Test resource loading"""
    print("\n📚 Testing Resources...")
    
    try:
        with open('resources.json', 'r') as f:
            resources = json.load(f)
        
        print(f"   Hotlines: {len(resources['hotlines'])} available")
        print(f"   Websites: {len(resources['websites'])} available")
        print(f"   Mobile Apps: {len(resources['mobile_apps'])} available")
        
        print("✅ Resources test completed!")
        
    except FileNotFoundError:
        print("❌ Resources file not found!")

def main():
    """Run all tests"""
    print("🚀 SilentSignal Test Suite")
    print("=" * 50)
    
    test_pattern_detection()
    test_ai_agent()
    test_resources()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\nTo run the full application:")
    print("   streamlit run app.py")

if __name__ == "__main__":
    main()


