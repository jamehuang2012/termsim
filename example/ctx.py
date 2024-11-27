import socket

# Define the path to the UNIX socket (must match the server's socket path)
SERVER_SOCKET = "/tmp/python_ipc_socket"

# Create a UNIX socket
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    # Connect to the server
    client.connect(SERVER_SOCKET)
    
    # Send a message to the server
    client.send(b"Hello from client!")
    
    print("Message sent to the server.")
    
finally:
    # Close the connection
    client.close()
