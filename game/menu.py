from typing import Tuple
from abc import abstractmethod, ABCMeta

import pygame

from .cell import Colors


class Actions(object):
    PLAY = "play"
    STOP = "stop"
    CHANGE_STATE = "change_state"
    CLEAR = "clear"
    NONE = None
    LOAD_BOARD = "load_board"
    SAVE_BOARD = "save_board"


class MenuLayout(object):
    PLAY_BUTTON_SIZE = (70, 70)
    TEXT_BUTTON_SIZE = (70, 30)
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

    def render(self, surface: pygame.Surface, position: Tuple[int]):
        surface.blit(self.surface, position)

    @abstractmethod
    def update(self):
        """Update the surface render of the entity."""


class Button(GameEntity, metaclass=ABCMeta):

    @abstractmethod
    def click(self) -> str:
        """Handle button being clicked. Returns action to be performed."""

    def generate_border(self) -> str:
        self.surface.fill(MenuLayout.MAIN_COLOR)
        position = (MenuLayout.BUTTONS_BORDER, MenuLayout.BUTTONS_BORDER)
        rectangle = (self.width - MenuLayout.BUTTONS_BORDER * 2, self.height - MenuLayout.BUTTONS_BORDER * 2)
        pygame.draw.rect(self.surface, MenuLayout.BACKGROUND_COLOR, (position, rectangle))


class TextButton(Button):

    def __init__(self, text: str, action: str):
        self.text = text
        self.action = action
        super().__init__(MenuLayout.TEXT_BUTTON_SIZE)

    def click(self) -> str:
        return self.action

    def update(self):

        self.generate_border()

        font = pygame.font.Font(pygame.font.get_default_font(), MenuLayout.FONT_SIZE)
        text_surface = font.render(self.text, True, Colors.GREEN)
        text_surface_rect = text_surface.get_rect()
        text_surface_x = (self.width - text_surface_rect[2]) // 2
        text_surface_y = (self.height - text_surface_rect[3]) // 2
        self.surface.blit(text_surface, dest=(text_surface_x, text_surface_y))


class PlayButton(Button):

    def __init__(self):
        self.stopped_mode = True
        super().__init__(MenuLayout.PLAY_BUTTON_SIZE)

    def click(self) -> str:
        self.stopped_mode = not self.stopped_mode
        self.update()
        return Actions.CHANGE_STATE

    def update(self):

        self.generate_border()

        if self.stopped_mode:
            pygame.draw.polygon(self.surface, Colors.GREEN, [(18, 15), (52, 35), (18, 55)])
        else:
            pygame.draw.rect(self.surface, Colors.GREEN, ((20, 15), (10, 40)))
            pygame.draw.rect(self.surface, Colors.GREEN, ((40, 15), (10, 40)))


class Menu(GameEntity):

    def __init__(self, size: Tuple[int, int]):
        width, _ = size
        self.play_button = PlayButton()
        self.play_button_pos = ((width - self.play_button.width) // 2, 15)

        self.clear_button = TextButton("Clear", Actions.CLEAR)
        self.clear_button_pos = ((width - self.clear_button.width) // 2, 100)

        self.load_button = TextButton("Load", Actions.LOAD_BOARD)
        self.load_button_pos = ((width - self.load_button.width) // 2, 145)

        self.save_button = TextButton("Save", Actions.SAVE_BOARD)
        self.save_button_pos = ((width - self.save_button.width) // 2, 190)

        super().__init__(size)

    def update(self):
        self.surface.fill(Colors.BLACK)
        self.play_button.render(self.surface, self.play_button_pos)
        self.clear_button.render(self.surface, self.clear_button_pos)
        self.load_button.render(self.surface, self.load_button_pos)
        self.save_button.render(self.surface, self.save_button_pos)

    def handle_click(self, x: int, y: int):
        if self.play_button.surface.get_rect(topleft=self.play_button_pos).collidepoint((x, y)):
            self.play_button.click()
            self.play_button.render(self.surface, (15, 15))

            return Actions.CHANGE_STATE
        elif self.clear_button.surface.get_rect(topleft=self.clear_button_pos).collidepoint((x, y)):
            return Actions.CLEAR
        elif self.load_button.surface.get_rect(topleft=self.load_button_pos).collidepoint((x, y)):
            return Actions.LOAD_BOARD
        elif self.save_button.surface.get_rect(topleft=self.save_button_pos).collidepoint((x, y)):
            return Actions.SAVE_BOARD
        else:
            return Actions.NONE
