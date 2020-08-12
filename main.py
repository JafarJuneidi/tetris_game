import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
      self.x = x
      self.y = y
      self.shape = shape
      self.color = shape_colors[shapes.index(self.shape)]
      self.rotation = 0

def create_grid(locked_pos = {}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    
    for i in range(len(grid)):
      for j in range(len(grid[i])):
        if (j, i) in locked_pos:
          c = locked_pos[(j, i)]
          grid[i][j] = c

    return grid


def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for row, line in enumerate(format):
      #horiz = list(line)
      for column, block in enumerate(line):
        if block == '0':
          positions.append((piece.x + column, piece.y + row))

    for i, pos in enumerate(positions):
      positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(piece, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
      if pos not in accepted_pos:
        if pos[1] > -1:
          return False

    return True


def check_lost(locked_positions):
  for pos in locked_positions:
    x, y = pos
    if y < 1:
      return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):  
    pass
   

def draw_grid_lines(surface, grid, row=0, col=0):
    s_x = top_left_x
    s_y = top_left_y

    for i in range(len(grid)):
      pygame.draw.line(surface, (128,128,128), (s_x, s_y + i*block_size), (s_x + play_width, s_y + i*block_size))
    for j in range(len(grid[1])):
      pygame.draw.line(surface, (128,128,128), (s_x + j*block_size, s_y), (s_x + j*block_size, s_y + play_height))

def clear_rows(grid, locked_positions):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
      if (0,0,0) not in grid[i]:
        inc += 1
        ind = i
        for j in range(len(grid[i])):
          try:
            del locked_positions[(j, i)]
          except:
            continue 

    if inc > 0:
      for key in sorted(list(locked_positions), key=lambda x:x[1])[::-1]:
        x, y = key
        if y < ind:
          new_key = (x, y + inc)
          locked_positions[new_key] = locked_positions.pop(key)

    return inc


def draw_next_shape(piece, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next shape", 1, (255,255,255))
    
    l_x = top_left_x + play_width + 30
    l_y = top_left_y + play_height/2 - 100
    
    surface.blit(label, (l_x + block_size//2, l_y))

    format = piece.shape[piece.rotation % len(piece.shape)]

    for row, line in enumerate(format):
      for column, block in enumerate(line):
        if block == '0':
          pygame.draw.rect(surface, piece.color, (l_x + column*block_size, l_y + block_size + row*block_size, block_size, block_size), 0)

    pygame.display.update()

def draw_window(surface, grid, score=0):
    surface.fill((0,0,0))
    
    font = pygame.font.SysFont("comicsans", 60)
    label = font.render("Tetris", 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width//2 - label.get_width()//2, 30))

    font = pygame.font.SysFont("comicsans", 30)
    label = font.render(f"Score: {score}", 1, (255,255,255))
    
    l_x = top_left_x + play_width + 30
    l_y = top_left_y + play_height/2 - 100 

    surface.blit(label, (l_x + 15, l_y + 190))

    for i in range(len(grid)):
      for j in range(len(grid[i])):
        pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid_lines(surface, grid)
    #pygame.display.update()


def main(win):
    
    locked_positions = {}
    #grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
      grid = create_grid(locked_positions)

      # timing and falling 
      fall_time += clock.get_rawtime()
      level_time += clock.get_rawtime()
      clock.tick()

      if level_time/1000 > 5:
        level_time = 0
        if fall_speed > 0.12:
          fall_speed -= 0.005

      if fall_time/1000 > fall_speed:
        fall_time = 0
        current_piece.y += 1
        if not valid_space(current_piece, grid) and current_piece.y > 0:
          current_piece.y -= 1
          change_piece = True


      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            current_piece.x -= 1
            if not valid_space(current_piece, grid):
              current_piece.x += 1
          if event.key == pygame.K_RIGHT:
            current_piece.x += 1
            if not valid_space(current_piece, grid):
              current_piece.x -= 1
          if event.key == pygame.K_DOWN:
            current_piece.y += 1
            if not valid_space(current_piece, grid):
              current_piece.y -= 1
          if event.key == pygame.K_UP: 
            current_piece.rotation += 1
            if not valid_space(current_piece, grid):
              current_piece.rotation -= 1

      piece_pos = convert_shape_format(current_piece)

      for point in piece_pos:
        x, y = point
        if y > -1:
          grid[y][x] = current_piece.color

      if change_piece:
        for point in piece_pos:
          p = (point[0], point[1])
          locked_positions[p] = current_piece.color
        current_piece = next_piece
        next_piece = get_shape()
        change_piece = False
        score += clear_rows(grid, locked_positions) * 10

      draw_window(win, grid, score)
      draw_next_shape(next_piece, win)

      if check_lost(locked_positions):
        run = False
    pygame.display.quit()


def main_menu(win):
    main(win)

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")

main_menu(win)  # start game