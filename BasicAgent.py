import minesweeperVScode
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

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()
        self.all_possible_cells = set()
        for h in range(height):
            for w in range(width):
                self.all_possible_cells.add((h, w))  # adds all locations (x,y) into all cells

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of clues (set of cells and count of how many are mines) about the game known to be true
        self.knowledgeBase = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for clue in self.knowledgeBase:
            clue.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # Remove addition of self.safes because of different algorithm
        for clue in self.knowledgeBase:
            clue.mark_safe(cell)

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
        self.moves_made.add(cell)
        self.mark_safe(cell)

        new_knowledge_cells = []

        # Loop over 3x3 cells and appending untouched cells to new_knowledge_cells
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:  # in bounds
                    if (i, j) not in self.moves_made and (i, j) not in self.safes:
                        new_knowledge_cells.append((i, j))  # for a given move, check if cell location is in set of moves_made or in set of safes

        # Appending the new Knowledge
        if len(new_knowledge_cells) != 0:
            self.knowledgeBase.append(Clue.Clue(new_knowledge_cells, count))

        while self.minify_knowledgebase() != self.knowledgeBase:
            pass

        print("\n\n\n\n")
        print("------------------------------------------------------------------")

        print("\nMove: ", cell)

        print("Knowledge Base:")
        for clue in self.knowledgeBase:
            print(clue)

        print("\nConfirmed Safe:")
        print(self.safes)

        print("\nConfirmed Mines:")
        print(self.mines)
        print("------------------------------------------------------------------")

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) > 0:
            return self.safes.pop()
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        freeSets = self.all_possible_cells - self.moves_made - self.mines  # makes a move that has not already been made and is known to not be a mine
        if len(freeSets) > 0:
            return random.choice(tuple(freeSets))
        else:
            return None

    def minify_knowledgebase(self):
        """
        Copy current knowledge base and iterate through each clue. Put the safes from each

        """
        knowledge_to_iterate = self.knowledgeBase.copy()

        for clue in knowledge_to_iterate:
            known_safes = clue.known_safes()  # call known_safes function from the Clue class, returns set of safe cells and stores in known_safes
            known_mines = clue.known_mines()  # call known_mines function from the Clue class, returns set of mine cells and stores in known_mines

            if known_safes:
                self.safes.update(known_safes)
                self.knowledgeBase.remove(clue)

            if known_mines:
                self.knowledgeBase.remove(clue)
                for mine in known_mines.union(
                        self.mines):  # if there is an overlap between known_mines and self.mines, mark the mine
                    self.mark_mine(mine)

        return self.knowledgeBase

    def getFlags(self):
        """
        Return all mines found till now
        """
        return self.mines
