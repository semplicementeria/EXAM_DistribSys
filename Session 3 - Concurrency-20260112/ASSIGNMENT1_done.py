import numpy as np
import multiprocessing
import threading
import time
import argparse
import os

# Function to generate N random intervals based on the chosen distr. function. 
# We wait for the generated time and write the timestamp on a file
def task_sequence(worker_id, distr, parameters, N, output_file, lock):
    
    # Generation of the inter-event values (SIZE = N)
    if distr == 'd':  # Deterministic
        values = np.full(N, parameters["tau"])
    elif distr == 'u':  # Uniform [0, T]
        values = np.random.uniform(0.0, parameters["T"], N)
    elif distr == 'e':  # Exponential with lambda as a parameter
        values = np.random.exponential(1 / parameters["lambda"], N)
    else:
        values = np.full(N, 1.0)
    
    print(f"Worker {worker_id} has generated the following intervals: {values}")
    
    # Execution of the generated interval
    for v in values:
        time.sleep(v)  # We wait for the generated interval
        ts_ms = int(round(time.time() * 1000))  # Timestamp in ms
        
        # Use the lock to prevent multiple workers from writing at the same time
        with lock:
            with open(output_file, "a") as f:
                f.write(f"{worker_id},{ts_ms}\n")
    
    return values

# The following are the execution modes:

def sequential_workers(W, distr, parameters, N, output_file, lock):
    # In the same process each worker is executed one after the other
    print(f"Starting sequential mode for worker {W}")
    for i in range(W):
        task_sequence(i + 1, distr, parameters, N, output_file, lock)

def multithreading_workers(W, distr, parameters, N, output_file, lock):
    # Parallel workers by using threads
    print(f"Starting multithreading mode for worker {W}")
    threads = []
    for i in range(W):
        t = threading.Thread(target=task_sequence, args=(i + 1, distr, parameters, N, output_file, lock))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def multiprocessing_workers(W, distr, parameters, N, output_file, lock):
    # Parallel workers but with separated processes
    print(f"Starting multiprocessing mode for worker {W}")
    processes = []
    for i in range(W):
        p = multiprocessing.Process(target=task_sequence, args=(i + 1, distr, parameters, N, output_file, lock))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

# Data analysis part:

def compute_averages(output_file):
    # here we read the timestamps from the file in order to compute the average per worker and the global one
    timestamps = {}
    
    # Then we read and group the workers
    if not os.path.exists(output_file):
        return

    with open(output_file, "r") as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split(",") # here we remove the white spaces and we split the two parts with a comma, to save it in a "parts" variable
            if len(parts) == 2: # if we have both the ts and W...
                worker_id, ts = map(int, parts) # we transform the extracted data in an integer and assign them to the specific variables of the previous list
                if worker_id not in timestamps:
                    timestamps[worker_id] = []
                timestamps[worker_id].append(ts)

    print("\nResults:")
    
    # Total storage for all intervals
    total_intervals = []
    
    for worker_id, ts_list in sorted(timestamps.items()):
        # Convert to numpy array and sort
        ts_array = np.sort(ts_list)
        # np.diff calculates [ts[1]-ts[0], ts[2]-ts[1], ...]
        intervals = np.diff(ts_array)
        
        if len(intervals) > 0:
            avg = np.mean(intervals)
            total_intervals.extend(intervals) # global inter-event average computed by using "extend" that takes the element one by one and sum it together directly from the list
            print(f"Worker {worker_id}: Inter-event average = {avg:.2f} ms")
    
    if total_intervals:
        print(f"\nGlobal inter-event average: {np.mean(total_intervals):.2f} ms")
    
# MAIN part for parsing

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analysis of inter-event intervals")
    parser.add_argument("--workers", "-w", type=int, required=True, help="Number of workers (W)")
    parser.add_argument("--intervals", "-n", type=int, required=True, help="Intervals per worker (N)")
    parser.add_argument("--dist", "-d", type=str, choices=["d", "u", "e"], required=True, help="Distribution function (d, u, e)")
    parser.add_argument("--param", "-p", type=float, required=True, help="Distribution parameter")
    parser.add_argument("--file", "-f", type=str, required=True, help="Output file (.txt)")
    parser.add_argument("--mode", "-m", type=str, choices=["seq", "threads", "processes"], required=True, help="Mode")

    args = parser.parse_args()

    # Initialization of the output file
    if not args.file.endswith(".txt"):
        print("Error: the file has to be .txt")
        exit(1)

    # Initialize the lock for synchronization
    lock = multiprocessing.Lock() #lock for the multiprocessing

    with open(args.file, "w") as f:
        f.write("worker_id,timestamp_ms\n")

    # Mapping of the parameters for the distribution
    params = {"tau": args.param, "T": args.param, "lambda": args.param}

    # Selection of the execution mode
    if args.mode == "seq":
        sequential_workers(args.workers, args.dist, params, args.intervals, args.file, lock)
    elif args.mode == "threads":
        multithreading_workers(args.workers, args.dist, params, args.intervals, args.file, lock)
    elif args.mode == "processes":
        multiprocessing_workers(args.workers, args.dist, params, args.intervals, args.file, lock)

    # Final analysis
    compute_averages(args.file)

# to try in the command line:
