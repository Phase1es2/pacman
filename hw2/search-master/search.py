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
    "*** YOUR CODE HERE ***"
    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    init_pos = problem.getStartState()

    #if(problem.isGoalState(init_pos)){ return ""};
    if problem.isGoalState(init_pos):
        return []
    
    #struct Node{
    #  pos, path, cost
    # }
    #stack<Node> stk
    stk = util.Stack()
    #stk.push(init_pos)
    stk.push((init_pos, [] , 0))
    #stk.push((init_pos, []))
    #unordered_set<Node> visited 
    visited = []

    #while(stk.size())
    while not stk.isEmpty():
        #auto a = stk.top()
        # stk.pop()
        curPos, path, cost= stk.pop()
        #curPos, path = stk.pop() 
        #if(!visited.count(a))
        if not curPos in visited:
        #   visited.insert(a)
            visited.append(curPos)
        
            if problem.isGoalState(curPos):
                return path
        
            #while(curPos.getSuccessors)
            #for pos, nextStep, cost in problem.getSuccessors(curPos):
            for nextPos, nextStep, cost in problem.getSuccessors(curPos):
                #if(!visited.find(curPos.getSuccessors))
                if not nextPos in visited:
                    #stk.push(successors)
                    paths = path + [nextStep]
                    stk.push((nextPos, paths, cost))
                    #stk.push((nextPos, paths))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    init_pos = problem.getStartState()
    if problem.isGoalState(init_pos):
        return []
    q = util.Queue()
    visited = []
     #struct Node{
    #  pos, path, cost
    # }
    #queue<Node> q
    q.push((init_pos, [], 0))
    
    #while(q.size())
    while not q.isEmpty():
        #auto a = q.front()
        #q.pop()
        curPos, path, costs = q.pop()

        if curPos not in visited:
            visited.append(curPos)

            if problem.isGoalState(curPos):
                return path
            #while(curPos.haveSuccessor)
            for nextPos, nextStep, cost in problem.getSuccessors(curPos):
                #if(!visited.count(successor))
                if nextPos not in visited:
                    paths = path + [nextStep]
                    #q.push(successors) add to q
                    q.push((nextPos, paths, cost))

    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    init_pos = problem.getStartState()
    if problem.isGoalState(init_pos):
        return []
    
    pq = util.PriorityQueue()

    visited = []

    pq.push((init_pos, [], 0), 0)

    while not pq.isEmpty():
        curPos, path, curCosts = pq.pop()
        
        if curPos not in visited:
            visited.append(curPos)

            if problem.isGoalState(curPos):
                return path
            
            for nextPos, nextStep, cost in problem.getSuccessors(curPos):
                if nextPos not in visited:
                    priority = curCosts + cost
                    paths = path + [nextStep]
                    pq.push((nextPos, paths, priority), priority)
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    init_pos = problem.getStartState()

    if problem.isGoalState(init_pos):
        return []
    
    pq = util.PriorityQueue()
    visited = []
    pq.push((init_pos, [], 0), 0)

    while not pq.isEmpty():
        curPos, path, curCosts = pq.pop()

        if curPos not in visited:
            visited.append(curPos)
            
            if problem.isGoalState(curPos):
                return path
            
            for nextPos, nextStep, cost in problem.getSuccessors(curPos):
                if nextPos not in visited:
                    paths = path + [nextStep]
                    totCost = curCosts + cost
                    heur = totCost + heuristic(nextPos, problem)
                    pq.push((nextPos, paths, totCost), heur)
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
