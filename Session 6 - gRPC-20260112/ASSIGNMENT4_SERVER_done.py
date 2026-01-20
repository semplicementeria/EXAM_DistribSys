import grpc
from concurrent import futures
import time
import random
import ASSIGNMENT4_pb2
import ASSIGNMENT4_pb2_grpc

class DistributionServiceServicer(ASSIGNMENT4_pb2_grpc.DistributionServiceServicer):
    
    def _run_cpu_task(self, interval):
        """
        Executes a CPU-intensive task for the specified interval.
        As specified in the assignment requirements.
        """
        start_time = time.time()
        while time.time() - start_time < interval:
            x = time.time() - start_time
            if x == 0: continue # Avoid division by zero at the very start
            x = float(x) / 3.141592
            x = float(3.141592) / x
        return time.time() - start_time

    def GenerateResponseTime(self, request, context):
        distr = request.distr_type
        param = request.parameter
        interval = 0.0

        # Calculate interval based on the requested distribution
        if distr == "deterministic":
            interval = param
        elif distr == "uniform":
            # Interval [0, T]
            interval = random.uniform(0, param)
        elif distr == "exponential":
            # random.expovariate uses lambda (rate)
            # Mean = 1/lambda
            interval = random.expovariate(param)
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid distribution type')
            return ASSIGNMENT4_pb2.GenerateResponse()

        print(f"Server: Received {distr} request. Emulating {interval:.4f}s of CPU work...")
        
        # Perform the emulated work
        actual_work_done = self._run_cpu_task(interval)
        
        return ASSIGNMENT4_pb2.GenerateResponse(
            generated_time=actual_work_done,
            message=f"Successfully simulated {distr} workload."
        )


"""
    Start the gRPC server and listen for client requests.
    The server runs on port 50051 and handles multiple requests using a thread pool.
    """
def serve():
    # We use a ThreadPool to allow concurrent CPU task execution
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) #multi-threaded server
    ASSIGNMENT4_pb2_grpc.add_DistributionServiceServicer_to_server(
        DistributionServiceServicer(), server
    )
    
    port = "50052" 
    server.add_insecure_port(f'[::]:{port}')
    print(f"gRPC Server started on port {port}")
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print(f"The server has been closed.")

if __name__ == '__main__':
    serve()
