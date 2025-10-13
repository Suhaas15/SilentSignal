#!/usr/bin/env python3
"""
SilentSignal Comprehensive Test Suite
Tests the accuracy of the emotional abuse detection system
"""

from silent_signal_agent import AdvancedSilentSignalAgent
from pattern_detector import AdvancedPatternDetector
from test_dataset import TEST_DATASET
import json

class SilentSignalTester:
    """Comprehensive testing suite for SilentSignal"""
    
    def __init__(self):
        self.agent = AdvancedSilentSignalAgent()
        self.pattern_detector = AdvancedPatternDetector()
        self.results = {
            "total_tests": 0,
            "correct_predictions": 0,
            "incorrect_predictions": 0,
            "false_positives": 0,
            "false_negatives": 0,
            "test_results": []
        }
    
    def run_all_tests(self):
        """Run all test cases and generate accuracy report"""
        print("🧪 SilentSignal Comprehensive Test Suite")
        print("=" * 60)
        
        # Test safe conversations
        print("\n📊 Testing Safe Conversations...")
        for test_case in TEST_DATASET["safe_conversations"]:
            self._run_test(test_case, "Safe")
        
        # Test concerning conversations
        print("\n⚠️ Testing Concerning Conversations...")
        for test_case in TEST_DATASET["concerning_conversations"]:
            self._run_test(test_case, "Concerning")
        
        # Test likely abuse conversations
        print("\n🚨 Testing Likely Abuse Conversations...")
        for test_case in TEST_DATASET["likely_abuse_conversations"]:
            self._run_test(test_case, "Likely Abuse")
        
        # Test pattern-specific cases
        print("\n🔍 Testing Pattern-Specific Cases...")
        for test_case in TEST_DATASET["pattern_tests"]:
            self._run_test(test_case, test_case["expected_risk"])
        
        # Test edge cases
        print("\n🎯 Testing Edge Cases...")
        for test_case in TEST_DATASET["edge_cases"]:
            self._run_test(test_case, test_case["expected_risk"])
        
        # Generate final report
        self._generate_report()
    
    def _run_test(self, test_case, expected_risk):
        """Run a single test case"""
        conversation = test_case["conversation"]
        test_name = test_case["name"]
        
        print(f"  Testing: {test_name}")
        
        # Get analysis from both systems
        agent_result = self.agent.analyze_conversation(conversation)
        pattern_result = self.pattern_detector.detect_patterns(conversation)
        
        # Determine final risk level (use the more severe of the two)
        agent_risk = agent_result["risk_level"]
        pattern_risk = pattern_result["risk_level"]
        
        # Risk level hierarchy: Safe < Concerning < Likely Abuse
        risk_hierarchy = {"Safe": 1, "Concerning": 2, "Likely Abuse": 3}
        final_risk = max([agent_risk, pattern_risk], key=lambda x: risk_hierarchy[x])
        
        # Check if prediction is correct
        is_correct = final_risk == expected_risk
        
        # Record results
        test_result = {
            "test_name": test_name,
            "expected_risk": expected_risk,
            "agent_risk": agent_risk,
            "pattern_risk": pattern_risk,
            "final_risk": final_risk,
            "is_correct": is_correct,
            "agent_score": agent_result.get("risk_score", 0),
            "pattern_score": pattern_result.get("risk_score", 0),
            "total_patterns": pattern_result.get("total_patterns", 0),
            "description": test_case.get("description", "")
        }
        
        self.results["test_results"].append(test_result)
        self.results["total_tests"] += 1
        
        if is_correct:
            self.results["correct_predictions"] += 1
            print(f"    ✅ CORRECT: {final_risk}")
        else:
            self.results["incorrect_predictions"] += 1
            print(f"    ❌ INCORRECT: Expected {expected_risk}, Got {final_risk}")
            
            # Categorize errors
            if expected_risk == "Safe" and final_risk != "Safe":
                self.results["false_positives"] += 1
            elif expected_risk != "Safe" and final_risk == "Safe":
                self.results["false_negatives"] += 1
        
        # Show detailed analysis for incorrect predictions
        if not is_correct:
            print(f"    Agent Analysis: {agent_risk} (score: {agent_result.get('risk_score', 0)})")
            print(f"    Pattern Analysis: {pattern_risk} (score: {pattern_result.get('risk_score', 0)})")
            print(f"    Patterns Found: {pattern_result.get('total_patterns', 0)}")
    
    def _generate_report(self):
        """Generate comprehensive accuracy report"""
        print("\n" + "=" * 60)
        print("📈 ACCURACY REPORT")
        print("=" * 60)
        
        total = self.results["total_tests"]
        correct = self.results["correct_predictions"]
        incorrect = self.results["incorrect_predictions"]
        
        accuracy = (correct / total) * 100 if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Correct Predictions: {correct}")
        print(f"Incorrect Predictions: {incorrect}")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"False Positives: {self.results['false_positives']}")
        print(f"False Negatives: {self.results['false_negatives']}")
        
        # Risk level breakdown
        print("\n📊 Risk Level Breakdown:")
        risk_counts = {}
        for result in self.results["test_results"]:
            risk = result["final_risk"]
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        for risk, count in risk_counts.items():
            print(f"  {risk}: {count} cases")
        
        # Show incorrect predictions
        print("\n❌ Incorrect Predictions:")
        incorrect_cases = [r for r in self.results["test_results"] if not r["is_correct"]]
        for case in incorrect_cases:
            print(f"  {case['test_name']}: Expected {case['expected_risk']}, Got {case['final_risk']}")
        
        # Performance analysis
        print("\n⚡ Performance Analysis:")
        avg_agent_score = sum(r["agent_score"] for r in self.results["test_results"]) / total
        avg_pattern_score = sum(r["pattern_score"] for r in self.results["test_results"]) / total
        avg_patterns = sum(r["total_patterns"] for r in self.results["test_results"]) / total
        
        print(f"  Average Agent Risk Score: {avg_agent_score:.1f}")
        print(f"  Average Pattern Risk Score: {avg_pattern_score:.1f}")
        print(f"  Average Patterns Detected: {avg_patterns:.1f}")
        
        # Save detailed results
        with open('test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Detailed results saved to test_results.json")
        
        # Recommendations
        print("\n💡 Recommendations:")
        if accuracy < 80:
            print("  ⚠️ Accuracy below 80% - consider improving pattern detection")
        if self.results["false_positives"] > 2:
            print("  ⚠️ High false positive rate - may be too sensitive")
        if self.results["false_negatives"] > 2:
            print("  ⚠️ High false negative rate - may miss abuse cases")
        
        if accuracy >= 85:
            print("  ✅ Good accuracy! System is performing well")
        elif accuracy >= 75:
            print("  ⚠️ Moderate accuracy - some improvements needed")
        else:
            print("  ❌ Low accuracy - significant improvements required")

def main():
    """Run the comprehensive test suite"""
    tester = SilentSignalTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()


