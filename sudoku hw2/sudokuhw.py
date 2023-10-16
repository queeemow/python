import random
import pathlib
import math

grid = """53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79"""

lilgrid = """.2..
4..1
3...
...2"""

def group(values: list, n: int): #преобразовать одномерный список в двумерный
    matrix = []

    for i in range(0, n):
        matrix.append([])
        for j in range(0,n):
            matrix[i].append(values[i*n + j])
    return matrix

def create_grid(puzzle: str): #преобразовать строку в матрицу
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, int(math.sqrt(len(puzzle.replace(" ", "").replace("\n", "")))))
    return grid

def display(grid: list): #отобразить матрицу
    print("\n\n\n")
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(grid[i][j], end = "   ")
            if (j + 1) % int(math.sqrt(len(grid))) == 0 and j % (len(grid) - 1) != 0:
                print("|", end = "   ")
        if(i + 1) % int(math.sqrt(len(grid))) == 0 and i != len(grid)-1:
                print()
                print("----------"* int(len(grid)/2))
        else:
            print("\n")

display(create_grid(lilgrid))

def getcol(puzzle: list, pos:tuple): # получить все значения из стобца указанной позиции
    col = []

    for i in range(len(puzzle)):
        if puzzle[i][pos[1]] != '.':
            col.append(puzzle[i][pos[1]])
    return col

def getrow(puzzle: list, pos:tuple): # получить все значения из строки указанной позиции
    return [k for k in puzzle[pos[0]] if k != '.']


def getblock(puzzle: list, pos:tuple): #ужас # получить все значения из блока указанной позиции
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

def find_empty_position(grid: list): #найти первую по порядку свободную позицию в матрице
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                return (i,j)
    return 0

print(getblock(create_grid(lilgrid), (1,1)))

def find_possible_values(grid: list, pos: tuple): #найти возмоные для данной свободной позиции значения
    vals = set(str(i) for i in range(1, len(grid) + 1))
    col = set(i for i in getcol(grid, pos))
    row = set(i for i in getrow(grid, pos))
    block = set(i for i in getblock(grid, pos))

    return (vals - col) & (vals - row) & (vals - block)

def solve(grid1: list): #решить судоку
    print("\n\nНЕ РАБОТАЕТ!")
    pass


def check_solution(grid: list): #проверить решение
    alldigits = set(str(i) for i in range(1, len(grid) + 1))
    for i in range(len(grid)):
        for j in range(len(grid)):
            if not set(getcol(grid ,(i,j))) == alldigits or not set(getrow(grid ,(i,j))) == alldigits or not set(getblock(grid ,(i,j))) == alldigits:
                print("---------INCORRECT SOLUTION OF THE GIVEN SUDOKU GRID--------")
                return
    print("---------SUDOKU WAS SOLVED CORRECTLY--------")

def generate_grid(n: int): #сгенеририровать новую нерешенную матрицу #работает неправильно, поскольку для правильной генерации необходима написанная функция solve()
    trugrid = create_grid('.' * 81)
    used = [(random.randint(0, len(grid) - 1), random.randint(0, len(grid) - 1))]
    p = 0
    f = n
    while p < n:
        pos1 = (random.randint(0, len(grid) - 1), random.randint(0, len(grid) - 1))
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

def read_sudoku(path: str): # прочитать матрицу из указанного файла
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)

def menu():
    ext = 1
    while(ext):
        print("\n\n\n\n--------Домашнее задание 2: Судоку----------\n\n\n\n")
        print("1 - Прочитать матрицу из файла в данной директории \n2 - Отобразить матрицу \n3 - Решить судоку(не работает)")
        ans = input("\n\n*******ДЛЯ ВЫХОДА ВВЕДИТЕ 0*******\n")
        match ans:
            case '1':
                name = input("\nВведите название файла: ")
                try:
                    matrix = read_sudoku(name)
                except FileNotFoundError:
                    print("\n!!!!!!!Введите корректное название файла!!!!!!!")
            case '2':
                display(matrix)
            case '3': 
                solve(matrix)
            case '0':
                ext = 0
                break
            case _:
                print("\nВведите корректный ответ")

if __name__ == "__main__":
    menu()
    pass