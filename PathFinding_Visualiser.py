import pygame
import math
from queue import PriorityQueue, Queue

# Initialize Pygame and font module
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 700  # Full width for the screen
GRID_SIZE = SCREEN_WIDTH  # Grid size will be the same as the screen width
WIN = pygame.display.set_mode((SCREEN_WIDTH, GRID_SIZE + 100))  # Extra space for time display
pygame.display.set_caption("Path Finding Algorithm")

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        if not self.is_start() and not self.is_end():
            self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def a_star_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def Djikstra_Algorithm(draw, grid, start, end):
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {spot: False for row in grid for spot in row}
    visited[start] = True

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if not visited[neighbor]:
                came_from[neighbor] = current
                visited[neighbor] = True
                queue.put(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap), 2)  # Thicker grid lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width), 2)  # Thicker grid lines

    # Draw the border around the grid
    pygame.draw.line(win, WHITE, (0, 0), (width, 0), 4)  # Top border
    pygame.draw.line(win, WHITE, (0, 0), (0, width), 4)  # Left border
    pygame.draw.line(win, WHITE, (width - 1, 0), (width - 1, width), 4)  # Right border
    pygame.draw.line(win, WHITE, (0, width - 1), (width, width - 1), 4)  # Bottom border

def draw(win, grid, rows, width):
    win.fill(BLACK)  # Change the background color to black

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def clear_grid(grid, start, end):
    for row in grid:
        for spot in row:
            if spot != start and spot != end and not spot.is_barrier():
                spot.reset()

def main(win, width):
    ROWS = 30  # Adjusted the number of rows to make the grid fit better
    grid = make_grid(ROWS, GRID_SIZE)

    start = None
    end = None

    run = True
    algorithm_running = False
    a_star_time = 0
    Djikstra_time = 0

    while run:
        draw(win, grid, ROWS, GRID_SIZE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, GRID_SIZE)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, GRID_SIZE)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    start_time = pygame.time.get_ticks()  # Start the timer for A*
                    a_star_algorithm(lambda: draw(win, grid, ROWS, GRID_SIZE), grid, start, end)
                    a_star_time = pygame.time.get_ticks() - start_time  # End the timer for A*

                    clear_grid(grid, start, end)  # Clear the grid, except barriers, start, and end spots

                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    start_time = pygame.time.get_ticks()  # Start the timer for BFS
                    Djikstra_Algorithm(lambda: draw(win, grid, ROWS, GRID_SIZE), grid, start, end)
                    Djikstra_time = pygame.time.get_ticks() - start_time  # End the timer for BFS

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, GRID_SIZE)

        if a_star_time or Djikstra_time:
            font = pygame.font.Font(None, 36)
            a_star_text = font.render(f'A* Time: {a_star_time / 1000:.2f} seconds', True, WHITE, BLACK)
            Djikstra_text = font.render(f'Dijkstra Time: {Djikstra_time / 1000:.2f} seconds', True, WHITE, BLACK)
            a_star_rect = a_star_text.get_rect(center=(SCREEN_WIDTH // 2, GRID_SIZE + 25))
            Djikstra_rect = Djikstra_text.get_rect(center=(SCREEN_WIDTH // 2, GRID_SIZE + 60))
            win.blit(a_star_text, a_star_rect)
            win.blit(Djikstra_text, Djikstra_rect)
            pygame.display.update()

    pygame.quit()

main(WIN, SCREEN_WIDTH)




