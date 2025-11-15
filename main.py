from queue import PriorityQueue

import pygame

pygame.init()

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 930
NODE_SIZE = 30
ROWS = SCREEN_HEIGHT // NODE_SIZE
COLUMNS = SCREEN_WIDTH // NODE_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Pathfinder Visualization')

WHITE = (255, 255, 255)
CHARCOAL_BLACK = (20, 20, 20)
EMERALD_GREEN = (0, 200, 120)
CRIMSON_RED = (220, 50, 70)
AQUA_BLUE = (0, 180, 255)
ROYAL_PURPLE = (140, 85, 255)
GOLD = (255, 200, 0)
GRAY = (180, 180, 180)

class Node:
    def __init__(self, row, column, width):
        self.row = row
        self.column = column
        self.x = column * width
        self.y = row * width
        self.color = WHITE
        self.width = width
        self.height = width
        self.neighbours = []

    def getPosition(self):
        return self.row, self.column

    def isClosed(self):
        return self.color == ROYAL_PURPLE

    def isOpen(self):
        return self.color == AQUA_BLUE

    def isBarrier(self):
        return self.color == CHARCOAL_BLACK

    def isStart(self):
        return self.color == EMERALD_GREEN

    def isEnd(self):
        return self.color == CRIMSON_RED

    def reset(self):
        self.color = WHITE

    def makeStart(self):
        self.color = EMERALD_GREEN

    def makeClosed(self):
        self.color = ROYAL_PURPLE

    def makeOpen(self):
        self.color = AQUA_BLUE

    def makeBarrier(self):
        self.color = CHARCOAL_BLACK

    def makeEnd(self):
        self.color = CRIMSON_RED

    def makePath(self):
        self.color = GOLD

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def updateNeighbours(self, grid):
        self.neighbours = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.column].isBarrier():
            self.neighbours.append(grid[self.row + 1][self.column])

        if self.row > 0 and not grid[self.row - 1][self.column].isBarrier():
            self.neighbours.append(grid[self.row - 1][self.column])

        if self.column < COLUMNS - 1 and not grid[self.row][self.column + 1].isBarrier():
            self.neighbours.append(grid[self.row][self.column + 1])

        if self.column > 0 and not grid[self.row][self.column - 1].isBarrier():
            self.neighbours.append(grid[self.row][self.column - 1])

    def __lt__(self, other):
        return False

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def createGrid():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(COLUMNS):
            node = Node(i, j, NODE_SIZE)
            grid[i].append(node)
    return grid

def drawGrid(screen):
    for i in range(ROWS):
        pygame.draw.line(screen, GRAY, (0, i * NODE_SIZE), (SCREEN_WIDTH, i * NODE_SIZE))

    for j in range(COLUMNS):
        pygame.draw.line(screen, GRAY, (j * NODE_SIZE, 0), (j * NODE_SIZE, SCREEN_HEIGHT))


def draw(screen, grid):
    screen.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(screen)

    drawGrid(screen)
    pygame.display.update()


def getPositionFromClick(position):
    x, y = position

    row = y // NODE_SIZE
    column = x // NODE_SIZE

    return row, column

def reconstructPath(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.makePath()
        draw()

def ASTAR(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = distance(start.getPosition(), end.getPosition())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstructPath(came_from, end, draw)
            end.makeEnd()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + distance(neighbour.getPosition(), end.getPosition())

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.makeOpen()

        draw()

        if current != start:
            current.makeClosed()

    return False

def main(screen, width):
    grid = createGrid()

    start = None
    end = None

    is_running = True
    started = False

    while is_running:
        draw(screen, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, column = getPositionFromClick(position)
                node = grid[row][column]

                if not start:
                    start = node
                    start.makeStart()

                elif not end:
                    end = node
                    end.makeEnd()

                elif node != end and node != start:
                    node.makeBarrier()

            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, column = getPositionFromClick(position)
                node = grid[row][column]
                node.reset()

                if node == start:
                    start = None

                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbours(grid)

                    ASTAR(lambda: draw(screen, grid), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = createGrid()


    pygame.quit()

main(screen, SCREEN_WIDTH)