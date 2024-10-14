#!/usr/bin/python
####################################################################################################
## TNE20003 Sample Chat Server Program                                                            ##
##                                                                                                ##
## Non threaded multi client Chat Server                                                          ##
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

## Select library to handle multiple sockets concurrently
import select


####################################################################################################
## def send_global_message(message, sender_id, socket_list, ignore_sockets)                       ##
##                                                                                                ##
## Send message to all sockets in socket_list EXCEPT sockets in ignore_list. Message is prepended ##
## with sender details (sender_id)                                                                ##
####################################################################################################
def send_global_message(message, sender_id, socket_list, ignore_sockets):
    for sock in socket_list:
        if sock not in ignore_sockets:
            sock.send(sender_id.encode())
            sock.send(message)


####################################################################################################
## def run_server(port)                                                                           ##
##                                                                                                ##
## Run the chat server on the nominated port. Open a TCP listening socket, then run an infinite   ##
## loop blocking on select on the listening socket and all accepted client sockets.               ##
## Within loop, add new clients to the list and remove them when they leave. When data comes from ##
## a client, echo it to all other clients in the chat                                             ##
####################################################################################################
def run_server(port):
    ## Create the listening TCP socket
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind((socket.gethostname(), port))

    ## Set TCP socket to start listening for incomming connections, up to 5 connections can be pending
    listen_socket.listen(5)

    ## Create lists of sockets for select to operate on
    inputs = [listen_socket]
    outputs = []

    while inputs:
        ## Block until one of the sockets in inputs or outputs is actionable
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        ## Loop through all sockets that either have data to read or new connection to accept
        for s in readable:
            ## This is the Listening socket, accept connection and add new socket to the inputs list
            if s is listen_socket:
                client_socket, client_address = s.accept()
                inputs.append(client_socket)
                print(f'Accepted connection from: {client_address[0]}:{client_address[1]}')

            ## This is a remote client socket, the socket either has data to read or has been closed by the remote client
            else:
                ## Actionable socket is a client socket - Try to perform a read
                (remote_ip, remote_port) = s.getpeername()
                data = s.recv(1024)

                ## Data successfully read from client socket, echo to all other sockets
                if data:
                    ## Send to all sockets in inputs that are not the listening socket or s(the sender)
                    print(f'Client({remote_ip}:{remote_port}): Echoing data ({data})')
                    send_global_message(data, f'{remote_ip}:{remote_port} - ', inputs, [s, listen_socket])

                ## No data read, socket is closed remotely. Remove from inputs and close locally
                else:
                    print(f'Connection Closed: {remote_ip}:{remote_port}')
                    send_global_message(f'{remote_ip}:{remote_port}'.encode(), f'REMOTE CLIENT LEFT CHAT - ', inputs, [s, listen_socket])
                    inputs.remove(s)
                    s.close()

        ## Loop through all sockets that have crashed/closed due to error
        for s in exceptional:
            (remote_ip, remote_port) = s.getpeername()

            print(f'Error on connection, closing: {remote_ip}:{remote_port}')
            send_global_message(f'{remote_ip}:{remote_port}'.encode(), f'REMOTE CLIENT LEFT CHAT - ', inputs, [s, listen_socket])

            inputs.remove(s)
            s.close()


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
    parser = argparse.ArgumentParser(description='Simple IRC Chat Server',
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
