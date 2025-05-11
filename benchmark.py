# benchmark.py – chạy 5 ván / solver, lưu JSON
import random, json, time, sys, multiprocessing as mp, importlib.machinery

# ───────────── cấu hình ─────────────
RUNS_PER_ALGO = 5
TIME_LIMIT_S  = 30
MODULE_FILE   = "agorithms.py"        # tên file thuật toán
OUT_FILE      = "benchmark_result.json"

# ───────────── nạp module solver ─────
loader = importlib.machinery.SourceFileLoader("user_algos", MODULE_FILE)
algos  = loader.load_module()
sys.modules["user_algos"] = algos

SOLVER_NAMES = [
    "a_star","bfs","dfs","backtracking","iddfs","hill_climbing","greedy",
    "simulated_annealing","genetic_algorithm","ida_star","local_beam_search",
    "stochastic_hill_climbing","backtracking_fc","min_conflicts",
    "steepest_ascent_hill","uniform_cost","q_learning_solver",
    "dqn_solver","sarsa_solver","pg_solver"
]
SOLVERS = [(n, getattr(algos, n))
           for n in SOLVER_NAMES if callable(getattr(algos, n, None))]

# ───────────── sinh bàn cờ solvable ──
GOAL = (1,2,3,4,5,6,7,8,0)
def _solvable(a):
    inv=sum(1 for i in range(8) for j in range(i+1,9)
            if a[i] and a[j] and a[i]>a[j])
    return inv%2==0
def random_state():
    while True:
        st=tuple(random.sample(range(9),9))
        if _solvable(st): return st

# ───────────── worker ────────────────
def _worker(fn, start, q):
    t0 = time.perf_counter()
    try:
        path, *_ = fn(start)
        q.put(("success" if path and path[-1]==GOAL else "no_solution",
               time.perf_counter()-t0))
    except MemoryError:
        q.put(("no_solution", 0.0))
    except Exception:
        q.put(("cannot_run", 0.0))

# ───────────── benchmark main ────────
def main():
    results={}
    for name, fn in SOLVERS:
        st = {"runs":RUNS_PER_ALGO, "success":0, "no_solution":0,
              "timeout":0, "cannot_run":0, "_times":[], "_times_ok":[]}
        print(f"{name:<24}", end="", flush=True)

        for _ in range(RUNS_PER_ALGO):
            init=random_state()
            q=mp.Queue()
            p=mp.Process(target=_worker, args=(fn, init, q), daemon=True)
            p.start(); p.join(TIME_LIMIT_S)

            if p.is_alive():                         # TIMEOUT
                p.terminate(); p.join()
                st["timeout"]+=1; print(" T", end="", flush=True)
            else:
                status, t = q.get()
                st[status]+=1
                st["_times"].append(t)
                if status=="success":
                    st["_times_ok"].append(t); print(" ✔", end="", flush=True)
                elif status=="no_solution":
                    print(" ✘", end="", flush=True)
                else:                                # cannot_run
                    print(" ?", end="", flush=True)

        # thời gian trung bình
        st["avg_time_success"] = (sum(st["_times_ok"])/len(st["_times_ok"])
                                  if st["_times_ok"] else None)
        st["avg_time"] = (sum(st["_times"])/len(st["_times"])
                          if st["_times"] else None)
        del st["_times"], st["_times_ok"]
        results[name]=st
        print()

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Benchmark finished → {OUT_FILE}")

# ───────────── Windows guard ─────────
if __name__ == "__main__":
    mp.freeze_support()
    main()
