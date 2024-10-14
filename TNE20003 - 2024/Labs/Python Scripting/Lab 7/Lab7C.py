
# Created by Tran Anh Thu Pham 
# Created on Sept 23, 2024
# Lab7C.py

import socket

#  Defining variables for the target web server (Google) and port (HTTP)
server = "www.google.com"
server_port = 80

# # # Creating a socket object
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

# Spliting the response into HTTP response, header, and body
http_response, rest_of_response = server_response.split(b'\r\n\r\n', 1)

# Decoding the HTTP response
http_response = http_response.decode()

# Spliting the HTTP response into status line and headers
status_line, headers = http_response.split('\r\n', 1)
status_code, status_message = status_line.split(' ', 1)

# Printing the formatted response code and message
print(f"Response Code: {status_code}")
print(f"Response Message: {status_message}")

# Checking if the HTTP response is not 200 and display an error message
if status_code != '200':
    print(f"Error: {status_code} {status_message}")
else:
    # Printing the HTML content
    print("\nHTML Content:")
    print(rest_of_response.decode())

# Parsing the headers and storing them in a dictionary
header_lines = headers.split('\r\n')
header_dict = {}
for header in header_lines:
    key, value = header.split(': ', 1)
    header_dict[key] = value

# Printing the formatted header dictionary
print("Response Headers:")
for key, value in header_dict.items():
    print(f"{key}: {value}")