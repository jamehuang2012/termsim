import socket
import os

SERVER_SOCKET = "/tmp/python_ipc_socket"

# Server
if os.path.exists(SERVER_SOCKET):
    os.remove(SERVER_SOCKET)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SERVER_SOCKET)
server.listen(1)
print("Server listening...")

#  Infinite loop to accept incoming connections

while True:
    connection, client_address = server.accept()

    try:
        print(f"Connection from {client_address}")

        # Receive the data from the client
        data = connection.recv(1024)
        print(f"Received: {data.decode()}")

    finally:
        # Clean up the connection
        connection.close()
        

