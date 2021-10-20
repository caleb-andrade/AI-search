"""
Created on      Sun Sep 13 20:07:18 2015
Last modified   Sat Sep 19 20:43:01 2015

@author: Caleb Andrade

Implementation of a game class and some other helper functions and 
an extension of game class with more methods to interact with 'search.py'
"""
import readGame
from config import DIRECTION

#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_corner(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################
class game:
    
    def __init__(self, filePath):
        self.gameState = readGame.readGameState(filePath)
        self.nodesExpanded = 0
        self.trace = []  
        
    def is_corner(self, pos):
         """
         Checks if pos lies in any of the four 2x2 corner matrices.
         """
         return 0 <= pos[0]%5 <=1 and 0 <= pos[1]%5 <=1
        
    def getNextPosition(self, oldPos, direction):
        """
        Returns the position two boxes away in the given direction.
        """
        return nextPeg(oldPos, direction, 2)
    
    def is_validMove(self, oldPos, direction):
        """
        Checks if new position is a valid move.
        """
        ###############################################
        # DONT Change Things in here
        newPos = self.getNextPosition(oldPos, direction)
        if self.is_corner(newPos):
            return False    
        ###############################################
        # is there a peg in oldPos?
        if self.gameState[oldPos[0]][oldPos[1]] != 1:
            return False         
        # is new move outside peg Board?
        if 6 < newPos[0] or newPos[0] < 0 or 6 < newPos[1] or newPos[1] < 0:
            return False        
        # is there a peg to jump?
        neighbor = nextPeg(oldPos, direction, 1)
        if self.gameState[neighbor[0]][neighbor[1]] == 0:
            return False
        # is new position unoccupied?
        if self.gameState[newPos[0]][newPos[1]] == 1:
            return False
        return True
    
    def getNextState(self, oldPos, direction):
        """
        Updates game state: empties both oldPos and jumped 
        peg holder, fills newPos.
        """
        if oldPos == None or direction == None:
            return self.gameState
        ###############################################
        # DONT Change Things in here
        self.nodesExpanded += 1
        if not self.is_validMove(oldPos, direction):
            print "Error, You are not checking for valid move"
            exit(0)
        ###############################################
        # update oldPos in game state and put it in trace                
        self.trace.append(oldPos)        
        self.gameState[oldPos[0]][oldPos[1]] = 0
        # update newPos in game state and put it in trace
        newPos = self.getNextPosition(oldPos, direction)
        self.trace.append(newPos)
        self.gameState[newPos[0]][newPos[1]] = 1
        # update crossed peg holder in game state
        crossPeg = nextPeg(oldPos, direction, 1)
        self.gameState[crossPeg[0]][crossPeg[1]] = 0
        return self.gameState 
        
# helper function for class game
def nextPeg(oldPos, direction, hopBy):
        """
        Returns the new position in the given 'direction', starting 
        from 'oldPos' and the number of boxes specified by 'hopBy'.
        """
        row = oldPos[0] + hopBy*DIRECTION[direction][0]
        col = oldPos[1] + hopBy*DIRECTION[direction][1]
        return row, col
        
# a subclass of game. Includes more methods to interact with search.py  
class game(game):
    """
    This is a sub-class of game class. 
    """
    
    def __str__(self):
        """
        As string.
        """
        row = ''
        for i in range(7):
            for j in range(7):
                if self.gameState[i][j] == -1:
                    row += '   '
                if self.gameState[i][j] == 1:
                    row += ' X '
                if self.gameState[i][j] == 0:
                    row += ' . '
            row += '\n'
        return row
        
    def pegPositions(self):
        """
        Returns the positions of pegs in game state as a list of tuples.
        """
        pegs = []
        for i in range(7):
            for j in range(7):
                if not self.is_corner((i, j)) and self.gameState[i][j] == 1:
                    pegs.append((i,j))
        return pegs
        
    def numberOfPegs(self):
        """
        Returns the number of pegs in the board.
        """
        return len(self.pegPositions())
        
    def isGoal(self):
        """
        Evaluates if the state is Goal: only one peg at the center.
        """
        return self.numberOfPegs() == 1 and self.gameState[3][3] == 1
        
    def makeCopy(self):
        """
        Returns a copy of gameState and trace.
        """
        gameStateCopy = [list(row) for row in self.gameState]
        return gameStateCopy, list(self.trace)
   
    def childrenStates(self):
        """
        Returns all possible children states for 'self.gameState', 
        stored as a list of tuples:'(parent, oldPos, direction)'.
        To get actual children, apply getChildren with 'parent', 
        'oldPos' and 'direction' as arguments.
        """
        children = []
        pegs = self.pegPositions()
        # for every peg determine its valid moves
        for oldPos in pegs:
            for direction in ('N', 'S', 'E', 'W'):
                if self.is_validMove(oldPos, direction):
                    children.append((self.makeCopy(), oldPos, direction))
        return children
                    
    def reverseMove(self):
        """
        Backtracks one step from current gameState and trace. Is the 
        reverse method of getNextState, used to backtrack initial state
        from a given state. Does not change nodesExpanded.
        """
        if len(self.trace) == 0:
            return
        # extracting move from trace and restoring values in game state
        newPos = self.trace.pop()
        oldPos = self.trace.pop()
        self.gameState[newPos[0]][newPos[1]] = 0
        self.gameState[oldPos[0]][oldPos[1]] = 1
        # restoring crossed peg value
        if newPos[0] == oldPos[0]:
            self.gameState[newPos[0]][(newPos[1] + oldPos[1])/2] = 1
        if newPos[1] == oldPos[1]:
            self.gameState[(newPos[0] + oldPos[0])/2][newPos[1]] = 1
        
def farthestManhattan(gameState):
    """
    Computes the farthest manhattan distance of any peg to the
    peg holder at the center. We divide this by two as a peg advances
    two boxes at each valid move.
    """
    champ = 0
    for i in range(7):
        for j in range(7):
            peg = gameState[i][j]
            if peg == 1:
                manhattan = abs(i-3) + abs(j-3)
                if manhattan > champ:
                    champ = manhattan
    return float(champ) / 2
        
def totalManhattan(gameState):
    """
    Computes the total sum of manhattan distances of all pegs to the
    peg holder at the center. We divide by two as a peg advances
    two boxes at each valid move.
    """
    total = 0
    for i in range(7):
        for j in range(7):
            peg = gameState[i][j]
            if peg == 1:
                total += abs(i-3) + abs(j-3)
    return float(total) / 2

def getChildren(parent, oldPos, direction):
    """
    Returns the 'gameState' of a children given its 'parent: 
    (gameState, trace)', 'oldPos' and 'direction'.
    """
    parent[1].append(oldPos)        
    parent[0][oldPos[0]][oldPos[1]] = 0
    # update newPos in game state and put it in trace
    newPos = nextPeg(oldPos, direction, 2)
    parent[1].append(newPos)
    parent[0][newPos[0]][newPos[1]] = 1
    # update crossed peg holder in game state
    crossPeg = nextPeg(oldPos, direction, 1)
    parent[0][crossPeg[0]][crossPeg[1]] = 0
    return parent 


  
        
   
