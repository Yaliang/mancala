# File: Player.py
# Author(s) names AND netid's:
# Date: 
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *
import time

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose the best move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        alpha = -INFINITY
        beta = +INFINITY
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValueAlphaBeta(nb, ply-1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
            alpha = max(alpha, score)
        #return the best score and move so far
        return score, move

    def maxValueAlphaBeta(self, board, ply, turn, alpha, beta):
        """ Find the minimax value with alpha-beta pruning for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        a = -INFINITY
        b = +INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
 
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValueAlphaBeta(nextBoard, ply-1, turn, a, b)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
            # update alpha
            a = max(a, score)
            # check lower bounder
            if a >= beta:
                # the lower bounder is no better than parent's upper bounder
                #print "beta pruning happen"
                break
        return score
    
    def minValueAlphaBeta(self, board, ply, turn, alpha, beta):
        """ Find the minimax value with alpha-beta pruning for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        a = -INFINITY
        b = +INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValueAlphaBeta(nextBoard, ply-1, turn, a, b)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
            # update beta
            b = min(b, score)
            # check upper bounder
            if b <= alpha:
                # the upper bounder is no better than parent's lower bounder
                #print "alpha pruning happen"
                break
        return score
    
    
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        startTime = time.time()
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            endTime = time.time()
            print "Use time", endTime - startTime, " s"
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            endTime = time.time()
            print "Use time", endTime - startTime, " s"
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            endTime = time.time()
            print "Use time", endTime - startTime, " s"
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            endTime = time.time()
            print "Use time", endTime - startTime, " s"
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            print "Custom player not yet implemented"
            return -1
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class MancalaPlayer(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        # own_cup_score = board.scoreCups[self.num-1]*2
        # side_cup = board.getPlayersCups(self.num)
        # blank_cup_score = 0
        # side_cup_score = 0
        # for cup_label in range(len(side_cup)):
        #     side_cup_score = side_cup[cup_label]
        #     if side_cup[cup_label] == 0 and 1 <= cup_label <= 2:
        #         blank_cup_score += 0.3
        #     elif side_cup[cup_label] == 0 and 3 <= cup_label <=5:
        #         blank_cup_score += 0.5
        #     else:
        #         blank_cup_score += 0.1
        # tolscore = own_cup_score + side_cup_score + blank_cup_score
        # #print "Calling score in MancalaPlayer"
        # return tolscore

        # get the # of stone in score cup
        selfSideInScoreCup = board.scoreCups[self.num-1]
        oppSideInScoreCup = board.scoreCups[self.opp-1]
        # get the situation of one side
        selfSideStoneInCup = board.getPlayersCups(self.num)
        oppSideStoneInCup = board.getPlayersCups(self.opp)
        # get the # of stone in one side by current situation
        selfSideStoneInCupSum = sum(board.getPlayersCups(self.num))
        oppSideStoneInCupSum = sum(board.getPlayersCups(self.opp))
        # calculate the # of stone which will cross in next step and the max distance that influenced
        selfSideStoneNextStepCross = 0
        oppSideStoneNextStepCross = 0
        selfSideInfluencedMax = 0
        oppSideInfluencedMax = 0
        for cupIndex in range(board.NCUPS):
            overOneSide = selfSideStoneInCup[cupIndex] - board.NCUPS - cupIndex
            while overOneSide > board.NCUPS + 1:
                selfSideStoneNextStepCross += board.NCUPS + 1
                overOneSide -= (board.NCUPS + 1)*2
                selfSideInfluencedMax = board.NCUPS
            selfSideStoneNextStepCross += overOneSide
            selfSideInfluencedMax = max(selfSideInfluencedMax, overOneSide)

            overOneSide = oppSideStoneInCup[cupIndex] - board.NCUPS - cupIndex
            while overOneSide > board.NCUPS + 1:
                oppSideStoneNextStepCross += board.NCUPS + 1
                overOneSide -= (board.NCUPS + 1)*2
                oppSideInfluencedMax = board.NCUPS
            oppSideStoneNextStepCross += overOneSide
            oppSideInfluencedMax = max(oppSideInfluencedMax, overOneSide)
        # calculate the # of stone which can be collect in opp's cup because of end in a emplty cup
        selfSideEndInEmptyBonus = 0
        oppSideEndInEmptyBonus = 0
        for cupIndex in range(board.NCUPS):
            circles = selfSideStoneInCup[cupIndex] / (2 * board.NCUPS + 1)
            circleLeft = selfSideStoneInCup[cupIndex] % (2 * board.NCUPS + 1)
            if (circles == 1) and (circleLeft == 0):
                selfSideEndInEmptyBonus = max(selfSideEndInEmptyBonus, oppSideStoneInCup[board.NCUPS - 1 - cupIndex])
            elif (circles == 0) and (circleLeft < board.NCUPS - cupIndex) and (circleLeft > 0) and (selfSideStoneInCup[cupIndex + circleLeft] == 0):
                selfSideEndInEmptyBonus = max(selfSideEndInEmptyBonus, oppSideStoneInCup[board.NCUPS - 1 - cupIndex - circleLeft])
            elif (circles == 0) and (circleLeft > 2 * board.NCUPS - cupIndex) and (selfSideStoneInCup[circleLeft + cupIndex - 2 * board.NCUPS -1] == 0):
                selfSideEndInEmptyBonus = max(selfSideEndInEmptyBonus, oppSideStoneInCup[board.NCUPS - circleLeft - cupIndex + 2 * board.NCUPS])

            circles = oppSideStoneInCup[cupIndex] / (2 * board.NCUPS + 1)
            circleLeft = oppSideStoneInCup[cupIndex] % (2 * board.NCUPS + 1)
            if (circles == 1) and (circleLeft == 0):
                oppSideEndInEmptyBonus = max(oppSideEndInEmptyBonus, selfSideStoneInCup[board.NCUPS - 1 - cupIndex])
            elif (circles == 0) and (circleLeft < board.NCUPS - cupIndex) and (circleLeft > 0) and (oppSideStoneInCup[cupIndex + circleLeft] == 0):
                oppSideEndInEmptyBonus = max(oppSideEndInEmptyBonus, selfSideStoneInCup[board.NCUPS - 1 - cupIndex - circleLeft])
            elif (circles == 0) and (circleLeft > 2 * board.NCUPS - cupIndex) and (oppSideStoneInCup[circleLeft + cupIndex - 2 * board.NCUPS -1] == 0):
                oppSideEndInEmptyBonus = max(oppSideEndInEmptyBonus, selfSideStoneInCup[board.NCUPS - circleLeft - cupIndex + 2 * board.NCUPS])

        if board.hasWon(self.num):
            return 100.0
        elif selfSideInScoreCup > board.NCUPS*4:
            return 100.0
        elif selfSideStoneNextStepCross == 0 and selfSideStoneInCupSum == 1 and selfSideStoneInCupSum + selfSideEndInEmptyBonus + selfSideInScoreCup > board.NCUPS*4:
            return 100.0
        elif selfSideInfluencedMax <= board.NCUPS-2 and selfSideStoneInCup[board.NCUPS-1] == 1 and selfSideStoneInCup[board.NCUPS-2] == 2 and selfSideInScoreCup+3 > board.NCUPS*4:
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        elif oppSideInScoreCup > board.NCUPS*4:
            return 0.0
        elif oppSideStoneNextStepCross == 0 and oppSideStoneInCupSum == 1 and oppSideStoneInCupSum + oppSideEndInEmptyBonus + oppSideInScoreCup > board.NCUPS*4:
            return 0.0
        elif oppSideInfluencedMax <= board.NCUPS-2 and oppSideStoneInCup[board.NCUPS-1] == 1 and oppSideStoneInCup[board.NCUPS-2] == 2 and oppSideInScoreCup+3 > board.NCUPS*4:
            return 0.0
        else:
            return selfSideInScoreCup * 2 + selfSideStoneInCupSum * 1 - selfSideStoneNextStepCross * 0.5 + oppSideStoneNextStepCross * 0.5 + selfSideEndInEmptyBonus * 0.5 - oppSideEndInEmptyBonus * 0.5
            #return 50.0