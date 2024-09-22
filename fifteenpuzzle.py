import search
import random
import math
 
# Module Classes
class FifteenPuzzleState:
    """The Fifteen Puzzle is an extension of the Eight Puzzle to a 4x4 grid."""
 
    def __init__(self, numbers):
        self.cells = []
        numbers = numbers[:]  # Make a copy to avoid side-effects.
        numbers.reverse()
        for row in range(4):
            self.cells.append([])
            for col in range(4):
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col
        
    def isGoal(self):
        """Checks if the puzzle is in its goal state."""
        current = 1
        for row in range(4):
            for col in range(4):
                if row == 3 and col == 3:
                    if self.cells[row][col] != 0:
                        return False
                else:
                    if self.cells[row][col] != current:
                        return False
                    current += 1
        return True
 
    def legalMoves(self):
        """Returns a list of legal moves from the current state."""
        moves = []
        row, col = self.blankLocation
        if row > 0:
            moves.append('up')
        if row < 3:
            moves.append('down')
        if col > 0:
            moves.append('left')
        if col < 3:
            moves.append('right')
        return moves
 
    def result(self, move):
        """Returns a new FifteenPuzzle with the updated state based on the provided move."""
        row, col = self.blankLocation
        if move == 'up':
            newrow, newcol = row - 1, col
        elif move == 'down':
            newrow, newcol = row + 1, col
        elif move == 'left':
            newrow, newcol = row, col - 1
        elif move == 'right':
            newrow, newcol = row, col + 1
        else:
            raise ValueError("Illegal Move")
 
        newPuzzle = FifteenPuzzleState([0]*16)
        newPuzzle.cells = [values[:] for values in self.cells]
        newPuzzle.cells[row][col], newPuzzle.cells[newrow][newcol] = self.cells[newrow][newcol], self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol
        return newPuzzle
 
    def __eq__(self, other):
        """Overloads '==' for comparing puzzle configurations."""
        for row in range(4):
            if self.cells[row] != other.cells[row]:
                return False
        return True
 
    def __hash__(self):
        return hash(str(self.cells))
 
    def __getAsciiString(self):
        """Returns a display string for the puzzle."""
        lines = []
        horizontalLine = ('-' * (17))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    display = '   '
                else:
                    display = f"{col:2} "
                rowLine += display + '|'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)
 
    def __str__(self):
        return self.__getAsciiString()
 
# The Search Problem Class
class FifteenPuzzleSearchProblem(search.SearchProblem):
    """Implementation of a SearchProblem for the Fifteen Puzzle domain."""
 
    def __init__(self, puzzle):
        self.puzzle = puzzle
 
    def getStartState(self):
        return self.puzzle
 
    def isGoalState(self, state):
        return state.isGoal()
 
    def getSuccessors(self, state):
        successors = []
        for action in state.legalMoves():
            successor = state.result(action)
            successors.append((successor, action, 1))
        return successors
 
    def getCostOfActions(self, actions):
        return len(actions)
 
    def getHeuristic(self, state):
        return h2(state)  # Change heuristic here as needed
 
# Utilities and Puzzle Data
FIFTEEN_PUZZLE_DATA = [
    [1, 2, 3, 4,
     5, 6, 7, 8,
     9, 10, 11, 12,
     13, 14, 15, 0],
    [1, 2, 3, 4,
     5, 6, 7, 8,
     9, 10, 11, 12,
     13, 15, 14, 0],
    [1, 2, 3, 4,
     5, 6, 7, 8,
     9, 10, 11, 0,
     13, 14, 15, 12],
    [1, 2, 3, 4,
     5, 6, 7, 8,
     9, 0, 11, 12,
     13, 10, 15, 14],
    [1, 2, 3, 4,
     5, 6, 7, 8,
     0, 10, 11, 12,
     13, 9, 15, 14],
    [1, 2, 3, 4,
     5, 6, 7, 8,
     9, 10, 11, 12,
     13, 14, 0, 15]
]
 
def loadFifteenPuzzle(puzzleNumber):
    """Loads a fifteen puzzle object based on the provided puzzle number."""
    if puzzleNumber < 0 or puzzleNumber >= len(FIFTEEN_PUZZLE_DATA):
        raise ValueError("Invalid puzzle number")
    return FifteenPuzzleState(FIFTEEN_PUZZLE_DATA[puzzleNumber])
 
def createRandomFifteenPuzzle(moves=100):
    """Creates a random fifteen puzzle by applying a series of random moves."""
    puzzle = FifteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])
    for _ in range(moves):
        move = random.choice(puzzle.legalMoves())
        puzzle = puzzle.result(move)
    return puzzle
 
def h1(state, problem=None):
    """Returns the number of misplaced tiles for the 15-puzzle."""
    goal = list(range(1, 16)) + [0]
    misplaced_tiles = 0
    current = 0
    for row in range(4):
        for col in range(4):
            if state.cells[row][col] != 0:
                if state.cells[row][col] != goal[current]:
                    misplaced_tiles += 1
            current += 1
    return misplaced_tiles
 
def h2(state, problem=None):
    """Returns the sum of the Euclidean distances of each tile from its actual goal position."""
    goal_positions = {
        0: (3, 3),
        1: (0, 0),
        2: (0, 1),
        3: (0, 2),
        4: (0, 3),
        5: (1, 0),
        6: (1, 1),
        7: (1, 2),
        8: (1, 3),
        9: (2, 0),
        10: (2, 1),
        11: (2, 2),
        12: (2, 3),
        13: (3, 0),
        14: (3, 1),
        15: (3, 2)
    }
   
    total_distance = 0
    for row in range(4):
        for col in range(4):
            value = state.cells[row][col]
            if value != 0:
                goal_row, goal_col = goal_positions[value]
                total_distance += math.sqrt((goal_row - row) ** 2 + (goal_col - col) ** 2)
    return total_distance
 
def h3(state, problem=None):
    """Returns the sum of the Manhattan distances of each tile from its goal position."""
    goal_positions = {
        0: (3, 3),
        1: (0, 0),
        2: (0, 1),
        3: (0, 2),
        4: (0, 3),
        5: (1, 0),
        6: (1, 1),
        7: (1, 2),
        8: (1, 3),
        9: (2, 0),
        10: (2, 1),
        11: (2, 2),
        12: (2, 3),
        13: (3, 0),
        14: (3, 1),
        15: (3, 2)
    }
   
    total_distance = 0
    for row in range(4):
        for col in range(4):
            value = state.cells[row][col]
            if value != 0:
                goal_row, goal_col = goal_positions[value]
                total_distance += abs(goal_row - row) + abs(goal_col - col)
    return total_distance
 
def h4(state, problem=None):
    """Calculates the out of row and column heuristic."""
    out_of_row = 0
    out_of_column = 0
    for row in range(4):
        for col in range(4):
            value = state.cells[row][col]
            if value != 0:
                goal_row = (value - 1) // 4
                goal_col = (value - 1) % 4
                if goal_row != row:
                    out_of_row += 1
                if goal_col != col:
                    out_of_column += 1
    return out_of_row, out_of_column
 
if __name__ == '__main__':
    puzzle = createRandomFifteenPuzzle(25)
    print('A random puzzle:')
    print(puzzle)
    problem = FifteenPuzzleSearchProblem(puzzle)
    path = search.aStarSearch(problem, h1)  # A* search will use the heuristic
    print('A* found a path of %d moves: %s' % (len(path), str(path)))
 
    # Calculate and display the number of misplaced tiles
    misplaced_tiles = h1(puzzle)
    print(f'Heuristic 1 gives: {misplaced_tiles}')
 
    # Calculate and display the Euclidean distance
    euclidean_distance = h2(puzzle)
    print(f'Heuristic 2 gives: {euclidean_distance}')
 
    # Calculate and display the Manhattan distance
    manhattan_distance = h3(puzzle)
    print(f'Heuristic 3 gives: {manhattan_distance}')
 
    # Calculate and display the Out of row/column heuristic
    out_of_row, out_of_column = h4(puzzle)
    print(f'Heuristic 4 gives: {out_of_row + out_of_column}')
 
    curr = puzzle
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i > 1], a))
        print(curr)
        input("Press return for the next state...")  # wait for key stroke
        i += 1