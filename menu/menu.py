from typing import Tuple, Dict

from game.cell import Colors
from menu import GameEntity, PlayButton, TextButton, Actions, HelpButton
from menu.buttons import Button


class MenuManager:

    def __init__(self):

        self.occupied_height = 0
        self.entities: Dict[Tuple[int, int], GameEntity] = {}
        self.buttons: Dict[Tuple[int, int], Button] = {}

    def add_free_entity(self, entity: GameEntity, position: Tuple[int, int]):
        if isinstance(entity, Button):
            self.buttons.update({position: entity})
        self.entities.update({position: entity})

    def add_stacked_entity(self, entity: GameEntity, position: Tuple[int, int]):
        self.add_free_entity(entity, position)
        self.occupied_height = position[1] + entity.height

    def handle_click(self, x: int, y: int) -> str:

        for position, button in self.buttons.items():
            if button.surface.get_rect(topleft=position).collidepoint((x, y)):
                action = button.click()
                return action

        return Actions.NONE.name


class Menu(GameEntity):

    def __init__(self, size: Tuple[int, int]):

        self.menu_manager = MenuManager()
        self.entities_distance = 15
        width, _ = size

        play_button = PlayButton()
        play_button_pos = ((width - play_button.width) // 2,
                           self.menu_manager.occupied_height + self.entities_distance)
        self.menu_manager.add_stacked_entity(play_button, play_button_pos)

        clear_button = TextButton("Clear", Actions.CLEAR.name)
        clear_button_pos = ((width - clear_button.width) // 2,
                            self.menu_manager.occupied_height + self.entities_distance)
        self.menu_manager.add_stacked_entity(clear_button, clear_button_pos)

        load_button = TextButton("Load", Actions.LOAD_BOARD.name)
        load_button_pos = ((width - load_button.width) // 2,
                           self.menu_manager.occupied_height + self.entities_distance)
        self.menu_manager.add_stacked_entity(load_button, load_button_pos)

        save_button = TextButton("Save", Actions.SAVE_BOARD.name)
        save_button_pos = ((width - save_button.width) // 2,
                           self.menu_manager.occupied_height + self.entities_distance)
        self.menu_manager.add_stacked_entity(save_button, save_button_pos)

        help_button = HelpButton()
        help_button_pos = ((width - help_button.width) // 2, 530)
        self.menu_manager.add_free_entity(help_button, help_button_pos)

        super().__init__(size)

    def update(self):
        self.surface.fill(Colors.BLACK)

        for position, entity in self.menu_manager.entities.items():
            entity.render(self.surface, position)

    def handle_click(self, x: int, y: int) -> str:
        action = self.menu_manager.handle_click(x, y)
        return action
