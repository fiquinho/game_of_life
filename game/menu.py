from typing import Tuple

import pygame

from .cell import Colors


class PlayButton(object):

    def __init__(self):

        self.surface = pygame.Surface((70, 70))
        self.stopped_mode = True

        self.update()

    def click(self):
        self.stopped_mode = not self.stopped_mode
        self.update()

    def update(self):

        self.surface.fill(Colors.GREEN)
        pygame.draw.rect(self.surface, Colors.BLACK, ((1, 1), (68, 68)))

        if self.stopped_mode:
            pygame.draw.polygon(self.surface, Colors.GREEN, [(18, 15), (52, 35), (18, 55)])
        else:
            pygame.draw.rect(self.surface, Colors.GREEN, ((20, 15), (10, 40)))
            pygame.draw.rect(self.surface, Colors.GREEN, ((40, 15), (10, 40)))

    def draw(self, surface: pygame.Surface, position: Tuple[int]):
        surface.blit(self.surface, position)


class Menu(object):

    def __init__(self, size: Tuple[int, int]):
        self.size = size

        self.surface = pygame.Surface(size)
        self.surface.fill(Colors.BLACK)

        self.play_button = PlayButton()
        self.play_button.draw(self.surface, (15, 15))

    def render(self, window: pygame.Surface, position: Tuple[int]):
        """Render element to screen"""
        window.blit(self.surface, position)

    def handle_click(self, x: int, y: int):
        if self.play_button.surface.get_rect(topleft=(15, 15)).collidepoint((x, y)):
            self.play_button.click()
            self.play_button.draw(self.surface, (15, 15))

            return True
        else:
            return False
