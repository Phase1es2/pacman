# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        infi = float("inf")

        "*** YOUR CODE HERE ***"
        # focusing on eating food.When ghost near don't go,
     #   newFood = successorGameState.getFood().asList()
        #get current game score 
        score = successorGameState.getScore() 
        #print(score)

        newGhost = successorGameState.getGhostPositions()
        #find the distance  to the closest friut
        foodList = newFood.asList()
        minFoodList = infi
        for food in foodList:
            minFoodList = min(minFoodList, manhattanDistance(newPos, food))

        #Initialize a ghost penalty 
        ghostPenalty = 0
        #check gost position and scaredTime to determine its impact on the evalutaion 
        for ghost, scaredTime in zip(newGhost, newScaredTimes):
            ghostDist = manhattanDistance(newPos, ghost)
            if scaredTime == 0:
                #If the ghosts not scared, penalize Pacamn for gettting too clost to ghost
                if ghostDist < 2:
                    return -infi
                else:
                    ghostPenalty -= 5.0 / ghostDist
            elif scaredTime > 0:
                #if ghost is scared, then encourage Pacaman to eat the ghost
                if ghostDist < scaredTime:
                    return score + 100.0 / (ghostDist + 1) #if it each the ghost the distance between Pacman and Ghost is 0
                else:
                    ghostPenalty += 3.0 / ghostDist
        # calculate the final evaluation score 
        return score + 1.0/minFoodList + ghostPenalty

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #check if the game is win or lose, in that case return Noe as no action need to return 

        """
        Pseudo code:
        def value(state):
            if the state is a terminal state: return the statee's utility
            if the next agent is MAX: return max-value(state)
            if the next agent is MIN: reutnr min-value(state)

        def max-value(state):
            initialize v = -inf
            for each successor of state:
                v = max(v, value(successor))
            return v

        def min-value(state):
            initialize v = +inf
            for each successor of state:
                v = min(v,value(successor))
            return v
        """
        if gameState.isWin() or gameState.isLose():
            return None
        
        #value function to calculate the minimax value of a state
        def value(agent, depth, gameState):
            #check if the game is win or lose, or we've reached to maxmium depth
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            #agent 0 is the Pacman, if it is the pacman's turn we want to maxmize the score
            if agent == 0:
                return max_value(agent, depth, gameState)
            else: #if it is ghost turn we want to minimize the score
                return min_value(agent, depth, gameState)
            
        #helper function for finding the minimum value of all the possible legal action for the state
        def min_value(agent, depth, gameState):
            #since we want to find the minimum, we init v to infinity
            v = float("inf")
            for action in gameState.getLegalActions(agent):
               #For each actions, find the minimax value and upadate the minimum value 
              v = min(v, value((agent + 1) % gameState.getNumAgents(), depth + (agent + 1) // gameState.getNumAgents(), gameState.generateSuccessor(agent, action)))
            return v
        
        #helper function for finding the maximum value of all the possible legal action for the state
        def max_value(agent, depth, gameState):
            #since we want to find the maxmum value, we init v to -infinity
            v = -float("inf")
            for action in gameState.getLegalActions(agent):
                #For each actions, find the minimax value and upadate the maximum value 
                v = max(v, value((agent + 1) % gameState.getNumAgents(), depth, gameState.generateSuccessor(agent, action)))
            return v
        
        #find the best action to take
        bestScore = float("-inf")
        bestAction = None
        #loop for all the possible action to take
        for action in gameState.getLegalActions(0):
            #get the game state resulting from taking the action
            successor = gameState.generateSuccessor(0, action)
            #calculate the minimax value ofthe resulting state
            score = value(1, 0, successor)
            #update the best score and actions 
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction
        #print(gameState.getNumAgents())
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        """
        Pseudo code:
        alpha: MAX's best option on path to root
        beta: MIN's best option on path to root

        def max-value(state. alpha, beta):
            initialize v = -inf
            for each successor of state:
                v = max(v, value(successor, alpha, beta))
                if v >= beta return v
                alpha = max(alpha, v)
            return v

        def min-value(state. alpha, beta):
            initialize v = -inf
            for each successor of state:
                v = min(v, value(successor, alpha, beta))
                if v <= alpha return v
                alpha = min(beta, v)
            return v
        """
        #if game is alread win or lose, it does not need to return anythign
        if gameState.isWin() or gameState.isLose():
            return None
        #helper function for value computation in minimaxwith alpha-beta pruning 
        def value(agent, depth, gameState, alpha, beta):
            #check terminal conditions
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            # if Pacman's turn Max
            if agent == 0:  
                return max_value(agent, depth, gameState, alpha, beta)
            else:  # if Ghost's turn Min 
                return min_value(agent, depth, gameState, alpha, beta)

        #Note you must not prune on equality in order to match  the set of states explored by autograder
        def min_value(agent, depth, gameState, alpha, beta):
            #initialize v to positive infinity
            v = float("inf")
            for action in gameState.getLegalActions(agent):
                #compute the value for this actions's successor state
                v = min(v, value((agent + 1) % gameState.getNumAgents(), depth + (agent + 1) // gameState.getNumAgents(), gameState.generateSuccessor(agent, action), alpha, beta))
                """
                (agent + 1) % gameState.getNumAgents() ==> calculates the next agent in the trun order, 'agent' is the current min player, 'agent + 1' is next agent
                depth + (agent + 1) // gameState.getNumAgents() ==> depth of the search for the next agent.
                since each agent gets a turn before the depth is incremented, (agent + 1) // gameState.getNumAgents() calculates the number of complete agent turns, and add it to the current depth.
                """
                #if v <= alpha:
                if v < alpha:
                    #prune the branch if v is less than alpha
                    return v
                #update beta for future pruning
                beta = min(beta, v)
            return v

        def max_value(agent, depth, gameState, alpha, beta):
            #initialize v to negative infinity
            v = float("-inf")
            for action in gameState.getLegalActions(agent):
                #compute the value for this actions's successor state
                v = max(v, value((agent + 1) % gameState.getNumAgents(), depth, gameState.generateSuccessor(agent, action), alpha, beta))
                #if v >= alpha:
                if v > beta:
                    #prune the branch if v is greater than beta
                    return v
                #update alpha for future pruning
                alpha = max(alpha, v)
            return v

        bestScore = float("-inf")
        bestAction = None
        alpha = float("-inf")
        beta = float("inf")
        #iterate over pacman's legal actions to find the best action using alpha-beta prunting 
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            #compute the score using minimax with alpha-beta pruning
            score = value(1, 0, successor, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            #upadte alpha for future pruning
            alpha = max(alpha, bestScore)

        return bestAction

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        """
        def value(state):
            if the state is a terminal state: rturn teh state's utility
            if the nexty agent is MAX: return max-value(state)
            if the next agent is EXP: return exp-value(state)


        def max-value(state):
            initialize v = -inf
            for each successor of state:
                v = max(v, value(successor))
            return v

        def exp-value(state):
            initialize v = 0
            for each successor of state:
                p = proabbility(successor)
                v += p * value(successor)
            return v
        """
         #if game is alread win or lose, it does not need to return anything
        if gameState.isWin() or gameState.isLose():
            return None
        

        def value(agent, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            # if Pacman's turn Max
            if agent == 0:  
                return max_value(agent, depth, gameState)
            else:  # if Ghost's turn Expected
                return exp_value(agent, depth, gameState)

        def exp_value(agent, depth, gameState):
            v = 0
            legal_actions = gameState.getLegalActions(agent)
            #calculate the probability of each actions 
            p = 1.0 / len(legal_actions)
            for action in legal_actions:
                #compute the value for this actions's successor and add it tto the expected value
                v += p * value((agent + 1) % gameState.getNumAgents(), depth + (agent + 1) // gameState.getNumAgents(), gameState.generateSuccessor(agent, action))
            return v
        #same as the max_value before 
        def max_value(agent, depth, gameState):
            v = float("-inf")
            for action in gameState.getLegalActions(agent):
                v = max(v, value((agent + 1) % gameState.getNumAgents(), depth, gameState.generateSuccessor(agent, action)))
            return v

        # find the best action for Pacman
        bestScore = float("-inf")
        bestAction = None
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = value(1, 0, successor)
            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #successorGameState = currentGameState.generatePacmanSuccessor()
    #get current state information
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    score = currentGameState.getScore()
    newCapsules = currentGameState.getCapsules()

    #let pacman to get closest food use manhattandistance to track the closet food
    foodDist = [manhattanDistance(newPos, food) for food in newFood.asList()]
    if len(foodDist) > 0:
        score -= min(foodDist) * 1.5

    #panalty for more remaining food
    score -= len(newFood.asList()) * 100

    #encourage Pacman to get closest capsules
    if len(newCapsules) > 0:
        capsuleDist = [manhattanDistance(newPos, capsule) for capsule in newCapsules]
        score -= min(capsuleDist) * 2
    
    #compute the distance between Pacaman and ghost
    ghostDist = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]


    if len(ghostDist) > 0 and min(newScaredTimes) == 0:
        minGhostDist = min(ghostDist)
        # If the ghost is too close
        if minGhostDist < 2:
            #set the panalty
            score -= 1000
        else:
            # encourage that pacman stay away from ghost
            score += minGhostDist
    #so fi the ghost is scared, then encourage pacman to eat the ghost
    for i in range(len(newGhostStates)):
        if newScaredTimes[i] > 0:
            score -= 2 * manhattanDistance(newPos, newGhostStates[i].getPosition())
    #panalizer states with capsules left
    score -= len(newCapsules) * 120
    
    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
