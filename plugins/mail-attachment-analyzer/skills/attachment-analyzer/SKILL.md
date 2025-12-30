---
name: attachment-analyzer
description: Intelligently analyze email attachments, automatically classify importance and extract key information. Optimized for email threads with context tracking.
---

# Email Attachment Analyzer

Intelligently analyze emails and their attachments with tiered processing strategies. Specially optimized for email threads, tracking attachment context and evolution in conversation history.

## Operation Modes

### 1. Quick Mode (Default) ⚡

**Token Usage: Minimal**

- ✅ Read email metadata (sender, subject, date)
- ✅ List all attachments (filename, type, size)
- ✅ Intelligently classify attachment importance
- ✅ Detect if part of email thread
- ❌ Do NOT extract attachment content

**Use Cases**:
- Quickly browse emails
- Determine if detailed analysis needed
- Batch process emails

### 2. Interactive Mode 🔄

**Token Usage: On-demand**

- ✅ Complete all quick mode features
- ✅ Provide detailed attachment metadata analysis
- ✅ Ask user: which attachments to extract?
- ⚡ Extract only after user selection

**Use Cases**:
- Selective attachment viewing
- Uncertain which attachments matter
- Control token consumption

### 3. Auto Mode 🤖

**Token Usage: Higher**

- ✅ Automatically extract high-importance attachments
- ✅ Full content analysis
- ✅ Generate structured report with action items
- ✅ Auto-cleanup temporary files

**Use Cases**:
- Important emails (contracts, invoices, government notices)
- Need comprehensive analysis
- Token cost not a concern

## When to Use This Skill

This skill is automatically invoked when users:

- Ask to analyze email attachments
- Request email content summary
- Need to understand email thread context
- Want to identify important documents in emails

**Example Triggers**:
- "Analyze this email <message-id>"
- "What attachments are in this email?"
- "Help me review this email thread"
- "Is there anything important in this email?"

## Execution Strategy

Based on user request, choose appropriate mode:

1. **Default to Quick Mode** if user wants overview
2. **Use Interactive Mode** if user seems uncertain
3. **Use Auto Mode** if:
   - Email from known important senders (HMRC, legal, finance)
   - Subject contains keywords (invoice, contract, urgent, tax)
   - User explicitly requests full analysis

## Email Thread Handling

### Thread Detection

Always check if email is part of thread:

```python
thread_paths = mcp__mail__get_thread_paths(message_id)
if len(thread_paths) > 1:
    # Analyze thread context
    # Track attachment evolution
    # Identify latest versions
```

### Attachment Context Analysis

For threads, provide context about:
- Which attachments are duplicates
- Which are version iterations (v1 → v2 → final)
- Which are the most recent/important
- Discussion context from email bodies

## Attachment Importance Classification

### 🚨 High Importance
- Government notices (HMRC, IRS, tax documents)
- Legal documents (contracts, agreements, NDAs)
- Financial documents (invoices, receipts, bills)
- Certificates (licenses, permits)
- File type: `.pdf`

### ⚠️ Medium Importance
- Technical documentation
- Reports and analysis
- Spreadsheets and presentations
- File types: `.pdf`, `.docx`, `.xlsx`, `.pptx`

### 💡 Low Importance
- Images (unless specified as evidence)
- Signatures
- Plain text files
- File types: `.png`, `.jpg`, `.txt`

## Output Format

Provide structured, actionable output:

```markdown
## 📧 Email Analysis

### Basic Information
- From: [sender]
- Subject: [subject]
- Date: [date]
- Thread: [Yes/No, with count if thread]

### 📎 Attachments Found

[List with importance classification]

### 💡 Key Findings
[Extract important information]

### ⚠️ Action Required
[List actionable items with deadlines]

### 📅 Important Dates
[Deadline reminders]
```

## Important Reminders

1. **Always cleanup temporary files** after analysis using `mcp__mail__cleanup_attachments`
2. **Respect user token preferences** - default to quick mode unless otherwise indicated
3. **Provide context** - explain why attachments are classified as important
4. **Track thread history** - help users understand attachment evolution
5. **Be proactive** - suggest auto mode for obviously important emails

## Example Scenarios

### Scenario 1: Tax Notice

User: "Analyze this email from HMRC"

Response:
1. Detect sender = HMRC → High importance
2. Use **auto mode**
3. Extract PDF attachments
4. Identify deadlines and amounts
5. Provide actionable checklist
6. Cleanup files

### Scenario 2: Unknown Email

User: "What's in this email?"

Response:
1. Use **quick mode**
2. List attachments with importance
3. Ask: "Found 1 high-importance PDF. Extract and analyze?"
4. Wait for user confirmation

### Scenario 3: Email Thread

User: "Help me understand this conversation"

Response:
1. Detect thread
2. Show thread timeline
3. Track attachment versions
4. Highlight latest/final versions
5. Summarize key discussion points
