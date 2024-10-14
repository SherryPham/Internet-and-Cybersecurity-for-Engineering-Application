
# Created by Tran Anh Thu Pham
# Created on 28/9/2024
# Lab8P_Client.py

import socket

# Define the UDP server address and port
server_address = ('127.0.0.1', 12345)

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

while True:
    # Prompt the user to enter a message
    user_message = input("Enter a message (or type 'exit' to quit): ")

    # Check if the user wants to exit
    if user_message.lower() == 'exit':
        break

    # Check if the user provided any input
    if user_message.strip():  # Removes leading/trailing whitespace
        # Construct the message with the required header
        message = f'{user_message}'

        # Send the message to the server 
        client_socket.sendto(user_message.encode('ascii'), server_address) # Change user_message to message when formatting the string with the header

        # Receive the response from the server
        response, _ = client_socket.recvfrom(1024)

        # Decode the received response as ASCII text
        response_message = response.decode('ascii')

        # Display the response from the server
        print("Server Response:", response_message)
    else:
        # Display the error message if user input is empty
        print("Error: Message cannot be empty. Please enter a valid message.")

# Close the client socket
client_socket.close()
