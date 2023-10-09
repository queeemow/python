import random
import pathlib

def create_grid(puzzle: str):
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid

def group(values: list, n: int):
    lis1 = []

    for i in range(0, n):
            lis1.append([])
            for j in range(0,n):
                 lis1[i].append(values[i*n + j])
    return lis1

grid = ("""53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79""")

truGrid = create_grid(grid)

def display(lis: list):
     print("\n\n\n")
     for i in range(0, len(lis)):
        for j in range(0, len(lis[i])):
            print(lis[i][j], end = "   ")
            if (j + 1) % 3 == 0 and j % 8 != 0:
             print("|", end = "   ")
        print("\n")
        if(i + 1) % 3 == 0 and i != len(lis)-1:
            print("-----------------------------------------")


def getcol(puzzle: list, pos:tuple):
    lis = []

    for i in range(0, len(puzzle)):
        if puzzle[i][pos[1]] != '.':
            lis.append(puzzle[i][pos[1]])
    return lis


def getrow(puzzle: list, pos:tuple):
    return [k for k in puzzle[pos[0]] if k != '.']


def getblock(puzzle: list, pos:tuple): #ужас
    lis = []
    if pos[0] < 3:
        if pos[1] < 3:
            for i in range(0,3):
                for j in range(0,3):
                    if  puzzle[i][j] != '.':
                        lis.append(puzzle[i][j])
            return lis
        if 6 > pos[1] >= 3:
            for i in range(0,3):
                for j in range(3,6):
                    if  puzzle[i][j] != '.':
                        lis.append(puzzle[i][j])
            return lis
        if pos[1] >= 6:
            for i in range(0,3):
                for j in range(6,9):
                    if  puzzle[i][j] != '.':
                        lis.append(puzzle[i][j])
            return lis
    if 6 > pos[0] >= 3:
        if pos[1] < 3:
            for i in range(3,6):
                for j in range(0,3):
                    if  puzzle[i][j] != '.':
                        lis.append(puzzle[i][j])
            return lis
        if 6 > pos[1] >= 3:
            for i in range(3,6):
                for j in range(3,6):
                    if  puzzle[i][j] != '.':
                        lis.append(puzzle[i][j])
            return lis
        if pos[1] >= 6:
            for i in range(3,6):
                for j in range(6,9):
                    if  puzzle[i][j] != '.':
                        lis.append(puzzle[i][j])
            return lis
    if pos[0] >= 6:
        if pos[1] < 3:
            for i in range(6,9):
                for j in range(0,3):
                    if puzzle[i][j] != '.':
                        lis.append(puzzle[i][j])
            return lis
        if 6 > pos[1] >= 3:
            for i in range(6,9):
                for j in range(3,6):
                    if  puzzle[i][j] != '.':
                        lis.append(puzzle[i][j])
            return lis
        if pos[1] >= 6:
            for i in range(6,9):
                for j in range(6,9):
                    if  puzzle[i][j] != '.':
                        lis.append(puzzle[i][j])
            return lis

def find_empty_position(grid: list):
    for i in range(0,len(grid)):
        for j in range(0, len(grid[i])):
            if grid[i][j] == '.':
                return (i,j)
    return 0

def find_possible_values(grid: list, pos: tuple):
    vals = set(str(i) for i in range(1,10))
    col = set(i for i in getcol(grid, pos))
    row = set(i for i in getrow(grid, pos))
    block = set(i for i in getblock(grid, pos))

    return (vals - col) & (vals - row) & (vals - block)


def solve(grid: list):
    pass

def check_solution(grid: list):
    a = set(str(i) for i in range(1,10))
    for i in range(0, 9):
        for j in range(0, 9):
            if not set(getcol(grid ,(i,j))) == a or not set(getrow(grid ,(i,j))) == a or not set(getblock(grid ,(i,j))) == a:
                print("---------INCORRECT SOLUTION OF THE GIVEN SUDOKU GRID--------")
                return
    print("---------SUDOKU WAS SOLVED CORRECTLY--------")

def generate_grid(n: int):
    trugrid = create_grid('.' * 81)
    used = [(random.randint(0, 8), random.randint(0,8))]
    p = 0
    f = n
    while p <= n:
        pos1 = (random.randint(0, 8), random.randint(0,8))
        if used[p] != (pos1):
            used.append(pos1)
            p = p + 1

    for k in range(0, n):
        pos = used[k]
        if len(find_possible_values(trugrid, pos)) > 0:
            trugrid[pos[0]][pos[1]] = list((find_possible_values(trugrid, pos)))[random.randint(0, len(find_possible_values(trugrid, pos)) - 1)] #баг в этой строке в индексе возможных значений
        else: 
            n = n + 1
            continue
    if n != f:
        print("количество пропущенных позиций = ".upper(), n - f)
    return trugrid

def read_sudoku(path: str):
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)

display(read_sudoku("puzzle3.txt"))
