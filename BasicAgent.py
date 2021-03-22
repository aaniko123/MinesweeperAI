import Environment
import numpy as np
import random
import Clue


# newEnvironment = minesweeperVScode.Environment # Load original environment -> used to compare with moves and update


class BasicAgent():
    """
    Represents Basic Agent
    Tasks: For each cell, keep track of:
            – if safe, the number of mines surrounding it indicated by the clue
            – the number of safe squares identified around it
            – the number of mines identified around it.
            – the number of hidden squares around it.

    2)  • If, for a given cell, the total number of mines (the clue) minus the number of revealed mines is the number of
            hidden neighbors, every hidden neighbor is a mine.

    3)  • If, for a given cell, the total number of safe neighbors (8 - clue) minus the number of revealed safe neighbors is
            the number of hidden neighbors, every hidden neighbor is safe.

    4)  • If a cell is identified as safe, reveal it and update your information.

    5)  • If a cell is identified as a mine, mark it and update your information.

    6)  • The above steps can be repeated until no more hidden cells can be conclusively identified.

    7)  • If no hidden cell can be conclusively identified as a mine or safe, pick a cell to reveal uniformly at random from
            the remaining cells.
    """

    def __init__(self, height=50, width=50):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.track_moves = set()
        self.total_cells = set()
        for h in range(height):
            for w in range(width):
                self.total_cells.add((h, w))  # adds all locations (x,y) into all cells

        # Keep track of cells known to be safe or mines
        self.mineSet = set()
        self.safeSet = set()

        # List of clues (set of cells and count of how many are mines) about the game known to be true
        self.knowledgeBase = []
        # [(set of cells = count), (set2 of cells = count), (set3 of cells = count)]

    def MarkMine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mineSet.add(cell)
        for clue in self.knowledgeBase:
            clue.MarkMine(cell)

    def MarkSafe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # Remove addition of self.safes because of different algorithm
        for clue in self.knowledgeBase:
            clue.MarkSafe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.track_moves.add(cell)
        self.MarkSafe(cell)

        updatedKnowledgeBase = []

        # Loop over 3x3 cells and appending untouched cells to new_knowledge_cells
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:  # in bounds
                    if (i, j) not in self.track_moves and (i, j) not in self.safeSet:
                        updatedKnowledgeBase.append((i,
                                                    j))  # for a given move, check if cell location is in set of moves_made or in set of safes

        # Appending the new Knowledge
        if len(updatedKnowledgeBase) != 0:
            self.knowledgeBase.append(Clue.Clue(updatedKnowledgeBase, count))

        while self.SimplifyKnowledgeBase() != self.knowledgeBase:
            pass

        print("\n\n\n\n")
        print("------------------------------------------------------------------")

        print("\nMove: ", cell)

        print("Knowledge Base:")
        for clue in self.knowledgeBase:
            print(clue)

        print("\nConfirmed Safe:")
        print(self.safeSet)

        print("\nConfirmed Mines:")
        print(self.mineSet)
        print("------------------------------------------------------------------")

    def move_safely(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safeSet) > 0:
            return self.safeSet.pop()
        else:
            return None

    def move_randomly(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        freeSets = self.total_cells - self.track_moves - self.mineSet  # makes a move that has not already been made and is known to not be a mine
        if len(freeSets) > 0:
            return random.choice(tuple(freeSets))
        else:
            return None

    def SimplifyKnowledgeBase(self):
        """
        Copy current knowledge base and iterate through each clue. Put the safes from each

        """
        GoThroughClues = self.knowledgeBase.copy()

        for clue in GoThroughClues:
            SafesQueried = clue.SafesKnown()  # call known_safes function from the Clue class, returns set of safe cells and stores in known_safes
            MinesQueried = clue.MinesKnown()  # call known_mines function from the Clue class, returns set of mine cells and stores in known_mines

            if SafesQueried:
                self.safeSet.update(SafesQueried)  # Update a set with the union of itself and others.
                self.knowledgeBase.remove(clue)

            if MinesQueried:
                self.knowledgeBase.remove(clue)
                for mine in MinesQueried.union(
                        self.mineSet):  # if there is an overlap between known_mines and self.mines, mark the mine
                    self.MarkMine(mine)

        return self.knowledgeBase

    def getFlags(self):
        """
        Return all mines found till now
        """
        return self.mineSet
