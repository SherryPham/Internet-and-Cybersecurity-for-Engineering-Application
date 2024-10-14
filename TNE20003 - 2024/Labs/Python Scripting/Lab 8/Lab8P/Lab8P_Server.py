
# Created by Tran Anh Thu Pham
# Created on 28/9/2024
# Lab8P_Server.py

import socket

# Define the server address and port
server_address = ('127.0.0.1', 12345)

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

while True:
    # Receive the message and address from the client
    data, client_address = server_socket.recvfrom(1024)

    # Decode the received data as ASCII text
    message = data.decode('ascii').strip()  # Removes any leading/trailing whitespace

    # Check if the received message matches the protocol definition
    if message.startswith("TNE20003:") and len(message) > len("TNE20003:"):
        client_message = message[len("TNE20003:"):]
        response = f"TNE20003:A:{client_message}"
    else:
        response = "TNE20003:E:Invalid message format"

    # Send the response back to the client
    server_socket.sendto(response.encode('ascii'), client_address)
