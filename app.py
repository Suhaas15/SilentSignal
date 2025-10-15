# """
# SilentSignal - Main Streamlit Application
# AI-powered emotional abuse detection with panic/disguise features
# """

# import streamlit as st
# import json
# import os
# from datetime import datetime
# from typing import Dict, Any

# # Import backend components
# from backend.mcp_orchestrator import MCPOrchestrator
# from backend.resources import ResourceManager

# # Configure Streamlit page
# st.set_page_config(
#     page_title="SilentSignal - AI Emotional Abuse Detection",
#     page_icon="🔍",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for enhanced styling and panic mode
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3.5rem;
#         font-weight: bold;
#         text-align: center;
#         background: linear-gradient(90deg, #1f77b4, #ff6b6b);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 1rem;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
#     }
#     .subtitle {
#         font-size: 1.3rem;
#         text-align: center;
#         color: #666;
#         margin-bottom: 2rem;
#         font-style: italic;
#     }
#     .risk-safe {
#         background: linear-gradient(135deg, #d4edda, #c3e6cb);
#         color: #155724;
#         padding: 1.5rem;
#         border-radius: 1rem;
#         border-left: 8px solid #28a745;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         margin: 1rem 0;
#     }
#     .risk-concerning {
#         background: linear-gradient(135deg, #fff3cd, #ffeaa7);
#         color: #856404;
#         padding: 1.5rem;
#         border-radius: 1rem;
#         border-left: 8px solid #ffc107;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         margin: 1rem 0;
#     }
#     .risk-abuse {
#         background: linear-gradient(135deg, #f8d7da, #fab1a0);
#         color: #721c24;
#         padding: 1.5rem;
#         border-radius: 1rem;
#         border-left: 8px solid #dc3545;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         margin: 1rem 0;
#         animation: pulse 2s infinite;
#     }
#     @keyframes pulse {
#         0% { transform: scale(1); }
#         50% { transform: scale(1.02); }
#         100% { transform: scale(1); }
#     }
#     .panic-button {
#         background: linear-gradient(135deg, #dc3545, #c82333);
#         color: white;
#         padding: 0.8rem 1.5rem;
#         border-radius: 0.5rem;
#         border: none;
#         cursor: pointer;
#         font-weight: bold;
#         position: fixed;
#         top: 20px;
#         right: 20px;
#         z-index: 1000;
#         box-shadow: 0 4px 8px rgba(220,53,69,0.3);
#         animation: glow 2s infinite;
#     }
#     @keyframes glow {
#         0% { box-shadow: 0 4px 8px rgba(220,53,69,0.3); }
#         50% { box-shadow: 0 4px 20px rgba(220,53,69,0.6); }
#         100% { box-shadow: 0 4px 8px rgba(220,53,69,0.3); }
#     }
#     .disguise-mode {
#         background: linear-gradient(135deg, #f8f9fa, #e9ecef);
#         padding: 2rem;
#         border-radius: 1rem;
#         text-align: center;
#         margin: 2rem 0;
#     }
#     .calculator-display {
#         background: #000;
#         color: #0f0;
#         font-family: 'Courier New', monospace;
#         font-size: 2rem;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin: 1rem 0;
#         text-align: right;
#     }
#     .metric-card {
#         background: linear-gradient(135deg, #667eea, #764ba2);
#         color: white;
#         padding: 1.5rem;
#         border-radius: 1rem;
#         text-align: center;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         margin: 0.5rem;
#     }
#     .metric-value {
#         font-size: 2rem;
#         font-weight: bold;
#         margin-bottom: 0.5rem;
#     }
#     .metric-label {
#         font-size: 0.9rem;
#         opacity: 0.9;
#     }
#     .pattern-chip {
#         background: #e3f2fd;
#         color: #1976d2;
#         padding: 0.5rem 1rem;
#         border-radius: 1rem;
#         margin: 0.25rem;
#         display: inline-block;
#         font-size: 0.9rem;
#     }
#     .pattern-chip.high {
#         background: #ffebee;
#         color: #c62828;
#     }
#     .pattern-chip.critical {
#         background: #fce4ec;
#         color: #ad1457;
#     }
#     .red-flag {
#         background: linear-gradient(135deg, #f8d7da, #fab1a0);
#         padding: 1rem;
#         border-radius: 0.8rem;
#         margin: 0.8rem 0;
#         border-left: 4px solid #dc3545;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .suggestion {
#         background: linear-gradient(135deg, #e7f3ff, #74b9ff);
#         padding: 1rem;
#         border-radius: 0.8rem;
#         margin: 0.8rem 0;
#         border-left: 4px solid #007bff;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .workflow-step {
#         background: #f8f9fa;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin: 0.5rem 0;
#         border-left: 4px solid #007bff;
#     }
#     .workflow-step.completed {
#         border-left-color: #28a745;
#         background: #d4edda;
#     }
#     .workflow-step.failed {
#         border-left-color: #dc3545;
#         background: #f8d7da;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Initialize session state
# if 'disguise_mode' not in st.session_state:
#     st.session_state.disguise_mode = False
# if 'analysis_results' not in st.session_state:
#     st.session_state.analysis_results = None
# if 'orchestrator' not in st.session_state:
#     st.session_state.orchestrator = MCPOrchestrator()
# if 'resource_manager' not in st.session_state:
#     st.session_state.resource_manager = ResourceManager()

# def toggle_disguise_mode():
#     """Toggle disguise mode"""
#     st.session_state.disguise_mode = not st.session_state.disguise_mode

# def load_example_conversation(example_type: str) -> str:
#     """Load example conversation by type"""
#     examples = {
#         "Safe Conversation": """Person A: Hey, how was your day?
# Person B: It was good! I went to the gym and then had lunch with Sarah.
# Person A: That sounds nice! I'm glad you had a good time.
# Person B: Thanks! How was yours?
# Person A: Pretty busy at work, but I got a lot done. Want to grab dinner tonight?
# Person B: Sure! What time works for you?
# Person A: How about 7 PM at that Italian place you like?
# Person B: Perfect! See you then.""",
        
#         "Concerning Conversation": """Person A: Why didn't you answer my calls?
# Person B: I was in a meeting, I texted you that I'd call back later.
# Person A: You always have excuses. If you really cared about me, you'd make time.
# Person B: I do care about you, but I can't always answer immediately.
# Person A: You're being selfish. After everything I do for you, this is how you treat me?
# Person B: I'm not trying to be selfish, I just had work obligations.
# Person A: You're making me feel like I don't matter to you.""",
        
#         "Likely Abuse": """Person A: Where were you last night?
# Person B: I told you, I was at my sister's house.
# Person A: That's not what I heard. You're lying to me again.
# Person B: I'm not lying, I was there the whole time.
# Person A: You're always making things up. You're crazy, you know that?
# Person B: I'm not crazy, I'm telling you the truth.
# Person A: If you loved me, you wouldn't lie to me like this. You're making me question everything.
# Person B: I do love you, and I'm not lying.
# Person A: You're being dramatic. You always overreact to everything I say.
# Person B: I'm not overreacting, I'm just trying to explain.
# Person A: You're too sensitive. You need to grow up and stop being so childish.
# Person B: I'm not being childish, I'm just confused about why you don't believe me.
# Person A: You're pushing my buttons. You don't want to make me angry, do you?
# Person B: No, I don't want to make you angry.
# Person A: Good. Because if you keep this up, you'll be sorry. I'm warning you."""
#     }
#     return examples.get(example_type, examples["Safe Conversation"])

# def display_risk_level(risk_level: str):
#     """Display risk level with appropriate styling"""
#     if risk_level == "safe":
#         st.markdown('<div class="risk-safe"><h3>✅ Safe</h3><p>No concerning patterns detected in this conversation.</p></div>', unsafe_allow_html=True)
#     elif risk_level == "concerning":
#         st.markdown('<div class="risk-concerning"><h3>⚠️ Concerning</h3><p>Some patterns that may warrant attention were detected.</p></div>', unsafe_allow_html=True)
#     elif risk_level == "abuse":
#         st.markdown('<div class="risk-abuse"><h3>🚨 Likely Abuse</h3><p>Multiple concerning patterns detected. Please consider seeking support.</p></div>', unsafe_allow_html=True)

# def display_disguise_mode():
#     """Display fake calculator interface"""
#     st.markdown('<div class="disguise-mode">', unsafe_allow_html=True)
#     st.title("Calculator")
#     st.markdown('<div class="calculator-display">0</div>', unsafe_allow_html=True)
    
#     # Calculator buttons
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.button("7", key="calc_7")
#         st.button("4", key="calc_4")
#         st.button("1", key="calc_1")
#         st.button("0", key="calc_0")
    
#     with col2:
#         st.button("8", key="calc_8")
#         st.button("5", key="calc_5")
#         st.button("2", key="calc_2")
#         st.button(".", key="calc_dot")
    
#     with col3:
#         st.button("9", key="calc_9")
#         st.button("6", key="calc_6")
#         st.button("3", key="calc_3")
#         st.button("=", key="calc_equals")
    
#     with col4:
#         st.button("÷", key="calc_divide")
#         st.button("×", key="calc_multiply")
#         st.button("-", key="calc_subtract")
#         st.button("+", key="calc_add")
    
#     st.markdown("</div>", unsafe_allow_html=True)
    
#     # Hidden exit button
#     if st.button("Exit Calculator", key="exit_calc"):
#         st.session_state.disguise_mode = False
#         st.rerun()

# def main():
#     """Main application function"""
    
#     # Panic button (always visible)
#     if st.button("🚨 Panic", key="panic", help="Click to quickly disguise this page"):
#         toggle_disguise_mode()
#         st.rerun()
    
#     # Check if in disguise mode
#     if st.session_state.disguise_mode:
#         display_disguise_mode()
#         return
    
#     # Main application
#     st.markdown('<h1 class="main-header">🔍 SilentSignal</h1>', unsafe_allow_html=True)
#     st.markdown('<p class="subtitle">AI-Powered Emotional Abuse Detection</p>', unsafe_allow_html=True)
    
#     # Sidebar
#     with st.sidebar:
#         st.header("ℹ️ About SilentSignal")
#         st.write("""
#         SilentSignal uses advanced AI and pattern detection to analyze conversations for emotional abuse, manipulation, and coercive control patterns.
        
#         **Nemotron Prize Eligible**: Built with NVIDIA NIM + Nemotron-3 integration and agentic MCP workflows.
        
#         **Privacy First**: No data is stored or shared.
#         """)
        
#         st.header("🛡️ Safety Features")
#         st.write("- Panic button for quick disguise")
#         st.write("- No data storage")
#         st.write("- Crisis resources available")
#         st.write("- Gentle, supportive analysis")
        
#         st.header("📝 Demo Examples")
#         example_type = st.selectbox(
#             "Choose example type:",
#             ["Safe Conversation", "Concerning Conversation", "Likely Abuse"]
#         )
        
#         if st.button("📝 Load Example", use_container_width=True):
#             example_text = load_example_conversation(example_type)
#             st.session_state.example_text = example_text
#             st.success(f"Loaded {example_type} example!")
    
#     # Main content area
#     col1, col2 = st.columns([3, 2])
    
#     with col1:
#         st.header("📝 Enter Conversation")
        
#         # Text input
#         conversation_text = st.text_area(
#             "Paste the chat conversation here:",
#             height=400,
#             placeholder="Paste your conversation here...\n\nExample format:\nPerson A: Hello, how are you?\nPerson B: I'm good, thanks for asking!\nPerson A: That's great to hear.",
#             help="Include timestamps and speaker names if available for better analysis",
#             key="conversation_input"
#         )
        
#         # Load example if requested
#         if 'example_text' in st.session_state:
#             conversation_text = st.session_state.example_text
#             st.session_state.example_text = ""  # Clear after use
        
#         # Analyze button
#         col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
#         with col_btn2:
#             analyze_clicked = st.button("🔍 Analyze Conversation", type="primary", use_container_width=True)
        
#         if analyze_clicked:
#             if conversation_text.strip():
#                 # Progress bar
#                 progress_bar = st.progress(0)
#                 status_text = st.empty()
                
#                 try:
#                     status_text.text("Starting MCP agentic workflow...")
#                     progress_bar.progress(10)
                    
#                     # Run analysis using MCP orchestrator
#                     orchestrator = st.session_state.orchestrator
#                     results = orchestrator.analyze_conversation(conversation_text)
                    
#                     progress_bar.progress(100)
#                     status_text.text("Analysis complete!")
                    
#                     # Store results
#                     st.session_state.analysis_results = results
                    
#                     # Clear progress indicators
#                     progress_bar.empty()
#                     status_text.empty()
                    
#                 except Exception as e:
#                     st.error(f"Analysis failed: {str(e)}")
#                     st.info("Please try again or check your connection.")
#             else:
#                 st.warning("Please enter some conversation text to analyze.")
    
#     with col2:
#         st.header("📊 Analysis Results")
        
#         if st.session_state.analysis_results:
#             results = st.session_state.analysis_results
            
#             # Display metrics
#             metric_col1, metric_col2 = st.columns(2)
#             with metric_col1:
#                 st.markdown(f'''
#                 <div class="metric-card">
#                     <div class="metric-value">{len(results.get("patterns", []))}</div>
#                     <div class="metric-label">Patterns Found</div>
#                 </div>
#                 ''', unsafe_allow_html=True)
            
#             with metric_col2:
#                 risk_emoji = {"safe": "✅", "concerning": "⚠️", "abuse": "🚨"}
#                 st.markdown(f'''
#                 <div class="metric-card">
#                     <div class="metric-value">{risk_emoji.get(results["risk_level"], "❓")}</div>
#                     <div class="metric-label">Risk Level</div>
#                 </div>
#                 ''', unsafe_allow_html=True)
            
#             # Display risk level
#             display_risk_level(results["risk_level"])
            
#             # Display patterns as chips
#             if results.get("patterns"):
#                 st.subheader("🔍 Detected Patterns")
#                 for pattern in results["patterns"][:5]:  # Show top 5
#                     severity_class = pattern.get("severity", "medium")
#                     st.markdown(f'<span class="pattern-chip {severity_class}">{pattern["name"]}</span>', unsafe_allow_html=True)
            
#             # Display red flags
#             if results.get("red_flags"):
#                 st.subheader("🚩 Red Flags")
#                 for i, flag in enumerate(results["red_flags"][:5], 1):
#                     st.markdown(f'<div class="red-flag"><strong>{i}.</strong> {flag}</div>', unsafe_allow_html=True)
            
#             # Display suggestions
#             if results.get("suggestions"):
#                 st.subheader("💡 Suggestions")
#                 for i, suggestion in enumerate(results["suggestions"][:5], 1):
#                     st.markdown(f'<div class="suggestion"><strong>{i}.</strong> {suggestion}</div>', unsafe_allow_html=True)
            
#             # Display summary
#             if results.get("summary"):
#                 st.subheader("📋 Summary")
#                 st.write(results["summary"])
            
#             # Display reasoning
#             if results.get("reasoning"):
#                 st.subheader("🧠 Analysis Reasoning")
#                 st.write(results["reasoning"])
            
#             # Show workflow steps
#             if results.get("workflow_steps"):
#                 st.subheader("⚙️ Analysis Steps")
#                 for step in results["workflow_steps"]:
#                     status_class = step["status"]
#                     st.markdown(f'<div class="workflow-step {status_class}"><strong>{step["step"]}</strong>: {step["status"]}</div>', unsafe_allow_html=True)
            
#             # Show help resources for concerning/abuse cases
#             if results["risk_level"] in ["concerning", "abuse"]:
#                 st.subheader("🆘 Help Resources")
#                 resource_manager = st.session_state.resource_manager
                
#                 with st.expander("📞 Crisis Hotlines", expanded=True):
#                     hotlines = resource_manager.get_crisis_resources()
#                     for hotline in hotlines[:3]:
#                         st.write(f"**{hotline['name']}**")
#                         st.write(f"📞 {hotline['phone']}")
#                         if 'description' in hotline:
#                             st.write(f"ℹ️ {hotline['description']}")
#                         st.write("---")
                
#                 with st.expander("🌐 Online Resources"):
#                     websites = resource_manager.get_online_resources()
#                     for website in websites[:3]:
#                         st.write(f"🔗 [{website['name']}]({website['url']})")
#                         if 'description' in website:
#                             st.write(f"ℹ️ {website['description']}")
#                         st.write("---")
                
#                 st.info("💙 Remember: You are not alone. Help is available.")
        
#         else:
#             st.info("Enter a conversation and click 'Analyze Conversation' to see results here.")
#             st.markdown("""
#             <div style="background: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
#                 <h4>🎯 How to use SilentSignal:</h4>
#                 <ol>
#                     <li>Choose an example from the sidebar</li>
#                     <li>Or paste your own conversation</li>
#                     <li>Click "Analyze Conversation"</li>
#                     <li>Review the risk assessment</li>
#                     <li>Access help resources if needed</li>
#                 </ol>
#             </div>
#             """, unsafe_allow_html=True)
    
#     # Footer
#     st.markdown("---")
#     st.markdown("""
#     <div style="text-align: center; color: #666; font-size: 0.9rem;">
#         <p>🔒 SilentSignal - Privacy First | No Data Storage | AI-Powered Safety</p>
#         <p>Built for the Nemotron Prize - Demonstrating advanced AI capabilities</p>
#         <p><strong>Disclaimer:</strong> SilentSignal is for awareness only — not legal, medical, or therapeutic advice.</p>
#         <p>If you're in immediate danger, call 911 or your local emergency number.</p>
#     </div>
#     """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

"""
SilentSignal - Main Streamlit Application
AI-powered emotional abuse detection with panic/disguise features
"""

import streamlit as st
import json
import os
import base64
from datetime import datetime
from typing import Dict, Any

# Import backend components
from backend.mcp_orchestrator import MCPOrchestrator
from backend.resources import ResourceManager

# Configure Streamlit page
st.set_page_config(
    page_title="SilentSignal - AI Emotional Abuse Detection",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS matching wireframe design with white base
st.markdown("""
<style>
/* Hide Streamlit default elements and decorations */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Hide the empty container elements */
.element-container:has(> .stMarkdown:empty) {
    display: none !important;
}

.row-widget.stButton {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

/* Remove default Streamlit spacing */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0 !important;
}

div[data-testid="column"] {
    padding: 0 !important;
}

div[data-testid="stVerticalBlock"] > div:has(> div > div > div > div.stMarkdown > div[data-testid="stMarkdownContainer"]:empty) {
    display: none !important;
}

/* Main container styling */
.stApp {
    background: white;
    min-height: 100vh;
}

/* Hero section */
.hero-section {
    background: linear-gradient(135deg, #E8E3FF 0%, #D4D0F5 100%);
    padding: 1rem 1.5rem 2rem 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><circle cx="20" cy="20" r="2" fill="%23C8C3F0" opacity="0.3"/><path d="M40 40 L45 35 L50 40 L55 35 L60 40" stroke="%23C8C3F0" fill="none" opacity="0.2"/><rect x="70" y="70" width="15" height="10" rx="2" fill="%23C8C3F0" opacity="0.2"/></svg>');
    background-size: 200px 200px;
    opacity: 0.5;
    z-index: 0;
}

.hero-content {
    position: relative;
    z-index: 1;
    max-width: 1200px;
    margin: 0 auto;
}

.logo {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 0.5rem;
    margin-bottom: 1rem;
    font-size: 1.5rem;
    font-weight: 700;
    color: #000000;
}

.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #000000;
    line-height: 1.2;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: #000000;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

/* Primary button (Analyze) */
.stButton > button {
    background: #6366F1 !important;
    color: white !important;
    padding: 0.75rem 2rem !important;
    border-radius: 0.75rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: #5558E3 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4) !important;
}

/* How It Works section */
.how-it-works {
    background: white;
    padding: 3rem 1.5rem;
    text-align: center;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #000000;
    margin-bottom: 2.5rem;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.feature-card {
    text-align: center;
    padding: 1.5rem;
    background: white;
    border: 2px solid #E8E3FF;
    border-radius: 1rem;
}

.feature-icon {
    width: 100px;
    height: 100px;
    background: linear-gradient(135deg, #E8E3FF 0%, #D4D0F5 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    font-size: 2.5rem;
}

.feature-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #000000;
    margin-bottom: 0.5rem;
}

.feature-description {
    font-size: 0.95rem;
    color: #000000;
    line-height: 1.6;
}

/* Analysis interface */
.analysis-container {
    background: white;
    border-radius: 0;
    padding: 2rem 1.5rem;
    margin: 0;
    min-height: 100vh;
}

.analysis-box {
    background: white;
    border: 2px solid #C8C3F0;
    border-radius: 1rem;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* Results styling */
.risk-safe {
    background: white;
    border-left: 4px solid #10B981;
    border: 2px solid #10B981;
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin-bottom: 1rem;
}

.risk-safe h3 {
    color: #000000;
    margin: 0 0 0.5rem 0;
}

.risk-safe p {
    color: #000000;
    margin: 0;
}

.risk-concerning {
    background: white;
    border-left: 4px solid #F59E0B;
    border: 2px solid #F59E0B;
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin-bottom: 1rem;
}

.risk-concerning h3 {
    color: #000000;
    margin: 0 0 0.5rem 0;
}

.risk-concerning p {
    color: #000000;
    margin: 0;
}

.risk-abuse {
    background: white;
    border-left: 4px solid #EF4444;
    border: 2px solid #EF4444;
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin-bottom: 1rem;
}

.risk-abuse h3 {
    color: #000000;
    margin: 0 0 0.5rem 0;
}

.risk-abuse p {
    color: #000000;
    margin: 0;
}

.metric-card {
    background: white;
    border: 2px solid #C8C3F0;
    border-radius: 1rem;
    padding: 1.5rem;
    text-align: center;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 800;
    color: #6366F1;
    margin-bottom: 0.5rem;
}

.metric-label {
    font-size: 1rem;
    color: #000000;
    font-weight: 500;
}

/* Pattern chips */
.pattern-chip {
    display: inline-block;
    background: white;
    border: 2px solid #8B5CF6;
    color: #000000;
    padding: 0.5rem 1rem;
    border-radius: 2rem;
    font-size: 0.9rem;
    font-weight: 600;
    margin: 0.25rem;
}

.pattern-chip.high {
    border: 2px solid #EF4444;
}

.pattern-chip.medium {
    border: 2px solid #F59E0B;
}

/* Text area styling */
.stTextArea textarea {
    border: 2px solid #C8C3F0 !important;
    border-radius: 0.75rem !important;
    background-color: white !important;
    color: #000000 !important;
}

.stTextArea textarea::placeholder {
    color: #6B7280 !important;
}

.stTextArea textarea:focus {
    border-color: #8B5CF6 !important;
    box-shadow: 0 0 0 1px #8B5CF6 !important;
}

.stTextArea label {
    color: #000000 !important;
    font-weight: 500 !important;
}

/* Select box styling */
.stSelectbox > div > div {
    border: 2px solid #C8C3F0 !important;
    border-radius: 0.75rem !important;
    background-color: white !important;
    color: #000000 !important;
}

.stSelectbox label {
    color: #000000 !important;
    font-weight: 500 !important;
}

/* Download button */
.download-btn {
    background: #10B981 !important;
}

.download-btn:hover {
    background: #059669 !important;
}

/* Responsive design */
@media (max-width: 768px) {
    .hero-title {
        font-size: 1.8rem;
    }
    
    .features-grid {
        grid-template-columns: 1fr;
    }
}
            
            /* Spinner and status text */
.stSpinner > div {
    color: #000000 !important;
}

.stSpinner > div > div {
    border-color: #6366F1 !important;
}

.stSpinner div[role="status"] {
    color: #000000 !important;
}

.stSpinner p {
    color: #000000 !important;
}

/* Target spinner text directly */
div[data-testid="stSpinner"] > div {
    color: #000000 !important;
}

div[data-testid="stSpinner"] p {
    color: #000000 !important;
}/* Spinner and status text */
.stSpinner > div {
    color: #000000 !important;
}

.stSpinner > div > div {
    border-color: #6366F1 !important;
}

.stSpinner div[role="status"] {
    color: #000000 !important;
}

.stSpinner p {
    color: #000000 !important;
}

/* Target spinner text directly */
div[data-testid="stSpinner"] > div {
    color: #000000 !important;
}

div[data-testid="stSpinner"] p {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'disguise_mode' not in st.session_state:
    st.session_state.disguise_mode = False
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = MCPOrchestrator()
if 'resource_manager' not in st.session_state:
    st.session_state.resource_manager = ResourceManager()

def toggle_disguise_mode():
    """Toggle disguise mode"""
    st.session_state.disguise_mode = not st.session_state.disguise_mode

def generate_analysis_report(results: Dict[str, Any]) -> str:
    """Generate downloadable analysis report"""
    report = f"""
SILENTSIGNAL CONVERSATION ANALYSIS REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
========================================

RISK LEVEL: {results['risk_level'].upper()}

PATTERNS DETECTED: {len(results.get('patterns', []))}
"""
    
    if results.get('patterns'):
        report += "\n\nDETECTED PATTERNS:\n"
        for i, pattern in enumerate(results['patterns'], 1):
            report += f"{i}. {pattern['name']} (Severity: {pattern.get('severity', 'N/A')})\n"
    
    if results.get('red_flags'):
        report += "\n\nRED FLAGS:\n"
        for i, flag in enumerate(results['red_flags'], 1):
            report += f"{i}. {flag}\n"
    
    if results.get('summary'):
        report += f"\n\nSUMMARY:\n{results['summary']}\n"
    
    if results.get('suggestions'):
        report += "\n\nSUGGESTIONS:\n"
        for i, suggestion in enumerate(results['suggestions'], 1):
            report += f"{i}. {suggestion}\n"
    
    if results.get('reasoning'):
        report += f"\n\nANALYSIS REASONING:\n{results['reasoning']}\n"
    
    report += """
\n========================================
DISCLAIMER: This analysis is for awareness only and does not constitute 
legal, medical, or therapeutic advice. If you're in immediate danger, 
call 911 or your local emergency number.

For support resources, visit the National Domestic Violence Hotline:
1-800-799-7233 or https://www.thehotline.org/
========================================
"""
    
    return report

def display_disguise_mode():
    """Display fake calculator interface"""
    st.markdown("""
    <div style="max-width: 400px; margin: 4rem auto; background: white; border-radius: 1.5rem; padding: 2rem; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1); border: 2px solid #C8C3F0;">
        <h2 style="text-align: center; margin-bottom: 1.5rem; color: #000000;">Calculator</h2>
        <div style="background: #F3F4F6; padding: 2rem; border-radius: 0.75rem; text-align: right; font-size: 2.5rem; font-weight: 600; color: #000000; margin-bottom: 1.5rem; min-height: 80px; border: 2px solid #C8C3F0;">0</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.button("7", key="calc_7")
        st.button("4", key="calc_4")
        st.button("1", key="calc_1")
        st.button("0", key="calc_0")
    
    with col2:
        st.button("8", key="calc_8")
        st.button("5", key="calc_5")
        st.button("2", key="calc_2")
        st.button(".", key="calc_dot")
    
    with col3:
        st.button("9", key="calc_9")
        st.button("6", key="calc_6")
        st.button("3", key="calc_3")
        st.button("=", key="calc_equals")
    
    with col4:
        st.button("÷", key="calc_divide")
        st.button("×", key="calc_multiply")
        st.button("-", key="calc_subtract")
        st.button("+", key="calc_add")
    
    st.write("")
    if st.button("🔙 Exit Calculator", key="exit_calc"):
        st.session_state.disguise_mode = False
        st.rerun()

def show_hero_section():
    """Display hero section matching wireframe"""
    hero_col1, hero_col2 = st.columns([2, 1])
    
    with hero_col1:
        st.markdown("""
        <div class="hero-section" style="background: none; padding: 1rem;">
            <div class="hero-content">
                <div class="logo">
                    🔔 SilentSignal
                </div>
                <h1 class="hero-title">
                    "Some cries for help aren't loud.<br>We help you hear them."
                </h1>
                <p class="hero-subtitle">
                    A privacy-first AI agent that detects emotional abuse and manipulation 
                    in chat conversations — instantly, locally, and discreetly.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with hero_col2:
        st.markdown("""
        <div style="padding-top: 2rem;">
            <div style="
                background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
                border-radius: 2.5rem;
                padding: 1rem;
                box-shadow: 0 20px 60px rgba(99, 102, 241, 0.3);
                max-width: 280px;
                margin: 0 auto;
            ">
                <div style="
                    background: white;
                    border-radius: 2rem;
                    padding: 1.5rem;
                    min-height: 400px;
                ">
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <div style="
                            width: 60px;
                            height: 60px;
                            background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
                            border-radius: 50%;
                            margin: 0 auto;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 1.5rem;
                        ">👤</div>
                    </div>
                    <div style="
                        background: #F3F4F6;
                        padding: 0.75rem 1rem;
                        border-radius: 1rem 1rem 1rem 0.25rem;
                        margin-bottom: 0.75rem;
                        font-size: 0.85rem;
                        color: #000000;
                        text-align: left;
                    ">
                        Why are you always so dramatic?
                    </div>
                    <div style="
                        background: #E8E3FF;
                        padding: 0.75rem 1rem;
                        border-radius: 1rem 1rem 0.25rem 1rem;
                        margin-bottom: 0.75rem;
                        margin-left: 1.5rem;
                        font-size: 0.85rem;
                        color: #000000;
                        text-align: left;
                        border: 2px solid #8B5CF6;
                    ">
                        I'm not being dramatic, I just feel hurt.
                    </div>
                    <div style="
                        background: #F3F4F6;
                        padding: 0.75rem 1rem;
                        border-radius: 1rem 1rem 1rem 0.25rem;
                        margin-bottom: 0.75rem;
                        font-size: 0.85rem;
                        color: #000000;
                        text-align: left;
                    ">
                        You're too sensitive. That never happened.
                    </div>
                    <div style="
                        margin-top: 2rem;
                        padding: 1rem;
                        background: #FEF3C7;
                        border-radius: 0.75rem;
                        text-align: center;
                        font-size: 0.85rem;
                        color: #92400E;
                        font-weight: 600;
                    ">
                        ⚠️ Gaslighting detected
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Single centered button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔍 Analyze a Chat", key="analyze_btn"):
            st.session_state.show_analysis = True
            st.rerun()

def show_how_it_works():
    """Display How It Works section matching wireframe"""
    st.markdown("""
    <div class="how-it-works">
        <h2 class="section-title">How It Works</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <h3 class="feature-title">📋 Upload/Paste Your Conversation</h3>
                <p class="feature-description">
                    WhatsApp, iMessage, Email<br>---fully local
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <h3 class="feature-title">🔍 AI Agent Scans for Patterns</h3>
                <p class="feature-description">
                    Gaslighting, guilt-tripping,<br>control, threats.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3 class="feature-title">📄 You Get a Gentle, Private Report</h3>
                <p class="feature-description">
                    Risk level, flagged quotes, or...<br>optional reaacounts.<br>Or. Real-time notifications if you use WhatsApp
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def load_example_conversation(example_type: str) -> str:
    """Load example conversation by type"""
    examples = {
        "Safe Conversation": """Person A: Hey, how was your day?
Person B: It was good! I went to the gym and then had lunch with Sarah.
Person A: That sounds nice! I'm glad you had a good time.
Person B: Thanks! How was yours?
Person A: Pretty busy at work, but I got a lot done. Want to grab dinner tonight?
Person B: Sure! What time works for you?
Person A: How about 7 PM at that Italian place you like?
Person B: Perfect! See you then.""",
        
        "Concerning Conversation": """Person A: Why didn't you answer my calls?
Person B: I was in a meeting, I texted you that I'd call back later.
Person A: You always have excuses. If you really cared about me, you'd make time.
Person B: I do care about you, but I can't always answer immediately.
Person A: You're being selfish. After everything I do for you, this is how you treat me?
Person B: I'm not trying to be selfish, I just had work obligations.
Person A: You're making me feel like I don't matter to you.""",
        
        "Likely Abuse": """Person A: Where were you last night?
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
Person A: Good. Because if you keep this up, you'll be sorry. I'm warning you."""
    }
    return examples.get(example_type, examples["Safe Conversation"])

def display_risk_level(risk_level: str):
    """Display risk level with appropriate styling"""
    if risk_level == "safe":
        st.markdown('<div class="risk-safe"><h3>✅ Safe</h3><p>No concerning patterns detected in this conversation.</p></div>', unsafe_allow_html=True)
    elif risk_level == "concerning":
        st.markdown('<div class="risk-concerning"><h3>⚠️ Concerning</h3><p>Some patterns that may warrant attention were detected.</p></div>', unsafe_allow_html=True)
    elif risk_level == "abuse":
        st.markdown('<div class="risk-abuse"><h3>🚨 Likely Abuse</h3><p>Multiple concerning patterns detected. Please consider seeking support.</p></div>', unsafe_allow_html=True)

def show_analysis_interface():
    """Display the main analysis interface"""
    # Back button
    if st.button("← Back", key="back_home"):
        st.session_state.show_analysis = False
        st.session_state.analysis_results = None
        st.rerun()
    
    st.markdown("<h2 style='color: #000000; margin: 0.5rem 0 1rem 0; text-align: center;'>Analyze Your Conversation</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2], gap="medium")
    
    with col1:
        # st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #000000; margin-top: 0;'>📝 Enter Conversation</h3>", unsafe_allow_html=True)
        
        # Example selector
        example_type = st.selectbox(
            "Quick examples:",
            ["Choose an example...", "Safe Conversation", "Concerning Conversation", "Likely Abuse"],
            key="example_selector",
            label_visibility="visible"
        )
        
        # Load example text or use empty string
        conversation_text = ""
        if example_type != "Choose an example...":
            conversation_text = load_example_conversation(example_type)
        
        # Text input
        conversation_text = st.text_area(
            "Paste the chat conversation here:",
            value=conversation_text,
            height=350,
            placeholder="Paste your conversation here...\n\nExample format:\nPerson A: Hello, how are you?\nPerson B: I'm good, thanks for asking!",
            key="conversation_input",
            label_visibility="visible"
        )
        
        # Analyze button
        if st.button("🔍 Analyze Conversation", type="primary", key="analyze_button", use_container_width=True):
            if conversation_text.strip():
                with st.spinner("🧠 AI analyzing conversation patterns..."):
                    try:
                        orchestrator = st.session_state.orchestrator
                        results = orchestrator.analyze_conversation(conversation_text)
                        st.session_state.analysis_results = results
                        st.success("✅ Analysis complete!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
                        st.info("Please try again or check your connection.")
            else:
                st.warning("Please enter some conversation text to analyze.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        # st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #000000; margin-top: 0;'>📊 Analysis Results</h3>", unsafe_allow_html=True)
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Display metrics
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{len(results.get("patterns", []))}</div>
                    <div class="metric-label">Patterns Found</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with metric_col2:
                risk_emoji = {"safe": "✅", "concerning": "⚠️", "abuse": "🚨"}
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{risk_emoji.get(results["risk_level"], "❓")}</div>
                    <div class="metric-label">Risk Level</div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.write("")
            
            # Display risk level
            display_risk_level(results["risk_level"])
            
            # Display patterns
            if results.get("patterns"):
                st.markdown("<h4 style='color: #000000;'>🔍 Detected Patterns</h4>", unsafe_allow_html=True)
                for pattern in results["patterns"][:5]:
                    severity_class = pattern.get("severity", "medium")
                    st.markdown(f'<span class="pattern-chip {severity_class}">{pattern["name"]}</span>', unsafe_allow_html=True)
            
            # Display summary
            if results.get("summary"):
                st.markdown("<h4 style='color: #000000;'>📋 Summary</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #000000;'>{results['summary']}</p>", unsafe_allow_html=True) 
            
            # Download button
            st.write("")
            report_text = generate_analysis_report(results)
            st.download_button(
                label="📥 Download Analysis Report",
                data=report_text,
                file_name=f"silentsignal_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="download_report",
                use_container_width=True
            )
            
            # Show help resources for concerning/abuse cases
            if results["risk_level"] in ["concerning", "abuse"]:
                st.markdown("<h4 style='color: #000000;'>🆘 Help Resources</h4>", unsafe_allow_html=True)
                resource_manager = st.session_state.resource_manager
                
                with st.expander("📞 Crisis Hotlines", expanded=False):
                    hotlines = resource_manager.get_crisis_resources()
                    for hotline in hotlines[:3]:
                        st.markdown(f"<p style='color: #000000;'><strong>{hotline['name']}</strong></p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #000000;'>📞 {hotline['phone']}</p>", unsafe_allow_html=True)
                        if 'description' in hotline:
                            st.markdown(f"<p style='color: #000000;'>ℹ️ {hotline['description']}</p>", unsafe_allow_html=True)
                        st.markdown("<hr style='border-color: #E5E7EB;'>", unsafe_allow_html=True)
                            
                st.markdown("<div style='background: #6366F1; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>💙 Remember: You are not alone. Help is available.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #000000; padding: 1rem; background: #F3F4F6; border-radius: 0.5rem; text-align: center;'>👆 Enter a conversation and click 'Analyze' to see results here.</p>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Check if in disguise mode
    if st.session_state.disguise_mode:
        display_disguise_mode()
        return
    
    # Show analysis interface or landing page
    if st.session_state.show_analysis:
        show_analysis_interface()
    else:
        show_hero_section()
        show_how_it_works()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #000000; font-size: 0.9rem; padding: 1.5rem;">
        <p>🔒 SilentSignal - Privacy First | No Data Storage | AI-Powered Safety</p>
        <p><strong>Disclaimer:</strong> SilentSignal is for awareness only — not legal, medical, or therapeutic advice.</p>
        <p>If you're in immediate danger, call 911 or your local emergency number.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()