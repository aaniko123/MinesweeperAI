import Environment
import numpy as np
import random


class Clue():
    """
    Each clue essentially contains a set of board cells as well as a count which indicates how many of those cells in
    the set are mines
    """

    def __init__(self, cells, count):  # initialize the clue class with cells and a count representing number of
        # neighboring mines

        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    # def __hash__(self):
    #     return hash((tuple(self.cells), self.count))

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def MinesKnown(self):
        """
        Returns a set of all cells in self.cells that are known to be mines, given that the length of the set is equal
        to the clue count
        """
        if len(self.cells) == self.count:
            return set(self.cells)
        else:
            return set()

    # def known_mines(self):
    #     """
    #     Returns the set of all cells in self.cells known to be mines.
    #     """
    #     if len(
    #             self.cells) == self.count:  # if all the cells in set of all cells is equal to the count(number of surrounding mines), all the cells in the set are mines
    #         return self.cells
    #     else:
    #         return None

    def SafesKnown(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        else:
            return set()

    # def known_safes(self):
    #     """
    #     Returns the set of all cells in self.cells known to be safe.
    #     """
    #     if self.count == 0:  # if all the cells in set of all cells is equal to a count(number of surrounding mines) of ZERO, all the cells in the set are safes
    #         return self.cells
    #     else:
    #         return None

    def MarkMine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return 1
        return 0

    # def mark_mine(self, cell):
    #     """
    #     If a cell is known to be a mine, remove it from the set of all board cells, and decrement count by 1
    #     """
    #     if cell in self.cells:
    #         self.cells.remove(cell)
    #         self.count -= 1

    def MarkSafe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            return 1
        return 0

    # def mark_safe(self, cell):
    #     """
    #     If a cell is known to be safe, remove it from the set of all board cells
    #     """
    #     if cell in self.cells:
    #         self.cells.remove(cell)

