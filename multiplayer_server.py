import socket
import threading

# Server settings
HOST = '127.0.0.1'
PORT = 5555

# Store client connections
clients = []

# Function to handle incoming client connections
def handle_client(conn, addr):
    print(f"New connection: {addr}")
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            # Broadcast the received data to all clients
            for client in clients:
                if client != conn:
                    client.sendall(data.encode('utf-8'))
        except:
            break

    print(f"Connection closed: {addr}")
    conn.close()
    clients.remove(conn)

# Main server function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server started...")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()