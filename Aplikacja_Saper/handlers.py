import tkinter as tk
from tkinter import messagebox
import sys
import time
import gui
import global_vars as g
import utils

def left_handler(grid, board, i, j, mine):
    """OBSLUGA LEWEGO PRZYCISKU MYSZY NA POLE (i, j)"""

    if board[i][j]["image"] == "" and not grid.tab[i][j].revealed:      #po kliknięciu - sprawdzamy czy przycisk wcześniej niewciśnięty
        board[i][j]["state"] = "disabled"                               #dajemy ze wciśniety - disabled
        board[i][j]["relief"] = tk.SUNKEN                               #dajemy motyw (wyglądu)

        if grid.tab[i][j].is_bomb:                                      #PRZYPADEK 1 - BOMBA:
            board[i][j]["image"] = mine                                 #jeśli na kliknietym polu jest bombą to dajemy obrazek
            board[i][j]["state"] = "normal"
            end_game(False, grid, board, mine)                                #end_game(win=false/true, grid, board) - przekazujemy ze nie wygrano

        # jeśli odkryte pole to sprawdzamy czy bomby dookoła i tu jest ta logika odkrywania
        # reszty pustych pól dalej do momentu aż będzie pole sąsiadujące z bombami

        else:                                                           #PRZYPADEK 2 - BEZ BOMBY:
            grid.tab[i][j].revealed = True                              #dodajemy "odkryte pole"
            g.SQUARES_REVEALED += 1                                     #dodajemy +1 ilosc odkrytych pól
            if grid.tab[i][j].bombs_around != 0:                            #SUBPRZYPADEK 1 - jeśli jest jakas bobma dookoła pola (i,j)
                board[i][j]["text"] = grid.tab[i][j].bombs_around           #TO dodajemy na nim tekst- liczbe sąsiadujących bomb (bombs_around klasa Square)

            else:                                                           #SUBPRZYPADEK 2 - jesli nie ma bomby dookoła
                for (x, y) in utils.neighbours(i, j):                       #lecimy pętlą po wszystkich polach w gridzie
                    left_handler(grid, board, x, y, mine)                   #funkcja zmienia wartosci pól na odkryte (automatycznie juz bez klikania na nie) (pierwszy if w funkcji)

            if g.SQUARES_REVEALED == (g.WIDTH * g.HEIGHT - g.BOMBS):        #SUBPRZYPADEK 3 - jesli wszystki pola bez bomb są odkryte to
                end_game(True, grid, board, mine)                                 #przekazujemy ze wygrano, end_game(win=false/true, grid, board)



def right_handler(grid, board, i, j, flag):
    """OBSLUGA PRAWEGO PRZYCISKU MYSZY NA POLE (i, j)"""

    #jeli pole bez flagi - dodaj flagę
    if not grid.tab[i][j].revealed:
        if board[i][j]["image"] == "":
            board[i][j]["image"] = flag
            board[i][j]["state"] = "normal"
            g.BOMBS_LEFT -= 1      #postawiono flagę, odejmujemy liczbe pozostalych bomb (wyswietlane potem dla usera)
    
        
        #jesli pole oflagowanie - zdejmujemy flagę
        else:
            board[i][j]["state"] = "disabled"
            board[i][j]["image"] = ""
            g.BOMBS_LEFT += 1

#win = True/False, zatrzymanie timera
def end_game(win, grid, board, mine):
    g.TIMER=0
    gui.reveal_all(grid, board, mine)
    
    if win:
        title = "Zakończono"
        msg = "Wygrałeś grę."
    else:
        title = "Zakończono"
        msg = "Przegrałeś grę."

    messagebox.showinfo(title, msg)

#nowa gra
def start_new_game(grid, board):

    #resetujemy wlasciwosci przyciskow na gridzie
    for x in range(g.HEIGHT):
        for y in range(g.WIDTH):
            grid.tab[x][y].reset()
            board[x][y]["image"] = ""
            board[x][y]["text"] = ""
            board[x][y]["state"] = tk.DISABLED
            board[x][y]["relief"] = tk.RAISED
            

    #dajemy znow domyslne wartosci z global_vars
    grid.add_bombs()
    g.SQUARES_REVEALED = 0
    g.BOMBS_LEFT = g.BOMBS
    g.INIT_TIME = time.time()
    g.TIMER = 1
    g.LOADED=1