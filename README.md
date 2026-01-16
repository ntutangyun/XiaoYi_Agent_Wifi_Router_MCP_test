# WiFi Router MCP Server

A Model Context Protocol (MCP) server that simulates a home WiFi router, providing tools, resources, and prompts for testing LLM agents in a home networking context.

## Features

### 🛠️ Tools (11 available)
The server exposes various tools for managing the simulated WiFi router:

- **scan_networks** - Scan for available WiFi networks in range
- **get_router_status** - Get current router status and system health
- **reboot_router** - Reboot the WiFi router
- **change_wifi_password** - Change the WiFi network password
- **change_ssid** - Change the WiFi network name (SSID)
- **enable_guest_network** - Enable/disable guest WiFi network
- **disconnect_device** - Disconnect a specific device from the network
- **change_channel** - Change the WiFi channel
- **set_frequency_band** - Set the WiFi frequency band (2.4GHz, 5GHz, or dual)
- **check_firmware_update** - Check for available firmware updates
- **run_speed_test** - Run an internet speed test

### 📦 Resources (5 available)
Access router information through resources:

- **router://devices** - List of all connected devices
- **router://stats** - Network performance statistics and metrics
- **router://config** - Current router configuration
- **router://logs** - Recent router activity logs
- **router://networks** - List of detected WiFi networks

### 💬 Prompts (5 available)
Interactive guides and troubleshooting assistance:

- **troubleshoot_connection** - Help with connection issues (slow speed, no connection, intermittent, device can't connect)
- **setup_guest_network** - Guide for setting up guest WiFi
- **optimize_performance** - Recommendations for router optimization
- **security_audit** - Security audit with recommendations
- **parental_controls** - Guide for device management and restrictions

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ntutangyun/XiaoYi_Agent_Wifi_Router_MCP_test.git
cd XiaoYi_Agent_Wifi_Router_MCP_test
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

Start the MCP server using stdio transport:

```bash
python run_server.py
```

Or run the module directly:

```bash
python -m wifi_router_mcp.server
```

Start the MCP server using Streamable HTTP transport (for MCP Inspector or HTTP clients) in a separate terminal:

```bash
python run_server.py --transport streamable-http --host 127.0.0.1 --port 3001
```

Point your MCP client to `http://localhost:3001/sse`.

### Testing with MCP Inspector

You can test the server using the MCP Inspector tool (stdio transport):

```bash
npx @modelcontextprotocol/inspector python run_server.py
```

This will open a web interface where you can:
- Browse available tools, resources, and prompts
- Execute tool calls with different parameters
- Read resources to see router state
- Test prompts with various arguments

To use Streamable HTTP, start the server with `--transport streamable-http` in one terminal
and open MCP Inspector separately (no server command). Then connect the Inspector to
`http://localhost:3001/sse`.

### Integrating with LLM Agents

Add this server to your MCP client configuration (e.g., Claude Desktop, Cline):

```json
{
  "mcpServers": {
    "wifi-router": {
      "command": "python",
      "args": ["/path/to/XiaoYi_Agent_Wifi_Router_MCP_test/run_server.py"]
    }
  }
}
```

## Example Usage Scenarios

### Scenario 1: Check Router Status
```
Agent: "What's the current status of my WiFi router?"
→ Calls: get_router_status()
→ Result: Shows SSID, connected devices, uptime, firmware version, etc.
```

### Scenario 2: Troubleshoot Slow Internet
```
Agent: "My internet is slow, what should I do?"
→ Uses prompt: troubleshoot_connection(issue_type="slow_speed")
→ Provides: Step-by-step troubleshooting guide
→ Suggests: Run speed test, check channel interference, switch to 5GHz
```

### Scenario 3: Set Up Guest Network
```
Agent: "I need to set up a guest WiFi network for visitors"
→ Uses prompt: setup_guest_network()
→ Provides: Configuration guide
→ Calls: enable_guest_network(enabled=true, guest_ssid="Guest_WiFi", guest_password="guest123")
→ Result: Guest network enabled
```

### Scenario 4: Security Audit
```
Agent: "Is my WiFi network secure?"
→ Uses prompt: security_audit()
→ Analyzes: Security mode, password strength, SSID, guest network
→ Provides: Security score and recommendations
```

### Scenario 5: Disconnect Unauthorized Device
```
Agent: "There's an unknown device connected. MAC: AA:BB:CC:DD:EE:01"
→ First reads: router://devices (to verify)
→ Calls: disconnect_device(mac_address="AA:BB:CC:DD:EE:01")
→ Result: Device disconnected
```

## Router State

The server maintains a simulated router state including:

- **Network Configuration**: SSID, password, frequency band, channel, security mode
- **Connected Devices**: List of devices with MAC addresses, IPs, signal strength
- **Network Statistics**: Download/upload speeds, latency, packet counts
- **System Information**: Firmware version, uptime, logs
- **Guest Network**: Separate SSID and password for visitors

All state changes (password changes, reboots, device disconnections) are logged and reflected in subsequent queries.

## Development

### Project Structure
```
XiaoYi_Agent_Wifi_Router_MCP_test/
├── wifi_router_mcp/
│   ├── __init__.py
│   └── server.py          # Main MCP server implementation
├── run_server.py          # Entry point script
├── pyproject.toml         # Project metadata
├── requirements.txt       # Dependencies
└── README.md             # This file
```

### Testing

The server can be tested interactively using MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python run_server.py
```

Or integrate with any MCP-compatible client to test the full functionality.

## Requirements

- Python 3.10 or higher
- mcp >= 1.0.0

## License

This project is provided as-is for testing and development purposes.

## Contributing

Feel free to open issues or submit pull requests to enhance the WiFi router simulation or add new features!
