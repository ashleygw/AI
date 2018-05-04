'''
bayesnet.py
A module that uses randvar class to create a more complex bayes network and 
then query it for more complex probabilities

'''

import randvar
import csv

class BayesNet:
    
    def __init__(self, rvnodelist):
        '''
        Creates a Bayes Net from a given list of RVNode objects.
        Each of the given RVNode objects should know about their dependencies

        This should be all you need for this constructor, but feel free
        to add code if you want.
        '''
        self.nlist = rvnodelist

    def train(self, examplelist):
        '''Trains this Bayes net from the given list of examples
       
            Essentially, each node in the network should be trained
            based on the examples given and their dependencies.

            Index in each example should correspond to index in nlist
            i.e. if our nlist consits of the three RVNodes [a1, b1, c1] 
            then an example [0, 0, 1] corresponds to a1=0, b1=0, c1=1.
        '''


    def sample(self):
        '''Return a single sample from this bayes network.
        Generate sample values in network order (i.e. the order given in the list
        when this network was created)

        When a sample is created, use sample values generated for the first RVs as the 
        dependent values for later RVs.
        '''
        samplevals = []

        return samplevals

                
def test_simplenet():
    r1 = randvar.RVNode('Cavity', [0,1])
    r2 = randvar.RVNode('Tootache', [0,1], dependencies = [r1])

    net = BayesNet([r1, r2])
    net.train([[0,0],
                [0,0],
                [0,0],
                [0,0],
                [0,0],
                [0,0],
                [0,1],
                [0,1],
                [1,0],
                [1,0],
                [1,0],
                [1,0],
                [1,1],
                [1,1],
                [1,1],
                [1,1],
                [1,1],
                [1,1],
                [1,1],
                [1,1],
                [1,1]])
    print(net.sample())

def test_complexnet():
    r1 = randvar.RVNode('Burglary', [0,1])
    r2 = randvar.RVNode('Earthquake', [0,1])
    r3 = randvar.RVNode('Alarm', [0,1], [r1, r2])
    r4 = randvar.RVNode('JohnCalls', [0,1], [r3])
    r5 = randvar.RVNode('MaryCalls', [0,1], [r4])
    net = BayesNet([r1, r2, r3, r4, r5])
    
    reader = csv.reader(open('training.txt'), delimiter=',')
    trainlist = []
    for row in reader:
        trainlist.append([int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4])])
    net.train(trainlist)

    print(net.sample())
    # at this point, generate a large number of samples and use these to estimate
    # P(Burglary = 1 | MaryCalls = 1), P(Burglary = 1 | MaryCalls = 1, JohnCalls = 1)

def main():
    test_simplenet()
    test_complexnet()

if __name__ == '__main__':
    main()
