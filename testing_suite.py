"""
Created on      Sun Sep 13 20:07:18 2015
Last modified   Sat Sep 24 16:15:01 2015

@author: Caleb Andrade

This is a small set of tests for pegSolitaireUtils.py and search.py
"""
import pegSolitaireUtils as psu
import search

def testMethod(answer, expected_answer, test_number):
    if answer == expected_answer:
        print "test", test_number, " passed!"
    else:
        print "test ", test_number, " failed"
        
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

# testing aStarTwo
print "\n***************************************************************"
print "\nTesting aStarTwo (totalManhattan)"
board = psu.game('game.txt')
print board
print search.aStarTwo(board)
print "nodes expanded: ", board.nodesExpanded

# testing aStarOne
print "\n***************************************************************"
print "\nTesting aStarOne (farthestManhattan)"
board = psu.game('game.txt')
print board
print search.aStarOne(board)
print "nodes expanded: ", board.nodesExpanded

# testing Iterative Deepening Search
print "\n***************************************************************"
print "\nTesting Iterative Deepening Search: "
board = psu.game('game.txt')
print board
print search.ItrDeepSearch(board)
print "Nodes expanded: ", board.nodesExpanded

# testing recursive Depth Limited Search
print "\n***************************************************************"
print "\nTesting recursive Depth Limited Search: "
depth = 12
board = psu.game('game.txt')
seen = [[] for i in range(depth + 1)]
print search.recursiveDLS(board, depth, seen)
for i in range(depth):
    print board
    board.reverseMove()

# loading an initial game
x = psu.game('game.txt')

# testing method is_corner
print "\n***************************************************************"
print "\nTesting method is_corner \n"
y = [[x.is_corner((i, j)) for i in range(7)] for j in range(7)]
for row in y:
    print row
print

# testing method nextPeg
print "\n***************************************************************"
print "\nTesting method nextPeg\n"
testMethod(psu.nextPeg((3, 3), 'N', 1), (2, 3), '1 nextPeg')
testMethod(psu.nextPeg((3, 3), 'S', 1), (4, 3), '2 nextPeg')
testMethod(psu.nextPeg((3, 3), 'E', 1), (3, 4), '3 nextPeg')
testMethod(psu.nextPeg((3, 3), 'W', 1), (3, 2), '4 nextPeg')
print

# testing method getNextPosition
print "\n***************************************************************"
print "\nTesting method getNextPosition\n"
testMethod(x.getNextPosition((3, 3), 'N'), (1, 3), '1 getNextPosition')
testMethod(x.getNextPosition((3, 3), 'S'), (5, 3), '2 getNextPosition')
testMethod(x.getNextPosition((3, 3), 'E'), (3, 5), '3 getNextPosition')
testMethod(x.getNextPosition((3, 3), 'W'), (3, 1), '4 getNextPosition')
print

# testing method is_validMove
print "\n***************************************************************"
print "\nTesting method is valid move\n"
testMethod(x.is_validMove((1, 3), 'N'), False, '1 is_validMove')
testMethod(x.is_validMove((1, 3), 'S'), False, '2 is_validMove')
testMethod(x.is_validMove((1, 3), 'E'), False, '3 is_validMove')
testMethod(x.is_validMove((1, 3), 'W'), False, '4 is_validMove')
testMethod(x.is_validMove((6, 4), 'N'), False, '5 is_validMove')
testMethod(x.is_validMove((6, 4), 'S'), False, '6 is_validMove')
testMethod(x.is_validMove((6, 4), 'E'), False, '7 is_validMove')
testMethod(x.is_validMove((6, 4), 'W'), False, '8 is_validMove')
testMethod(x.is_validMove((2, 0), 'N'), False, '5 is_validMove')
testMethod(x.is_validMove((2, 0), 'S'), False, '6 is_validMove')
testMethod(x.is_validMove((2, 0), 'E'), False, '7 is_validMove')
testMethod(x.is_validMove((2, 0), 'W'), False, '8 is_validMove')
testMethod(x.is_validMove((2, 3), 'N'), True, '9 is_validMove')
testMethod(x.is_validMove((2, 3), 'S'), False, '10 is_validMove')
testMethod(x.is_validMove((2, 3), 'E'), True, '11 is_validMove')
testMethod(x.is_validMove((2, 3), 'W'), True, '12 is_validMove')

# testing method getNextState
print "\n***************************************************************"
print "\nTesting getNextState and isGoal methods \n"
testMethod(x.isGoal(), False, '1 isGoal')
print "Trace: ", x.trace
print x
x.getNextState((2, 3), 'E')
testMethod(x.isGoal(), False, '2 isGoal')
print "Trace: ", x.trace
print x
x.getNextState((4, 3), 'N')
testMethod(x.isGoal(), False, '3 isGoal')
print "Trace: ", x.trace
print x
x.getNextState((2, 2), 'E')
testMethod(x.isGoal(), False, '4 isGoal')
print "Trace: ", x.trace
print x
x.getNextState((2, 5), 'W')
testMethod(x.isGoal(), False, '5 isGoal')
print "Trace: ", x.trace
print x
x.getNextState((1, 3), 'S')
testMethod(x.isGoal(), True, '6 isGoal')
print "Trace: ", x.trace
print x

# testing method reverseMove, and Manhattan heuristics
print "\n***************************************************************"
print "\nTesting reverseMove method and Manhattan heuristics \n"
print "Farthest Manhattan: ", psu.farthestManhattan(x.gameState)
print "Total Manhattan: ", psu.totalManhattan(x.gameState) 
print x
x.reverseMove()
print "Farthest Manhattan: ", psu.farthestManhattan(x.gameState)
print "Total Manhattan: ", psu.totalManhattan(x.gameState)
print x
x.reverseMove()
print "Farthest Manhattan: ", psu.farthestManhattan(x.gameState)
print "Total Manhattan: ", psu.totalManhattan(x.gameState)
print x
x.reverseMove()
print "Farthest Manhattan: ", psu.farthestManhattan(x.gameState)
print "Total Manhattan: ", psu.totalManhattan(x.gameState)
print x
x.reverseMove()
print "Farthest Manhattan: ", psu.farthestManhattan(x.gameState)
print "Total Manhattan: ", psu.totalManhattan(x.gameState)
print x
x.reverseMove()
print "Farthest Manhattan: ", psu.farthestManhattan(x.gameState)
print "Total Manhattan: ", psu.totalManhattan(x.gameState)
print x
x.reverseMove()

# testing method childrenStates
print "\n***************************************************************"
print "\nTesting childrenStates method\n"
x = psu.game('game.txt')
print x
print "Trace: ", x.trace
print "Nodes expanded: ", x.nodesExpanded

for item in x.childrenStates():
    print "\nNeighbor "
    child = psu.getChildren(item[0], item[1], item[2])
    print "Trace: ", child[1]
    print "Nodes expanded: ", x.nodesExpanded
    printBoard(child[0])    
    
print "\n\nMove: ((2, 3), 'N')----------------------------------------"
x.getNextState((2, 3), 'N')
print x
for item in x.childrenStates():
    print "\nNeighbor "
    child = psu.getChildren(item[0], item[1], item[2])
    print "Trace: ", child[1]
    print "Nodes expanded: ", x.nodesExpanded
    printBoard(child[0])
x.reverseMove()

print "\n\nMove: ((2, 3), 'E')----------------------------------------"
x.getNextState((2, 3), 'E')
print x
for item in x.childrenStates():
    print "\nNeighbor "
    child = psu.getChildren(item[0], item[1], item[2])
    print "Trace: ", child[1]
    print "Nodes expanded: ", x.nodesExpanded
    printBoard(child[0])
x.reverseMove()

print "\n\nMove: ((2, 3), 'W')----------------------------------------"
x.getNextState((2, 3), 'W')
print x
for item in x.childrenStates():
    print "\nNeighbor "
    child = psu.getChildren(item[0], item[1], item[2])
    print "Trace: ", child[1]
    print "Nodes expanded: ", x.nodesExpanded
    printBoard(child[0])
x.reverseMove()

print "\n\nMove: ((3, 3), 'S')----------------------------------------"
x.getNextState((3, 3), 'S')
print x
for item in x.childrenStates():
    print "\nNeighbor "
    child = psu.getChildren(item[0], item[1], item[2])
    print "Trace: ", child[1]
    print "Nodes expanded: ", x.nodesExpanded
    printBoard(child[0])
x.reverseMove()



    





