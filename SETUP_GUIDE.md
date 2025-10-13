# 🚀 SilentSignal - Complete Setup Guide

## 📦 What's Included

This is a complete AI-powered emotional abuse detection system with:
- ✅ Nemotron Prize-eligible architecture (MCP + RAG + Agentic workflow)
- ✅ WhatsApp integration (sends replies back to your phone!)
- ✅ Advanced pattern detection (12 categories, 240+ indicators)
- ✅ Streamlit web UI
- ✅ Privacy-first design (no data storage)
- ✅ Works even without NVIDIA NIM (robust fallback system)

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Extract the Project
```bash
unzip SilentSignal_Complete.zip
cd SilentSignal
```

### Step 2: Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
cp env_example.txt .env
```

### Step 3A: Run the Web UI (Optional)
```bash
# In Terminal 1
source .venv/bin/activate
streamlit run app.py
```
Open browser to `http://localhost:8501`

### Step 3B: Run WhatsApp Integration
```bash
# In Terminal 1
source .venv/bin/activate
uvicorn integrations.whatsapp_fastapi:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Set Up ngrok (for WhatsApp)
```bash
# In Terminal 2
# Install ngrok if needed: brew install ngrok
ngrok config add-authtoken YOUR_NGROK_AUTHTOKEN
ngrok http 8000
```
**Copy the https URL shown** (e.g., `https://a1b2-c3d4.ngrok.io`)

### Step 5: Configure Twilio Webhook
1. Go to [Twilio Console](https://console.twilio.com) → Messaging → WhatsApp → Sandbox
2. Set "When a message comes in": `https://YOUR-NGROK-URL/whatsapp/inbound`
3. Method: **POST**
4. Click **Save**
5. If not joined yet: From your phone, send the join code to the Twilio sandbox number

### Step 6: Test on WhatsApp! 📱
Send a message to your Twilio WhatsApp number:

**Try this:**
```
You never listen to me. If you really cared, you'd make time. You're being selfish.
```

**You should receive:**
```
⚠️ Risk Level: Concerning

🔍 Patterns Detected:
Guilt Tripping, Emotional Manipulation

🚩 Red Flags: 3 detected

💡 Suggestion:
Pay attention to how this conversation makes you feel

⚠️ Note: Monitor the situation carefully
```

---

## 🧪 Test Different Messages

### Safe Message
```
Thanks for understanding. Let's talk about it when you're free. Have a great day!
```
**Expected:** ✅ Risk Level: Safe

### Concerning Message
```
You never listen. If you loved me, you'd do this. You're being selfish again.
```
**Expected:** ⚠️ Risk Level: Concerning

### Abuse Message
```
You're crazy. That never happened. If you leave, I'll hurt myself. You owe me.
```
**Expected:** 🚨 Risk Level: Abuse (includes crisis hotline)

---

## 📁 Project Structure

```
SilentSignal/
├── app.py                          # Streamlit web UI
├── silent_signal_agent.py          # Core AI agent with fallback
├── pattern_detector.py             # Advanced pattern detection
├── backend/
│   ├── mcp_orchestrator.py         # Agentic workflow orchestration
│   ├── nimo_client.py              # NVIDIA NIM client
│   ├── analyzer.py                 # Fusion logic
│   └── resources.py                # Help resources
├── integrations/
│   └── whatsapp_fastapi.py         # WhatsApp webhook API
├── data/
│   ├── pattern_knowledge.json      # RAG knowledge base
│   └── resources.json              # Help resources
├── examples/
│   ├── safe.txt                    # Example conversations
│   ├── concerning.txt
│   └── abusive.txt
├── tests/
│   └── test_rules.py               # Unit tests
├── requirements.txt                # Python dependencies
├── Makefile                        # Convenience commands
└── README.md                       # Full documentation
```

---

## 🛠️ Makefile Commands

Instead of running commands manually, use:

```bash
make setup      # Install dependencies
make run-ui     # Start Streamlit UI
make run-api    # Start WhatsApp API
make test       # Run tests
make health     # Check API health
```

---

## 🔍 How It Works

### Agentic Workflow (MCP Orchestration)
1. **Preprocess**: Segment conversation into turns
2. **RAG Retrieval**: Load abuse pattern definitions from knowledge base
3. **Pattern Detection**: Run rule-based detection (12 categories, 240+ indicators)
4. **AI Reasoning**: Call Nemotron-3 via NVIDIA NIM for contextual analysis
5. **Fusion**: Combine rule-based + AI outputs for final risk assessment
6. **Fallback**: If NIM unavailable, use advanced pattern detector alone

### Pattern Categories (12 Types)
- Gaslighting (20+ patterns)
- Guilt-tripping (25+ patterns)
- Threats (30+ patterns)
- Intimidation (20+ patterns)
- Isolation (15+ patterns)
- Financial control (15+ patterns)
- Sexual coercion (20+ patterns)
- Monitoring (15+ patterns)
- Blame-shifting (25+ patterns)
- Love-bombing (15+ patterns)
- Passive-aggressive (25+ patterns)
- Sarcasm/contempt (15+ patterns)

### Risk Assessment
- **Safe**: < 15 points, no high-severity patterns
- **Concerning**: 35-59 points or moderate patterns
- **Likely Abuse**: 60+ points or multiple high-severity patterns

---

## 🔐 Privacy & Security

- ✅ **No data storage** - All analysis in-memory only
- ✅ **No logging of conversations** - Only metadata logged
- ✅ **Local processing** - Messages not sent to external servers (except NIM if enabled)
- ✅ **Panic button** - UI has disguise feature for safety
- ✅ **Disclaimer** - Not medical/legal advice

---

## ⚙️ Environment Variables (.env)

```bash
# NVIDIA NIM (optional - system works without it)
NIM_BASE_URL=http://localhost:8000/v1
NIM_API_KEY=your_api_key_here

# Twilio (for WhatsApp integration)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token

# Privacy
SILENTSIGNAL_ALLOW_PERSIST=0
```

**Note:** The system works perfectly without NVIDIA NIM configured - it uses the advanced pattern detection fallback.

---

## 🐛 Troubleshooting

### Port 8000 Already in Use
```bash
lsof -ti:8000 | xargs kill -9
```

### WhatsApp Not Receiving Replies
1. Check ngrok is running and URL is correct
2. Verify Twilio webhook URL includes `/whatsapp/inbound`
3. Check Terminal 1 logs for errors
4. Test locally: `python test_twiml_response.py`

### NIM Timeout Errors (Normal!)
```
ERROR: Request failed: Read timed out
```
This is **expected** if NVIDIA NIM isn't running. The system automatically uses fallback mode.

### Missing Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Python Version Issues
Requires Python 3.10+:
```bash
python3 --version
```

---

## 🧪 Testing

### Test Pattern Detection
```bash
python test_accuracy.py
```

### Test WhatsApp TwiML
```bash
python test_twiml_response.py
```

### Test Web UI
```bash
streamlit run app.py
# Open browser to http://localhost:8501
```

### Test with curl
```bash
curl -X POST http://localhost:8000/whatsapp/inbound \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890" \
  -d "Body=You never listen to me"
```

---

## 🏆 Nemotron Prize Eligibility

This project qualifies for the Nemotron Prize because:
- ✅ **Agentic Workflow**: MCP orchestration with multi-step reasoning
- ✅ **RAG Integration**: Retrieves abuse pattern definitions from knowledge base
- ✅ **Hybrid Reasoning**: Fuses rule-based + AI outputs
- ✅ **Measurable Impact**: Detects emotional abuse with explainable results
- ✅ **Advanced Capabilities**: Contextual reasoning, pattern fusion, fallback system

---

## 📚 Documentation

- `README.md` - Full project documentation
- `WHATSAPP_SETUP.md` - Detailed WhatsApp integration guide
- `WHATSAPP_FIX.md` - Fix documentation for form parsing
- `PROJECT_SUMMARY.md` - Feature summary
- `data/pattern_knowledge.json` - RAG knowledge base

---

## 🎯 Next Steps

1. **Test locally** - Run UI and try different messages
2. **Set up WhatsApp** - Follow steps 3B-6 above
3. **Demo preparation** - Use `examples/*.txt` for demos
4. **Customize** - Add more patterns, resources, or features
5. **Deploy** - Use ngrok for temporary deployment

---

## 💡 Tips for Hackathon Demo

1. **Show the live WhatsApp integration** - Send message from your phone
2. **Explain the agentic workflow** - MCP orchestration steps
3. **Highlight the hybrid approach** - Rule-based + AI fusion
4. **Emphasize privacy** - No data storage, in-memory processing
5. **Show different risk levels** - Use example messages
6. **Mention Nemotron Prize** - Agentic workflow + RAG compliance

---

## 🆘 Support

If you encounter issues:
1. Check the logs in Terminal 1 (API server)
2. Verify ngrok URL matches Twilio webhook
3. Test locally with `python test_twiml_response.py`
4. Check `.env` file exists (copy from `env_example.txt`)
5. Ensure Python 3.10+ and all dependencies installed

---

## 📄 License

This project is for educational and awareness purposes only. Not intended as medical, legal, or therapeutic advice.

---

## 🎉 Ready to Go!

Your SilentSignal installation is complete! 

**Start with:**
```bash
cd SilentSignal
source .venv/bin/activate
uvicorn integrations.whatsapp_fastapi:app --reload --host 0.0.0.0 --port 8000
```

Then set up ngrok and Twilio, and you're live! 🚀

