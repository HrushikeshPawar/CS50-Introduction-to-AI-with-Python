import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            domain = list(self.domains[variable])
            for value in domain:
                if len(value) != variable.length:
                    self.domains[variable].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        

        # Check if variables overlaps
        overlap = self.crossword.overlaps[x, y]

        if overlap is None:
            return False

        flag = 0
        flag1 = 0
        remove_values = list()

        for word1 in self.domains[x]:
            for word2 in self.domains[y]:
                if word1[overlap[0]] == word2[overlap[1]]:
                   flag1 = 1
                   break
            if flag1 != 1:
                remove_values.append(word1)
                flag = 1
        
        if remove_values != []:
            for value in remove_values:
                self.domains[x].remove(value)
            
        # Check if revision is made
        if flag == 0:
            return False
        else:
            return True

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        # Check if the 'arcs' is empty
        if arcs == None:
            arcs = list()
            for variable in self.crossword.variables:
                for var in self.crossword.neighbors(variable):
                    arcs.append((variable, var))

        for x, y in arcs:
           if self.revise(x, y):
               for neighbour in self.crossword.neighbors(x):
                   arcs.append((x, neighbour))
        
        return len(self.domains[x]) > 0

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        # Compare length of assignment and length of domains
        if len(assignment) != len(self.domains):
            return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        # Check the length of words and variable
        for variable in assignment.keys():
            word1 = assignment[variable]
            if len(word1) != variable.length:
                return False
        
            # Check for conflict in char and Uniqueness
            for var in assignment:
                word2 = assignment[var]
                if variable != var:
                    if word1 == word2:
                        return False

                    overlap = self.crossword.overlaps[variable, var]
                    if overlap is not None:
                        i, j = overlap
                        if word1[i] != word2[j]:
                            return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        # Get list of unassigned neighbouring variables
        unassigned_neighbour = self.crossword.neighbors(var) - set(assignment.keys())

        # Define counter dictionary
        counter_dic = dict()

        for word in self.domains[var]:
            cnt = 0
            for variable in unassigned_neighbour:
                overlap = self.crossword.overlaps[var, variable]

                # Loop through all words of a neighbourhood variable
                for neighbour_word in self.domains[variable]:
                    if word[overlap[0]] != neighbour_word[overlap[1]]:
                        cnt += 1
                
            # Add the word and its counter to dic
            counter_dic[word] = cnt

        result = sorted(counter_dic, key=counter_dic.get)
        return result

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        #"""
        # Make a list of unassigned variables
        unassigned_variables = dict()
        for var in self.domains.keys():
            if var not in assignment:
                unassigned_variables[var] = len(self.domains[var])
        
        # Sort dic according to values in domains
        unassigned_variable_sorted = sorted(unassigned_variables, key=unassigned_variables.get)

        # Variables with same values in domains
        same_domains = [unassigned_variable_sorted[0]]
        for var in unassigned_variable_sorted:
            if var == same_domains[0]: continue
            if unassigned_variables[var] == unassigned_variables[same_domains[0]]:
                same_domains.append(var)

        if len(same_domains) == 1:
            return same_domains[0]
        else:
            result = dict()
            for var in same_domains:
                result[var] = len(self.crossword.neighbors(var))
            
            result = sorted(result, key=result.get, reverse=True)
            return result[0]
        """
        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return variable
        """

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment
        
        # Assign unassigned var
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is None:
                    assignment[var] = None
                else:
                    return result

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
