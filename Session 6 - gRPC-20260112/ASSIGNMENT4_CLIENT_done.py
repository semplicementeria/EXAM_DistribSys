import argparse
import time
import grpc
import threading
import ASSIGNMENT4_pb2
import ASSIGNMENT4_pb2_grpc

def send_request(distr_type, param, server_address, verbose=False, thread_id=None):
    """
    Encapsulates the gRPC call logic.
    """
    prefix = f"[Thread {thread_id}] " if thread_id is not None else ""
    
    try:
        # I create a channel and a stub
        with grpc.insecure_channel(server_address) as channel:
            stub = ASSIGNMENT4_pb2_grpc.DistributionServiceStub(channel)

            if verbose:
                print(f"{prefix}Connecting to {server_address}...")

            # we prepare the request message with the fields that have to be the same as the proto file
            request = ASSIGNMENT4_pb2.GenerateRequest(
                distr_type=distr_type, 
                parameter=param
            )

            # here there's the call of the remote method
            start_time = time.time()
            response = stub.GenerateResponseTime(request)
            elapsed = time.time() - start_time

            # Output results
            print(f"{prefix}[SERVER] {response.message}")
            print(f"{prefix}[CLIENT] Measured: {elapsed:.3f}s | Reported: {response.generated_time:.3f}s")
            
    except grpc.RpcError as e:
        print(f"{prefix}gRPC Error: {e.code()} - {e.details()}")

def main():
    parser = argparse.ArgumentParser(description="gRPC Client for Random Response Time Generation")
    parser.add_argument("--dist", "-d", type=str, choices=["d", "u", "e"], required=True,
                        help="Distribution: d=deterministic, u=uniform, e=exponential")
    parser.add_argument("--param", "-p", type=float, required=True,
                        help="Parameter: (fixed time for d, max interval T for u, lambda for e)")
    parser.add_argument("--server", "-s", type=str, default="localhost", help="Server IP (default: localhost)")
    parser.add_argument("--port", "-P", type=int, default=50052, help="Server Port (default: 50052)")
    parser.add_argument("--threads", "-t", type=int, default=1, help="Number of concurrent requests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()

    # Map short codes to the strings expected by your server logic
    dist_map = {"d": "deterministic", "u": "uniform", "e": "exponential"}
    distr_type = dist_map[args.dist]
    server_address = f"{args.server}:{args.port}"

    if args.threads > 1:
        print(f"Launching {args.threads} concurrent requests...")
        threads = []
        for i in range(args.threads):
            t = threading.Thread(
                target=send_request, 
                args=(distr_type, args.param, server_address, args.verbose, i+1)
            )
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
    else:
        # Single-threaded execution
        send_request(distr_type, args.param, server_address, args.verbose)

if __name__ == "__main__":
    main()
