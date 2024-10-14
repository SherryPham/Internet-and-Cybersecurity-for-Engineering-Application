
# Created by Tran Anh Thu Pham
# Created on 28/9/2024
# Lab8C_Client.py

import socket

# Define the server address and port for TCP
server_address = ('127.0.0.1', 12345)

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(server_address)

try:
    while True:
        # Prompt the user to enter a message
        user_message = input("Enter a message (or type 'exit' to quit): ")

        # Check if the user wants to exit
        if user_message.lower() == 'exit':
            break

         # Check if the user provided any input
        if user_message.strip():  # Removes leading/trailing whitespace
            # Construct the message with the required header
            message = f'TNE20003:{user_message}'

            # Send the message to the server 
            client_socket.send(user_message.encode('ascii')) # Change user_message to message when formatting the string with the header

            # Receive the response from the server
            response = client_socket.recv(1024)

            # Decode the received response as ASCII text
            response_message = response.decode('ascii')

            # Display the response from the server
            print("Server Response:", response_message)
        else:
            # Display the error message if user input is empty
            print("Error: Message cannot be empty. Please enter a valid message.")

finally:
    # Close the client socket when done
    client_socket.close()
