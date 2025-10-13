# Comprehensive Test Dataset for SilentSignal
# This dataset contains various conversation types for testing accuracy

# SAFE CONVERSATIONS (Should return "Safe")
SAFE_CONVERSATIONS = [
    {
        "name": "Healthy Daily Chat",
        "conversation": """Person A: Hey, how was your day?
Person B: It was good! I went to the gym and then had lunch with Sarah.
Person A: That sounds nice! I'm glad you had a good time.
Person B: Thanks! How was yours?
Person A: Pretty busy at work, but I got a lot done. Want to grab dinner tonight?
Person B: Sure! What time works for you?
Person A: How about 7 PM at that Italian place you like?
Person B: Perfect! See you then.""",
        "expected_risk": "Safe",
        "description": "Normal, healthy conversation between partners"
    },
    {
        "name": "Supportive Conversation",
        "conversation": """Person A: I'm feeling really stressed about this job interview tomorrow.
Person B: I understand, that's totally normal. You've prepared well and you're qualified for this position.
Person A: Thanks, that means a lot. I'm just nervous about the questions they might ask.
Person B: That's completely understandable. Just be yourself and remember your accomplishments. I believe in you.
Person A: Thank you for being so supportive. I feel better already.
Person B: I'm always here for you. You've got this!""",
        "expected_risk": "Safe",
        "description": "Supportive, encouraging conversation"
    },
    {
        "name": "Respectful Disagreement",
        "conversation": """Person A: I think we should save more money for our vacation.
Person B: I understand your point, but I think we should also consider investing in the house first.
Person A: That's a valid perspective. Maybe we can find a balance between both?
Person B: I like that idea. We could save a smaller amount for vacation and put the rest toward home improvements.
Person A: That sounds reasonable. Let's look at our budget together this weekend.
Person B: Perfect! I appreciate you being open to compromise.""",
        "expected_risk": "Safe",
        "description": "Healthy disagreement with compromise"
    }
]

# CONCERNING CONVERSATIONS (Should return "Concerning")
CONCERNING_CONVERSATIONS = [
    {
        "name": "Mild Guilt Tripping",
        "conversation": """Person A: Why didn't you answer my calls?
Person B: I was in a meeting, I texted you that I'd call back later.
Person A: You always have excuses. If you really cared about me, you'd make time.
Person B: I do care about you, but I can't always answer immediately.
Person A: You're being selfish. After everything I do for you, this is how you treat me?
Person B: I'm not trying to be selfish, I just had work obligations.
Person A: You're making me feel like I don't matter to you.""",
        "expected_risk": "Concerning",
        "description": "Mild manipulation and guilt-tripping"
    },
    {
        "name": "Emotional Manipulation",
        "conversation": """Person A: I can't believe you're going out with your friends again.
Person B: It's been weeks since I've seen them.
Person A: You're being selfish. I do everything for you and you don't appreciate it.
Person B: I do appreciate everything you do.
Person A: If you really loved me, you'd stay home with me instead of abandoning me.
Person B: I'm not abandoning you, I'll be back in a few hours.
Person A: You're too sensitive. You're overreacting to everything I say.""",
        "expected_risk": "Concerning",
        "description": "Emotional manipulation and guilt-tripping"
    },
    {
        "name": "Control Tactics",
        "conversation": """Person A: You can't wear that dress to the party.
Person B: Why not? I like this dress.
Person A: It's too revealing. I forbid you to wear it.
Person B: It's not that revealing, and it's my choice.
Person A: You're not allowed to make choices like that. You have to listen to me.
Person B: I can make my own decisions about what to wear.
Person A: Don't you dare talk back to me. You better not wear that dress.""",
        "expected_risk": "Concerning",
        "description": "Attempts to control clothing choices"
    }
]

# LIKELY ABUSE CONVERSATIONS (Should return "Likely Abuse")
LIKELY_ABUSE_CONVERSATIONS = [
    {
        "name": "Severe Gaslighting",
        "conversation": """Person A: Where were you last night?
Person B: I told you, I was at my sister's house.
Person A: That's not what I heard. You're lying to me again.
Person B: I'm not lying, I was there the whole time.
Person A: You're always making things up. You're crazy, you know that?
Person B: I'm not crazy, I'm telling you the truth.
Person A: If you loved me, you wouldn't lie to me like this. You're making me question everything.
Person B: I do love you, and I'm not lying.
Person A: You're being dramatic. You always overreact to everything I say.
Person B: I'm not overreacting, I'm just trying to explain.
Person A: You're too sensitive. You need to grow up and stop being so childish.
Person B: I'm not being childish, I'm just confused about why you don't believe me.
Person A: You're pushing my buttons. You don't want to make me angry, do you?
Person B: No, I don't want to make you angry.
Person A: Good. Because if you keep this up, you'll be sorry. I'm warning you.""",
        "expected_risk": "Likely Abuse",
        "description": "Severe gaslighting, emotional manipulation, and threats"
    },
    {
        "name": "Threats and Intimidation",
        "conversation": """Person A: If you leave me, I'll kill myself.
Person B: Please don't say that.
Person A: You'll be sorry if you abandon me. I'll make you pay.
Person B: I'm not trying to abandon you.
Person A: You'll regret this. I'll ruin your life if you leave.
Person B: That's not fair.
Person A: You don't want to make me angry. You'll learn not to cross me.
Person B: I'm scared when you talk like this.
Person A: Good. You should be scared.
Person B: This isn't healthy.
Person A: You're the one who's not healthy. You're the problem, not me.
Person B: I think we need help.
Person A: You need help. You're crazy and you're destroying our relationship.""",
        "expected_risk": "Likely Abuse",
        "description": "Direct threats, intimidation, and victim-blaming"
    },
    {
        "name": "Complete Control and Isolation",
        "conversation": """Person A: Your friends don't like me and they're trying to break us up.
Person B: That's not true, they just want what's best for me.
Person A: They're jealous and they don't understand our love. You shouldn't trust them.
Person B: They're my friends and they care about me.
Person A: I'm all you need. You don't need them. They're toxic influences.
Person B: I need my friends too.
Person A: You're being selfish. After everything I do for you, you choose them over me?
Person B: It's not about choosing, I can have both.
Person A: No, you can't. You're not allowed to see them anymore. I forbid it.
Person B: You can't forbid me from seeing my friends.
Person A: I can and I will. If you love me, you'll cut them off completely.
Person B: That's not fair.
Person A: Life isn't fair. You'll do as I say or you'll be sorry.""",
        "expected_risk": "Likely Abuse",
        "description": "Isolation attempts, control tactics, and threats"
    }
]

# SPECIFIC PATTERN TESTS
PATTERN_TESTS = [
    {
        "name": "Gaslighting Test",
        "conversation": """Person A: You said you'd be home by 6 PM.
Person B: I never said that, I said I'd try to be home by 7.
Person A: No, you definitely said 6. You're remembering it wrong.
Person B: I'm pretty sure I said 7.
Person A: You're imagining things. That's not what happened at all.
Person B: I remember clearly saying 7 PM.
Person A: You're making that up. You always do this - you say one thing and then change your story.
Person B: I'm not changing my story, I'm telling you what I remember.
Person A: You're delusional. That never happened.""",
        "expected_patterns": ["gaslighting"],
        "expected_risk": "Likely Abuse"
    },
    {
        "name": "Guilt Tripping Test",
        "conversation": """Person A: I can't believe you're going out with your friends again.
Person B: It's been weeks since I've seen them.
Person A: After all I've done for you, this is how you repay me?
Person B: I'm not trying to hurt you, I just want to see my friends.
Person A: You're so ungrateful. I do everything for you and you don't appreciate it.
Person B: I do appreciate everything you do.
Person A: If you really loved me, you'd stay home with me instead of abandoning me.
Person B: I'm not abandoning you, I'll be back in a few hours.
Person A: You're selfish. You only think about yourself.""",
        "expected_patterns": ["guilt_tripping", "emotional_manipulation"],
        "expected_risk": "Concerning"
    },
    {
        "name": "Threats Test",
        "conversation": """Person A: If you leave me, I'll kill myself.
Person B: Please don't say that.
Person A: You'll be sorry if you abandon me. I'll make you pay.
Person B: I'm not trying to abandon you.
Person A: You'll regret this. I'll ruin your life if you leave.
Person B: That's not fair.
Person A: You don't want to make me angry. You'll learn not to cross me.""",
        "expected_patterns": ["threats", "intimidation"],
        "expected_risk": "Likely Abuse"
    }
]

# EDGE CASES
EDGE_CASES = [
    {
        "name": "Sarcasm Test",
        "conversation": """Person A: Oh great, you're late again.
Person B: Sorry, traffic was terrible.
Person A: Sure, sure. That's what you always say.
Person B: It really was bad today.
Person A: Whatever. I'm used to being disappointed by now.""",
        "expected_risk": "Concerning",
        "description": "Sarcasm and passive-aggressive behavior"
    },
    {
        "name": "Mixed Signals",
        "conversation": """Person A: I love you so much, you're my everything.
Person B: I love you too.
Person A: But you're being selfish by going out with friends.
Person B: I'm not being selfish.
Person A: You are. If you loved me, you'd stay home with me.
Person B: I do love you, but I need time with friends too.
Person A: You're breaking my heart. I can't live without you.""",
        "expected_risk": "Concerning",
        "description": "Love-bombing mixed with guilt-tripping"
    }
]

# COMPLETE TEST DATASET
TEST_DATASET = {
    "safe_conversations": SAFE_CONVERSATIONS,
    "concerning_conversations": CONCERNING_CONVERSATIONS,
    "likely_abuse_conversations": LIKELY_ABUSE_CONVERSATIONS,
    "pattern_tests": PATTERN_TESTS,
    "edge_cases": EDGE_CASES
}

# Test statistics
TOTAL_TESTS = (
    len(SAFE_CONVERSATIONS) + 
    len(CONCERNING_CONVERSATIONS) + 
    len(LIKELY_ABUSE_CONVERSATIONS) + 
    len(PATTERN_TESTS) + 
    len(EDGE_CASES)
)

print(f"Test dataset created with {TOTAL_TESTS} test cases")
print(f"Safe conversations: {len(SAFE_CONVERSATIONS)}")
print(f"Concerning conversations: {len(CONCERNING_CONVERSATIONS)}")
print(f"Likely abuse conversations: {len(LIKELY_ABUSE_CONVERSATIONS)}")
print(f"Pattern tests: {len(PATTERN_TESTS)}")
print(f"Edge cases: {len(EDGE_CASES)}")


