from math import sqrt
import time
import sys

debug = False

def read_pizza(filename):
    '''
        Czyta wejście, działa, olać
    '''
    with open(filename) as f:
        lines = f.readlines()
        R, C, L, H = [int(it) for it in lines[0].split(' ')]
        pizza = [list(it.rstrip()) for it in lines[1:]]
        return R, C, L, H, pizza

def print_solution(slices):
    '''
        printuje rozwiązanie, działa, olać
    '''
    print(len(slices))
    for slice in slices:
        print(' '.join(map(str, slice)))

def print_available(available):
    for y in available:
        for x in y:
            print('-' if x else '+', end=' ')
        print()

R, C, L, H, pizza = read_pizza(sys.argv[1])

def divisors(n):
    '''
    input:
            n - pole kwadratu
    output:
      t - tablica zawierająca wszystkie możliwe prostokąty wewnątrz danego kwadratu
    '''
    t = []
    for i in range(1, int(sqrt(n)) + 1):
        if n % i == 0: 
            t.append(i)
            t.append(n//i)
    return t

def rects(area):
    '''
        zwraca zbiór wszystkich możliwych prostokątów utworzonych z danego kwadratu
    '''
    return {(it, area // it) for it in divisors(area)}

def is_valid(slice):
    '''
        sprawdza czy dany prostokąt spełnia założenia zadania dla jednego kawałka
    '''
    y0, x0, y1, x1 = slice
    toma = 0
    mush = 0
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if pizza[y][x] == 'T': toma += 1
            if pizza[y][x] == 'M': mush += 1
    return toma >= L and mush >= L

def rect_candidates(area):
    '''
        zwraca możliwe kawałki dla danych rozmiarów prostokątów
    '''
    cand = {}
    for rect in rects(area):
        w, h = rect
        for y in range(0, R - h +1):
            for x in range(0, C - w +1):
                if rect not in cand: cand[rect] = []
                cand[rect].append((y, x, y+h-1, x+w-1))
    return cand

def valid_rects(area):
    '''
        zwraca wszystkie kawałki spełniające założenia zadania
    '''
    return {k: [it for it in v if is_valid(it)] for k, v in rect_candidates(area).items()}

def is_available(available, slice):
    y0, x0, y1, x1 = slice
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not available[y][x]:
                return False
    return True

def marked(available, slice):
    y0, x0, y1, x1 = slice
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            available[y][x] = False

def result():
    available = []
    for y in range(R):
        available.append([])
        for x in range(C):
            available[y].append(True)

    answer = []
    for area in range(H, L*2 -1, -1):
        if debug:
            print(area)
        for slices in valid_rects(area).values():
            for slice in slices:
                if is_available(available, slice):
                    marked(available, slice)
                    #print('adding:', slice)
                    #print_available(available)
                    answer.append(slice)
    return answer, available

def used(taken):
    sum = 0
    for row in taken:
        for col in row:
            if col == False:
                sum += 1
    return sum

t0 = time.time()
solution, taken = result()
print_solution(solution)
if debug:
    s = used(taken)
    print("score =", s, 100*s/(C*R), '%')
    print("time =", time.time() - t0, "sec")

