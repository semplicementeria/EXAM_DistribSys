import time
import multiprocessing
from os import getpid, getppid

# Simple example task
def task(n):
    # Print the process ID and the parent process ID
    print(f"Task {n} started ('Pid: {getpid()}, PPid: {getppid()})")
    # Uncomment one of the two options:
    # 1. Sleep for 2 seconds
    #time.sleep(2)
    # 2. Execute some CPU-intensive workload
    for x in range(1, 20000000):
        float(x) / 3.141592  # Dividing x by Pi
        float(3.141592) / x  # Dividing the number Pi by x
    print(f"Task {n} finished\n")

def sequential_example():
    print("Sequential Example")
    for i in range(5):
        task(i)

# Function to demonstrate multiprocessing
def multiprocessing_example():
    print("Multiprocessing Example")
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=task, args=(i,))
        processes.append(p)
        p.start()
    
    # Wait for all processes to finish
    for p in processes:
        p.join()

# Run the example
if __name__ == '__main__':
    sequential_example()
    multiprocessing_example()
