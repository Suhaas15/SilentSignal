"""
NVIDIA NIM Client for Nemotron-3 Integration
Handles communication with NVIDIA NIM API
"""

import requests
import json
import os
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class NimoClient:
    """
    Client for NVIDIA NIM API with Nemotron-3 integration
    """
    
    def __init__(self):
        # Prefer NVIDIA hosted endpoint by default; can be overridden in .env
        self.base_url = os.getenv('NIM_BASE_URL', 'https://integrate.api.nvidia.com/v1')
        self.api_key = os.getenv('NIM_API_KEY', '')
        self.model = os.getenv('NIM_MODEL', 'nvidia/nemotron-3-8b-instruct')
        self.timeout = int(os.getenv('ANALYSIS_TIMEOUT', '30'))
        self.use_openai_sdk = os.getenv('NIM_USE_OPENAI_SDK', '0') == '1'
        self.reason_min = int(os.getenv('NIM_REASONING_MIN', '0'))
        self.reason_max = int(os.getenv('NIM_REASONING_MAX', '0'))
        
    def analyze_conversation(self, conversation_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze conversation using Nemotron-3 with enriched context
        
        Args:
            conversation_text: The conversation to analyze
            context: Additional context from RAG and pattern detection
            
        Returns:
            Structured analysis result
        """
        try:
            # Create enriched prompt with RAG context
            prompt = self._create_enriched_prompt(conversation_text, context)
            
            # Call Nemotron-3 via NIM (OpenAI SDK if enabled, else raw requests)
            if self.use_openai_sdk:
                response = self._call_nim_api_openai(prompt)
            else:
                response = self._call_nim_api(prompt)
            
            # Parse and validate response
            result = self._parse_response(response)
            
            return result
            
        except Exception as e:
            logger.error(f"NIM API error: {e}")
            return self._get_fallback_response(conversation_text)
    
    def _create_enriched_prompt(self, conversation_text: str, context: Dict[str, Any]) -> str:
        """Create prompt enriched with RAG context and pattern information"""
        
        # Extract RAG context
        rag_patterns = context.get('rag_patterns', [])
        detected_patterns = context.get('detected_patterns', [])
        
        # Build context section
        context_section = ""
        if rag_patterns:
            context_section += "\n\nRELEVANT PATTERN DEFINITIONS:\n"
            for pattern in rag_patterns:
                context_section += f"- {pattern['name']}: {pattern['definition']}\n"
        
        if detected_patterns:
            context_section += "\n\nDETECTED PATTERNS:\n"
            for pattern in detected_patterns:
                context_section += f"- {pattern['category']}: {pattern['description']}\n"
        
        prompt = f"""You are SilentSignal, an expert AI assistant specializing in detecting emotional abuse, manipulation, and coercive control patterns in conversations.

Your task is to analyze the following conversation for signs of emotional abuse, manipulation, gaslighting, guilt-tripping, threats, control tactics, and other harmful patterns.

{context_section}

CONVERSATION TO ANALYZE:
{conversation_text}

Please provide a comprehensive analysis in the following JSON format:
{{
    "risk_level": "safe|concerning|abuse",
    "patterns": [
        {{
            "name": "gaslighting",
            "description": "Specific example of gaslighting found",
            "severity": "high",
            "evidence": "Exact quote from conversation"
        }}
    ],
    "summary": "Overall assessment with specific evidence",
    "red_flags": [
        "Specific concerning phrases or patterns found",
        "Another red flag example"
    ],
    "suggestions": [
        "Gentle, supportive suggestion for the person",
        "Another helpful suggestion"
    ],
    "reasoning": "Explanation of how the analysis was conducted",
    "confidence": 0.85
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

Be thorough, specific, and supportive in your analysis. Focus on patterns rather than individual words.
"""
        return prompt
    
    def _call_nim_api(self, prompt: str) -> Optional[str]:
        """Call NVIDIA NIM API with the prompt"""
        try:
            # If using hosted endpoint without an API key, fail fast to fallback
            if (self.base_url.startswith('https://integrate.api.nvidia.com') and not self.api_key):
                logger.warning("NIM_BASE_URL points to NVIDIA hosted endpoint but NIM_API_KEY is missing. Falling back.")
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
                "max_tokens": 2000,
                "temperature": 0.2,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"NIM API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def _call_nim_api_openai(self, prompt: str) -> Optional[str]:
        """Call NVIDIA Integrate endpoint via OpenAI SDK (optional reasoning)."""
        try:
            # Lazy import to avoid hard dependency if not used
            from openai import OpenAI
        except Exception as e:
            logger.error(f"OpenAI SDK not available: {e}")
            return None

        # Require API key for hosted endpoint
        if (self.base_url.startswith('https://integrate.api.nvidia.com') and not self.api_key):
            logger.warning("NIM_BASE_URL points to NVIDIA hosted endpoint but NIM_API_KEY is missing. Falling back.")
            return None

        client = OpenAI(base_url=self.base_url, api_key=self.api_key)

        extra_body: Dict[str, Any] = {}
        if self.reason_min > 0 and self.reason_max > 0:
            # Models that support reasoning can accept these fields
            extra_body = {
                "min_thinking_tokens": self.reason_min,
                "max_thinking_tokens": self.reason_max,
            }

        try:
            completion = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2000,
                stream=False,
                extra_body=extra_body if extra_body else None,
            )

            choice = completion.choices[0]
            # Prefer message content; include reasoning_content if present
            content = getattr(choice.message, 'content', None)
            reasoning = getattr(choice.message, 'reasoning_content', None)
            if reasoning and content:
                return f"Reasoning:\n{reasoning}\n\nAnswer:\n{content}"
            return content or None
        except Exception as e:
            logger.error(f"NIM(OpenAI) API error: {e}")
            return None

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate Nemotron response"""
        try:
            if response:
                # Look for JSON block in the response
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                
                if start_idx != -1 and end_idx != -1:
                    json_str = response[start_idx:end_idx]
                    result = json.loads(json_str)
                    
                    # Validate required fields
                    required_fields = ['risk_level', 'patterns', 'summary', 'red_flags', 'suggestions']
                    for field in required_fields:
                        if field not in result:
                            result[field] = []
                    
                    return result
            
            return self._get_fallback_response("")
            
        except json.JSONDecodeError:
            logger.error("Failed to parse NIM response as JSON")
            return self._get_fallback_response("")
    
    def _get_fallback_response(self, conversation_text: str) -> Dict[str, Any]:
        """Fallback response when NIM is unavailable"""
        return {
            "risk_level": "concerning",
            "patterns": [
                {
                    "name": "analysis_unavailable",
                    "description": "AI analysis unavailable - using fallback detection",
                    "severity": "medium",
                    "evidence": "Technical limitation"
                }
            ],
            "summary": "Unable to complete full AI analysis. Please review the conversation carefully and trust your instincts.",
            "red_flags": ["AI analysis unavailable - please use pattern detection results"],
            "suggestions": [
                "Please review the conversation carefully",
                "Consider seeking support if you feel unsafe",
                "Trust your instincts about the relationship dynamics"
            ],
            "reasoning": "Fallback analysis due to technical limitations",
            "confidence": 0.3
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check if NIM API is available"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}' if self.api_key else ''
            }
            
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                return {"status": "healthy", "available": True}
            else:
                return {"status": "unhealthy", "available": False, "error": response.text}
                
        except Exception as e:
            return {"status": "unhealthy", "available": False, "error": str(e)}


