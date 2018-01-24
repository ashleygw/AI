from random import randint


class DNA:
    defaultLifespan = 50
    def __init__(self, genes):
        if len(genes) != 0:
            self.genes = genes
        else:
            self.genes = []
            for i in range(DNA.defaultLifespan):
                self.genes.append(randint(0, 3))  # 4 available moves

    def crossover(self, partner):
        print(len(partner.genes))
        newgenes = []
        mid = randint(0, len(self.genes))
        difference = abs(len(self.genes) - len(partner.genes))
        if len(self.genes) > len(partner.genes):
            #cull = len(partner.genes) + int(difference/2)
            for i in range(len(partner.genes)):
                if i > mid:
                    newgenes.append(self.genes[i])
                else:
                    newgenes.append(partner.genes[i])
            for i in range(int(difference/2)):
                newgenes.append(self.genes[len(partner.genes) + i])
        else:
            #cull = len(self.genes) + int(difference/2)
            for i in range(len(self.genes)):
                if i > mid:
                    newgenes.append(partner.genes[i])
                else:
                    newgenes.append(self.genes[i])
            for i in range(int(difference/2)):
                newgenes.append(partner.genes[len(self.genes) + i])


        return DNA(newgenes)

    def mutation(self):
        index = len(self.genes)
        i=0
        while i < index:
            if randint(0, 100) < 2:
                self.genes[i] = randint(0, 3)
            if randint(0,100) < 2:
                self.genes.append(randint(0,3))
                index += 1
            if randint(0,100) < 3:
                del self.genes[i]
                index -= 1
            i+=1
