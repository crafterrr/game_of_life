import pygame
from pygame.locals import *
import numpy
import time


class Cell:
    def __init__(self, x, y, state=1):
        self.x = x
        self.y = y
        self.state = state
        self.ncount = 0

    def refresh(self):
        if self.ncount < 2:
            self.state = 0
        elif self.ncount == 3:
            self.state = 1
        elif self.ncount > 3:
            self.state = 0


class CellList:
    def __init__(self, cell_width, cell_height, randomize=0.5):
        """
                    Создание списка клеток.

                    Клетка считается живой, если ее значение равно 1.
                    В противном случае клетка считается мертвой, то
                    есть ее значение равно 0.
                    Если параметр randomize = True, то создается список, где
                    каждая клетка может быть равновероятно живой или мертвой.
                    """
        self.i = -1
        self.j = 0
        self.cell_width = cell_width
        self.cell_height = cell_height
        if randomize is not False:
            self.cells = [[Cell(x, y, numpy.random.choice([1, 0],
                            p=[randomize, 1 - randomize]))
                           for x in range(0, cell_width)]
                          for y in range(0, cell_height)]
        else:
            f = open('data.txt', 'r')
            states = [s for s in f.read() if s in '10']
            self.cells = []
            for y in range(0, cell_height):
                self.cells.append([])
                for x in range(0, cell_width):
                    try:
                        self.cells[y].append\
                            (Cell(x, y, int(states[y * cell_width + x])))
                    except IndexError:
                        self.cells[y].append(Cell(x, y, 0))
                print(states)

    def refresh(self):
        def set_neighbours(cell):
            nei_count = 0
            xs = cell.x - 1
            xf = cell.x + 2
            ys = cell.y - 1
            yf = cell.y + 2
            if (cell.x == 0):
                xs = cell.x
            elif (cell.x == self.cell_width - 1):
                xf = cell.x + 1
            if (cell.y == 0):
                ys = cell.y
            elif (cell.y == self.cell_height - 1):
                yf = cell.y + 1
            # print(ys,yf, xs, xf)
            for row in range(ys, yf):
                for col in range(xs, xf):
                    if self.cells[row][col].state == 1:
                        nei_count += 1
            if cell.state == 1 and nei_count > 0:
                nei_count -= 1
            cell.ncount = nei_count

        for cell in self:
            set_neighbours(cell)
        for cell in self:
            cell.refresh()

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.cell_height - 1:
            self.i += 1
        elif self.j < self.cell_width - 1:
            self.j += 1
            self.i = 0
        else:
            self.i = -1
            self.j = 0
            raise StopIteration
        return self.cells[self.i][self.j]


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=20):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        self.speed = 1 / speed
        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.clist = CellList(self.cell_width, self.cell_height, False)
        # print(self.cell_width)
        # print(self.cell_height)

    def draw_grid(self):
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_cell_list(self, rects):
        """
        Отображение списка клеток 'rects' с закрашиванием их в
        соответствующе цвета
        """
        for cell in rects:
            x = self.cell_size * cell.x
            y = self.cell_size * cell.y
            if cell.state == 1:
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 (x + 1, y + 1, self.cell_size - 1,
                                  self.cell_size - 1))
                # print(cell.x, cell.y)
            else:
                pygame.draw.rect(self.screen, pygame.Color('white'),
                                 (x + 1, y + 1, self.cell_size - 1,
                                  self.cell_size - 1))
                # print(cell.x,cell.y)

    def refresh(self):
        self.clist.refresh()

    def run(self):
        pygame.init()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.draw_grid()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_cell_list(self.clist)
            pygame.display.flip()
            time.sleep(self.speed)
            self.refresh()
        pygame.quit()


if __name__ == '__main__':
    game = GameOfLife(1200, 600, 20, 8)
    game.run()
