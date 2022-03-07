import webbrowser
import sys
import tkinter as tk
from tkinter import filedialog
from time import time

import pygame

from game.configs import WindowConfig, Actions, BoardConfig
from game.board import Board
from game.menu import Menu, SpeedDisplay


root = tk.Tk()
root.withdraw()
pygame.init()
pygame.display.set_caption("Game of Life")


class Engine(object):

    def __init__(self):
        self.window = pygame.display.set_mode(WindowConfig.GAME_WINDOW)
        self.current_speed = 5
        self.stopped_time = True

        self.menu = Menu(size=WindowConfig.MENU_WINDOW, current_speed=self.current_speed)
        self.board = Board(columns=BoardConfig.WIDTH, rows=BoardConfig.HEIGHT,
                           cell_side=BoardConfig.CELL_SIDE, window_size=WindowConfig.BOARD_WINDOW)

    @property
    def actions(self):
        return {Actions.PLAY.name: self.change_state,
                Actions.STOP.name: self.change_state,
                Actions.CHANGE_STATE.name: self.change_state,
                Actions.NONE.name: self.none_action,
                Actions.CLEAR.name: self.clear_board,
                Actions.LOAD_BOARD.name: self.load_board,
                Actions.SAVE_BOARD.name: self.save_board,
                Actions.MIN_SPEED.name: self.min_speed,
                Actions.REDUCE_SPEED.name: self.decrease_speed,
                Actions.INCREASE_SPEED.name: self.increase_speed,
                Actions.MAX_SPEED.name: self.max_speed,
                Actions.OPEN_RULES.name: self.open_rules
                }

    def min_speed(self):
        self.current_speed = 1
        self.update_menu_speed()

    def decrease_speed(self):
        if self.current_speed == 1:
            return
        self.current_speed -= 1
        self.update_menu_speed()

    def increase_speed(self):
        if self.current_speed == 20:
            return

        self.current_speed += 1
        self.update_menu_speed()

    def max_speed(self):
        self.current_speed = 20
        self.update_menu_speed()

    def update_menu_speed(self):
        for _, entity in self.menu.menu_manager.entities.items():
            if isinstance(entity, SpeedDisplay):
                entity.current_speed = self.current_speed

    def change_state(self):
        self.stopped_time = not self.stopped_time

    def save_board(self):
        board_path = filedialog.asksaveasfilename(initialdir="game/boards")
        if board_path != "":
            self.board.save_board(board_path)

    def load_board(self):
        board_path = filedialog.askopenfilename(initialdir="game/boards")
        if board_path != "":
            self.board.load_board(board_path)

    def none_action(self):
        pass

    @staticmethod
    def open_rules():
        webbrowser.open(WindowConfig.RULES_DIR)

    def clear_board(self):
        self.board.reset()

    def render(self):
        self.board.render(self.window, position=(WindowConfig.MENU_WINDOW[0], 0))
        self.menu.render(self.window, position=(0, 0))
        pygame.display.update()

    def handle_click(self, x: int, y: int):
        if x < WindowConfig.MENU_WINDOW[0]:
            action = self.menu.handle_click(x, y)
            self.actions[action]()
        else:
            if self.stopped_time:
                board_x = x - WindowConfig.MENU_WINDOW[0]
                self.board.handle_click(board_x, y)

    def run_game(self, render: bool = False):
        run = True
        clock = pygame.time.Clock()
        last_update = time()

        while run:
            # This will delay the game to given FPS
            clock.tick(BoardConfig.FPS)

            # This will loop through a list of any keyboard or mouse events.
            for event in pygame.event.get():
                # Checks if the red button in the corner of the window is clicked
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos[0], event.pos[1])

            if not self.stopped_time:

                now = time()
                if now - last_update >= 1 / self.current_speed:
                    self.board.update_state()
                    last_update = now

            self.menu.update()
            self.render() if render else None
