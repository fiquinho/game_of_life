from typing import Tuple

import pygame

from .cell import Colors


class PlayButton(object):

    def __init__(self):

        self.surface = pygame.Surface((70, 70))
        self.surface.fill(Colors.IRIS)
        pygame.draw.polygon(self.surface, Colors.YELLOW, [(18, 15), (52, 35), (18, 55)])

    def draw(self, surface: pygame.Surface, position: Tuple[int]):
        surface.blit(self.surface, position)


class Menu(object):

    def __init__(self, size: Tuple[int, int]):
        self.size = size

        self.surface = pygame.Surface(size)
        self.surface.fill(Colors.BLUE_JEANS)

        self.play_button = PlayButton()
        self.play_button.draw(self.surface, (15, 15))

    def render(self, window: pygame.Surface, position: Tuple[int]):
        """Render element to screen"""
        window.blit(self.surface, position)

    def handle_click(self, x: int, y: int):
        if self.surface.get_rect().collidepoint((x, y)):
            return True
        else:
            return False
