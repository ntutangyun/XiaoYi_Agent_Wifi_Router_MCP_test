"""
Example Usage Scenarios for WiFi Router MCP Server

This file demonstrates how an LLM agent would interact with the 
WiFi Router MCP server in various scenarios.
"""

# =============================================================================
# SCENARIO 1: Check Router Status
# =============================================================================
"""
User: "What's the current status of my WiFi router?"

Agent Action:
1. Calls tool: get_router_status()

Agent Response:
"Your router is online and functioning properly:
- Network Name (SSID): XiaoYi_Home_WiFi
- Frequency: 2.4GHz on channel 6
- Security: WPA3
- Connected Devices: 3
- Uptime: 5 days, 0 hours
- Firmware: v2.1.4
- Guest Network: Disabled

Everything looks good! Your router has been running for 5 days without issues."
"""

# =============================================================================
# SCENARIO 2: Troubleshoot Slow Internet
# =============================================================================
"""
User: "My internet is really slow today. What should I check?"

Agent Action:
1. Uses prompt: troubleshoot_connection(issue_type="slow_speed")
2. Calls tool: run_speed_test()
3. Calls tool: scan_networks()
4. Reads resource: router://devices

Agent Response:
"I've run some diagnostics on your network. Here's what I found:

Speed Test Results:
- Download: 92.4 Mbps
- Upload: 40.8 Mbps
- Latency: 14 ms

Your speeds are good but slightly below your usual 95 Mbps. I noticed:
1. You have 3 devices connected, which is normal
2. Channel 6 is showing moderate interference from 2 neighboring networks
3. You're currently on 2.4GHz which has more range but slower speeds

Recommendations:
1. Switch to 5GHz band for faster speeds (if your devices support it)
2. Try changing to channel 1 or 11 to avoid interference
3. Check if any device is streaming/downloading heavily

Would you like me to switch to 5GHz or change the channel?"
"""

# =============================================================================
# SCENARIO 3: Set Up Guest Network for Party
# =============================================================================
"""
User: "I'm having a party this weekend. Can you set up a guest WiFi network?"

Agent Action:
1. Uses prompt: setup_guest_network()
2. Calls tool: enable_guest_network(enabled=true, guest_ssid="Party_WiFi", 
                                    guest_password="Welcome2023")

Agent Response:
"Perfect! I've set up a guest network for your party:

Guest Network Details:
- Network Name: Party_WiFi
- Password: Welcome2023
- Status: Active

Your guests can connect to 'Party_WiFi' using the password above. This keeps 
them separate from your main network, so they can't access your personal devices 
or files. The guest network has internet access only.

After the party, I can disable the guest network for you. Just let me know!"
"""

# =============================================================================
# SCENARIO 4: Security Audit
# =============================================================================
"""
User: "Is my WiFi secure? I'm worried about hackers."

Agent Action:
1. Uses prompt: security_audit()
2. Reads resource: router://config
3. Reads resource: router://devices

Agent Response:
"I've performed a security audit of your network. Here's your security report:

Overall Security Score: 85/100 ✅

Strengths:
✓ Using WPA3 (latest security standard)
✓ Unique SSID (not using default name)
✓ Good password length (15 characters)
✓ Firmware is up to date (v2.1.4)

Recommendations:
1. Enable guest network for visitors (currently disabled)
2. Consider changing your password every 3-6 months
3. Monitor connected devices regularly for unknown devices

Current Connected Devices:
✓ iPhone 14 (192.168.1.101)
✓ MacBook Pro (192.168.1.102)
✓ Smart TV (192.168.1.103)

All devices appear to be yours. Your network is well-secured! The main 
improvement would be enabling a guest network so visitors don't need your 
main password."
"""

# =============================================================================
# SCENARIO 5: Remove Unknown Device
# =============================================================================
"""
User: "There's a device called 'Unknown-Device' connected that I don't recognize. 
      Its MAC address is AA:BB:CC:DD:EE:04"

Agent Action:
1. Reads resource: router://devices (to confirm device exists)
2. Calls tool: disconnect_device(mac_address="AA:BB:CC:DD:EE:04")
3. Recommends: change_wifi_password()

Agent Response:
"I've immediately disconnected the unknown device (AA:BB:CC:DD:EE:04) from 
your network.

For additional security, I recommend changing your WiFi password since 
someone may have gained unauthorized access. This will disconnect all 
devices, and you'll need to reconnect your legitimate devices with the 
new password.

Would you like me to change your WiFi password now? If yes, please provide 
a new strong password (at least 12 characters, mix of letters, numbers, 
and symbols)."
"""

# =============================================================================
# SCENARIO 6: Optimize for Gaming
# =============================================================================
"""
User: "I'm getting lag in my online games. Can you optimize my router?"

Agent Action:
1. Uses prompt: optimize_performance()
2. Calls tool: scan_networks()
3. Calls tool: set_frequency_band(band="5GHz")
4. Calls tool: change_channel(channel=36)

Agent Response:
"I've optimized your router for gaming. Here's what I changed:

Changes Made:
1. ✓ Switched from 2.4GHz to 5GHz band (lower latency, faster speeds)
2. ✓ Changed to channel 36 (no interference detected)
3. ✓ Verified firmware is up to date

Expected Improvements:
- Lower latency (typically 5-10ms better)
- More stable connection (less interference)
- Higher bandwidth (better for downloads/streaming)

Note: 5GHz has shorter range than 2.4GHz. If you're far from the router, 
you might need to move closer or use a WiFi extender.

Try your game now and let me know if the lag improves!"
"""

# =============================================================================
# SCENARIO 7: Parental Controls for Bedtime
# =============================================================================
"""
User: "My kids should stop using WiFi at 9 PM. Can you help?"

Agent Action:
1. Uses prompt: parental_controls()
2. Suggests: enable_guest_network() for kids' devices
3. Shows how to: disconnect_device() at bedtime

Agent Response:
"I can help you manage your kids' internet access! Here's a solution:

Setup:
1. Create a separate 'Kids_WiFi' network just for their devices
2. Connect their devices to this network instead of your main network
3. You can easily disable this network at bedtime

Let me set this up:

Would you like me to:
1. Create 'Kids_WiFi' network now?
2. Set a password for it?

Then each evening at 9 PM, you can tell me 'disable kids WiFi' and I'll 
turn it off. In the morning, say 'enable kids WiFi' to turn it back on.

This way your devices stay connected while controlling access for the kids' 
devices. Plus, you don't need to share your main WiFi password with them!"
"""

# =============================================================================
# SCENARIO 8: Router Won't Connect
# =============================================================================
"""
User: "My phone says it's connected but I can't access the internet!"

Agent Action:
1. Uses prompt: troubleshoot_connection(issue_type="no_connection")
2. Calls tool: get_router_status()
3. Calls tool: run_speed_test()
4. Suggests: reboot_router()

Agent Response:
"This is a common issue! Let's troubleshoot:

Router Status Check:
✓ Router is powered on
✓ WiFi is broadcasting (XiaoYi_Home_WiFi)
✓ 3 devices connected
✓ Uptime: 5 days

Possible Causes:
1. DNS cache issue on your phone
2. Router needs a reboot (been up for 5 days)
3. ISP connection problem

Quick Fixes to Try:
1. On your phone: Forget the network and reconnect
2. Turn WiFi off and on again on your phone
3. Restart your phone

If those don't work, I can reboot the router for you. This will disconnect 
all devices for about 2 minutes, then everything will reconnect automatically.

Would you like me to reboot the router?"
"""

# =============================================================================
# SCENARIO 9: Performance Monitoring
# =============================================================================
"""
User: "Can you show me how my network is performing?"

Agent Action:
1. Reads resource: router://stats
2. Calls tool: run_speed_test()
3. Reads resource: router://devices

Agent Response:
"Here's your network performance report:

Internet Speed:
- Download: 95.3 Mbps ⚡
- Upload: 42.1 Mbps ⚡
- Latency: 12 ms ✓
- Connection: Excellent

Network Activity:
- Packets Sent: 15,430,982
- Packets Received: 18,923,451
- Data Downloaded: 1.2 TB
- Data Uploaded: 234.5 GB

Connected Devices (3):
- iPhone 14: Signal -45 dBm (Excellent)
- MacBook Pro: Signal -38 dBm (Excellent)
- Smart TV: Signal -55 dBm (Good)

Overall Health: ✅ Excellent
Your network is performing very well! All devices have strong signals and 
your internet speeds are solid."
"""

# =============================================================================
# SCENARIO 10: Regular Maintenance
# =============================================================================
"""
User: "Should I do anything to maintain my router?"

Agent Action:
1. Calls tool: check_firmware_update()
2. Reads resource: router://config (check uptime)
3. Reads resource: router://logs

Agent Response:
"Let me check your router's health:

Firmware Status:
✓ Current Version: v2.1.4
✓ Latest Version: v2.1.4
✓ Status: Up to date

Uptime: 5 days, 0 hours
→ Your router has been running smoothly for 5 days. This is fine.

Recent Activity (Last 5 Events):
1. [2026-01-16 02:15:33] Device connected: iPhone 14
2. [2026-01-16 01:45:22] Firmware update check: Up to date
3. [2026-01-16 00:30:11] Device disconnected: iPad
4. [2026-01-15 23:12:45] Channel optimization: Switched to channel 6
5. [2026-01-15 22:00:00] Daily backup completed

Maintenance Recommendations:
✓ No action needed right now
✓ Consider rebooting if uptime exceeds 30 days
✓ Check for firmware updates monthly (currently up to date)
✓ Review connected devices weekly for unknown devices

Your router is in great shape! Keep doing what you're doing."
"""
