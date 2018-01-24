"""
Make sure to fill in the following information before submitting your
assignment. Your grade may be affected if you leave it blank!
For usernames, make sure to use your Whitman usernames (i.e. exleyas).
File name: uninformed.py
Author username(s): ashleygw millersm
Date: 1/22/2018
"""


import puzzle8 as p


def solve_one_away(state):
    """ returns the single move required to solve the puzzle, as a tuple """
    bs = p.blank_square(state)
    moves = p.neighbors(bs)
    for dest in moves:
        if p.move_blank(state, dest) == 42374116:
            return bs, dest

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

