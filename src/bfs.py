from collections import deque
import time

# 8 arah ketetanggaan pada grid (horizontal, vertikal, diagonal)
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


def bfs_reveal(grid, rows, cols, start_r, start_c, revealed):
    """
    Menjalankan Breadth-First Search (BFS) dari titik (start_r, start_c)
    untuk membuka seluruh sel kosong (nilai 0) yang terhubung beserta
    sel perbatasan yang memiliki angka petunjuk.
    """
    start_time = time.perf_counter()
    newly_revealed = []
    queue = deque([(start_r, start_c)])
    visited = set(revealed)
    visited.add((start_r, start_c))
    nodes_visited = 0

    while queue:
        r, c = queue.popleft()
        nodes_visited += 1
        newly_revealed.append((r, c))

        # Ekspansi tetangga hanya dilakukan jika sel saat ini bernilai 0
        if grid[r][c] == 0:
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                    if grid[nr][nc] != -1:  # Pastikan tidak membuka ranjau
                        visited.add((nr, nc))
                        queue.append((nr, nc))

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    metrics = {
        "nodes_visited": nodes_visited,
        "cells_revealed": len(newly_revealed),
        "execution_time_ms": round(elapsed_ms, 4),
    }
    return newly_revealed, metrics