import numpy as np
import multiprocessing
import threading
import time
import argparse
import os

# --- CORE LOGIC ---

def task_sequence(worker_id, distr, parameters, N, output_file):
    """
    Genera N intervalli basati sulla distribuzione scelta, attende il tempo 
    generato e scrive il timestamp su file.
    """
    # Generazione degli intervalli inter-evento (N valori)
    if distr == 'd':  # Deterministica
        values = np.full(N, parameters["tau"])
    elif distr == 'u':  # Uniforme [0, T]
        values = np.random.uniform(0.0, parameters["T"], N)
    elif distr == 'e':  # Esponenziale con parametro lambda
        values = np.random.exponential(1 / parameters["lambda"], N)
    else:
        values = np.full(N, 1.0)
    
    print(f"Worker {worker_id} ha generato gli intervalli: {values}")
    
    # Esecuzione della sequenza di eventi
    for v in values:
        time.sleep(v)  # Attesa dell'intervallo generato
        ts_ms = round(time.time() * 1000)  # Timestamp in millisecondi
        
        # Scrittura su file (append mode). 
        # Nota: In Python l'append di stringhe brevi è generalmente gestito dal SO in modo atomico.
        with open(output_file, "a") as f:
            f.write(f"{worker_id},{ts_ms}\n")
    
    return values

# --- EXECUTION MODES ---

def sequential_workers(W, distr, parameters, N, output_file):
    """Esegue i worker uno dopo l'altro nello stesso processo."""
    print(f"Avvio di {W} worker in modalità SEQUENZIALE...")
    for i in range(W):
        task_sequence(i + 1, distr, parameters, N, output_file)

def multithreading_workers(W, distr, parameters, N, output_file):
    """Esegue i worker parallelamente utilizzando i Thread."""
    print(f"Avvio di {W} worker in modalità MULTITHREADING...")
    threads = []
    for i in range(W):
        t = threading.Thread(target=task_sequence, args=(i + 1, distr, parameters, N, output_file))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def multiprocessing_workers(W, distr, parameters, N, output_file):
    """Esegue i worker parallelamente utilizzando Processi separati."""
    print(f"Avvio di {W} worker in modalità MULTIPROCESSING...")
    processes = []
    for i in range(W):
        p = multiprocessing.Process(target=task_sequence, args=(i + 1, distr, parameters, N, output_file))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

# --- DATA ANALYSIS ---

def compute_averages(output_file):
    """Legge i timestamp dal file e calcola la media per worker e globale."""
    timestamps = {}
    
    # Lettura e raggruppamento dei dati per worker_id
    with open(output_file, "r") as f:
        next(f)  # Salta l'intestazione CSV
        for line in f:
            worker_id, ts = map(int, line.strip().split(","))
            if worker_id not in timestamps:
                timestamps[worker_id] = []
            timestamps[worker_id].append(ts)

    print("\n--- RISULTATI ANALISI ---")
    
    # Calcolo della media per singolo worker
    for worker_id, ts_list in sorted(timestamps.items()):
        ts_list.sort() # Assicura l'ordine cronologico
        intervals = [ts_list[i + 1] - ts_list[i] for i in range(len(ts_list) - 1)]
        avg = sum(intervals) / len(intervals) if intervals else 0
        print(f"Worker {worker_id}: Media inter-evento = {avg:.2f} ms")

    # Calcolo della media complessiva (tutti i timestamp uniti)
    all_ts = sorted([ts for sub in timestamps.values() for ts in sub])
    overall_intervals = [all_ts[i + 1] - all_ts[i] for i in range(len(all_ts) - 1)]
    overall_avg = sum(overall_intervals) / len(overall_intervals) if overall_intervals else 0
    print(f"\nMedia inter-evento globale: {overall_avg:.2f} ms")

# --- MAIN ENTRY POINT ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisi tempi inter-evento con concorrenza")
    parser.add_argument("--workers", "-w", type=int, required=True, help="Numero di worker (W)")
    parser.add_argument("--intervals", "-n", type=int, required=True, help="Intervalli per worker (N)")
    parser.add_argument("--dist", "-d", type=str, choices=["d", "u", "e"], required=True, help="Distribuzione (d, u, e)")
    parser.add_argument("--param", "-p", type=float, required=True, help="Parametro della distribuzione")
    parser.add_argument("--file", "-f", type=str, required=True, help="File di output (.txt)")
    parser.add_argument("--mode", "-m", type=str, choices=["seq", "threads", "processes"], required=True, help="Modalità")

    args = parser.parse_args()

    # Inizializzazione file di output
    if not args.file.endswith(".txt"):
        print("Errore: Il file deve avere estensione .txt")
        exit(1)

    with open(args.file, "w") as f:
        f.write("worker_id,timestamp_ms\n")

    # Mappatura parametri distribuzione
    params = {"tau": args.param, "T": args.param, "lambda": args.param}

    # Selezione della modalità di esecuzione
    if args.mode == "seq":
        sequential_workers(args.workers, args.dist, params, args.intervals, args.file)
    elif args.mode == "threads":
        multithreading_workers(args.workers, args.dist, params, args.intervals, args.file)
    elif args.mode == "processes":
        multiprocessing_workers(args.workers, args.dist, params, args.intervals, args.file)

    # Analisi finale
    compute_averages(args.file)
