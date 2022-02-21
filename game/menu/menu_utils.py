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
    MIN_SPEED = 7
    REDUCE_SPEED = 8
    INCREASE_SPEED = 9
    MAX_SPEED = 10
    OPEN_RULES = 11


class MenuLayout:
    PLAY_BUTTON_SIZE = (70, 70)
    TEXT_BUTTON_SIZE = (70, 30)
    HELP_BUTTON_SIZE = (40, 40)
    BUTTONS_BORDER = 1
    FONT_FILE = "game/assets/SourceCodePro-Regular.ttf"
    SPEED_DISPLAY_FONT = "game/assets/digital-7.mono.ttf"
    FONT_SIZE = 18
    BACKGROUND_COLOR = Colors.BLACK
    MAIN_COLOR = Colors.GREEN
    SPEED_LABEL_SIZE = (70, 25)
    SPEED_DISPLAY_SIZE = (70, 40)
    SPEED_BUTTONS_SIZE = (35, 25)


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

    @abstractmethod
    def click(self) -> str:
        """Handle entity being clicked. Returns action to be performed."""


class LineSeparator(GameEntity):

    def __init__(self, width: int):
        self.stopped_mode = True
        super().__init__((width, 1))

    def click(self) -> str:
        return Actions.NONE.name

    def update(self):
        self.surface.fill(MenuLayout.MAIN_COLOR)


class SpeedTitle(GameEntity):
    def __init__(self):
        self.font = pygame.font.Font(MenuLayout.FONT_FILE, MenuLayout.FONT_SIZE)
        super().__init__(MenuLayout.SPEED_LABEL_SIZE)

    def update(self):
        text_surface = self.font.render("Speed", True, MenuLayout.MAIN_COLOR)
        text_surface_rect = text_surface.get_rect()
        text_surface_x = (self.width - text_surface_rect[2]) // 2
        text_surface_y = (self.height - text_surface_rect[3]) // 2
        self.surface.blit(text_surface, dest=(text_surface_x, text_surface_y))

    def click(self) -> str:
        return Actions.NONE.name


class SpeedDisplay(GameEntity):

    def __init__(self, current_speed: int):
        self.current_speed = current_speed
        self.font = pygame.font.Font(MenuLayout.SPEED_DISPLAY_FONT, MenuLayout.SPEED_DISPLAY_SIZE[1])
        super().__init__(MenuLayout.SPEED_DISPLAY_SIZE)

    def update(self):
        self.surface.fill(MenuLayout.BACKGROUND_COLOR)
        text_surface = self.font.render(str(self.current_speed), True, MenuLayout.MAIN_COLOR)
        text_surface_rect = text_surface.get_rect()
        text_surface_x = (self.width - text_surface_rect[2]) // 2
        self.surface.blit(text_surface, dest=(text_surface_x, 0))

    def click(self) -> str:
        return Actions.NONE.name
