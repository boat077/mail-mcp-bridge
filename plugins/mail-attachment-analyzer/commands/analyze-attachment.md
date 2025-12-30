---
allowed-tools: mcp__mail__read_email, mcp__mail__get_thread_paths, mcp__mail__read_thread, mcp__mail__extract_attachments, mcp__mail__cleanup_attachments
description: Intelligently analyze email attachments with 3 modes (quick/interactive/auto). Optimized for email threads with context tracking.
---

# Email Attachment Analyzer

Intelligently analyze emails and their attachments with tiered processing strategies. Specially optimized for email threads, tracking attachment context and evolution.

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

## Email Thread Handling

### Thread Detection

Use `mcp__mail__get_thread_paths` to check if email is part of conversation thread:

```javascript
// Single email
message_id = "<abc@example.com>"

// Check for thread
thread_paths = get_thread_paths(message_id)
if (thread_paths.length > 1) {
  // This is part of an email thread
}
```

### Attachment Context in Threads

Analyze attachment value within thread context:

**Scenario Examples**:

1. **Draft → Revision → Final**
   ```
   Email 1: contract_v1.pdf
   Email 2: "Updated" → contract_v2.pdf
   Email 3: "Final" → contract_final.pdf ⚠️ Most important
   ```
   Action: Only extract latest version

2. **Supplementary Materials**
   ```
   Email 1: "Issue screenshot" → screenshot.png
   Email 2: "Log file" → logs.txt
   Email 3: "Fix proposal" → fix_proposal.pdf ⚠️ Critical
   ```
   Action: Prioritize solution document, others on-demand

3. **Duplicate Attachments**
   ```
   Email 1: invoice_2024.pdf
   Email 2: RE: ... → invoice_2024.pdf (same file)
   Email 3: RE: ... → invoice_2024.pdf (same file)
   ```
   Action: Analyze only once

### Thread Analysis Output

For email threads, output format:

```markdown
## 📧 Email Thread Analysis

### Thread Information
- Email Count: 3
- Time Span: 2024-01-15 to 2024-01-20
- Participants: Alice, Bob, You

### 📎 Attachment Evolution

1. **contract_v1.pdf** (Email 1 - 2024-01-15)
   - Sender: Alice
   - Size: 1.2MB
   - Importance: ⚠️ Medium (superseded by later version)

2. **contract_v2.pdf** (Email 2 - 2024-01-18)
   - Sender: Bob
   - Size: 1.3MB
   - Importance: ⚠️ Medium (revision)

3. **contract_final.pdf** (Email 3 - 2024-01-20) ⭐
   - Sender: Alice
   - Size: 1.4MB
   - Importance: 🚨 High (final version)
   - Context: Final version after two rounds of revision, requires focus

### 💡 Smart Recommendation
Extract only latest version `contract_final.pdf`, previous versions superseded.
```

## Execution Flow

### Quick Mode

```python
# 1. Read email
email = mcp__mail__read_email(message_id)

# 2. Check for thread
thread_paths = mcp__mail__get_thread_paths(message_id)
is_thread = len(thread_paths) > 1

# 3. Analyze attachment metadata
for attachment in email.attachments:
    importance = judge_importance(attachment)
    print(f"- {attachment.filename} ({attachment.size}) - {importance}")

# 4. If thread, provide context analysis
if is_thread:
    analyze_thread_context(thread_paths)
```

### Interactive Mode

```python
# 1-3. Same as quick mode

# 4. Ask user
print("High-importance attachments found:")
print("[1] contract.pdf - Contract document")
print("[2] invoice.pdf - Invoice")
print("\nExtract these attachments? (enter numbers or 'all')")
```

### Auto Mode

```python
# 1-3. Same as quick mode

# 4. Extract high-importance attachments
high_importance = [a for a in attachments if a.importance == "high"]
filenames = [a.filename for a in high_importance]
extracted = mcp__mail__extract_attachments(message_id, filenames)

# 5. Read and analyze
for file_path in extracted:
    content = read(file_path)
    analyze_content(content)

# 6. Cleanup
mcp__mail__cleanup_attachments([message_id])
```

## Attachment Importance Classification

### 🚨 High Importance
- **Government notices**: HMRC, IRS tax documents
- **Legal documents**: Contracts, agreements, NDAs
- **Financial documents**: Invoices, receipts, bills
- **Certificates**: Certificates, licenses, permits

**File types**: `.pdf`

### ⚠️ Medium Importance
- **Technical docs**: Requirements, design proposals
- **Reports**: Analysis reports, test reports
- **Spreadsheets**: Excel, CSV data
- **Presentations**: PPT, Keynote

**File types**: `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.pages`, `.numbers`

### 💡 Low Importance
- **Images**: Screenshots, photos (unless evidence)
- **Signatures**: Signature files
- **Text**: `.txt`, `.log`
- **Code**: Source code files

**File types**: `.png`, `.jpg`, `.txt`, `.log`

### ❌ Ignore
- **Duplicate files**: Appears multiple times in thread
- **System files**: `.signature`, `.vcf`
- **Outdated versions**: Superseded by new versions

## Output Formats

### Quick Mode Output

```markdown
## 📧 Quick Email Analysis

### Basic Information
- From: HMRC <noreply@hmrc.gov.uk>
- Subject: VAT Return Due Reminder
- Date: 2025-01-15 10:30:00
- Email Thread: No (single email)

### 📎 Attachment Overview
Found 2 attachments:

1. **VAT_Return_Q4_2024.pdf** (245KB)
   - Type: PDF document
   - Importance: 🚨 High
   - Reason: Tax document + PDF format

2. **payment_guide.pdf** (128KB)
   - Type: PDF document
   - Importance: ⚠️ Medium
   - Reason: Reference document

### 💡 Mode Switch Suggestion
Recommend **interactive mode** to view first attachment details.

Command: Try "Analyze this email <message-id> --interactive"
```

### Interactive Mode Output

```markdown
## 📧 Email Analysis (Interactive Mode)

### Basic Information
[... same as quick mode ...]

### 📎 Attachment Analysis

1. **VAT_Return_Q4_2024.pdf** (245KB) 🚨
   - Content Type: Tax return form
   - Key Info Preview: Due date, amount payable
   - Recommendation: ✅ Suggest extraction

2. **payment_guide.pdf** (128KB) ⚠️
   - Content Type: Operation guide
   - Recommendation: 📖 View on-demand

### ❓ Attachment Extraction Choice

Detected 1 high-importance attachment.

**Options**:
- `1` - Extract only VAT_Return_Q4_2024.pdf
- `all` - Extract all attachments
- `skip` - Skip extraction

Please enter option or attachment number:
```

### Auto Mode Output

```markdown
## 📧 Complete Email Analysis

### Basic Information
[... same as quick mode ...]

### 📎 Detailed Attachment Analysis

#### 1. VAT_Return_Q4_2024.pdf 🚨

**Content Summary**:
- Document Type: VAT quarterly return
- Period: 2024 Q4 (Oct-Dec)
- Due Date: **2025-01-31** ⚠️
- Amount Payable: £1,234.56

**Key Information Extracted**:
- Sales: £15,000.00
- Input Tax: £2,500.00
- Output Tax: £3,000.00
- Net Payable: £500.00 + Penalty £734.56

**⚠️ Required Actions**:
1. [ ] **Pay £1,234.56 before 2025-01-31**
2. [ ] Login to HMRC account to confirm
3. [ ] Save payment receipt

**📅 Important Dates**:
- ⚠️ 2025-01-31: Filing deadline
- Late penalty: £10 per day

---

#### 2. payment_guide.pdf ⚠️

**Content Summary**:
- Document Type: Payment operation guide
- Contains: Bank transfer info, online payment steps

**Reference Value**:
Refer to this document if payment method needed.

---

### 🎯 Priority Action List

**Urgent** (within 7 days):
1. [ ] Pay £1,234.56 (deadline: 2025-01-31)

**Important** (within 30 days):
2. [ ] Download and save return copy

**Reference**:
3. [ ] Read payment guide (if needed)

---

✅ **Temporary files cleaned up**
```

## Usage Commands

```bash
# Default: quick mode
Analyze this email <message-id>

# Interactive mode
Analyze this email <message-id> --interactive
Analyze this email <message-id> -i

# Auto mode
Analyze this email <message-id> --auto
Analyze this email <message-id> -a

# Analyze entire thread
Analyze this email <message-id> --thread
Analyze this email <message-id> -t

# Combined usage
Analyze this email <message-id> --auto --thread
```

## Important Notes

1. **Performance Optimization**
   - Quick mode consumes no extra tokens (metadata only)
   - Interactive mode precisely controls which attachments to extract
   - Auto mode suitable for scenarios requiring detailed analysis

2. **Privacy & Security**
   - All extracted attachments auto-cleaned after analysis
   - Temporary files stored in system-configured directory (default `/tmp/mail-mcp-attachments`)
   - `cleanup_attachments` ensures no residual files

3. **Thread Identification**
   - Auto-detect if email belongs to conversation thread
   - For threads, analyze attachment evolution in conversation flow
   - Identify duplicate attachments and version iteration relationships

4. **Token Optimization Recommendations**
   - Daily browsing: Use quick mode
   - Selective viewing: Use interactive mode
   - Important documents: Use auto mode
   - Long threads: Quick mode first to view attachment list, then decide depth
