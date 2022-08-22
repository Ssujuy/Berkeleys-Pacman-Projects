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

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
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
    """
    "*** YOUR CODE HERE ***"

    mystack = util.Stack()                      #for DFS we use stack as our frontier
    visited = []                                #keep a visited list to avoid revisiting nodes
    mystack.push(problem.getStartState())       #push starting position in stack
    state = 0
    child = 0
    action = 0
    cost = 0
    children = []
    actions_list = []
    

    while mystack.isEmpty() == 0 :              

        child = mystack.pop()                   #pop child node to expand from stack


        if child == problem.getStartState() :       #if function helps because on first loop we dont have action or cost , because we are on starting position

            state = child

        else :

            state = child[0]                        #keep action,cost,state on variables
            action = child[1]
            cost = child[2]
            actions_list = mystack.pop()            #next pop is a list of actions we ued to reach the node-child

        if problem.isGoalState(state) == 1 :        #if node is a goal-state we return actions_list , which is a sequence of actions to reach that node

            return actions_list


        elif state not in visited :                 #if node is not in visited_list


            visited.append(state)                   #appends node in list , to not revisit/expand later
            children = problem.expand(state)        #expands node to find child nodes
            for i in children :

                temp_actions_list = actions_list + [i[1]]      #add action to reach child node to sequence of actions
                mystack.push(temp_actions_list)                 #push new action sequence list and child node , (Stack follows last-in first-out rule , so after expanding nodes for depth = 1 we will expand 1 node for depth = 2 etc)
                mystack.push(i)
    
    return None


        

        



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"


    visited = []
    state = 0
    child = 0
    action = 0
    cost = 0
    children = []
    actions_list = []

    myqueue = util.Queue()                  #for BFS we use queue as our frontier , (queue uses first-in first-out policy , so for depth = 1 all child nodes will be expanded before expanding nodes for depth = 2)
    myqueue.push(problem.getStartState())

    while myqueue.isEmpty() == 0 :

        child = myqueue.pop()               #pops child node from queue

        if child == problem.getStartState() :     #if function helps because on first loop we dont have action or cost , because we are on starting position  

            state = child
        
        else :

            state = child[0]                    #keep action,cost,state on variables
            action = child[1]
            cost = child[2]
            actions_list = myqueue.pop()

        if problem.isGoalState(state) == 1 :        #if node is a goal-state we return actions_list , which is a sequence of actions to reach that node

            return actions_list
        
        if state not in visited :                   #if node is not in visited_list

            visited.append(state)                   #appends node in list , to not revisit/expand later
            children = problem.expand(state)        #expands node to find child nodes

            for i in children :

                myqueue.push(i)                                 #child node is pushed first because of queue rule
                temp_actions_list = actions_list + [i[1]]       #add action to reach child node to sequence of actions
                myqueue.push(temp_actions_list)
 
    return None




    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    visited = []
    state = 0
    child = 0
    action = 0
    cost = 0
    children = []
    actions_list = []
    f = 0

    Pqueue_node = util.PriorityQueue()                  #in Astar search we will use PriorityQueue , (priority value will be f = h + g function (g = cost , h = heuristic-value) , PriorityQueue will pop node with the smallest value )
    Pqueue_actions = util.PriorityQueue()

    f = heuristic(problem.getStartState(),problem)      #f = g + h , but for staring position g is 0

    Pqueue_node.push(problem.getStartState(),f)          

    while Pqueue_node.isEmpty() == 0 :

        child = Pqueue_node.pop()                       #pop node with smallest value

        if child == problem.getStartState() :           #if function helps because on first loop we dont have action or cost , because we are on starting position  

            state = child

        else :

            state = child[0]                            #keep action,cost,state on variables
            action = child[1]
            cost = child[2]
            actions_list = Pqueue_actions.pop()

        if problem.isGoalState(state) == 1 :             #if node is a goal-state we return actions_list , which is a sequence of actions to reach that node

            return actions_list

        if state not in visited :                        #if node is not in visited_list   

            visited.append(state)                        #appends node in list , to not revisit/expand later
            children = problem.expand(state)             #expands node to find child nodes

            for i in children :

                temp_actions_list = actions_list + [i[1]]       #add action to reach child node to sequence of actions
                f = heuristic(i[0],problem) + problem.getCostOfActionSequence(temp_actions_list)            #finds value of f = g + h function 
                Pqueue_actions.push(temp_actions_list,f)        #we push new sequeencee of actions and child node in PriorityQueue with the same value-priority 
                Pqueue_node.push(i,f)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
