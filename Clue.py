import minesweeperVScode
import numpy as np
import random


class Clue():
    """
    Logical statement about a Minesweeper game
    A clue consists of a set of board cells,
    and a count of how many of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(
                self.cells) == self.count:  # if all the cells in set of all cells is equal to the count(number of surrounding mines), all the cells in the set are mines
            return self.cells
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:  # if all the cells in set of all cells is equal to a count(number of surrounding mines) of ZERO, all the cells in the set are safes
            return self.cells
        else:
            return None

    def mark_mine(self, cell):
        """
        If a cell is known to be a mine, remove it from the set of all board cells, and decrement count by 1
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        If a cell is known to be safe, remove it from the set of all board cells
        """
        if cell in self.cells:
            self.cells.remove(cell)
