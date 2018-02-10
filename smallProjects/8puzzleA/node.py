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
        return self.get_state() == other.get_state and self.get_fcost() == other.get_fcost()