import itertools
import random
import Clue
import Environment


class ImprovedAgent():
    """
    Minesweeper game player
    """

    def __init__(self, height=50, width=50):

        # Initialize the initial dimensions, height and width of the board
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

        # Set of sentences about the game known to be true
        self.knowledgeBase = []

    def MarkMine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        counter = 0
        self.mineSet.add(cell)
        for clue in self.knowledgeBase:
            counter = counter + clue.MarkMine(cell)
        return counter

    def MarkSafe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        counter = 0
        self.safeSet.add(cell)
        for clue in self.knowledgeBase:
            counter = counter + clue.MarkSafe(cell)
        return counter

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
        # mark the cell as a move that has been made
        self.track_moves.add(cell)

        # mark the cell as safe
        self.MarkSafe(cell)

        # add new sentence
        # find neighbors
        i, j = cell
        neighboringCells = set()
        for row in range(max(0, i - 1), min(i + 2, self.height)):
            for col in range(max(0, j - 1), min(j + 2, self.width)):
                if (row, col) != (i, j): # ignores the cell itself, and parses through neighboring cells and adds it to set of neighbors
                    neighboringCells.add((row, col))
        # add neighbors and value to sentence
        self.knowledgeBase.append(Clue.Clue(neighboringCells, count))

        # mark additional cells as safe or mines
        self.updateKnowledgeBase()

        inferences = self.new_inferences()

        while inferences:
            for clue in inferences:
                self.knowledgeBase.append(clue)

            # mark additional cells as safe or mines
            self.updateKnowledgeBase()

            inferences = self.new_inferences()
        print("\nMove: ", cell)

        while self.SimplifyKnowledgeBase() != self.knowledgeBase:
            pass

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

    def move_safely(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.track_moves, but should not modify any of those values.
        """
        for move in self.safeSet:
            if move not in self.track_moves and move not in self.mineSet:
                self.print_data()
                return move

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

    def print_data(self):
        print("\n\n\n")
        print("------------------------------------------------------------------")
        print("KnowlegeBase: ")
        for clue in self.knowledgeBase:
            print("\t", clue.cells, " = ", clue.count)
        print("\nConfirmed Safe:")
        print(self.safeSet)

        print("\nConfirmed Mines:")
        print(self.mineSet)
        print("------------------------------------------------------------------")

    def new_inferences(self):
        inferences = []
        removals = []

        # for each sentence known
        for clue1 in self.knowledgeBase:
            # mark for removal if it is empty
            if clue1.cells == set():
                removals.append(clue1)
                continue
            # pick another
            for clue2 in self.knowledgeBase:
                # mark for removal if empty
                if clue2.cells == set():
                    removals.append(clue2)
                    continue
                # make sure they're different sentences
                if clue1 != clue2:
                    # if s2 is a subset of s1
                    if clue2.cells.issubset(clue1.cells):
                        diff_cells = clue1.cells.difference(clue2.cells)
                        diff_count = clue1.count - clue2.count
                        # an inference can be drawn
                        new_inference = Clue.Clue(diff_cells, diff_count)
                        if new_inference not in self.knowledgeBase:
                            inferences.append(new_inference)

        # remove sentences without any cells
        self.knowledgeBase = [x for x in self.knowledgeBase if x not in removals]
        return inferences

    def updateKnowledgeBase(self):
        # repeat update if an update was made in the previous cycle
        counter = 1
        while counter:
            counter = 0
            for clue in self.knowledgeBase:
                for cell in clue.SafesKnown():
                    self.MarkSafe(cell)
                    counter += 1
                for cell in clue.MinesKnown():
                    self.MarkMine(cell)
                    counter += 1
            for cell in self.safeSet:
                counter += self.MarkSafe(cell)
            for cell in self.mineSet:
                counter += self.MarkMine(cell)

    def getFlags(self):
        """
        Return all mines found till now
        """
        return self.mineSet
