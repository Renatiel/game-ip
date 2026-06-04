import pygame
import pygame.locals as pg_lc
from interfaces import grid_style

pygame.init()
screen_colors = {
  "tile_color": (15, 15, 15),
  "bg_color": (30, 30, 30),
}
pygame.display.set_caption("Map Maker")


class Canvas:
  def __init__(self):
    self.drawings: list[grid_style] = []
    self.pallet_colors = {
      "black": {"rgb": (0, 0, 0)},
      "red": {"rgb": (200, 0, 0)},
      "green": {"rgb": (0, 200, 0)},
      "blue": {"rgb": (0, 0, 200)},
      "white": {"rgb": (200, 200, 200)},
    }
    self.ink_heigth = 50

    self.border = 5
    self.gap = 1
    self.tile_size = 16
    self.tiles_amount = 32

    self.canvas_size = (
      self.tile_size * self.tiles_amount
      + self.border * 2
      + self.gap * (self.tiles_amount - 1)
    )
    self.screen = pygame.display.set_mode((self.canvas_size * 1.2, self.canvas_size))
    self.screen.fill(screen_colors["bg_color"])

    self.create_grid()
    self.draw_pallet()
    self.insert_colors()

  def create_grid(self):
    for line in range(self.tiles_amount):
      self.drawings.append([])
      for col in range(self.tiles_amount):
        pos_x = (
          self.border + (self.gap + self.tile_size if col > 0 else self.tile_size) * col
        )
        pos_y = (
          self.border
          + (self.gap + self.tile_size if line > 0 else self.tile_size) * line
        )
        pos_size = (
          pos_x,
          pos_y,
          self.tile_size,  # size x
          self.tile_size,  # size y
        )

        grid = (screen_colors["tile_color"], pos_size)
        self.drawings[line].append(grid)
    self.selected_grid = self.drawings[0][0]

  def draw_grid(self):
    for line in self.drawings:
      for slot in line:
        pygame.draw.rect(self.screen, slot[0], slot[1])  # tile

  def draw(self, matrix_coords, color=None):
    if not color:
      color = self.pallet_colors["red"]["rgb"]

    proportion_coef = self.canvas_size / self.tiles_amount
    col = int(matrix_coords[0] / proportion_coef)
    line = int(matrix_coords[1] / proportion_coef)

    if col <= self.tiles_amount - 1 and line <= self.tiles_amount - 1:
      slot = self.drawings[line][col]

      if matrix_coords:
        self.drawings[line][col] = (color,) + (tuple(slot[1]),)

  def draw_pallet(self):
    pallet_pos_x = self.canvas_size
    pallet_pos_y = self.border
    self.pallet_width = self.canvas_size * 0.2 - self.border
    self.pallet_heigth = self.canvas_size - self.border * 2

    container_form = pygame.Rect(
      pallet_pos_x, pallet_pos_y, self.pallet_width, self.pallet_heigth
    )

    self.pallet = self.screen.subsurface(container_form)
    self.pallet.fill((25, 25, 25))

  def insert_colors(self):
    pos_y = 0

    for key in self.pallet_colors:
      self.pallet_colors[key]["ink"] = pygame.draw.rect(
        self.pallet,
        self.pallet_colors[key]["rgb"],
        (0, pos_y, self.pallet_width - self.gap, self.ink_heigth),
      )
      pos_y += self.ink_heigth + self.border

  def change_color(self, mouse_pos):
    proportion_coef = self.ink_heigth + self.border
    ink_idx = mouse_pos[1] // proportion_coef
    if mouse_pos[0] > self.canvas_size and ink_idx < len(self.pallet_colors):
      print(list(self.pallet_colors.keys())[ink_idx])


canvas = Canvas()

running_game = True
while running_game:
  canvas.draw_grid()
  for event in pygame.event.get():
    if event.type == pg_lc.QUIT:
      running_game = False

  if pygame.mouse.get_pressed()[0]:
    try:
      canvas.draw(tuple(event.pos))
      canvas.change_color(tuple(event.pos))
    except AttributeError:
      pass

  elif pygame.mouse.get_pressed()[2]:
    try:
      canvas.draw(tuple(event.pos), screen_colors["tile_color"])
    except AttributeError:
      pass

  pygame.display.update()

pygame.quit()
