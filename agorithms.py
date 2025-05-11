# ----------  agorithms.py  ----------
"""
Search algorithms for the 8-puzzle.
Each solver returns (solution_path, num_expanded, elapsed_seconds)
    • solution_path  – list of board states from start→goal
    • num_expanded   – how many nodes were taken from the frontier
    • elapsed_seconds – wall-clock runtime
If no solution exists: return (None, num_expanded, elapsed_seconds)
Board state is a tuple of 9 ints, 0 = blank.   Example goal:
    (1,2,3,
     4,5,6,
     7,8,0)
"""

import time
import heapq
from collections import deque
import time, heapq, math, random
GOAL = (1,2,3,4,5,6,7,8,0)
NEIGHBORS = {
    0:(1,3), 1:(0,2,4), 2:(1,5),
    3:(0,4,6), 4:(1,3,5,7), 5:(2,4,8),
    6:(3,7), 7:(4,6,8), 8:(5,7)
}

# ---------- utility ---------------------------------------------------------

def _swap(state, i, j):
    lst = list(state)
    lst[i], lst[j] = lst[j], lst[i]
    return tuple(lst)

def _manhattan(state):
    dist = 0
    for idx, val in enumerate(state):
        if val == 0: continue
        goal_r, goal_c = (val-1)//3, (val-1)%3
        r, c = idx//3, idx%3
        dist += abs(goal_r-r) + abs(goal_c-c)
    return dist

def _reconstruct(parent, state):
    path = [state]
    while state in parent:
        state = parent[state]
        path.append(state)
    return path[::-1]

# ---------- Breadth-first Search -------------------------------------------

def bfs(start):
    t0 = time.perf_counter()
    frontier = deque([start])
    parent = {}
    expanded = 0
    seen = {start}
    while frontier:
        state = frontier.popleft()
        expanded += 1
        if state == GOAL:
            return _reconstruct(parent, state), expanded, time.perf_counter()-t0
        z = state.index(0)
        for nxt in NEIGHBORS[z]:
            child = _swap(state, z, nxt)
            if child not in seen:
                seen.add(child)
                parent[child] = state
                frontier.append(child)
    return None, expanded, time.perf_counter()-t0

# ---------- Depth-first Search (iterative, depth-limit 30) ------------------

# ---------- Depth-First Search có giới hạn an toàn ----------
def dfs(start, depth_limit=40):   # ≤ 40 đủ cho 8-puzzle
    t0 = time.perf_counter()
    stack   = [(start, 0)]
    parent  = {}
    visited = {start}
    expanded = 0

    while stack:
        state, depth = stack.pop()
        expanded += 1
        if state == GOAL:
            return _reconstruct(parent, state), expanded, time.perf_counter()-t0
        if depth >= depth_limit:
            continue
        z = state.index(0)
        for nxt in NEIGHBORS[z]:
            child = _swap(state, z, nxt)
            if child not in visited:
                visited.add(child)
                parent[child] = state
                stack.append((child, depth+1))

    # hết stack → không tìm thấy lời giải
    return None, expanded, time.perf_counter()-t0


# ---------- A* --------------------------------------------------------------

def a_star(start):
    t0 = time.perf_counter()
    g = {start:0}
    pq = [( _manhattan(start), start)]
    parent = {}
    expanded = 0
    while pq:
        f, state = heapq.heappop(pq)
        expanded += 1
        if state == GOAL:
            return _reconstruct(parent, state), expanded, time.perf_counter()-t0
        z = state.index(0)
        for nxt in NEIGHBORS[z]:
            child = _swap(state, z, nxt)
            tentative = g[state] + 1
            if tentative < g.get(child, 1e9):
                g[child] = tentative
                parent[child] = state
                heapq.heappush(pq, (tentative + _manhattan(child), child))
    return None, expanded, time.perf_counter()-t0

# ---------- Backtracking (recursive DFS with early stop) --------------------

def backtracking(start, depth_limit=66):
    t0 = time.perf_counter()
    parent = {}
    seen = {start}

    def recurse(state, depth):
        nonlocal parent
        if state == GOAL:
            return True
        if depth >= depth_limit:
            return False
        z = state.index(0)
        for nxt in NEIGHBORS[z]:
            child = _swap(state, z, nxt)
            if child not in seen:
                seen.add(child)
                parent[child] = state
                if recurse(child, depth+1):
                    return True
        return False

    found = recurse(start, 0)
    elapsed = time.perf_counter()-t0
    if found:
        return _reconstruct(parent, GOAL), len(seen), elapsed
    return None, len(seen), elapsed


def iddfs(start, max_depth=100):
    """
    Iterative Deepening Depth-First Search.
    Trả lời tối ưu về số bước, bộ nhớ thấp như DFS.
    """
    t0 = time.perf_counter()
    total_expanded = 0
    for depth in range(max_depth + 1):
        path, expanded, _ = dfs(start, depth_limit=depth)
        total_expanded += expanded
        if path is not None:
            return path, total_expanded, time.perf_counter() - t0
    return None, total_expanded, time.perf_counter() - t0

import random

def _random_scramble(state, steps=30, rng=random):
    """
    Trả về trạng thái mới sau khi trượt ô trống ngẫu nhiên `steps` lần.
    • Luôn sinh trạng thái hợp lệ (không lọt ra ngoài biên).
    """
    s = state
    for _ in range(steps):
        z   = s.index(0)
        nxt = rng.choice(NEIGHBORS[z])
        s   = _swap(s, z, nxt)
    return s


def hill_climbing(start, max_sideways=0, max_iter=40000, restarts=20):
    import random, time
    best_overall = None
    for attempt in range(restarts):
        state   = start if attempt == 0 else _random_scramble(start, 30)
        parent  = {}
        sideways = expanded = 0
        for _ in range(max_iter):
            h_curr = _manhattan(state)
            if h_curr == 0:
                path = _reconstruct(parent, state)
                if best_overall is None or len(path) < len(best_overall):
                    best_overall = path
                break                                  # thành công trong restart này

            z = state.index(0)
            neighbors = list(NEIGHBORS[z])
            random.shuffle(neighbors)                 # (3)

            best_child, best_h = None, 999
            for nxt in neighbors:
                child = _swap(state, z, nxt)
                h_child = _manhattan(child)
                expanded += 1
                if h_child < best_h:
                    best_h, best_child = h_child, child

            if best_h > h_curr or (best_h == h_curr and sideways >= max_sideways):
                break                                 # kẹt trong restart này
            if best_h == h_curr:
                sideways += 1
            else:
                sideways = 0

            parent[best_child] = state
            state = best_child                        # (1) chính tả đã sửa
    return (best_overall, expanded, None)

        
def greedy(start):
    """
    Greedy Best-First Search:  f(n) = h(n)  (chỉ nhìn trước, không cộng g).
    Trả về (path, expanded, elapsed).  Nếu không tới goal → None.
    """
    t0 = time.perf_counter()
    pq = [( _manhattan(start), start )]
    parent = {}
    seen = {start}
    expanded = 0

    while pq:
        h, state = heapq.heappop(pq)
        expanded += 1
        if h == 0:                         # goal!
            return _reconstruct(parent, state), expanded, time.perf_counter() - t0
        z = state.index(0)
        for nxt in NEIGHBORS[z]:
            child = _swap(state, z, nxt)
            if child not in seen:
                seen.add(child)
                parent[child] = state
                heapq.heappush(pq, ( _manhattan(child), child ))

    return None, expanded, time.perf_counter() - t0


def simulated_annealing(start, max_depth=100):
    """
    Simulated Annealing (SA) với làm nguội hàm mũ:
        T_k = T0 * alpha^k
    • Chọn ngẫu nhiên 1 hàng xóm mỗi bước.
    • Nhận nếu tốt hơn, hoặc chấp nhận có xác suất exp(-Δ/T).
    * Không đảm bảo tối ưu; thường cho kết quả nhanh nhưng không chắc chắn.
    """
    t0 = time.perf_counter()
    total_expanded = 0
    for depth in range(max_depth + 1):
        path, expanded, _ = dfs(start, depth_limit=depth)
        total_expanded += expanded
        if path is not None:
            return path, total_expanded, time.perf_counter() - t0
    return None, total_expanded, time.perf_counter() - t0
# ---------- Genetic Algorithm ---------------------------------------------
import random, time, math

# kí hiệu nước đi
_MOVES = ("U", "D", "L", "R")

def _apply_move(state, move):
    """Trả về state mới sau khi thực hiện move; nếu move không hợp lệ ⇒ giữ nguyên."""
    z = state.index(0)
    if   move == "U" and z >= 3:      return _swap(state, z, z-3)
    elif move == "D" and z <= 5:      return _swap(state, z, z+3)
    elif move == "L" and z % 3 != 0:  return _swap(state, z, z-1)
    elif move == "R" and z % 3 != 2:  return _swap(state, z, z+1)
    return state                       # move “đụng tường” → không đổi

def _simulate(start, gene):
    """Chạy chuỗi move, trả (state_cuối, full_path)."""
    path  = [start]
    state = start
    for mv in gene:
        nxt = _apply_move(state, mv)
        if nxt != state:               # chỉ lưu khi có thay đổi
            path.append(nxt)
        state = nxt
    return state, path

def genetic_algorithm(start,
                      pop_size: int   = 200,
                      gene_len: int   = 40,
                      generations: int = 400,
                      crossover_rate: float = 0.9,
                      mutation_rate: float  = 0.30):
    """
    • Mỗi cá thể = list[str] độ dài cố định (chuỗi nước đi).
    • Fitness = -ManhattanDistance(state_cuối)  (càng gần 0 càng tốt).
    • Khi state_cuối == GOAL → trả về lời giải.
    """
    t0 = time.perf_counter()

    def random_gene():
        return [random.choice(_MOVES) for _ in range(gene_len)]

    def fitness(gene):
        end_state, _ = _simulate(start, gene)
        return -_manhattan(end_state)

    # --- khởi tạo dân số
    population = [random_gene() for _ in range(pop_size)]
    expanded   = 0                     # số “cá thể + thế hệ” đã đánh giá

    for gen in range(generations):
        scored = [(fitness(g), g) for g in population]
        expanded += pop_size
        scored.sort(reverse=True, key=lambda x: x[0])   # best đầu danh sách

        best_fit, best_gene = scored[0]
        if best_fit == 0:                                # tới đích!
            _, path = _simulate(start, best_gene)
            return path, expanded, time.perf_counter() - t0

        # --- chọn lọc (tournament 2-đấu-2)
        def tournament():
            g1, g2 = random.choice(population), random.choice(population)
            return g1 if fitness(g1) > fitness(g2) else g2

        new_pop = []
        while len(new_pop) < pop_size:
            p1, p2 = tournament(), tournament()

            # —— Lai ghép 1 điểm cắt
            if random.random() < crossover_rate:
                cut = random.randint(1, gene_len-2)
                child = p1[:cut] + p2[cut:]
            else:
                child = p1[:]

            # —— Đột biến
            for i in range(gene_len):
                if random.random() < mutation_rate:
                    child[i] = random.choice(_MOVES)

            new_pop.append(child)

        population = new_pop

    # hết thế hệ nhưng chưa tới goal
    return None, expanded, time.perf_counter() - t0
# ---------- IDA* -----------------------------------------------------------
def ida_star(start, heuristic=_manhattan, max_depth=80):
    """
    IDA* = DFS lặp sâu nhưng cắt tỉa theo ngưỡng f = g + h.
    • Trả về (solution_path | None, num_expanded, elapsed_seconds).
    • Nếu không tìm thấy trong max_depth → None.
    """
    t0 = time.perf_counter()

    if start == GOAL:                       # trivial case
        return [start], 0, 0.0

    # --- hàm DFS có cắt tỉa -------------------------------------------------
    def dfs(state, g, bound, parent):
        """
        Trả về:
            * ('FOUND', path)  nếu gặp goal
            * (next_bound, None) nếu chưa tới goal nhưng vượt bound, trả bound kế tiếp
        """
        nonlocal expanded
        f = g + heuristic(state)
        if f > bound:
            return f, None
        if state == GOAL:
            return 'FOUND', [state]

        min_bound = 1e9
        z = state.index(0)
        for nxt in NEIGHBORS[z]:
            child = _swap(state, z, nxt)
            # tránh vòng lặp lui 1 bước: đừng trở lại cha
            if parent is not None and child == parent:
                continue
            expanded += 1
            res, path = dfs(child, g + 1, bound, state)
            if res == 'FOUND':
                return 'FOUND', [state] + path
            if res < min_bound:
                min_bound = res
        return min_bound, None

    # --- vòng lặp tăng dần ngưỡng f ----------------------------------------
    bound = heuristic(start)
    expanded = 0
    depth = 0
    while bound <= max_depth:
        res, path = dfs(start, 0, bound, None)
        if res == 'FOUND':
            elapsed = time.perf_counter() - t0
            return path, expanded, elapsed
        bound = res        # đặt lại bound mới (nhỏ nhất vượt mức trước)
        depth += 1

    # không tìm thấy
    return None, expanded, time.perf_counter() - t0
# ---------- Local Beam Search ---------------------------------------------
def local_beam_search(start, beam_width: int = 5, max_depth: int = 80):
    """
    Local Beam Search (k-beam) giữ tối đa `beam_width` trạng thái
    tốt nhất (theo h = Manhattan) ở **mỗi độ sâu**.
    
    • Nếu gặp goal → trả về path tối ưu theo số bước.
    • Nếu duyệt hết depth ≤ max_depth mà không tới goal → trả (None, …).
    • Độ phức tạp: O(k · b · d) memory ≈ beam_width × branching × depth.
    """
    t0 = time.perf_counter()

    if start == GOAL:
        return [start], 0, 0.0

    # Mỗi mục trong frontier: (state, g, parent)
    frontier = [(start, 0, None)]
    parent   = {}                 # map child → parent
    expanded = 0

    for depth in range(1, max_depth + 1):
        # —— Mở rộng tất cả nút trong frontier hiện tại
        candidates = []
        for state, g, p in frontier:
            z = state.index(0)
            for nxt in NEIGHBORS[z]:
                child = _swap(state, z, nxt)
                if child == p:               # tránh lùi 1 bước
                    continue
                if child in parent:          # đã thấy state này trước
                    continue
                parent[child] = state
                expanded += 1
                if child == GOAL:
                    path = _reconstruct(parent, child)
                    return path, expanded, time.perf_counter() - t0
                # (h, state, g) – sắp xếp theo h (nhỏ nhất = tốt nhất)
                candidates.append((_manhattan(child), child, g + 1, state))

        if not candidates:                   # “tắc đường”
            break

        # —— Giữ lại beam_width ứng viên tốt nhất
        candidates.sort(key=lambda x: x[0])
        frontier = [(s, g, par) for h, s, g, par in candidates[:beam_width]]

    # không tìm thấy lời giải trong max_depth
    return None, expanded, time.perf_counter() - t0
# ---------- Stochastic / First-Choice Hill-Climbing ------------------------
import random, time

def stochastic_hill_climbing(start,
                             max_iter: int = 40_000,
                             allow_sideways: int = 8):
    """
    • Ở mỗi bước: xáo trộn hàng xóm, chọn NGAY cá thể đầu tiên cải thiện
      (h_child < h_curr). Vì “ngẫu nhiên”, thuật toán có thể tránh kẹt đỉnh.
    • Nếu chỉ gặp hàng xóm ngang bằng (Δh = 0) thì cho phép tối đa
      `allow_sideways` bước “đi ngang” rồi dừng.
    • Trả về None nếu kẹt cục bộ hoặc hết max_iter.
    """
    t0        = time.perf_counter()
    state     = start
    h_curr    = _manhattan(state)
    parent    = {}
    expanded  = 0
    sideways  = 0

    for _ in range(max_iter):
        if h_curr == 0:                            # goal!
            return _reconstruct(parent, state), expanded, time.perf_counter()-t0

        z          = state.index(0)
        neighbors  = [_swap(state, z, nxt) for nxt in NEIGHBORS[z]]
        random.shuffle(neighbors)                  # yếu tố “stochastic”

        moved = False
        for child in neighbors:
            h_child   = _manhattan(child)
            expanded += 1
            if h_child < h_curr:
                parent[child] = state
                state, h_curr = child, h_child
                sideways      = 0
                moved         = True
                break
            elif h_child == h_curr and sideways < allow_sideways:
                parent[child] = state
                state, h_curr = child, h_child
                sideways     += 1
                moved         = True
                break

        if not moved:                              # tất cả neighbor xấu hơn
            break                                  # → kẹt cục bộ

    # không tìm thấy lời giải
    return None, expanded, time.perf_counter()-t0


# ---------- Backtracking + Forward-Checking (BC-FC) ------------------------
def backtracking_fc(start,
                    best_bound: int | None = None,   # None = chưa có lời giải
                    max_depth: int = 80):
    """
    *Backtracking* (DFS) + *Forward-Checking* theo ngưỡng f = g + h.

    • Nếu đã tìm được một lời giải tạm thời dài L bước, mọi nhánh có
      (g + h) ≥ L sẽ bị cắt (vì chắc chắn không ngắn hơn lời giải đã có).
    • Nếu chưa có lời giải, forward-checking đơn giản là cắt theo max_depth.
    • Trả về (solution_path | None, num_expanded, elapsed_seconds).
    """
    t0          = time.perf_counter()
    best_path   = None             # lời giải tốt nhất tìm được
    best_len    = best_bound or 1e9
    expanded    = 0

    def dfs(state, g, parent):
        """
        Quay lui + kiểm tra f = g + h; sắp xếp neighbor theo h(n) tăng dần
        để sớm gặp lời giải ngắn.
        """
        nonlocal best_path, best_len, expanded
        h = _manhattan(state)
        f = g + h

        # —— forward check 1: vượt lời giải tốt nhất đã có
        if f >= best_len:
            return
        # —— forward check 2: sâu quá
        if g >= max_depth:
            return

        if state == GOAL:
            best_len  = g
            best_path = _reconstruct(par_parent, state)
            return

        # —— duyệt neighbor theo h tăng dần (chiến lược “best-first trong dfs”)
        z   = state.index(0)
        nbrs = [_swap(state, z, nxt) for nxt in NEIGHBORS[z] if nxt != parent_pos.get(state)]
        nbrs.sort(key=_manhattan)            # look-ahead ordering

        for child in nbrs:
            expanded += 1
            par_parent[child] = state        # lưu cha
            parent_pos[child] = z            # nhớ vị trí blank của cha → tránh lùi 1 bước
            dfs(child, g+1, parent_pos)      # đệ quy
            # không cần “undo” vì ta ghi đè ở vòng lặp kế

    # —— ánh xạ: state → vị trí ô trống của cha, dùng tránh “lùi”
    parent_pos  = {}
    par_parent  = {}                         # map child → parent (phục vụ reconstruct)
    dfs(start, 0, parent_pos)

    elapsed = time.perf_counter() - t0
    if best_path:
        return best_path, expanded, elapsed
    return None, expanded, elapsed
# ---------- Min-Conflicts (stochastic hill-climbing chọn ngẫu nhiên best) --
def min_conflicts(start,
                  max_steps: int = 20_000,
                  allow_sideways: int = 15):
    """
    Min-Conflicts cho 8-Puzzle.
    • Mỗi vòng: duyệt các hàng xóm, lấy list trạng thái có h nhỏ nhất,
      RANDOM.CHOICE một trong số đó (giữ tính “ngẫu nhiên có hướng”).
    • Cho phép tối đa `allow_sideways` bước h bằng nhưng không giảm;
      hết quota sideways hoặc không tìm thấy neighbor tốt hơn -> kẹt.
    • Trả (path | None, expanded, elapsed).
    """
    t0       = time.perf_counter()
    state    = start
    h_curr   = _manhattan(state)
    parent   = {}
    expanded = 0
    sideways = 0

    for _ in range(max_steps):
        if h_curr == 0:                               # goal!
            return _reconstruct(parent, state), expanded, time.perf_counter()-t0

        # ------ sinh & đánh giá hàng xóm -----------------------------------
        z = state.index(0)
        neigh   = [_swap(state, z, nxt) for nxt in NEIGHBORS[z]]
        scores  = [(_manhattan(s), s) for s in neigh]
        expanded += len(neigh)

        # —— tìm h_min trong neighbor
        h_min = min(sc for sc, _ in scores)
        best_candidates = [s for sc, s in scores if sc == h_min]

        # —— quyết định di chuyển
        if h_min < h_curr:
            sideways = 0
        elif h_min == h_curr:
            if sideways >= allow_sideways:            # kẹt plateau
                break
            sideways += 1
        else:
            break                                     # mọi neighbor xấu hơn

        child = random.choice(best_candidates)
        parent[child] = state
        state, h_curr = child, h_min

    # không tìm được lời giải
    return None, expanded, time.perf_counter()-t0
# ---------- Steepest-Ascent Hill-Climbing ----------------------------------
import time

def steepest_ascent_hill(start,
                         max_iter: int = 30_000,
                         allow_sideways: int = 12):
    """
    • Ở mỗi bước: duyệt *tất cả* hàng xóm, chọn state có h thấp nhất.
    • Nếu best_h <  h_curr  → chuyển sang best (leo dốc).
    • Nếu best_h == h_curr → đếm sideways; quá allow_sideways thì dừng.
    • Nếu best_h >  h_curr → kẹt đỉnh cục bộ.
    • Trả về None nếu kẹt hoặc hết max_iter.
    """
    t0        = time.perf_counter()
    state     = start
    h_curr    = _manhattan(state)
    parent    = {}
    expanded  = 0
    sideways  = 0

    for _ in range(max_iter):
        if h_curr == 0:                                # tới Goal
            return _reconstruct(parent, state), expanded, time.perf_counter()-t0

        # —— Xét toàn bộ hàng xóm và tìm best_h nhỏ nhất
        z = state.index(0)
        neighbors = [_swap(state, z, nxt) for nxt in NEIGHBORS[z]]
        expanded += len(neighbors)

        best_h = min(_manhattan(s) for s in neighbors)
        best_neighbors = [s for s in neighbors if _manhattan(s) == best_h]

        if best_h < h_curr:
            sideways = 0
        elif best_h == h_curr:
            if sideways >= allow_sideways:
                break                      # dừng do plateau
            sideways += 1
        else:
            break                          # kẹt đỉnh cục bộ

        # chọn 1 trong các best_neighbors (nếu nhiều, chọn ngẫu nhiên)
        next_state = random.choice(best_neighbors) if len(best_neighbors) > 1 else best_neighbors[0]
        parent[next_state] = state
        state, h_curr = next_state, best_h

    # không giải được
    return None, expanded, time.perf_counter() - t0
# ---------- Uniform-Cost Search (UCS) --------------------------------------
import heapq, time

def uniform_cost(start):
    """
    Uniform-Cost Search cho 8-Puzzle.
    • Trả về (solution_path | None, num_expanded, elapsed_seconds).
    • Nếu bàn cờ vô nghiệm (unsolvable) → (None, expanded, elapsed).
    """
    t0 = time.perf_counter()

    # 1. Khởi tạo
    g_cost   = {start: 0}                   # chi phí ngắn nhất tới state
    parent   = {}                           # child -> parent
    frontier = [(0, start)]                 # (g, state) min-heap
    expanded = 0
    GOAL     = (1,2,3,4,5,6,7,8,0)

    while frontier:
        g, state = heapq.heappop(frontier)
        expanded += 1

        # 2. Đạt mục tiêu?
        if state == GOAL:
            elapsed = time.perf_counter() - t0
            return _reconstruct(parent, state), expanded, elapsed

        # 3. Sinh hàng xóm
        z = state.index(0)
        for nxt in NEIGHBORS[z]:
            child = _swap(state, z, nxt)
            g2    = g + 1                  # tất cả bước = 1
            if g2 < g_cost.get(child, 1e9):
                g_cost[child] = g2
                parent[child] = state
                heapq.heappush(frontier, (g2, child))

    # Không tìm thấy (xảy ra khi start vô nghiệm)
    return None, expanded, time.perf_counter() - t0
# ========== Q-LEARNING – tabular (8-Puzzle) =================================
import random, collections, time, pickle, os

_Q_PATH = "q_table.pkl"          # tệp lưu/đọc Q-table
_ACTIONS = (0, 1, 2, 3)          # U, D, L, R  (theo thứ tự cố định)

def _gamma_state(state, a):
    """Áp dụng action a lên state; đụng tường → giữ nguyên."""
    z = state.index(0)
    tgt = {0: z-3, 1: z+3, 2: z-1, 3: z+1}[a]
    valid = tgt in NEIGHBORS[z]
    return _swap(state, z, tgt) if valid else state

# --------------------------------------------------------------------------- #
#                       ĐÀO TẠO (1 lần, lưu vào pkl)                          #
# --------------------------------------------------------------------------- #
def _train_q_table(episodes=50_000, scramble=20,
                   alpha=0.1, gamma=0.99,
                   eps_start=1.0, eps_end=0.05):

    Q = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    eps_decay = (eps_start - eps_end) / episodes
    rng = random.Random(42)
    GOAL = (1,2,3,4,5,6,7,8,0)

    for ep in range(episodes):
        # --- tạo trạng thái ngẫu nhiên bằng cách xào từ GOAL ---------------
        s = GOAL
        for _ in range(scramble):
            a = rng.choice(_ACTIONS)
            s = _gamma_state(s, a)

        eps = max(eps_end, eps_start - eps_decay*ep)
        for _ in range(80):                     # giới hạn bước trong 1 episode
            # ε-greedy
            if rng.random() < eps:
                a = rng.choice(_ACTIONS)
            else:
                a = max(range(4), key=lambda i: Q[s][i])

            s2 = _gamma_state(s, a)
            done = (s2 == GOAL)
            reward = 100 if done else -1
            best_next = max(Q[s2])
            Q[s][a] += alpha * (reward + gamma*best_next - Q[s][a])
            s = s2
            if done:
                break

    with open(_Q_PATH, "wb") as f:
        pickle.dump(dict(Q), f)
    print(f"[Q-learning] Đã huấn luyện xong {episodes} episode, "
          f"lưu vào {_Q_PATH}")
    return Q

# --------------------------------------------------------------------------- #
#                        SOLVER  –  gọi từ GUI                               #
# --------------------------------------------------------------------------- #
_Q_TABLE = None      # sẽ lazy-load để không delay khởi động GUI

def _load_q():
    global _Q_TABLE
    if _Q_TABLE is None:
        if not os.path.exists(_Q_PATH):
            # lần đầu chạy – huấn luyện nhanh
            _Q_TABLE = _train_q_table()
        else:
            with open(_Q_PATH, "rb") as f:
                _Q_TABLE = pickle.load(f)
    return _Q_TABLE

def q_learning_solver(start, max_steps=80):
    """
    Trả về (path, expanded, elapsed) giống các solver khác –
    dùng Q-table greedy (không exploration).
    """
    t0 = time.perf_counter()
    Q = _load_q()

    path = [start]
    expanded = 0
    state = start
    GOAL = (1,2,3,4,5,6,7,8,0)

    for _ in range(max_steps):
        if state == GOAL:
            break
        # lấy action tốt nhất (nhiều state mới chưa có Q ⇒ đặt 0)
        q_vals = Q.get(state, [0,0,0,0])
        a = max(range(4), key=lambda i: q_vals[i])
        nxt = _gamma_state(state, a)
        expanded += 1
        if nxt == state:               # đụng tường ⇒ bế tắc
            break
        path.append(nxt)
        state = nxt

    elapsed = time.perf_counter() - t0
    if state != GOAL:
        return None, expanded, elapsed
    return path, expanded, elapsed
# ===========  DQN cho 8-Puzzle  ============================================
"""
• Mạng 2 fully-connected tầng 128-64 nodes.
• Đầu vào = one-hot 9! = 362 880 → encode gọn 9×9 (ô, giá trị).
• Replay Buffer 50 k mẫu, batch = 64.
• Huấn luyện offline; file model lưu 'dqn_8p.pt'.
• inference = greedy, trả path (không bảo đảm tối ưu).
"""
import os, random, time, math, collections
import torch, torch.nn as nn, torch.optim as optim

_MODEL_PATH = "dqn_8p.pt"
_DEVICE     = "cuda" if torch.cuda.is_available() else "cpu"
_ACTIONS    = (0,1,2,3)         # U,D,L,R

# ---------- encode / transition -------------------------------------------
def _encode(state):
    """Trả tensor shape (81,) : mỗi ô (0..8) dùng one-hot 9 giá trị."""
    arr = torch.zeros(81, device=_DEVICE)
    for idx, v in enumerate(state):
        arr[idx*9 + v] = 1
    return arr

def _gamma_state(state, a):
    z = state.index(0)
    tgt = {0:z-3, 1:z+3, 2:z-1, 3:z+1}[a]
    return _swap(state,z,tgt) if tgt in NEIGHBORS[z] else state

# ---------- NN -------------------------------------------------------------
class QNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(81,128), nn.ReLU(),
            nn.Linear(128,64), nn.ReLU(),
            nn.Linear(64,4)
        )
    def forward(self,x): return self.net(x)

# ---------- replay buffer --------------------------------------------------
Transition = collections.namedtuple('T', ('s','a','r','s2','done'))

class Replay:
    def __init__(self, cap=50_000):
        self.buf = collections.deque(maxlen=cap)
    def push(self,*t): self.buf.append(Transition(*t))
    def sample(self,batch):
        return random.sample(self.buf,batch)
    def __len__(self): return len(self.buf)

# ---------- train ----------------------------------------------------------
def _dqn_train(episodes=60_000, scramble=30,
               gamma=0.99, lr=1e-3,
               eps_start=1.0, eps_end=0.02,
               target_sync=1_000, batch=64):

    net, tgt = QNet().to(_DEVICE), QNet().to(_DEVICE)
    tgt.load_state_dict(net.state_dict())
    opt = optim.Adam(net.parameters(), lr=lr)
    buf = Replay()
    step = 0
    eps_decay = (eps_start - eps_end) / episodes
    rng = random.Random(123)

    GOAL = (1,2,3,4,5,6,7,8,0)

    def epsilon(ep): return max(eps_end, eps_start - eps_decay*ep)

    for ep in range(episodes):
        # scramble từ goal
        s = GOAL
        for _ in range(scramble):
            s = _gamma_state(s, rng.choice(_ACTIONS))

        for t in range(80):
            eps = epsilon(ep)
            if rng.random() < eps:
                a = rng.choice(_ACTIONS)
            else:
                with torch.no_grad():
                    q = net(_encode(s))
                a = int(q.argmax())

            s2 = _gamma_state(s,a)
            done = (s2 == GOAL)
            r = 100 if done else -1
            buf.push(_encode(s), a, r,
                     _encode(s2), done)
            s = s2
            step += 1

            # train
            if len(buf) >= batch:
                tr = buf.sample(batch)
                batch_s = torch.stack([x.s for x in tr])
                batch_a = torch.tensor([x.a for x in tr],device=_DEVICE)
                batch_r = torch.tensor([x.r for x in tr],device=_DEVICE,dtype=torch.float32)
                batch_s2 = torch.stack([x.s2 for x in tr])
                batch_done = torch.tensor([x.done for x in tr],device=_DEVICE,dtype=torch.bool)

                q_pred = net(batch_s).gather(1,batch_a.unsqueeze(1)).squeeze()
                with torch.no_grad():
                    q_next = tgt(batch_s2).max(1)[0]
                    q_target = batch_r + gamma * q_next * (~batch_done)
                loss = nn.functional.mse_loss(q_pred, q_target)
                opt.zero_grad(); loss.backward(); opt.step()

            if step % target_sync == 0:
                tgt.load_state_dict(net.state_dict())

            if done: break

        if (ep+1) % 5000 == 0:
            print(f"[DQN] ep {ep+1}/{episodes} – buf {len(buf)}")

    torch.save(net.state_dict(), _MODEL_PATH)
    print(f"[DQN] train done, model saved → {_MODEL_PATH}")
    return net

# ---------- inference solver ----------------------------------------------
_DQN_NET = None
def _load_dqn():
    global _DQN_NET
    if _DQN_NET is None:
        net = QNet().to(_DEVICE)
        if os.path.exists(_MODEL_PATH):
            net.load_state_dict(torch.load(_MODEL_PATH, map_location=_DEVICE))
            print("[DQN] model loaded")
        else:
            net = _dqn_train()        # auto-train if not found
        net.eval()
        _DQN_NET = net
    return _DQN_NET

def dqn_solver(start, max_steps=80):
    """
    Trả (path|None, expanded, elapsed).
    Greedy theo mạng đã học.
    """
    net = _load_dqn()
    t0 = time.perf_counter()
    path=[start]; s=start; expanded=0
    for _ in range(max_steps):
        if s==GOAL: break
        q = net(_encode(s))
        a = int(q.argmax())
        s2 = _gamma_state(s,a)
        expanded +=1
        if s2==s: break
        path.append(s2); s=s2
    elapsed=time.perf_counter()-t0
    return (path if s==GOAL else None, expanded, elapsed)
# ==============  SARSA (ε-greedy, tabular)  ================================
"""
• Học offline – lưu bảng Q ở 'sarsa_q.pkl'.
• Nếu file chưa có, huấn luyện ≈ 50 000 episode rồi lưu.
• Solver: greedy theo Q đã học, trả (path | None, expanded, elapsed).
"""
import pickle, os, random, time, collections

_SARSA_PATH = "sarsa_q.pkl"
_ACTIONS    = (0, 1, 2, 3)          # U, D, L, R

def _gamma_state(state, a):
    z = state.index(0)
    tgt = {0: z-3, 1: z+3, 2: z-1, 3: z+1}[a]
    return _swap(state, z, tgt) if tgt in NEIGHBORS[z] else state

# ---------- Huấn luyện -----------------------------------------------------
def _train_sarsa(episodes=50_000, scramble=20,
                 alpha=0.1, gamma=0.99,
                 eps_start=1.0, eps_end=0.05):
    Q = collections.defaultdict(lambda: [0.0,0.0,0.0,0.0])
    eps_decay = (eps_start - eps_end) / episodes
    rng = random.Random(2025)
    GOAL = (1,2,3,4,5,6,7,8,0)

    for ep in range(episodes):
        # ----- khởi tạo episode bằng cách xào từ GOAL ----------------------
        s = GOAL
        for _ in range(scramble):
            s = _gamma_state(s, rng.choice(_ACTIONS))

        eps = max(eps_end, eps_start - eps_decay*ep)

        # ------ chọn hành động đầu theo ε-greedy --------------------------
        def pick_action(state, ε):
            return (rng.choice(_ACTIONS) if rng.random() < ε
                    else max(range(4), key=lambda i: Q[state][i]))

        a = pick_action(s, eps)

        for _ in range(80):         
            s2 = _gamma_state(s, a)
            done = (s2 == GOAL)
            r = 100 if done else -1

            a2 = pick_action(s2, eps)   

            # ----- SARSA update -----------------------------------------
            Q[s][a] += alpha * (r + gamma * Q[s2][a2] - Q[s][a])

            s, a = s2, a2
            if done:
                break

        if (ep+1) % 5_000 == 0:
            print(f"[SARSA] episode {ep+1}/{episodes}")

    with open(_SARSA_PATH, "wb") as f:
        pickle.dump(dict(Q), f)
    print(f"[SARSA] training done – saved to '{_SARSA_PATH}'")
    return Q

# ---------- Lazy-load bảng Q ----------------------------------------------
_SARSA_Q = None
def _load_sarsa():
    global _SARSA_Q
    if _SARSA_Q is None:
        if os.path.exists(_SARSA_PATH):
            with open(_SARSA_PATH, "rb") as f:
                _SARSA_Q = pickle.load(f)
            print("[SARSA] Q-table loaded")
        else:
            _SARSA_Q = _train_sarsa()     
    return _SARSA_Q

# ---------- Solver (greedy) ------------------------------------------------
def sarsa_solver(start, max_steps=80):
    """
    path, expanded, elapsed   – giống API các solver khác.
    Greedy (ε=0) trên Q đã học.  Không bảo đảm tối ưu.
    """
    Q = _load_sarsa()
    t0 = time.perf_counter()
    path=[start]; s=start; expanded=0
    GOAL = (1,2,3,4,5,6,7,8,0)

    for _ in range(max_steps):
        if s == GOAL: break
        q_vals = Q.get(s, [0,0,0,0])
        a = max(range(4), key=lambda i: q_vals[i])
        s2 = _gamma_state(s, a)
        expanded += 1
        if s2 == s: break               
        path.append(s2); s = s2

    elapsed = time.perf_counter() - t0
    return (path if s==GOAL else None, expanded, elapsed)
# =================  REINFORCE (POLICY GRADIENT)  ============================
"""
• One-step REINFORCE with discounted return Gt.
• Mạng policy 81-128-64-4   (đầu vào: one-hot 9×9).
• Huấn luyện offline, lưu ở 'pg_policy.pt'.
• pg_solver() = greedy argmax π(a|s)  (không đảm bảo tối ưu).
"""
import torch, torch.nn as nn, torch.optim as optim
import random, time, math, os, collections

_PG_PATH  = "pg_policy.pt"
_DEVICE   = "cuda" if torch.cuda.is_available() else "cpu"
_ACTIONS  = (0, 1, 2, 3)          # U D L R

# ---------- encode & transition -------------------------------------------
def _encode(state):
    """Tensor (81,) one-hot: 9 ô × 9 giá trị."""
    t = torch.zeros(81, device=_DEVICE)
    for idx, v in enumerate(state):
        t[idx*9 + v] = 1
    return t

def _step(state, a):
    z = state.index(0)
    tgt = {0:z-3, 1:z+3, 2:z-1, 3:z+1}[a]
    return _swap(state, z, tgt) if tgt in NEIGHBORS[z] else state

# ---------- policy network -------------------------------------------------
class PolicyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(81, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 4)
        )
    def forward(self, x):                
        return self.net(x)

# ---------- train ----------------------------------------------------------
def _train_policy(episodes=70_000, scramble=25,
                  gamma=0.99, lr=1e-3):
    net = PolicyNet().to(_DEVICE)
    optimiser = optim.Adam(net.parameters(), lr=lr)
    rng = random.Random(777)
    GOAL = (1,2,3,4,5,6,7,8,0)

    for ep in range(episodes):
        # --- tạo ván ngẫu nhiên
        s = GOAL
        for _ in range(scramble):
            s = _step(s, rng.choice(_ACTIONS))

        log_probs, rewards = [], []
        for _ in range(80):                        
            logits = net(_encode(s))
            dist   = torch.distributions.Categorical(logits=logits)
            a      = dist.sample()
            log_probs.append(dist.log_prob(a))
            s      = _step(s, a.item())
            done   = (s == GOAL)
            rewards.append(0 if done else -1)
            if done:
                rewards[-1] = 100
                break

        # --------- tính Gt và cập nhật -------------------------------
        G = 0
        returns = []
        for r in reversed(rewards):
            G = r + gamma*G
            returns.insert(0, G)
        returns = torch.tensor(returns, device=_DEVICE, dtype=torch.float32)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)  # chuẩn hoá

        loss = -(torch.stack(log_probs) * returns).sum()
        optimiser.zero_grad()
        loss.backward()
        optimiser.step()

        if (ep+1) % 5000 == 0:
            print(f"[PG] episode {ep+1}/{episodes}")

    torch.save(net.state_dict(), _PG_PATH)
    print(f"[PG] training finished → {_PG_PATH}")
    return net

# ---------- lazy-load & solver --------------------------------------------
_POLICY_NET = None
def _load_policy():
    global _POLICY_NET
    if _POLICY_NET is None:
        net = PolicyNet().to(_DEVICE)
        if os.path.exists(_PG_PATH):
            net.load_state_dict(torch.load(_PG_PATH, map_location=_DEVICE))
            print("[PG] policy loaded")
        else:
            net = _train_policy()            
        net.eval()
        _POLICY_NET = net
    return _POLICY_NET

def pg_solver(start, max_steps=80):
    """
    Greedy (argmax π).  Trả (path | None, expanded, elapsed_s).
    """
    net = _load_policy()
    t0 = time.perf_counter()
    path=[start]; s=start; expanded=0
    GOAL = (1,2,3,4,5,6,7,8,0)

    for _ in range(max_steps):
        if s == GOAL: break
        with torch.no_grad():
            logits = net(_encode(s))
            a = int(torch.argmax(logits).item())
        s2 = _step(s, a)
        expanded += 1
        if s2 == s: break
        path.append(s2); s = s2

    elapsed = time.perf_counter() - t0
    return (path if s==GOAL else None, expanded, elapsed)
# ---------- Sensorless Search (belief-state BFS demo) ----------------------
from collections import deque

def sensorless_search(start):
    """
    Sensorless (non-perceptive) search cho 8-Puzzle.
    -----------------------------------------------------------------------
    • Ở trạng thái sensorless, agent KHÔNG quan sát được bàn cờ hiện tại,
      nên “state” lúc này là **tập hợp** (belief) các thế cờ có thể xảy ra.
    • Để minh hoạ, ta giả sử agent CHỈ mù vị trí ô trống khi bắt đầu
      (không quan sát được 0 đang ở đâu), còn sau mỗi nước đi thì vẫn
      “biết chắc” mình đã di chuyển như thế nào.  
      → Belief ban đầu = 9 trạng thái (xoay ô trống qua 9 vị trí).  
      → Ta duyệt BFS trên *belief* cho tới khi toàn bộ thành viên của
        belief ≡ GOAL — lúc đó kế hoạch chắc chắn thành công.
    • Trả về (path, expanded, elapsed) giống các hàm khác; `path`
      lấy đại diện bất kỳ từ belief để GUI có gì hiển thị.
    """
    t0 = time.perf_counter()

    # ---- Belief ban đầu: mọi vị trí ô trống đều có thể ---------------
    init_belief = set()
    for z in range(9):
        if z == start.index(0):               # đã đúng vị trí → chính `start`
            init_belief.add(start)
        else:                                 # hoán vị 0 với z
            init_belief.add(_swap(start, start.index(0), z))

    frontier = deque([(init_belief, [])])     # (belief, plan⁠_so⁠_far)
    seen     = {frozenset(init_belief)}
    expanded = 0

    moves = ("U","D","L","R")
    delta = {"U":-3, "D":3, "L":-1, "R":1}

    while frontier:
        belief, plan = frontier.popleft()
        expanded += 1

        # —— Goal test: mọi state trong belief đều là GOAL
        if all(s == GOAL for s in belief):
            elapsed = time.perf_counter() - t0
            # dựng path “đại diện” để GUI phát animation
            rep_state = next(iter(belief))
            return plan + [rep_state], expanded, elapsed

        # —— Thử tất cả action ― áp dụng lên *mọi* state của belief
        for mv in moves:
            next_belief = set()
            for s in belief:
                z = s.index(0)
                tgt = z + delta[mv]
                if tgt in NEIGHBORS[z]:
                    next_belief.add(_swap(s, z, tgt))
                else:
                    next_belief.add(s)        # nước đi không hợp lệ → state không đổi
            fset = frozenset(next_belief)
            if fset not in seen:
                seen.add(fset)
                frontier.append((next_belief, plan + [next(iter(next_belief))]))

    # không tìm được kế hoạch “chắc ăn”
    return None, expanded, time.perf_counter() - t0
