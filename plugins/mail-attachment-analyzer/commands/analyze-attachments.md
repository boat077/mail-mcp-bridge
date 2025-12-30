---
skill: analyze-attachments
---

# Analyze Attachments

Deep attachment analysis with extraction, importance classification, and content analysis.

**Use when**: You need to extract and view email attachments, analyze document content, or identify important files.

**What it does**:

- Lists all attachments with metadata
- Classifies by importance (High/Medium/Low)
- Extracts selected files
- Analyzes document content
- Identifies deadlines and action items
- Auto-cleans temporary files

**Operation modes**:

- Quick Mode: Lists attachments without extracting
- Interactive Mode: Asks which files to extract
- Auto Mode: Auto-extracts high-importance files (invoices, contracts, tax docs)

**Example**:

```text
User: /analyze-attachments
AI: Please provide the email Message-ID
User: <msg@example.com>
AI: Found 3 attachments:
   1. invoice.pdf (High importance)
   2. report.docx (Medium importance)
   3. screenshot.png (Low importance)
   Would you like to extract the invoice?
```

**Features**:

- Detects high-importance files automatically
- Extracts key information (dates, amounts, deadlines)
- Cleans up temporary files after analysis

**Related commands**:

- `/analyze-email` - For single email analysis
- `/analyze-thread` - For complete thread analysis
