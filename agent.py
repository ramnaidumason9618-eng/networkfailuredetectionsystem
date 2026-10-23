import socket
import time

HOST = "0.0.0.0"
PORT = 5055


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen(5)
    except OSError as error:
        print("Could not start the monitoring agent:", error)
        print("Check whether port", PORT, "is already being used.")
        return

    print("=" * 48)
    print("DYNAMIC NETWORK MONITOR - REMOTE AGENT")
    print("=" * 48)
    print("Listening on port", PORT)
    print("Keep this program running on the second laptop.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            connection, address = server.accept()
            with connection:
                try:
                    connection.settimeout(3)
                    data = connection.recv(100).decode("utf-8", errors="ignore").strip()
                    if data == "PING":
                        connection.sendall(("PONG " + str(time.time())).encode("utf-8"))
                except (OSError, ConnectionError):
                    pass
    except KeyboardInterrupt:
        print("\nRemote agent stopped.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
