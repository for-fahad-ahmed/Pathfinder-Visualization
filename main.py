import pygame
import tkinter as tk
from queue import PriorityQueue
from queue import Queue


pygame.init()

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 930
NODE_SIZE = 30
ROWS = SCREEN_HEIGHT // NODE_SIZE
COLUMNS = SCREEN_WIDTH // NODE_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Pathfinder Visualization')

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (0, 200, 120)
RED = (220, 50, 70)
BLUE = (0, 180, 255)
PURPLE = (140, 85, 255)
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
        return self.color == PURPLE

    def isOpen(self):
        return self.color == BLUE

    def isBarrier(self):
        return self.color == BLACK

    def isStart(self):
        return self.color == GREEN

    def isEnd(self):
        return self.color == RED

    def reset(self):
        self.color = WHITE

    def makeStart(self):
        self.color = GREEN

    def makeClosed(self):
        self.color = PURPLE

    def makeOpen(self):
        self.color = BLUE

    def makeBarrier(self):
        self.color = BLACK

    def makeEnd(self):
        self.color = RED

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

def show_instructions():
    root = tk.Tk()
    root.title("Key Mapping")
    root.geometry("450x220")
    instructions = [
        "KEY MAPPING:",
        "Left Click  - Place Start, End and Barriers",
        "Right Click - Remove node",
        "A - Run A* algorithm",
        "B - Run BFS algorithm",
        "D - Run DFS algorithm",
        "C - Clear the grid",
        "\n*After reading, Please close this window to proceed"
    ]
    for i, line in enumerate(instructions):
        label = tk.Label(root, text=line, font=("Arial", 12))
        label.pack(anchor="w")
    root.mainloop()

show_instructions()


def displayStats(screen, algorithm_name, nodes_visited, path_length):
    font = pygame.font.Font(None, 32)

    stats_text = f"{algorithm_name} | Nodes Visited: {nodes_visited} | Path Length: {path_length}"
    text_surface = font.render(stats_text, True, BLACK)

    background = pygame.Surface((len(stats_text) * 12 + 20, 45))
    background.set_alpha(200)
    background.fill((220, 220, 220))

    screen.blit(background, (10, 10))
    screen.blit(text_surface, (15, 15))


def h_score(p1, p2):
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

def drawGridLines(screen):
    for i in range(ROWS):
        pygame.draw.line(screen, GRAY, (0, i * NODE_SIZE), (SCREEN_WIDTH, i * NODE_SIZE))

    for j in range(COLUMNS):
        pygame.draw.line(screen, GRAY, (j * NODE_SIZE, 0), (j * NODE_SIZE, SCREEN_HEIGHT))


def draw(screen, grid, stats=None):
    screen.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(screen)

    drawGridLines(screen)

    if stats:
        displayStats(screen, stats['name'], stats['visited'], stats['path'])

    pygame.display.update()


def getPositionOfClick(position):
    x, y = position

    row = y // NODE_SIZE
    column = x // NODE_SIZE

    return row, column

def reconstructPath(came_from, current, draw):
    path_length = 0
    while current in came_from:
        current = came_from[current]
        current.makePath()
        path_length += 1
        draw()

    return path_length

def a_star(draw, grid, start, end):
    no_of_nodes_visited = 0
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = h_score(start.getPosition(), end.getPosition())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, 0, 0

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path_length = reconstructPath(came_from, end, draw)
            end.makeEnd()
            start.makeStart()
            return True, no_of_nodes_visited, path_length

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h_score(neighbour.getPosition(), end.getPosition())

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.makeOpen()

        draw()

        if current != start:
            current.makeClosed()
            no_of_nodes_visited += 1

    return False, no_of_nodes_visited, 0

def bfs(draw, grid, start, end):
    no_of_nodes_visited = 0
    visited = [[False for _ in range(COLUMNS)] for _ in range(ROWS)]
    came_from = {}

    to_be_visited = Queue()
    to_be_visited.put(start)
    visited[start.row][start.column] = True

    while not to_be_visited.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, 0, 0

        current = to_be_visited.get()

        if current == end:
            path_length = reconstructPath(came_from, end, draw)
            end.makeEnd()
            start.makeStart()
            return True, no_of_nodes_visited, path_length


        for neighbour in current.neighbours:
            row, col = neighbour.row, neighbour.column

            if not visited[row][col]:
                visited[row][col] = True
                came_from[neighbour] = current
                to_be_visited.put(neighbour)

                if neighbour != end:
                    neighbour.makeOpen()

        draw()

        if current != start:
            current.makeClosed()
            no_of_nodes_visited += 1

    return False, no_of_nodes_visited, 0


def dfs(draw, grid, start, end):
    no_of_nodes_visited = 0
    stack = [start]
    visited = set()
    came_from = {}

    while len(stack) > 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, 0, 0

        current = stack.pop()

        if current not in visited:
            visited.add(current)

            if current == end:
                path_length = reconstructPath(came_from, current, draw)
                end.makeEnd()
                start.makeStart()
                return True, no_of_nodes_visited, path_length

            for neighbour in current.neighbours:
                if neighbour not in visited:
                    stack.append(neighbour)
                    came_from[neighbour] = current

                    if neighbour != end:
                        neighbour.makeOpen()

            if current != start:
                current.makeClosed()
                no_of_nodes_visited += 1

            draw()

    return False, no_of_nodes_visited, 0

def main(screen, width):
    grid = createGrid()

    start = None
    end = None

    is_running = True
    started = False
    current_stats = None

    while is_running:
        draw(screen, grid, current_stats)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, column = getPositionOfClick(position)
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
                row, column = getPositionOfClick(position)
                node = grid[row][column]
                node.reset()

                if node == start:
                    start = None

                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbours(grid)
                    started = True
                    path_found, nodes_visited, path_length = a_star(lambda: draw(screen, grid, current_stats), grid, start, end)
                    current_stats = {'name': 'A*', 'visited': nodes_visited, 'path': path_length}
                    if not path_found:
                        current_stats['path'] = "No path found"
                    started = False

                if event.key == pygame.K_b and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbours(grid)
                    started = True
                    path_found, nodes_visited, path_length = bfs(lambda: draw(screen, grid, current_stats), grid, start, end)
                    current_stats = {'name': 'BFS', 'visited': nodes_visited, 'path': path_length}
                    if not path_found:
                        current_stats['path'] = "No path found"
                    started = False

                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbours(grid)
                    started = True
                    path_found, nodes_visited, path_length = dfs(lambda: draw(screen, grid, current_stats), grid, start, end)
                    current_stats = {'name': 'DFS', 'visited': nodes_visited, 'path': path_length}
                    if not path_found:
                        current_stats['path'] = "No path found"
                    started = False

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = createGrid()


    pygame.quit()

main(screen, SCREEN_WIDTH)