# SilentSignal - Nemotron Prize Eligible AI Project

## 🏆 Nemotron Prize Compliance

**SilentSignal** is built specifically for the Nemotron Prize with advanced agentic workflows:

- **Nemotron-3 via NVIDIA NIM**: Real AI integration for contextual reasoning
- **MCP Orchestration**: Multi-step agentic workflow with RAG
- **Hybrid Intelligence**: Rule-based + AI reasoning fusion
- **Explainable AI**: Structured outputs with reasoning chains
- **Measurable Impact**: Emotional abuse detection with crisis intervention

## 🧠 Core Innovation

SilentSignal uses a **hybrid RAG workflow** that:
1. **Retrieves** abuse pattern definitions from local knowledge base
2. **Enriches** Nemotron-3 context with psychological definitions
3. **Fuses** rule-based pattern detection with AI reasoning
4. **Generates** explainable risk assessments with structured outputs

## 🚀 Quick Start

```bash
# Setup environment
make setup

# Install dependencies (includes python-multipart for WhatsApp)
pip install -r requirements.txt

# Run Streamlit UI
make run-ui

# Run WhatsApp API
make run-api

# Test WhatsApp form parsing
python test_whatsapp_form.py

# Run tests
make test
```

**Important**:
- The `python-multipart` library is required for WhatsApp integration to parse Twilio's form-encoded webhook data.
- To use NVIDIA hosted Nemotron-3, set `NIM_BASE_URL=https://integrate.api.nvidia.com/v1` and put your API key from `https://build.nvidia.com/settings/api-keys` into `NIM_API_KEY`. Optionally set `NIM_MODEL` (default `nvidia/nemotron-3-8b-instruct`).
 - To use the OpenAI SDK against NVIDIA Integrate (and enable reasoning models), set `NIM_USE_OPENAI_SDK=1` and ensure `openai` is installed (already in `requirements.txt`). You can control thinking tokens with `NIM_REASONING_MIN` and `NIM_REASONING_MAX`.

## 📱 Live Demo

**Streamlit UI**: https://silent-signal-frontend.onrender.com/

## 🛡️ Privacy & Safety

- **Zero Data Storage**: All processing in-memory only
- **Panic Button**: Disguise mode with fake calculator view
- **Crisis Resources**: Integrated help hotlines and support
- **Local Processing**: No external data transmission

## 🏗️ Architecture

```
SilentSignal/
├── app.py                    # Streamlit UI
├── backend/                  # Core AI engine
│   ├── mcp_orchestrator.py   # Agentic workflow
│   ├── nimo_client.py        # Nemotron-3 NIM client
│   ├── prompts.py            # Structured prompts
│   ├── pattern_detector.py   # Rule-based detection
│   ├── analyzer.py           # Fusion logic
│   ├── resources.py          # Help resources
│   └── report_builder.py     # PDF export
├── integrations/             # External APIs
│   └── whatsapp_fastapi.py   # WhatsApp webhook
├── data/                     # Knowledge base
│   ├── resources.json        # Crisis resources
│   └── pattern_knowledge.json # RAG knowledge base
├── examples/                 # Test conversations
└── tests/                    # Test suite
```

## 🧩 Nemotron Integration

**Nemotron-3** is used for:
- Contextual reasoning about emotional dynamics
- Intent detection and manipulation patterns
- Structured JSON output generation
- Explainable risk assessment reasoning

**MCP Workflow**:
1. Text preprocessing and segmentation
2. RAG retrieval of abuse pattern definitions
3. Nemotron-3 context enrichment
4. Rule-based pattern matching
5. Hybrid fusion and scoring
6. Structured report generation

## 📊 Example Output

```json
{
  "risk_level": "concerning",
  "patterns": ["gaslighting", "guilt_tripping"],
  "summary": "Detected manipulation tactics including reality denial and emotional coercion",
  "red_flags": ["You're imagining things", "If you loved me"],
  "suggestions": ["Trust your instincts", "Consider professional support"],
  "reasoning": "Hybrid analysis combining pattern detection with AI reasoning"
}
```

## 🔧 Environment Setup

Copy `.env.example` to `.env` and configure:
- `NIM_BASE_URL`: Your NVIDIA NIM endpoint (default hosted: `https://integrate.api.nvidia.com/v1`)
- `NIM_API_KEY`: Your API key from NVIDIA Build (`https://build.nvidia.com/settings/api-keys`)
- `NIM_MODEL`: Optional model (e.g., `nvidia/nvidia-nemotron-nano-9b-v2` for reasoning)
- `NIM_USE_OPENAI_SDK`: Set to `1` to use OpenAI SDK path
- `NIM_REASONING_MIN`/`NIM_REASONING_MAX`: Optional thinking token bounds for reasoning models
- `TWILIO_*`: For WhatsApp integration

### Email Alerts (optional)
- To email on abuse risk via Gmail SMTP, set in `.env`:
  - `EMAIL_ALERTS=1`
  - `EMAIL_METHOD=gmail`
  - `SMTP_HOST=smtp.gmail.com`
  - `SMTP_PORT=587`
  - `SMTP_USER=your_gmail_address`
  - `SMTP_PASS=your_gmail_app_password`
  - `EMAIL_FROM=your_gmail_address`
  - `EMAIL_TO=comma,separated,recipients`
  - `ALERT_MIN_INTERVAL_SECONDS=60` (rate limit per sender)

Gmail setup: enable 2FA on your account, create an “App Password” for Mail, and paste it into `SMTP_PASS`.

## 📱 WhatsApp Integration

Twilio webhook endpoint: `/whatsapp/inbound`
- Receives message payloads
- Runs SilentSignal analysis
- Returns concise risk summary
- Supports ngrok for local testing

## 🧪 Testing

Comprehensive test suite covering:
- Rule-based pattern detection
- Nemotron integration
- MCP workflow orchestration
- Fusion logic accuracy
- Edge cases and safety

## 🚀 Future Enhancements

- Multilingual support
- Chrome extension for real-time analysis
- Therapist-assist dashboard
- Mobile app with offline capabilities
- Advanced RAG with vector embeddings

---

**Built for the Nemotron Prize** - Demonstrating advanced AI capabilities in emotional abuse detection with measurable social impact.
