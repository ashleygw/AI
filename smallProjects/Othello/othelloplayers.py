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


def utility(board, color):
    '''This very silly utility just adds up all the 1s, -1s, and 0s
    stored on the othello board.'''
    sum = 0
    for i in range(1, othelloboard.SIZE - 1):
        for j in range(1, othelloboard.SIZE - 1):
            sum += board.array[i][j]
            if i == 1 or j == 1 or i == othelloboard.SIZE - 1 or j == othelloboard.SIZE - 1:
                sum += board.array[i][j] * 2    
    return sum * color


stabilityHeuristic = [[4,-3,2,2,2,2,-3,4],[-3,-4,-1,-1,-1,-1,-4,-3],[2,-1,1,0,0,1,-1,2],[2,-1,0,1,1,0,-1,2],[2,-1,0,1,1,0,-1,2],[2,-1,1,0,0,1,-1,2],[-3,-4,-1,-1,-1,-1,-4,-3],[4,-3,2,2,2,2,-3,4]]
def utility2(board, color):
    sum = 0
    for i in range(1, othelloboard.SIZE - 1):
        for j in range(1, othelloboard.SIZE - 1):
            sum += board.array[i][j] * stabilityHeuristic[i-1][j-1] 
    return sum * color


class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''

    def __init__(self, name, color, utility, plies):
        self.name = name
        self.color = color
        self.utilityfn = utility
        self.plies = plies

    def chooseMove(self, board):
        moves = board._legalMoves(self.color)
        #movies = []
        if moves:
            bestMove = -1000
            for move in moves:
                #value = self.minimax(self.plies - 1, board.makeMove(move[0],move[1],self.color), -self.color, False,-100,100) # False = min case
                value = self.MINimax(board.makeMove(move[0],move[1],self.color), self.plies-1, -1000,1000)
                #value = self.negamax(self.plies - 1, board.makeMove(move[0],move[1],self.color),-self.color,-1000,1000)
                if value > bestMove:
                    bestMove = value
                    bestMoveFound = move
            return bestMoveFound
        else: return None

    def terminalStateBAD(self, board):
        return not board._legalMoves(1) and not board._legalMoves(-1)
        

    def MINimax(self, board, depth, alpha = None, beta = None):
        if depth == 0 or self.terminalStateBAD(board):
            return utility(board, self.color)
        boards = []
        for i in range(1, 9):
            for j in range(1, 9):
                bcopy = board.makeMove(i, j, -self.color)
                if bcopy != None:
                    boards.append(bcopy)
        if not boards:
            return self.miniMAX(board, depth - 1, alpha,beta)
        bestMove = 100
        for board in boards:
            bestMove = min(bestMove, self.miniMAX(board, depth - 1, alpha,beta))
            if bestMove <= alpha:
                return bestMove
            beta = min(beta, bestMove)
        return bestMove

    def miniMAX(self, board, depth, alpha = None, beta = None):
        if depth == 0 or self.terminalStateBAD(board):
            return utility(board, self.color)
        boards = []
        for i in range(1, 9):
            for j in range(1, 9):
                bcopy = board.makeMove(i, j, self.color)
                if bcopy != None:
                    boards.append(bcopy)
        if not boards:
            return self.MINimax(board, depth - 1, alpha,beta)
        bestMove = -100
        for board in boards:
            bestMove = max(bestMove, self.MINimax(board, depth - 1, alpha,beta))
            if bestMove >= beta:
                return bestMove
            alpha = max(alpha, bestMove)
        return bestMove


    def minimax(self, depth, board, turn, toggle, alpha=None, beta=None):
        boards = []
        for i in range(1, 9):
            for j in range(1, 9):
                bcopy = board.makeMove(i, j, turn)
                if bcopy != None:
                    boards.append(bcopy)

        if depth == 0:
            return utility(board, self.color)

        if not boards:
            if not board._legalMoves(-turn):
                return utility(board, self.color)
            else:
                return self.minimax(depth - 1, board, -turn, not toggle,alpha,beta)
        
        if toggle: #MAX CASE
            #print(spacing + "MAXIMIZING at depth: ", depth)
            bestMove = -100
            for board in boards:
                temp = self.minimax(depth - 1, board, -turn, False,alpha,beta)
                #choices.append(temp)
                bestMove = max(bestMove, temp)
                alpha = max(alpha, bestMove)
                if beta <= alpha:
                    return bestMove
        else:
            #print(spacing + "MINIMIZING at depth: ", depth)
            bestMove = 100 # MIN CASE
            for board in boards:
                temp = self.minimax(depth - 1, board, -turn, True,alpha,beta)
                #choices.append(temp)
                bestMove = min(bestMove, temp)
                beta = min(bestMove, beta)
                if beta <= alpha:
                    return bestMove
        #print(spacing + str(choices))
        #print(spacing + "BEST MOVE: ", bestMove, "Depth: ", depth)
        return bestMove

    def negamax(self, depth, board,turn, alpha, beta):
        if depth == 0:
            return utility2(board, turn)
        boards = []
        for i in range(1, 9):
            for j in range(1, 9):
                bcopy = board.makeMove(i, j, turn)
                if bcopy != None:
                    boards.append(bcopy)
        if not boards:
            if not board._legalMoves(-turn):
                return utility2(board, self.color)
            else:
                return -self.negamax(depth - 1, board,-turn,-beta,-alpha)
        for b in boards:
            score = -self.negamax(depth - 1,b,-turn, -beta, -alpha);
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
            return alpha


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