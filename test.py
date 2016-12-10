from gomoku import State
from gomoku import SearchEngine
from gomoku import evaluate_state
from gomoku import get_winner


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


# basic test to test functionality of the ai to recognize different patterns.
## only one move on the board.
## 1 live
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
## 5 live
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
## 4 live
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
## 4 live 1 die
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
## 3 live
def basic_evaluation_test6():
    action = (7, 7)
    state = State(action, None, 1, 2)
    state.populate_states([(7, 5), (7, 6)], 1)
    state.populate_states([(3, 6), (3, 7)], 2)
    score = evaluate_state(state)
    if score != 50:
        print("failed basic_evaluation_test6\n")
        return 0
    print("passed basic_evaluation_test6\n")
    return 1


## TODO take a look at this test what should the score be ?
## 3 live 1 die
def basic_evaluation_test7():
    action = (7, 7)
    state = State(action, None, 1, 2)
    state.populate_states([(7, 5), (7, 6)], 1)
    state.populate_states([(8, 6), (8, 7), (7, 8)], 2)
    score = evaluate_state(state)
    if score != 40:
        print("failed basic_evaluation_test7\n")
        return 0
    print("passed basic_evaluation_test7\n")
    return 1


## 2 live 1 die
def basic_evaluation_test8():
    action = (7, 7)
    state = State(action, None, 1, 2)
    state.populate_states([(7, 6)], 1)
    state.populate_states([(7, 8)], 2)
    score = evaluate_state(state)
    if score != 10:
        print("failed basic_evaluation_test8\n")
        return 0
    print("passed basic_evaluation_test8\n")
    return 1


## 2 live
def basic_evaluation_test9():
    action = (7, 7)
    state = State(action, None, 1, 2)
    state.populate_states([(7, 6)], 1)
    state.populate_states([(5, 5)], 2)
    score = evaluate_state(state)
    if score != 20:
        print("failed basic_evaluation_test9\n")
        return 0
    print("passed basic_evaluation_test9\n")
    return 1


def basic_evaluation_test10():
    action = (7, 7)
    state = State(action, None, 1, 2)
    state.populate_states([(7, 5), (7, 6), (8, 7), (9, 7)], 1)
    state.populate_states([(7, 8), (5, 6), (5, 7), (5, 8)], 2)
    score = evaluate_state(state)
    if score != 70:
        print("failed basic_evaluation_test10\n")
        return 0
    print("passed basic_evaluation_test10\n")
    return 1


## take the winning move
def basic_next_step_test1():
    action = (7, 6)
    state = State(action, None, 2, 1)
    search_engine = SearchEngine()
    state.populate_states([(7, 3), (7, 4), (7, 5)], 2)
    state.populate_states([(8, 3), (8, 4), (8, 5), (8, 6)], 1)
    action = search_engine.next_move(state)
    result = [(8, 2), (8, 7)]

    if action not in result:
        print("failed basic_next_step_test1\n")
        return 0
    print("passed basic_next_step_test1\n")
    return 1


## prevent the other player from making a game winning move
def basic_next_step_test2():
    action = (7, 5)
    state = State(action, None, 2, 1)
    search_engine = SearchEngine()
    state.populate_states([(7, 3), (7, 4)], 2)
    state.populate_states([(8, 3), (8, 4)], 1)
    action = search_engine.next_move(state)
    result = [(7, 2), (7, 6)]

    if action not in result:
        print("failed basic_next_step_test2\n")
        return 0
    print("passed basic_next_step_test2\n")
    return 1


def main():
    tests_passed = 0;
    total_tests = 14;

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

    passed = basic_evaluation_test7()
    tests_passed += passed

    passed = basic_evaluation_test8()
    tests_passed += passed

    passed = basic_evaluation_test9()
    tests_passed += passed

    passed = basic_evaluation_test10()
    tests_passed += passed

    passed = basic_next_step_test1()
    tests_passed += passed

    passed = basic_next_step_test2()
    tests_passed += passed
    print("You passed %d/%d tests." % (tests_passed, total_tests))


if __name__ == "__main__":
    main()
