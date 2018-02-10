"""
Make sure to fill in the following information before submitting your
assignment. Your grade may be affected if you leave it blank!
For usernames, make sure to use your Whitman usernames (i.e. exleyas).
File name: uninformed.py
Author username(s): ashleygw millersm
Date: 1/22/2018
"""

import puzzle8 as p
solved = False
toggle = False
from informed import astar, manhattan_distance, num_wrong_tiles

class Node:
    def __init__(self, board, parent):
        self.board = board
        self.next = None
        self.bs = p.blank_square(board)
        moves = p.neighbors(self.bs)
        self.children = moves
        self.parent = parent

    def getboard(self):
        return self.board

    def getChildren(self):
        return self.children

    def getParent(self):
        return self.parent


def depthlimited(state, limit):
    global solved, toggle
    startnode = Node(state, None)
    ret = []
    solved = False
    toggle = False
    def dlhelper(lim, node):
        global solved, toggle

        if node.board == p.solution():
            solved = True

        if lim == 0 and not solved:
            return

        for i in node.children:
            if not solved:
                x = Node(p.move_blank(node.board, i), node)
                dlhelper(lim-1, x)
        if solved:
            if node.parent:
                x = node.bs
                y = node.parent.bs
                if toggle:
                    ret.append((x, y))
                else:
                    ret.append((y, x))
        return

    dlhelper(limit, startnode)
    if len(ret) > 0:
        return ret[::-1]
    else:
        return None


def itdeep(state):
    if state == p.solution():
        return []
    exitCondition = False
    iter = 0
    ret = []
    while not exitCondition:
        #print("Depth, ", iter)
        ret = depthlimited(state, iter)
        if not ret:
            iter += 1
        else:
            exitCondition = True
    return ret


def verify(state, solution):
    print(solution)
    currentState = state
    for i in solution:
        currentState = p.move_blank(currentState, i[1])
    if currentState == p.solution():
        print("Correct Solution")

for i in range(100):
    print(i)
    sample = p.random_state(35)
    #sample = p.state([1,2,0,5,4,6,7,8,3])
    #print(p.display(sample))
    sol = itdeep(sample)
    #sol = astar(sample, manhattan_distance)
    verify(sample, sol)











# def solve_one_away(state):
#     """ returns the single move required to solve the puzzle, as a tuple """
#     bs = p.blank_square(state)
#     moves = p.neighbors(bs)
#     for dest in moves:
#         if p.move_blank(state, dest) == 42374116:
#             return bs, dest

    # if state == 300300148:
    #     return 5, 8
    # if state == 348484132:
    #     return 7, 8
    # else:
    #     print("Not solvable in one move")
    #     return state


# sample = p.state([1,2,3,4,5,0,7,8,6])
# print(p.state([1,2,3,4,5,0,7,8,6]))
# print(solve_one_away(sample))

