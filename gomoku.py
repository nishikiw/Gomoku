import math
import heapq
import random

size = 15


def initial_board():
    board = {}
    for i in range(1,size+1):
        board[i] = {}
        for j in range(1,size+1):
            board[i][j] = 0
    return board


class State:
    """Define state of gomoku game."""

    def __init__(self, action, pre_state, action_player=2, next_player=1, has_color=True):
        """Initialization for creating a state.
        AI is player 1 (MAX) and human player is player 2 (MIN).
        self.player is the player who is going to make next move.
        """

        self.action = action
        # Initial state
        if pre_state is None:
            self.action_player = action_player
            self.player = next_player
            self.available_moves = set()
            for x in range(1, 16):
                for y in range(1, 16):
                    if (x, y) != action:
                        self.available_moves.add((x, y))
            self.occupied = {}
            if next_player == 1:
                self.occupied[action] = 2
            else:
                self.occupied[action] = 1
            self.top = action[0]
            self.bottom = action[0]
            self.left = action[1]
            self.right = action[1]
            global use_color
            use_color = has_color
        else:
            self.action_player = pre_state.player
            if pre_state.player == 1:
                self.player = 2
            else:
                self.player = 1
            self.available_moves = set(pre_state.available_moves)
            self.available_moves.remove(action)
            self.occupied = dict(pre_state.occupied)
            self.occupied[action] = pre_state.player
            # Set the most top, bottom, left, and right index for the state.
            if action[0] < pre_state.top:
                self.top = action[0]
            else:
                self.top = pre_state.top
            if action[0] > pre_state.bottom:
                self.bottom = action[0]
            else:
                self.bottom = pre_state.bottom
            if action[1] < pre_state.left:
                self.left = action[1]
            else:
                self.left = pre_state.left
            if action[1] > pre_state.right:
                self.right = action[1]
            else:
                self.right = pre_state.right
        self.pre_state = pre_state
        if self.action_player == 1:
            self.value = evaluate_state(self)
        else:
            self.value = -evaluate_state(self)

    def successors(self):
        """Get successor states."""

        if self.player == 1:    # MAX HEAP
            children = []
            for (x, y) in self.available_moves:
                if (y >= self.left - 3) and (y <= self.right + 3) and (x >= self.top - 3) and (x <= self.bottom + 3):
                    child = State((x, y), self)
                    heap_key = -child.value-random.random()
                    heapq.heappush(children, (heap_key, child))
            return children
        else:   # MIN HEAP:
            children = []
            for (x, y) in self.available_moves:
                if (y >= self.left - 3) and (y <= self.right + 3) and (x >= self.top - 3) and (x <= self.bottom + 3):
                    child = State((x, y), self)
                    heap_key = child.value - random.random()
                    heapq.heappush(children, (heap_key, child))
            return children

    def populate_states(self, list, player):
        """Used for testing to generate a state."""
        if self.pre_state is None:
            for action in list:
                self.occupied[action] = player
                self.available_moves.remove(action)
            return 1
        print("you can only populate at the init state")
        return 0

    def __str__(self):
        """Print the board of current state."""
        s = "  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15\n"
        board = initial_board()
        count = 1
        for i in self.occupied:
            board[i[0]][i[1]] = self.occupied[i]
        space = ''
        for i in range(0, 16):
            space += ' '
        start = '---'.join(space)
        s += start+'\n|'
        for row in range(1,16):
            for col in range(1,16):
                if use_color and (row, col) == self.action:
                    s += '\033[91m'
                if board[row][col] == 0:
                    s += '   |'
                elif board[row][col] == 1:
                    s += ' O |'
                else:
                    s += ' X |'
                if use_color and (row, col) == self.action:
                    s += '\033[0m'
                    s += '\033[0m'
            s+=str(count)+'\n'+start+'\n|'
            count += 1

        s = s[:len(s)-1]
        s += "\n*****************************************************************************"
        return s[:len(s)-1]


class SearchEngine:
    """ The search method to determine next step. """

    def next_move(self, cur_state):
        """Given the current state, return the best movement to next state.
        AI is always player 1, so we only need to calculate for MAX.
        """

        alpha, final_state, min_level, action_took = self.alpha_beta(cur_state, 1, 0, -math.inf, math.inf, math.inf)
        #print("-----------------------------------------")
        #print("value = "+str(alpha)+", min_level = "+str(min_level))
        #print("previous: top="+str(cur_state.top)+", bottom="+str(cur_state.bottom)+", left="+str(cur_state.left)+", right="+str(cur_state.right))
        #print(final_state.pre_state)
        return action_took

    def alpha_beta(self, cur_state, limit, cur_level, alpha, beta, min_level):
        """Alpha-beta pruning with limited depth. Leaves are evaluated by evaluation function."""

        # Evaluate current state.
        if cur_level == limit or get_action_score(cur_state.action[0], cur_state.action[1], cur_state.action_player, cur_state.occupied)==100:
            return cur_state.value, cur_state, cur_level, None
        else:
            child_list = cur_state.successors()
            final_state = None
            action_took = None
            if cur_state.player == 1:  # MAX player
                for i in range(len(child_list)):
                    c = heapq.heappop(child_list)
                    (c_alpha, c_state, c_level, action) = self.alpha_beta(c[1], limit, cur_level + 1, alpha, beta, min_level)
                    # print("HERE: "+str(c_alpha)+" "+str(c_level))
                    if (c_alpha > alpha) or (c_alpha == alpha and c_level < min_level):
                        alpha = c_alpha
                        final_state = c_state
                        action_took = c[1].action
                        min_level = c_level
                    if beta <= alpha:
                        break
                return alpha, final_state, min_level, action_took
            else:  # MIN player
                for i in range(len(child_list)):
                    c = heapq.heappop(child_list)
                    (c_beta, c_state, c_level, action) = self.alpha_beta(c[1], limit, cur_level + 1, alpha, beta, min_level)
                    # print("c_beta = " + str(c_beta) + ", beta = " + str(beta))
                    if (c_beta < beta) or (c_beta == beta and c_level < min_level):
                        beta = c_beta
                        final_state = c_state
                        action_took = c[1].action
                        min_level = c_level
                    if beta <= alpha:
                        break
                return beta, final_state, min_level, action_took


def get_winner(state):
    """If there is a winner for state, return the winner. Else if it's terminal state and no player won,
    return 0. Else return -1."""
    state_val = get_action_score(state.action[0], state.action[1], state.action_player, state.occupied)
    if state_val == 100:
        return state.action_player
    elif len(state.available_moves) == 0:
        return 0
    else:
        return -1


def evaluate_state(state):
    """Input a state, return the value of the state."""

    my_score = get_action_score(state.action[0], state.action[1], state.action_player, state.occupied)
    other_score = get_action_score(state.action[0], state.action[1], state.player, state.occupied)
    
    return max(my_score, other_score)


def get_action_score(x, y, player, occupied):
    """Input a state, return the value of the state."""

    vertical_num = 1
    horizontal_num = 1
    diagonal_num = 1
    antidiagonal_num = 1

    dictionary = {}

    # Calculate the number of pieces in a roll on a vertical line, and how many sides are blocked.
    vertical_blocked_1 = 0
    vertical_blocked_2 = 0
    for i in range(1, min(5, x)):
        if (x - i, y) in occupied:
            if occupied[(x - i, y)] == player:
                vertical_num += 1
                if x - i ==1:
                    vertical_blocked_1 =1
            else:
                vertical_blocked_1 = 1
                break
        else:
            break
    if x == 1:
        vertical_blocked_1 = 1    

    for i in range(1, min(5, size - x + 1)):
        if (x + i, y) in occupied:
            
            if occupied[(x + i, y)] == player:
                vertical_num += 1
                if x + i==15:
                    vertical_blocked_2 = 1 
            else:
                vertical_blocked_2 = 1
                break
        else:
            break
    if x == 15:
        vertical_blocked_2 = 1    

    if (vertical_num, vertical_blocked_1 + vertical_blocked_2) in dictionary:
        dictionary[(vertical_num, vertical_blocked_1 + vertical_blocked_2)] += 1
    else:
        dictionary[(vertical_num, vertical_blocked_1 + vertical_blocked_2)] = 1

    # Calculate the number of pieces in a roll on a horizontal line, and how many sides are blocked.
    horizontal_blocked_1 = 0
    horizontal_blocked_2 = 0
    for i in range(1, min(5, y)):
        if (x, y - i) in occupied:
            if occupied[(x, y - i)] == player:
                horizontal_num += 1
                if y - i == 1:
                    horizontal_blocked_1 = 1
            else:
                horizontal_blocked_1 = 1
                break
        else:
            break
    if y == 1:
        horizontal_blocked_1 = 1    
    for i in range(1, min(5, size - y + 1)):
        if (x, y + i) in occupied:
            if occupied[(x, y + i)] == player:
                horizontal_num += 1
                if y + i == 15:
                    horizontal_blocked_2 = 1
            else:
                horizontal_blocked_2 = 1
                break
        else:
            break
    if y == 15:
        horizontal_blocked_1 = 1

    if (horizontal_num, horizontal_blocked_1 + horizontal_blocked_2) in dictionary:
        dictionary[(horizontal_num, horizontal_blocked_1 + horizontal_blocked_2)] += 1
    else:
        dictionary[(horizontal_num, horizontal_blocked_1 + horizontal_blocked_2)] = 1

    # Calculate the number of pieces in a roll through the diagonal, and how many sides are blocked.
    diagonal_blocked_1 = 0
    diagonal_blocked_2 = 0
    for i in range(1, min(5, x, y)):
        if (x - i, y - i) in occupied:
            if occupied[(x - i, y - i)] == player:
                diagonal_num += 1
                if x - i==1 or y-i==1:
                    diagonal_blocked_1 = 1
            else:
                diagonal_blocked_1 = 1
                break
        else:
            break
    if x == 1 or y == 1:
        diagonal_blocked_1 = 1

    
    for i in range(1, min(5, size - x + 1, size - y + 1)):
        if (x + i, y + i) in occupied:
            if occupied[(x + i, y + i)] == player:
                diagonal_num += 1
                if x + i == 15 or y + i==15:
                    diagonal_blocked_2 = 1
            else:
                diagonal_blocked_2 = 1
                break
        else:
            break
    if x == 15 or y < 15:
        diagonal_blocked_2 = 1    

    if (diagonal_num, diagonal_blocked_1 + diagonal_blocked_2) in dictionary:
        dictionary[(diagonal_num, diagonal_blocked_1 + diagonal_blocked_2)] += 1
    else:
        dictionary[(diagonal_num, diagonal_blocked_1 + diagonal_blocked_2)] = 1

    # Calculate the number of pieces in a roll through the antidiagonal, and how many sides are blocked.
    antidiagonal_blocked_1 = 0
    antidiagonal_blocked_2 = 0
    for i in range(1, min(5, size - x + 1, y)):
        if (x + i, y - i) in occupied:
            if occupied[(x + i, y - i)] == player:
                antidiagonal_num += 1
                if x + i==1 or y - i==1:
                    antidiagonal_blocked_1 = 1
            else:
                antidiagonal_blocked_1 = 1
                break
        else:
            break
    if x == 1 or y == 1:
        antidiagonal_blocked_1 = 1    

    if x < 5 or size - y < 4:
        antidiagonal_blocked_2 = 1
    for i in range(1, min(5, x, size - y + 1)):
        if (x - i, y + i) in occupied:
            if occupied[(x - i, y + i)] == player:
                antidiagonal_num += 1
                if x - i==15 or y + i==15:
                    antidiagonal_blocked_2 = 1
            else:
                antidiagonal_blocked_2 = 1
                break
        else:
            break
    if x == 15 or y == 15:
        antidiagonal_blocked_2 = 1    

    if (antidiagonal_num, antidiagonal_blocked_1 + antidiagonal_blocked_2) in dictionary:
        dictionary[(antidiagonal_num, antidiagonal_blocked_1 + antidiagonal_blocked_2)] += 1
    else:
        dictionary[(antidiagonal_num, antidiagonal_blocked_1 + antidiagonal_blocked_2)] = 1

    # Return the score
    if ((5, 0) in dictionary) or ((5, 1) in dictionary) or ((5, 2) in dictionary):
        return 100
    elif ((4, 0) in dictionary) or ((4, 1) in dictionary and dictionary[(4, 1)] > 1) or (
                    (4, 1) in dictionary and (3, 0) in dictionary):
        return 90
    elif (4, 1) in dictionary:
        return 80
    elif ((3, 0) in dictionary) and (dictionary[(3, 0)] > 1):
        return 70
    elif ((3, 0) in dictionary) and ((3, 1) in dictionary):
        return 60
    elif (3, 0) in dictionary:
        return 50
    elif ((2, 0) in dictionary) and (dictionary[(2, 0)] > 1):
        return 40
    elif (3, 1) in dictionary:
        return 30
    elif (2, 0) in dictionary:
        return 20
    elif (2, 1) in dictionary:
        return 10
    else:
        return 0