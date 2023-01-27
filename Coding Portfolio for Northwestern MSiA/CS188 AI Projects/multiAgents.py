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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        new_food = newFood.asList()
        food_score_0 = successorGameState.getScore() - len(new_food)
        food_dist = [manhattanDistance(newPos, food_pos) for food_pos in new_food]
        if len(food_dist) > 0:
            food_score = 1/min(food_dist) + food_score_0
        if len(food_dist) == 0:
            food_score = food_score_0 + 2
        for ghost_state in newGhostStates:
            ghost_x, ghost_y = ghost_state.getPosition()
            ghost_x, ghost_y = int(ghost_x), int(ghost_y)
            if manhattanDistance(newPos, (ghost_x, ghost_y)) <= 2:
                food_score = food_score_0 - 99999
        return food_score




def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        return self.minimax_search(gameState, self.depth, 0)[1]

    def minimax_search(self,gameState,dist_to_root,agentIndex):
        if gameState.isLose() or gameState.isWin() or dist_to_root == 0:
            return self.evaluationFunction(gameState), Directions.STOP
        #if Pacman, max search
        if agentIndex == 0:
            return self.max(gameState, dist_to_root, agentIndex)
        #if ghost, min search
        else:
            return self.min(gameState, dist_to_root, agentIndex)


    def min(self, gameState, dist_to_root, agentIndex):
        #if last ghost, then go to the next layer:
        num_agents = gameState.getNumAgents()
        if agentIndex == num_agents - 1:
            new_dist_to_root = dist_to_root - 1
            new_agent = 0 #back to Pacman
        else:
            new_agent = agentIndex + 1
            new_dist_to_root = dist_to_root
        #explore an agent's actions:
        actions = gameState.getLegalActions(agentIndex)
        min_score = float('inf')
        for action in actions:
            suc_state = gameState.generateSuccessor(agentIndex, action)
            new_score = self.minimax_search(suc_state,new_dist_to_root,new_agent)[0]
            if new_score < min_score:
                min_score = new_score
                min_action = action
        return min_score, min_action

    def max(self, gameState, dist_to_root, agentIndex):
        #if last ghost, then go to the next layer:
        num_agents = gameState.getNumAgents()
        if agentIndex == num_agents - 1:
            new_dist_to_root = dist_to_root - 1
            new_agent = 0 #back to Pacman
        else:
            new_agent = agentIndex + 1
            new_dist_to_root = dist_to_root
        #explore an agent's actions:
        actions = gameState.getLegalActions(agentIndex)
        max_score = -float('inf')
        for action in actions:
            suc_state = gameState.generateSuccessor(agentIndex, action)
            new_score = self.minimax_search(suc_state,new_dist_to_root,new_agent)[0]
            if new_score > max_score:
                max_score = new_score
                max_action = action
        return max_score, max_action




        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.AlphaBetaSearch(gameState, 0, -float('inf'), float('inf'), self.depth)[1]

    def AlphaBetaSearch(self, gameState, agentIndex, Alpha, Beta, dist_to_root):
        if gameState.isLose() or gameState.isWin() or dist_to_root == 0:
            return self.evaluationFunction(gameState), Directions.STOP
        #if Pacman, do Alpha search
        if agentIndex == 0:
            return self.AlphaSearch(gameState, agentIndex, Alpha, Beta, dist_to_root)
        else:
            return self.BetaSearch(gameState, agentIndex, Alpha, Beta, dist_to_root)

    def AlphaSearch(self, gameState, agentIndex, Alpha, Beta, dist_to_root):
        num_agents = gameState.getNumAgents()
        if agentIndex == num_agents - 1:
            new_dist_to_root = dist_to_root - 1
            new_agent = 0 #back to Pacman
        else:
            new_agent = agentIndex + 1
            new_dist_to_root = dist_to_root
        max_val = -float('inf')
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            suc_state = gameState.generateSuccessor(agentIndex, action)
            new_score = self.AlphaBetaSearch(suc_state,new_agent,Alpha,Beta,new_dist_to_root)[0]
            if new_score > Beta:
                return new_score, action
            if new_score > max_val:
                max_val = new_score
                max_action = action
            Alpha = max(Alpha, max_val)
        return max_val, max_action

    def BetaSearch(self,gameState, agentIndex, Alpha, Beta, dist_to_root):
        num_agents = gameState.getNumAgents()
        if agentIndex == num_agents - 1:
            new_dist_to_root = dist_to_root - 1
            new_agent = 0 #back to Pacman
        else:
            new_agent = agentIndex + 1
            new_dist_to_root = dist_to_root
        min_val = float('inf')
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            suc_state = gameState.generateSuccessor(agentIndex, action)
            new_score = self.AlphaBetaSearch(suc_state,new_agent,Alpha,Beta,new_dist_to_root)[0]
            if new_score < Alpha:
                return new_score, action
            if new_score < min_val:
                min_val = new_score
                min_action = action
            Beta = min(Beta, min_val)
        return min_val, min_action



        #util.raiseNotDefined()



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """

        def helper_max(gameState, agentIndex):
            agentNum = gameState.getNumAgents()
            if agentIndex % agentNum == 0:
                max_action = None
                max_val = -float('inf')
                for action in gameState.getLegalActions(agentIndex % agentNum):
                    suc_state = gameState.generateSuccessor(agentIndex % agentNum, action)
                    if suc_state.isWin() or suc_state.isLose():
                        val = self.evaluationFunction(suc_state)
                    else:
                        val, act = helper_max(suc_state, agentIndex+1)
                    if val > max_val:
                        max_val = val
                        max_action = action

                return (max_val, max_action)

            # Ghost, Take average
            else:
                max_action = None
                lst = []
                for action in gameState.getLegalActions(agentIndex % agentNum):
                    suc_state = gameState.generateSuccessor(agentIndex % agentNum, action)
                    if suc_state.isWin() or suc_state.isLose() or agentIndex+1 == agentNum * self.depth:
                        val = self.evaluationFunction(suc_state)
                    else:
                        val, act = helper_max(suc_state, agentIndex + 1)
                    lst += [val]
                avg = sum(lst) / len(lst)
                return (avg, None)
        return helper_max(gameState, 0)[1]

        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    pB = currentGameState.getCapsules()
    GhostPos = currentGameState.getGhostPosition(1)
    GhostStates = currentGameState.getGhostStates()
    new_Scared_Times = [ghostState.scaredTimer for ghostState in GhostStates]
    curr_score = currentGameState.getScore()
    food_score = len(Food.asList())
    bscore =  curr_score - food_score - 10 * len(pB)
    dist_to_food = [manhattanDistance(Pos, food_pos) for food_pos in Food.asList()]
    if len(dist_to_food) > 0:
        bscore += 1/min(dist_to_food) # same as above
    elif manhattanDistance(Pos, GhostPos) <= 2: #Ghost too close
        bscore -= 99999
    return bscore
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
