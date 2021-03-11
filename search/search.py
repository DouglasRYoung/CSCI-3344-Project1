# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
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

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    stack = util.Stack()
    startNode = problem.getStartState()
    cost = 0
    action = []
    visited = {}
    stack.push((startNode, action, cost))
    while not stack.isEmpty():
        current = stack.pop()
        if problem.isGoalState(current[0]):
            return current[1]

        if current[0] not in visited:
            visited[current[0]] = True
            for next, act, co in problem.getSuccessors(current[0]):
                if next and next not in visited:
                    stack.push((next, current[1] + [act], current[2] + co))
        
    "util.raiseNotDefined()"

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    startNode = problem.getStartState()
    cost = 0
    action = []
    visited = {}
    queue.push((startNode, action, cost))
    while not queue.isEmpty():
        current = queue.pop()
        if problem.isGoalState(current[0]):
            return current[1]

        if current[0] not in visited:
            visited[current[0]] = True
            for next, act, co in problem.getSuccessors(current[0]):
                if next and next not in visited:
                    queue.push((next, current[1] + [act], current[2] + co))
        
    "util.raiseNotDefined()"

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
     #Get Starting Node and Starting State
    startState = problem.getStartState()
    
    #Now we add a cost to our starting Node (state, action, cost)
    startNode = (startState, [], 0)
    #Use PriorityQueue method for UCS
    base = util.PriorityQueue()
    #What states we have already been too, holds the cost now
    nodesFound = {}    #(state, cost)

     #---- Begin with Starting Node ----

    #Push Starting Node
    base.push(startNode, 0)

    #---- Begin Going Through States ----
    while not base.isEmpty():
        #Get the current state and actions list and Cost out of the top of the PriorityQueue 
        currentNode, actions, currentCost = base.pop()

        #Check if currentState is inside our found Nodes/States
        if (currentNode not in nodesFound) or (currentCost < nodesFound[currentNode]):
            nodesFound[currentNode] = currentCost
        
            #Check if Node/State is at Goal State
            if problem.isGoalState(currentNode):
                return actions
            #If not Goal State but inside inside NodesFound then we want the successors of Node
            else: 
                successors = problem.getSuccessors(currentNode)  #List of [(successor, action, stepCost)..]
                
                #push each successor to priority Queue
                for successorState, succAction, succstepCost in successors:
                    actionNow = actions + [succAction]
                    costNow = currentCost + succstepCost
                    stateNow = (successorState, actionNow, costNow)
                    base.update(stateNow, costNow)

    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    evaluate = util.PriorityQueue()
    
    startState = problem.getStartState()
    heuristicCost = 0
    pathCost = 0
    actions = list()
    visited = list()
    evaluate.push((startState, actions, pathCost), heuristicCost)
    while not evaluate.isEmpty():
        currentSpace = evaluate.pop()
        if problem.isGoalState(currentSpace[0]):
            return currentSpace[1]
            
        if currentSpace[0] not in visited:
            visited.append(currentSpace[0])
            for adjacent, move, cost in problem.getSuccessors(currentSpace[0]):
                if adjacent not in visited:
                    evaluate.push((adjacent, currentSpace[1] + [move], currentSpace[2] + cost), (currentSpace[2] + cost + heuristic(adjacent, problem)))
    
    return list()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
