# Comments to the code were kindly provided by ChatGPT

# Import the necessary module
import argparse
from socket import *

def startTCPserver(serverAddress, serverPort):
    '''Launch TCP server in iterative mode'''

    # Create a TCP socket for the server
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Bind the server socket to the specified address and port number
    serverSocket.bind((serverAddress, serverPort))

    # Listen for incoming connections
    serverSocket.listen()

    # Print a message indicating that the server is ready to receive connections
    print("The iterative TCP server is ready to receive")

    # Handle exceptions when interrupting the server with CTRL+C
    try:

        # Continuous loop to accept and handle incoming connections
        while True:
        
            # Accept a new connection
            connectionSocket, addr = serverSocket.accept()
        
            # Print a message indicating a new connection
            print("[+] New connection from " + addr[0] + ":" + str(addr[1]))
        
            # Send a welcome message to the client
            helloString = "Welcome, I'm a server that can convert lowercase sentences to uppercase. I'm ready!"
            connectionSocket.send(helloString.encode())

            # Loop to continuously wait for input from the client until an empty string is received
            while True:
                # Receive a sentence from the client
                sentence_enc = connectionSocket.recv(1024)
                sentence = sentence_enc.decode()

                # Check if the received string is empty
                if not sentence:
                    break  # Exit the loop if an empty string is received
        
                # Print the received sentence and client's address
                print("Sentence \"" + sentence + "\" received from " + addr[0] + ":" + str(addr[1]))
        
                # Convert the sentence to uppercase
                capitalizedSentence = sentence.upper()
        
                # Send the capitalized sentence back to the client
                connectionSocket.send(capitalizedSentence.encode())
        
            # Print a message indicating the connection is closing
            print("[+] Closing connection from " + addr[0] + ":" + str(addr[1]))

            # Close the connection socket
            connectionSocket.close()

    except KeyboardInterrupt:
        # Print a message indicating that the server is terminating
        print("The server is terminating")

        # Release the socket address
        serverSocket.close()

if __name__ == "__main__":

    # Parse the input command line
    parser = argparse.ArgumentParser(description="Start an iterarive TCP server.")
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=55000, help='Server-side TCP port number (default: 55000)')
    parser.add_argument('-a', '--address', metavar='ADDR', type=str, default='', help='IP address the server must listen on (default: any)')
    args = parser.parse_args()
    print(f"Parsed CLI arguments: {vars(args)}")

    # Launch TCP server
    startTCPserver(args.address, args.port)