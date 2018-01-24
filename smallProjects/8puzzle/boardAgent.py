from dna import DNA
import puzzle8

class BoardAgent:
    state = puzzle8.random_state(100)
    def __init__(self, dna=DNA([])):
        self.board = BoardAgent.state
        self.completed = False
        self.numMoves = 0
        self.tick = 0
        self.fitness = 0
        self.dna = dna

    def convertMove(self, move):
        return {
            0: -1,  # Left
            1: 1,   # Right
            2: 3,  # Down
            3: -3    # Up
        }[move]

    def makeMove(self):
        if self.board == 42374116 and not self.completed:
            print(self.tick)
            self.completed = True
        if not self.completed:
            bs = puzzle8.blank_square(self.board)
            if self.tick < len(self.dna.genes):
                convertDest = self.convertMove(self.dna.genes[self.tick]) + bs
                if convertDest in puzzle8.neighbors(bs):
                    self.board = puzzle8.move_blank(self.board, convertDest)
        else:
            self.fitness += 40
        self.tick += 1

    def calcFitness(self):
        sum = 0
        for i in range(8):
            if puzzle8.get_tile(self.board, i) == [1,2,3,4,5,6,7,8,0][i]:
                sum += 3
        #self.fitness = 1/(abs(puzzle8.solution() - self.board)+.001)
        self.fitness = sum * sum + 1 * 1/self.tick
        #print(self.fitness)
        if self.completed:
            #print("Found solution in " + str(self.tick) + " moves!")
            self.fitness *= 10
