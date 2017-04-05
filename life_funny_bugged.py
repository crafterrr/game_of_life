import pygame
from pygame.locals import *
import random
import time

class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
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

    def cell_list(self, randomize=True):
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1.
        В противном случае клетка считается мертвой, то
        есть ее значение равно 0.
        Если параметр randomize = True, то создается список, где
        каждая клетка может быть равновероятно живой или мертвой.
        """
        if randomize is True:
            self.cell_states = [[random.choice([True, False])
                                 for x in range(0, self.cell_width)] for y in range(0, self.cell_height)]
        else:
            self.cell_states = [[True for x in range(0, self.cell_width)] for y in range(0, self.cell_height)]
            # print(self.cell_states)
            # print('A')

    def draw_cell_list(self, rects):
        """
        Отображение списка клеток 'rects' с закрашиванием их в
        соответствующе цвета
        """
        for row in range(0, len(rects)):
            for col in range(0, len(rects[row])):
                x = col
                y = row
                # print(x,y)
                x *= self.cell_size
                y *= self.cell_size
                if rects[row][col] is True:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, self.cell_size, self.cell_size))
                    # print(x, y)
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, self.cell_size, self.cell_size))

    def check_neighbours(self, x, y):
        nei_count = 0
        xs = x - 1
        xf = x + 2
        ys = y - 1
        yf = y + 2
        if (x == 0):
            xs = x
        elif (x == len(self.cell_states[0]) - 1):
            xf = x + 1
        if (y == 0):
            ys = y
        elif (y == len(self.cell_states) - 1):
            yf = y + 1
        # print(ys,yf, xs, xf)
        for row in range(ys, yf):
            for col in range(xs, xf):
                if self.cell_states[row][col] is True:
                    nei_count += 1
        if self.cell_states[y][x] is True and nei_count > 0:
            nei_count -= 1
        return nei_count

    def refresh(self):
        self.updated_states = self.cell_states[:][:]
        for row in range(0, len(self.cell_states)):
            for col in range(0, len(self.cell_states[row])):
                # print(row,col)
                nbours = self.check_neighbours(col, row)
                # print(nbours)
                if nbours < 2:
                    self.updated_states[row][col] = (False)
                elif nbours == 3:
                    self.updated_states[row][col] = (True)
                elif nbours > 3:
                    self.updated_states[row][col] = (False)
                else:
                    self.updated_states[row][col] = (self.cell_states[row][col])
        self.cell_states = self.updated_states[:][:]


    def run(self):
        pygame.init()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.cell_list()
        # self.refresh()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.cell_states)
            pygame.display.flip()
            time.sleep(0.05)
            self.refresh()
        pygame.quit()


if __name__ == '__main__':
    game = GameOfLife(1000, 500, 20)
    game.run()
