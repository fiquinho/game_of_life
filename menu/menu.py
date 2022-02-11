from typing import Tuple, Dict

from game.cell import Colors
from menu import GameEntity, PlayButton, TextButton, Actions, HelpButton
from menu.menu_utils import LineSeparator, SpeedDisplay, SpeedTitle


class MenuManager:

    def __init__(self, size: Tuple[int, int]):
        self.width, self.height = size
        self.entities_distance = 15
        self.occupied_height = 0
        self.entities: Dict[Tuple[int, int], GameEntity] = {}

    def add_free_entity(self, entity: GameEntity, position: Tuple[int, int]):
        self.entities.update({position: entity})

    def add_stacked_entity(self, entity: GameEntity):
        """Adds an entity to the entities stack from top to bottom. It centers the
        entity in the horizontal axis."""
        next_vertical_position = self.occupied_height + self.entities_distance
        position = ((self.width - entity.width) // 2, next_vertical_position)

        self.add_free_entity(entity, position)
        self.occupied_height = next_vertical_position + entity.height

    def handle_click(self, x: int, y: int) -> str:

        for position, entity in self.entities.items():
            if entity.surface.get_rect(topleft=position).collidepoint((x, y)):
                action = entity.click()
                return action

        return Actions.NONE.name


class Menu(GameEntity):

    def __init__(self, size: Tuple[int, int], current_speed: int):

        self.menu_manager = MenuManager(size)
        self.current_speed = current_speed
        width, height = size

        play_button = PlayButton()
        self.menu_manager.add_stacked_entity(play_button)

        clear_button = TextButton("Clear", Actions.CLEAR.name)
        self.menu_manager.add_stacked_entity(clear_button)

        load_button = TextButton("Load", Actions.LOAD_BOARD.name)
        self.menu_manager.add_stacked_entity(load_button)

        save_button = TextButton("Save", Actions.SAVE_BOARD.name)
        self.menu_manager.add_stacked_entity(save_button)

        line_separator = LineSeparator(width)
        self.menu_manager.add_stacked_entity(line_separator)
        
        speed_title = SpeedTitle()
        self.menu_manager.add_stacked_entity(speed_title)

        speed_display = SpeedDisplay(self.current_speed)
        self.menu_manager.add_stacked_entity(speed_display)
        
        help_button = HelpButton()
        help_button_pos = ((width - help_button.width) // 2, 530)
        self.menu_manager.add_free_entity(help_button, help_button_pos)

        super().__init__(size)

    def update(self):
        self.surface.fill(Colors.BLACK)

        for position, entity in self.menu_manager.entities.items():
            entity.render(self.surface, position)
    
    def click(self):
        pass

    def handle_click(self, x: int, y: int) -> str:
        action = self.menu_manager.handle_click(x, y)
        return action
