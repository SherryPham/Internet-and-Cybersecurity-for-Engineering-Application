#!/usr/bin/python
####################################################################################################
## TNE20003 Sample Echo Server Program                                                            ##
##                                                                                                ##
## Very simple threaded version that supports multiple concurrent connections (but locked to a    ##
## single core                                                                                    ##
##                                                                                                ##
## Programmed by Jason But                                                                        ##
####################################################################################################

####################################################################################################
## Required Libraries                                                                             ##
####################################################################################################
## Command line parameter parsing
import argparse

## Network Socket library
import socket

## Threading library
import threading


####################################################################################################
## def handle_client(client_socket)                                                               ##
##                                                                                                ##
## Handle the echo server for a single connected remote computer. Get any data sent over the      ##
## provided TCP connection and echo it back. When the remote side closes the connection, close    ##
## the local socket and return                                                                    ##
####################################################################################################
def handle_client(client_socket):
    ## Print information about remote client
    (remote_ip, remote_port) = client_socket.getpeername()
    print(f'Thread: Accepted connection from {remote_ip}:{remote_port}')

    ## Loop until remote PC breaks connection
    while True:
        ## Get next block of data from the remote client (max 1024 bytes)
        data = client_socket.recv(1024)

        ## If data is invalid, the remote end has closed the connection. Break loop to return
        if not data: break

        ## Return sent data to client
        print(f'Thread({remote_ip}:{remote_port}): Echoing data ({data})')
        client_socket.send(data)  # send data to the client

    ## Close socket connection
    client_socket.close()
    print(f'Thread({remote_ip}:{remote_port}): Connection Closed')


####################################################################################################
## def run_server(port)                                                                           ##
##                                                                                                ##
## Run the echo server on the nominated port. Open a TCP listening socket, then run an infinite   ##
## loop accepting connections and handing them off to handle_client() in a separate thread        ##
####################################################################################################
def run_server(port):
    ## Create the listening TCP socket
    listen_socket = socket.socket()
    listen_socket.bind((socket.gethostname(), port))

    ## Set TCP socket to start listening for incomming connections, up to 5 connections can be pending
    listen_socket.listen(5)

    #thread_list = []

    while True:
        print('Parent: Waiting for connection...')

        ## Accept remote connection from client
        (client_socket, address) = listen_socket.accept()

        ## Create and start the thread to handle the client. Thread will self-terminate when when client closes the connection
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


####################################################################################################
## Class to allow an integer only in the provided range. Used to limit allowable options on CLI   ##
## parameters to a range of values                                                                ##
####################################################################################################
class IntRange:
    ## Constructor - Internally store min and max values integer can take
    def __init__(self, imin, imax):
        self.imin = imin
        self.imax = imax

    ## Validate integer - If not an integer or value is outside allowed range, raise an exception for the ArgParse to handle
    def __call__(self, arg):
        try:
            value = int(arg)
        except ValueError:
            raise argparse.ArgumentTypeError(f"Must be an integer in the range [{self.imin}, {self.imax}]")
        if (value < self.imin) or (value > self.imax):
            raise argparse.ArgumentTypeError(f"Must be an integer in the range [{self.imin}, {self.imax}]")
        return value


####################################################################################################
## Main Program                                                                                   ##
####################################################################################################
def main():
    # Parse command line options
    parser = argparse.ArgumentParser(description='Non Blocking Echo Server',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     allow_abbrev=False)

    ## port option specifies port to use, must be in range 1024-16384, default is 1024
    parser.add_argument("-p", "--port", type=IntRange(1024, 16384), default=1024, help=f"Port number to run the echo server on (default=1024)")

    ## Parse command line options
    arguments = parser.parse_args()

    ## Run server on specified port
    run_server(arguments.port)


####################################################################################################
## Run main function when executed, do nothing if imported                                        ##
####################################################################################################
if __name__ == '__main__':
    try:
        main()
    except socket.error as err:
        print(f'Socket Library Error: {err}')
    except KeyboardInterrupt as err:
        print(f'\n\nProgram terminated')


