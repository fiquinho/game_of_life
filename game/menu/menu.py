from typing import Tuple, Dict

from game.configs import Actions, Colors
from game.menu import GameEntity, PlayButton, TextButton, HelpButton
from game.menu import LineSeparator, SpeedDisplay, SpeedTitle, SpeedButton


class MenuManager:

    def __init__(self, size: Tuple[int, int]):
        """Manages positions for entities in the menu as well as the
        clicks on those entities.

        :param size: The size of the menu in pixels
        """
        self.width, self.height = size
        self.entities_distance = 15
        self.occupied_height = 0
        self.entities: Dict[Tuple[int, int], GameEntity] = {}

    def next_vertical_position(self):
        """The next vertical position for a stacked entity."""
        return self.occupied_height + self.entities_distance

    def add_free_entity(self, entity: GameEntity, position: Tuple[int, int]):
        """Adds an entity to the manager in any position.

        :param entity: The entity to add
        :param position: Where the entity will be placed
        """
        self.entities.update({position: entity})

    def add_stacked_entity(self, entity: GameEntity):
        """Adds an entity to the entities stack from top to bottom. It centers the
        entity in the horizontal axis. Updates the current occupied_height.

        :param entity: The entity to add
        """
        position = ((self.width - entity.width) // 2, self.next_vertical_position())

        self.add_free_entity(entity, position)
        self.occupied_height = self.next_vertical_position() + entity.height

    def handle_click(self, x: int, y: int) -> str:
        """Handles a click in the menu. Uses the click method of
        the clicked entity.

        :param x: Horizontal position
        :param y: Vertical position
        :return: The action to execute
        """
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

        speed_step_controls_height = self.menu_manager.next_vertical_position()
        reduce_button = SpeedButton("-", Actions.REDUCE_SPEED.name)
        width_spaces = (width - (2 * reduce_button.width)) // 3
        reduce_button_pos = (width_spaces, speed_step_controls_height)
        self.menu_manager.add_free_entity(reduce_button, reduce_button_pos)

        increase_button = SpeedButton("+", Actions.INCREASE_SPEED.name)
        increase_button_pos = (width_spaces * 2 + increase_button.width, speed_step_controls_height)
        self.menu_manager.add_free_entity(increase_button, increase_button_pos)

        speed_full_controls_height = speed_step_controls_height + reduce_button.height + width_spaces
        min_button = SpeedButton("min", Actions.MIN_SPEED.name)
        min_button_pos = (width_spaces, speed_full_controls_height)
        self.menu_manager.add_free_entity(min_button, min_button_pos)

        max_button = SpeedButton("max", Actions.MAX_SPEED.name)
        max_button_pos = (width_spaces * 2 + increase_button.width, speed_full_controls_height)
        self.menu_manager.add_free_entity(max_button, max_button_pos)

        help_button = HelpButton()
        help_button_pos = ((width - help_button.width) // 2, 530)
        self.menu_manager.add_free_entity(help_button, help_button_pos)

        super().__init__(size)

    def update(self):
        self.surface.fill(Colors.BLACK)

        for position, entity in self.menu_manager.entities.items():
            entity.update()
            entity.render(self.surface, position)
    
    def click(self):
        pass

    def handle_click(self, x: int, y: int) -> str:
        action = self.menu_manager.handle_click(x, y)
        return action
