import requests
import json
import os
import re
from typing import Dict, List, Any, Tuple
from collections import Counter

class AdvancedSilentSignalAgent:
    """
    Advanced AI Agent for emotional abuse detection with sophisticated analysis
    """
    
    def __init__(self):
        # Align with backend env naming; prefer hosted endpoint by default
        self.nim_endpoint = os.getenv('NIM_BASE_URL', 'https://integrate.api.nvidia.com/v1')
        self.api_key = os.getenv('NIM_API_KEY', '')
        self.model = os.getenv('NIM_MODEL', 'nvidia/nemotron-3-8b-instruct')
        
        # Emotional abuse indicators
        self.abuse_indicators = self._initialize_abuse_indicators()
        self.emotional_markers = self._initialize_emotional_markers()
        
    def _initialize_abuse_indicators(self) -> Dict[str, List[str]]:
        """Initialize comprehensive abuse indicators"""
        return {
            "power_imbalance": [
                "i'm the man here", "i'm in charge", "i make the decisions",
                "you don't get a say", "i know what's best", "you're not smart enough",
                "you need me", "you can't survive without me", "you're helpless without me"
            ],
            "control_tactics": [
                "you can't", "you're not allowed", "i forbid you", "you must",
                "you have to", "don't you dare", "you better not", "i won't let you"
            ],
            "emotional_manipulation": [
                "you're too sensitive", "you're overreacting", "you're being dramatic",
                "you're being childish", "grow up", "get over it", "stop crying"
            ],
            "isolation_attempts": [
                "your friends don't like me", "your family is toxic", "they're trying to break us up",
                "don't listen to them", "they don't understand us", "they're jealous"
            ],
            "threats": [
                "i'll leave you", "you'll be sorry", "i'll make you pay", "you'll regret this",
                "i'll hurt myself", "i'll kill myself", "you'll never find someone like me"
            ],
            "gaslighting": [
                "that never happened", "you're imagining things", "you're making that up",
                "that's not what i said", "you're remembering it wrong", "you're crazy"
            ],
            "guilt_tripping": [
                "if you loved me", "after all i've done for you", "you're ungrateful",
                "i do everything for you", "you don't appreciate me", "you're selfish"
            ]
        }
    
    def _initialize_emotional_markers(self) -> Dict[str, List[str]]:
        """Initialize emotional state markers"""
        return {
            "fear": ["scared", "afraid", "terrified", "frightened", "worried", "anxious"],
            "anger": ["angry", "mad", "furious", "rage", "irritated", "annoyed"],
            "sadness": ["sad", "depressed", "hurt", "crying", "upset", "devastated"],
            "confusion": ["confused", "lost", "don't understand", "unclear", "mixed up"],
            "defensiveness": ["defensive", "protecting", "justifying", "explaining", "defending"],
            "submission": ["sorry", "apologizing", "agreeing", "giving in", "complying"]
        }
    
    def analyze_conversation(self, conversation_text: str) -> Dict[str, Any]:
        """
        Comprehensive conversation analysis with multiple detection methods
        """
        try:
            # Parse conversation structure
            conversation_data = self._parse_conversation(conversation_text)
            
            # Multi-layered analysis
            analysis_results = {
                "conversation_structure": conversation_data,
                "emotional_analysis": self._analyze_emotional_dynamics(conversation_data),
                "power_analysis": self._analyze_power_dynamics(conversation_data),
                "abuse_indicators": self._detect_abuse_indicators(conversation_data),
                "sentiment_analysis": self._analyze_sentiment(conversation_data),
                "risk_assessment": self._assess_risk_level(conversation_data),
                "ai_insights": self._get_ai_insights(conversation_text)
            }
            
            # Combine all analyses
            return self._synthesize_analysis(analysis_results)
            
        except Exception as e:
            print(f"Error in analysis: {e}")
            # Use enhanced fallback that leverages pattern detection
            return self._get_fallback_insights(conversation_text)
    
    def _parse_conversation(self, conversation_text: str) -> Dict[str, Any]:
        """Parse conversation into structured data"""
        lines = conversation_text.strip().split('\n')
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
                    "word_count": len(message.split()),
                    "sentiment_score": self._calculate_sentiment_score(message)
                })
        
        # Analyze conversation structure
        speakers = [msg["speaker"] for msg in messages]
        speaker_counts = Counter(speakers)
        
        return {
            "messages": messages,
            "total_messages": len(messages),
            "speakers": list(speaker_counts.keys()),
            "speaker_counts": dict(speaker_counts),
            "conversation_length": len(conversation_text),
            "is_balanced": len(set(speaker_counts.values())) <= 1
        }
    
    def _analyze_emotional_dynamics(self, conversation_data: Dict) -> Dict[str, Any]:
        """Analyze emotional patterns in the conversation"""
        messages = conversation_data["messages"]
        
        emotional_scores = {
            "fear": 0, "anger": 0, "sadness": 0, "confusion": 0,
            "defensiveness": 0, "submission": 0
        }
        
        emotional_indicators = []
        
        for message in messages:
            text_lower = message["message"].lower()
            
            for emotion, markers in self.emotional_markers.items():
                for marker in markers:
                    if marker in text_lower:
                        emotional_scores[emotion] += 1
                        emotional_indicators.append({
                            "emotion": emotion,
                            "marker": marker,
                            "speaker": message["speaker"],
                            "message": message["message"][:100] + "..." if len(message["message"]) > 100 else message["message"]
                        })
        
        # Calculate emotional imbalance
        total_emotional_indicators = sum(emotional_scores.values())
        dominant_emotion = max(emotional_scores, key=emotional_scores.get) if total_emotional_indicators > 0 else None
        
        return {
            "emotional_scores": emotional_scores,
            "total_emotional_indicators": total_emotional_indicators,
            "dominant_emotion": dominant_emotion,
            "emotional_indicators": emotional_indicators,
            "emotional_imbalance": total_emotional_indicators > 5
        }
    
    def _analyze_power_dynamics(self, conversation_data: Dict) -> Dict[str, Any]:
        """Analyze power dynamics between speakers"""
        messages = conversation_data["messages"]
        speaker_counts = conversation_data["speaker_counts"]
        
        if len(speaker_counts) < 2:
            return {"error": "Need at least 2 speakers for power analysis"}
        
        # Calculate power indicators for each speaker
        power_indicators = {}
        
        for speaker in speaker_counts.keys():
            speaker_messages = [msg for msg in messages if msg["speaker"] == speaker]
            
            power_score = 0
            indicators = []
            
            for message in speaker_messages:
                text_lower = message["message"].lower()
                
                # Check for power indicators
                for category, patterns in self.abuse_indicators.items():
                    for pattern in patterns:
                        if pattern in text_lower:
                            power_score += 1
                            indicators.append({
                                "category": category,
                                "pattern": pattern,
                                "message": message["message"]
                            })
            
            power_indicators[speaker] = {
                "power_score": power_score,
                "message_count": len(speaker_messages),
                "avg_message_length": sum(msg["length"] for msg in speaker_messages) / len(speaker_messages),
                "indicators": indicators
            }
        
        # Determine power imbalance
        power_scores = {speaker: data["power_score"] for speaker, data in power_indicators.items()}
        max_power_speaker = max(power_scores, key=power_scores.get)
        power_imbalance = max(power_scores.values()) - min(power_scores.values())
        
        return {
            "power_indicators": power_indicators,
            "power_imbalance": power_imbalance,
            "dominant_speaker": max_power_speaker,
            "is_power_imbalanced": power_imbalance > 3
        }
    
    def _detect_abuse_indicators(self, conversation_data: Dict) -> Dict[str, Any]:
        """Detect specific abuse indicators"""
        messages = conversation_data["messages"]
        
        detected_indicators = {
            "power_imbalance": [],
            "control_tactics": [],
            "emotional_manipulation": [],
            "isolation_attempts": [],
            "threats": [],
            "gaslighting": [],
            "guilt_tripping": []
        }
        
        for message in messages:
            text_lower = message["message"].lower()
            
            for category, patterns in self.abuse_indicators.items():
                for pattern in patterns:
                    if pattern in text_lower:
                        detected_indicators[category].append({
                            "speaker": message["speaker"],
                            "pattern": pattern,
                            "message": message["message"],
                            "context": self._get_context(message["message"], pattern)
                        })
        
        # Calculate severity scores
        severity_scores = {}
        for category, indicators in detected_indicators.items():
            severity_scores[category] = len(indicators)
        
        total_indicators = sum(severity_scores.values())
        
        return {
            "detected_indicators": detected_indicators,
            "severity_scores": severity_scores,
            "total_indicators": total_indicators,
            "most_severe_category": max(severity_scores, key=severity_scores.get) if total_indicators > 0 else None
        }
    
    def _analyze_sentiment(self, conversation_data: Dict) -> Dict[str, Any]:
        """Analyze sentiment patterns"""
        messages = conversation_data["messages"]
        
        sentiment_scores = []
        speaker_sentiments = {}
        
        for message in messages:
            sentiment = message["sentiment_score"]
            sentiment_scores.append(sentiment)
            
            speaker = message["speaker"]
            if speaker not in speaker_sentiments:
                speaker_sentiments[speaker] = []
            speaker_sentiments[speaker].append(sentiment)
        
        # Calculate average sentiments
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        speaker_avg_sentiments = {}
        for speaker, sentiments in speaker_sentiments.items():
            speaker_avg_sentiments[speaker] = sum(sentiments) / len(sentiments)
        
        # Detect sentiment patterns
        negative_messages = [msg for msg in messages if msg["sentiment_score"] < -0.3]
        positive_messages = [msg for msg in messages if msg["sentiment_score"] > 0.3]
        
        return {
            "overall_sentiment": avg_sentiment,
            "speaker_sentiments": speaker_avg_sentiments,
            "negative_messages": len(negative_messages),
            "positive_messages": len(positive_messages),
            "sentiment_imbalance": len(negative_messages) - len(positive_messages),
            "is_negative_dominant": len(negative_messages) > len(positive_messages) * 2
        }
    
    def _assess_risk_level(self, conversation_data: Dict) -> Dict[str, Any]:
        """Comprehensive risk assessment with improved accuracy"""
        # Get all analysis components
        emotional_analysis = self._analyze_emotional_dynamics(conversation_data)
        power_analysis = self._analyze_power_dynamics(conversation_data)
        abuse_indicators = self._detect_abuse_indicators(conversation_data)
        sentiment_analysis = self._analyze_sentiment(conversation_data)
        
        # Calculate risk score with improved weighting
        risk_score = 0
        
        # Emotional indicators (weighted more heavily)
        if emotional_analysis["emotional_imbalance"]:
            risk_score += 15
        if emotional_analysis["dominant_emotion"] in ["fear", "anger"]:
            risk_score += 20
        if emotional_analysis["total_emotional_indicators"] > 3:
            risk_score += 10
        
        # Power dynamics (critical factor)
        if power_analysis.get("is_power_imbalanced", False):
            risk_score += 25
        if power_analysis.get("power_imbalance", 0) > 5:
            risk_score += 20
        if power_analysis.get("power_imbalance", 0) > 10:
            risk_score += 15
        
        # Abuse indicators (most important)
        risk_score += abuse_indicators["total_indicators"] * 8
        
        # Sentiment analysis
        if sentiment_analysis["is_negative_dominant"]:
            risk_score += 15
        if sentiment_analysis["sentiment_imbalance"] < -5:
            risk_score += 10
        if sentiment_analysis["negative_messages"] > sentiment_analysis["positive_messages"] * 3:
            risk_score += 10
        
        # Conversation structure analysis
        if not conversation_data["is_balanced"]:
            risk_score += 5
        
        # Determine risk level with improved thresholds
        if risk_score >= 70:
            risk_level = "Likely Abuse"
        elif risk_score >= 40:
            risk_level = "Concerning"
        elif risk_score >= 20:
            risk_level = "Concerning"
        else:
            risk_level = "Safe"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": {
                "emotional_imbalance": emotional_analysis["emotional_imbalance"],
                "power_imbalance": power_analysis.get("is_power_imbalanced", False),
                "abuse_indicators": abuse_indicators["total_indicators"],
                "negative_sentiment": sentiment_analysis["is_negative_dominant"],
                "conversation_imbalance": not conversation_data["is_balanced"]
            }
        }
    
    def _get_ai_insights(self, conversation_text: str) -> Dict[str, Any]:
        """Get AI-powered insights using NIM/Nemotron"""
        try:
            prompt = self._create_advanced_prompt(conversation_text)
            ai_response = self._send_to_nim(prompt)
            return self._parse_ai_response(ai_response)
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return self._get_fallback_insights(conversation_text)
    
    def _create_advanced_prompt(self, conversation_text: str) -> str:
        """Create sophisticated prompt for AI analysis"""
        return f"""
You are SilentSignal, an expert AI assistant specializing in detecting emotional abuse, manipulation, and coercive control patterns in conversations.

Analyze the following conversation for signs of emotional abuse, manipulation, gaslighting, guilt-tripping, threats, control tactics, and other harmful patterns.

CONVERSATION TO ANALYZE:
{conversation_text}

Please provide a comprehensive analysis in the following JSON format:
{{
    "risk_level": "Safe|Concerning|Likely Abuse",
    "abuse_patterns": [
        {{
            "pattern": "gaslighting",
            "description": "Specific example of gaslighting found",
            "severity": "high",
            "evidence": "Exact quote from conversation"
        }}
    ],
    "emotional_dynamics": {{
        "power_imbalance": "Description of power dynamics",
        "emotional_manipulation": "Evidence of emotional manipulation",
        "victim_response": "How the victim is responding"
    }},
    "red_flags": [
        "Specific concerning phrases or patterns found",
        "Another red flag example"
    ],
    "suggestions": [
        "Gentle, supportive suggestion for the person",
        "Another helpful suggestion"
    ],
    "emotional_analysis": "Detailed analysis of emotional dynamics and power balance",
    "summary": "Overall assessment with specific evidence",
    "safety_concerns": "Any immediate safety concerns identified"
}}

Focus on these specific patterns:
1. **Gaslighting**: Denying reality, making someone question their memory/perception
2. **Guilt-tripping**: Making someone feel guilty for normal behavior
3. **Threats**: Direct or implied threats (including self-harm threats)
4. **Control tactics**: Attempts to control behavior, relationships, or decisions
5. **Emotional manipulation**: Using emotions to get compliance
6. **Isolation attempts**: Trying to cut off support systems
7. **Intimidation**: Using fear or intimidation
8. **Minimization**: Downplaying concerns or feelings
9. **Blame-shifting**: Making everything the other person's fault
10. **Love-bombing**: Excessive affection followed by withdrawal
11. **Power imbalance**: One person dominating the conversation
12. **Victim-blaming**: Making the victim responsible for the abuse

Be thorough, specific, and supportive in your analysis. Focus on patterns rather than individual words.
"""
    
    def _send_to_nim(self, prompt: str) -> str:
        """Send prompt to NVIDIA NIM endpoint"""
        try:
            # If using hosted endpoint without an API key, skip to fallback
            if (self.nim_endpoint.startswith('https://integrate.api.nvidia.com') and not self.api_key):
                return None
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}' if self.api_key else ''
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1500,
                "temperature": 0.2,
                "stream": False
            }
            
            response = requests.post(
                f"{self.nim_endpoint}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"NIM API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response and extract structured data"""
        try:
            if response:
                # Look for JSON block in the response
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                
                if start_idx != -1 and end_idx != -1:
                    json_str = response[start_idx:end_idx]
                    return json.loads(json_str)
            
            return self._get_fallback_insights("")
            
        except json.JSONDecodeError:
            return self._get_fallback_insights("")
    
    def _synthesize_analysis(self, analysis_results: Dict) -> Dict[str, Any]:
        """Synthesize all analysis components into final result"""
        risk_assessment = analysis_results["risk_assessment"]
        abuse_indicators = analysis_results["abuse_indicators"]
        ai_insights = analysis_results["ai_insights"]
        
        # Combine red flags from all sources
        red_flags = []
        
        # From abuse indicators
        for category, indicators in abuse_indicators["detected_indicators"].items():
            for indicator in indicators:
                red_flags.append(f"{category.replace('_', ' ').title()}: {indicator['pattern']}")
        
        # From AI insights
        if "red_flags" in ai_insights:
            red_flags.extend(ai_insights["red_flags"])
        
        # Get suggestions
        suggestions = ai_insights.get("suggestions", [
            "Trust your instincts about how this conversation makes you feel",
            "Consider talking to a trusted friend or counselor",
            "Remember that healthy relationships don't involve manipulation or control"
        ])
        
        return {
            "risk_level": risk_assessment["risk_level"],
            "risk_score": risk_assessment["risk_score"],
            "red_flags": red_flags[:10],  # Limit to top 10
            "suggestions": suggestions,
            "emotional_analysis": ai_insights.get("emotional_analysis", "Analysis incomplete"),
            "summary": ai_insights.get("summary", "Unable to complete full analysis"),
            "safety_concerns": ai_insights.get("safety_concerns", ""),
            "abuse_patterns": ai_insights.get("abuse_patterns", []),
            "detailed_analysis": analysis_results
        }
    
    def _calculate_sentiment_score(self, text: str) -> float:
        """Simple sentiment scoring"""
        positive_words = ["good", "great", "happy", "love", "wonderful", "amazing", "fantastic", "excellent"]
        negative_words = ["bad", "terrible", "awful", "hate", "horrible", "angry", "sad", "upset", "frustrated"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total_words = len(text.split())
        if total_words == 0:
            return 0
        
        return (positive_count - negative_count) / total_words
    
    def _get_context(self, message: str, pattern: str) -> str:
        """Get context around a pattern"""
        pattern_lower = pattern.lower()
        message_lower = message.lower()
        
        start_idx = message_lower.find(pattern_lower)
        if start_idx == -1:
            return message
        
        context_start = max(0, start_idx - 50)
        context_end = min(len(message), start_idx + len(pattern) + 50)
        
        return message[context_start:context_end]
    
    def _get_fallback_insights(self, conversation_text: str) -> Dict[str, Any]:
        """Enhanced fallback insights when AI is unavailable"""
        # Use the pattern-based analysis as fallback
        from pattern_detector import AdvancedPatternDetector
        pattern_detector = AdvancedPatternDetector()
        pattern_result = pattern_detector.detect_patterns(conversation_text)
        
        # Generate insights based on pattern analysis
        risk_level = pattern_result["risk_level"]
        patterns = pattern_result["patterns"]
        
        # Create red flags from detected patterns
        red_flags = []
        for pattern in patterns[:5]:  # Limit to top 5
            red_flags.append(f"{pattern['category'].replace('_', ' ').title()}: {pattern['description']}")
        
        # Generate contextual suggestions
        suggestions = self._generate_contextual_suggestions(risk_level, patterns)
        
        # Create emotional analysis
        emotional_analysis = self._generate_emotional_analysis(pattern_result)
        
        # Create summary
        summary = self._generate_summary(pattern_result, len(patterns))
        
        return {
            "risk_level": risk_level,
            "risk_score": pattern_result.get("risk_score", 0),
            "red_flags": red_flags,
            "suggestions": suggestions,
            "emotional_analysis": emotional_analysis,
            "summary": summary,
            "safety_concerns": self._assess_safety_concerns(risk_level, patterns),
            "abuse_patterns": patterns,
            "detailed_analysis": {"pattern_analysis": pattern_result}
        }
    
    def _generate_contextual_suggestions(self, risk_level: str, patterns: List) -> List[str]:
        """Generate contextual suggestions based on risk level and patterns"""
        suggestions = []
        
        if risk_level == "Safe":
            suggestions = [
                "This conversation appears healthy and respectful",
                "Continue communicating openly and honestly",
                "Remember that healthy relationships involve mutual respect"
            ]
        elif risk_level == "Concerning":
            suggestions = [
                "Pay attention to how this conversation makes you feel",
                "Consider discussing your concerns with a trusted friend or counselor",
                "Trust your instincts about the relationship dynamics",
                "Set clear boundaries about what behavior you find acceptable"
            ]
        else:  # Likely Abuse
            suggestions = [
                "This conversation shows concerning patterns of manipulation or control",
                "Please consider reaching out to a crisis hotline or counselor",
                "Your safety and well-being are important",
                "Consider talking to a trusted friend or family member",
                "Remember that you deserve to be treated with respect and kindness"
            ]
        
        # Add pattern-specific suggestions
        pattern_categories = [p["category"] for p in patterns]
        if "gaslighting" in pattern_categories:
            suggestions.append("Consider keeping a record of conversations to verify your memory")
        if "threats" in pattern_categories:
            suggestions.append("If you feel unsafe, please contact emergency services or a crisis hotline")
        if "isolation_attempts" in pattern_categories:
            suggestions.append("Maintain connections with friends and family - isolation is a red flag")
        
        return suggestions[:6]  # Limit to 6 suggestions
    
    def _generate_emotional_analysis(self, pattern_result: Dict) -> str:
        """Generate emotional analysis based on pattern detection"""
        total_patterns = pattern_result["total_patterns"]
        risk_level = pattern_result["risk_level"]
        
        if risk_level == "Safe":
            return "The conversation shows healthy communication patterns with mutual respect and understanding."
        elif risk_level == "Concerning":
            return f"Detected {total_patterns} concerning patterns that may indicate manipulation or unhealthy dynamics. The conversation shows signs of emotional manipulation or control tactics."
        else:
            return f"Multiple serious abuse patterns detected ({total_patterns} patterns). This conversation shows clear signs of emotional abuse, manipulation, and potentially dangerous behavior."
    
    def _generate_summary(self, pattern_result: Dict, pattern_count: int) -> str:
        """Generate summary based on analysis results"""
        risk_level = pattern_result["risk_level"]
        patterns = pattern_result["patterns"]
        
        if risk_level == "Safe":
            return "No concerning patterns detected. This appears to be a healthy conversation."
        elif risk_level == "Concerning":
            pattern_types = [p["category"] for p in patterns[:3]]
            return f"Detected concerning patterns including: {', '.join(pattern_types)}. Please review the relationship dynamics carefully."
        else:
            pattern_types = [p["category"] for p in patterns[:3]]
            return f"Multiple serious abuse patterns detected including: {', '.join(pattern_types)}. This conversation shows clear signs of emotional abuse and manipulation."
    
    def _assess_safety_concerns(self, risk_level: str, patterns: List) -> str:
        """Assess safety concerns based on analysis"""
        if risk_level == "Likely Abuse":
            pattern_categories = [p["category"] for p in patterns]
            if "threats" in pattern_categories:
                return "Immediate safety concern: Threats detected. Please consider your safety and reach out for help."
            elif "intimidation" in pattern_categories:
                return "Safety concern: Intimidation patterns detected. Consider reaching out to a crisis hotline."
            else:
                return "Safety concern: Multiple abuse patterns detected. Please consider seeking support."
        elif risk_level == "Concerning":
            return "Monitor the situation and trust your instincts. Consider seeking support if patterns continue."
        else:
            return "No immediate safety concerns detected."
    
    def _fallback_analysis(self, conversation_text: str) -> Dict[str, Any]:
        """Comprehensive fallback analysis"""
        # Basic keyword analysis
        concerning_keywords = [
            'you always', 'you never', 'you should', 'you must',
            'if you loved me', 'you made me', 'it\'s your fault',
            'you\'re crazy', 'you\'re imagining', 'that never happened',
            'you\'re too sensitive', 'you\'re overreacting', 'i\'ll leave you',
            'you\'ll be sorry', 'i\'ll hurt myself', 'you\'re selfish'
        ]
        
        found_patterns = []
        text_lower = conversation_text.lower()
        
        for keyword in concerning_keywords:
            if keyword in text_lower:
                found_patterns.append(f"Concerning phrase detected: '{keyword}'")
        
        # Determine risk level
        if len(found_patterns) >= 5:
            risk_level = "Likely Abuse"
        elif len(found_patterns) >= 2:
            risk_level = "Concerning"
        else:
            risk_level = "Safe"
        
        return {
            "risk_level": risk_level,
            "risk_score": len(found_patterns) * 5,
            "red_flags": found_patterns,
            "suggestions": [
                "Trust your instincts about how this conversation makes you feel",
                "Consider talking to a trusted friend or counselor",
                "Remember that healthy relationships don't involve manipulation or control",
                "If you feel unsafe, please reach out to a crisis hotline"
            ],
            "emotional_analysis": "Basic pattern analysis completed. For more detailed analysis, please ensure the AI service is running.",
            "summary": f"Found {len(found_patterns)} concerning patterns. Please review carefully and seek support if needed.",
            "safety_concerns": "Please assess your safety and reach out for help if needed."
        }