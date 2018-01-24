from boardAgent import BoardAgent
import random
class Population:
    def __init__(self, popsize):
        self.agents = []
        self.matingpool = []
        self.popsize = popsize
        for i in range(self.popsize):
            self.agents.append(BoardAgent())

    def evaluate(self):
        maxfit = 0
        for i in range(self.popsize):
            self.agents[i].calcFitness()
            if self.agents[i].fitness > maxfit:
                maxfit = self.agents[i].fitness
        for i in range(self.popsize):
            self.agents[i].fitness /= maxfit

        self.matingpool = []
        for i in range(self.popsize):
            n = int(self.agents[i].fitness) * 100
            for j in range(n):
                self.matingpool.append(self.agents[i])
        print(str(maxfit) + ": maxfit")

    def selection(self):
        newAgents = []
        for i in range(len(self.agents)):
            parentA = random.choice(self.matingpool).dna
            parentB = random.choice(self.matingpool).dna
            child = parentA.crossover(parentB)
            child.mutation()
            newAgents.append(BoardAgent(child))
        self.agents = newAgents

    def run(self):
        for i in range(self.popsize):
            self.agents[i].makeMove()
            #  Show
