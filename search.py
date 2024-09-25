# search.py
# ---------
# Licensing Information: You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
 
"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""
 
import util
# Example of how it might be imported
   ##from game import Game  # Adjust based on your project structure
 
 
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    """
 
    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()
 
    def isGoalState(self, state):
        """
        state: Search state
 
        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()
 
    def getSuccessors(self, state):
        """
        state: Search state
 
        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor.
        """
        util.raiseNotDefined()
 
    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take
 
        This method returns the total cost of a particular sequence of actions. The
        sequence must be composed of legal moves.
        """
        util.raiseNotDefined()
 
 
def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions # type: ignore
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]
 
 
def depthFirstSearch(problem):
   
    stack = util.Stack()
    visited = set()
    stack.push((problem.getStartState(), []))  # push (state, path)
 
    while not stack.isEmpty():
        state, actions = stack.pop()
 
        if problem.isGoalState(state):
            return actions
 
        if state not in visited:
            visited.add(state)
 
            for successor, action, stepCost in problem.getSuccessors(state):
                new_actions = actions + [action]
                stack.push((successor, new_actions))
 
    return []  # Failure
 
 
def breadthFirstSearch(problem):
   
    queue = util.Queue()
    visited = set()
    queue.push((problem.getStartState(), []))
 
    while not queue.isEmpty():
        state, actions = queue.pop()
 
        if problem.isGoalState(state):
            return actions
 
        if state not in visited:
            visited.add(state)
 
            for successor, action, stepCost in problem.getSuccessors(state):
                new_actions = actions + [action]
                queue.push((successor, new_actions))
 
    return []  # Failure
 
 
def uniformCostSearch(problem):
   
    pq = util.PriorityQueue()
    visited = set()
    pq.push((problem.getStartState(), []), 0)
 
    while not pq.isEmpty():
        state, actions = pq.pop()
 
        if problem.isGoalState(state):
            return actions
 
        if state not in visited:
            visited.add(state)
 
            for successor, action, stepCost in problem.getSuccessors(state):
                new_actions = actions + [action]
                new_cost = problem.getCostOfActions(new_actions)
                pq.push((successor, new_actions), new_cost)
 
    return []  # Failure
 
 
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem. This heuristic is trivial.
    """
    return 0
 
 
 


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
   
    pq = util.PriorityQueue()
    visited = set()
    expanded_nodes = 0  # Track the number of expanded nodes
    max_fringe_size = 0  # Track the maximum size of the priority queue
    
    pq.push((problem.getStartState(), []), 0)

    while not pq.isEmpty():
        # Update max fringe size
        max_fringe_size = max(max_fringe_size, pq.count)
        
        state, actions = pq.pop()
        
        if problem.isGoalState(state):
            return actions, expanded_nodes, max_fringe_size  # Return the solution path, expanded nodes, and max fringe size

        if state not in visited:
            visited.add(state)
            expanded_nodes += 1  # Increment expanded nodes

            for successor, action, stepCost in problem.getSuccessors(state):
                new_actions = actions + [action]
                cost = problem.getCostOfActions(new_actions) + heuristic(successor, problem)
                pq.push((successor, new_actions), cost)

    return [], expanded_nodes, max_fringe_size  # Return failure with metrics

 
 
# Abbreviations for search algorithms
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
