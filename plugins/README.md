# Mail MCP Plugins

Claude Code plugins for [Mail MCP](../README.md) - Email processing and analysis tools.

## About

This marketplace contains Claude Code plugins that work with Mail MCP server to provide intelligent email analysis capabilities.

## Available Plugins

### 1. Mail Attachment Analyzer

Intelligently analyze email attachments with automatic importance classification and thread tracking.

**Features**:
- 3 analysis modes (quick/interactive/auto)
- Email thread detection and version tracking
- Smart document classification (invoices, contracts, tax docs)
- Action item extraction with deadlines
- Automatic cleanup

[View Details →](mail-attachment-analyzer/README.md)

## Installation

### Prerequisites

Mail MCP server must be installed and running. See [main README](../README.md) for setup instructions.

### Install Plugins

```bash
# 1. Navigate to mail-mcp repository
cd ~/mail-mcp

# 2. Add this marketplace
/plugin marketplace add ~/mail-mcp/plugins

# 3. Install plugins
/plugin install mail-attachment-analyzer@mail-mcp

# 4. Restart Claude Code
```

## Usage

After installation, plugins work in two ways:

### Auto-Triggered (Skills)

AI automatically uses plugins when appropriate:

```
Analyze this email <message-id>
What's in this email?
Help me review this thread
```

### Manual Commands

Explicitly invoke with:

```
/mail-mcp:analyze-attachment
```

## How It Works

```
Claude Code Plugin
       ↓
  Mail MCP Server (must be running)
       ↓
  macOS Mail.app
       ↓
  Email Data
```

**Important**: Plugins are lightweight (just Markdown files). The actual email processing is done by Mail MCP server, which must be running locally.

## Plugin Development

### Structure

```
plugins/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace config
├── mail-attachment-analyzer/     # Plugin 1
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── commands/                 # Manual commands
│   ├── skills/                   # Auto-triggered skills
│   └── README.md
└── README.md                     # This file
```

### Adding New Plugins

1. Create plugin directory:
   ```bash
   mkdir -p plugins/my-plugin/{.claude-plugin,commands,skills}
   ```

2. Create `plugin.json`:
   ```json
   {
     "name": "my-plugin",
     "description": "Plugin description",
     "version": "1.0.0",
     "author": {"name": "Your Name"}
   }
   ```

3. Add command or skill (`.md` files)

4. Register in `marketplace.json`:
   ```json
   {
     "plugins": [
       {
         "name": "my-plugin",
         "source": "./my-plugin",
         "description": "...",
         "version": "1.0.0"
       }
     ]
   }
   ```

5. Test:
   ```bash
   /plugin uninstall my-plugin@mail-mcp
   /plugin install my-plugin@mail-mcp
   ```

### Testing

Since plugins are local:

1. Edit plugin files
2. Reinstall: `/plugin uninstall ... && /plugin install ...`
3. Restart Claude Code
4. Test functionality

Changes take effect immediately - no need to restart Mail MCP server.

## Updating

### Update Plugins

```bash
# 1. Pull latest code
cd ~/mail-mcp
git pull

# 2. Reinstall plugins
/plugin uninstall mail-attachment-analyzer@mail-mcp
/plugin install mail-attachment-analyzer@mail-mcp

# 3. Restart Claude Code
```

### Update Mail MCP Server

```bash
cd ~/mail-mcp
git pull
pip install -r requirements.txt
# Restart server
```

## Troubleshooting

### Plugins Not Working

1. **Check Mail MCP server is running**:
   ```bash
   ps aux | grep mail
   ```

2. **Verify MCP tools available**:
   Ask Claude: "What MCP tools do you have?"
   Should see `mcp__mail__*` tools

3. **Check plugin installation**:
   ```bash
   /plugin list
   # Should show mail-attachment-analyzer@mail-mcp
   ```

### Common Issues

**"Tool not found" error**:
- Mail MCP server not running
- Check `.claude/settings.json` has correct MCP configuration

**Plugin command not appearing**:
- Restart Claude Code after installation
- Check plugin.json format
- Verify marketplace.json includes the plugin

**Attachment extraction fails**:
- Check `/tmp/mail-mcp-attachments/` directory exists
- Verify disk space
- Check file permissions

## Contributing

Contributions welcome! To add a new plugin:

1. Fork the repository
2. Create plugin in `plugins/` directory
3. Update `marketplace.json`
4. Test locally
5. Submit pull request

## License

© 2025 Fatbobman. Part of Mail MCP project.
