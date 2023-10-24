import pygame
from pygame.locals import *
import random

class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10, randomize: bool = False): # конструктор
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed
        self.grid = self.create_grid(randomize)
        self.live = False
        self.gen = 0 #отображать поколения

    def print_matrix(self):#вывести матрицу состояний ячеек в консоль
        for k in range(len(self.grid)):
            for p in range(len(self.grid[k])):
                print((p, k), end ="")
            print()

    def draw_lines(self):#Отрисовка сетки
        pygame.init()
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (0, y), (self.width, y))
    
    def run(self) -> None: #Зацикленная игра
        pygame.display.set_caption('Game of Life: -- Закрасьте поля и нажмите Return --')
        pygame.init()
        clock = pygame.time.Clock()
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN: # при клике на ячейку она оживает до игры
                    pos = event.pos
                    self.add_cell(pos)
                if event.type == pygame.KEYDOWN: # для старта нажмите ентер
                    if event.key == pygame.K_RETURN:
                        self.live = True #Начать отрисовывать следующие состояния через функцию get_next_generation
                        pygame.display.set_caption(f'Game of Life: -- Для выхода нажмите Q --')
                    if event.key == pygame.K_q:
                        running = 0
            self.draw_lines()
            self.draw_grid()
            if self.live:
                prevgrid = self.grid
                if self.grid == self.get_next_generation():
                    print("GAME HAS ENDED ON THE GENERATION: ", self.gen)
                    self.live = 0
                self.gen = self.gen + 1
                pygame.display.set_caption(f'Game of Life: поколение {self.gen} -- Для выхода нажмите Q --')
                self.grid = self.get_next_generation()
                if prevgrid == self.get_next_generation():
                    print("GAME HAS ENDED ON THE GENERATION: ", self.gen)
                    self.live = 0
            pygame.display.flip()
            clock.tick(self.speed)

    def add_cell(self ,pos: tuple): #Оживить ячейку
        self.grid[pos[1] // self.cell_size][pos[0] // self.cell_size] = 1

    def create_grid(self, randomize: bool=False):#Начальное состояние поля 
        grid = []

        for i in range(self.cell_height):
            grid.append([])
            for j in range(self.cell_width):
                if randomize:
                    grid[i].append(random.randint(0,1))
                else:
                    grid[i].append(0)
        return grid
    
    def draw_grid(self):#Отрисочка поля
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color("White"), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color("Black"), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
        
    def get_neighbours(self, cell: tuple):#Получить соседние клетки для переданной
        neigh = []

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if len(self.grid) - 1 > y > 0 and len(self.grid[y]) - 1 > x > 0:  
                    if abs(cell[0] - x) <= 1 and abs(cell[1] - y) <= 1 and cell != (x,y):
                        neigh.append((x,y))
                else:
                    if abs(cell[0] - x) <= 1 and abs(cell[1] - y) <= 1 and cell != (x,y):
                        neigh.append((x,y))
                    elif len(self.grid[y]) - 2 <= abs(cell[0] + x) <= len(self.grid[y]) and len(self.grid) - 2 <= abs(cell[1] + y) <= len(self.grid):
                        neigh.append((x,y))
        return neigh
    
    def get_next_generation(self): #просчитать следующий кадр
        nextgrid = []
        for y in range(len(self.grid)):
            nextgrid.append([])
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 1 and 2 <= len([cell for cell in self.get_neighbours((x, y)) if self.grid[cell[1]][cell[0]] == 1]) <= 3:
                    nextgrid[y].append(1)
                elif self.grid[y][x] == 0 and len([cell for cell in self.get_neighbours((x, y)) if self.grid[cell[1]][cell[0]] == 1]) == 3:
                    nextgrid[y].append(1)
                else:
                    nextgrid[y].append(0)
        return nextgrid


def menu():
    while(1):
        ans = input("""1 - Задать размер экрана: 
2 - Задать размер клетки:
3 - Задать скорость:
4 - Случайная генерация начальных клеток:
5 - Использовать рекомендованные настройки: 
************ДЛЯ ЗАВЕРШЕНИЯ ВВОДА ВВЕДИТЕ 0**************\n""")
        match ans:
            case '1':
                try:
                    width = int(input("\nВведите ширину экрана: "))
                    height = int(input("\nВведите высоту экрана: "))
                    print("-----DONE-----")
                except:
                    print("******ЧТО-ТО ПОШЛО НЕ ТАК. ПОВТОРИТЕ ВВОД ВХОДНЫХ ДАННЫХ********")
            case '2':
                try:
                    cell_size = int(input("\nВведите размер клетки: "))
                    print("-----DONE-----")
                except:
                    print("******ЧТО-ТО ПОШЛО НЕ ТАК. ПОВТОРИТЕ ВВОД ВХОДНЫХ ДАННЫХ********")
            case '3':
                try:
                    speed = int(input("\nВведите желаемую скорость генерации новых поколений: "))
                    print("-----DONE-----")
                except:
                    print("******ЧТО-ТО ПОШЛО НЕ ТАК. ПОВТОРИТЕ ВВОД ВХОДНЫХ ДАННЫХ********")
            case '4':
                try:
                    randomize = int(input("\n0 - Выключить случайню генерацию начального состояния клеток\n1 - Включить случайную генерацию начального состояния клеток: "))
                    print("-----DONE-----")
                except:
                    print("******ЧТО-ТО ПОШЛО НЕ ТАК. ПОВТОРИТЕ ВВОД ВХОДНЫХ ДАННЫХ********")
            case '5':
                width = 1080
                height = 940
                cell_size = 40
                speed = 140
                randomize = 1
                print("-----DONE-----")
            case '0':
                break
            case _:
                print("\n*******Что-то пошло не так. Повторите ввод номера параметра******")
    try:
        return (width, height, cell_size, speed, randomize)
    except:
        print("******ЧТО-ТО ПОШЛО НЕ ТАК. ПОВТОРИТЕ ВВОД ВХОДНЫХ ДАННЫХ********")
if __name__ == '__main__':
    ans = menu()
    game = GameOfLife(ans[0], ans[1], ans[2], ans[3], ans[4]) #Ширина Высота Рзамер ячейки ФПС Рандомная начальная позиция
    game.run()