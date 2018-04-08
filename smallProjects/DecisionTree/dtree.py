'''
Decision tree trainer program

Usage: 
python3 dtree.py inputfile.csv
'''
import sys
import argparse
import csv
import bisect
import random
import math

class DTNode:
    '''
    Class representing a node of a decision tree
    '''
    def __init__(self, classification = None):
        # attribute index to split on
        self.attrindex = 0
        self.classification = classification
        self.children = {}

    def add_child(self, value, subtree):
        self.children[value] = subtree

class DTree:
    '''
    Class representing a decision tree
    '''
    def __init__(self, traindata):
        self.train(traindata)

    def classify(self, item):
        '''Given a single item, runs it on this decision tree and returns its
        classification.'''
        return self.rec_classify(self.root, item)

    def rec_classify(self, dtnode, item):
        '''Helper function to do tree recursion when classifying.
        '''
        if dtnode.classification != None:
            return dtnode.classification
        value = item[dtnode.attrindex]
        if value not in dtnode.children:
            sys.stderr.write('Error, there is no subtree for this example.\n')
            return None
        else:
            return self.rec_classify(dtnode.children[value], item)

    def test(self, testlist):
        '''Test the decision tree on the given list.
        Assumes that for each example in the given list, the last column is the correct classification.
        '''
        correct = 0
        for item in testlist:
            result = self.classify(item)
            if result == item[-1]:
                correct += 1
        print("Got %d/%d correct (=%.2f%%) on the test set." %
            (correct, len(testlist), 100 * correct/len(testlist)))

    def train(self, traindata):
        self.root = self.rec_train(traindata, list(range(len(traindata[0]) - 1)), None)
        
    def rec_train(self, examples, remaining_attributes, parent_examples):
        '''
        Returns a tree that is trained using the book's Decision-tree-learning algorithm
        '''
        if len(examples) == 0:
            return DTNode(classification = plurality(parent_examples))
        elif len(remaining_attributes) == 0:
            return DTNode(classification = plurality(examples))
        else:
            same = True
            cl = examples[0][-1]
            for e in examples:
                if e[-1] != cl:
                    same = False

            if same == True:
                #print('created leaf with class ' + cl)
                return DTNode(classification = cl)
            else:
                # recursive code
                attrindex = get_best_split_attr(examples, remaining_attributes)
                rtree = DTNode()
                rtree.attrindex = attrindex
                possible_values = get_values(examples, attrindex)
                for val in possible_values:
                    ex_subset = []
                    for item in examples:
                        if item[attrindex] == val:
                            ex_subset.append(item)
                    subtreeattrs = remaining_attributes[:]
                    subtreeattrs.remove(attrindex)
                    rtree.add_child(val, self.rec_train(ex_subset, subtreeattrs, examples))
                return rtree


def get_best_split_attr(datalist, remaining_attributes):
    '''Looks at the examples in datalist and determines the 
        best attribute (of remaining attributes) to split on.

        remaining_attributes is a list of indices into data items
        that tells us which attributes we can use to split on
    '''
    assert isinstance(datalist, list), 'datalist must be a list'
    assert isinstance(remaining_attributes, list), 'remaining_attributes must be a list'
    # This is part 3.3
    #  Figure out the split on the remaining attributes that will give us the 
    #  most information gain, and return that index.
    new_lists = {}
    splitEntropy = {}
    #GET current entropy
    survivors = 0
    dead = 0
    for row in datalist:
        if row[11] == "1":
            survivors +=1
        else:
             dead +=1
    # print("S",survivors)
    # print("D",dead)
    # assert(survivors+dead == len(datalist))
    currentEntropy = -survivors/len(datalist)*math.log(survivors/len(datalist),2) - dead/len(datalist)*math.log(dead/len(datalist),2)
    # print(currentEntropy)
    for i in remaining_attributes:
        new_lists = {}
        
        for x in datalist:
            if x[i] in new_lists:
                new_lists[x[i]].append(x)
            else:
                new_lists[x[i]] = [x]
        for key,value in new_lists.items():
            survivors = 0
            dead = 0
            for row in value:
                if row[11] == "1":
                    survivors +=1
                else:
                    dead +=1
            if dead == 0 or survivors == 0:
                splitEntropy[i] = 0
            else:
                splitEntropy[i] = -survivors/len(value)*math.log(survivors/len(value),2) - dead/len(value)*math.log(dead/len(value),2)
    print(splitEntropy)
    minEntropy = min(splitEntropy, key=splitEntropy.get)
    print(minEntropy)
    return minEntropy

def plurality(examples):
    '''Given a set of examples, returns the plurality of their classification
    (i.e. if there are mostly A's, some B's, some C's, will return A.)
    
    Assumes that the last item of each example is its correct classification
    '''
    ccount = {}
    for e in examples:
        if e[-1] not in ccount:
            ccount[e[-1]] = 1
        else:
            ccount[e[-1]] += 1
    attr = examples[0][-1]
    for k in ccount:
        if ccount[k] > ccount[attr]:
            attr = k
    return attr

def get_values(datalist, attrindex):
    '''gets all possible values of the given datalist at a given index
    '''
    assert isinstance(attrindex, int), 'attrindex must be an int'
    assert isinstance(datalist, list), 'datalist must be a list'
    rvals = set()
    for item in datalist:
        rvals.add(item[attrindex])
    return list(rvals)

def split_data(datalist):
    '''
    split the data into separate training and test sets
    '''
    assert isinstance(datalist, list), "datalist must be a list"
    # Part 3.2
    # You should implement this yourself. Erase the return line that 
    #  is here now, and split the data properly, return it.
    random.shuffle(datalist)
    return datalist[:int(-len(datalist)*.1)], datalist[-int(-len(datalist)*.9):]

def get_interval(x,category):
    if category == "age":
        bisectionList = [0,10,20,30,40,50,60,70,80,1000]
    else: # Fare
        bisectionList = [0,10,30,80,150,220,300,9999]
    i = bisect.bisect_right(bisectionList,x)
    return (bisectionList[i-1], bisectionList[i])

def load_csv_file(fname):
    '''loads a csv file into a two-dimensional list of lists.
        This code assumes that the first line is column header information.
        Further code assumes that the last column is the y column and everything
        else is the x vector
    '''
    assert isinstance(fname, str), "fname must be a string"
    
    # This is part 3.1
    # You may want to change this to get your program to treat certain data differently
    # i.e. turn age data into "adult"/"child" or something like that
    # You may want to think about what to do with missing data.
    # all of that can happen here.

    reader = csv.reader(open(fname), delimiter=',', quotechar='"')
    datalist = []
    totalYears = 0
    ageSize = 0
    totalFare = 0
    fareSize = 0
    i = 0
    for row in reader:
        if i == 0:
            i+=1
            continue
        #Names
        row[1] = row[1][0] #Make last name the first letter only
        #Age
        if row[3]:
            totalYears+= float(row[3])
            ageSize += 1 
        #Parch
        if row[5] != 0:
            row[5] = 1
        #Ticket number
        row[6] = row[6][0]
        #fare
        if row[7]:
            totalFare += float(row[7])
            fareSize += 1
        #Cabin
        if row[8]:
            row[8] = row[8][0]
        else:
            row[8] = ""
        #Home Dest
        if not row[10]:
            row[10]= ""
        datalist.append(row)

    ageAvg = totalYears/ageSize
    fareAvg = totalFare/fareSize
    # for row in datalist[1:]:
    #     if not row[10]:
    #         row[10] = random.choice(datalist)[10]
    for row in datalist[1:]:
        if not row[3]:
            row[3] = ageAvg
        if not row[7]: # Potentially a bad idea
            row[7] = fareAvg
    # Buckets
    for row in datalist[1:]:
        row[3] = get_interval(float(row[3]),"age")
        row[7] = get_interval(float(row[7]),"fare")
    # toss out row 0 and return
    return datalist[1:]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the csv file to read in and build a tree for")
    args = parser.parse_args()

    data = load_csv_file(args.filename)
    train,test = split_data(data)
    dt = DTree(train)
    dt.test(test)


if __name__ == '__main__':
    main()