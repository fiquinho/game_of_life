from typing import Tuple

import pygame

from game.configs import Colors


class Cell(object):

    def __init__(self, side: int, position: Tuple[int, int]):

        self.alive: bool = False
        self.position: Tuple[int, int] = position

        self.surface = pygame.Surface((side, side))
        self.surface.fill(Colors.BLACK)
        # pygame.draw.rect(self.surface, Colors.BLACK, ((0, 0), (side, side)))

        self.cell_surface = pygame.Surface((side - 2, side - 2))
        self.cell_surface.fill(Colors.WHITE)

    def render(self, window: pygame.Surface):
        """Render element to screen"""
        self.surface.blit(self.cell_surface, (1, 1))
        window.blit(self.surface, self.position)

    def is_alive(self):
        return self.alive

    def change_state(self):

        if self.is_alive():
            self.alive = False
            self.cell_surface.fill(Colors.WHITE)

        else:
            self.alive = True
            self.cell_surface.fill(Colors.BLACK)

    def populate(self):
        if not self.is_alive():
            self.change_state()

    def die(self):
        if self.is_alive():
            self.change_state()

    def update(self, alive_neighbors: int):

        if 0 <= alive_neighbors <= 1:
            self.die()
        elif alive_neighbors == 3:
            self.populate()
        elif 4 <= alive_neighbors <= 8:
            self.die()
