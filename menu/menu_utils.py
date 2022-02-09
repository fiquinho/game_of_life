from enum import Enum
from typing import Tuple
from abc import abstractmethod, ABCMeta

import pygame

from game import Colors


class Actions(Enum):
    PLAY = 0
    STOP = 1
    CHANGE_STATE = 2
    CLEAR = 3
    NONE = 4
    LOAD_BOARD = 5
    SAVE_BOARD = 6


class MenuLayout:
    PLAY_BUTTON_SIZE = (70, 70)
    TEXT_BUTTON_SIZE = (70, 30)
    HELP_BUTTON_SIZE = (40, 40)
    BUTTONS_BORDER = 1
    FONT_SIZE = 18
    BACKGROUND_COLOR = Colors.BLACK
    MAIN_COLOR = Colors.GREEN


class GameEntity(metaclass=ABCMeta):

    def __init__(self, size: Tuple[int, int]):
        self.size = size
        self.surface = pygame.Surface(self.size)
        self.update()

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

    @property
    def rect(self) -> pygame.Rect:
        return self.surface.get_rect()

    def render(self, surface: pygame.Surface, position: Tuple[int, int]):
        surface.blit(self.surface, position)

    @abstractmethod
    def update(self):
        """Update the surface render of the entity."""
