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
        # Collect legal moves and child states
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

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #ektos apo thn epomenh 8esh prepei na valw kai thn twrinh 8esh tou pacman

        "*** YOUR CODE HERE ***"

        total_score = childGameState.getScore()                                   #defining variables that will help solving the problem
        total_manh = 0
        newFood_list = newFood.asList()
        food_manh = []

        for x in newFood_list :                                                    #iterate all food dot positions

            manh = util.manhattanDistance(newPos,x)                                #finds manhattan distance between next poisiton of pacman and food position x
            food_manh.append(manh)                                                 #apppends manhattan distance to a list
            
        
        if len(food_manh) == 0 :                                                    #if food_manh list is empty there are no more food dots so we return the score

            return total_score


        for dist in food_manh :                                                     #add all manhattan distances in 1 variable (total_manh)

            total_manh = total_manh + dist


        for i in newGhostStates :                                                   #iterate all new Ghost positions

            manh = util.manhattanDistance(i.getPosition(),newPos)                   #find manhattan distance between new Ghost position (i) and new Pacman position (newPos)

            if manh == 1 :                                                          #if manhattan distance is 1 return (a very small number ie -1000 , so there is no chance this number is the biggest)

                return -1000                                                        #if helps so pacman can avoid ghosts

        total_score = total_score + (1/total_manh)                                  #since higher numbers and we want to get to the closest dot
                                                                                    #we have to reverse our manhattan distance addition so the higher the sum the loewst the total score                   
        return total_score

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

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def MAXVALUE(gameState,depth):                                               #function to return maximum value!!

            v = -(float("inf"))                                                      #v(value) starts from -oo  
                                                                                       
            Action = None
            Act_List = []                                                             #define an empty list and fill it with all legal actions of pacman
            Act_List = gameState.getLegalActions(0)

            if len(Act_List) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:                #if Pacman lost/won/there are no more legal actions to be done

                return(self.evaluationFunction(gameState),None)                                                     #return evaluation function with no Action as argument

            for a in Act_List:                                                      #iterates all legal actions 

                next_state = gameState.getNextState(0, a)                           #get next state of pacman(after doing a-action)

                next = MINVALUE(next_state, 1, depth)                               #call MINVALUE function with 1 as index                         
                next_score = next[0]                                                #get the score returned fro  min value 

                if(next_score > v):                                                 #compare it with v if v is less than next score v = next score and Action becomes current action of for (Action = a) 

                    v = next_score
                    Action = a                             

            return(v,Action)                                                        #returns score and action

        def MINVALUE(gameState,index,depth):                                        #function to return minimum value!!

            v = float("inf")                                                        #v(value) starts as +oo

            Action = None
            Act_List = []                                                           
            Act_List = gameState.getLegalActions(index)                             #define an empty list and fill it with all legal actions of agent with id => index

            if len(Act_List) == 0:                                                  #if there are no more legal actions we return evaluation function result with noaction as argument

                return(self.evaluationFunction(gameState),None)



            for a in Act_List:                                                      #iterate all legal actions of agent

                next_state = gameState.getNextState(index, a)                       #get the next state of agent after it does the action a

                if(index == gameState.getNumAgents() - 1):                          #check if min value function was called with pacman agent index or with other index!!

                    next = MAXVALUE(next_state,depth + 1)                           #call MAXVALUE function and returns the result to next

                else:

                    next = MINVALUE(next_state,index + 1,depth)                     #call MINVALUE function and returns the result to next

                next_score = next[0]                                                #takes score of next 

                if(next_score < v):                                                 #compare next_score to v if v more than next_score v becomes next score and Action becomes current action of for (Action = a)

                    v=next_score
                    Action = a

            return(v,Action)
            
        max_value = MAXVALUE(gameState,0)                                           #call MAXVALUE with current gamestate and index = 0(pacman id index!!)
        Next_Action = max_value[1]                                                  #get the next action which a result of MAXVALUE function
        return Next_Action       

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def MINVALUE(gameState, index, alpha, beta, depth):                         #function to return minimum value!!

            Act_List = []
            Act_List = gameState.getLegalActions(index)

            v = float("inf")                                                        #define an empty list and fill it with all legal actions of agent with id => index

            for a in Act_List:                                                      #iterate all legal actions of agent                                                    

                next_state = gameState.getNextState(index,a)                        #get the next state of agent after it does the action a
                temp = ALPHABETA(next_state, index + 1 , alpha, beta, depth)        #call ALPHABETA function

                if v > temp :                                                       #checks if value return from ALPHABETA is less than v

                    v = temp

                if v < alpha:                                                       #difference from previous functions is that now we have the pruning
                                                                                    #v < alpha , v < beta 
                    return v
                
                if v < beta :

                    beta = v

            return v

        def MAXVALUE(gameState, index, alpha, beta, depth):                          #function to return maximum value!!

            Act_List = []                                                            #define an empty list and fill it with all legal actions of agent with id =>index
            Act_List = gameState.getLegalActions(index)

            v = float("-inf")                                                        #now v starts as -oo

            for a in Act_List:

                next_state = gameState.getNextState(index,a)
                temp = ALPHABETA(next_state, index + 1, alpha, beta, depth)

                if v < temp :                                                           #again here we have pruning v > beta , v > alha

                    v = temp

                if v > beta:

                    return v

                if v > alpha :

                    alpha = v

            return v

        def ALPHABETA(gameState, index, alpha, beta, depth):                                #ALPHABETA function

            if index >= gameState.getNumAgents():                                           #this function is very similar to MINIMAX as it should be
                                                                                            #because it is an improved version of it
                index = 0                                                                   #to have less time complexity
                depth = depth + 1

            if ((depth == self.depth)) or ((gameState.isWin()) or (gameState.isLose())):     

                return self.evaluationFunction(gameState)

            if index == 0:

                return MAXVALUE(gameState, index, alpha, beta, depth)

            else:

                return MINVALUE(gameState, index, alpha, beta, depth)


        index = 0
        Action = 0
        alpha = float("-inf")
        beta = float("inf")

        Action_List = gameState.getLegalActions(index)

        for a in Action_List:                                           #iterate all legal actions of agent Pacman                              

            next_state = gameState.getNextState(index,a)                #get next state of Pacman agent after doing action a
            v = ALPHABETA(next_state,index + 1,alpha,beta,0)            #call ALPHABETA function

            if v > alpha:

              alpha = v
              Action = a

        return Action

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

        def MAXVALUE(gameState,index,depth):                                #function to return maximum value!!(basically same function as in minimax but now calls EXPECTIMAX) fuunction                

            Act_List = []                                                   #define an empty list and fill it with all legal actions of agent with id =>index
            Act_List = gameState.getLegalActions(index)
            v = float("-inf")                                               #v(value) starts as -oo

            for a in Act_List:                                              #iterate all legal actions                                              

                next_state = gameState.getNextState(index,a)                #get next state of Pacman agent after doing action a
                temp = EXPECTIMAX(next_state,index + 1,depth)               #call expectimax function
                
                if v < temp :                                               #compares v to tem(return value of EXPECTIMMAX function) if v is less than temp v becomes temp

                    v = temp

            return v


        def PROBVALUE(gameState,index,depth):                                #this is the probabillity function                                                            

            Act_List = []                                                    #define an empty list and fill it with all legal actions of agent with id =>index
            Act_List = gameState.getLegalActions(index)

            v = 0                                                            #v(value )is equal to 0 at start
            chance = 1.0 / len(Act_List)                                     #chance is given according to number of legal actions available

            for a in Act_List:                                               #iterates all legal actions

                next_state = gameState.getNextState(index,a)                 #finds the next game state after the agent does the action a
                temp = EXPECTIMAX(next_state,index + 1,depth) * chance       #calls EXPECTIMAX function and adds the temp value returned to v
                v = v + temp

            return v

        def EXPECTIMAX(gameState,index,depth):                               #EXPECTIMAX function is very similar to previous ALHABETA function

            if index >= gameState.getNumAgents():                            

                index = 0
                depth = depth + 1

            if (depth == self.depth or gameState.isWin() or gameState.isLose()):                #if Pacman has lost/won/reached the maximum depth

                return self.evaluationFunction(gameState)                                       #return score of evaluation function

            if index == 0:                                                                      #checks if this the index of Pacman

                return MAXVALUE(gameState,index,depth)                                          #if yes we return MAXVALUE function result

            else:

                return PROBVALUE(gameState,index,depth)                                         #if not we return PROBVALUE function result


        index = 0
        Action = ""
        v = float("-inf")                                                       #v(value) starts as -oo
        Act_List = []                                                           #define an empty list and fill it with all legal actions
        Act_List = gameState.getLegalActions(index)

        for a in Act_List:                                                      #iterates all legal actions

            next_state = gameState.getNextState(index,a)                        #get the next state of pacman agent after he does the action a
            next_v = EXPECTIMAX(next_state,index + 1,0)                         #take the EXPECTIMAX value returned

            if next_v > v:                                                      #compare it with v(value)  

                v = next_v                                                      #make v equal to next_v if next_v is larger than v
                Action = a                                                      #make action equal to current action-a of for 

        return Action


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
