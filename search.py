"""
Created on      Sun Sep 13 20:07:18 2015
Last modified   Sat Sep 24 16:15:01 2015

@author: Caleb Andrade

This is an implementation of Iterative Deepening Search and A* to solve
Solitaire 33. A* uses two different heuristics: farthestManhattan and 
totalManhattan. A pruning technique is used in A* to eliminate duplicates,
this is implemented by the function 'bestChild(queue)'
"""
import pegSolitaireUtils as psu

def ItrDeepSearch(pegSolitaireObject):
    # set initial parameters    
    depth = 0
    finish = False
    # make a copy of initial gameState
    gameState = [list(row) for row in pegSolitaireObject.gameState]
    while not finish:
        # reset instance variables to initial state
        pegSolitaireObject.gameState = gameState
        pegSolitaireObject.trace = []
        # initialize list of seen states
        seenStates = [[] for idx in range(depth + 1)]
        # apply recursion
        trace = recursiveDLS(pegSolitaireObject, depth, seenStates)
        if trace != []:
            finish = True
        depth += 1
    return trace

def aStarOne(pegSolitaireObject):
    return aStar(pegSolitaireObject, 1)
      
def aStarTwo(pegSolitaireObject):
    return aStar(pegSolitaireObject, 2)
    
#************************************************************************
# Helper functions
    
def recursiveDLS(board, limit, seen):
    """
    Recursive Depth Limited Search implementation to solve Solitaire 33.
    Takes as arguments a game object 'board', an integer 'limit' and an 2Darray
    'seen'. The first argument is the root of the game search tree, the second
    argument is the depth that limits DFS, the third argument is the seen game
    states that will be expanded at each iteration of DLS. This array stores those seen states,
    so that already seen gameStates are not explored (pruning rule). Each seen
    state is stored in a sublist according to the depth at which it was seen.
    """
    cutoff = False
    if board.isGoal():
        return board.trace
    elif limit == 0:
        return []
    else:
        for item in board.childrenStates():
            child = psu.getChildren(item[0], item[1], item[2])
            # checking if child has been seen before
            if child[0] in seen[limit]:
                # pruning rule applied!
                continue
            else:
                # state not previously seen, add it to seen
                seen[limit].append(child[0])
            # updating game state and trace of board to child's values
            board.gameState = child[0]
            board.trace = child[1]
            board.reverseMove()
            board.getNextState(item[1], item[2])
            trace = recursiveDLS(board, limit - 1, seen)
            if len(trace) == 0:
                cutoff = True
            elif trace != [(0,0)]:
                return trace
    if cutoff:
        return []
    else:
        return [(0,0)]

def aStar(board, n):
    """
    Takes as argument a game object 'board' and 'n' which takes values
    in {1, 2}, referring to the priority function f1 or f2. 
    Returns the trace of the solution using the Astar algorithm. 
    Elements in queue are tuples: '(parent, priority, peg, direction)',
    a child is constructed as 'parent.getNextState(peg, direction)'.
    """
    # initialize PQ
    root = board.makeCopy()
    queue = [(root, priority(root, n), None, None)] 
    while len(queue) > 0:
        # sort by priority
        queue.sort(key = lambda item: item[1])
        node = bestChild(queue) 
        # updating game state and trace of board to node's values
        board.gameState = node[0][0]  
        board.trace = node[0][1]
        board.reverseMove()
        board.getNextState(node[2], node[3])
        # checking if we found the goal state
        if board.isGoal(): 
            return board.trace
        for item in board.childrenStates():
            child = psu.getChildren(item[0], item[1], item[2])
            queue.append((child, priority(child, n), item[1], item[2]))
    print "\nNo solution for this input!"
    return []

def priority(StateTrace, n):
    """
    Computes the priority of a board's gameSate and Trace according to 
    heuristic n = 1 or 2. Receives as input a tuple '((gameState, trace), n)'.
    """
    if n == 1:
        return psu.farthestManhattan(StateTrace[0]) + len(StateTrace[1])/2
    if n == 2: 
        return psu.totalManhattan(StateTrace[0]) + len(StateTrace[1])/2
        
def bestChild(queue):
    """
    Pops the child with least priority, also, eliminates duplicates of this
    child by searching only those with the same priority than the child, at 
    the beginning of the queue.
    """
    child = queue.pop(0)
    idx = 0
    indices = []
    # while elements searched for, have the same priority
    while(idx < len(queue) and queue[idx][1] == child[1]):
        if queue[idx][0][0] == child[0][0]:
            indices.append(idx)
        idx += 1
    
    if len(indices) > 0:
        indices.sort(reverse = True)
        for i in indices:
            queue.pop(i)
    return child
    
def printBoard(gameState):
    """
    Returns a string representation of a gameState.
    """
    row = ''
    for i in range(7):
        for j in range(7):
            if gameState[i][j] == -1:
                row += '   '
            if gameState[i][j] == 1:
                row += ' X '
            if gameState[i][j] == 0:
                row += ' . '
        row += '\n'
    print row

    
    
    
        
        
        
    
