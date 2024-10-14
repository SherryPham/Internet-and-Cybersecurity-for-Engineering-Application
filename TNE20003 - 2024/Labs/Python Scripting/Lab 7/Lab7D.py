
# Created by Tran Anh Thu Pham 
# Created on Sept 23, 2024
# Lab7D.py

import socket
import urllib.request
from bs4 import BeautifulSoup

#  Defining variables for the target web server (Google) and port (HTTP)
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

# Checking if the HTTP response is not 200 and display an error message
if status_code != '200':
    print(f"Error: {status_code} {status_message}")
else:
    # Printing the HTML content
    print("\nHTML Content:")
    print(rest_of_response.decode())

# A function checking for an image file in the html content that is extracted
def extract_image_url(server_response):
    soup = BeautifulSoup(server_response, 'html.parser') # Object to parse the HTML content
    img_tag = soup.find('img')
    # Checking for an <img> tag and returning the value of the 'src' attribute if found and returning None otherwise
    if img_tag:
        return img_tag['src']
    else:
        return None

# A function downloading the image from a URL and saving it with a specific filename
def download_image(base_url, resource_url, filename):
    full_url = urllib.parse.urljoin(base_url, resource_url)
    urllib.request.urlretrieve(full_url, filename)

# Main execution begins here
def main():
    base_url = "https://www.google.com"
    server_response = urllib.request.urlopen(base_url)
    server_content = server_response.read()
    # Function call
    img_url = extract_image_url(server_content)

    if img_url:
        img_filename = "google_image.png"
        # Function call
        download_image(base_url, img_url, img_filename)
        print(f"Image downloaded: {img_filename}") # Success message
    else:
        print("Image URL not found on the page.") # Error message

if __name__ == "__main__":
    main()