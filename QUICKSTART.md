# Quick Start Guide - WiFi Router MCP Server

This guide will help you quickly get the WiFi Router MCP Server up and running.

## Installation (2 minutes)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ntutangyun/XiaoYi_Agent_Wifi_Router_MCP_test.git
   cd XiaoYi_Agent_Wifi_Router_MCP_test
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python test_server.py
   ```
   
   You should see:
   ```
   ✅ All basic tests passed!
   🎉 WiFi Router MCP Server is ready!
   ```

## Testing with MCP Inspector (5 minutes)

The fastest way to explore the server's capabilities (stdio transport):

```bash
npx @modelcontextprotocol/inspector python run_server.py
```

This opens a web interface where you can:
- Browse all 11 tools, 5 resources, and 5 prompts
- Execute tools interactively
- View resources in real-time
- Test prompts with different parameters

### Using Streamable HTTP

If you want to use the Streamable HTTP transport, start the server like this:

```bash
python run_server.py --transport streamable-http --host 127.0.0.1 --port 3001
```

Then connect MCP Inspector to `http://localhost:3001/sse`.

### Try These Examples:

1. **Get Router Status:**
   - Tool: `get_router_status`
   - Arguments: `{}`
   
2. **Scan Networks:**
   - Tool: `scan_networks`
   - Arguments: `{}`
   
3. **View Connected Devices:**
   - Resource: `router://devices`
   
4. **Security Audit:**
   - Prompt: `security_audit`
   - Arguments: None

## Integration with Claude Desktop (5 minutes)

1. **Locate Claude config file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add server configuration:**
   ```json
   {
     "mcpServers": {
       "wifi-router": {
         "command": "python",
         "args": ["/absolute/path/to/XiaoYi_Agent_Wifi_Router_MCP_test/run_server.py"]
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Test it:**
   - Open Claude Desktop
   - Look for the 🔌 icon indicating MCP servers are connected
   - Try: "What's the status of my WiFi router?"

## Integration with Cline (VSCode)

1. **Open Cline settings in VSCode**
2. **Add MCP server:**
   ```json
   {
     "mcpServers": {
       "wifi-router": {
         "command": "python",
         "args": ["/absolute/path/to/XiaoYi_Agent_Wifi_Router_MCP_test/run_server.py"]
       }
     }
   }
   ```
3. **Reload VSCode**
4. **Test with Cline:** "Check my WiFi router status"

## Quick Test Commands

Once connected, try these commands with your LLM agent:

### Basic Status
```
"What's the current status of my WiFi router?"
"How many devices are connected to my WiFi?"
"What's my current internet speed?"
```

### Troubleshooting
```
"My internet is slow, help me troubleshoot"
"I can't connect to WiFi, what should I check?"
"My connection keeps dropping, what's wrong?"
```

### Configuration
```
"Change my WiFi password to: MyNewSecurePassword123"
"Enable a guest network called Guest_WiFi"
"Switch to 5GHz frequency"
```

### Security
```
"Is my WiFi network secure?"
"Show me all connected devices"
"Disconnect the device with MAC AA:BB:CC:DD:EE:01"
```

### Performance
```
"Run a speed test"
"Optimize my router for gaming"
"Find the best WiFi channel"
```

## Common Issues & Solutions

### Issue: "mcp module not found"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Command 'python' not found"
**Solution:** Use `python3` instead
```bash
python3 run_server.py
```

### Issue: Server not showing in Claude/Cline
**Solution:** 
1. Check the absolute path in config is correct
2. Restart the client application
3. Check server logs for errors

### Issue: Tools not working
**Solution:** 
1. Run `python test_server.py` to verify installation
2. Check if `mcp` package is properly installed
3. Make sure Python 3.10+ is being used

## Next Steps

1. **Read USAGE_EXAMPLES.py** - See 10 detailed scenarios showing how agents interact with the server

2. **Check README.md** - Full documentation of all features

3. **Experiment** - Try different commands and scenarios with your LLM agent

4. **Customize** - Modify `wifi_router_mcp/server.py` to add your own features

## Support

- Open an issue on GitHub
- Check the README.md for detailed documentation
- Run `python test_server.py` to diagnose issues

---

**You're ready to go! 🚀**

Try asking your LLM agent: *"What can you tell me about my WiFi router?"*
