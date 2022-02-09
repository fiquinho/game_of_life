from abc import abstractmethod, ABCMeta

import pygame

from game import Colors
from menu import MenuLayout, GameEntity, Actions


class Button(GameEntity, metaclass=ABCMeta):

    @abstractmethod
    def click(self) -> str:
        """Handle button being clicked. Returns action to be performed."""

    def generate_border(self):
        """Adds background color and a border to the surface"""
        self.surface.fill(MenuLayout.MAIN_COLOR)
        position = (MenuLayout.BUTTONS_BORDER, MenuLayout.BUTTONS_BORDER)
        rectangle = (self.width - MenuLayout.BUTTONS_BORDER * 2, self.height - MenuLayout.BUTTONS_BORDER * 2)
        pygame.draw.rect(self.surface, MenuLayout.BACKGROUND_COLOR, (position, rectangle))


class TextButton(Button):

    def __init__(self, text: str, action: str):
        self.text = text
        self.action = action
        self.font = pygame.font.Font(pygame.font.get_default_font(), MenuLayout.FONT_SIZE)
        super().__init__(MenuLayout.TEXT_BUTTON_SIZE)

    def click(self) -> str:
        return self.action

    def update(self):

        self.generate_border()

        text_surface = self.font.render(self.text, True, Colors.GREEN)
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
        return Actions.CHANGE_STATE.name

    def update(self):

        self.generate_border()

        if self.stopped_mode:
            pygame.draw.polygon(self.surface, Colors.GREEN, [(18, 15), (52, 35), (18, 55)])
        else:
            pygame.draw.rect(self.surface, Colors.GREEN, ((20, 15), (10, 40)))
            pygame.draw.rect(self.surface, Colors.GREEN, ((40, 15), (10, 40)))


class HelpButton(Button):

    def __init__(self):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        super().__init__(MenuLayout.HELP_BUTTON_SIZE)

    def click(self) -> str:
        return Actions.NONE.name

    def update(self):

        self.generate_border()

        text_surface = self.font.render("?", True, Colors.GREEN)
        text_surface_rect = text_surface.get_rect()
        text_surface_x = (self.width - text_surface_rect[2]) // 2
        text_surface_y = (self.height - text_surface_rect[3]) // 2
        self.surface.blit(text_surface, dest=(text_surface_x, text_surface_y))
