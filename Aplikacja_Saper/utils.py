import global_vars as g

""" zwraca liste koordynatów sąsiadów komórki (i, j)"""
def neighbours(i, j):

    list = []
    for (x, y) in [ (i-1, j-1), (i-1, j), (i-1, j+1),   #sprawdzanie z lewej, po ukosie, z gory itd.
                    (i, j-1), (i, j+1),
                    (i+1, j-1), (i+1, j), (i+1, j+1)]:
        if x in range(g.HEIGHT) and y in range(g.WIDTH): #sprawdzanie czy zawiera sie w gridzie
            list.append((x, y))
    return list



"""obsługa wyjątków"""
def set_parameters(argv):

    #czy wartosc argumentow jest rozna od 3
    if len(argv) != 3:
        if len(argv) != 0:
            print("Nieprawidłowe wartości")
            print("Potrzeba 3 argumentow (wysokość, szerokość, ilość bomb)")
        return

    #czy parametry są liczbą
    try:
        height = int(argv[0])
        width = int(argv[1])
        bombs = int(argv[2])
    except ValueError:
        print("Nieprawidłowe wartości")
        print("Argumenty muszą być liczbą")
        return

    #czy podane wartosci są obsługiwane
    if  height <= 0 or width <= 0 or bombs <= 0 or bombs >= height*width:
        print("Nieprawidłowe wartości")
        print("Nie można utworzyć gry z podanymi parametrami")
        return

    g.HEIGHT = height
    g.WIDTH = width
    g.BOMBS = bombs
    g.BOMBS_LEFT = bombs