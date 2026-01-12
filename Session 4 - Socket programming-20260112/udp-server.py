# Comments to the code were kindly provided by ChatGPT

# Import the necessary module
import argparse
from socket import *

def startUDPserver(serverAddress, serverPort):
    '''Launch UDP server'''

    # Create a UDP socket for the server
    serverSocket = socket(AF_INET, SOCK_DGRAM)

    # Bind the server socket to the specified address and port number
    serverSocket.bind((serverAddress, serverPort))

    # Print a message indicating that the UDP server is ready to receive
    print("The UDP server is ready to receive")

    # Handle exceptions when interrupting the server with CTRL+C
    try:

        # Continuous loop to receive and respond to incoming messages
        while True:

            # Receive a message and the client's address from the client socket
            sentence_enc, clientAddress = serverSocket.recvfrom(2048)

            # Decode the received message
            sentence = sentence_enc.decode()
        
            # Print the received sentence and client's address
            print("Sentence \"" + sentence + "\" received from " + clientAddress[0] + ":" + str(clientAddress[1]))
        
            # Convert the sentence to uppercase
            capitalizedSentence = sentence.upper()
        
            # Encode the capitalized sentence
            capitalizedSentence_enc = capitalizedSentence.encode()
        
            # Send the capitalized sentence back to the client
            serverSocket.sendto(capitalizedSentence_enc, clientAddress)

    except KeyboardInterrupt:
    
        # Print a message indicating that the server is terminating
        print("The server is terminating")

    # Release the socket address
    serverSocket.close()


if __name__ == "__main__":

    # Parse the input command line
    parser = argparse.ArgumentParser(description="Start a UDP server.")
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=55000, help='Server-side UDP port number (default: 55000)')
    parser.add_argument('-a', '--address', metavar='ADDR', type=str, default='', help='IP address the server must listen on (default: any)')
    args = parser.parse_args()
    print(f"Parsed CLI arguments: {vars(args)}")

    # Launch UDP server
    startUDPserver(args.address, args.port)

