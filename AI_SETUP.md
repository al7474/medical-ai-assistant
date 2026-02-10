# 🤖 AI Configuration Guide - Medical Assistant

## 🎯 Overview

Your Medical AI Assistant now supports intelligent conversations using:
- **OpenAI GPT** (GPT-3.5, GPT-4)
- **Anthropic Claude** (Claude 3 Sonnet, Opus, Haiku)

The AI service falls back to simple responses if no API key is configured.

---

## 🚀 Quick Setup (5 minutes)

### Option 1: OpenAI (Recommended for beginners)

**1. Get API Key:**
- Visit: https://platform.openai.com/api-keys
- Click "Create new secret key"
- Copy your key (starts with `sk-...`)

**2. Configure:**
```bash
# Create .env file from example
cp .env.example .env

# Edit .env and add your key
OPENAI_API_KEY=sk-your-actual-key-here
AI_PROVIDER=openai
AI_MODEL=gpt-3.5-turbo  # or gpt-4 if you have access
```

**3. Restart server:**
```bash
python -m uvicorn main:app --reload
```

✅ Done! AI is now enabled.

---

### Option 2: Anthropic Claude

**1. Get API Key:**
- Visit: https://console.anthropic.com/
- Create account and get API key
- Copy your key (starts with `sk-ant-...`)

**2. Configure:**
```bash
# Edit .env file
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
AI_PROVIDER=anthropic
AI_MODEL=claude-3-sonnet-20240229
```

**3. Restart server:**
```bash
python -m uvicorn main:app --reload
```

✅ Done! Claude is now enabled.

---

## 🧪 Testing the AI

### Using Swagger UI (Easiest)
1. Open: http://localhost:8000/docs
2. Click on `POST /chat`
3. Click "Try it out"
4. Enter:
```json
{
  "text": "Hello! I have a headache. What should I do?"
}
```
5. Click "Execute"
6. See AI response!

### Using curl
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello! I have a headache for 3 days."}'
```

### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"text": "I need help scheduling an appointment"}
)

print(response.json()["bot_response"])
```

---

## 📊 Check AI Status

```bash
# Check if AI is enabled
curl http://localhost:8000/info
```

Look for:
```json
"ai_status": {
  "available": true,
  "provider": "openai",
  "model": "gpt-3.5-turbo"
}
```

---

## 💰 Pricing & Usage

### OpenAI GPT-3.5-turbo
- **Input:** $0.0005 / 1K tokens (~750 words)
- **Output:** $0.0015 / 1K tokens
- **Example:** 100 conversations ≈ $0.50 - $2.00

### OpenAI GPT-4
- **Input:** $0.03 / 1K tokens
- **Output:** $0.06 / 1K tokens
- **Example:** 100 conversations ≈ $30 - $60

### Anthropic Claude 3 Sonnet
- **Input:** $0.003 / 1K tokens
- **Output:** $0.015 / 1K tokens
- **Example:** 100 conversations ≈ $3 - $6

💡 **Tip:** Start with GPT-3.5-turbo for development (cheaper)

---

## 🔧 Configuration Options

### Available Models

**OpenAI:**
- `gpt-3.5-turbo` - Fast, cheap, good quality ✅ Recommended
- `gpt-4` - Best quality, expensive
- `gpt-4-turbo-preview` - Faster GPT-4

**Anthropic:**
- `claude-3-haiku-20240307` - Fastest, cheap
- `claude-3-sonnet-20240229` - Balanced ✅ Recommended
- `claude-3-opus-20240229` - Best quality, expensive

### Environment Variables

```bash
# Provider (choose one)
AI_PROVIDER=openai        # or: anthropic
AI_MODEL=gpt-3.5-turbo    # or any model above

# API Keys (only one needed)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 🐛 Troubleshooting

### "AI Service not available"
- Check if API key is set in `.env`
- Make sure key doesn't have spaces
- Restart the server after adding key

### "Incorrect API key provided"
- Verify your key at provider's website
- Make sure you copied the full key
- Check for extra spaces or quotes

### "Rate limit exceeded"
- You've hit the usage limit
- Wait a few minutes or upgrade your plan
- See provider's dashboard for usage

### "Model not found"
- Check model name spelling
- Verify you have access to that model
- Try `gpt-3.5-turbo` as fallback

---

## 🔒 Security Best Practices

**DO:**
- ✅ Keep API keys in `.env` file
- ✅ Add `.env` to `.gitignore`
- ✅ Use environment variables
- ✅ Rotate keys periodically
- ✅ Monitor usage and costs

**DON'T:**
- ❌ Commit API keys to git
- ❌ Share keys in public
- ❌ Use production keys in development
- ❌ Hardcode keys in source code

---

## 🎓 How It Works

```
User Message → FastAPI Endpoint → ChatService
                                        ↓
                                   LangChain
                                        ↓
                              LLM (OpenAI/Anthropic)
                                        ↓
                                   Response → User
```

### Features:
- **System Prompt:** Medical assistant instructions
- **Context:** Can include user info, medical history
- **Memory:** Conversation history (coming soon)
- **Fallback:** Simple responses if AI unavailable

---

## 📈 Next Steps

Once AI is working:
1. ✅ Add conversation memory (store chat history)
2. ✅ Integrate with user database (personalized responses)
3. ✅ Add appointment scheduling via AI
4. ✅ Implement LangGraph for complex workflows
5. ✅ Add WebSocket for real-time chat

Need help? Check:
- [OpenAI Documentation](https://platform.openai.com/docs)
- [Anthropic Documentation](https://docs.anthropic.com/)
- [LangChain Documentation](https://python.langchain.com/)

---

## ✅ Success Checklist

- [ ] API key obtained from OpenAI or Anthropic
- [ ] `.env` file created and configured
- [ ] Server restarted
- [ ] Tested `/info` endpoint shows `ai_available: true`
- [ ] Tested `/chat` endpoint with a message
- [ ] Got AI response (not fallback)

**All checked?** 🎉 Your AI is ready!
