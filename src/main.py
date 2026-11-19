import tkinter as tk
from ui import MinesweeperApp


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = MinesweeperApp(root, rows=10, cols=10, num_mines=12)
    root.mainloop()
