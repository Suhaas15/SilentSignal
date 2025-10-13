# 📱 SilentSignal WhatsApp Integration - Complete Setup Guide

## 🎯 What You'll Achieve
After following these steps, you'll be able to send WhatsApp messages and receive real-time emotional abuse analysis!

---

## 📋 **ALL STEPS FROM START TO FINISH**

### **STEP 1: Create Twilio Account (FREE)**

1. **Visit**: https://www.twilio.com/try-twilio
2. **Click**: "Sign up for free"
3. **Fill out form**:
   - Email address
   - Password
   - Phone number (for verification)
4. **Verify**: Enter the code they send to your phone
5. **Complete profile**: Answer a few quick questions
6. **Get $15 FREE credit**: Automatically added to your account

✅ **Result**: You now have a Twilio account!

---

### **STEP 2: Get Your Twilio Credentials**

1. **Log in to Twilio Console**: https://console.twilio.com/
2. **On the dashboard**, you'll see:
   ```
   Account Info
   ├── ACCOUNT SID: ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   └── AUTH TOKEN: [Show]
   ```
3. **Copy Account SID**: Click the copy button
4. **Reveal Auth Token**: Click "Show" then copy it
5. **Save somewhere safe**: You'll need these in Step 4

✅ **Result**: You have your Account SID and Auth Token!

---

### **STEP 3: Set Up WhatsApp Sandbox**

1. **In Twilio Console**, click the left menu:
   - **Messaging** → **Try it out** → **Send a WhatsApp message**
2. **You'll see sandbox instructions**:
   ```
   Sandbox Number: +1 415 523 8886 (example)
   Join Code: join <random-word>
   ```
3. **Open WhatsApp on your phone**
4. **Send a message to the sandbox number**:
   - To: `+1 415 523 8886` (or your sandbox number)
   - Message: `join <your-random-word>`
5. **Wait for confirmation**: "You are all set! The sandbox can now send/receive messages."

✅ **Result**: Your WhatsApp is connected to Twilio sandbox!

---

### **STEP 4: Configure SilentSignal**

1. **Open your `.env` file** in SilentSignal folder:
   ```bash
   # You can use any text editor
   nano .env
   # or
   code .env
   ```

2. **Add your Twilio credentials**:
   ```bash
   # NVIDIA NIM Configuration (can leave as is for now)
   NIM_BASE_URL=http://localhost:8000/v1
   NIM_API_KEY=
   
   # ADD YOUR TWILIO CREDENTIALS HERE:
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here
   
   # Other settings (leave as is)
   SILENTSIGNAL_ALLOW_PERSIST=0
   SILENTSIGNAL_DEBUG=False
   ```

3. **Save the file**: Ctrl+O (save), Ctrl+X (exit) in nano

✅ **Result**: SilentSignal is configured with your Twilio credentials!

---

### **STEP 5: Install and Set Up Ngrok**

Ngrok creates a public URL that points to your local computer.

1. **Download Ngrok**: https://ngrok.com/download
2. **Sign up for free**: https://dashboard.ngrok.com/signup
3. **Get your auth token**: On dashboard, copy your authtoken
4. **Install ngrok**:
   ```bash
   # Mac (with Homebrew)
   brew install ngrok/ngrok/ngrok
   
   # Or manually: download, unzip, and move to /usr/local/bin
   ```
5. **Authenticate**:
   ```bash
   ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN
   ```

✅ **Result**: Ngrok is installed and ready!

---

### **STEP 6: Start All Services**

You need **3 terminal windows**:

**Terminal 1 - WhatsApp API:**
```bash
cd "/Users/dishant/FILES/PROJECTS AND HOMEWORKS/NVEDIA HACKATHON/SilentSignal"
uvicorn integrations.whatsapp_fastapi:app --reload --host 0.0.0.0 --port 8000
```
✅ You'll see: `Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 - Ngrok Tunnel:**
```bash
ngrok http 8000
```
✅ You'll see something like:
```
Forwarding    https://1234-abc-def.ngrok.io -> http://localhost:8000
```
**COPY THIS URL!** You'll need it in Step 7!

**Terminal 3 - Streamlit UI (Optional):**
```bash
cd "/Users/dishant/FILES/PROJECTS AND HOMEWORKS/NVEDIA HACKATHON/SilentSignal"
streamlit run app.py
```
✅ You'll see: `URL: http://localhost:8501`

---

### **STEP 7: Configure Twilio Webhook**

1. **Go back to Twilio Console**
2. **Navigate to**: Messaging → Try it out → Send a WhatsApp message
3. **Scroll down to "Sandbox Configuration"**
4. **Find "WHEN A MESSAGE COMES IN"**
5. **Paste your ngrok URL + endpoint**:
   ```
   https://1234-abc-def.ngrok.io/whatsapp/inbound
   ```
   (Replace `1234-abc-def` with YOUR ngrok URL from Terminal 2)
6. **Select**: HTTP POST
7. **Click**: Save

✅ **Result**: Twilio will now send WhatsApp messages to SilentSignal!

---

### **STEP 8: TEST IT!**

1. **Open WhatsApp on your phone**
2. **Go to your chat with the Twilio sandbox number**
3. **Send a test message**:
   ```
   You're always making excuses. If you really cared about me, you'd make time. You're being selfish.
   ```
4. **Wait 2-3 seconds**
5. **You should receive a response**:
   ```
   ⚠️ Risk Level: Concerning
   🔍 Patterns: guilt_tripping, emotional_manipulation
   🚩 Red Flags: 2 detected
   💡 Suggestions: Pay attention to how this conversation makes you feel
   ⚠️ Monitor the situation carefully
   ```

✅ **SUCCESS!** Your WhatsApp integration is working!

---

## 🔍 **Testing Without WhatsApp**

You can test the API directly:

```bash
curl -X POST http://localhost:8000/whatsapp/test \
  -H "Content-Type: application/json" \
  -d '{"message": "You are always making excuses. If you really cared about me, you would make time."}'
```

---

## 🐛 **Troubleshooting**

### **Problem: Not receiving responses**
- Check Terminal 1: Is the API running?
- Check Terminal 2: Is ngrok running?
- Check Twilio webhook URL: Is it correct?
- Check ngrok URL: Did it change? (Free ngrok URLs change on restart)

### **Problem: "404 Not Found" error**
- Make sure webhook URL ends with `/whatsapp/inbound`
- Check if ngrok is still running

### **Problem: Timeout errors**
- Your internet connection might be slow
- The analysis is working, just takes longer
- Responses will still come through

---

## 🎉 **Quick Start Script**

Save this as `start_whatsapp.sh`:

```bash
#!/bin/bash
echo "Starting SilentSignal WhatsApp Integration..."

# Terminal 1: Start API
cd "/Users/dishant/FILES/PROJECTS AND HOMEWORKS/NVEDIA HACKATHON/SilentSignal"
uvicorn integrations.whatsapp_fastapi:app --reload --host 0.0.0.0 --port 8000 &

# Wait for API to start
sleep 3

# Terminal 2: Start ngrok
ngrok http 8000 &

echo "✅ Services started!"
echo "📱 Configure Twilio webhook with your ngrok URL + /whatsapp/inbound"
```

Then run: `bash start_whatsapp.sh`

---

## 📦 **Your Zip File**

✅ **Created**: `SilentSignal.zip` in `/Users/dishant/FILES/PROJECTS AND HOMEWORKS/NVEDIA HACKATHON/`

To extract later:
```bash
unzip SilentSignal.zip
cd SilentSignal
pip install -r requirements.txt
```

---

## 🎯 **Summary Checklist**

- [ ] Create Twilio account (FREE)
- [ ] Get Account SID and Auth Token
- [ ] Join WhatsApp sandbox
- [ ] Configure .env file
- [ ] Install ngrok
- [ ] Start WhatsApp API (Terminal 1)
- [ ] Start ngrok (Terminal 2)
- [ ] Copy ngrok URL
- [ ] Configure Twilio webhook
- [ ] Test with WhatsApp message

**Total Time**: ~15 minutes
**Cost**: $0 (all free tier)

---

## 🆘 **Need Help?**

- **Twilio Docs**: https://www.twilio.com/docs/whatsapp
- **Ngrok Docs**: https://ngrok.com/docs
- **Test API**: http://localhost:8000/docs (FastAPI docs)

**Your WhatsApp integration is ready to go!** 🚀
