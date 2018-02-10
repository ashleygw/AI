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


def utility(board, color='white'):
    '''This very silly utility just adds up all the 1s, -1s, and 0s
    stored on the othello board.'''
    sum = 0
    for i in range(1, othelloboard.SIZE - 1):
        for j in range(1, othelloboard.SIZE - 1):
            sum += board.array[i][j]
            if i == 1 or j == 1 or i == othelloboard.SIZE - 1 or j == othelloboard.SIZE - 1:
                sum += board.array[i][j] * 2
    return sum

def minimax(depth, board, color, toggle, alpha=None, beta=None):
    moves = board._legalMoves(color)
    if depth == 0 or not moves:
        if (color == 1 and not toggle) or (color == -1 and toggle):
            return -utility(board)
        else:
            return utility(board) #white is positive evaluation
    else:
        if toggle: #MAX CASE
            bestMove = -9999
            for move in moves:
                bestMove = max(bestMove, minimax(depth - 1, board.makeMove(move[0],move[1], color), color * -1, not toggle))
        else:
            bestMove = 9999 # MIN CASE
            for move in moves:
                bestMove = min(bestMove, minimax(depth - 1, board.makeMove(move[0],move[1], color), color * -1, not toggle))
        return bestMove



class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''

    def __init__(self, name, color, utility, plies):
        self.name = name
        self.color = color
        self.utilityfn = utility
        self.plies = plies

    def chooseMove(self, board):
        '''This very silly player just returns the first legal move
        that it finds.'''
        moves = board._legalMoves(self.color)
        if moves:
            bestMove = -9999
            bestMoveFound = moves[0]  # why not
            for move in moves:
                value = minimax(self.plies - 1, board.makeMove(move[0],move[1],self.color), -1 * self.color, 0)
                if value >= bestMove:
                    bestMove = value
                    bestMoveFound = move
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
