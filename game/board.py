import csv
from typing import Tuple, Set, Dict
from pathlib import Path

import numpy as np
from pygame import Surface

from .cell import Cell, Colors


class CellPosition(object):
    """Stores a cell position in a board, in units"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return f"CellPosition( x = {self.x}, y = {self.y} )"

    def as_tuple(self) -> Tuple[int, int]:
        return self.x, self.y


def get_position_neighbours(position: 'CellPosition') -> Set['CellPosition']:
    neighbours: Set[CellPosition] = {
        CellPosition(position.x - 1, position.y - 1),
        CellPosition(position.x, position.y - 1),
        CellPosition(position.x + 1, position.y - 1),
        CellPosition(position.x + 1, position.y),
        CellPosition(position.x + 1, position.y + 1),
        CellPosition(position.x, position.y + 1),
        CellPosition(position.x - 1, position.y + 1),
        CellPosition(position.x - 1, position.y)}        # Left

    return neighbours


class Board(object):

    def __init__(self, columns: int, rows: int, cell_side: int,
                 window_size: Tuple[int, int]):

        self.columns = columns
        self.rows = rows
        self.cell_side = cell_side
        self.window_size = window_size

        self.window = Surface(window_size)
        self.window.fill(Colors.BLACK)

        self.board: np.array = np.array([
            [Cell(self.cell_side, (row * cell_side, column * cell_side))
             for column in range(rows)]
            for row in range(columns)
        ])

        self.active_cells: Set[CellPosition] = set()

    def reset(self):
        for cell_position in self.active_cells:
            self.board[cell_position.as_tuple()].die()

    def render(self, window: Surface, position: Tuple[int, int]):

        [[cell.render(self.window) for cell in column] for column in self.board]
        window.blit(self.window, position)

    def handle_click(self, x: int, y: int):

        cell_x = int(x / self.cell_side)
        cell_y = int(y / self.cell_side)
        cell_position = CellPosition(cell_x, cell_y)

        self.board[cell_position.as_tuple()].change_state()

        if self.board[cell_position.as_tuple()].is_alive():
            self.active_cells.add(CellPosition(cell_x, cell_y))
        else:
            self.active_cells.remove(CellPosition(cell_x, cell_y))

    def get_alive_neighbours(self, position: CellPosition) -> int:
        alive_neighbours = 0
        for neighbour in get_position_neighbours(position):
            if self.valid_position(neighbour):
                alive_neighbours += int(self.board[neighbour.as_tuple()].is_alive())

        return alive_neighbours
    
    def valid_position(self, position: CellPosition):
        x_valid = 0 <= position.x < self.columns
        y_valid = 0 <= position.y < self.rows
        
        return x_valid and y_valid
    
    def update_state(self):
        cells_alive_neighbours: Dict[CellPosition, int] = {}
        for active_cell in self.active_cells:

            if active_cell not in cells_alive_neighbours:
                cells_alive_neighbours[active_cell] = self.get_alive_neighbours(active_cell)

            for neighbour in get_position_neighbours(active_cell):
                if neighbour not in cells_alive_neighbours and self.valid_position(neighbour):
                    cells_alive_neighbours[neighbour] = self.get_alive_neighbours(neighbour)

        new_alive: Set[CellPosition] = set()
        for cell_position, alive_neighbours in cells_alive_neighbours.items():
            cell = self.board[cell_position.as_tuple()]
            cell.update(alive_neighbours)
            if cell.is_alive():
                new_alive.add(cell_position)

        self.active_cells = new_alive

    def load_board(self, board_file: Path):
        self.reset()
        with open(board_file, "r", newline="") as f:
            reader = csv.reader(f)

            for y, row in enumerate(reader):
                for x, value in enumerate(row):
                    if value == "1":
                        self.board[(x, y)].populate()
                        self.active_cells.add(CellPosition(x, y))

    def save_board(self, board_file: Path):
        with open(board_file, "w", newline="") as f:
            writer = csv.writer(f)

            for y in range(self.rows):
                write_row = []
                for x in range(self.columns):
                    if self.board[(x, y)].is_alive():
                        write_row.append("1")
                    else:
                        write_row.append("0")
                writer.writerow(write_row)
