import itertools
import random


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
        if (len(self.cells) == self.count):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # If the number of elements in the set "self.cells" is 0 #
        if (self.count == 0):
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

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # Check if the cell is present in the Sentence #
        if (cell in self.cells):
            # If True remove the cell #
            self.cells.discard(cell)



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
        # Update this in all the Sentences #
        if cell not in self.safes:
            self.mark_safe(cell)



        """         Part 3          """
        # Create  empty set for Neighbours to sit in #
        neighbors = set()

        # Loop over all the neighbors of the given cell #
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Our neighbor #
                if 0 <= i < self.height and 0 <= j < self.width:

                    # Check if the neighbor is already in moves_made #
                    if ((i, j) in self.moves_made):
                        continue

                    # Check if the neighbor is a known mine #
                    if ((i, j) in self.mines):
                        count -= 1
                        continue

                    # Check if the neighbor is a known safe #
                    if ((i, j) in self.safes):
                        continue

                    # Atlast add it to the places #
                    neighbors.add((i, j))

        # After going throuh all neighbors add a sentence to knowledge base #
        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)


        """         Part 4          """
        # Create empty sets for new mines and safes to sit in #
        new_safes = set()
        new_mines = set()

        # Iterate over whole knowledge base #
        for sentence in self.knowledge:
            if (len(sentence.cells) == 0):
                self.knowledge.remove(sentence)
            else:
                tmp_safes = sentence.known_safes()
                tmp_mines = sentence.known_mines()                

                if (type(tmp_safes) is set):
                    new_safes |= tmp_safes

                if (type(tmp_mines) is set):
                    new_mines |= tmp_mines

        for safe in new_safes:
            self.mark_safe(safe)

        for mine in new_mines:
            self.mark_mine(mine)



        """         Part 5          """
        prev_sentence = new_sentence

        new_inferences = []

        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
            #elif prev_sentence == sentence:
            #    break
            elif prev_sentence.cells <= sentence.cells:
                inf_cells = sentence.cells - prev_sentence.cells
                inf_count = sentence.count - prev_sentence.count

                new_inferences.append(Sentence(inf_cells, inf_count))

            prev_sentence = sentence

        self.knowledge += new_inferences


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # Make copy of self.safe #
        safe_moves = self.safes.copy()

        # Remove the moves made #
        safe_moves -= self.moves_made

        # If No moves in self_moves #
        if (len(safe_moves) == 0):
            return None

        # Retrun safe move #
        return safe_moves.pop()


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
                if (((i, j) not in self.moves_made) and ((i, j) not in self.mines)):
                    moves.append((i, j))


        # If the set is empty return None #
        if (len(moves) == 0):
            return None
        else:
            return random.choice(moves)
