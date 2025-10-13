"""
Analyzer - Fusion Logic Engine
Combines rule-based and AI analyses into explainable results
"""

import json
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Analyzer:
    """
    Analyzer that fuses rule-based pattern detection with AI analysis
    """
    
    def __init__(self):
        self.fusion_weights = {
            "pattern_detection": 0.4,
            "ai_analysis": 0.6
        }
    
    def fuse_analyses(self, pattern_results: Dict[str, Any], nemotron_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fuse rule-based pattern detection with AI analysis
        
        Args:
            pattern_results: Results from pattern detection
            nemotron_results: Results from Nemotron analysis
            
        Returns:
            Fused analysis result
        """
        try:
            # Extract key metrics
            pattern_risk_level = pattern_results.get("risk_level", "safe")
            pattern_score = pattern_results.get("risk_score", 0)
            pattern_patterns = pattern_results.get("patterns", [])
            
            ai_risk_level = nemotron_results.get("risk_level", "safe")
            ai_patterns = nemotron_results.get("patterns", [])
            ai_summary = nemotron_results.get("summary", "")
            ai_red_flags = nemotron_results.get("red_flags", [])
            ai_suggestions = nemotron_results.get("suggestions", [])
            ai_confidence = nemotron_results.get("confidence", 0.5)
            
            # Calculate fused risk level
            fused_risk_level = self._calculate_fused_risk_level(
                pattern_risk_level, ai_risk_level, pattern_score, ai_confidence
            )
            
            # Calculate fused risk score
            fused_risk_score = self._calculate_fused_risk_score(
                pattern_score, ai_confidence, pattern_patterns, ai_patterns
            )
            
            # Combine patterns
            combined_patterns = self._combine_patterns(pattern_patterns, ai_patterns)
            
            # Combine red flags
            combined_red_flags = self._combine_red_flags(pattern_results, ai_red_flags)
            
            # Generate fused suggestions
            fused_suggestions = self._generate_fused_suggestions(
                fused_risk_level, combined_patterns, ai_suggestions
            )
            
            # Generate reasoning
            reasoning = self._generate_reasoning(
                pattern_results, nemotron_results, fused_risk_level
            )
            
            return {
                "risk_level": fused_risk_level,
                "risk_score": fused_risk_score,
                "patterns": combined_patterns,
                "summary": ai_summary or self._generate_summary(fused_risk_level, combined_patterns),
                "red_flags": combined_red_flags,
                "suggestions": fused_suggestions,
                "reasoning": reasoning,
                "confidence": ai_confidence,
                "fusion_breakdown": {
                    "pattern_detection_score": pattern_score,
                    "ai_confidence": ai_confidence,
                    "pattern_risk_level": pattern_risk_level,
                    "ai_risk_level": ai_risk_level
                }
            }
            
        except Exception as e:
            logger.error(f"Fusion analysis error: {e}")
            return self._get_fallback_fusion(pattern_results, nemotron_results)
    
    def _calculate_fused_risk_level(self, pattern_level: str, ai_level: str, pattern_score: int, ai_confidence: float) -> str:
        """Calculate fused risk level from both analyses"""
        # Risk level hierarchy
        risk_hierarchy = {"safe": 1, "concerning": 2, "abuse": 3}
        
        # Weight the AI analysis by confidence
        ai_weight = ai_confidence
        pattern_weight = 1.0 - ai_weight
        
        # Calculate weighted risk levels
        pattern_value = risk_hierarchy.get(pattern_level, 1)
        ai_value = risk_hierarchy.get(ai_level, 1)
        
        # Additional scoring based on pattern score
        if pattern_score >= 50:
            pattern_value = max(pattern_value, 3)  # Force to abuse level
        elif pattern_score >= 25:
            pattern_value = max(pattern_value, 2)  # Force to concerning level
        
        # Weighted average
        fused_value = (pattern_value * pattern_weight) + (ai_value * ai_weight)
        
        # Convert back to risk level
        if fused_value >= 2.5:
            return "abuse"
        elif fused_value >= 1.5:
            return "concerning"
        else:
            return "safe"
    
    def _calculate_fused_risk_score(self, pattern_score: int, ai_confidence: float, pattern_patterns: List, ai_patterns: List) -> float:
        """Calculate fused risk score"""
        # Normalize pattern score to 0-1 range
        normalized_pattern_score = min(pattern_score / 100.0, 1.0)
        
        # Calculate AI score based on patterns and confidence
        ai_score = ai_confidence * (len(ai_patterns) / 10.0)  # Normalize by max expected patterns
        
        # Weighted combination
        fused_score = (normalized_pattern_score * self.fusion_weights["pattern_detection"]) + \
                     (ai_score * self.fusion_weights["ai_analysis"])
        
        return min(fused_score * 100, 100)  # Convert back to 0-100 scale
    
    def _combine_patterns(self, pattern_patterns: List, ai_patterns: List) -> List[Dict[str, Any]]:
        """Combine patterns from both analyses"""
        combined = []
        
        # Add pattern detection results
        for pattern in pattern_patterns:
            combined.append({
                "name": pattern["category"],
                "description": pattern["description"],
                "severity": pattern["severity"],
                "evidence": pattern["matches"][0] if pattern["matches"] else "Pattern detected",
                "source": "pattern_detection",
                "confidence": 0.8
            })
        
        # Add AI analysis results
        for pattern in ai_patterns:
            combined.append({
                "name": pattern.get("name", "unknown"),
                "description": pattern.get("description", ""),
                "severity": pattern.get("severity", "medium"),
                "evidence": pattern.get("evidence", ""),
                "source": "ai_analysis",
                "confidence": pattern.get("confidence", 0.7)
            })
        
        # Remove duplicates and sort by severity
        unique_patterns = {}
        for pattern in combined:
            key = pattern["name"]
            if key not in unique_patterns or pattern["confidence"] > unique_patterns[key]["confidence"]:
                unique_patterns[key] = pattern
        
        # Sort by severity
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        sorted_patterns = sorted(
            unique_patterns.values(),
            key=lambda x: severity_order.get(x["severity"], 0),
            reverse=True
        )
        
        return sorted_patterns[:10]  # Limit to top 10 patterns
    
    def _combine_red_flags(self, pattern_results: Dict[str, Any], ai_red_flags: List[str]) -> List[str]:
        """Combine red flags from both analyses"""
        combined_flags = []
        
        # Add pattern-based red flags
        pattern_patterns = pattern_results.get("patterns", [])
        for pattern in pattern_patterns:
            if pattern["matches"]:
                combined_flags.append(f"{pattern['category'].replace('_', ' ').title()}: {pattern['matches'][0]}")
        
        # Add AI red flags
        combined_flags.extend(ai_red_flags)
        
        # Remove duplicates and limit
        unique_flags = list(dict.fromkeys(combined_flags))  # Preserve order while removing duplicates
        return unique_flags[:10]  # Limit to top 10 red flags
    
    def _generate_fused_suggestions(self, risk_level: str, patterns: List[Dict], ai_suggestions: List[str]) -> List[str]:
        """Generate fused suggestions based on risk level and patterns"""
        suggestions = []
        
        # Base suggestions by risk level
        if risk_level == "safe":
            suggestions = [
                "This conversation appears healthy and respectful",
                "Continue communicating openly and honestly",
                "Remember that healthy relationships involve mutual respect"
            ]
        elif risk_level == "concerning":
            suggestions = [
                "Pay attention to how this conversation makes you feel",
                "Consider discussing your concerns with a trusted friend or counselor",
                "Trust your instincts about the relationship dynamics",
                "Set clear boundaries about what behavior you find acceptable"
            ]
        else:  # abuse
            suggestions = [
                "This conversation shows concerning patterns of manipulation or control",
                "Please consider reaching out to a crisis hotline or counselor",
                "Your safety and well-being are important",
                "Consider talking to a trusted friend or family member",
                "Remember that you deserve to be treated with respect and kindness"
            ]
        
        # Add pattern-specific suggestions
        pattern_names = [p["name"] for p in patterns]
        if "gaslighting" in pattern_names:
            suggestions.append("Consider keeping a record of conversations to verify your memory")
        if "threats" in pattern_names:
            suggestions.append("If you feel unsafe, please contact emergency services or a crisis hotline")
        if "isolation_attempts" in pattern_names:
            suggestions.append("Maintain connections with friends and family - isolation is a red flag")
        if "financial_control" in pattern_names:
            suggestions.append("Consider financial independence and separate accounts")
        if "sexual_coercion" in pattern_names:
            suggestions.append("Your consent and comfort are important - you have the right to say no")
        
        # Add AI suggestions if available
        suggestions.extend(ai_suggestions)
        
        # Remove duplicates and limit
        unique_suggestions = list(dict.fromkeys(suggestions))
        return unique_suggestions[:8]  # Limit to 8 suggestions
    
    def _generate_reasoning(self, pattern_results: Dict[str, Any], nemotron_results: Dict[str, Any], fused_risk_level: str) -> str:
        """Generate explainable reasoning for the analysis"""
        pattern_score = pattern_results.get("risk_score", 0)
        pattern_count = pattern_results.get("total_patterns", 0)
        ai_confidence = nemotron_results.get("confidence", 0.5)
        
        reasoning_parts = []
        
        # Pattern detection reasoning
        if pattern_count > 0:
            reasoning_parts.append(f"Rule-based detection found {pattern_count} abuse patterns with a risk score of {pattern_score}")
        
        # AI analysis reasoning
        if ai_confidence > 0.5:
            reasoning_parts.append(f"AI analysis provided contextual reasoning with {ai_confidence:.1%} confidence")
        
        # Fusion reasoning
        reasoning_parts.append(f"Hybrid analysis combining pattern detection with AI reasoning resulted in '{fused_risk_level}' risk level")
        
        # Additional context
        if pattern_score >= 50:
            reasoning_parts.append("High pattern score indicates multiple serious abuse indicators")
        elif pattern_score >= 25:
            reasoning_parts.append("Moderate pattern score suggests concerning manipulation tactics")
        
        return ". ".join(reasoning_parts) + "."
    
    def _generate_summary(self, risk_level: str, patterns: List[Dict]) -> str:
        """Generate summary based on risk level and patterns"""
        if risk_level == "safe":
            return "No concerning patterns detected. This appears to be a healthy conversation."
        elif risk_level == "concerning":
            pattern_types = [p["name"] for p in patterns[:3]]
            return f"Detected concerning patterns including: {', '.join(pattern_types)}. Please review the relationship dynamics carefully."
        else:
            pattern_types = [p["name"] for p in patterns[:3]]
            return f"Multiple serious abuse patterns detected including: {', '.join(pattern_types)}. This conversation shows clear signs of emotional abuse and manipulation."
    
    def _get_fallback_fusion(self, pattern_results: Dict[str, Any], nemotron_results: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback fusion when analysis fails"""
        return {
            "risk_level": pattern_results.get("risk_level", "concerning"),
            "risk_score": pattern_results.get("risk_score", 0),
            "patterns": pattern_results.get("patterns", []),
            "summary": "Analysis incomplete due to technical issues. Please review the conversation carefully.",
            "red_flags": ["Technical analysis error - please review manually"],
            "suggestions": [
                "Please review the conversation carefully",
                "Consider seeking support if you feel unsafe",
                "Trust your instincts about the relationship dynamics"
            ],
            "reasoning": "Fallback analysis due to technical limitations",
            "confidence": 0.3,
            "fusion_breakdown": {
                "pattern_detection_score": pattern_results.get("risk_score", 0),
                "ai_confidence": 0.0,
                "pattern_risk_level": pattern_results.get("risk_level", "concerning"),
                "ai_risk_level": "unknown"
            }
        }


