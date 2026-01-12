# Comments to the code were kindly provided by ChatGPT

# Import the necessary module
import argparse
from socket import *

def startUDPclient(serverName, serverPort):
    '''Launch UDP client in interactive mode'''

    # Create a UDP socket for the client
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # Prompt the user to input a lowercase sentence
    sentence = input("Input lowercase sentence: ")

    # Encode the input sentence
    sentence_enc = sentence.encode()

    # Send the encoded sentence to the server
    clientSocket.sendto(sentence_enc, (serverName, serverPort))

    # Receive the modified sentence and the server's address from the server socket
    modifiedSentence, serverAddress = clientSocket.recvfrom(2048)

    # Print the modified sentence received from the server
    print("From Server: " + modifiedSentence.decode())

    # Close the client socket
    clientSocket.close()


if __name__ == "__main__":

    # Parse the input command line
    parser = argparse.ArgumentParser(description="Start an interactive UDP client.")
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=55000, help='Server-side UDP port number (default: 55000)')
    parser.add_argument('server', metavar='SERVER', type=str, help='Server host name or IP address')
    args = parser.parse_args()
    print(f"Parsed CLI arguments: {vars(args)}")

    # Launch UDP client in interactive mode
    startUDPclient(args.server, args.port)

