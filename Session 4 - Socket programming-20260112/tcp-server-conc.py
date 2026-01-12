# Import the necessary modules
import argparse
from socket import *
from os import getpid, getppid
from threading import get_native_id
import threading
import multiprocessing

# Multithreaded server - function to serve client requests
def handleClient(conn, clientAddress, clientPort):

    # Print a message indicating a new thread was spawned
    print("[+] New server socket worker spawned for client " + clientAddress + ":" + str(clientPort))
    print("Thread ID: " + str(get_native_id()) + " - PID: " + str(getpid()) + " - PPID: " + str(getppid()))

    # Send a welcome message to the client
    helloString = "Welcome, I'm a server that can convert lowercase sentences to uppercase. I'm ready!"
    conn.send(helloString.encode())

    # Loop to continuously wait for input from the client until an empty string is received
    while True:
        # Receive a sentence from the client
        sentence_enc = conn.recv(1024)
        sentence = sentence_enc.decode()

        # Check if the received string is empty
        if not sentence:
            break  # Exit the loop if an empty string is received

        # Print the received sentence and client's address
        print("Sentence \"" + sentence + "\" received from " + clientAddress + ":" + str(clientPort))

        # Convert the sentence to uppercase
        capitalizedSentence = sentence.upper()

        # Send the capitalized sentence back to the client
        conn.send(capitalizedSentence.encode())

    # Print a message indicating the connection is closing
    print("[+] Closing connection from " + clientAddress + ":" + str(clientPort))

    # Close the connection socket
    conn.close()

    # Print a message indicating that the worker is terminating
    print("Worker with ID = " + str(get_native_id()) + " is terminating")


def startTCPserver(serverAddress, serverPort, concurrencyMode):
    '''Launch TCP server in concurrent mode'''
 
    # Create a TCP socket for the server
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Bind the server socket to the specified address (any) and port number
    serverSocket.bind((serverAddress,serverPort))

    # Listen for incoming connections
    serverSocket.listen()

    # Print a message indicating that the server is ready to receive connections
    print("The concurrent TCP server is ready to receive (PID = " + str(getpid()) + ")")

    # Handle exceptions when interrupting the server with CTRL+C
    try:

        # Continuous loop to accept and handle incoming connections
        while True:
            # Accept a new connection
            connectionSocket, addr = serverSocket.accept()

            # Spawn a new worker to handle the incoming connection
            if concurrencyMode == "proc":
                srv = multiprocessing.Process(target=handleClient, args=(connectionSocket, addr[0], addr[1]))
            elif concurrencyMode == "thr":
                srv = threading.Thread(target=handleClient, args=(connectionSocket, addr[0], addr[1]))
            else:
                raise ValueError("Unsupported concurrency mode")

            srv.start()

    except KeyboardInterrupt:
        # Print a message indicating that the server is terminating
        print("The server is terminating")

        # Release the socket address
        serverSocket.close()


if __name__ == "__main__":

    # Parse the input command line
    parser = argparse.ArgumentParser(description="Start a concurrent TCP server.")
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=55000, help='Server-side TCP port number (default: 55000)')
    parser.add_argument('-a', '--address', metavar='ADDR', type=str, default='', help='IP address the server must listen on (default: any)')
    parser.add_argument('-m', '--concurrency-mode', metavar='MODE', type=str, default='proc', choices=['proc','thr'], help='Concurrency mode: process or thread (default: proc)')
    args = parser.parse_args()
    print(f"Parsed CLI arguments: {vars(args)}")

    # Launch TCP server
    startTCPserver(args.address, args.port, args.concurrency_mode)
