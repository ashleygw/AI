'''
othelloboard.py

Othello Game info

Don't make changes to this code.

'''

import copy
import othelloplayers

# Constant values used throughout the code
WHITE = 1
BLACK = -1
EMPTY = 0
SIZE = 10


class OthelloBoard:
    '''An Othello board, with a variety of methods for managing a game.'''

    def __init__(self, array=None):
        '''If the parameter 'board' is left out, then the game board
        is initialized to its typical starting postion. Alternatively,
        a two-dimensional list with a pre-existing starting position
        can be supplied as well. Note that the size of the board is
        10x10, instead of 8x8; this is because leaving a blank ring
        around the edge of the board makes the rest of the code much
        simpler.'''
        if array:
            self.array = array
        else:
            self.array = [[EMPTY] * SIZE for i in range(SIZE)]
            self.array[4][4] = WHITE
            self.array[5][5] = WHITE
            self.array[4][5] = BLACK
            self.array[5][4] = BLACK

    def display(self):
        '''Displays the current board to the terminal window, with
        headers across the left and top. While some might accuse this
        text output as being "old school," having a scrollable game
        history actually makes debugging much easier.'''
        print('  ', end='')
        for i in range(1, 9):
            print(i, end='')
        print()
        print()
        for i in range(1, SIZE - 1):
            print(i, '', end='')
            for j in range(1, SIZE - 1):
                if self.array[i][j] == WHITE:
                    print('W', end='')
                elif self.array[i][j] == BLACK:
                    print('B', end='')
                else:
                    print('-', end='')
            print()

    def makeMove(self, row, col, piece):
        ''' Returns None if move is not legal. Otherwise returns an
        updated OthelloBoard, which is a copy of the original.'''

        # A move cannot be made if a piece is already there.
        if self.array[row][col] != EMPTY:
            return None

        # A move cannot be made if the piece "value" is not black or white.
        if piece != BLACK and piece != WHITE:
            return None

        # Make a copy of the board (not just the pointer!)
        bcopy = copy.deepcopy(self.array)
        bcopy[row][col] = piece

        # Ranges for use below
        rowup = range(row + 1, SIZE)
        rowdown = range(row - 1, -1, -1)
        rowfixed = [row for i in range(SIZE)]
        colup = range(col + 1, SIZE)
        coldown = range(col - 1, -1, -1)
        colfixed = [col for i in range(SIZE)]

        # Set up ranges of tuples representing all eight directions.
        vectors = [list(zip(rowup, coldown)), list(zip(rowup, colfixed)),
                   list(zip(rowup, colup)), list(zip(rowdown, coldown)),
                   list(zip(rowdown, colfixed)), list(zip(rowdown, colup)),
                   list(zip(rowfixed, coldown)), list(zip(rowfixed, colup))]

        # Try to make a move in each direction. Record if at least one
        # of them succeeds.
        flipped = False
        for vector in vectors:

            # Determine how far you can go in this direction. If you
            # see the opponent's piece, that's a candidate for
            # flipping: count and keep moving. If you see your own
            # piece, that's the end of the range and you're done. If
            # you see a blank space, you must not have had one of your
            # own pieces on the other end of the range.
            count = 0
            for (r, c) in vector:
                if bcopy[r][c] == -1 * piece:
                    count += 1
                elif bcopy[r][c] == piece:
                    break
                else:
                    count = 0
                    break

            # If range is nontrivial, then it's a successful move.
            if count > 0:
                flipped = True

            # Actually record the flips.
            # i = 0
            # while i < count:
            # print(r, c)
            # (r,c) = next(vector)
            # bcopy[r][c] = piece
            # i += 1
            for i in range(count):
                (r, c) = vector[i]
                bcopy[r][c] = piece

        if flipped:
            return OthelloBoard(bcopy)
        else:
            return None

    def _legalMoves(self, color):
        '''To be a legal move, the space must be blank, and you must take at
        least one piece. Note that this method works by attempting to
        move at each possible square, and recording which moves
        succeed. Therefore, using this method in order to try to limit
        which spaces you actually use in makeMoves is futile.'''
        moves = []
        for i in range(1, SIZE - 1):
            for j in range(1, SIZE - 1):
                bcopy = self.makeMove(i, j, color)
                if bcopy != None:
                    moves.append((i, j))
        return moves

    def scores(self):
        '''Returns a list of black and white scores for the current board.'''
        score = [0, 0]
        for i in range(1, SIZE - 1):
            for j in range(1, SIZE - 1):
                if self.array[i][j] == BLACK:
                    score[0] += 1
                elif self.array[i][j] == WHITE:
                    score[1] += 1
        return score

    def playGame(self, agent1=None, agent2=None):
        '''Manages playing an actual game of Othello.'''

        print('Black goes first.')
        # Two player objects: [BLACK, WHITE]
        players = [agent1, agent2]
        colorNames = ('BLACK', 'WHITE')
        colorValues = (BLACK, WHITE)
        invalidPasses = [0, 0]
        illegalMoves = [0, 0]

        # if either agent was not given, set both of them
        if agent1 == None or agent2 == None:
            # Determine whether each player is human or computer, and
            # instantiate accordingly
            for i in range(2):
                response = input('Should ' + colorNames[i] + \
                                 ' be (h)uman or (c)omputer? ')
                if response.lower() == 'h':
                    name = input("What is the player's name? ")
                    players[i] = othelloplayers.HumanPlayer(name, colorValues[i])
                else:
                    plies = int(input("How many plies ahead " + \
                                      "should the computer look? "))
                    players[i] = othelloplayers.ComputerPlayer(
                        'compy' + colorNames[i], colorValues[i],
                        othelloplayers.utility, plies)

        # Number of times a "pass" move has been made, in a row
        passes = 0

        done = False
        curBoard = self
        while not done:

            # Black goes, then white
            for i in range(2):

                # Display board and statistics
                curBoard.display()
                scores = curBoard.scores()
                print('Statistics: score / invalid passes / illegal moves')
                for j in range(2):
                    print(colorNames[j] + ':', scores[j], '/', invalidPasses[j], '/', illegalMoves[j])
                print()
                print('Turn:', colorNames[i])

                # Obtain move that player makes
                move = players[i].chooseMove(curBoard)

                if move == None:
                    # If no move is made, that is considered a
                    # pass. Verify that there were in fact no legal
                    # moves available. If there were, allow the pass
                    # anyway (this is easier to code), but record that
                    # an invalid pass was taken.

                    passes += 1
                    print(colorNames[i] + ' passes.')
                    legalMoves = curBoard._legalMoves(colorValues[i])
                    if legalMoves != []:
                        print(colorNames[i] + \
                              ' passed, but there was a legal move.')
                        print('Legal moves: ' + str(legalMoves))
                        invalidPasses[i] += 1
                else:
                    # If a move is made, make the move on the
                    # board. makeMove returns None if the move is
                    # illegal. Record as an illegal move, and forfeit
                    # the player's turn. This is easier to code than
                    # offering another turn.

                    passes = 0
                    print(colorNames[i] + ' chooses ' + str(move) + '.')
                    bcopy = curBoard.makeMove(move[0], move[1], colorValues[i])
                    if bcopy == None:
                        print('That move is illegal, turn is forfeited.')
                        illegalMoves[i] += 1
                    else:
                        curBoard = bcopy
                print()

                # To keep code simple, never test for win or loss; if
                # one player has won, lost, or tied, two passes must
                # occur in a row.
                if passes == 2:
                    print('Both players passed, game is over.')
                    done = True
                    break

        # Display final outcome
        scores = curBoard.scores()
        if scores[0] > scores[1]:
            print('Black wins!')
        elif scores[1] > scores[0]:
            print('White wins!')
        else:
            print('Tie game!')


if __name__ == '__main__':
    OthelloBoard().playGame()
