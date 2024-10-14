
# Created by Tran Anh Thu Pham 
# Created on Sept 23, 2024
# Lab7P.py

import socket

# Defining variables for the target web server (Google) and port (HTTP)
server = "www.google.com"
server_port = 80

# Creating a socket object
lab_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to the web server
lab_socket.connect((server, server_port))

# Sending an HTTP GET request
client_request = f"GET / HTTP/1.0\r\nHost: {server}\r\n\r\n"
lab_socket.send(client_request.encode())

# Receiving and processing the response
server_response = b""
while True:
    data = lab_socket.recv(1024)  # Receiving data in chunks of 1024 bytes
    if not data:
        break
    server_response += data

# Closing the socket connection
lab_socket.close()

# Spliting the response into HTTP response header, and body
http_response, rest_of_response = server_response.split(b'\r\n\r\n', 1)

# Printing the HTML content
print(rest_of_response.decode())

