import numpy as np
import multiprocessing
import threading
import time
import argparse
import os

#I've added the lock to ensure that only one worker writes the file at a time in order to prevent race  conditions.

file_lock = multiprocessing.Lock()
thread_lock = threading.Lock()

# Function to generate N random intervals based on the chosen distr. function. We wait for the generated time and write the timestamp on a file
def task_sequence(worker_id, distr, parameters, N, output_file):
    
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
        
        # Then we write to file safely using the appropriate lock
        with mode_lock:
            with open(output_file, "a") as f:
                f.write(f"{worker_id},{ts_ms}\n")
    
    return values

# The following are the execution modes:

def sequential_workers(W, distr, parameters, N, output_file):
    # In the same process each worker is executed one after the other
    print(f"Starting sequential mode for worker {W}")
    for i in range(W):
        task_sequence(i + 1, distr, parameters, N, output_file)

def multithreading_workers(W, distr, parameters, N, output_file):
    # Parallel workers by using threads
    print(f"Starting multithreading mode for worker {W}")
    threads = []
    for i in range(W):
        t = threading.Thread(target=task_sequence, args=(i + 1, distr, parameters, N, output_file))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def multiprocessing_workers(W, distr, parameters, N, output_file):
    # Parallel workers but with separated processes
    print(f"Starting multiprocessing mode for worker {W}")
    processes = []
    for i in range(W):
        p = multiprocessing.Process(target=task_sequence, args=(i + 1, distr, parameters, N, output_file))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

# Data analysis part:

def compute_averages(output_file):
    # here we read the timestamps from the file in order to compute the average per worker and the global one
    timestamps = {}
    
    # Then we read and group the workers
    with open(output_file, "r") as f:
        next(f)  # Salta l'intestazione CSV
        for line in f:
            worker_id, ts = map(int, line.strip().split(","))
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
            total_intervals.extend(intervals)
            print(f"Worker {worker_id}: Media inter-evento = {avg:.2f} ms")
    
    if total_intervals:
        print(f"\nMedia inter-evento globale: {np.mean(total_intervals):.2f} ms")
    
# MAIN part for parsing

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisi tempi inter-evento con concorrenza")
    parser.add_argument("--workers", "-w", type=int, required=True, help="Numero di worker (W)")
    parser.add_argument("--intervals", "-n", type=int, required=True, help="Intervalli per worker (N)")
    parser.add_argument("--dist", "-d", type=str, choices=["d", "u", "e"], required=True, help="Distribuzione (d, u, e)")
    parser.add_argument("--param", "-p", type=float, required=True, help="Parametro della distribuzione")
    parser.add_argument("--file", "-f", type=str, required=True, help="File di output (.txt)")
    parser.add_argument("--mode", "-m", type=str, choices=["seq", "threads", "processes"], required=True, help="Modalità")

    args = parser.parse_args()

    # Initialization of the output file
    if not args.file.endswith(".txt"):
        print("Errore: Il file deve avere estensione .txt")
        exit(1)

    with open(args.file, "w") as f:
        f.write("worker_id,timestamp_ms\n")

    # Mapping of the parameters for the distribution
    params = {"tau": args.param, "T": args.param, "lambda": args.param}

    # Selection of the execution mode
    if args.mode == "seq":
        sequential_workers(args.workers, args.dist, params, args.intervals, args.file)
    elif args.mode == "threads":
        multithreading_workers(args.workers, args.dist, params, args.intervals, args.file)
    elif args.mode == "processes":
        multiprocessing_workers(args.workers, args.dist, params, args.intervals, args.file)

    # Final analysis
    compute_averages(args.file)
