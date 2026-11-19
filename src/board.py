import random
from bfs import bfs_reveal, DIRECTIONS


class MinesweeperBoard:
    def __init__(self, rows=10, cols=10, num_mines=12):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.mines = set()
        self.revealed = set()
        self.game_over = False
        self.won = False
        self._place_mines()
        self._calculate_numbers()

    def _place_mines(self):
        all_coords = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        self.mines = set(random.sample(all_coords, self.num_mines))
        for r, c in self.mines:
            self.grid[r][c] = -1  # -1 menandakan ranjau

    def _calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:
                    continue
                count = 0
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in self.mines:
                        count += 1
                self.grid[r][c] = count

    def reveal_cell(self, r, c):
        """
        Membuka sel (r, c) menggunakan BFS jika sel aman.
        Mengembalikan tuple (status, newly_revealed, metrics).
        """
        if self.game_over or (r, c) in self.revealed:
            return "ignored", [], None

        if (r, c) in self.mines:
            self.game_over = True
            self.won = False
            return "mine", list(self.mines), None

        newly_revealed, metrics = bfs_reveal(
            self.grid, self.rows, self.cols, r, c, self.revealed
        )
        self.revealed.update(newly_revealed)

        total_safe_cells = (self.rows * self.cols) - self.num_mines
        if len(self.revealed) == total_safe_cells:
            self.game_over = True
            self.won = True
            return "win", newly_revealed, metrics

        return "safe", newly_revealed, metrics