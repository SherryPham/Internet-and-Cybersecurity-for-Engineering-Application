
# Created by Tran Anh Thu Pham
# Created on 28/9/2024
# Lab8C_Server.py

import socket

# Define the server address and port for TCP
server_address = ('127.0.0.1', 12345)

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Start listening for incoming connections (max 5 pending connections)
server_socket.listen(5)

while True:
    print('Waiting for a connection...')

    # Accept an incoming connection and create a new socket for communication
    client_socket, client_address = server_socket.accept()
    print(f'Connection established with {client_address}')

    try:
        while True:
            # Receive the data from the client
            data = client_socket.recv(1024)

            # Decode the received data as ASCII text
            message = data.decode('ascii').strip()  # Removes any leading/trailing whitespace

            # Check if the received message matches the protocol definition
            if message.startswith("TNE20003:") and len(message) > len("TNE20003:"):
                client_message = message[len("TNE20003:"):]
                response = f"TNE20003:A:{client_message}"
            else:
                response = "TNE20003:E:Invalid message format"

            # Send the response back to the client
            client_socket.send(response.encode('ascii'))

    finally:
        # Close the client socket when the client disconnects
        client_socket.close()
