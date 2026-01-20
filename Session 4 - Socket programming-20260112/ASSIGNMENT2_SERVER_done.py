import argparse
from socket import *
import time
from os import getpid, getppid
from threading import get_native_id
import multiprocessing
import threading

# Lists to store timing info
connection_times = []      # time elapsed between connection setups
data_times = []            # time elapsed between data receptions
lock = threading.Lock()    # to protect shared lists in threaded mode

# Iterative server function (the client will select this if wanted)
def TCPserverIterative(Server_address, Server_port, verbose=False):

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((Server_address, Server_port)) #command to associate the server address and server port 
    serverSocket.listen() #here the server starts to hear if there are clients that will make a sort of request

    print("The server is ready.")

    last_connection_time = None

    try: #we control if the socket is opening correctly with a loop and check also the connection
        
        while True: 
            #we accept the new connection to the client 
            connectionSocket, addr = serverSocket.accept()
            print("[+] New connection from " + addr[0] + ":" + str(addr[1])) #addr[0] corresponds to the server address, while addr[1] corresponds to the port and all is transformed in a string 

            # Measure time between connections
            now = time.time() * 1000  # in milliseconds
            if last_connection_time is not None:
                elapsed_ms = now - last_connection_time
                connection_times.append(elapsed_ms)
            last_connection_time = now 

            connectionSocket.send(b"Hello! You are connected to the server.") #confirmation from server (greeting at the client)

            last_data_time = None

            while True: 
                sentence_enc = connectionSocket.recv(1024) #packet size for small texts
                if not sentence_enc:
                    break
                now_data = time.time() * 1000  # in milliseconds

                # Measure inter-arrival time between data receptions
                if last_data_time is not None:
                    elapsed_data_ms = now_data - last_data_time
                    data_times.append(elapsed_data_ms)
                last_data_time = now_data

                sentence = sentence_enc.decode(errors="replace")

                #print the received sentence and client's address
                if verbose:
                    print("Sentence \"" + sentence + "\" received from " + addr[0] + ":" + str(addr[1]))
                
                #we send back to the client the sentence (echo)
                connectionSocket.send(sentence.encode())
                
            #advise that we are closing the connection after receiving packets
            print("[+] Closing connection from " + addr[0] + ":" + str(addr[1]))
            connectionSocket.close()

    except KeyboardInterrupt:
        print("The server has stopped.")

        # Compute and print average inter-arrival times
        if connection_times:
            print(f"Average connection inter-arrival time: {sum(connection_times)/len(connection_times):.2f} ms")
        if data_times:
            print(f"Average data inter-arrival time: {sum(data_times)/len(data_times):.2f} ms")

    #Release the socket address
    serverSocket.close()


# Handler per il client nella concurrency
def HandleClient(conn, Client_address, Client_port, verbose=False):

    # Server and threads to which we refer (the parent one practically)
    print("[+] New server socket worker spawned for client " + Client_address + ":" + str(Client_port)) 
    print("Thread ID: " + str(get_native_id()) + " - PID: " + str(getpid()) + " - PPID: " + str(getppid()))

    # Send greeting inside the worker for concurrency
    conn.send(b"Hello! You are connected to the server.")

    last_data_time = None

    try:
        while True:
            #we receive a sentence from the client
            sentence_enc = conn.recv(1024)
            if not sentence_enc:
                break
            sentence = sentence_enc.decode(errors="replace") # same as before but with the decode (specular from the pov of the client)

            # Measure time between data receptions
            now_data = time.time() * 1000  # milliseconds
            if last_data_time is not None:
                elapsed_data_ms = now_data - last_data_time
                
                # Lock to safely append in threaded mode
                with lock:
                    data_times.append(elapsed_data_ms)
            last_data_time = now_data
            
            #print the received sentence and client's address
            if verbose:
                print("Sentence \"" + sentence + "\" received from " + Client_address + ":" + str(Client_port))
            
            #send the sentence back to the client (echo)
            conn.send(sentence.encode())

    except ConnectionResetError:
        print(f"[!] Connection reset by client {Client_address}:{Client_port}")
    finally:
        conn.close()
        print(f"[x] Connection closed for {Client_address}:{Client_port}")


# Function to launch the server in concurrency mode
def TCPserverConcurrency(Server_address, Server_port, Concurrency_mode, verbose=False):  
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((Server_address,Server_port))
    serverSocket.listen()

    print("The concurrent TCP server is ready to receive (PID = " + str(getpid()) + ")")

    last_connection_time = None

    try:
        while True:
            # Accept a new connection
            connectionSocket, addr = serverSocket.accept()

            # Measure time between connections
            now = time.time() * 1000
            if last_connection_time is not None:
                elapsed_ms = now - last_connection_time
                with lock:
                    connection_times.append(elapsed_ms)
            last_connection_time = now

            # Spawn a new worker to handle the incoming connection
            if Concurrency_mode == "proc": 
                srv = multiprocessing.Process(target=HandleClient, args=(connectionSocket, addr[0], addr[1], verbose)) 
            elif Concurrency_mode == "thr":
                srv = threading.Thread(target=HandleClient, args=(connectionSocket, addr[0], addr[1], verbose)) 
            else:
                raise ValueError("Unsupported concurrency mode")

            srv.start()

    except KeyboardInterrupt:
        print("The server is terminating")

        # Compute and print average inter-arrival times
        if connection_times:
            print(f"Average connection inter-arrival time: {sum(connection_times)/len(connection_times):.2f} ms")
        if data_times:
            print(f"Average data inter-arrival time: {sum(data_times)/len(data_times):.2f} ms")

        # Release the socket address
        serverSocket.close()


#New function to start the server basing on if I have to go in the first or second function
def startTCPserver(Server_address, Server_port, Concurrency_mode, verbose=False):
    if Concurrency_mode == "iter":
        TCPserverIterative(Server_address, Server_port, verbose=verbose)
    elif Concurrency_mode in ["proc", "thr"]:
        TCPserverConcurrency(Server_address, Server_port, Concurrency_mode, verbose=verbose)
    else:
        raise ValueError("Invalid concurrency mode. Choose from: iter, proc, thr.")


#---- main con argparse
if __name__ == "__main__":

    # Parse the input command line
    parser = argparse.ArgumentParser(description="Start a concurrent TCP server.")
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=55000, help='Server-side TCP port number (default: 55000)')
    parser.add_argument('-a', '--address', metavar='ADDR', type=str, default='', help='IP address the server must listen on (default: any)')
    #so if I want the iterative or the proc I have to change the default case:
    parser.add_argument('-m', '--concurrency-mode', metavar='MODE', type=str, default='iter', choices=['iter', 'proc', 'thr'], help='Server mode: iter (iterative), proc (process-based), thr (thread-based). Default: iter')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output (print received messages)') 
    args = parser.parse_args()
    print(f"Parsed CLI arguments: {vars(args)}")

    # Launch TCP server
    startTCPserver(args.address, args.port, args.concurrency_mode, args.verbose)



#POSSIBLE TESTS: 
# 1. un server, un client, multithread: python3 ASSIGNMENT2_SERVER_done.py --port 55000 --concurrency-mode thr --verbose
#python3 ASSIGNMENT2_CLIENT_done.py --workers 3 --intervals 5 --dist u --param 2.0 --server 127.0.0.1 --port 55000 --verbose

#2. un server, client multipli in concurrency mode: python3 ASSIGNMENT2_SERVER_done.py --port 55001 --concurrency-mode proc --verbose
#python3 ASSIGNMENT2_CLIENT_done.py -w 2 -n 4 -d d -p 1.0 -s 127.0.0.1 -P 55001 -v
#python3 ASSIGNMENT2_CLIENT_done.py -w 3 -n 5 -d u -p 2.0 -s 127.0.0.1 -P 55001 -v
#python3 ASSIGNMENT2_CLIENT_done.py -w 4 -n 6 -d e -p 0.5 -s 127.0.0.1 -P 55001 -v

#3. server iterativo e due client: 
#python ASSIGNMENT2_SERVER_done.py --port 55002 --concurrency-mode iter --verbose 
#python ASSIGNMENT2_CLIENT_done.py -w 2 -n 4 -d u -p 1.0 -s 127.0.0.1 -P 55002 -v
#python ASSIGNMENT2_CLIENT_done.py -w 3 -n 3 -d d -p 0.5 -s 127.0.0.1 -P 55002 -v


