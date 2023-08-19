import socket
import time
import threading
import argparse

def connect_to_server(ip, port, connections, result_list):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    start_time = time.time()
    try:
        client_socket.connect((ip, port))
        connection_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        result_list.append((True, connection_time))
        connections.append(client_socket)  # Keep the connection open
    except Exception as e:
        result_list.append((False, None))

def print_stats(results, delay_threshold):
    successful_connections = sum(1 for success, _ in results if success)
    failed_connections = sum(1 for success, _ in results if not success)
    delayed_connections = sum(1 for success, connection_time in results if success and connection_time > delay_threshold)
    print(f"Current statistics: Successful={successful_connections}, Failed={failed_connections}, Delayed={delayed_connections}")
    
def run_test(ips, port, num_connections, delay_threshold):
    for ip in ips:
        print(f"Running test on {ip}:{port}")
        threads = []
        results = []
        connections = []  # List to store open connections

        # Create and start threads
        for _ in range(num_connections):
            thread = threading.Thread(target=connect_to_server, args=(ip, port, connections, results))
            thread.start()
            threads.append(thread)

        # Print stats every second without waiting for all threads to finish
        while any(thread.is_alive() for thread in threads):
            print_stats(results, delay_threshold)
            time.sleep(1) # Delay to allow results to be processed

        # Close all open connections
        for conn in connections:
            conn.close()

        # Final statistics
        successful_connections = sum(1 for success, _ in results if success)
        delayed_connections = sum(1 for success, connection_time in results if success and connection_time > delay_threshold)

        print(f"Total connections: {num_connections}")
        print(f"Successful connections: {successful_connections}")
        print(f"Delayed connections: {delayed_connections} (more than {delay_threshold} milliseconds)")

# Rest of the code remains the same


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Connection Tester")
    parser.add_argument("ips", nargs='+', help="IP addresses of the servers")
    parser.add_argument("port", type=int, help="Port number of the servers")
    parser.add_argument("num_connections", type=int, help="Total number of connections to attempt")
    parser.add_argument("delay_threshold", type=float, help="Threshold for delayed connections in milliseconds")
    args = parser.parse_args()

    run_test(args.ips, args.port, args.num_connections, args.delay_threshold)
