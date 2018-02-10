'''
Some test cases for the heuristics

'''

import informed
import puzzle8

def test_num_wrong_tiles():
    ''' test cases for the number of wrong tiles heuristic'''
    goal = puzzle8.solution()
    assert informed.num_wrong_tiles(goal) == 0

    teststate1 = puzzle8.state([1,2,3,4,5,6,7,0,8])
    assert informed.num_wrong_tiles(teststate1) == 1

    teststate2 = puzzle8.state([0,1,2,3,4,5,6,7,8])
    assert informed.num_wrong_tiles(teststate2) == 8

    teststate3 = puzzle8.state([0,1,2,4,6,3,7,5,8])
    assert informed.num_wrong_tiles(teststate3) == 6

    print("passed num_wrong_tiles tests")

def test_manhattan_distance():
    '''test cases for manhattan distance heuristic'''

    goal = puzzle8.solution()
    assert informed.manhattan_distance(goal) == 0

    teststate1 = puzzle8.state([1,2,3,4,5,6,7,0,8])
    assert informed.manhattan_distance(teststate1) == 1

    teststate2 = puzzle8.state([0,1,2,3,4,5,6,7,8])
    assert informed.manhattan_distance(teststate2) == 12

    teststate3 = puzzle8.state([0,1,2,4,6,3,7,5,8])
    assert informed.manhattan_distance(teststate3) == 6

    print("passed manhattan_distance tests")

def main():
    test_num_wrong_tiles()
    test_manhattan_distance()

if __name__ == '__main__':
    main()
