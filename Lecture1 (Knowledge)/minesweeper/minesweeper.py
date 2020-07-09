import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
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

        # If the number of elements in the set "cells" is equal to the count #
        if (len(self.set) == count):
            return self.set

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # If the number of elements in the set "self.cells" is 0 #
        if (len(self.cells) == 0):
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # Check if the cell is present in the Sentence #
        if (cell in self.cells):
            # If True remove the cell #
            self.cells.discard(cell)

            # Decrease the count by 1 #
            self.count -= 1
        else:
            return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # Check if the cell is present in the Sentence #
        if (cell in self.cells):
            # If True remove the cell #
            self.cells.discard(cell)
        else:
            return



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

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

        """         Part 1          """
        # Add the cell to the moves_made set #
        self.moves_made.add(cell)



        """         Part 2          """
        # Add the cell to the self.safes set #
        self.safes.add(cell)

        # Update this in all the Sentences #
        mark_safe(self, cell)



        """         Part 3          """
        places = set()

        # Loop over all the neighbors of the given cell #
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Our neighbor #
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor = (cell[0] + (i - 1), cell[0] + (j - 1))

                    # Check if the neighbor is already in moves_made #
                    if ((i, j) in self.moves_made):
                        continue

                    # Check if the neighbor is a known mine #
                    elif ((i, j) in self.mines):
                        count -= 1
                        continue

                    # Atlast add it to the places #
                    else:
                        places.add((i, j))

        # After going throuh all neighbors add a sentence to knowledge base #
        self.knowledge.append(Sentence(places, count))


        """         Part 4          """
        def part4():
            # Iterate over all the sentences in knowledge base #
            for sent in deepcopy(self.knowledge):
                # If the count is empty all cells in sentence are safe #
                if (sent.count == 0):
                    for cell in sent.cells:
                        # Mark as Safe #
                        self.mark_safe(cell)
                # If the len of sentence is equal to count all cells are safe #
                elif (len(sent.cells) == sent.count):
                    for cell in sent.cells:
                        # Mark as Mine #
                        self.mark_mine(cell)

        part4()


        """         Part 5          """
        # Deepcopy of the Knowledge Base #
        known = deepcopy(self.knowledge)

        # Iterate over whole knowledge base for Sets and its Subsets #
        for Set in known:
            for Subset in known:
                # Check if both are not same and Set is bigger that Subset#
                if ((Set != Subset) and (len(Set.cells) >= len(Subset.cells)) and Subset.issubset(Set)):
                    # Then get the Set - Subset #
                    newset = Set.cells.difference(Subset.cells)
                    newcount = Set.count - Subset.count

                    #  Add to the Knowledge Base #
                    self.knowledge.add(Sentence(newset, newcount))

                    # Again run part4 #
                    part4()


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # Iterate moves in self.safes #
        for cell in self.safes:
            # Check if move is not made #
            if (cell not in self.moves_made):
                return cell

        # If no safe cell known #
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Initialize set of correct moves #
        moves = []

        # List all makeable moves #
        for i in range(self.height-1):
            for j in range(self.width-1):
                # If cell is not in moves_made and is not mine add to moves #
                if (((i, j) not in self.moves_made) and ((i, j) not in self.mines):
                    moves.append((i, j))


        # If the set is empty return None #
        if (moves is []):
            return None
        else:
            return random.choice(moves)
