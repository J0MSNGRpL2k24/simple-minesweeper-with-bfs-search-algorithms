import tkinter as tk
from tkinter import messagebox
from board import MinesweeperBoard

REVEAL_DELAY_MS = 18

NUMBER_COLORS = {
    1: "#1976D2",
    2: "#388E3C",
    3: "#D32F2F",
    4: "#7B1FA2",
    5: "#FF8F00",
    6: "#0097A7",
    7: "#424242",
    8: "#9E9E9E",
}


class MinesweeperApp:
    def __init__(self, root, rows=10, cols=10, num_mines=12):
        self.root = root
        self.root.title("BFSWeeper - Minesweeper with BFS Reveal")
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines

        self.top_frame = tk.Frame(root, pady=8)
        self.top_frame.pack()

        self.status_label = tk.Label(
            self.top_frame,
            text=f"Mines: {self.num_mines} | BFS Ready",
            font=("Consolas", 11, "bold"),
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.reset_btn = tk.Button(
            self.top_frame,
            text="Restart",
            font=("Consolas", 10, "bold"),
            command=self.reset_game,
        )
        self.reset_btn.pack(side=tk.RIGHT, padx=10)

        self.metrics_label = tk.Label(root, font=("Consolas", 10))
        self.metrics_label.pack()

        self.board_frame = tk.Frame(root, padx=10, pady=10)
        self.board_frame.pack()

        tk.Label(root, text="Click to reveal · Right-click or Control-click to flag").pack()

        self.reveal_job = None
        self.buttons = {}
        self.board = None
        self._build_grid_ui()
        self.reset_game()

    def _build_grid_ui(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.board_frame,
                    width=3,
                    height=1,
                    font=("Consolas", 12, "bold"),
                    relief=tk.RAISED,
                    command=lambda row=r, col=c: self.on_left_click(row, col),
                )
                for gesture in ("<Button-3>", "<Button-2>", "<Control-Button-1>"):
                    btn.bind(gesture, lambda event, row=r, col=c: self.on_flag_click(row, col))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn

    def reset_game(self):
        if self.reveal_job is not None:
            self.root.after_cancel(self.reveal_job)
            self.reveal_job = None
        self.board = MinesweeperBoard(self.rows, self.cols, self.num_mines)
        self._update_counts()
        self.metrics_label.config(text="BFS ready")
        for btn in self.buttons.values():
            btn.config(
                text="",
                relief=tk.RAISED,
                bg="#E0E0E0",
                fg="black",
            )

    def _update_counts(self):
        self.status_label.config(
            text=f"Mines: {self.num_mines} | Flags: {len(self.board.flagged)}"
        )

    def on_flag_click(self, r, c):
        if self.reveal_job is None and self.board.toggle_flag(r, c):
            flagged = (r, c) in self.board.flagged
            self.buttons[(r, c)].config(
                text="⚑" if flagged else "",
                fg="#B45309" if flagged else "black",
            )
            self._update_counts()
        return "break"

    def on_left_click(self, r, c):
        if self.reveal_job is not None:
            return
        status, cells, metrics = self.board.reveal_cell(r, c)

        if status == "ignored":
            return

        if status == "mine":
            self._show_mines(cells)
            return

        self.metrics_label.config(
            text=f"BFS: {metrics['cells_revealed']} cells | {metrics['execution_time_ms']} ms"
        )

        self._animate_reveal(iter(cells), status == "win")

    def _animate_reveal(self, cells, won):
        cell = next(cells, None)
        if cell is not None:
            self._render_revealed_cell(*cell)
            self.reveal_job = self.root.after(REVEAL_DELAY_MS, self._animate_reveal, cells, won)
            return

        self.reveal_job = None
        if won:
            self.status_label.config(text="Victory! All safe cells cleared.")
            messagebox.showinfo("Victory!", "Congratulations! All safe cells have been cleared.")

    def _show_mines(self, cells):
        for mr, mc in cells:
            self.buttons[(mr, mc)].config(
                text="*", bg="#EF5350", fg="white", relief=tk.SUNKEN
            )
        self.status_label.config(text="Game Over! Hit a mine.")
        messagebox.showinfo("Game Over", "Boom! You hit a mine. Try again!")

    def _render_revealed_cell(self, r, c):
        value = self.board.grid[r][c]
        self.buttons[(r, c)].config(
            text=str(value) if value > 0 else "",
            relief=tk.SUNKEN,
            bg="#FAFAFA",
            fg=NUMBER_COLORS.get(value, "black"),
        )


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = MinesweeperApp(root, rows=10, cols=10, num_mines=12)
    root.mainloop()