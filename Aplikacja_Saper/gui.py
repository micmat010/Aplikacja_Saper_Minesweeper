import tkinter as tk
import tkinter.font as tkf
import time
import classes as cls
import utils
import handlers
import global_vars as g

def create_main_window():
    window = tk.Tk()  # glowne okienko
    window["bg"] = "white"  # tło
    window.resizable(width=False, height=False)  # stały rozmar
    return window

# ładowanie obrazków
def create_images():
    flag = tk.PhotoImage(file="images/red_flag.gif")
    mine = tk.PhotoImage(file="images/mine.gif")
    return (flag, mine)

# game frame
def create_board(window, GRID, flag, mine):
    """wygląd kwadracika"""
    # https://www.tutorialspoint.com/python/tk_relief.htm
    # https://stackoverflow.com/questions/39416021/border-for-tkinter-label
    game_frame = tk.Frame(window, borderwidth=2, relief=tk.SUNKEN)

    def create_square(i, j):
        """frame"""
        f = tk.Frame(game_frame, height=30, width=30)

        """przyciski"""
        s = tk.Button(f, borderwidth=1, state="normal",
                      disabledforeground="#000000")
        s.pack(fill=tk.BOTH, expand=True)

        # pack - wypełnia okienko przyciskami nie zostawiając wolnej przestrzeni
        # https://www.tutorialspoint.com/python/tk_pack.htm

        def __handler(event, x=i, y=j):
            """bindowanie przycisków"""
            if event.num == 1:
                if(g.LOADED==1):
                    handlers.left_handler(GRID, BOARD, i, j, mine)
            elif event.num == 3:
                if(g.LOADED==1):
                    handlers.right_handler(GRID, BOARD, i, j, flag)
            else:
                raise Exception('Problem z odczytem przycisku myszy!')
        
        s.bind("<Button-1>", __handler)
        s.bind("<Button-3>", __handler)

        f.pack_propagate(False)
        f.grid(row=i, column=j)
        return s

    """frame z kwadracikami """
    BOARD = [[create_square(i, j) for j in range(g.WIDTH)]
             for i in range(g.HEIGHT)]

    game_frame.pack(padx=10, pady=10, side=tk.BOTTOM)
    return BOARD

def create_top_frame(window, grid, board):
    top_frame = tk.Frame(window, borderwidth=2, height=40, relief=tk.GROOVE)
    top_frame.pack(padx=0, pady=0, side=tk.TOP, fill="x")

    for i in range(4):
        top_frame.columnconfigure(i, weight=1)

    # tutaj wstawianie wszystkich elementów
    create_bombs_counter(top_frame)
    create_new_game_button(top_frame, grid, board)
    create_new_difficulty_button(top_frame, grid, board)
    create_time_counter(top_frame)
    return top_frame


def create_bombs_counter(top_frame):
    """licznik  pozostalych bomb, to tylko wyswietla dla  (BOMBS_LEFT)"""
    bombs_counter_str = tk.StringVar()

    # StringVar
    # https://stackoverflow.com/questions/51783852/what-is-the-difference-between-a-variable-and-stringvar-of-tkinter/51785046

    def update_bombs_counter():
        bombs_counter_str.set(g.BOMBS_LEFT)
        top_frame.after(100, update_bombs_counter)

    update_bombs_counter()

    # wyswietlenie labelu
    bombs_counter = tk.Label(top_frame, height=1, width=4, bg='white',
                             textvariable=bombs_counter_str,
                             font=tkf.Font(weight='bold', size=10))
    bombs_counter.grid(row=0, column=0, padx=5, sticky=tk.W)


def create_new_game_button(top_frame, grid, board):
    """przycisk nowej gry, middle left"""

    def _start_new_game(g=grid, b=board):
        handlers.start_new_game(grid, board)

    # wyswietlenie przycisku
    newgame_button = tk.Button(top_frame, bd=1, width=15, text="Nowa gra", state='disabled',
                               command=_start_new_game)
    newgame_button.grid(row=0, column=1, padx=0, sticky=tk.E)


def create_new_difficulty_button(top_frame, grid, board):
    """wybieranie poziomu trudnosci, middle right"""
    new_button = tk.Button(top_frame, bd=1, width=15, text="Poziom trudnosci",
                           command=lambda: openNewWindow(top_frame, grid, board))
    new_button.grid(row=0, column=3, padx=0, sticky=tk.W)


# TIMER
def create_time_counter(top_frame):
    """timer"""
    time_counter_str = tk.StringVar()

    def update_time_counter():
        top_frame.after(100, update_time_counter);
        if(g.TIMER==1): time_counter_str.set(int((time.time() - g.INIT_TIME) // 1))

    update_time_counter();

    """lejbel timera"""
    time_counter = tk.Label(top_frame, height=1, width=4, bg='white',
                            textvariable=time_counter_str,
                            font=tkf.Font(slant='italic', size=10))
    time_counter.grid(row=0, column=4, padx=5, sticky=tk.E)

def openNewWindow(top_frame, grid, board):
    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Toplevel()

    # sets the title of the
    # Toplevel widget
    newWindow.title("Poziom trudności")

    # sets the geometry of toplevel
    newWindow.geometry("280x100+330+330")
    newWindow.iconbitmap('images/logo2.ico')

    # A Label widget to show in toplevel
    tk.Label(newWindow,
             text="Wybierz poziom trudności:").pack()

    tk.Button(newWindow, bd=1, width=15, text="Łatwy - 20 bomb", command=lambda: set_diff(0, top_frame, grid, board, newWindow)).pack()
    tk.Button(newWindow, bd=1, width=15, text="Średni - 24 bomby", command=lambda: set_diff(1, top_frame, grid, board, newWindow)).pack()
    tk.Button(newWindow, bd=1, width=15, text="Trudny - 28 bomb", command=lambda: set_diff(2, top_frame, grid, board, newWindow)).pack()
    
#ustaw poziom trudnosci, zaladuj przycisk Nowa gra ponownie
def set_diff(x, top_frame, grid, board, newWindow):
    
    diff = x
    
    def _start_new_game(g=grid, b=board):
        handlers.start_new_game(grid, board)
    
    newgame_button = tk.Button(top_frame, bd=1, width=15, text="Nowa gra", command=_start_new_game)
    newgame_button.grid(row=0, column=1, padx=0, sticky=tk.E)

    if diff == 0:
        g.BOMBS_LEFT = g.BOMBS = 20
        newWindow.destroy()
        handlers.start_new_game(grid, board)
        return diff

    elif diff == 1:
        g.BOMBS_LEFT = g.BOMBS = 24
        newWindow.destroy()
        handlers.start_new_game(grid, board)
        return diff

    elif diff == 2:
        g.BOMBS = g.BOMBS_LEFT = 28
        newWindow.destroy()
        handlers.start_new_game(grid, board)
        return diff

#pokaż całą mapę
def reveal_all(grid, board, mine):
    
     for i in range (g.HEIGHT):
        for j in range (g.WIDTH):
            
            if board[i][j]["image"] == "" and not grid.tab[i][j].revealed:      #po kliknięciu - sprawdzamy czy przycisk wcześniej niewciśnięty
                board[i][j]["state"] = "disabled"                               #dajemy ze wciśniety - disabled
                board[i][j]["relief"] = tk.SUNKEN                               #dajemy motyw (wyglądu)
        
                if grid.tab[i][j].is_bomb:                                      #PRZYPADEK 1 - BOMBA:
                    board[i][j]["image"] = mine                                 #jeśli na kliknietym polu jest bombą to dajemy obrazek
                    board[i][j]["state"] = "normal"
 

                else:                                                           #PRZYPADEK 2 - BEZ BOMBY:
                    grid.tab[i][j].revealed = True                              #dodajemy "odkryte pole"
                    g.SQUARES_REVEALED += 1                                     #dodajemy +1 ilosc odkrytych pól
                    if grid.tab[i][j].bombs_around != 0:                            #SUBPRZYPADEK 1 - jeśli jest jakas bobma dookoła pola (i,j)
                        board[i][j]["text"] = grid.tab[i][j].bombs_around           #TO dodajemy na nim tekst- liczbe sąsiadujących bomb (bombs_around klasa Square)