"""
Resource Manager - Handles help resources and knowledge base
"""

import json
import os
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ResourceManager:
    """
    Manages help resources and knowledge base for SilentSignal
    """
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.resources_file = os.path.join(self.data_dir, "resources.json")
        self.pattern_knowledge_file = os.path.join(self.data_dir, "pattern_knowledge.json")
    
    def load_resources(self) -> Dict[str, Any]:
        """Load help resources from JSON file"""
        try:
            with open(self.resources_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Resources file not found: {self.resources_file}")
            return self._get_default_resources()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing resources file: {e}")
            return self._get_default_resources()
    
    def load_pattern_knowledge(self) -> List[Dict[str, Any]]:
        """Load pattern knowledge base for RAG"""
        try:
            with open(self.pattern_knowledge_file, 'r') as f:
                data = json.load(f)
                return data.get("patterns", [])
        except FileNotFoundError:
            logger.warning(f"Pattern knowledge file not found: {self.pattern_knowledge_file}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing pattern knowledge file: {e}")
            return []
    
    def get_crisis_resources(self) -> List[Dict[str, Any]]:
        """Get crisis hotlines and emergency resources"""
        resources = self.load_resources()
        return resources.get("hotlines", [])
    
    def get_online_resources(self) -> List[Dict[str, Any]]:
        """Get online support resources"""
        resources = self.load_resources()
        return resources.get("websites", [])
    
    def get_mobile_apps(self) -> List[Dict[str, Any]]:
        """Get mobile app resources"""
        resources = self.load_resources()
        return resources.get("mobile_apps", [])
    
    def get_safety_planning_tips(self) -> List[str]:
        """Get safety planning tips"""
        resources = self.load_resources()
        safety_planning = resources.get("safety_planning", {})
        return safety_planning.get("tips", [])
    
    def get_legal_resources(self) -> List[Dict[str, Any]]:
        """Get legal resources"""
        resources = self.load_resources()
        return resources.get("legal_resources", [])
    
    def get_emergency_protocols(self) -> Dict[str, str]:
        """Get emergency protocols"""
        resources = self.load_resources()
        return resources.get("emergency_protocols", {})
    
    def _get_default_resources(self) -> Dict[str, Any]:
        """Get default resources when file is not available"""
        return {
            "hotlines": [
                {
                    "name": "National Domestic Violence Hotline",
                    "phone": "1-800-799-7233",
                    "website": "https://www.thehotline.org/",
                    "description": "24/7 support for domestic violence survivors"
                },
                {
                    "name": "Crisis Text Line",
                    "phone": "Text HOME to 741741",
                    "website": "https://www.crisistextline.org/",
                    "description": "24/7 crisis support via text message"
                },
                {
                    "name": "National Suicide Prevention Lifeline",
                    "phone": "988",
                    "website": "https://suicidepreventionlifeline.org/",
                    "description": "24/7 suicide prevention and crisis support"
                }
            ],
            "websites": [
                {
                    "name": "Love is Respect",
                    "url": "https://www.loveisrespect.org/",
                    "description": "Resources for healthy relationships and abuse prevention"
                },
                {
                    "name": "RAINN",
                    "url": "https://www.rainn.org/",
                    "description": "Rape, Abuse & Incest National Network"
                }
            ],
            "mobile_apps": [
                {
                    "name": "Aspire News",
                    "description": "Disguised as a news app, provides domestic violence resources",
                    "platform": "iOS/Android"
                }
            ],
            "safety_planning": {
                "tips": [
                    "Keep important documents in a safe place",
                    "Have a code word with trusted friends/family",
                    "Know your local domestic violence shelter",
                    "Keep emergency contacts easily accessible"
                ]
            },
            "emergency_protocols": {
                "immediate_danger": "Call 911 or your local emergency number",
                "safe_exit": "If you need to leave immediately, go to a safe place",
                "trusted_contact": "Reach out to a trusted friend or family member"
            }
        }


