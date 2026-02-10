# Phase 4: LangGraph Intelligent Workflows - Completed ✅

**Completion Date:** February 10, 2026

## Overview

Phase 4 implements intelligent agent workflows using LangGraph, enabling the AI assistant to autonomously use tools, perform multi-step reasoning, and execute complex tasks. The agent can access medical data, search documents, manage appointments, and combine information from multiple sources to provide comprehensive responses.

## Key Features Implemented

### 1. Agent Tools System
- **Location:** `backend/services/agent_tools.py`
- **Functionality:** Six specialized tools that the agent can invoke

#### Available Tools:

**1. search_medical_documents**
- Semantic search through user's uploaded medical documents
- Uses FAISS vector store from Phase 3
- Returns top-k relevant document excerpts
- Automatically filters by user_id for privacy

**2. get_user_medical_profile**
- Retrieves complete medical profile
- Includes: age, blood type, height, weight, BMI
- Medical history: allergies, chronic conditions, medications, surgeries
- Lifestyle factors: smoking, alcohol, exercise
- Formatted output with emoji indicators

**3. get_upcoming_appointments**
- Lists future appointments within specified timeframe
- Default: next 30 days
- Shows: date, time, doctor, type, reason, status
- Sorted chronologically

**4. create_appointment**
- Creates new appointments
- Validates date format (ISO 8601)
- Prevents past appointments
- Returns confirmation with appointment ID
- Automatic status: "scheduled"

**5. list_medical_documents**
- Lists user's uploaded documents
- Shows: title, type, upload date, processing status
- Configurable limit (default: 10)
- Most recent first

**6. get_current_date_time**
- Provides current date and time
- Useful for temporal context
- Formatted in readable format ("Monday, February 10, 2026")

### 2. LangGraph Agent Service
- **Location:** `backend/services/langgraph_agent_service.py`
- **Architecture:** State-based graph workflow

#### Agent Components:

**State Management:**
```python
class AgentState(TypedDict):
    messages: Annotated[List, add_messages]
    user_id: int
    user_context: Optional[str]
```

**Graph Workflow:**
```
Entry → Agent Node → Conditional Edge
                         ↓
         Tools Needed?  Yes → Tools Node → Agent Node
                         ↓
                        No → END
```

**Key Features:**
- **Multi-provider support:** OpenAI (GPT-4) or Anthropic (Claude)
- **Tool binding:** LLM automatically bound with all tools
- **Conversation history:** Maintains last 10 messages for context
- **Medical context injection:** User profile injected into system prompt
- **Error handling:** Graceful fallbacks if tools fail
- **Async execution:** Full async/await support

**System Prompt:**
- Defines agent capabilities and guidelines
- Emphasizes medical safety and privacy
- Provides tool usage examples
- Sets interaction style (empathetic, professional)

### 3. Agent API Endpoints
- **Location:** `backend/api/routes/agent.py`

#### Endpoints:

**POST /agent/chat**
- Chat with the intelligent agent
- Request body:
  ```json
  {
    "message": "Your question here",
    "conversation_id": 123,  // optional
    "use_context": true      // include medical profile & history
  }
  ```
- Response:
  ```json
  {
    "response": "Agent's answer",
    "conversation_id": 123,
    "tools_used": ["search_medical_documents", "get_upcoming_appointments"]
  }
  ```
- Automatically saves conversation to database
- Includes medical context and conversation history

**GET /agent/capabilities**
- Returns list of available tools
- Shows tool descriptions and parameters
- Indicates which AI provider is active
- Useful for frontend UI building

**POST /agent/test-tool/{tool_name}**
- Direct tool testing endpoint
- Development and debugging aid
- Bypasses agent reasoning
- Parameters passed as JSON body

### 4. WebSocket Agent Integration
- **Location:** `backend/api/routes/websocket.py`
- **Enhancement:** Agent mode in real-time chat

**Usage:**
```json
{
  "type": "message",
  "text": "Schedule an appointment for next week",
  "use_agent": true
}
```

**Features:**
- Optional agent activation per message
- Fallback to simple chat if agent unavailable
- Typing indicator shows "Agent is working..."
- Response includes mode: "agent" or "chat"
- Conversation history provided to agent
- Saves agent interactions to database

**Response Format:**
```json
{
  "type": "message",
  "text": "I've scheduled your appointment...",
  "mode": "agent",
  "provider": "langgraph_agent",
  "model": "openai",
  "timestamp": "2026-02-10T15:30:00"
}
```

## Technical Architecture

### LangGraph Workflow

```
User Message
    ↓
Agent Node (LLM)
    ↓
Evaluate: Need tools?
    ↓
  Yes → Execute Tools → Results → Agent Node (with results)
    ↓                                    ↓
   No ← ← ← ← ← ← ← ← ← ← Final Response
    ↓
  END
```

### Tool Execution Flow

1. **User sends message** with complex request
2. **Agent analyzes** request and decides which tools to use
3. **Tools execute** in parallel or sequence (LangGraph decides)
4. **Results returned** to agent
5. **Agent synthesizes** information from all tool results
6. **Final response** formatted for user

### State Persistence

- Messages accumulate in state
- Tool results added as ToolMessage objects
- Context maintained across tool invocations
- Final state returned with complete conversation

## Dependencies

```python
# Already installed from Phase 3
langgraph==0.2.60
langchain==0.3.13
langchain-core==0.3.63
langchain-openai==0.2.14
langchain-anthropic==0.3.7
```

## Configuration Requirements

### Environment Variables

```bash
# .env file - At least ONE required for agent
OPENAI_API_KEY=sk-...        # Recommended for best tool calling
# OR
ANTHROPIC_API_KEY=sk-ant-... # Alternative
```

**Note:** OpenAI is recommended for Phase 4 as it has better tool calling capabilities than Anthropic.

## Usage Examples

### Example 1: Multi-step Appointment Scheduling

**User:** "I need to schedule a cardiology appointment next Monday at 10am"

**Agent Process:**
1. Calls `get_current_date_time` to determine "next Monday"
2. Calls `create_appointment` with calculated date
3. Returns confirmation with details

**Response:**
```
✅ I've scheduled your cardiology appointment!

📅 Date: Monday, February 17, 2026 at 10:00 AM
👨‍⚕️ Doctor: [To be assigned]
📋 Type: Specialist - Cardiology
🆔 Appointment ID: 42

Would you like me to add any specific notes or reasons for this visit?
```

### Example 2: Document-based Question

**User:** "What was my blood pressure from my last checkup?"

**Agent Process:**
1. Calls `search_medical_documents` with query "blood pressure checkup"
2. Finds relevant lab results
3. Extracts blood pressure reading
4. Provides answer with source reference

**Response:**
```
According to your lab results from January 15, 2026:

📊 Blood Pressure: 120/80 mmHg
✅ Status: Normal range

This is from your "Annual Physical Exam - Lab Results" document.
Your blood pressure is within the healthy range (systolic: 90-120, diastolic: 60-80).
```

### Example 3: Medical Profile Summary

**User:** "What medications am I currently taking?"

**Agent Process:**
1. Calls `get_user_medical_profile`
2. Extracts medications section
3. Formats in user-friendly way

**Response:**
```
💊 Your Current Medications:

1. Metformin 500mg - Twice daily with meals
2. Lisinopril 10mg - Once daily in the morning
3. Atorvastatin 20mg - Once daily at bedtime

Please remember to take these as prescribed and consult your doctor before making any changes.
```

### Example 4: Complex Multi-tool Query

**User:** "Do I have any appointments this week and are there any mentions of diabetes in my documents?"

**Agent Process:**
1. Calls `get_current_date_time` to determine current week
2. Calls `get_upcoming_appointments` with 7-day window
3. Calls `search_medical_documents` with query "diabetes"
4. Synthesizes results from all three tools

**Response:**
```
📅 **Upcoming Appointments This Week:**
- Wednesday, February 12, 2026 at 2:00 PM - Follow-up with Dr. Smith

🔍 **Diabetes Mentions in Your Records:**
I found several references to diabetes in your documents:

1. Your lab results from January show HbA1c levels of 6.2%, which indicates prediabetes
2. Your doctor prescribed Metformin to manage blood sugar levels
3. Nutrition recommendations include low-carb diet and regular exercise

Your Wednesday appointment would be a good time to discuss your diabetes management plan with Dr. Smith.
```

## Testing

### Test Agent Capabilities

```bash
# 1. Get available tools
GET http://localhost:8000/agent/capabilities
Authorization: Bearer YOUR_JWT_TOKEN
```

### Test Individual Tool

```bash
# 2. Test appointment lookup
POST http://localhost:8000/agent/test-tool/get_upcoming_appointments
Authorization: Bearer YOUR_JWT_TOKEN
{
  "days_ahead": 30
}
```

### Test Agent Chat

```bash
# 3. Chat with agent
POST http://localhost:8000/agent/chat
Authorization: Bearer YOUR_JWT_TOKEN
{
  "message": "What are my upcoming appointments?",
  "use_context": true
}
```

### Test WebSocket Agent

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat?token=YOUR_JWT_TOKEN');

ws.send(JSON.stringify({
  type: 'message',
  text: 'Search my documents for blood pressure readings',
  use_agent: true
}));
```

## Database Verification

### Check Agent Conversations

```sql
-- View agent conversations
SELECT 
    c.id,
    c.title,
    COUNT(m.id) as message_count,
    MAX(m.created_at) as last_message,
    m.ai_provider
FROM conversations c
JOIN messages m ON m.conversation_id = c.id
WHERE m.ai_provider = 'langgraph_agent'
GROUP BY c.id, m.ai_provider
ORDER BY MAX(m.created_at) DESC;
```

### View Agent Tool Usage

```sql
-- Messages from agent
SELECT 
    content,
    ai_provider,
    ai_model,
    tokens_used,
    created_at
FROM messages
WHERE ai_provider = 'langgraph_agent'
ORDER BY created_at DESC
LIMIT 10;
```

## Performance Considerations

### Tool Execution Time
- Single tool: ~1-3 seconds
- Multiple tools: ~3-8 seconds (parallel execution)
- Complex multi-step: ~5-15 seconds

### Cost Optimization
- OpenAI GPT-4o-mini: ~$0.15 per 1M input tokens
- Tool calls add 20-40% to token usage
- Agent reasoning adds overhead vs simple chat

### Rate Limiting
- No built-in rate limiting (add in Phase 6)
- Consider limiting:
  - Requests per user per minute
  - Tools per conversation
  - Maximum agent iterations

## Error Handling

### Tool Failures
```python
# Tools don't crash the agent
try:
    result = await tool.ainvoke(params)
except Exception as e:
    result = f"❌ Error: {str(e)}"
    # Agent continues with error message
```

### Agent Failures
```python
# Falls back to simple chat
if not agent_available:
    response = await simple_chat_service.chat(message)
```

### Database Failures
```python
# Non-blocking persistence
try:
    save_to_database(message)
except Exception:
    print("⚠️ Failed to save message")
    # Continue without saving
```

## Security Considerations

### Tool Access Control
- All tools validate `user_id`
- Database queries filtered by user
- No cross-user data access possible
- Appointments only visible to owner

### API Key Protection
- Keys stored in .env (not committed)
- No keys in logs or responses
- Environment variables only

### SQL Injection Prevention
- All queries use SQLAlchemy ORM
- Parameterized queries
- No raw SQL with user input

## Known Limitations

1. **No streaming:** Agent responses are not streamed (all-or-nothing)
2. **No cancellation:** Once started, agent runs to completion
3. **Limited iterations:** Default max iterations (can be extended)
4. **No memory across sessions:** Agent doesn't remember beyond conversation
5. **Tool parallelization:** LangGraph decides, not optimal for all cases
6. **No custom workflows:** Single predefined graph structure

## Future Enhancements (Potential)

- [ ] Custom workflows per user type
- [ ] Streaming agent responses
- [ ] Agent cancellation mid-execution
- [ ] Long-term memory across sessions
- [ ] Parallel tool execution optimization
- [ ] Conditional logic nodes
- [ ] Human-in-the-loop approval for actions
- [ ] Agent analytics dashboard
- [ ] Cost tracking per agent run
- [ ] A/B testing different prompts

## Files Created/Modified

### New Files
```
backend/services/agent_tools.py                   (300+ lines)
backend/services/langgraph_agent_service.py       (250+ lines)
backend/api/routes/agent.py                       (180+ lines)
```

### Modified Files
```
backend/main.py                                   (Added agent router)
backend/api/routes/websocket.py                   (Added agent mode)
```

## Integration with Previous Phases

### With Phase 1 (Medical Data Models)
- Agent tools query MedicalProfile model
- Appointments CRUD through agent
- Medical documents accessible via tools

### With Phase 2 (User Context)
- Conversation history provided to agent
- Context saved for each agent interaction
- Medical context injected into agent prompt

### With Phase 3 (RAG)
- `search_medical_documents` uses FAISS vector store
- Document content available to agent
- Semantic search integrated into agent workflow

### For Phase 5 (Advanced Frontend)
- `/agent/capabilities` endpoint for UI
- Tool testing endpoint for debugging
- WebSocket agent mode for real-time

## Success Metrics

✅ **Implemented:**
- 6 functional agent tools
- LangGraph state-based workflow
- Multi-step reasoning capability
- Tool calling with OpenAI/Anthropic
- REST and WebSocket agent endpoints
- Conversation persistence
- Error handling and fallbacks

✅ **Code Quality:**
- Type hints throughout
- Comprehensive error handling
- Async/await patterns
- Modular architecture
- Reusable components

✅ **Architecture:**
- Clean separation of concerns
- Tools decoupled from agent logic
- State management with TypedDict
- Extensible tool system

## Next Phase: Phase 5 (Advanced Frontend UI)

**Objective:** Build comprehensive medical dashboard with agent integration

**Planned Features:**
- Medical dashboard with visualizations
- Document viewer with PDF preview
- Agent chat interface with tool indicators
- Medical profile management
- Appointment calendar
- Analytics and insights

**Estimated Effort:** 12-16 hours

---

## Conclusion

Phase 4 successfully implements intelligent agent workflows using LangGraph, transforming the medical assistant from a simple chatbot into an autonomous agent capable of complex reasoning and multi-step task execution. The agent can seamlessly access medical data, search documents, manage appointments, and combine information from multiple sources.

The modular tool system makes it easy to add new capabilities, while the state-based workflow ensures reliable execution. Integration with previous phases (medical data, context, RAG) creates a powerful system that understands patient history and provides personalized assistance.

**Status:** ✅ Phase 4 Complete - Ready for Phase 5

---

**Documentation:** All technical documentation in English (per LANGUAGE_GUIDELINES.md)  
**User Interface:** Spanish (end-user facing)  
**Completion Date:** February 10, 2026
