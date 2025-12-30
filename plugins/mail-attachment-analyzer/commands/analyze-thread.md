---
skill: analyze-thread
---

# Analyze Email Thread

Comprehensive analysis of an email thread including conversation flow, timeline, participants, and key points.

**Use when**: You need to understand complete conversation context or track discussion progression.

**What it does**:

- Reads all emails in the thread
- Shows conversation timeline
- Identifies participants and their roles
- Extracts key decisions and action items
- Tracks attachment evolution
- Handles large threads intelligently

**Features**:

- Smart quote stripping reduces token usage by ~80%
- Detects and warns about truncated emails
- Suggests reading important emails individually if needed

**Example**:

```text
User: /analyze-thread
AI: Please provide any Message-ID from the thread
User: <msg@example.com>
AI: [Shows full thread analysis with timeline and key points]
```

**Related commands**:

- `/analyze-email` - For single email analysis
- `/analyze-attachments` - For deep attachment analysis
