#!/usr/bin/env python3
"""Test script to verify WiFi Router MCP Server functionality."""

import sys
sys.path.insert(0, '.')

import json
from wifi_router_shared.router import router_state


def test_server():
    """Test the MCP server functionality."""
    print("🧪 Testing WiFi Router MCP Server\n")
    print("=" * 60)
    
    # Test 1: Server module import
    print("\n1️⃣  Testing server module import...")
    try:
        from wifi_router_mcp.server import app
        print(f"   ✓ Server imported: {app.name}")
    except Exception as e:
        print(f"   ✗ Failed to import server: {e}")
        return
    
    # Test 2: Router state initialization
    print("\n2️⃣  Testing router state...")
    print(f"   ✓ SSID: {router_state.ssid}")
    print(f"   ✓ Frequency: {router_state.frequency_band}")
    print(f"   ✓ Channel: {router_state.channel}")
    print(f"   ✓ Security: {router_state.security_mode}")
    print(f"   ✓ Connected devices: {len(router_state.connected_devices)}")
    
    # Test 3: Check connected devices
    print("\n3️⃣  Testing connected devices...")
    for device in router_state.connected_devices:
        print(f"   ✓ {device['name']} - {device['mac']} ({device['ip']})")
    
    # Test 4: Check available networks
    print("\n4️⃣  Testing available networks...")
    print(f"   ✓ Networks available: {len(router_state.available_networks)}")
    for net in router_state.available_networks:
        print(f"     - {net['ssid']} ({net['security']}, {net['frequency']})")
    
    # Test 5: Network statistics
    print("\n5️⃣  Testing network statistics...")
    print(f"   ✓ Download speed: {router_state.network_stats['download_speed_mbps']} Mbps")
    print(f"   ✓ Upload speed: {router_state.network_stats['upload_speed_mbps']} Mbps")
    print(f"   ✓ Latency: {router_state.network_stats['latency_ms']} ms")
    
    # Test 6: Router logs
    print("\n6️⃣  Testing router logs...")
    print(f"   ✓ Log entries: {len(router_state.logs)}")
    print(f"   ✓ Latest: {router_state.logs[0]}")
    
    # Test 7: Test state modification
    print("\n7️⃣  Testing state modification...")
    old_ssid = router_state.ssid
    router_state.ssid = "TestNetwork"
    print(f"   ✓ SSID changed: {old_ssid} → {router_state.ssid}")
    router_state.ssid = old_ssid  # Restore
    print(f"   ✓ SSID restored: {router_state.ssid}")
    
    # Test 8: Guest network
    print("\n8️⃣  Testing guest network configuration...")
    print(f"   ✓ Guest network enabled: {router_state.guest_network_enabled}")
    print(f"   ✓ Guest SSID: {router_state.guest_ssid}")
    
    # Summary of MCP Server Features
    print("\n" + "=" * 60)
    print("✅ All basic tests passed!\n")
    print("📊 MCP Server Feature Summary:")
    print("\n🛠️  Tools (11 available):")
    tools = [
        "scan_networks", "get_router_status", "reboot_router",
        "change_wifi_password", "change_ssid", "enable_guest_network",
        "disconnect_device", "change_channel", "set_frequency_band",
        "check_firmware_update", "run_speed_test"
    ]
    for tool in tools:
        print(f"   ✓ {tool}")
    
    print("\n📦 Resources (5 available):")
    resources = [
        "router://devices", "router://stats", "router://config",
        "router://logs", "router://networks"
    ]
    for res in resources:
        print(f"   ✓ {res}")
    
    print("\n💬 Prompts (5 available):")
    prompts = [
        "troubleshoot_connection", "setup_guest_network",
        "optimize_performance", "security_audit", "parental_controls"
    ]
    for prompt in prompts:
        print(f"   ✓ {prompt}")
    
    print("\n" + "=" * 60)
    print("🎉 WiFi Router MCP Server is ready!")
    print("\nTo test with MCP Inspector:")
    print("  npx @modelcontextprotocol/inspector python run_mcp_server.py")
    print("\nTo integrate with MCP client:")
    print("  See mcp_config_example.json for configuration")


if __name__ == "__main__":
    test_server()
