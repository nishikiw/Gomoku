from gomoku_cat import State
from gomoku_cat import SearchEngine
from gomoku_cat import evaluate_state
from gomoku_cat import get_winner

## safety test to ensure the game will end.
## a state that have a winner.
def winner_test1():
    action = (7, 7)
    state = State(action, None, 1, 2)
    state.populate_states([(7, 3), (7, 4), (7, 5), (7, 6)], 1)
    state.populate_states([(8, 3), (8, 4), (8, 5), (8, 6)], 2)
    winner = get_winner(state)
    if winner != 1:
        print("failed winner_test1\n")
        return 0
    print("passed winner_test1\n")
    return 1

## a state with no winner.
def winner_test2():
    action = (7, 7)
    state = State(action, None, 1, 2)
    state.populate_states([(7, 3), (7, 4), (7, 5), (6, 6)], 1)
    state.populate_states([(8, 3), (8, 4), (8, 5), (8, 6)], 2)
    winner = get_winner(state)
    if winner != -1:
        print("failed winner_test2\n")
        return 0
    print("passed winner_test2\n")
    return 1

#basic test to test functionality of the ai to recognize different patterns.
## only one move on the board.
def basic_evaluation_test1():
    action = (7, 7)
    state = State(action, None, 1, 2)
    score = evaluate_state(state)
    if score != 0:
        print("failed basic_evaluation_test1\n")
        return 0
    print("passed basic_evaluation_test1\n")
    return 1

## there is a winning move on the board near the action placed
## realize a high score
def basic_evaluation_test2():
    action = (7, 7)
    state = State(action, None, 1, 2)
    state.populate_states([(7, 3), (7, 4), (7, 5), (7, 6)], 1)
    state.populate_states([(8, 3), (8, 4), (8, 5), (8, 6)], 2)
    score = evaluate_state(state)
    if score != 100:
        print("failed basic_evaluation_test2\n")
        return 0
    print("passed basic_evaluation_test2\n")
    return 1

## populated not around action so score is not able to update, this should not
## increase the score since this does not increase the region tracked by the ai
def basic_evaluation_test3():
    action = (5, 5)
    state = State(action, None, 1, 2)
    state.populate_states([(1, 3), (1, 4), (1, 5), (1, 6)], 1)
    state.populate_states([(8, 3), (8, 4), (8, 5), (8, 6), (8, 7)], 2)
    score = evaluate_state(state)
    if score != 0:
        print("failed basic_evaluation_test3\n")
        return 0
    print("passed basic_evaluation_test3\n")
    return 1

## realize there is a connected 4 with no obstacles
def basic_evaluation_test4():
    action = (7, 7)
    state = State(action, None, 1, 2)
    state.populate_states([(7, 4), (7, 5), (7, 6)], 1)
    state.populate_states([(8, 3), (8, 4), (8, 5)], 2)
    score = evaluate_state(state)
    if score != 90:
        print("failed basic_evaluation_test4\n")
        return 0
    print("passed basic_evaluation_test4\n")
    return 1

## realize there is a connected 4 with 1 obstables after placing action
def basic_evaluation_test5():
    action = (7, 7)
    state = State(action, None, 1, 2)
    state.populate_states([(7, 4), (7, 5), (7, 6)], 1)
    state.populate_states([(7, 8), (8, 4), (8, 5)], 2)
    score = evaluate_state(state)
    if score != 60:
        print("failed basic_evaluation_test5\n")
        return 0
    print("passed basic_evaluation_test5\n")
    return 1

## TODO take a look at this test what should the score be ?
def basic_evaluation_test6():
    action = (7, 7)
    state = State(action, None, 1, 2)
    state.populate_states([(7, 5), (7, 6)], 1)
    state.populate_states([(8, 6), (8, 7)], 2)
    score = evaluate_state(state)
    print(score)
    if score != 80:
        print("failed basic_evaluation_test5\n")
        return 0
    print("passed basic_evaluation_test5\n")
    return 1

def main():
    tests_passed = 0;
    total_tests = 7;

    passed = winner_test1()
    tests_passed += passed

    passed = winner_test2()
    tests_passed += passed

    passed = basic_evaluation_test1()
    tests_passed += passed

    passed = basic_evaluation_test2()
    tests_passed += passed

    passed = basic_evaluation_test3()
    tests_passed += passed

    passed = basic_evaluation_test4()
    tests_passed += passed

    passed = basic_evaluation_test5()
    tests_passed += passed

    passed = basic_evaluation_test6()
    tests_passed += passed
    print("You passed %d/%d tests." % (tests_passed,total_tests))

if __name__ =="__main__":
    main()
