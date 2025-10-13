import re
import json
from typing import Dict, List, Any, Tuple
from collections import defaultdict

class AdvancedPatternDetector:
    """
    Advanced pattern detector for emotional abuse with sophisticated analysis
    Uses multiple detection methods and scoring systems
    """
    
    def __init__(self):
        self.patterns = self._initialize_advanced_patterns()
        self.context_patterns = self._initialize_context_patterns()
        self.severity_weights = self._initialize_severity_weights()
        
    def _initialize_advanced_patterns(self) -> Dict[str, Dict]:
        """Initialize comprehensive patterns with context awareness"""
        return {
            "gaslighting": {
                "patterns": [
                    r"that never happened",
                    r"you're imagining things",
                    r"you're making that up",
                    r"that's not what i said",
                    r"you're remembering it wrong",
                    r"you're crazy",
                    r"you're delusional",
                    r"that's all in your head",
                    r"you're confused",
                    r"you're misremembering",
                    r"that's not how it went",
                    r"you're twisting my words",
                    r"i never said that",
                    r"you're hearing things",
                    r"that's not what happened",
                    r"you're making it up",
                    r"you're lying about that",
                    r"that's not true",
                    r"you're wrong about that",
                    r"you're mistaken"
                ],
                "severity": "high",
                "description": "Making someone question their reality, memory, or sanity"
            },
            "guilt_tripping": {
                "patterns": [
                    r"if you loved me",
                    r"after all i've done for you",
                    r"you're ungrateful",
                    r"i do everything for you",
                    r"you don't appreciate me",
                    r"i sacrifice so much for you",
                    r"you're selfish",
                    r"you don't care about me",
                    r"you're breaking my heart",
                    r"i give up everything for you",
                    r"you're hurting me",
                    r"i'm always there for you",
                    r"you never think about me",
                    r"i put you first always",
                    r"you're so ungrateful",
                    r"after everything i've given you",
                    r"you're taking me for granted",
                    r"i deserve better than this",
                    r"you're making me feel worthless",
                    r"i'm not asking for much"
                ],
                "severity": "medium",
                "description": "Using guilt to manipulate behavior and compliance"
            },
            "threats": {
                "patterns": [
                    r"i'll leave you",
                    r"you'll be sorry",
                    r"i'll make you pay",
                    r"you'll regret this",
                    r"i'll hurt myself",
                    r"i'll kill myself",
                    r"you'll never find someone like me",
                    r"i'll ruin your life",
                    r"you'll lose everything",
                    r"i'll destroy you",
                    r"you'll pay for this",
                    r"i'll make you suffer",
                    r"you'll wish you never met me",
                    r"i'll take everything from you",
                    r"you'll be alone forever",
                    r"i'll hurt someone you love",
                    r"you'll never be happy again",
                    r"i'll make sure you suffer",
                    r"you'll get what's coming to you",
                    r"i'll make you miserable"
                ],
                "severity": "critical",
                "description": "Direct or implied threats to control or intimidate"
            },
            "control_tactics": {
                "patterns": [
                    r"you can't",
                    r"you're not allowed",
                    r"i forbid you",
                    r"you must",
                    r"you have to",
                    r"don't you dare",
                    r"you better not",
                    r"i won't let you",
                    r"you're not going to",
                    r"i don't want you to",
                    r"you shouldn't",
                    r"i don't allow",
                    r"you're forbidden",
                    r"i won't permit",
                    r"you're not permitted",
                    r"i control this",
                    r"you need my permission",
                    r"i decide what you do",
                    r"you'll do as i say",
                    r"i'm in charge here"
                ],
                "severity": "high",
                "description": "Attempts to control behavior, choices, or decisions"
            },
            "emotional_manipulation": {
                "patterns": [
                    r"you're too sensitive",
                    r"you're overreacting",
                    r"you're being dramatic",
                    r"you're making a big deal",
                    r"you're being ridiculous",
                    r"you're being childish",
                    r"grow up",
                    r"get over it",
                    r"stop crying",
                    r"you're being emotional",
                    r"you're hysterical",
                    r"you're irrational",
                    r"you're being stupid",
                    r"you're acting crazy",
                    r"you're being paranoid",
                    r"you're overthinking",
                    r"you're being negative",
                    r"you're always complaining",
                    r"you're being difficult",
                    r"you're impossible to deal with"
                ],
                "severity": "medium",
                "description": "Invalidating emotions and making someone feel wrong for feeling"
            },
            "isolation_attempts": {
                "patterns": [
                    r"your friends don't like me",
                    r"your family is toxic",
                    r"they're trying to break us up",
                    r"don't listen to them",
                    r"they don't understand us",
                    r"they're jealous",
                    r"they're bad influences",
                    r"you shouldn't trust them",
                    r"they're manipulating you",
                    r"they don't care about you",
                    r"they're using you",
                    r"they're not good for you",
                    r"they're trying to control you",
                    r"they're brainwashing you",
                    r"they're turning you against me",
                    r"they're the problem",
                    r"you don't need them",
                    r"i'm all you need",
                    r"they're holding you back",
                    r"they're jealous of our relationship"
                ],
                "severity": "high",
                "description": "Attempting to cut someone off from their support system"
            },
            "blame_shifting": {
                "patterns": [
                    r"you made me do this",
                    r"it's your fault",
                    r"you caused this",
                    r"you started it",
                    r"you provoked me",
                    r"you pushed me to this",
                    r"you're the problem",
                    r"you're the one who",
                    r"you made me angry",
                    r"you're making me act this way",
                    r"you're forcing me to",
                    r"you're driving me crazy",
                    r"you're making me lose control",
                    r"you're the reason i'm like this",
                    r"you're destroying our relationship",
                    r"you're ruining everything",
                    r"you're the one with issues",
                    r"you're the toxic one",
                    r"you're the abusive one",
                    r"you're the one who needs help"
                ],
                "severity": "high",
                "description": "Making someone else responsible for your actions or behavior"
            },
            "minimization": {
                "patterns": [
                    r"it's not that bad",
                    r"you're exaggerating",
                    r"it's not a big deal",
                    r"you're being dramatic",
                    r"other people have it worse",
                    r"you're lucky",
                    r"it could be worse",
                    r"stop complaining",
                    r"you're overreacting",
                    r"it's not worth getting upset about",
                    r"you're making mountains out of molehills",
                    r"it's not important",
                    r"you're being silly",
                    r"it's not worth it",
                    r"you're being petty",
                    r"it's nothing",
                    r"you're being ridiculous",
                    r"it's not worth your time",
                    r"you're being childish",
                    r"it's not that serious"
                ],
                "severity": "medium",
                "description": "Downplaying concerns, feelings, or experiences"
            },
            "love_bombing": {
                "patterns": [
                    r"i love you more than anything",
                    r"you're my everything",
                    r"i can't live without you",
                    r"you're perfect",
                    r"i've never felt this way",
                    r"you're my soulmate",
                    r"i'll do anything for you",
                    r"you're the only one for me",
                    r"you're my world",
                    r"i'm nothing without you",
                    r"you're my reason for living",
                    r"i'll die without you",
                    r"you're my everything",
                    r"i'm obsessed with you",
                    r"you're my addiction",
                    r"i can't get enough of you",
                    r"you're my drug",
                    r"i'm addicted to you",
                    r"you're my life",
                    r"i worship you"
                ],
                "severity": "medium",
                "description": "Excessive affection used as manipulation tactic"
            },
            "intimidation": {
                "patterns": [
                    r"you don't want to make me angry",
                    r"you're pushing my buttons",
                    r"i'm warning you",
                    r"you're testing my patience",
                    r"don't make me",
                    r"you're asking for trouble",
                    r"i'm not someone you want to mess with",
                    r"you'll learn not to cross me",
                    r"you're playing with fire",
                    r"you're walking on thin ice",
                    r"you're skating on thin ice",
                    r"you're treading dangerous ground",
                    r"you're pushing your luck",
                    r"you're asking for it",
                    r"you're looking for trouble",
                    r"you're being stupid",
                    r"you're making a mistake",
                    r"you'll regret this",
                    r"you're being foolish",
                    r"you're being reckless"
                ],
                "severity": "high",
                "description": "Using fear or intimidation to control behavior"
            },
            "financial_control": {
                "patterns": [
                    r"you can't afford it",
                    r"we don't have money for that",
                    r"you're wasting money",
                    r"you're being irresponsible",
                    r"i control the money",
                    r"you don't need that",
                    r"you're being selfish",
                    r"you're spending too much",
                    r"you're being greedy",
                    r"you don't deserve that",
                    r"you're being materialistic",
                    r"you're shallow",
                    r"you only care about money",
                    r"you're using me for money",
                    r"you're a gold digger",
                    r"you're only with me for money",
                    r"you're being manipulative",
                    r"you're trying to control me",
                    r"you're being abusive",
                    r"you're the problem"
                ],
                "severity": "high",
                "description": "Using money or financial control as manipulation"
            },
            "sexual_coercion": {
                "patterns": [
                    r"if you loved me you would",
                    r"you owe me",
                    r"you're being selfish",
                    r"you're not attracted to me",
                    r"you're rejecting me",
                    r"you're hurting me",
                    r"you're being cruel",
                    r"you're being mean",
                    r"you're being unfair",
                    r"you're being unreasonable",
                    r"you're being difficult",
                    r"you're being stubborn",
                    r"you're being childish",
                    r"you're being immature",
                    r"you're being selfish",
                    r"you're being inconsiderate",
                    r"you're being thoughtless",
                    r"you're being cold",
                    r"you're being distant",
                    r"you're being unloving"
                ],
                "severity": "critical",
                "description": "Using manipulation to coerce sexual activity"
            },
            "passive_aggressive": {
                "patterns": [
                    r"oh great",
                    r"that's fine",
                    r"whatever",
                    r"i'm used to it",
                    r"i don't care",
                    r"do whatever you want",
                    r"i'm not mad",
                    r"it's whatever",
                    r"i'm fine",
                    r"nothing's wrong",
                    r"i'm not upset",
                    r"it doesn't matter",
                    r"i don't mind",
                    r"it's up to you",
                    r"i'm not bothered",
                    r"it's not a big deal",
                    r"i'm not complaining",
                    r"i'm not saying anything",
                    r"i'm not going to argue",
                    r"i'm not going to fight"
                ],
                "severity": "medium",
                "description": "Passive-aggressive behavior and indirect hostility"
            },
            "sarcasm": {
                "patterns": [
                    r"oh wonderful",
                    r"that's just great",
                    r"how lovely",
                    r"what a surprise",
                    r"how nice",
                    r"that's perfect",
                    r"exactly what i wanted",
                    r"just what i needed",
                    r"how thoughtful",
                    r"how considerate",
                    r"that's helpful",
                    r"that's useful",
                    r"how kind",
                    r"how generous",
                    r"how sweet",
                    r"how thoughtful",
                    r"how caring",
                    r"how loving",
                    r"how romantic",
                    r"how perfect"
                ],
                "severity": "low",
                "description": "Sarcastic comments and tone"
            }
        }
    
    def _initialize_context_patterns(self) -> Dict[str, List[str]]:
        """Patterns that indicate context of abuse"""
        return {
            "escalation": [
                r"i'm getting angry",
                r"you're making me mad",
                r"i'm losing my temper",
                r"you're pushing me too far",
                r"i'm about to lose it",
                r"you're testing my limits",
                r"i'm reaching my breaking point",
                r"you're driving me crazy",
                r"i'm losing control",
                r"you're making me snap"
            ],
            "victim_blaming": [
                r"you asked for it",
                r"you deserved it",
                r"you brought this on yourself",
                r"you made me do this",
                r"you're asking for trouble",
                r"you're looking for a fight",
                r"you're being difficult",
                r"you're being unreasonable",
                r"you're being impossible",
                r"you're being stubborn"
            ],
            "power_imbalance": [
                r"i'm the man here",
                r"i'm in charge",
                r"i make the decisions",
                r"you don't get a say",
                r"i know what's best",
                r"you're not smart enough",
                r"you're not capable",
                r"you need me",
                r"you can't survive without me",
                r"you're helpless without me"
            ]
        }
    
    def _initialize_severity_weights(self) -> Dict[str, int]:
        """Weights for different severity levels"""
        return {
            "critical": 10,
            "high": 7,
            "medium": 4,
            "low": 2
        }
    
    def detect_patterns(self, conversation_text: str) -> Dict[str, Any]:
        """
        Advanced pattern detection with context awareness and scoring
        """
        detected_patterns = []
        pattern_counts = defaultdict(int)
        severity_scores = defaultdict(int)
        context_indicators = []
        
        # Convert to lowercase for case-insensitive matching
        text_lower = conversation_text.lower()
        
        # Split into sentences for better context analysis
        sentences = re.split(r'[.!?]+', text_lower)
        
        # Check each pattern category
        for category, pattern_data in self.patterns.items():
            category_matches = []
            severity = pattern_data["severity"]
            weight = self.severity_weights[severity]
            
            for pattern in pattern_data["patterns"]:
                matches = re.findall(pattern, text_lower)
                if matches:
                    category_matches.extend(matches)
                    pattern_counts[category] += len(matches)
                    severity_scores[category] += len(matches) * weight
            
            if category_matches:
                detected_patterns.append({
                    "category": category,
                    "description": pattern_data["description"],
                    "severity": severity,
                    "matches": category_matches[:3],  # Show first 3 matches
                    "count": len(category_matches),
                    "score": severity_scores[category]
                })
        
        # Check for context patterns
        for context_type, patterns in self.context_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    context_indicators.append(context_type)
                    break
        
        # Calculate overall risk score
        total_score = sum(severity_scores.values())
        risk_level = self._calculate_risk_level(total_score, pattern_counts, context_indicators)
        
        # Analyze conversation dynamics
        dynamics = self._analyze_conversation_dynamics(conversation_text)
        
        return {
            "patterns": detected_patterns,
            "pattern_counts": dict(pattern_counts),
            "total_patterns": sum(pattern_counts.values()),
            "risk_level": risk_level,
            "risk_score": total_score,
            "context_indicators": context_indicators,
            "dynamics": dynamics,
            "severity_breakdown": dict(severity_scores)
        }
    
    def _calculate_risk_level(self, total_score: int, pattern_counts: Dict, context_indicators: List) -> str:
        """Calculate risk level based on multiple factors with improved accuracy"""
        # Base scoring with more nuanced thresholds
        if total_score >= 60:
            return "Likely Abuse"
        elif total_score >= 35:
            return "Concerning"
        elif total_score >= 15:
            return "Concerning"
        
        # Context-based adjustments
        if "escalation" in context_indicators and total_score >= 20:
            return "Likely Abuse"
        if "victim_blaming" in context_indicators and total_score >= 25:
            return "Likely Abuse"
        if "power_imbalance" in context_indicators and total_score >= 20:
            return "Concerning"
        
        # Pattern count adjustments with more specific thresholds
        if len(pattern_counts) >= 6:
            return "Likely Abuse"
        elif len(pattern_counts) >= 4:
            return "Concerning"
        elif len(pattern_counts) >= 2:
            return "Concerning"
        
        # Check for specific high-severity patterns
        high_severity_patterns = ["threats", "gaslighting", "intimidation", "sexual_coercion"]
        high_severity_count = sum(pattern_counts.get(pattern, 0) for pattern in high_severity_patterns)
        
        if high_severity_count >= 2:
            return "Likely Abuse"
        elif high_severity_count >= 1 and total_score >= 10:
            return "Concerning"
        
        return "Safe"
    
    def _analyze_conversation_dynamics(self, conversation_text: str) -> Dict[str, Any]:
        """Analyze conversation dynamics and power balance"""
        lines = conversation_text.split('\n')
        person_a_lines = []
        person_b_lines = []
        
        for line in lines:
            if line.strip().startswith('Person A:'):
                person_a_lines.append(line)
            elif line.strip().startswith('Person B:'):
                person_b_lines.append(line)
        
        # Calculate message counts
        a_count = len(person_a_lines)
        b_count = len(person_b_lines)
        
        # Analyze message length
        a_avg_length = sum(len(line) for line in person_a_lines) / max(a_count, 1)
        b_avg_length = sum(len(line) for line in person_b_lines) / max(b_count, 1)
        
        # Check for one-sided conversations
        total_messages = a_count + b_count
        if total_messages > 0:
            a_percentage = (a_count / total_messages) * 100
            b_percentage = (b_count / total_messages) * 100
        else:
            a_percentage = b_percentage = 0
        
        return {
            "person_a_messages": a_count,
            "person_b_messages": b_count,
            "person_a_avg_length": round(a_avg_length, 1),
            "person_b_avg_length": round(b_avg_length, 1),
            "person_a_percentage": round(a_percentage, 1),
            "person_b_percentage": round(b_percentage, 1),
            "is_one_sided": abs(a_percentage - b_percentage) > 30,
            "total_messages": total_messages
        }
    
    def get_pattern_explanations(self) -> Dict[str, str]:
        """Get detailed explanations for different abuse patterns"""
        explanations = {}
        for category, data in self.patterns.items():
            explanations[category] = data["description"]
        return explanations