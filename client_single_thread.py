import socket
import time
import threading
import argparse

def connect_to_server(ip, port, connections, results, delay_threshold):
    while len(connections) < results['num_connections']:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start_time = time.time()
        try:
            client_socket.connect((ip, port))
            connection_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if connection_time > delay_threshold:
                results['delayed'] += 1
            results['successful'] += 1
            connections.append(client_socket)  # Keep the connection open
        except Exception as e:
            results['failed'] += 1

def run_test(ips, port, num_connections, delay_threshold, timeout):
    for ip in ips:
        print(f"Running test on {ip}:{port}")
        results = {'successful': 0, 'failed': 0, 'delayed': 0, 'num_connections': num_connections}
        connections = []  # List to store open connections

        # Start background thread for connecting
        connection_thread = threading.Thread(target=connect_to_server, args=(ip, port, connections, results, delay_threshold))
        connection_thread.start()

        # Monitor progress in the main thread
        start_time = time.time()
        while connection_thread.is_alive() and time.time() - start_time < timeout:
            print(f"Current statistics: Successful={results['successful']}, Failed={results['failed']}, Delayed={results['delayed']}")
            time.sleep(1)

        if connection_thread.is_alive():
            print("Test timed out!")
            connection_thread.join()  # Optional: Wait for thread to finish

        # Close all open connections
        for conn in connections:
            conn.close()

        print(f"Total connections: {num_connections}")
        print(f"Successful connections: {results['successful']}")
        print(f"Delayed connections: {results['delayed']} (more than {delay_threshold} milliseconds)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Connection Tester")
    parser.add_argument("ips", nargs='+', help="IP addresses of the servers")
    parser.add_argument("port", type=int, help="Port number of the servers")
    parser.add_argument("num_connections", type=int, help="Total number of connections to attempt")
    parser.add_argument("delay_threshold", type=float, help="Threshold for delayed connections in milliseconds")
    parser.add_argument("timeout", type=int, help="Timeout for the test in seconds")
    args = parser.parse_args()

    run_test(args.ips, args.port, args.num_connections, args.delay_threshold, args.timeout)
