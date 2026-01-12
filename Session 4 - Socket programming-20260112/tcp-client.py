# Comments to the code were kindly provided by ChatGPT

# Import the necessary module
import argparse
from socket import *

def startTCPclient(serverName, serverPort):
    '''Launch TCP client in interactive mode'''

    # Create a TCP socket for the client
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Connect the client socket to the server
    clientSocket.connect((serverName, serverPort))

    # Receive a greeting message from the server and print it
    helloString_enc = clientSocket.recv(1024)
    print(helloString_enc.decode())

    # Loop to continuously prompt the user for input until an empty string is entered
    while True:
        # Prompt the user to enter a sentence
        sentence = input("Enter a lowercase sentence (or type an empty string to exit): ")
    
        # Check if the input string is empty
        if not sentence:
            break  # Exit the loop if an empty string is entered
    
        # Send the input sentence to the server
        clientSocket.send(sentence.encode())
    
        # Receive a response from the server and print it
        modifiedSentence_enc = clientSocket.recv(1024)
        print("From the server: " + modifiedSentence_enc.decode())

    # Close the client socket
    clientSocket.close()


if __name__ == "__main__":

    # Parse the input command line
    parser = argparse.ArgumentParser(description="Start an interactive TCP client.")
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=55000, help='Server-side TCP port number (default: 55000)')
    parser.add_argument('server', metavar='SERVER', type=str, help='Server host name or IP address')
    args = parser.parse_args()
    print(f"Parsed CLI arguments: {vars(args)}")

    # Launch TCP client in interactive mode
    startTCPclient(args.server, args.port)