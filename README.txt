DYNAMIC NETWORK FAILURE DETECTION AND RECOVERY SYSTEM
=====================================================

WHAT THIS PROJECT DOES
----------------------
This project monitors a real TCP service running on a second laptop.
It reports when that service becomes unreachable and when it becomes reachable again.

It demonstrates:
- TCP socket communication for real-time reachability checks
- Graph/network state for the two devices and their connection
- Disjoint Set Union (DSU) for connectivity components
- Segment Tree for failed-node counts and maximum latency range queries
- Event logging for connection loss and recovery

IMPORTANT
---------
This detects whether the monitoring agent is reachable. It cannot always tell
whether the cause is Wi-Fi disconnection, a powered-off laptop, a firewall,
or a temporary network problem. It does not force Wi-Fi to reconnect.

FILES
-----
agent.py         Run on the SECOND laptop.
monitor.py       Run on the MAIN/MONITORING laptop.
network.py       Graph/network model using DSU and Segment Tree.
dsu.py           Disjoint Set Union implementation.
segment_tree.py  Segment Tree implementation.

REQUIREMENTS
------------
Python 3.9 or newer is recommended. No third-party Python packages are required.
Both laptops need to be on the same Wi-Fi/LAN, or otherwise able to reach each other.

SETUP
-----

1. Copy the entire DynamicNetworkMonitor folder to BOTH laptops.
   You can use a USB drive or a trusted file-sharing method.

2. Find the SECOND laptop's local IPv4 address.

   On macOS:
     System Settings > Wi-Fi > Details for the connected network
     Look for IP Address.

   On Windows:
     Open Command Prompt and run:
       ipconfig
     Look for IPv4 Address under the active Wi-Fi adapter.

3. On the SECOND laptop, open a terminal in this folder and run:
     python3 agent.py
   On Windows, if python3 is not recognized, try:
     py agent.py

   Keep this program running. It listens on TCP port 5055.

4. On the MAIN laptop, open a terminal in this folder and run:
     python3 monitor.py
   On Windows, if python3 is not recognized, try:
     py monitor.py

5. When asked, enter the second laptop's local IPv4 address, for example:
     192.168.1.11
   Use the real address shown on that laptop, not this example.

6. The monitor should display ONLINE/CONNECTED and a latency value.

TESTING FAILURE AND RECOVERY
----------------------------
1. Keep monitor.py running on the main laptop.
2. Stop agent.py on the second laptop using Ctrl+C.
3. Within a few checks, the monitor should show CONNECTION LOST.
4. Start agent.py again on the second laptop.
5. The monitor should show CONNECTION RESTORED.

This test proves failure/recovery detection for the monitored service.
To test a Wi-Fi interruption, you may disconnect and reconnect the second laptop's
Wi-Fi, but the operating system or network may take time to reconnect.

TROUBLESHOOTING
---------------
- If it always says UNREACHABLE, confirm both laptops are on the same network.
- Confirm the IP address is correct and has not changed.
- Check whether the router has "AP isolation", "client isolation", or guest-network
  isolation enabled. Such settings can prevent laptops from communicating.
- The second laptop's firewall may block incoming TCP connections. If prompted by
  the operating system, allow Python to accept connections on your private/local
  network. Do not disable the firewall completely.
- Ensure port 5055 is not already being used.
- Some campus Wi-Fi networks intentionally isolate devices. Use a permitted
  private Wi-Fi network or personal hotspot if allowed by your institution.
- On macOS, use python3; on Windows, use py or python as available.

DSA NOTES FOR YOUR PRESENTATION
-------------------------------
Graph:
  Two vertices represent the monitoring laptop and remote laptop. The edge is
  active while the remote monitoring agent responds.

DSU:
  Reports connected components. When link state changes, the model rebuilds DSU,
  because standard DSU does not support deleting edges directly.

Segment Tree:
  Stores per-node failed status and latency, supporting range queries in O(log N).
  The two-node example is small; the Segment Tree demonstrates the structure and
  can be extended to monitor more devices.

Complexities:
  DSU find/union: amortized O(alpha(N)) with path compression and union by size.
  Segment Tree update/query: O(log N).
  Each TCP check: bounded by the configured connection timeout plus response time.

HONEST PROJECT LIMITATION
-------------------------
This starter implementation monitors one remote agent. For a larger multi-device
network, extend the monitor to read a list of devices and represent each monitored
link separately. The current recovery message means the remote agent is reachable
again; it does not repair the operating system's Wi-Fi connection automatically.
