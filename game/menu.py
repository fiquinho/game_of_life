from typing import Tuple

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
    CLEAR_BUTTON_SIZE = (70, 30)
    FONT_SIZE = 18


class GameEntity(object):

    def __init__(self, size: Tuple[int, int]):
        self.size = size
        self.surface = pygame.Surface(self.size)

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

    @property
    def rect(self) -> pygame.Rect:
        return self.surface.get_rect()


class TextButton(GameEntity):

    def __init__(self, text: str):
        super().__init__(MenuLayout.CLEAR_BUTTON_SIZE)
        self.text = text
        self.update()

    def update(self):

        self.surface.fill(Colors.GREEN)
        pygame.draw.rect(self.surface, Colors.BLACK,
                         ((1, 1), (self.width - 2, self.height - 2)))

        font = pygame.font.Font(pygame.font.get_default_font(), MenuLayout.FONT_SIZE)

        # now print the text
        text_surface = font.render(self.text, True, Colors.GREEN)
        text_surface_rect = text_surface.get_rect()
        text_surface_x = (self.width - text_surface_rect[2]) // 2
        text_surface_y = (self.height - text_surface_rect[3]) // 2
        self.surface.blit(text_surface, dest=(text_surface_x, text_surface_y))

    def draw(self, surface: pygame.Surface, position: Tuple[int]):
        surface.blit(self.surface, position)


class PlayButton(GameEntity):

    def __init__(self):

        super().__init__(MenuLayout.PLAY_BUTTON_SIZE)
        self.stopped_mode = True
        self.update()

    def click(self):
        self.stopped_mode = not self.stopped_mode
        self.update()

    def update(self):

        self.surface.fill(Colors.GREEN)
        pygame.draw.rect(self.surface, Colors.BLACK, ((1, 1), (self.width - 2, self.height - 2)))

        if self.stopped_mode:
            pygame.draw.polygon(self.surface, Colors.GREEN, [(18, 15), (52, 35), (18, 55)])
        else:
            pygame.draw.rect(self.surface, Colors.GREEN, ((20, 15), (10, 40)))
            pygame.draw.rect(self.surface, Colors.GREEN, ((40, 15), (10, 40)))

    def draw(self, surface: pygame.Surface, position: Tuple[int]):
        surface.blit(self.surface, position)


class Menu(GameEntity):

    def __init__(self, size: Tuple[int, int]):
        super().__init__(size)
        self.surface.fill(Colors.BLACK)

        self.play_button = PlayButton()
        self.play_button_pos = ((self.width - self.play_button.width) // 2, 15)
        self.play_button.draw(self.surface, self.play_button_pos)

        self.clear_button = TextButton("Clear")
        self.clear_button_pos = ((self.width - self.clear_button.width) // 2, 100)
        self.clear_button.draw(self.surface, self.clear_button_pos)

        self.load_button = TextButton("Load")
        self.load_button_pos = ((self.width - self.load_button.width) // 2, 145)
        self.load_button.draw(self.surface, self.load_button_pos)

        self.save_button = TextButton("Save")
        self.save_button_pos = ((self.width - self.save_button.width) // 2, 190)
        self.save_button.draw(self.surface, self.save_button_pos)

    def render(self, window: pygame.Surface, position: Tuple[int]):
        """Render element to screen"""
        window.blit(self.surface, position)

    def handle_click(self, x: int, y: int):
        if self.play_button.surface.get_rect(topleft=self.play_button_pos).collidepoint((x, y)):
            self.play_button.click()
            self.play_button.draw(self.surface, (15, 15))

            return Actions.CHANGE_STATE
        elif self.clear_button.surface.get_rect(topleft=self.clear_button_pos).collidepoint((x, y)):
            return Actions.CLEAR
        elif self.load_button.surface.get_rect(topleft=self.load_button_pos).collidepoint((x, y)):
            return Actions.LOAD_BOARD
        elif self.save_button.surface.get_rect(topleft=self.save_button_pos).collidepoint((x, y)):
            return Actions.SAVE_BOARD
        else:
            return Actions.NONE
