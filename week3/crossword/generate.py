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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        for varibale, words in self.domains.items():
            variable_length = varibale.length
            for word in words:
                if len(word) != variable_length:
                    words.remove(word)
                    
    
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        x_domain = self.domains[x]
        y_domain = self.domains[y]
        overlaps = self.crossword.overlaps[x, y]
        revison_made = False
        possible_candidate_in_y = False
        
        for x_value in x_domain:
            overlaps_in_x = x_value[overlaps[0]]
            for y_value in y_domain:
                if y_value[overlaps[1]] == overlaps_in_x:
                    possible_candidate_in_y = True
                    break
            if possible_candidate_in_y == False:
                x_domain.remove(x_value)
                revison_made = True
            
        return revison_made
    
    
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []
        if not arcs:
            variables = list(self.domains.keys())
            for i in range(len(variables) - 1):
                for j in range(i, len(variables), 1):
                    queue.append(variables[i], variables[j])
        else:
            queue = arcs
        
        while len(queue) != 0:
            arc = queue.pop(0)
            if len(self.domains[arc[0]]) == 0:
                return False
            revision = self.revise(arc[0], arc[1])
            if revision:
                for neighbour in self.crossword.neighbors(arc[0]):
                    queue.append(neighbour)

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains.keys():
            if var not in assignment.keys() or not assignment[var]:
                return False
        return True

    
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var, value in assignment.items():
            # check for variable length
            if len(value) != var.length:
                return False
            # check for same overlap
            for neighbour in self.crossword.neighbors(var):
                neighbour_value = assignment[neighbour]
                overlap = self.crossword.overlaps[var, neighbour]
                if value[overlap[0]] != neighbour_value[overlap[1]]:
                    return False
        
        # check for distinct value 
        return len(assignment.values()) != len(set(assignment.values()))

    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        original_domain = self.domains[var]
        weighted_domain = {value:0 for value in original_domain}
        unassigned_variables = [variable for variable in self.crossword.neighbors(var) if variable not in assignment]
        
        for value in original_domain:
            for neighbour in unassigned_variables:
                overlap = self.crossword.overlaps[var, neighbour]
                restriction = value[overlap[0]]
                for word in self.domains[neighbour]:
                    if word[overlap[1]] != restriction:
                        weighted_domain[value] += 1
        
        return sorted(weighted_domain.keys(), key=lambda k: weighted_domain[k])
    
    
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # minimum number of remaining values first
        unassigned_variables = {variable: domain for variable, domain in self.domains.items() if variable not in assignment}
        min_value = min((map(len, unassigned_variables.values())))
        min_variables = [var for var, value in unassigned_variables.items() if len(value) == min_value]
        if len(min_variables) == 1:
            return min_variables[0]
        
        # if there exist a tie, sort them with the highest degree
        degree = {var: len(self.crossword.neighbours(var)) for var in min_variables}
        return sorted(degree.keys(), key=lambda k: degree[k])[-1]


    def inference(self, assignment):
        """
        Calling ac3() to test whether we can made new conclusion based on that new assginment
        """
        ac3_result = self.ac3()
        if ac3_result == False:
            return False
        return {variable:domain for variable, domain in self.domains.items() if variable not in assignment and len(domain) == 1}        
    
    
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment): 
            if self.consistent(assignment):
                original_domain = self.domains.copy()
                original_assignment = assignment.copy()
                
                assignment[var] = value
                
                # inference based on the new assignment
                inferences = self.inference(assignment)
                if inferences != False:
                    for var in inferences:
                        assignment[var] = inferences[var]                
                    backtrack_result = self.backtrack(assignment)
                    if backtrack_result:
                        return backtrack_result
                # turn back to original state if this value is not valid
                self.domains = original_domain
                assignment = original_assignment
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
