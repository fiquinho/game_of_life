from enum import Enum
from pathlib import Path


GAME_WINDOW = (900, 600)
MENU_WINDOW = (100, GAME_WINDOW[1])
BOARD_WINDOW = (GAME_WINDOW[0] - MENU_WINDOW[0], GAME_WINDOW[1])


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (57, 255, 20)


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


class BoardConfig:
    WIDTH = 40
    HEIGHT = 30
    CELL_SIDE = 20
    FPS = 60


class MenuLayout:
    PLAY_BUTTON_SIZE = (70, 70)
    TEXT_BUTTON_SIZE = (70, 30)
    HELP_BUTTON_SIZE = (40, 40)
    BUTTONS_BORDER = 1
    FONT_FILE = Path("game/assets/SourceCodePro-Regular.ttf")
    SPEED_DISPLAY_FONT = Path("game/assets/digital-7.mono.ttf")
    FONT_SIZE = 18
    BACKGROUND_COLOR = Colors.BLACK
    MAIN_COLOR = Colors.GREEN
    SPEED_LABEL_SIZE = (70, 25)
    SPEED_DISPLAY_SIZE = (70, 40)
    SPEED_BUTTONS_SIZE = (35, 25)
