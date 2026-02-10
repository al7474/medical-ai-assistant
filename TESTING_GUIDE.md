# Testing Setup Guide

## 🚀 Quick Start for Testing Phase 4

This guide will help you test the LangGraph agent with Gemini API and realistic medical data.

---

## 📋 Prerequisites

1. **Google Gemini API Key**
   - Get your free API key: https://makersuite.google.com/app/apikey
   - Free tier includes generous limits for testing

2. **Database Running**
   - Ensure PostgreSQL is running (docker-compose up -d)

3. **Python Environment**
   - Virtual environment activated
   - All dependencies installed

---

## ⚙️ Setup Steps

### 1. Install Gemini Dependencies

```bash
cd backend
pip install langchain-google-genai==2.0.7 google-generativeai==0.8.3
```

### 2. Configure Environment

Edit your `.env` file (or create from `.env.example`):

```bash
# AI Configuration - Use Gemini
AI_PROVIDER=gemini
AI_MODEL=gemini-1.5-flash

# Google Gemini API Key
GEMINI_API_KEY=your-actual-api-key-here

# Keep database settings
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/medical_assistant
```

### 3. Create Test User

Run the test user creation script:

```bash
python create_test_user.py
```

This will create:
- ✅ Test user account (testuser@example.com / Test123!)
- ✅ Complete medical profile (45-year-old male with diabetes and hypertension)
- ✅ 4 upcoming appointments
- ✅ 2 past appointments  
- ✅ 4 medical documents (lab results, BP log, medication list, education materials)
- ✅ Sample conversation history

### 4. Start Backend

```bash
python main.py
```

You should see:
```
✅ AI Service initialized with Google Gemini (gemini-1.5-flash)
✅ LangGraph Agent initialized with 6 tools
```

---

## 🧪 Testing the Agent

### Option A: Web Interface

1. Open frontend: http://localhost:3000
2. Login with: `testuser@example.com` / `Test123!`
3. In chat, enable "Use Agent" mode
4. Try these queries:

```
What are my current medications?
Show me my upcoming appointments
When is my next appointment with Dr. González?
Search my lab results for glucose levels
What should I know about my diabetes?
Schedule a follow-up with Dr. Martínez in 2 weeks
```

### Option B: Test Script

Edit `test_agent.py` and add your JWT token:
```python
JWT_TOKEN = "your-jwt-token-here"
```

Then run tests:
```bash
python test_agent.py
```

### Option C: Direct API Testing

1. **Get JWT Token:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser@example.com&password=Test123!"
```

2. **Check Agent Capabilities:**
```bash
curl http://localhost:8000/agent/capabilities \
  -H "Authorization: Bearer YOUR_TOKEN"
```

3. **Chat with Agent:**
```bash
curl -X POST http://localhost:8000/agent/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are my current medications?",
    "use_context": true
  }'
```

4. **Test Individual Tools:**
```bash
# Get medical profile
curl -X POST http://localhost:8000/agent/test-tool/get_user_medical_profile \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'

# Get upcoming appointments
curl -X POST http://localhost:8000/agent/test-tool/get_upcoming_appointments \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"days_ahead": 30}'

# Search medical documents
curl -X POST http://localhost:8000/agent/test-tool/search_medical_documents \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "glucose", "max_results": 3}'
```

### Option D: WebSocket Testing

Open browser console and run:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/test');
const token = 'YOUR_JWT_TOKEN';

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: token
  }));
  
  setTimeout(() => {
    ws.send(JSON.stringify({
      type: 'message',
      text: 'What are my upcoming appointments?',
      use_agent: true,
      use_context: true
    }));
  }, 1000);
};

ws.onmessage = (event) => {
  console.log('Received:', JSON.parse(event.data));
};
```

---

## 🎯 Test Scenarios

### Basic Tool Testing
- ✅ Get user medical profile
- ✅ List upcoming appointments
- ✅ Search medical documents
- ✅ Get current date/time

### Multi-Step Reasoning
- ✅ "Find my next cardiology appointment and tell me what I should ask the doctor"
- ✅ "Check my lab results for glucose and compare to my target range"
- ✅ "When are my appointments in the next 2 weeks and which doctors?"

### Context-Aware Responses
- ✅ "What medications am I taking for blood pressure?"
- ✅ "What are my diet restrictions based on my conditions?"
- ✅ "Should I be concerned about my recent lab results?"

### Appointment Management
- ✅ "Schedule a follow-up with Dr. González next month"
- ✅ "When is my ophthalmology screening?"
- ✅ "List all my appointments with cardiologists"

### Document Search
- ✅ "Show me my latest HbA1c results"
- ✅ "What does my blood pressure log say?"
- ✅ "Find information about my medications"

---

## 📊 Verification Queries

Run these SQL queries to verify test data:

```sql
-- Check user
SELECT id, email, username, full_name FROM users WHERE email = 'testuser@example.com';

-- Check medical profile
SELECT * FROM medical_profiles WHERE user_id = (SELECT id FROM users WHERE email = 'testuser@example.com');

-- Check appointments
SELECT appointment_date, appointment_type, doctor_name, status 
FROM appointments 
WHERE user_id = (SELECT id FROM users WHERE email = 'testuser@example.com')
ORDER BY appointment_date;

-- Check documents
SELECT filename, description, LENGTH(original_text) as text_length
FROM medical_documents
WHERE user_id = (SELECT id FROM users WHERE email = 'testuser@example.com');

-- Check conversation
SELECT c.title, COUNT(m.id) as message_count
FROM conversations c
LEFT JOIN messages m ON m.conversation_id = c.id
WHERE c.user_id = (SELECT id FROM users WHERE email = 'testuser@example.com')
GROUP BY c.id, c.title;
```

---

## 🐛 Troubleshooting

### "AI Service not available"
- Check GEMINI_API_KEY in .env
- Verify API key is valid (not a placeholder)
- Ensure AI_PROVIDER=gemini in .env

### "No tool calls in response"
- Gemini models support tool calling
- Check agent logs for errors
- Verify tools are initialized properly

### "User not found"
- Run `create_test_user.py` again
- Check database connection
- Verify user exists: `SELECT * FROM users WHERE email = 'testuser@example.com';`

### "Vector store not initialized"
- Documents need to be processed
- RAG system requires FAISS indexing
- Check medical_documents table has data

### WebSocket connection fails
- Ensure backend is running on port 8000
- Check JWT token is valid (not expired)
- Verify WebSocket route is registered

---

## 📈 Expected Performance

### Response Times
- Simple tool call (profile, appointments): 1-3 seconds
- Document search: 2-5 seconds
- Multi-step reasoning: 5-15 seconds

### Gemini API Costs
- Free tier: 60 requests/minute
- gemini-1.5-flash: Very low cost (~$0.000125/1K tokens)
- Perfect for development and testing

### Token Usage
- Average query: 500-2000 tokens
- With medical context: 1500-4000 tokens
- Daily testing: Well within free limits

---

## ✅ Success Criteria

Your testing is successful if:

1. ✅ Agent responds to queries with tool usage
2. ✅ Medical profile retrieval works correctly
3. ✅ Appointments are listed accurately
4. ✅ Document search finds relevant information
5. ✅ Multi-step queries result in multiple tool calls
6. ✅ Conversation is saved to database
7. ✅ Error handling works (graceful degradation)
8. ✅ Context is properly injected (allergies, conditions mentioned)

---

## 🎉 Next Steps

After successful testing:

1. ✅ Verify all 6 tools work individually
2. ✅ Test complex multi-step scenarios
3. ✅ Check conversation persistence
4. ✅ Review logs for errors
5. ✅ Test error handling (invalid inputs)
6. ✅ Measure performance metrics
7. 🚀 Proceed to Phase 5: Advanced Frontend UI

---

## 📚 Additional Resources

- **Gemini API Docs:** https://ai.google.dev/docs
- **LangChain Gemini:** https://python.langchain.com/docs/integrations/chat/google_generative_ai
- **PHASE4_COMPLETED.md:** Full agent documentation
- **test_agent.py:** Automated test scenarios

---

## 💡 Pro Tips

1. **Use descriptive queries:** "Show my diabetes medications" works better than "medications"
2. **Reference dates:** "Next week", "in 2 weeks", "next month" helps with appointments
3. **Be specific:** "Lab results" vs "Show me my HbA1c from January"
4. **Test edge cases:** Invalid dates, missing data, complex multi-tool scenarios
5. **Monitor logs:** Watch backend console for tool execution details
6. **Check database:** Verify data persistence after each test

---

## 🔄 Clean Up

To reset test data:
```bash
# Delete test user (cascade will remove all related data)
python -c "
import asyncio
from database import async_session
from models import User
from sqlalchemy import select

async def cleanup():
    async with async_session() as db:
        result = await db.execute(select(User).where(User.email == 'testuser@example.com'))
        user = result.scalar_one_or_none()
        if user:
            await db.delete(user)
            await db.commit()
            print('✅ Test user deleted')
        else:
            print('⚠️  Test user not found')

asyncio.run(cleanup())
"
```

Then run `create_test_user.py` again for fresh data.

---

**Happy Testing! 🎉**
