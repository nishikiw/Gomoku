import math

size = 15


class State:
    """Define state of gomoku game."""

    def __init__(self, action, pre_state):
        """Initialization for creating a state."""

        self.action = action
        if pre_state.player == 1:
            self.player = 2
        else:
            self.player = 1
        self.available_moves = pre_state.available_move.copy()
        self.available_moves.remove(action)
        self.occupied = pre_state.occupied.copy()
        self.occupied[action] = self.player
        # Set the most top, bottom, left, and right index for the state.
        if action[1] < pre_state.top:
            self.top = action[0]
        else:
            self.top - pre_state.top
        if action[1] > pre_state.bottom:
            self.bottom = action[0]
        else:
            self.bottom = pre_state.bottom
        if action[0] < pre_state.left:
            self.left = action[1]
        else:
            self.left = pre_state.left
        if action[0] > pre_state.right:
            self.right = action[1]
        else:
            self.right = pre_state.right

    def next_player(self):
        """Return the player in successor state. Player 1 is MAX and Player 2 is MIN."""
        if self.player == 1:
            return 2
        else:
            return 1

    def successors(self):
        """Get successor states."""

        children = []
        for (x, y) in self.available_moves:
            if (x >= self.left) and (x <= self.right) and (y >= self.top) and (y <= self.bottom):
                child = State((x, y), self)
                children.append(child)
        return children

    def print_board(self):
        """Print the board of current state."""

        print(self.board)


class SearchEngine:
    """ The search method to determine next step. """

    def nextMove(self, cur_state):
        """Given the current state, return the best movement to next state."""

        children = cur_state.successors()
        next_move = None
        if cur_state.player == 1:   # MAX player
            max_val = -math.inf
            for c in children:
                c_val = self.alpha_beta(c, 3, 1, -math.inf, math.inf)
                if c_val > max_val:
                    max_val = c_val
                    next_move = c.action
        else:   # MIN player
            min_val = math.inf
            for c in children:
                c_val = self.alpha_beta(c, 3, 1, -math.inf, math.inf)
                if c_val < min_val:
                    min_val = c_val
                    next_move = c.action
        return next_move


    def alpha_beta(self, cur_state, limit, cur_level, alpha, beta):
        """Alpha-beta pruning with limited depth. Leaves are evaluated by evaluation function."""

        if cur_level == limit:
            if cur_state.player == 1:   # MAX player
                return cur_state.evaluate_state(cur_state)
            else:   # MIN player
                return -cur_state.evaluate_state(cur_state)
        else:
            child_list = cur_state.successors()
            if cur_state.player == 1:   # MAX player
                for c in child_list:
                    alpha = max(alpha, self.alpha_beta(c, limit, cur_level+1, alpha, beta))
                    if beta <= alpha:
                        break
                return alpha
            else:   # MIN player
                for c in child_list:
                    beta = min(beta, self.alpha_beta(c, limit, cur_level+1, alpha, beta))
                    if beta <= alpha:
                        break
                return beta

    def evaluate_state(self, state):
        """Input a state, return the value of the state."""

        x = state.action[0]
        y = state.action[1]
        player = state.player
        occupied = state.occupied

        vertical_num = 1
        horizontal_num = 1
        diagonal_num = 1
        antidiagonal_num = 1

        dictionary = {}

        # Calculate the number of pieces in a roll on a vertical line, and how many sides are blocked.
        if y < 5:
            vertical_blocked_1 = 1
        for i in range(1, min(5, x)):
            if (x, y - i) in occupied:
                if occupied[(x, y - i)] == player:
                    vertical_num += 1
                else:
                    vertical_blocked_1 = 1
                    break
            else:
                break

        if size - y < 4:
            vertical_blocked_2 = 1
        for i in range(1, min(5, size - y + 1)):
            if (x, y + i) in occupied:
                if occupied[(x, y + i)] == player:
                    vertical_num += 1
                else:
                    vertical_blocked_2 = 1
                    break
            else:
                break

        if (vertical_num, vertical_blocked_1 + vertical_blocked_2) in dictionary:
            dictionary[(vertical_num, vertical_blocked_1 + vertical_blocked_2)] += 1
        else:
            dictionary[(vertical_num, vertical_blocked_1 + vertical_blocked_2)] = 1

        # Calculate the number of pieces in a roll on a horizontal line, and how many sides are blocked.
        if x < 5:
            horizontal_blocked_1 = 1
        for i in range(1, min(5, x)):
            if (x - i, y) in occupied:
                if occupied[(x - i, y)] == player:
                    horizontal_num += 1
                else:
                    horizontal_blocked_1 = 1
                    break
            else:
                break

        if size - x < 4:
            horizontal_blocked_2 = 1
        for i in range(1, min(5, size - x + 1)):
            if (x + i, y) in occupied:
                if occupied[(x + i, y)] == player:
                    horizontal_num += 1
                else:
                    horizontal_blocked_2 = 1
                    break
            else:
                break

        if (horizontal_num, horizontal_blocked_1 + horizontal_blocked_2) in dictionary:
            dictionary[(horizontal_num, horizontal_blocked_1 + horizontal_blocked_2)] += 1
        else:
            dictionary[(horizontal_num, horizontal_blocked_1 + horizontal_blocked_2)] = 1

        # Calculate the number of pieces in a roll through the diagonal, and how many sides are blocked.
        if x < 5 or y < 5:
            diagonal_blocked_1 = 1
        for i in range(1, min(5, x, y)):
            if (x - i, y - i) in occupied:
                if occupied[(x - i, y - i)] == player:
                    diagonal_num += 1
                else:
                    diagonal_blocked_1 = 1
                    break
            else:
                break

        if size - x < 4 or size - y < 4:
            diagonal_blocked_2 = 1
        for i in range(1, min(5, size - x + 1, size - y + 1)):
            if (x + i, y + i) in occupied:
                if occupied[(x + i, y + i)] == player:
                    diagonal_num += 1
                else:
                    diagonal_blocked_2 = 1
                    break
            else:
                break

        if (diagonal_num, diagonal_blocked_1 + diagonal_blocked_2) in dictionary:
            dictionary[(diagonal_num, diagonal_blocked_1 + diagonal_blocked_2)] += 1
        else:
            dictionary[(diagonal_num, diagonal_blocked_1 + diagonal_blocked_2)] = 1

        # Calculate the number of pieces in a roll through the antidiagonal, and how many sides are blocked.
        if size - x < 4 or y < 5:
            antidiagonal_blocked_1 = 1
        for i in range(1, min(5, size - x + 1, y)):
            if (x + i, y - i) in occupied:
                if occupied[(x + i, y - i)] == player:
                    antidiagonal_num += 1
                else:
                    antidiagonal_blocked_1 = 1
                    break
            else:
                break

        if x < 5 or size - y < 4:
            antidiagonal_blocked_2 = 1
        for i in range(1, min(5, x, size - y + 1)):
            if (x - i, y + i) in occupied:
                if occupied[(x - i, y + i)] == player:
                    antidiagonal_num += 1
                else:
                    antidiagonal_blocked_2 = 1
                    break
            else:
                break

        if (antidiagonal_num, antidiagonal_blocked_1 + antidiagonal_blocked_2) in dictionary:
            dictionary[(antidiagonal_num, antidiagonal_blocked_1 + antidiagonal_blocked_2)] += 1
        else:
            dictionary[(antidiagonal_num, antidiagonal_blocked_1 + antidiagonal_blocked_2)] = 1

        # Return the score
        if ((5, 0) in dictionary) or ((5, 1) in dictionary) or ((5, 2) in dictionary):
            return 100
        elif ((4, 0) in dictionary) or ((4, 1) in dictionary and dictionary[(4, 1) > 1]) or ((4, 1) in dictionary and (3, 0) in dictionary):
            return 90
        elif (3, 0) in dictionary and dict[(3, 0)] > 1:
            return 80
        elif (3, 0) in dictionary and (3, 1) in dictionary:
            return 70
        elif (4, 1) in dictionary:
            return 60
        elif (3, 0) in dictionary:
            return 50
        elif (2, 0) in dictionary and dictionary[(2, 0)] > 1:
            return 40
        elif (3, 1) in dictionary:
            return 30
        elif (2, 0) in dictionary:
            return 20
        elif (2, 1) in dictionary:
            return 10
        else:
            return 0
