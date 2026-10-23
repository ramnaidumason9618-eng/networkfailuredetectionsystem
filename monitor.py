import socket
import time
from datetime import datetime

from network import Network

PORT = 5055
CHECK_INTERVAL_SECONDS = 2
CONNECT_TIMEOUT_SECONDS = 1.5


def check_device(ip_address):
    """Return (online, latency_ms). Uses a small TCP PING/PONG exchange."""
    start = time.perf_counter()
    try:
        with socket.create_connection(
            (ip_address, PORT), timeout=CONNECT_TIMEOUT_SECONDS
        ) as connection:
            connection.settimeout(CONNECT_TIMEOUT_SECONDS)
            connection.sendall(b"PING")
            reply = connection.recv(100).decode("utf-8", errors="ignore")
            if not reply.startswith("PONG"):
                return False, 0.0
        elapsed_ms = (time.perf_counter() - start) * 1000
        return True, elapsed_ms
    except (OSError, ConnectionError, TimeoutError):
        return False, 0.0


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    print("=" * 58)
    print("DYNAMIC NETWORK FAILURE DETECTION AND RECOVERY SYSTEM")
    print("=" * 58)
    print("This monitor checks a TCP agent on the other laptop.")
    print("Both laptops should be on a network that allows device-to-device traffic.")
    remote_ip = input("Enter the second laptop's IPv4 address: ").strip()

    if not remote_ip:
        print("An IP address is required.")
        return

    network = Network()
    previous_status = None
    event_log = []

    print("\nMonitoring", remote_ip, "on TCP port", PORT)
    print("Check interval:", CHECK_INTERVAL_SECONDS, "seconds")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            online, latency = check_device(remote_ip)
            network.set_remote_status(online, latency)

            if previous_status is None:
                event = "INITIAL STATUS: ONLINE" if online else "INITIAL STATUS: UNREACHABLE"
                event_log.append((timestamp(), event))
            elif online and not previous_status:
                event = "CONNECTION RESTORED"
                event_log.append((timestamp(), event))
            elif not online and previous_status:
                event = "CONNECTION LOST"
                event_log.append((timestamp(), event))
            else:
                event = None

            print("\033[2J\033[H", end="")  # Clear terminal screen where supported.
            print("=" * 58)
            print("DYNAMIC NETWORK FAILURE DETECTION AND RECOVERY SYSTEM")
            print("=" * 58)
            print("Last check:", timestamp())
            print("Monitor laptop: ONLINE")
            print("Remote laptop :", "ONLINE" if online else "UNREACHABLE")
            print("Connection    :", "CONNECTED" if online else "DISCONNECTED")
            print("Latency       :", f"{latency:.2f} ms" if online else "N/A")
            print("Active links  :", 1 if online else 0)
            print("Components    :", network.component_count())
            print("Failed nodes  :", network.failed_count())
            print("Max latency   :", f"{network.max_latency():.2f} ms")
            print("-" * 58)

            if event:
                print("EVENT:", event)
                print("TIME :", event_log[-1][0])

            print("\nRecent event log:")
            if not event_log:
                print("  No events yet.")
            else:
                for event_time, event_text in event_log[-8:]:
                    print(" ", event_time, "-", event_text)

            print("\nTip: stop agent.py on the other laptop to test a failure.")
            print("Start agent.py again to test recovery.")
            previous_status = online
            time.sleep(CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nMonitor stopped.")


if __name__ == "__main__":
    main()
