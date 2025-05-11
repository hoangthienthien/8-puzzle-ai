# modern_8puzzle_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading, random, time
import json, os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
import matplotlib.pyplot as plt
import agorithms as pa  # Đảm bảo bạn có file này

# ----------------------------- Constants ----------------------------- #
PRIMARY = "#3F72AF"
SECONDARY = "#112D4E"
ACCENT = "#DBE2EF"
BG_LIGHT = "#F4F6F8"
WARNING = "#E74C3C"
SUCCESS = "#2ECC71"
STATS = "#6C5CE7"
TILE_BG = "#ECF0F1"
TEXT_COLOR = "#1F2A44"

SCALE = 2.5
TILE_PX = int(60 * SCALE)
FONT_SIZE = int(11 * SCALE)
PAD = 12
BTN_W = 20

TILE_FONT = ("Helvetica", int(FONT_SIZE * 1.8), "bold")
TITLE_FONT = ("Helvetica", int(FONT_SIZE * 1.6), "bold")
BTN_FONT = ("Helvetica", int(FONT_SIZE * 0.9), "bold")
INFO_FONT = ("Helvetica", int(FONT_SIZE * 0.8))
COMBO_FONT = ("Helvetica", int(FONT_SIZE * 0.8))

CATEGORIES = {
    "Informed search": [("A*", pa.a_star), ("Greedy", pa.greedy),
                         ("IDA*", pa.ida_star),
                         ],
    "Uninformed search": [("BFS", pa.bfs), ("DFS", pa.dfs), ("Backtracking", pa.backtracking),
                           ("IDDFS", pa.iddfs), ("UCS", pa.uniform_cost)],
    "CSPs": [("BT-FC", pa.backtracking_fc), ("Min-Conf", pa.min_conflicts)],
    "Local search": [("Hill-Climb", pa.hill_climbing), ("Stoch-HC", pa.stochastic_hill_climbing),
                      ("Steepest-HC", pa.steepest_ascent_hill), ("SA", pa.simulated_annealing),
                      ("GA", pa.genetic_algorithm),("Beam-k", lambda s: pa.local_beam_search(s, beam_width=5))],
    "Reinforcement learning": [("Q-Learn", pa.q_learning_solver), ("SARSA", pa.sarsa_solver),
                                ("DQN", pa.dqn_solver), ("PG", pa.pg_solver)],
    "Sensorless search": [                       # 👈 thêm cụm này
        ("Sensorless-BFS", pa.sensorless_search)
    ],
}

ALGO_INFO = {
    # ――― Informed search ―――
    "A*": "A* search evaluates f(n)=g(n)+h(n) and explores nodes in a priority queue for optimal paths.",
    "Greedy": "Greedy best-first picks the node with the smallest heuristic h(n); fast but not optimal.",
    "IDA*": "Iterative-Deepening A* does DFS with increasing f-cutoffs, combining A*’s optimality with DFS memory thrift.",
    
    # ――― Uninformed search ―――
    "BFS": "Breadth-First Search expands the shallowest frontier first, guaranteeing the shortest-step solution.",
    "DFS": "Depth-First Search dives down a branch to the depth limit before backtracking; low memory, non-optimal.",
    "Backtracking": "Recursive DFS that abandons branches on failure, useful for constraint satisfaction or deep trees.",
    "IDDFS": "Iterative-Deepening DFS repeats DFS with depth limits 0,1,2…; optimal depth cost, tiny memory.",
    "UCS": "Uniform-Cost Search expands the lowest-cost g(n) node, delivering an optimal solution with unit costs.",
    
    # ――― Sensorless search ―――
    "Sensorless-BFS": "Belief-state BFS plans when the agent cannot sense the exact state, searching over state sets.",
    
    # ――― CSPs ―――
    "BT-FC": "Backtracking with Forward-Checking prunes branches whose g+h already exceed the best found plan.",
    "Min-Conf": "Min-Conflicts picks a random best neighbor each step, escaping local plateaus in CSP landscapes.",
    
    # ――― Local search ―――
    "Hill-Climb": "Simple hill climbing chooses the neighbor with the lowest h(n); stops at peaks or plateaus.",
    "Stoch-HC": "Stochastic (first-choice) HC shuffles neighbors and moves to the first that improves h(n).",
    "Steepest-HC": "Steepest-Ascent HC evaluates all neighbors each step and moves to the globally best h(n).",
    "SA": "Simulated Annealing accepts worse moves with probability e^(-Δ/T) as temperature cools, avoiding traps.",
    "GA": "Genetic Algorithm evolves a population of move strings using selection, crossover and mutation.",
    "Beam-k": "Local k-Beam Search keeps the best k states at each depth, trading breadth for memory control.",
    
    # ――― Reinforcement learning ―――
    "Q-Learn": "Tabular Q-Learning uses off-policy updates to learn action values, then follows the greedy policy.",
    "SARSA": "On-policy SARSA updates Q(s,a) with the next action actually taken, yielding a smoother policy.",
    "DQN": "Deep Q-Network approximates Q-values with a neural net and replay buffer for large state spaces.",
    "PG": "Policy Gradient (REINFORCE) directly optimizes π(a|s) by following the gradient of expected return."
}


class ModernPuzzleGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle Solver")
        self._build_ui()
        self.reset_board()
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _panel(self, parent, title, top_pad=0):
        frame = tk.LabelFrame(parent, text=title, bg=BG_LIGHT, font=TITLE_FONT,
                              fg=SECONDARY, labelanchor="n")
        frame.pack(fill="x", pady=(top_pad, PAD))
        return frame

    def _stat_line(self, parent, label):
        row = tk.Frame(parent, bg=BG_LIGHT)
        row.pack(anchor="w")
        tk.Label(row, text=label, font=INFO_FONT, bg=BG_LIGHT, fg=TEXT_COLOR).pack(side="left")
        val = tk.Label(row, text="-", font=INFO_FONT, bg=BG_LIGHT, fg=TEXT_COLOR)
        val.pack(side="left", padx=PAD)
        return val

    def _build_ui(self):
        self.configure(bg=BG_LIGHT)
        root = tk.Frame(self, bg=BG_LIGHT, padx=PAD * 2, pady=PAD * 2)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        tk.Label(root, text="8-Puzzle Solver", font=TITLE_FONT, bg=BG_LIGHT, fg=SECONDARY).grid(row=0, column=0, columnspan=2, pady=(0, PAD * 2))

        # Left panel
        left = tk.Frame(root, bg=BG_LIGHT)
        left.grid(row=1, column=0, sticky="n", padx=PAD * 2)

        board_frame = tk.Frame(left, bg=SECONDARY, bd=4, relief="ridge")
        board_frame.pack(pady=(0, PAD * 2))
        board = tk.Frame(board_frame, bg=SECONDARY)
        board.pack()
        self.tiles = []
        for r in range(3):
            for c in range(3):
                cell = tk.Frame(board, bg=SECONDARY)
                cell.grid(row=r, column=c, padx=1, pady=1)
                lbl = tk.Label(cell, width=2, height=1, font=TILE_FONT, bg=TILE_BG, fg=TEXT_COLOR)
                lbl.pack(ipadx=TILE_PX // 4, ipady=TILE_PX // 6)
                self.tiles.append(lbl)

        self.combo_vars = []
        self.selected_algo = None
        combo_frame = tk.LabelFrame(left, text="Algorithms", bg=ACCENT, fg=SECONDARY,
                                    font=TITLE_FONT, bd=2, relief="groove", labelanchor="n")
        combo_frame.pack(fill="x", pady=PAD)
        for cat, algos in CATEGORIES.items():
            sub = tk.Frame(combo_frame, bg=ACCENT)
            sub.pack(fill="x", pady=PAD // 2)
            tk.Label(sub, text=cat, font=INFO_FONT, bg=ACCENT, fg=SECONDARY).pack(anchor="w")
            var = tk.StringVar()
            self.combo_vars.append(var)
            cb = ttk.Combobox(sub, textvariable=var, values=[n for n, _ in algos],
                              font=COMBO_FONT, state="readonly")
            cb.pack(fill="x", pady=2)
            cb.bind("<<ComboboxSelected>>", self._make_handler(var, dict(algos)))

        # Right panel
        right = tk.Frame(root, bg=BG_LIGHT)
        right.grid(row=1, column=1, sticky="nsew", padx=(PAD * 3, 0))
        stats = self._panel(right, "Statistics")
        self.steps_val = self._stat_line(stats, "Steps:")
        self.time_val = self._stat_line(stats, "Time:")

        self.info_panel = self._panel(right, "Algorithm Info", top_pad=PAD * 2)
        self.algo_info_lbl = tk.Label(self.info_panel, text="Pick an algorithm ↓",
                                      wraplength=260, justify="left", bg=ACCENT,
                                      fg=TEXT_COLOR, font=INFO_FONT)
        self.algo_info_lbl.pack(fill="x")

        # Controls moved to right
        ctrl_frame = tk.Frame(right, bg=BG_LIGHT)
        ctrl_frame.pack(pady=PAD * 2)
        self.run_btn = tk.Button(ctrl_frame, text="Run", width=BTN_W, bg=PRIMARY, fg="white",
                                 font=BTN_FONT, activebackground="#2D6DD2",
                                 command=self._run_clicked)
        self.run_btn.pack(pady=PAD)
        self.stat_btn = tk.Button(ctrl_frame, text="Statistics", width=BTN_W, bg=SUCCESS, fg="white",
                                  font=BTN_FONT, activebackground="#27AE60",
                                  command=self._show_stats)
        self.stat_btn.pack(pady=PAD)
        self.reset_btn = tk.Button(ctrl_frame, text="New Puzzle", width=BTN_W, bg=WARNING, fg="white",
                                   font=BTN_FONT, activebackground="#C0392B",
                                   command=self.reset_board)
        self.reset_btn.pack(pady=PAD)

    def _make_handler(self, var, lookup):
        def cb(_):
            name = var.get()
            for v in self.combo_vars:
                if v is not var: v.set('')
            self.selected_algo = (name, lookup[name])
            self.algo_info_lbl.config(text=ALGO_INFO.get(name, "No info."))
        return cb

    def _draw_board(self, state):
        for i, val in enumerate(state):
            if val == 0:
                self.tiles[i].config(text='', bg=ACCENT, relief="flat")
            else:
                self.tiles[i].config(text=str(val), bg=TILE_BG, relief="raised")

    def _is_solvable(self, arr):
        inv = sum(1 for i in range(8) for j in range(i+1, 9) if arr[i] and arr[j] and arr[i] > arr[j])
        return inv % 2 == 0

    def reset_board(self):
        while True:
            arr = random.sample(range(9), 9)
            if self._is_solvable(arr): break
        self.current_state = tuple(arr)
        self._draw_board(self.current_state)
        for v in self.combo_vars: v.set('')
        self.selected_algo = None
        self.steps_val.config(text="–")
        self.time_val.config(text="–")
        self.algo_info_lbl.config(text="Pick an algorithm ↓")

    def _run_clicked(self):
        if self.selected_algo is None:
            messagebox.showinfo("Select Algorithm", "Please select an algorithm first.")
            return
        name, fn = self.selected_algo
        self.run_btn.config(state="disabled")
        self.reset_btn.config(state="disabled")
        self.steps_val.config(text="...")
        self.time_val.config(text="Searching...")

        def worker():
            t0 = time.perf_counter()
            try:
                path, _, _ = fn(self.current_state)
            except Exception as e:
                self._back_to_idle(str(e))
                return

            if path is None:
                self._back_to_idle("No solution found or algorithm returned nothing.")
                return

            for st in path:
                self.after(0, lambda s=st: self._draw_board(s))
                time.sleep(0.15)

            total = time.perf_counter() - t0
            self.after(0, lambda: (
                self.steps_val.config(text=str(len(path) - 1)),
                self.time_val.config(text=f"{total:.4f} s"),
                self.reset_btn.config(state="normal"),
                self.run_btn.config(state="normal")
            ))


        threading.Thread(target=worker, daemon=True).start()

    def _back_to_idle(self, msg):
        self.after(0, lambda: (
            messagebox.showinfo("Error", msg),
            self.run_btn.config(state="normal"),
            self.reset_btn.config(state="normal")
        ))

    def _show_stats(self):
        FILE = "benchmark_result.json"
        if not os.path.exists(FILE):
            messagebox.showinfo("File Not Found", f"Missing '{FILE}'. Run benchmark.py first.")
            return
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        algos = list(data.keys())
        succ = [data[a]["success"] for a in algos]
        tot = [data[a]["timeout"] for a in algos]
        nosol = [data[a]["no_solution"] for a in algos]

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = [SUCCESS, ACCENT, WARNING]
        ax.bar(algos, succ, label="Success", color=colors[0])
        ax.bar(algos, nosol, bottom=succ, label="No solution", color=colors[1])
        ax.bar(algos, tot, bottom=[s + n for s, n in zip(succ, nosol)], label="Timeout", color=colors[2])
        ax.set_ylabel("Runs (5 per algorithm)")
        ax.set_title("Benchmark Results")
        ax.legend()
        fig.tight_layout()

        win = tk.Toplevel(self)
        win.title("Statistics")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=PAD)

if __name__ == "__main__":
    tk.Tk.report_callback_exception = lambda *a, **k: None
    app = ModernPuzzleGUI()
    app.mainloop()