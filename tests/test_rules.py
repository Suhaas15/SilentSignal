"""
SilentSignal Test Suite
Comprehensive tests for all components
"""

import pytest
import json
import os
from unittest.mock import Mock, patch

# Import components to test
from backend.pattern_detector import PatternDetector
from backend.nimo_client import NimoClient
from backend.analyzer import Analyzer
from backend.resources import ResourceManager
from backend.mcp_orchestrator import MCPOrchestrator

class TestPatternDetector:
    """Test pattern detection functionality"""
    
    def setup_method(self):
        self.detector = PatternDetector()
    
    def test_gaslighting_detection(self):
        """Test gaslighting pattern detection"""
        text = "That never happened. You're imagining things. You're making that up."
        result = self.detector.detect_patterns(text)
        
        assert result["risk_level"] in ["concerning", "abuse"]
        assert result["total_patterns"] > 0
        assert any(p["category"] == "gaslighting" for p in result["patterns"])
    
    def test_guilt_tripping_detection(self):
        """Test guilt-tripping pattern detection"""
        text = "If you loved me, you would do this. After all I've done for you, you're being selfish."
        result = self.detector.detect_patterns(text)
        
        assert result["risk_level"] in ["concerning", "abuse"]
        assert any(p["category"] == "guilt_tripping" for p in result["patterns"])
    
    def test_threats_detection(self):
        """Test threat pattern detection"""
        text = "I'll leave you if you don't do this. You'll be sorry. I'll hurt myself."
        result = self.detector.detect_patterns(text)
        
        assert result["risk_level"] == "abuse"
        assert any(p["category"] == "threats" for p in result["patterns"])
    
    def test_safe_conversation(self):
        """Test safe conversation detection"""
        text = "Hey, how was your day? It was good! I went to the gym and had lunch with Sarah."
        result = self.detector.detect_patterns(text)
        
        assert result["risk_level"] == "safe"
        assert result["total_patterns"] == 0
    
    def test_risk_level_calculation(self):
        """Test risk level calculation logic"""
        # Test different score thresholds
        assert self.detector._calculate_risk_level(70, {"threats": 2}) == "abuse"
        assert self.detector._calculate_risk_level(40, {"guilt_tripping": 1}) == "concerning"
        assert self.detector._calculate_risk_level(10, {}) == "safe"

class TestNimoClient:
    """Test NIM client functionality"""
    
    def setup_method(self):
        self.client = NimoClient()
    
    @patch('requests.post')
    def test_successful_api_call(self, mock_post):
        """Test successful NIM API call"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': '{"risk_level": "concerning", "patterns": []}'}}]
        }
        mock_post.return_value = mock_response
        
        result = self.client.analyze_conversation("test message", {})
        
        assert result["risk_level"] == "concerning"
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_api_failure(self, mock_post):
        """Test API failure handling"""
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        result = self.client.analyze_conversation("test message", {})
        
        assert result["risk_level"] == "concerning"  # Fallback response
        assert "analysis_unavailable" in result["patterns"][0]["name"]
    
    def test_health_check(self):
        """Test health check functionality"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            result = self.client.health_check()
            
            assert result["status"] == "healthy"
            assert result["available"] is True

class TestAnalyzer:
    """Test analyzer fusion logic"""
    
    def setup_method(self):
        self.analyzer = Analyzer()
    
    def test_fuse_analyses(self):
        """Test analysis fusion"""
        pattern_results = {
            "risk_level": "concerning",
            "risk_score": 30,
            "patterns": [{"category": "guilt_tripping", "description": "test", "severity": "medium", "matches": ["test"]}]
        }
        
        nemotron_results = {
            "risk_level": "concerning",
            "patterns": [{"name": "guilt_tripping", "description": "test", "severity": "medium", "evidence": "test"}],
            "summary": "Test summary",
            "red_flags": ["Test red flag"],
            "suggestions": ["Test suggestion"],
            "confidence": 0.8
        }
        
        result = self.analyzer.fuse_analyses(pattern_results, nemotron_results)
        
        assert result["risk_level"] == "concerning"
        assert len(result["patterns"]) > 0
        assert len(result["suggestions"]) > 0
        assert "reasoning" in result
    
    def test_fused_risk_level_calculation(self):
        """Test fused risk level calculation"""
        # Test different combinations
        assert self.analyzer._calculate_fused_risk_level("abuse", "abuse", 60, 0.9) == "abuse"
        assert self.analyzer._calculate_fused_risk_level("safe", "concerning", 20, 0.7) == "concerning"
        assert self.analyzer._calculate_fused_risk_level("safe", "safe", 5, 0.5) == "safe"

class TestResourceManager:
    """Test resource management"""
    
    def setup_method(self):
        self.resource_manager = ResourceManager()
    
    def test_load_resources(self):
        """Test resource loading"""
        resources = self.resource_manager.load_resources()
        
        assert "hotlines" in resources
        assert "websites" in resources
        assert len(resources["hotlines"]) > 0
    
    def test_load_pattern_knowledge(self):
        """Test pattern knowledge loading"""
        patterns = self.resource_manager.load_pattern_knowledge()
        
        assert isinstance(patterns, list)
        if patterns:  # If file exists
            assert "name" in patterns[0]
            assert "definition" in patterns[0]
    
    def test_get_crisis_resources(self):
        """Test crisis resource retrieval"""
        resources = self.resource_manager.get_crisis_resources()
        
        assert isinstance(resources, list)
        if resources:
            assert "name" in resources[0]
            assert "phone" in resources[0]

class TestMCPOrchestrator:
    """Test MCP orchestrator workflow"""
    
    def setup_method(self):
        self.orchestrator = MCPOrchestrator()
    
    def test_preprocessing(self):
        """Test conversation preprocessing"""
        text = """Person A: Hello there
Person B: Hi! How are you?
Person A: I'm good, thanks!"""
        
        result = self.orchestrator._preprocess_conversation(text)
        
        assert result["total_messages"] == 3
        assert len(result["speakers"]) == 2
        assert "Person A" in result["speakers"]
        assert "Person B" in result["speakers"]
    
    def test_rag_retrieval(self):
        """Test RAG pattern retrieval"""
        preprocessed_data = {
            "messages": [{"message": "you're crazy and imagining things"}],
            "cleaned_text": "you're crazy and imagining things"
        }
        
        result = self.orchestrator._retrieve_pattern_definitions(preprocessed_data)
        
        assert "retrieved_patterns" in result
        assert "conversation_keywords" in result
        assert isinstance(result["retrieved_patterns"], list)
    
    def test_workflow_status(self):
        """Test workflow status tracking"""
        status = self.orchestrator.get_workflow_status()
        
        assert "steps" in status
        assert "overall_status" in status
        assert len(status["steps"]) == 6  # Number of workflow steps
    
    @patch('backend.mcp_orchestrator.MCPOrchestrator._analyze_with_nemotron')
    def test_full_workflow(self, mock_nemotron):
        """Test full workflow execution"""
        # Mock Nemotron analysis
        mock_nemotron.return_value = {
            "risk_level": "concerning",
            "patterns": [],
            "summary": "Test summary",
            "red_flags": [],
            "suggestions": [],
            "confidence": 0.8
        }
        
        text = "You're always making excuses. If you loved me, you'd make time."
        result = self.orchestrator.analyze_conversation(text)
        
        assert result["risk_level"] in ["safe", "concerning", "abuse"]
        assert "workflow_steps" in result
        assert "analysis_timestamp" in result
        assert "reasoning" in result

class TestIntegration:
    """Integration tests"""
    
    def test_end_to_end_analysis(self):
        """Test complete end-to-end analysis"""
        orchestrator = MCPOrchestrator()
        
        # Test with concerning conversation
        text = """Person A: You're always making excuses. If you really cared about me, you'd make time.
Person B: I do care about you, but I can't always answer immediately.
Person A: You're being selfish. After everything I do for you, this is how you treat me?"""
        
        result = orchestrator.analyze_conversation(text)
        
        assert result["risk_level"] in ["concerning", "abuse"]
        assert len(result["patterns"]) > 0
        assert len(result["suggestions"]) > 0
        assert "workflow_steps" in result
    
    def test_safe_conversation_analysis(self):
        """Test safe conversation analysis"""
        orchestrator = MCPOrchestrator()
        
        text = """Person A: Hey, how was your day?
Person B: It was good! I went to the gym and had lunch with Sarah.
Person A: That sounds nice! I'm glad you had a good time."""
        
        result = orchestrator.analyze_conversation(text)
        
        assert result["risk_level"] == "safe"
        assert len(result["patterns"]) == 0
        assert "workflow_steps" in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"])


