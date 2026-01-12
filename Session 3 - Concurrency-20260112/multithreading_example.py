import time
import threading
from os import getpid, getppid

# Simple example task
def task(n):
    # Refer to the global variable "total"
    global total
    # Print the process ID and the parent process ID
    print(f"Task {n} started ('Pid: {getpid()}, PPid: {getppid()})")
    # Uncomment one of the two options:
    # 1. Sleep for 2 seconds
    time.sleep(2)
    # 2. Execute some CPU-intensive workload
    #for x in range(1, 20000000):
    #    float(x) / 3.141592  # Dividing x by Pi
    #    float(3.141592) / x  # Dividing the number Pi by x
    total = total + n
    print(f"Task {n} finished, total is {total}\n")

def sequential_example():
    print("Sequential Example")
    for i in range(5):
        task(i)

# Function to demonstrate multithreading
def multithreading_example():
    print("Multithreading Example")
    threads = []
    for i in range(5):
        t = threading.Thread(target=task, args=(i,))
        threads.append(t)
        t.start()
    
    # Wait for all threads to finish
    for t in threads:
        t.join()

# Run the example
if __name__ == '__main__':
    total = 0
    sequential_example()
    total = 0
    multithreading_example()
