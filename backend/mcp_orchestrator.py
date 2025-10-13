"""
MCP Orchestrator - Agentic Workflow Engine
Orchestrates multi-step analysis pipeline with RAG and Nemotron integration
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

from .nimo_client import NimoClient
from .pattern_detector import PatternDetector
from .analyzer import Analyzer
from .resources import ResourceManager

logger = logging.getLogger(__name__)

@dataclass
class AnalysisStep:
    """Represents a step in the agentic workflow"""
    name: str
    status: str  # pending, running, completed, failed
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class MCPOrchestrator:
    """
    MCP (Model Context Protocol) Orchestrator
    Manages the agentic workflow for conversation analysis
    """
    
    def __init__(self):
        self.nimo_client = NimoClient()
        self.pattern_detector = PatternDetector()
        self.analyzer = Analyzer()
        self.resource_manager = ResourceManager()
        
        # Workflow steps
        self.steps = [
            AnalysisStep("preprocessing", "pending"),
            AnalysisStep("rag_retrieval", "pending"),
            AnalysisStep("pattern_detection", "pending"),
            AnalysisStep("nemotron_analysis", "pending"),
            AnalysisStep("fusion_analysis", "pending"),
            AnalysisStep("report_generation", "pending")
        ]
    
    def analyze_conversation(self, conversation_text: str) -> Dict[str, Any]:
        """
        Execute the complete agentic workflow for conversation analysis
        
        Args:
            conversation_text: The conversation to analyze
            
        Returns:
            Complete analysis result with explainable reasoning
        """
        try:
            logger.info("Starting MCP agentic workflow")
            
            # Step 1: Preprocessing
            self._update_step_status("preprocessing", "running")
            preprocessed_data = self._preprocess_conversation(conversation_text)
            self._update_step_status("preprocessing", "completed", preprocessed_data)
            
            # Step 2: RAG Retrieval
            self._update_step_status("rag_retrieval", "running")
            rag_context = self._retrieve_pattern_definitions(preprocessed_data)
            self._update_step_status("rag_retrieval", "completed", rag_context)
            
            # Step 3: Pattern Detection
            self._update_step_status("pattern_detection", "running")
            pattern_results = self._detect_patterns(preprocessed_data)
            self._update_step_status("pattern_detection", "completed", pattern_results)
            
            # Step 4: Nemotron Analysis
            self._update_step_status("nemotron_analysis", "running")
            nemotron_results = self._analyze_with_nemotron(
                conversation_text, rag_context, pattern_results
            )
            self._update_step_status("nemotron_analysis", "completed", nemotron_results)
            
            # Step 5: Fusion Analysis
            self._update_step_status("fusion_analysis", "running")
            fusion_results = self._fuse_analyses(pattern_results, nemotron_results)
            self._update_step_status("fusion_analysis", "completed", fusion_results)
            
            # Step 6: Report Generation
            self._update_step_status("report_generation", "running")
            final_report = self._generate_final_report(fusion_results, rag_context)
            self._update_step_status("report_generation", "completed", final_report)
            
            logger.info("MCP agentic workflow completed successfully")
            return final_report
            
        except Exception as e:
            logger.error(f"MCP workflow error: {e}")
            return self._get_error_report(str(e))
    
    def _preprocess_conversation(self, conversation_text: str) -> Dict[str, Any]:
        """Preprocess conversation text for analysis"""
        # Clean and normalize text
        cleaned_text = conversation_text.strip()
        
        # Split into messages
        lines = cleaned_text.split('\n')
        messages = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Extract speaker and message
            if ':' in line:
                speaker, message = line.split(':', 1)
                speaker = speaker.strip()
                message = message.strip()
                
                messages.append({
                    "speaker": speaker,
                    "message": message,
                    "length": len(message),
                    "word_count": len(message.split())
                })
        
        # Analyze conversation structure
        speakers = [msg["speaker"] for msg in messages]
        speaker_counts = {}
        for speaker in speakers:
            speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1
        
        return {
            "original_text": conversation_text,
            "cleaned_text": cleaned_text,
            "messages": messages,
            "total_messages": len(messages),
            "speakers": list(set(speakers)),
            "speaker_counts": speaker_counts,
            "conversation_length": len(cleaned_text),
            "is_balanced": len(set(speaker_counts.values())) <= 1
        }
    
    def _retrieve_pattern_definitions(self, preprocessed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve relevant pattern definitions using RAG"""
        # Extract keywords from conversation
        messages = preprocessed_data["messages"]
        all_text = " ".join([msg["message"] for msg in messages]).lower()
        
        # Load pattern knowledge base
        pattern_knowledge = self.resource_manager.load_pattern_knowledge()
        
        # Find relevant patterns
        relevant_patterns = []
        for pattern in pattern_knowledge:
            # Check if pattern keywords appear in conversation
            keywords = pattern.get("keywords", [])
            if any(keyword.lower() in all_text for keyword in keywords):
                relevant_patterns.append(pattern)
        
        return {
            "retrieved_patterns": relevant_patterns,
            "total_patterns": len(relevant_patterns),
            "conversation_keywords": self._extract_keywords(all_text)
        }
    
    def _detect_patterns(self, preprocessed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run rule-based pattern detection"""
        conversation_text = preprocessed_data["cleaned_text"]
        return self.pattern_detector.detect_patterns(conversation_text)
    
    def _analyze_with_nemotron(self, conversation_text: str, rag_context: Dict[str, Any], pattern_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze conversation using Nemotron-3 with enriched context"""
        # Prepare context for Nemotron
        context = {
            "rag_patterns": rag_context["retrieved_patterns"],
            "detected_patterns": pattern_results.get("patterns", [])
        }
        
        return self.nimo_client.analyze_conversation(conversation_text, context)
    
    def _fuse_analyses(self, pattern_results: Dict[str, Any], nemotron_results: Dict[str, Any]) -> Dict[str, Any]:
        """Fuse rule-based and AI analyses"""
        return self.analyzer.fuse_analyses(pattern_results, nemotron_results)
    
    def _generate_final_report(self, fusion_results: Dict[str, Any], rag_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final explainable report"""
        report = {
            "risk_level": fusion_results.get("risk_level", "safe"),
            "risk_score": fusion_results.get("risk_score", 0),
            "patterns": fusion_results.get("patterns", []),
            "summary": fusion_results.get("summary", ""),
            "red_flags": fusion_results.get("red_flags", []),
            "suggestions": fusion_results.get("suggestions", []),
            "reasoning": fusion_results.get("reasoning", ""),
            "confidence": fusion_results.get("confidence", 0.0),
            "workflow_steps": self._get_workflow_summary(),
            "rag_context": {
                "patterns_retrieved": rag_context["total_patterns"],
                "keywords_analyzed": len(rag_context["conversation_keywords"])
            },
            "analysis_timestamp": self._get_timestamp(),
            "safety_concerns": self._assess_safety_concerns(fusion_results)
        }
        
        return report
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from conversation"""
        # Simple keyword extraction (can be enhanced with NLP)
        words = text.split()
        # Filter out common words and get unique words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "must", "can", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"}
        
        keywords = []
        for word in words:
            word = word.lower().strip(".,!?;:")
            if len(word) > 3 and word not in common_words:
                keywords.append(word)
        
        return list(set(keywords))
    
    def _assess_safety_concerns(self, fusion_results: Dict[str, Any]) -> str:
        """Assess safety concerns based on analysis"""
        risk_level = fusion_results.get("risk_level", "safe")
        patterns = fusion_results.get("patterns", [])
        
        if risk_level == "abuse":
            pattern_names = [p.get("name", "") for p in patterns]
            if "threats" in pattern_names:
                return "Immediate safety concern: Threats detected. Please consider your safety and reach out for help."
            elif "intimidation" in pattern_names:
                return "Safety concern: Intimidation patterns detected. Consider reaching out to a crisis hotline."
            else:
                return "Safety concern: Multiple abuse patterns detected. Please consider seeking support."
        elif risk_level == "concerning":
            return "Monitor the situation and trust your instincts. Consider seeking support if patterns continue."
        else:
            return "No immediate safety concerns detected."
    
    def _get_workflow_summary(self) -> List[Dict[str, Any]]:
        """Get summary of workflow steps"""
        return [
            {
                "step": step.name,
                "status": step.status,
                "has_result": step.result is not None,
                "has_error": step.error is not None
            }
            for step in self.steps
        ]
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _update_step_status(self, step_name: str, status: str, result: Optional[Dict[str, Any]] = None, error: Optional[str] = None):
        """Update step status in workflow"""
        for step in self.steps:
            if step.name == step_name:
                step.status = status
                step.result = result
                step.error = error
                break
    
    def _get_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generate error report when workflow fails"""
        return {
            "risk_level": "concerning",
            "risk_score": 0,
            "patterns": [],
            "summary": f"Analysis failed due to technical error: {error_message}",
            "red_flags": ["Technical analysis error - please review manually"],
            "suggestions": [
                "Please review the conversation carefully",
                "Consider seeking support if you feel unsafe",
                "Trust your instincts about the relationship dynamics"
            ],
            "reasoning": "Fallback analysis due to technical error",
            "confidence": 0.0,
            "workflow_steps": self._get_workflow_summary(),
            "error": error_message,
            "analysis_timestamp": self._get_timestamp(),
            "safety_concerns": "Unable to assess safety concerns due to technical error"
        }
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status"""
        return {
            "steps": [
                {
                    "name": step.name,
                    "status": step.status,
                    "has_result": step.result is not None,
                    "has_error": step.error is not None
                }
                for step in self.steps
            ],
            "overall_status": "completed" if all(step.status == "completed" for step in self.steps) else "running"
        }


