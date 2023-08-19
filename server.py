import socket
import threading
import argparse

def handle_client(client_socket):
    try:
        # Simple data handling, just echoing the data
        data = client_socket.recv(1024)
        client_socket.sendall(data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

def start_server(port, max_connections):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(max_connections)
    print(f"Server is listening on port {port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Accepted connection from {address}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server")
    parser.add_argument("port", type=int, help="Port number to listen on")
    parser.add_argument("max_connections", type=int, help="Maximum number of connections to handle")
    args = parser.parse_args()

    start_server(args.port, args.max_connections)

#sample run python server.py <PORT> <MAX_CONNECTIONS>
