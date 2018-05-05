"""
Make sure to fill in the following information before submitting your
assignment. Your grade may be affected if you leave it blank!
For usernames, make sure to use your Whitman usernames (i.e. exleyas). 
File name: bayesnet.py
Author username(s): ashleygw, millersm
Date: 5/4/2018
"""
'''
bayesnet.py
A module that uses randvar class to create a more complex bayes network and 
then query it for more complex probabilities
'''

import randvar
import csv
from itertools import chain
from collections import defaultdict
class BayesNet:
    
    def __init__(self, rvnodelist):
        '''
        Creates a Bayes Net from a given list of RVNode objects.
        Each of the given RVNode objects should know about their dependencies

        This should be all you need for this constructor, but feel free
        to add code if you want.
        '''
        self.nlist = rvnodelist
        self.depIndexes = {}
        for i, x in enumerate(rvnodelist):
            self.depIndexes[x] = i

    def train(self, examplelist):
        '''Trains this Bayes net from the given list of examples
       
            Essentially, each node in the network should be trained
            based on the examples given and their dependencies.

            Index in each example should correspond to index in nlist
            i.e. if our nlist consits of the three RVNodes [a1, b1, c1] 
            then an example [0, 0, 1] corresponds to a1=0, b1=0, c1=1.
        '''
        for i, node in enumerate(self.nlist):
            if not node.deps:
                node.train([x[i] for x in examplelist])
            else:
                dep_indices = [self.nlist.index(x) for x in node.deps]
                targets = [x[i] for x in examplelist]
                dep_list = []
                for i in dep_indices:
                    dep_list.append([x[i] for x in examplelist])
                training_list = dep_list + [targets]
                training_list = list(map(list, zip(*training_list)))
                node.train(training_list)



    def sample(self):
        '''Return a single sample from this bayes network.
        Generate sample values in network order (i.e. the order given in the list
        when this network was created)

        When a sample is created, use sample values generated for the first RVs as the 
        dependent values for later RVs.
        '''
        samplevals = []
        for i, node in enumerate(self.nlist):
            #print(node.CPT)
            if not node.deps:
                sample = node.sample()
                samplevals.append(sample)
            else:
                known = []
                for x in node.deps:
                    known.append(samplevals[self.depIndexes[x]])
                sample = node.sample(known)
                samplevals.append(sample)
        # print(samplevals)
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
    zcount = 0
    for i in range(1):
        result = net.sample()
        if result == 0:
            zcount += 1
    #print('After 1000 samples, got %d 0s.' % zcount)

def test_complexnet():
    r1 = randvar.RVNode('Burglary', [0,1])
    r2 = randvar.RVNode('Earthquake', [0,1])
    r3 = randvar.RVNode('Alarm', [0,1], [r1, r2])
    r4 = randvar.RVNode('JohnCalls', [0,1], [r3])
    r5 = randvar.RVNode('MaryCalls', [0,1], [r4])
    net = BayesNet([r1, r2, r3, r4, r5])
    
    reader = csv.reader(open('training.txt'), delimiter=',')
    trainlist = []
    cheatdictionary = defaultdict(lambda:0)
    total = 0
    for row in reader:
        total += 1
        cheatdictionary[tuple([int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4])])] +=1
        trainlist.append([int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4])])
    net.train(trainlist)
    udic = defaultdict(lambda: 0)
    for x in range(100000):
        udic[tuple(net.sample())] += 1
    # for x in cheatdictionary:
    #     print("ACTUAL ",x,": ",cheatdictionary[x]/total)
    for x in udic:
        print("MY/Actual",x,": ", udic[x]/100000, "X:   ", cheatdictionary[x]/total)
    # at this point, generate a large number of samples and use these to estimate
    # P(Burglary = 1 | MaryCalls = 1), P(Burglary = 1 | MaryCalls = 1, JohnCalls = 1)

def main():
    test_simplenet()
    test_complexnet()

if __name__ == '__main__':
    main()
