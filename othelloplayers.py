"""
Make sure to fill in the following information before submitting your
assignment. Your grade may be affected if you leave it blank!
For usernames, make sure to use your Whitman usernames (i.e. exleyas).
File name: othelloplayers.py
Author username(s): ashleygw
Date: Friday 9th February
"""

'''You should modify the chooseMove code for the ComputerPlayer
class. You should also modify the utility function, which should
return a number indicating the value of that board position (the
bigger the better).

Feel free to add additional methods or functions.'''

import othelloboard


class HumanPlayer:
    '''Interactive player: prompts the user to make a move.'''

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def chooseMove(self, board):
        while True:
            try:
                move = eval('(' + input(self.name + ': enter row, column (or type "0,0" if no legal move): ') + ')')

                if len(move) == 2 and type(move[0]) == int and type(move[1]) == int and (move[0] in range(1, 9) and move[1] in range(1, 9) or move == (0, 0)):
                    break

                print('Illegal entry, try again.')
            except Exception:
                print('Illegal entry, try again.')

        if move == (0, 0):
            return None
        else:
            return move


def utility(board):
    '''This very silly utility just adds up all the 1s, -1s, and 0s
    stored on the othello board.'''
    sum = 0
    for i in range(1, othelloboard.SIZE - 1):
        for j in range(1, othelloboard.SIZE - 1):
            sum += board.array[i][j]
            if i == 1 or j == 1 or i == othelloboard.SIZE - 1 or j == othelloboard.SIZE - 1:
                sum += board.array[i][j] * 2
    return sum

def minimax(depth, board, turn, toggle, alpha=None, beta=None):
    moves = board._legalMoves(turn)
    spacing = "    " * depth
    choices = []
    if depth!=0:
        print(spacing + "Current Depth: ", depth)

    if depth == 0:
        # if og == -1:
        # if (turn == 1 and not toggle) or (turn == -1 and toggle):
        #     return utility(board) * turn * -1
        # else:
        #     return -utility(board) * turn
        return utility(board) *turn * -1  # Board state evaluated by not turn
        # else:
            # return utility(board) * turn 
    if not moves:
        return minimax(depth - 1, board, turn*-1, not toggle)
    if toggle: #MAX CASE
        print(spacing + "MAXIMIZING at depth: ", depth)
        bestMove = -100
        for move in moves:
            temp = minimax(depth - 1, board.makeMove(move[0],move[1], turn), turn * -1, not toggle)
            choices.append(temp)
            bestMove = max(bestMove, temp)
    else:
        print(spacing + "MINIMIZING at depth: ", depth)
        bestMove = 100 # MIN CASE
        for move in moves:
            temp = minimax(depth - 1, board.makeMove(move[0],move[1], turn), turn * -1, not toggle)
            choices.append(temp)
            bestMove = min(bestMove, temp)
    print(spacing + str(choices))
    print(spacing + "BEST MOVE: ", bestMove, "Depth: ", depth)
    return bestMove



class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''

    def __init__(self, name, color, utility, plies):
        self.name = name
        self.color = color
        self.utilityfn = utility
        self.plies = plies

    def chooseMove(self, board):
        moves = board._legalMoves(self.color)
        movies = []
        if moves:
            # if self.color == 1:
            #     toggle = False
            # else: toggle = True
            bestMove = -100
            #bestMoveFound = moves[0]  # why not
            for move in moves:
                value = minimax(self.plies - 1, board.makeMove(move[0],move[1],self.color), self.color * -1, False)
                movies.append(value)
                if value >= bestMove:
                    bestMove = value
                    bestMoveFound = move
            print("Best:", bestMove, "Choices:", movies)
            return bestMoveFound
        else: return None



"""def chooseMoveCopy(self, board):
        '''This very silly player just returns the first legal move
        that it finds.'''
        moves = []
        for i in range(1, othelloboard.SIZE - 1):
            for j in range(1, othelloboard.SIZE - 1):
                bcopy = board.makeMove(i, j, self.color)
                if bcopy:
                    print('Utility value = ', self.utilityfn(bcopy))
                    return (i, j)
        return None
"""
"""
    def chooseMoveLargestSum(self, board):
        '''This very silly player just returns the first legal move
        that it finds.'''
        moves = []
        summoves = {}
        for i in range(1, othelloboard.SIZE - 1):
            for j in range(1, othelloboard.SIZE - 1):
                bcopy = board.makeMove(i, j, self.color)
                if bcopy:
                    # ADD to list of possible moves
                    moves.append((i,j))
                    print('Utility value = ', self.utilityfn(bcopy))
        max = -1
        for x in moves:
            temp = x[0]+x[1]
            summoves[temp] = x
            if temp > max:
                max = temp
            elif temp == max:
                if summoves[max][0] > x[0]: #Saved max value r is bigger than current r
                    summoves[max] = x
"""