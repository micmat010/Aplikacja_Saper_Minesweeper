import tkinter as tk
import sys
import classes as cls
import gui
import utils


utils.set_parameters(sys.argv[1:])

GRID = cls.Grid()
GRID.add_bombs()

window = gui.create_main_window()
window.title("Saper")
window.iconbitmap('images/logo.ico')

flag, mine = gui.create_images()
BOARD = gui.create_board(window, GRID, flag, mine)
top_frame = gui.create_top_frame(window, GRID, BOARD)

tk.mainloop()