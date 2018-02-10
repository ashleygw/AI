class Node:
    '''
    Node class that keeps track of bookkeeping for our informed searches.
    '''

    def __init__(self, state, fcost, path):
        '''Constructor for a Node object

            state - the state associated with this Node
            fcost - the result of the evaluation function f(n) on this state
            path - the path to this node from the start state

            note: if we had variable path costs, we'd need to also keep track of that,
            but in the 8-puzzle len(path) is sufficient to determine path cost to a given node.
        '''
        self._state = state
        self._fcost = fcost
        self._path = path

    def get_state(self):
        return self._state

    def get_fcost(self):
        return self._fcost

    def get_path(self):
        return self._path

    def __lt__(self, other):
        return self.get_fcost() < other.get_fcost()

    def __le__(self, other):
        return self.get_fcost() <= other.get_fcost()

    def __gt__(self, other):
        return self.get_fcost() > other.get_fcost()

    def __ge__(self, other):
        return self.get_fcost() >= other.get_fcost()

    def __eq__(self, other):
        return self._state == other._state and self.get_fcost() == other.get_fcost()

def num_wrong_tiles(state):
    sum = 0
    for i in range(8):
        if get_tile(state, i) != i+1:
            sum+=1
    return sum

def movesaway(tile,i): # i is what tile should be there, tile is what is there
    if i != 8:
        return abs(xylocation(i)[0] - xylocation(tile)[0]) + abs(xylocation(i)[1] - xylocation(tile)[1])
    else:
        return 0

def manhattan_distance(state):
    sum = 0
    for i in range(9):
        tile = get_tile(state, i)
        locationitshouldbein = (tile - 1)%9
        sum += movesaway(i, locationitshouldbein)
    print(sum)
    return sum
    
    
def verify(state, sol):
    print(sol)
    currentState = state
    for i in sol:
        currentState = move_blank(currentState, i[1])
    if currentState == solution():
        print("Correct Solution")


def astar(state, heuristic):
    start = Node(state, 0, [])
    frontier = PriorityQueue()
    frontier.put(start)
    explored = set()
    while not frontier.empty():
        node = frontier.get()
        if node._state == solution():
            return node.get_path()
        else:
            if node._state in explored:
                continue
            explored.add(node._state)
            for c in neighbors(blank_square(node._state)):
                newboardstate = move_blank(node._state, c)
                newcost = len(node.get_path())
                currentblank = blank_square(node._state)
                newblank = blank_square(newboardstate)
                newpath = node.get_path()[:]
                newpath.append(((currentblank,newblank)))
                child = Node(newboardstate, newcost, newpath)
                if child not in frontier.queue or child._state not in explored:
                    frontier.put(child)
    return None

for i in range(100):
    sample = random_state(20)
    #sample = state([8,6,7,2,5,4,3,0,1])  #  Hardest possible board state
    sol = astar(sample, manhattan_distance)
    verify(sample, sol)

# #start = time.time()

# end = time.time()
# print(end - start)
#Random state 100: Manhattan_Distance: 30 -- Num wrong tiles: 16:40 -- Itdeep: Did not finish
#Random state 50: Manhattan_Distance 3.9s -- Num wrong tiles: 47s   -- Itdeep: Did not finish
#Random state 35: Manhattan_Distance 2.05s -- Num wrong tiles: 1:03 -- Itdeep: 6:10
#Random state 20: Manhattan_Distance 1.28 -- Num wrong tiles: 1.86s -- Itdeep: 11 s
"""
We found that the iterative deepening approach slowed down dramatically around depth 16. Manhattan Distance is much
faster than num wrong tiles on 'more random' (more scrambled) boards. Scrambling by randomly moving the board is hard
to test in the cases where it randomly makes an extremely hard board. The hardest boards can take 31 moves to solve, and 
our itdeep function can't solve anything that requires more than 17 moves in any reasonable amount of time. We had to
run our tests of itdeep multiple times until we had one that finished, it got stuck a couple times. 
"""
