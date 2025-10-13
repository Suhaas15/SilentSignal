"""
WhatsApp FastAPI Integration
Handles incoming WhatsApp messages via Twilio webhook
"""

from fastapi import FastAPI, Request, HTTPException, Form, BackgroundTasks
from fastapi.responses import JSONResponse, PlainTextResponse
import json
import os
from typing import Dict, Any, Optional
import logging
from dotenv import load_dotenv
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
import time

from backend.mcp_orchestrator import MCPOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="SilentSignal WhatsApp API",
    description="AI-powered emotional abuse detection for WhatsApp messages",
    version="1.0.0"
)

# Initialize orchestrator
orchestrator = MCPOrchestrator()

# Safe startup diagnostics (no secrets)
logger.info(
    "NIM configured: base_url=%s, model=%s, api_key_present=%s",
    os.getenv("NIM_BASE_URL", ""),
    os.getenv("NIM_MODEL", ""),
    bool(os.getenv("NIM_API_KEY"))
)

# In-memory rate-limit state for alerts: last send timestamp per sender
_LAST_ALERT_TS_BY_SENDER: Dict[str, float] = {}
_ALERT_MIN_INTERVAL_SECONDS = int(os.getenv("ALERT_MIN_INTERVAL_SECONDS", "60"))

def _sanitize_snippet(text: str, max_len: int = 300) -> str:
    snippet = (text or "").replace("\r", " ").replace("\n", " ")
    return snippet[:max_len].strip()

def _should_send_email_alert(risk_level: str) -> bool:
    if not os.getenv("EMAIL_ALERTS", "0") in ("1", "true", "True"):
        return False
    rl = (risk_level or "").lower()
    return "abuse" in rl  # matches "abuse" or "likely abuse"

def _queue_email_alert(background_tasks: BackgroundTasks, sender_whatsapp: str, body_text: str, analysis_results: Dict[str, Any], message_sid: Optional[str]):
    # Rate limit per sender
    now = time.time()
    last_ts = _LAST_ALERT_TS_BY_SENDER.get(sender_whatsapp, 0)
    if now - last_ts < _ALERT_MIN_INTERVAL_SECONDS:
        logger.info("Skipping email alert due to rate limit for sender %s", sender_whatsapp)
        return

    _LAST_ALERT_TS_BY_SENDER[sender_whatsapp] = now

    background_tasks.add_task(_send_email_alert_task, sender_whatsapp, body_text, analysis_results, message_sid)

def _send_email_alert_task(sender_whatsapp: str, body_text: str, analysis_results: Dict[str, Any], message_sid: Optional[str]):
    try:
        method = os.getenv("EMAIL_METHOD", "gmail").lower()
        if method != "gmail":
            logger.info("EMAIL_METHOD not gmail; skipping send")
            return

        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_pass = os.getenv("SMTP_PASS", "")
        email_from = os.getenv("EMAIL_FROM", smtp_user)
        email_to = os.getenv("EMAIL_TO", "").split(",")
        email_to = [e.strip() for e in email_to if e.strip()]

        if not (smtp_user and smtp_pass and email_from and email_to):
            logger.error("Email alert missing configuration; ensure SMTP_USER/PASS and EMAIL_FROM/EMAIL_TO are set")
            return

        # Build email content
        risk_level = analysis_results.get("risk_level", "")
        patterns = analysis_results.get("patterns", [])
        red_flags = analysis_results.get("red_flags", [])

        # Top flag summary similar to WhatsApp text
        top_flag = None
        try:
            if patterns:
                top = patterns[0]
                category_name = (top.get("category") or top.get("name", "")).replace("_", " ").title()
                matches = top.get("matches") or []
                if matches:
                    example = str(matches[0])[:120]
                    top_flag = f"Top Flag: {category_name} — \"{example}\""
                elif top.get("description"):
                    top_flag = f"Top Flag: {category_name} — {top.get('description')[:140]}"
            if not top_flag and red_flags:
                top_flag = f"Top Flag: {str(red_flags[0])[:140]}"
        except Exception:
            pass

        snippet = _sanitize_snippet(body_text, 300)
        ts = datetime.utcnow().isoformat() + "Z"

        subject = f"[ALERT] Abuse detected from {sender_whatsapp}"
        lines = [
            f"Alert Timestamp: {ts}",
            f"From: {sender_whatsapp}",
            f"Risk Level: {risk_level}",
        ]
        if top_flag:
            lines.append(top_flag)
        lines.extend([
            "", "Message Snippet:", snippet,
        ])
        if message_sid:
            lines.extend(["", f"Twilio MessageSid: {message_sid}"])

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = email_from
        msg["To"] = ", ".join(email_to)
        msg.set_content("\n".join(lines))

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        logger.info("Email alert sent to %s", email_to)
    except Exception as e:
        logger.error("Email alert failed: %s", e)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "SilentSignal WhatsApp API"}

@app.post("/whatsapp/inbound")
async def handle_whatsapp_message(
    Body: str = Form(...),
    From: str = Form(...),
    To: Optional[str] = Form(None),
    MessageSid: Optional[str] = Form(None),
    AccountSid: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = None
):
    """
    Handle incoming WhatsApp messages from Twilio webhook
    
    Twilio sends form-encoded data with these fields:
    - Body: The message text
    - From: Sender's WhatsApp number (e.g., "whatsapp:+1234567890")
    - To: Recipient's WhatsApp number
    - MessageSid: Unique message identifier
    - AccountSid: Twilio account identifier
    """
    try:
        logger.info(f"Received WhatsApp message from {From}: {Body[:50]}...")
        
        if not Body.strip():
            return PlainTextResponse(
                content="Error: No message body provided",
                status_code=400
            )
        
        # Analyze the message using SilentSignal
        try:
            analysis_results = orchestrator.analyze_conversation(Body)
            
            # Generate concise response
            response_text = generate_whatsapp_text_response(analysis_results)
            
            logger.info(f"Analysis completed: {analysis_results['risk_level']} risk level")

            # Trigger email alert if configured and abuse level
            try:
                if _should_send_email_alert(str(analysis_results.get("risk_level", ""))):
                    if background_tasks is not None:
                        _queue_email_alert(background_tasks, From, Body, analysis_results, MessageSid)
            except Exception as e:
                logger.error(f"Email alert trigger error: {e}")
            
            # Return TwiML response for WhatsApp
            twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{response_text}</Message>
</Response>"""
            
            return PlainTextResponse(content=twiml_response, media_type="application/xml")
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return PlainTextResponse(
                content="""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Sorry, analysis failed. Please try again.</Message>
</Response>""",
                media_type="application/xml",
                status_code=200  # Twilio expects 200 even on errors
            )
    
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return PlainTextResponse(
            content="""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Sorry, an error occurred. Please try again.</Message>
</Response>""",
            media_type="application/xml",
            status_code=200  # Twilio expects 200 even on errors
        )

def generate_whatsapp_text_response(analysis_results: Dict[str, Any]) -> str:
    """Generate concise text response for WhatsApp (TwiML)"""
    risk_level = analysis_results.get("risk_level", "safe")
    patterns = analysis_results.get("patterns", [])
    red_flags = analysis_results.get("red_flags", [])
    suggestions = analysis_results.get("suggestions", [])
    
    # Risk level emojis
    risk_emojis = {
        "safe": "✅",
        "concerning": "⚠️", 
        "abuse": "🚨"
    }
    
    # Build response message
    response_parts = []
    
    # Risk level
    risk_emoji = risk_emojis.get(risk_level, "❓")
    response_parts.append(f"{risk_emoji} *Risk Level: {risk_level.title()}*")
    response_parts.append("")  # Blank line
    
    # Patterns detected
    if patterns:
        pattern_names = [p.get("category", p.get("name", "")).replace("_", " ").title() for p in patterns[:3]]
        if pattern_names:
            response_parts.append(f"🔍 *Patterns Detected:*")
            response_parts.append(", ".join(pattern_names))
            response_parts.append("")  # Blank line
    
    # Red flags
    if red_flags:
        response_parts.append(f"🚩 *Red Flags:* {len(red_flags)} detected")
        # Add a short description of the top red flag for clarity
        top_flag_summary = None
        try:
            # Prefer structured pattern info if available
            if patterns:
                top = patterns[0]
                category_name = (top.get("category") or top.get("name", "")).replace("_", " ").title()
                desc = (top.get("description") or "").strip()
                matches = top.get("matches") or []
                if matches:
                    # Use the first matched phrase as a concise example
                    example = str(matches[0])[:80]
                    top_flag_summary = f"📝 Top Flag: {category_name} — \"{example}\""
                elif desc:
                    top_flag_summary = f"📝 Top Flag: {category_name} — {desc[:100]}"
            # Fallback to the first red flag string
            if not top_flag_summary and isinstance(red_flags, list) and red_flags:
                top_flag_summary = f"📝 Top Flag: {str(red_flags[0])[:100]}"
        except Exception:
            pass
        if top_flag_summary:
            response_parts.append(top_flag_summary)
        response_parts.append("")  # Blank line
    
    # Suggestions
    if suggestions:
        response_parts.append(f"💡 *Suggestion:*")
        response_parts.append(suggestions[0])
        response_parts.append("")  # Blank line
    
    # Safety concern
    if risk_level == "abuse":
        response_parts.append("🆘 *IMPORTANT:* This shows concerning patterns.")
        response_parts.append("Consider reaching out for help:")
        response_parts.append("• National DV Hotline: 1-800-799-7233")
    elif risk_level == "concerning":
        response_parts.append("⚠️ *Note:* Monitor the situation carefully")
        response_parts.append("Pay attention to how conversations make you feel")
    else:
        response_parts.append("No concerning patterns detected in this message.")
    
    # Join response and return
    message = "\n".join(response_parts)
    
    # Escape XML special characters
    message = message.replace("&", "&amp;")
    message = message.replace("<", "&lt;")
    message = message.replace(">", "&gt;")
    message = message.replace('"', "&quot;")
    message = message.replace("'", "&apos;")
    
    return message

def generate_whatsapp_response(analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate concise response for WhatsApp"""
    risk_level = analysis_results.get("risk_level", "safe")
    patterns = analysis_results.get("patterns", [])
    red_flags = analysis_results.get("red_flags", [])
    suggestions = analysis_results.get("suggestions", [])
    
    # Risk level emojis
    risk_emojis = {
        "safe": "✅",
        "concerning": "⚠️", 
        "abuse": "🚨"
    }
    
    # Build response message
    response_parts = []
    
    # Risk level
    risk_emoji = risk_emojis.get(risk_level, "❓")
    response_parts.append(f"{risk_emoji} Risk Level: {risk_level.title()}")
    
    # Patterns detected
    if patterns:
        pattern_names = [p["name"] for p in patterns[:3]]
        response_parts.append(f"🔍 Patterns: {', '.join(pattern_names)}")
    
    # Red flags
    if red_flags:
        response_parts.append(f"🚩 Red Flags: {len(red_flags)} detected")
    
    # Suggestions
    if suggestions:
        response_parts.append(f"💡 Suggestions: {suggestions[0]}")
    
    # Safety concern
    if risk_level == "abuse":
        response_parts.append("🆘 Consider reaching out for help")
    elif risk_level == "concerning":
        response_parts.append("⚠️ Monitor the situation carefully")
    
    # Join response
    response_message = "\n".join(response_parts)
    
    return {
        "message": response_message,
        "risk_level": risk_level,
        "patterns_count": len(patterns),
        "red_flags_count": len(red_flags),
        "analysis_timestamp": analysis_results.get("analysis_timestamp", ""),
        "confidence": analysis_results.get("confidence", 0.0)
    }

@app.post("/whatsapp/test")
async def test_whatsapp_analysis(request: Request):
    """Test endpoint for WhatsApp analysis"""
    try:
        data = await request.json()
        message = data.get("message", "")
        
        if not message:
            return JSONResponse(
                content={"error": "No message provided"},
                status_code=400
            )
        
        # Analyze message
        analysis_results = orchestrator.analyze_conversation(message)
        response = generate_whatsapp_response(analysis_results)
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Test analysis error: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/whatsapp/status")
async def get_status():
    """Get service status"""
    try:
        # Check orchestrator health
        workflow_status = orchestrator.get_workflow_status()
        
        return {
            "status": "healthy",
            "orchestrator_status": workflow_status["overall_status"],
            "workflow_steps": len(workflow_status["steps"]),
            "service": "SilentSignal WhatsApp API"
        }
        
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "service": "SilentSignal WhatsApp API"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


