import socket
import sys

def test_connection(ip, port):
    try:
        print(f"Attempting to connect to {ip} on port {port}...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Set a timeout for the connection
            s.connect((ip, port))
            print(f"Connection to {ip}:{port} successful.")
    except socket.timeout:
        print(f"Connection to {ip}:{port} timed out.")
    except socket.error as err:
        print(f"Connection to {ip}:{port} failed: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 test_connection.py <IP_ADDRESS> <PORT>")
        sys.exit(1)

    ip_address = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Error: Port must be an integer.")
        sys.exit(1)

    test_connection(ip_address, port)
