import tkinter as tk
from tkinter import messagebox
from board import MinesweeperBoard

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
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn

    def reset_game(self):
        self.board = MinesweeperBoard(self.rows, self.cols, self.num_mines)
        self.status_label.config(text=f"Mines: {self.num_mines}")
        self.metrics_label.config(text="BFS ready")
        for (r, c), btn in self.buttons.items():
            btn.config(
                text="",
                relief=tk.RAISED,
                bg="#E0E0E0",
                fg="black",
            )

    def on_left_click(self, r, c):
        status, cells, metrics = self.board.reveal_cell(r, c)

        if status == "ignored":
            return

        if status == "mine":
            self._show_mines(cells)
            return

        self._render_revealed_cells(cells)
        self.metrics_label.config(
            text=f"BFS: {metrics['cells_revealed']} cells | {metrics['execution_time_ms']} ms"
        )

        if status == "win":
            self.status_label.config(text="Victory! All safe cells cleared.")
            messagebox.showinfo("Victory!", "Congratulations! All safe cells have been cleared.")

    def _show_mines(self, cells):
        for mr, mc in cells:
            self.buttons[(mr, mc)].config(
                text="*", bg="#EF5350", fg="white", relief=tk.SUNKEN
            )
        self.status_label.config(text="Game Over! Hit a mine.")
        messagebox.showinfo("Game Over", "Boom! You hit a mine. Try again!")

    def _render_revealed_cells(self, cells):
        for cr, cc in cells:
            val = self.board.grid[cr][cc]
            btn = self.buttons[(cr, cc)]
            btn.config(
                text=str(val) if val > 0 else "",
                relief=tk.SUNKEN,
                bg="#FAFAFA",
                fg=NUMBER_COLORS.get(val, "black"),
            )


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = MinesweeperApp(root, rows=10, cols=10, num_mines=12)
    root.mainloop()