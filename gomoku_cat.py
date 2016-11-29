size = 15

class State:
    """Define state of gomoku game."""

    def __init__(self, action, pre_state):
        """Initialization for creating a state."""
        if pre_state.player == 1:
            self.player = 2
        else:
            self.player = 1
        self.available_move = pre_state.available_move.copy()
        self.available_move.remove(action)
        self.occupied = pre_state.occupied.copy()
        self.occupied[action] = self.player


    def successors(self):
        '''Get succssor states.'''

        #IMPLEMENT
        return

    def print_board(self):
        '''Print the board of current state.'''

        print(self.board)


class SearchEngine:
    """ The search method to determine next step. """

    def nextMove(cur_state):
        """Given the current state, return the best movement to next state."""

    def ids(cur_state):

    def dls(cur_state, limit):
        """Depth limited search with limit limit."""

    def evaluate_state(state):
        """Input a state, return the value of the state."""

        x = state.action[0]
        y = state.action[1]
        player = state.player
        occupied = state.occupied

        vertical_num = 0
        horizontal_num = 0
        diagonal_num = 0
        antidiagonal_num = 0

        dict = {}

        # Calculate the number of pieces in a roll on a vertical line, and how many sides are blocked.
        if y < 5:
            vertical_blocked_1 = 1
        for i in range(1, min(5, x)):
            if (x, y-i) in occupied:
                if occupied[(x, y-i)] == player:
                    vertical_num += 1
                else:
                    vertical_blocked_1 = 1
                    break
            else:
                break

        if size - y < 4:
            vertical_blocked_2 = 1
        for i in range(1, min(5, size-y+1)):
            if (x, y+i) in occupied:
                if occupied[(x, y+i)] == player:
                    vertical_num += 1
                else:
                    vertical_blocked_2 = 1
                    break
            else:
                break

        if (vertical_num, vertical_blocked_1+vertical_blocked_2) in dict:
            dict[(vertical_num, vertical_blocked_1+vertical_blocked_2)] += 1
        else:
            dict[(vertical_num, vertical_blocked_1 + vertical_blocked_2)] = 1

        # Calculate the number of pieces in a roll on a horizontal line, and how many sides are blocked.
        if x < 5:
            horizontal_blocked_1 = 1
        for i in range(1, min(5, x)):
            if (x-i, y) in occupied:
                if occupied[(x-i, y)] == player:
                    horizontal_num += 1
                else:
                    horizontal_blocked_1 = 1
                    break
            else:
                break

        if size - x < 4:
            horizontal_blocked_2 = 1
        for i in range(1, min(5, size-x+1)):
            if (x+i, y) in occupied:
                if occupied[(x+i, y)] == player:
                    horizontal_num += 1
                else:
                    horizontal_blocked_2 = 1
                    break
            else:
                break

        if (horizontal_num, horizontal_blocked_1+horizontal_blocked_2) in dict:
            dict[(horizontal_num, horizontal_blocked_1+horizontal_blocked_2)] += 1
        else:
            dict[(horizontal_num, horizontal_blocked_1+horizontal_blocked_2)] = 1

        # Calculate the number of pieces in a roll through the diagonal, and how many sides are blocked.
        if x < 5 or y < 5:
            diagonal_blocked_1 = 1
        for i in range(1, min(5, x, y)):
            if (x-i, y-i) in occupied:
                if occupied[(x-i, y-i)] == player:
                    diagonal_num += 1
                else:
                    diagonal_blocked_1 = 1
                    break
            else:
                break

        if size-x < 4 or size-y < 4:
            diagonal_blocked_2 = 1
        for i in range(1, min(5, size-x+1, size-y+1)):
            if (x+i, y+i) in occupied:
                if occupied[(x+i, y+i)] == player:
                    diagonal_num += 1
                else:
                    diagonal_blocked_2 = 1
                    break
            else:
                break

        if (diagonal_num, diagonal_blocked_1+diagonal_blocked_2) in dict:
            dict[(diagonal_num, diagonal_blocked_1+diagonal_blocked_2)] += 1
        else:
            dict[(diagonal_num, diagonal_blocked_1+diagonal_blocked_2)] = 1

        # Calculate the number of pieces in a roll through the antidiagonal, and how many sides are blocked.
        if size-x < 4 or y < 5:
            antidiagonal_blocked_1 = 1
        for i in range(1, min(5, size-x+1, y)):
            if (x+i, y-i) in occupied:
                if occupied[(x+i, y-i)] == player:
                    antidiagonal_num += 1
                else:
                    antidiagonal_blocked_1 = 1
                    break
            else:
                break

        if x < 5 or size-y < 4:
            antidiagonal_blocked_2 = 1
        for i in range(1, min(5, x, size-y+1)):
            if (x-i, y+i) in occupied:
                if occupied[(x-i, y+i)] == player:
                    antidiagonal_num += 1
                else:
                    antidiagonal_blocked_2 = 1
                    break
            else:
                break

        if (antidiagonal_num, antidiagonal_blocked_1+antidiagonal_blocked_2) in dict:
            dict[(antidiagonal_num, antidiagonal_blocked_1+antidiagonal_blocked_2)] += 1
        else:
            dict[(antidiagonal_num, antidiagonal_blocked_1+antidiagonal_blocked_2)] = 1

        # Return the score
        if ((5, 0) in dict) or ((5, 1) in dict) or ((5, 2) in dict):
            return 100
        elif ((4, 0) in dict) or ((4, 1) in dict and dict[(4, 1) > 1]) or ((4, 1) in dict and (3, 0) in dict):
            return 90
        elif (3, 0) in dict and dict[(3, 0)] > 1:
            return 80
        elif (3, 0) in dict and (3, 1) in dict:
            return 70
        elif (4, 1) in dict:
            return 60
        elif (3, 0) in dict:
            return 50
        elif (2, 0) in dict and dict[(2, 0)] > 1:
            return 40
        elif (3, 1) in dict:
            return 30
        elif (2, 0) in dict:
            return 20
        elif (2, 1) in dict:
            return 10
        else:
            return 0