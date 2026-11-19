import tkinter as tk
from board import MinesweeperBoard

REVEAL_DELAY_MS = 18
BACKGROUND = "#F1F5F9"
INK = "#172554"
MUTED = "#475569"
COVERED = "#BFDBFE"
REVEALED = "#F8FAFC"
FLAGGED = "#FDE68A"
MINE = "#FECACA"
BOARD_BACKGROUND = "#94A3B8"

NUMBER_COLORS = {
    1: "#1976D2",
    2: "#388E3C",
    3: "#D32F2F",
    4: "#7B1FA2",
    5: "#92400E",
    6: "#0097A7",
    7: "#424242",
    8: "#475569",
}


class MinesweeperApp:
    def __init__(self, root, rows=10, cols=10, num_mines=12):
        self.root = root
        self.root.title("BFSWeeper - Minesweeper with BFS Reveal")
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines

        root.configure(bg=BACKGROUND, padx=20, pady=18)

        header = tk.Frame(root, bg=BACKGROUND)
        header.pack(fill=tk.X)
        tk.Label(
            header, text="BFSweeper", bg=BACKGROUND, fg=INK,
            font=("TkDefaultFont", 22, "bold"),
        ).pack(side=tk.LEFT)
        restart = tk.Label(
            header, text="Restart", bg="#1D4ED8", fg="white",
            font=("TkDefaultFont", 11, "bold"), padx=14, pady=7,
            takefocus=True, highlightthickness=2,
            highlightbackground=BACKGROUND, highlightcolor=INK,
        )
        restart.pack(side=tk.RIGHT)
        for gesture in ("<Button-1>", "<space>", "<Return>"):
            restart.bind(gesture, lambda event: self.reset_game())
        restart.bind("<Enter>", lambda event: restart.configure(bg="#1E40AF"))
        restart.bind("<Leave>", lambda event: restart.configure(bg="#1D4ED8"))

        counters = tk.Frame(root, bg=BACKGROUND)
        counters.pack(fill=tk.X, pady=(10, 8))
        self.counts_label = tk.Label(counters, bg=BACKGROUND, fg=INK)
        self.counts_label.pack(side=tk.LEFT)
        self.progress_label = tk.Label(counters, bg=BACKGROUND, fg=INK)
        self.progress_label.pack(side=tk.RIGHT)

        self.board_frame = tk.Frame(root, bg=BOARD_BACKGROUND, padx=1, pady=1)
        self.board_frame.pack()

        self.status_label = tk.Label(
            root, bg=BACKGROUND, fg=INK, font=("TkDefaultFont", 12, "bold"),
        )
        self.status_label.pack(pady=(10, 2))
        self.metrics_label = tk.Label(root, bg=BACKGROUND, fg=MUTED)
        self.metrics_label.pack()
        tk.Label(
            root, text="Click to reveal · Right-click or Control-click to flag",
            bg=BACKGROUND, fg=MUTED,
        ).pack(pady=(8, 0))

        self.reveal_job = None
        self.tiles = {}
        self.board = None
        self._build_grid_ui()
        self.reset_game()

    def _build_grid_ui(self):
        for r in range(self.rows):
            for c in range(self.cols):
                tile = tk.Label(
                    self.board_frame, width=3, height=1, padx=2, pady=3,
                    font=("TkFixedFont", 14, "bold"), takefocus=True,
                    highlightthickness=2, highlightcolor="#1D4ED8",
                )
                for gesture in ("<Button-1>", "<space>", "<Return>"):
                    tile.bind(
                        gesture,
                        lambda event, row=r, col=c: self.on_left_click(row, col),
                    )
                for gesture in ("<Button-3>", "<Button-2>", "<Control-Button-1>", "<Key-f>"):
                    tile.bind(
                        gesture,
                        lambda event, row=r, col=c: self.on_flag_click(row, col),
                    )
                tile.grid(row=r, column=c, padx=1, pady=1)
                self.tiles[(r, c)] = tile

    def _paint_tile(self, r, c, text, background, foreground=INK):
        self.tiles[(r, c)].config(
            text=text, bg=background, fg=foreground, highlightbackground=background,
        )

    def reset_game(self):
        if self.reveal_job is not None:
            self.root.after_cancel(self.reveal_job)
            self.reveal_job = None
        self.board = MinesweeperBoard(self.rows, self.cols, self.num_mines)
        self._update_counts()
        self._update_progress()
        self.status_label.config(text="Choose a tile to start", fg=INK)
        self.metrics_label.config(text="BFS ready")
        for r, c in self.tiles:
            self._paint_tile(r, c, "", COVERED)

    def _update_counts(self):
        self.counts_label.config(
            text=f"Mines {self.num_mines}   ·   Flags {len(self.board.flagged)}"
        )

    def _update_progress(self):
        safe_cells = self.rows * self.cols - self.num_mines
        self.progress_label.config(text=f"Revealed {len(self.board.revealed)} / {safe_cells}")

    def on_flag_click(self, r, c):
        if self.reveal_job is None and self.board.toggle_flag(r, c):
            if (r, c) in self.board.flagged:
                self._paint_tile(r, c, "⚑", FLAGGED, "#78350F")
            else:
                self._paint_tile(r, c, "", COVERED)
            self._update_counts()
        return "break"

    def on_left_click(self, r, c):
        if self.reveal_job is not None:
            return
        status, cells, metrics = self.board.reveal_cell(r, c)

        if status == "ignored":
            return

        if status == "mine":
            self._show_mines(cells, (r, c))
            return

        self.metrics_label.config(
            text=f"BFS: {metrics['cells_revealed']} cells | {metrics['execution_time_ms']} ms"
        )

        self.status_label.config(text="Revealing tiles…", fg=INK)
        self._animate_reveal(iter(cells), status == "win")

    def _animate_reveal(self, cells, won):
        cell = next(cells, None)
        if cell is not None:
            self._render_revealed_cell(*cell)
            self.reveal_job = self.root.after(REVEAL_DELAY_MS, self._animate_reveal, cells, won)
            return

        self.reveal_job = None
        self._update_progress()
        if won:
            self.status_label.config(text="Victory · All safe tiles cleared", fg="#166534")
        else:
            self.status_label.config(text="Choose a tile", fg=INK)

    def _show_mines(self, cells, hit):
        for r, c in cells:
            self._paint_tile(r, c, "✹", MINE, "#991B1B")
        self._paint_tile(*hit, "✹", "#B91C1C", "#FFFFFF")
        self.status_label.config(text="Game over · You hit a mine", fg="#991B1B")

    def _render_revealed_cell(self, r, c):
        value = self.board.grid[r][c]
        self._paint_tile(r, c, str(value) if value else "", REVEALED, NUMBER_COLORS.get(value, INK))
