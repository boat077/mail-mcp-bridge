# Mail Attachment Analyzer

Claude Code plugin for intelligent email attachment analysis. Works with [Mail MCP](../../README.md) server.

## Features

- **3 Analysis Modes**: Quick (metadata only), Interactive (user-controlled), Auto (full analysis)
- **Thread Detection**: Track attachment evolution across email conversations
- **Smart Classification**: Automatically identify important documents (invoices, contracts, tax notices)
- **Version Tracking**: Detect iterations (draft → v1 → v2 → final)
- **Action Extraction**: Pull out deadlines, amounts, and required actions

## Installation

### Prerequisites

1. Mail MCP server must be installed and running (see [main README](../../README.md))

### Install Plugin

```bash
# Navigate to mail-mcp repository root
cd ~/mail-mcp

# Add marketplace
/plugin marketplace add ~/mail-mcp/plugins

# Install plugin
/plugin install mail-attachment-analyzer@mail-mcp
```

Restart Claude Code after installation.

## Usage

### Two Ways to Use

#### 1. Auto-Triggered (Skill Mode)

AI automatically uses this skill when you:

```
Analyze this email <message-id>
What attachments are in this email?
Help me review this email thread
```

#### 2. Manual Command

Explicitly invoke with:

```
/mail-mcp:analyze-attachment
```

### Mode Parameters

Add mode hints in your natural language request:

- **Quick mode**: "Quickly check this email"
- **Interactive mode**: "Help me review this email" (asks for confirmation)
- **Auto mode**: "Fully analyze this HMRC email" (auto-extracts important attachments)
- **Thread mode**: "Analyze this email conversation"

## Examples

### Example 1: Tax Notice

```
Input: Analyze this HMRC email <abc@hmrc.gov.uk>

Output:
📧 Email Analysis
- From: HMRC <noreply@hmrc.gov.uk>
- Subject: VAT Return Due
- Attachments: VAT_Return_Q4_2024.pdf (245KB) 🚨 High

📎 Attachment Analysis
- Type: VAT quarterly return
- Due Date: 2025-01-31 ⚠️
- Amount: £1,234.56

⚠️ Action Required:
1. [ ] Pay £1,234.56 before 2025-01-31
2. [ ] Login to HMRC to confirm
```

### Example 2: Email Thread

```
Input: Help me understand this contract discussion <xyz@company.com>

Output:
📧 Email Thread (4 emails, 2025-01-10 to 01-15)

📎 Attachment Evolution:
1. contract_draft.pdf (Email 1) - ⚠️ Superseded
2. contract_v2.pdf (Email 2) - ⚠️ Revision
3. contract_final.pdf (Email 3) - ⭐ Latest

💡 Recommendation:
Extract only contract_final.pdf (final version after 2 revisions)
```

## How It Works

### With Mail MCP Server

```
User Request
    ↓
Plugin (analyze-attachment command/skill)
    ↓
Mail MCP Tools (mcp__mail__*)
    ↓
- mcp__mail__read_email
- mcp__mail__get_thread_paths
- mcp__mail__extract_attachments
- mcp__mail__cleanup_attachments
    ↓
Structured Analysis Report
```

### Attachment Importance

**High 🚨**:
- PDFs from government (HMRC, IRS)
- Invoices, contracts, legal docs
- Keywords: tax, invoice, contract, urgent

**Medium ⚠️**:
- Technical docs, reports
- Spreadsheets, presentations

**Low 💡**:
- Images, signatures, text files

## Configuration

No additional configuration needed. The plugin automatically uses Mail MCP tools when available.

### Required MCP Tools

The plugin requires these tools from Mail MCP:
- `mcp__mail__read_email`
- `mcp__mail__get_thread_paths`
- `mcp__mail__read_thread`
- `mcp__mail__extract_attachments`
- `mcp__mail__cleanup_attachments`

If Mail MCP is not running, the plugin will not function.

## Development

### File Structure

```
mail-attachment-analyzer/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── analyze-attachment.md    # Manual command
├── skills/
│   └── attachment-analyzer/
│       └── SKILL.md             # Auto-triggered skill
└── README.md
```

### Updating

Since this is a local plugin:

```bash
# Make changes to files
vim commands/analyze-attachment.md

# Reinstall to apply changes
/plugin uninstall mail-attachment-analyzer@mail-mcp
/plugin install mail-attachment-analyzer@mail-mcp

# Restart Claude Code
```

Changes are immediate - no need to restart Mail MCP server.

## Troubleshooting

### Plugin Not Working

1. **Check Mail MCP is running**:
   ```bash
   ps aux | grep mail-mcp
   ```

2. **Verify plugin installation**:
   ```bash
   /plugin list
   # Should show: mail-attachment-analyzer@mail-mcp
   ```

3. **Check MCP tools available**:
   Ask Claude: "What MCP tools do you have access to?"
   Should include `mcp__mail__*` tools

### Attachment Extraction Fails

- Ensure temporary directory exists: `/tmp/mail-mcp-attachments/`
- Check disk space
- Verify attachment file permissions

## License

© 2025 Fatbobman. Part of Mail MCP project.
