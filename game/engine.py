from typing import Optional
from time import time

import pygame
from dataclasses import dataclass

from .board import Board
from menu.menu import Menu, Actions


GAME_WINDOW = (900, 600)
MENU_WINDOW = (100, GAME_WINDOW[1])
BOARD_WINDOW = (GAME_WINDOW[0] - MENU_WINDOW[0], GAME_WINDOW[1])

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


@dataclass
class GameConfig(object):
    board_width: int
    board_height: int
    cell_side: int
    fps: Optional[int] = None

    @property
    def board_size(self):
        return self.board_width, self.board_height

    @property
    def board_pixels_size(self):
        return self.board_width * self.cell_side, self.board_height * self.cell_side


class Engine(object):

    def __init__(self, game_config: GameConfig):
        self.config = game_config
        self.window = pygame.display.set_mode(GAME_WINDOW)

        self.stopped_time = True

        self.menu = Menu(size=MENU_WINDOW)

        pygame.display.set_caption("Game of Life")

        self.board = Board(columns=self.config.board_width, rows=self.config.board_height,
                           cell_side=self.config.cell_side, window_size=BOARD_WINDOW)

    @property
    def actions(self):
        return {Actions.PLAY.name: self.change_state,
                Actions.STOP.name: self.change_state,
                Actions.CHANGE_STATE.name: self.change_state,
                Actions.NONE.name: self.none_action,
                Actions.CLEAR.name: self.clear_board,
                Actions.LOAD_BOARD.name: self.load_board,
                Actions.SAVE_BOARD.name: self.save_board}

    def change_state(self):
        self.stopped_time = not self.stopped_time

    def save_board(self):
        board_path = filedialog.asksaveasfilename()
        self.board.save_board(board_path)

    def load_board(self):
        board_path = filedialog.askopenfilename()
        self.board.load_board(board_path)

    def none_action(self):
        pass

    def clear_board(self):
        self.board.reset()

    def render(self):
        self.board.render(self.window, position=(MENU_WINDOW[0], 0))
        self.menu.render(self.window, position=(0, 0))
        pygame.display.update()

    def handle_click(self, x: int, y: int):
        if x < MENU_WINDOW[0]:
            action = self.menu.handle_click(x, y)
            self.actions[action]()
        else:
            if self.stopped_time:
                board_x = x - MENU_WINDOW[0]
                self.board.handle_click(board_x, y)

    def run_game(self, render: bool = False):
        run = True
        clock = pygame.time.Clock()
        last_update = time()

        while run:
            # This will delay the game to given FPS
            clock.tick(self.config.fps)

            # This will loop through a list of any keyboard or mouse events.
            for event in pygame.event.get():
                # Checks if the red button in the corner of the window is clicked
                if event.type == pygame.QUIT:
                    run = False  # Ends the game loop

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos[0], event.pos[1])
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.change_state()

            if not self.stopped_time:

                now = time()
                if now - last_update >= 0.33:
                    self.board.update_state()
                    last_update = now

            self.menu.update()
            self.render() if render else None
