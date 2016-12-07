from gomoku_cat import State
from gomoku_cat import SearchEngine


def main():
    print("Welcome to Gomoku!")
    choice = input("Would you like to go first? (yes/no): ")
    while choice.lower() != "yes" and choice.lower() != "no":
        choice = input("Wrong input. Please write 'yes' or 'no': ")
    # Set up initial state.
    if choice.lower() == "yes":
        action_str = input("Please enter a location (x and y separated by space in range [1, 15]. example: 1 3): ")
        action_lst = action_str.split()
        action = (int(action_lst[0]), int(action_lst[1]))
        state = State(action, None, 1)
    else:
        action = (8, 8)
        state = State(action, None, 2)

    state.print_board()
    search_engine = SearchEngine()
    while search_engine.get_winner(state) == -1:
        if state.player == 1:   # AI need to make next move
            action = search_engine.next_move(state)
            state = State(action, state)
        else:   # Player need to make next move
            action_str = input("Please enter your move: ")
            action_lst = action_str.split()
            action = (int(action_lst[0]), int(action_lst[1]))
            state = State(action, state)
        print("score: "+str(search_engine.evaluate_state(state)))
        state.print_board()
    winner = search_engine.get_winner(state)
    if winner == 1:
        print("Game end. Please try again.")
    elif winner == 2:
        print("Congrats! You win!")
    else:
        print("Game end with a tie.")

if __name__ == "__main__":
    # execute only if run as a script
    main()