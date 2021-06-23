#MODEL

#klasa kwadracika - Square
# - definiujemy koordynaty
# - definiujemy funkcje reset pola
# - definiujemy funkcje reveal, czyli odkryte pole
#klasa grid- Grid
# -wypelnianie kwadracikami
# - wypelnianie bombami

import random
import utils
import global_vars as g #dostarczamy stamtad te zmienne --> g.WIDTH, g.HEIGHT, g.BOMBS

""" pojedynczy kwadracik na gridzie """
class Square():

    def __init__(self, x, y):  #ustawiamy koordy kwadracika
        self.x = x
        self.y = y
        self.reset() #ustawiamy mu wartosci poczatkowe

    def reset(self): #ustawia wartosci poczatkowe
        self.is_bomb = False #czy pole jest z bombą
        self.revealed = False #czy odkryte
        self.bombs_around = 0 #ilosc sąsiadów 

    def reveal(self): #ustawia tylko parametr reveal na 1
        self.revealed = True
        return (self.is_bomb, self.bombs_around)

""" grid z kwadracikami """
class Grid():

    def __init__(self):
        #tab: List[List[Square]] - wypelnia siatke z list obiektem square
        self.tab = [[Square(i, j)   for j in range(g.WIDTH)]   #wysokosc i szerokosc importowane z global_vars.py
                                    for i in range(g.HEIGHT)]

    def reset(self):
        for line in self.tab:
            for sq in line: #petla leci po lini i potem po osobnym kwadraciku po kolei
                sq.reset()  #resetuje wartosci (funkcja reset z klasy Square)

    """ wypelnianie gridu bombami """
    def add_bombs(self):

        if g.BOMBS <= 0 or g.BOMBS >= g.HEIGHT*g.WIDTH:
            raise Exception("Nieprawidłowa liczba bomb!")
        else:
            #https://docs.python.org/3/library/random.html
            #sample wybiera losowo 0 lub 1 z siatki, drugi parametr to ilość wyborów, czyli g.BOMBS

            pos = random.sample([(i, j) for j in range(g.WIDTH) 
                                        for i in range (g.HEIGHT)]
                                ,g.BOMBS)


            for (i, j) in pos:                             #bierzemy "pos" czyli liste z pozycjami bomb
                self.tab[i][j].is_bomb = True              #ustawiamy wartosc pola z siatki na 1 czyli bomba
                for (i2, j2) in utils.neighbours(i, j):    #DODAWANIE SĄSIEDNIM KOMÓRKOM INFORMACJI ZE SĄSIADUJĄ Z BOMBĄ
                    self.tab[i2][j2].bombs_around += 1     #(zwiekszamy liczbe pokazującą liczbe sasiednich bomb)