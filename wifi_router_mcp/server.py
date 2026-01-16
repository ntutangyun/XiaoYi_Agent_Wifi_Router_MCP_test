"""WiFi Router MCP Server - Simulates a home WiFi router."""

import asyncio
import json
import random
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Optional
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    Prompt,
    PromptMessage,
    GetPromptResult,
)
import mcp.server.stdio
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route


# Simulated router state
class RouterState:
    """Simulates the state of a WiFi router."""
    
    def __init__(self):
        self.ssid = "XiaoYi_Home_WiFi"
        self.password = "secure_password_123"
        self.is_on = True
        self.frequency_band = "2.4GHz"  # Can be "2.4GHz", "5GHz", or "dual"
        self.channel = 6
        self.max_devices = 32
        self.security_mode = "WPA3"
        self.guest_network_enabled = False
        self.guest_ssid = "XiaoYi_Guest"
        self.guest_password = "guest123"
        self.firmware_version = "v2.1.4"
        self.uptime_seconds = 432000  # 5 days
        
        # Connected devices
        self.connected_devices = [
            {
                "name": "iPhone 14",
                "mac": "AA:BB:CC:DD:EE:01",
                "ip": "192.168.1.101",
                "connected_time": "2 hours",
                "signal_strength": -45,
            },
            {
                "name": "MacBook Pro",
                "mac": "AA:BB:CC:DD:EE:02",
                "ip": "192.168.1.102",
                "connected_time": "5 hours",
                "signal_strength": -38,
            },
            {
                "name": "Smart TV",
                "mac": "AA:BB:CC:DD:EE:03",
                "ip": "192.168.1.103",
                "connected_time": "5 days",
                "signal_strength": -55,
            },
        ]
        
        # Available networks (for scanning)
        self.available_networks = [
            {
                "ssid": "XiaoYi_Home_WiFi",
                "signal_strength": -30,
                "security": "WPA3",
                "frequency": "2.4GHz",
                "channel": 6,
            },
            {
                "ssid": "Neighbor_WiFi",
                "signal_strength": -70,
                "security": "WPA2",
                "frequency": "2.4GHz",
                "channel": 11,
            },
            {
                "ssid": "CoffeeShop_Public",
                "signal_strength": -85,
                "security": "Open",
                "frequency": "5GHz",
                "channel": 36,
            },
        ]
        
        # Network statistics
        self.network_stats = {
            "download_speed_mbps": 95.3,
            "upload_speed_mbps": 42.1,
            "latency_ms": 12,
            "packets_sent": 15430982,
            "packets_received": 18923451,
            "bytes_sent": "234.5 GB",
            "bytes_received": "1.2 TB",
        }
        
        # Router logs
        self.logs = [
            "[2026-01-16 02:15:33] Device connected: iPhone 14 (192.168.1.101)",
            "[2026-01-16 01:45:22] Firmware update check: Up to date",
            "[2026-01-16 00:30:11] Device disconnected: iPad (192.168.1.105)",
            "[2026-01-15 23:12:45] Channel optimization: Switched to channel 6",
            "[2026-01-15 22:00:00] Daily backup completed",
        ]


# Initialize router state
router_state = RouterState()

# Create MCP server
app = Server("wifi-router-mcp-server")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available router resources."""
    return [
        Resource(
            uri="router://devices",
            name="Connected Devices",
            mimeType="application/json",
            description="List of all devices currently connected to the router",
        ),
        Resource(
            uri="router://stats",
            name="Network Statistics",
            mimeType="application/json",
            description="Current network performance statistics and metrics",
        ),
        Resource(
            uri="router://config",
            name="Router Configuration",
            mimeType="application/json",
            description="Current router configuration including SSID, security, and settings",
        ),
        Resource(
            uri="router://logs",
            name="Router Logs",
            mimeType="text/plain",
            description="Recent router activity logs and events",
        ),
        Resource(
            uri="router://networks",
            name="Available Networks",
            mimeType="application/json",
            description="List of WiFi networks detected by the router",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific router resource."""
    uri_str = str(uri)
    if uri_str == "router://devices":
        return json.dumps({
            "connected_devices": router_state.connected_devices,
            "total_devices": len(router_state.connected_devices),
            "max_devices": router_state.max_devices,
        }, indent=2)
    
    elif uri_str == "router://stats":
        return json.dumps(router_state.network_stats, indent=2)
    
    elif uri_str == "router://config":
        return json.dumps({
            "ssid": router_state.ssid,
            "password": "********",  # Always mask password for security
            "is_on": router_state.is_on,
            "frequency_band": router_state.frequency_band,
            "channel": router_state.channel,
            "security_mode": router_state.security_mode,
            "guest_network_enabled": router_state.guest_network_enabled,
            "guest_ssid": router_state.guest_ssid if router_state.guest_network_enabled else None,
            "guest_password": "********" if router_state.guest_network_enabled else None,
            "firmware_version": router_state.firmware_version,
            "uptime_seconds": router_state.uptime_seconds,
            "uptime_readable": f"{router_state.uptime_seconds // 86400} days, {(router_state.uptime_seconds % 86400) // 3600} hours",
        }, indent=2)
    
    elif uri_str == "router://logs":
        return "\n".join(router_state.logs)
    
    elif uri_str == "router://networks":
        return json.dumps({
            "available_networks": router_state.available_networks,
            "total_networks": len(router_state.available_networks),
        }, indent=2)
    
    else:
        raise ValueError(f"Unknown resource URI: {uri_str}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available router tools."""
    return [
        Tool(
            name="scan_networks",
            description="Scan for available WiFi networks in range",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_router_status",
            description="Get current router status including connection info and system health",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="reboot_router",
            description="Reboot the WiFi router",
            inputSchema={
                "type": "object",
                "properties": {
                    "confirm": {
                        "type": "boolean",
                        "description": "Confirm the reboot action",
                    }
                },
                "required": ["confirm"],
            },
        ),
        Tool(
            name="change_wifi_password",
            description="Change the WiFi network password",
            inputSchema={
                "type": "object",
                "properties": {
                    "new_password": {
                        "type": "string",
                        "description": "New WiFi password (minimum 8 characters)",
                    }
                },
                "required": ["new_password"],
            },
        ),
        Tool(
            name="change_ssid",
            description="Change the WiFi network name (SSID)",
            inputSchema={
                "type": "object",
                "properties": {
                    "new_ssid": {
                        "type": "string",
                        "description": "New WiFi network name",
                    }
                },
                "required": ["new_ssid"],
            },
        ),
        Tool(
            name="enable_guest_network",
            description="Enable or disable guest WiFi network",
            inputSchema={
                "type": "object",
                "properties": {
                    "enabled": {
                        "type": "boolean",
                        "description": "Enable (true) or disable (false) guest network",
                    },
                    "guest_ssid": {
                        "type": "string",
                        "description": "Guest network SSID (optional, only if enabling)",
                    },
                    "guest_password": {
                        "type": "string",
                        "description": "Guest network password (optional, only if enabling)",
                    }
                },
                "required": ["enabled"],
            },
        ),
        Tool(
            name="disconnect_device",
            description="Disconnect a specific device from the network",
            inputSchema={
                "type": "object",
                "properties": {
                    "mac_address": {
                        "type": "string",
                        "description": "MAC address of the device to disconnect",
                    }
                },
                "required": ["mac_address"],
            },
        ),
        Tool(
            name="change_channel",
            description="Change the WiFi channel",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {
                        "type": "integer",
                        "description": "WiFi channel number (1-11 for 2.4GHz, 36-165 for 5GHz)",
                    }
                },
                "required": ["channel"],
            },
        ),
        Tool(
            name="set_frequency_band",
            description="Set the WiFi frequency band",
            inputSchema={
                "type": "object",
                "properties": {
                    "band": {
                        "type": "string",
                        "enum": ["2.4GHz", "5GHz", "dual"],
                        "description": "Frequency band to use",
                    }
                },
                "required": ["band"],
            },
        ),
        Tool(
            name="check_firmware_update",
            description="Check for available firmware updates",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="run_speed_test",
            description="Run an internet speed test",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute a router tool."""
    
    if name == "scan_networks":
        result = {
            "status": "success",
            "networks_found": len(router_state.available_networks),
            "networks": router_state.available_networks,
            "timestamp": datetime.now().isoformat(),
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "get_router_status":
        result = {
            "status": "online",
            "ssid": router_state.ssid,
            "is_on": router_state.is_on,
            "frequency_band": router_state.frequency_band,
            "channel": router_state.channel,
            "security_mode": router_state.security_mode,
            "connected_devices": len(router_state.connected_devices),
            "firmware_version": router_state.firmware_version,
            "uptime": f"{router_state.uptime_seconds // 86400} days, {(router_state.uptime_seconds % 86400) // 3600} hours",
            "guest_network": "enabled" if router_state.guest_network_enabled else "disabled",
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "reboot_router":
        if arguments.get("confirm"):
            router_state.uptime_seconds = 0
            router_state.logs.insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Router rebooted")
            result = {
                "status": "success",
                "message": "Router is rebooting. This will take approximately 2 minutes.",
                "timestamp": datetime.now().isoformat(),
            }
        else:
            result = {
                "status": "cancelled",
                "message": "Reboot cancelled. Set confirm=true to proceed.",
            }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "change_wifi_password":
        new_password = arguments.get("new_password", "")
        if len(new_password) < 8:
            result = {
                "status": "error",
                "message": "Password must be at least 8 characters long",
            }
        else:
            router_state.password = new_password
            router_state.logs.insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WiFi password changed")
            result = {
                "status": "success",
                "message": f"WiFi password updated successfully. All devices will need to reconnect.",
                "new_password_length": len(new_password),
            }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "change_ssid":
        new_ssid = arguments.get("new_ssid", "")
        if not new_ssid:
            result = {
                "status": "error",
                "message": "SSID cannot be empty",
            }
        else:
            old_ssid = router_state.ssid
            router_state.ssid = new_ssid
            router_state.logs.insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SSID changed from '{old_ssid}' to '{new_ssid}'")
            result = {
                "status": "success",
                "message": f"SSID changed from '{old_ssid}' to '{new_ssid}'. All devices will need to reconnect.",
                "new_ssid": new_ssid,
            }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "enable_guest_network":
        enabled = arguments.get("enabled", False)
        router_state.guest_network_enabled = enabled
        
        if enabled:
            if arguments.get("guest_ssid"):
                router_state.guest_ssid = arguments["guest_ssid"]
            if arguments.get("guest_password"):
                router_state.guest_password = arguments["guest_password"]
            
            router_state.logs.insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Guest network enabled: {router_state.guest_ssid}")
            result = {
                "status": "success",
                "message": "Guest network enabled",
                "guest_ssid": router_state.guest_ssid,
                "guest_password_set": True,
                "note": "Password has been set but is not displayed for security. Check router configuration to view masked password.",
            }
        else:
            router_state.logs.insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Guest network disabled")
            result = {
                "status": "success",
                "message": "Guest network disabled",
            }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "disconnect_device":
        mac_address = arguments.get("mac_address", "")
        device = next((d for d in router_state.connected_devices if d["mac"] == mac_address), None)
        
        if device:
            router_state.connected_devices.remove(device)
            router_state.logs.insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Device disconnected: {device['name']} ({mac_address})")
            result = {
                "status": "success",
                "message": f"Device '{device['name']}' disconnected successfully",
                "device": device,
            }
        else:
            result = {
                "status": "error",
                "message": f"Device with MAC address {mac_address} not found",
            }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "change_channel":
        channel = arguments.get("channel")
        if channel:
            old_channel = router_state.channel
            router_state.channel = channel
            router_state.logs.insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Channel changed from {old_channel} to {channel}")
            result = {
                "status": "success",
                "message": f"Channel changed from {old_channel} to {channel}",
                "new_channel": channel,
            }
        else:
            result = {
                "status": "error",
                "message": "Channel number is required",
            }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "set_frequency_band":
        band = arguments.get("band")
        if band in ["2.4GHz", "5GHz", "dual"]:
            old_band = router_state.frequency_band
            router_state.frequency_band = band
            router_state.logs.insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Frequency band changed from {old_band} to {band}")
            result = {
                "status": "success",
                "message": f"Frequency band changed from {old_band} to {band}",
                "new_band": band,
            }
        else:
            result = {
                "status": "error",
                "message": "Invalid band. Must be '2.4GHz', '5GHz', or 'dual'",
            }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "check_firmware_update":
        # Simulate firmware check
        result = {
            "status": "success",
            "current_version": router_state.firmware_version,
            "latest_version": router_state.firmware_version,
            "update_available": False,
            "message": "Your router firmware is up to date",
            "checked_at": datetime.now().isoformat(),
        }
        router_state.logs.insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Firmware update check: Up to date")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "run_speed_test":
        # Simulate speed test with slight variations
        result = {
            "status": "success",
            "download_mbps": round(router_state.network_stats["download_speed_mbps"] + random.uniform(-5, 5), 2),
            "upload_mbps": round(router_state.network_stats["upload_speed_mbps"] + random.uniform(-3, 3), 2),
            "latency_ms": router_state.network_stats["latency_ms"] + random.randint(-2, 2),
            "jitter_ms": random.randint(1, 5),
            "tested_at": datetime.now().isoformat(),
        }
        router_state.logs.insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Speed test completed: {result['download_mbps']} Mbps down, {result['upload_mbps']} Mbps up")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available router prompts."""
    return [
        Prompt(
            name="troubleshoot_connection",
            description="Get help troubleshooting WiFi connection issues",
            arguments=[
                {
                    "name": "issue_type",
                    "description": "Type of issue: slow_speed, no_connection, intermittent, or device_cant_connect",
                    "required": True,
                }
            ],
        ),
        Prompt(
            name="setup_guest_network",
            description="Guide for setting up a guest WiFi network",
            arguments=[],
        ),
        Prompt(
            name="optimize_performance",
            description="Get recommendations for optimizing router performance",
            arguments=[],
        ),
        Prompt(
            name="security_audit",
            description="Perform a security audit and get recommendations",
            arguments=[],
        ),
        Prompt(
            name="parental_controls",
            description="Guide for setting up parental controls and device restrictions",
            arguments=[],
        ),
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
    """Get a specific router prompt."""
    
    if name == "troubleshoot_connection":
        issue_type = arguments.get("issue_type", "no_connection") if arguments else "no_connection"
        
        troubleshooting_steps = {
            "slow_speed": """
## Troubleshooting Slow WiFi Speed

Current router status:
- SSID: {ssid}
- Channel: {channel}
- Frequency: {frequency}
- Connected devices: {devices}

### Recommended Actions:
1. Check if too many devices are connected (current: {devices})
2. Consider switching to 5GHz band for better speed
3. Change channel if there's interference (use scan_networks tool)
4. Run a speed test to measure actual performance
5. Check if any device is consuming excessive bandwidth

### Commands to try:
- Use `run_speed_test` to measure current speed
- Use `scan_networks` to find less crowded channels
- Use `set_frequency_band` to switch to 5GHz if supported
- Use `change_channel` to switch to a less congested channel
            """,
            "no_connection": """
## Troubleshooting No Connection

Current router status:
- Router is: {"ON" if router_state.is_on else "OFF"}
- SSID: {ssid}
- Security: {security}

### Recommended Actions:
1. Verify the router is powered on and all lights are normal
2. Check if the device can see the network (use scan_networks)
3. Verify you're using the correct password
4. Try rebooting the router
5. Check if the device's MAC address is blocked

### Commands to try:
- Use `get_router_status` to check router health
- Use `scan_networks` to verify network is visible
- Use `reboot_router` if other steps don't work
            """,
            "intermittent": """
## Troubleshooting Intermittent Connection

Current router status:
- Channel: {channel}
- Frequency: {frequency}
- Uptime: {uptime}

### Recommended Actions:
1. Check for channel interference from neighboring networks
2. Verify firmware is up to date
3. Check router logs for errors or patterns
4. Consider changing channel or frequency band
5. Check if router needs a reboot (high uptime: {uptime})

### Commands to try:
- Use `scan_networks` to check for interference
- Use `check_firmware_update` to ensure latest firmware
- Read `router://logs` resource to check for errors
- Use `change_channel` if interference is detected
- Use `reboot_router` if uptime is very high
            """,
            "device_cant_connect": """
## Troubleshooting Device Connection Issues

Current router status:
- Connected devices: {devices}/{max_devices}
- Security mode: {security}
- Guest network: {"enabled" if router_state.guest_network_enabled else "disabled"}

### Recommended Actions:
1. Check if device limit is reached (current: {devices}/{max_devices})
2. Verify device supports the security mode (WPA3 may not work on older devices)
3. Try forgetting and re-adding the network on the device
4. Check if MAC filtering is enabled
5. Try connecting to guest network to isolate the issue

### Commands to try:
- Use `get_router_status` to check device count
- Read `router://devices` resource to see connected devices
- Use `enable_guest_network` to create a test network
- Consider temporarily changing security mode if device is old
            """,
        }
        
        template = troubleshooting_steps.get(issue_type, troubleshooting_steps["no_connection"])
        message_text = template.format(
            ssid=router_state.ssid,
            channel=router_state.channel,
            frequency=router_state.frequency_band,
            devices=len(router_state.connected_devices),
            max_devices=router_state.max_devices,
            security=router_state.security_mode,
            uptime=f"{router_state.uptime_seconds // 86400} days",
        )
        
        return GetPromptResult(
            description=f"Troubleshooting guide for {issue_type.replace('_', ' ')}",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=message_text),
                )
            ],
        )
    
    elif name == "setup_guest_network":
        message_text = f"""
## Setting Up Guest WiFi Network

A guest network allows visitors to access the internet without accessing your main network and devices.

### Current Status:
- Main SSID: {router_state.ssid}
- Guest Network: {"Enabled" if router_state.guest_network_enabled else "Disabled"}
- Guest SSID: {router_state.guest_ssid if router_state.guest_network_enabled else "Not set"}

### Steps to Enable:
1. Choose a guest network name (SSID) - something like "{router_state.ssid}_Guest"
2. Set a strong but shareable password
3. Use the `enable_guest_network` tool with enabled=true

### Example Command:
```
enable_guest_network(
    enabled=true,
    guest_ssid="{router_state.guest_ssid}",
    guest_password="your_guest_password"
)
```

### Security Best Practices:
- Use a different password than your main network
- Change the guest password regularly
- Share only with trusted visitors
- Consider disabling when not needed

### To Disable:
Use `enable_guest_network(enabled=false)`
        """
        
        return GetPromptResult(
            description="Guide for setting up guest network",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=message_text),
                )
            ],
        )
    
    elif name == "optimize_performance":
        message_text = f"""
## Router Performance Optimization Guide

### Current Configuration:
- Frequency Band: {router_state.frequency_band}
- Channel: {router_state.channel}
- Connected Devices: {len(router_state.connected_devices)}
- Security Mode: {router_state.security_mode}

### Optimization Recommendations:

#### 1. Choose the Right Frequency Band
- **2.4GHz**: Better range, more interference, slower speed
- **5GHz**: Shorter range, less interference, faster speed
- **Dual Band**: Best of both worlds

Current: {router_state.frequency_band}
Command: `set_frequency_band(band="5GHz")` or `set_frequency_band(band="dual")`

#### 2. Optimize Channel Selection
- Scan for neighboring networks: `scan_networks()`
- Find least congested channel
- Change channel: `change_channel(channel=X)`

Current channel: {router_state.channel}

#### 3. Device Management
- Disconnect unused devices: `disconnect_device(mac_address="XX:XX:XX:XX:XX:XX")`
- Monitor device count: Currently {len(router_state.connected_devices)} devices

#### 4. Regular Maintenance
- Check for firmware updates: `check_firmware_update()`
- Reboot periodically if uptime is high (current: {router_state.uptime_seconds // 86400} days)
- Monitor logs: Read `router://logs` resource

#### 5. Monitor Performance
- Run regular speed tests: `run_speed_test()`
- Check network stats: Read `router://stats` resource

### Quick Actions:
1. Run `scan_networks()` to check interference
2. Run `run_speed_test()` to baseline performance
3. Run `check_firmware_update()` to ensure latest version
        """
        
        return GetPromptResult(
            description="Router performance optimization guide",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=message_text),
                )
            ],
        )
    
    elif name == "security_audit":
        security_score = 0
        recommendations = []
        
        # Check security mode
        if router_state.security_mode == "WPA3":
            security_score += 30
        elif router_state.security_mode == "WPA2":
            security_score += 20
            recommendations.append("Consider upgrading to WPA3 for better security")
        else:
            security_score += 5
            recommendations.append("⚠️ CRITICAL: Upgrade to WPA3 immediately")
        
        # Check password strength
        if len(router_state.password) >= 16:
            security_score += 25
        elif len(router_state.password) >= 12:
            security_score += 20
        elif len(router_state.password) >= 8:
            security_score += 10
            recommendations.append("Use a longer password (16+ characters recommended)")
        else:
            recommendations.append("⚠️ CRITICAL: Password is too short")
        
        # Check SSID
        if "default" in router_state.ssid.lower() or "admin" in router_state.ssid.lower():
            recommendations.append("Change default SSID to something unique")
        else:
            security_score += 15
        
        # Check guest network
        if router_state.guest_network_enabled:
            security_score += 15
            if router_state.guest_password != router_state.password:
                security_score += 15
            else:
                recommendations.append("Use a different password for guest network")
        else:
            recommendations.append("Consider enabling guest network for visitors")
        
        # Firmware
        recommendations.append("Keep firmware updated - check regularly with `check_firmware_update()`")
        
        message_text = f"""
## Security Audit Report

### Overall Security Score: {security_score}/100

### Current Security Settings:
- Security Mode: {router_state.security_mode}
- Password Length: {len(router_state.password)} characters
- SSID: {router_state.ssid}
- Guest Network: {"Enabled" if router_state.guest_network_enabled else "Disabled"}
- Firmware Version: {router_state.firmware_version}

### Recommendations:
"""
        for i, rec in enumerate(recommendations, 1):
            message_text += f"{i}. {rec}\n"
        
        message_text += """

### Security Best Practices:
1. Use WPA3 security mode
2. Use a strong, unique password (16+ characters)
3. Change passwords regularly (every 3-6 months)
4. Enable guest network for visitors
5. Keep firmware updated
6. Monitor connected devices regularly
7. Disable WPS if available
8. Change default admin credentials

### Commands for Security:
- `change_wifi_password(new_password="your_strong_password")`
- `enable_guest_network(enabled=true, guest_ssid="Guest", guest_password="guest_pass")`
- `check_firmware_update()`
- Read `router://devices` to monitor connected devices
- Read `router://logs` to check for suspicious activity
        """
        
        return GetPromptResult(
            description="Security audit report with recommendations",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=message_text),
                )
            ],
        )
    
    elif name == "parental_controls":
        message_text = f"""
## Parental Controls and Device Management Guide

### Current Device Count: {len(router_state.connected_devices)}

### Connected Devices:
"""
        for device in router_state.connected_devices:
            message_text += f"- {device['name']} ({device['mac']}) - {device['ip']}\n"
        
        message_text += """

### Available Controls:

#### 1. Device Disconnection
Disconnect specific devices from the network:
- Command: `disconnect_device(mac_address="XX:XX:XX:XX:XX:XX")`
- Use case: Enforce screen time limits, bedtime rules

#### 2. Guest Network for Kids
Create a separate network with controlled access:
- Command: `enable_guest_network(enabled=true, guest_ssid="Kids_WiFi", guest_password="kids123")`
- Benefits: Easier to disable, separate from main network

#### 3. Schedule-Based Access
Manage when devices can connect:
- Monitor connections via `router://devices` resource
- Disconnect devices during restricted hours
- Re-enable during allowed hours

#### 4. Device Monitoring
Keep track of device usage:
- Read `router://devices` to see all connected devices
- Read `router://logs` to see connection/disconnection history
- Read `router://stats` to monitor bandwidth usage

### Example Workflow:

**Set up kids' network:**
```
1. enable_guest_network(enabled=true, guest_ssid="Kids_WiFi", guest_password="kids_password")
2. Connect kids' devices to guest network
3. Disable guest network during homework/bedtime: enable_guest_network(enabled=false)
4. Re-enable when appropriate: enable_guest_network(enabled=true)
```

**Enforce device limits:**
```
1. Check connected devices: Read router://devices
2. Identify device to restrict: Find MAC address
3. Disconnect device: disconnect_device(mac_address="XX:XX:XX:XX:XX:XX")
```

### Best Practices:
1. Communicate rules clearly with family members
2. Use guest network for better control
3. Regular check-ins on device usage
4. Balance restriction with trust
5. Lead by example with your own device usage

### Commands Reference:
- `enable_guest_network()` - Manage guest/kids network
- `disconnect_device()` - Remove device from network
- Read `router://devices` - Monitor all devices
- Read `router://logs` - Track activity
        """
        
        return GetPromptResult(
            description="Guide for parental controls and device management",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=message_text),
                )
            ],
        )
    
    else:
        raise ValueError(f"Unknown prompt: {name}")


async def main():
    """Main entry point for the WiFi router MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def create_streamable_http_app() -> Starlette:
    """Create a Starlette app that serves MCP over Streamable HTTP."""
    session_manager = StreamableHTTPSessionManager(app)

    async def streamable_http_asgi(scope, receive, send) -> None:
        await session_manager.handle_request(scope, receive, send)

    async def health_check(_request):
        return JSONResponse({"status": "ok"})

    @asynccontextmanager
    async def lifespan(_app: Starlette):
        async with session_manager.run():
            yield

    app_instance = Starlette(
        routes=[
            Mount("/sse", app=streamable_http_asgi),
            Route("/health", endpoint=health_check, methods=["GET"]),
        ],
        lifespan=lifespan,
    )

    app_instance.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app_instance


if __name__ == "__main__":
    asyncio.run(main())
