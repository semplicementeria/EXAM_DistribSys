import numpy as np
import threading
import time
import argparse
import socket

# Function to generate N random intervals and send timestamps via Socket
def task_sequence_socket(worker_id, distr, parameters, N, server_ip, server_port, verbose):
    try:
        # Create a TCP stream socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        
        # Optional: Receive initial greeting from server
        greeting = client_socket.recv(1024).decode(errors="replace")
        if verbose:
            print(f"[Worker {worker_id}] Connected. Server says: {greeting.strip()}")

        # Generation of the inter-event values (SIZE = N)
        if distr == 'd':  # Deterministic
            values = np.full(N, parameters["tau"])
        elif distr == 'u':  # Uniform [0, T]
            values = np.random.uniform(0.0, parameters["T"], N)
        elif distr == 'e':  # Exponential (param is rate lambda)
            # numpy's exponential uses scale (1/lambda)
            values = np.random.exponential(1 / parameters["lambda"], N)
        else:
            values = np.full(N, 1.0)
        
        # Execution and sending
        for i, v in enumerate(values):
            time.sleep(v)  # Wait for the generated interval
            
            # Generate the timestamp string
            ts_ms = int(round(time.time() * 1000))
            message = f"Worker {worker_id}, Event {i+1}, Timestamp {ts_ms}"
            
            if verbose:
                print(f"[Worker {worker_id}] Sending: {message}")
            
            # Send data to server
            client_socket.send(message.encode())
            
            # Wait for echo/ack from server to maintain stream sync
            client_socket.recv(1024)

        client_socket.close()
        if verbose:
            print(f"[Worker {worker_id}] Task completed and connection closed.")

    except Exception as e:
        print(f"Error in Worker {worker_id}: {e}")

# Multithreading execution (Required by the assignment)
def multithreading_workers(W, distr, parameters, N, server_ip, server_port, verbose):
    print(f"Starting {W} threads connecting to {server_ip}:{server_port}...")
    threads = []
    for i in range(W):
        # We pass worker_id i+1 to match your previous logic
        t = threading.Thread(target=task_sequence_socket, 
                             args=(i + 1, distr, parameters, N, server_ip, server_port, verbose))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    print("All workers have finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multithreaded TCP Timestamp Client")
    
    # Required Arguments
    parser.add_argument("--server", "-s", type=str, required=True, help="Server IP address or hostname")
    parser.add_argument("--workers", "-w", type=int, required=True, help="Number of workers (W)")
    parser.add_argument("--intervals", "-n", type=int, required=True, help="Intervals per worker (N)")
    parser.add_argument("--dist", "-d", type=str, choices=["d", "u", "e"], required=True, help="Distribution (d, u, e)")
    parser.add_argument("--param", "-p", type=float, required=True, help="Distribution parameter")
    
    # Optional Arguments
    parser.add_argument("--port", "-P", type=int, default=55000, help="Server TCP port (default: 55000)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Map parameters for the distribution
    params = {"tau": args.param, "T": args.param, "lambda": args.param}

    # Run in multithreading mode
    multithreading_workers(args.workers, args.dist, params, args.intervals, args.server, args.port, args.verbose)
