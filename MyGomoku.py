from Game import *
def initial_board(size):
    board = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(0)
        board.append(row)
    return board

def max_heapify(A, i):
    '''
    This function can maintain heap property of A
    '''
    l = 2*i+1
    r = 2*i+2
    if l < len(A) and A[l].value > A[i].value:
        largest = l
    else:
        largest = i
    if r < len(A) and A[r].value > A[largest].value:
        largest = r
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        max_heapify(A, largest)

def build_max_heap(A):
    '''
    Build a max heap for A
    '''
    i = (len(A)-1)//2
    while i != -1:
        max_heapify(A,i)
        i -= 1

def min_heapify(A, i):
    '''
    This function can maintain heap property of A
    '''
    l = 2*i+1
    r = 2*i+2
    if l < len(A) and A[l].value < A[i].value:
        small = l
    else:
        small = i
    if r < len(A) and A[r].value < A[small].value:
        small = r
    if small != i:
        A[i], A[small] = A[small], A[i]
        min_heapify(A, small)

def build_min_heap(A):
    '''
    Build a min heap for A
    '''
    i = (len(A)-1)//2
    while i != -1:
        min_heapify(A,i)
        i -= 1

class GomokuState(Game):
    '''
    Define the state of Gomoku.
    '''
    
    def __init__(self, action, parent, board_size, player, available, unavailable):
        '''
        Create a new Gomoku.
        a) self.action === the name of the action used to generate
        this state from parent. If it is the initial state a good
        convention is to supply the action name "START". Otherwise,
        action is the location of the last movement.
        b) parent the state from which this state was generated
        c) board_size is the length of the board.
        d) player repesents who should place a go piece in this state.
        1 represents Max player, and -1 represents Min player
        e) available is a set of locations which players can put a go in the state
        f) unavailable is a dictionary of locations which players placed go.
        '''
        self.action = action
        self.parent = parent
        self.board_size = board_size
        self.player = player
        self.available = available
        self.unavailable = unavailable
        self.utility = 0
        self.value = 0
    
    def terminal_test(self, state):
        '''
        Return the terminal if it is won or there are no empty location
        '''
        return state.utility != 0 or len(state.available) == 0
    
        
    def __str__(self):
        s = ""
        board = initial_board(self.board_size)
        for i in self.unavailable:
            board[i[0]][i[1]] = self.unavailable[i]
        space = ''
        for i in range(0, self.board_size+1):
            space += ' '
        start = '---'.join(space)
        s += start+'\n|'
        for row in board:
            for e in row:
                if e == 0:
                    s += '   |'
                elif e == 1:
                    s += ' O |'
                else:
                    s += ' X |'
            s+='\n'+start+'\n|'
            
        return s[:len(s)-1]
    def successors(self):
        '''
        Generates all the actions that can be performed from this state, and the
        states those actions will create
        '''
        successors = []
        # this means the game just start
        if self.action == 'START':
            player = 1
        else:
            player = self.player*(-1)
        for location in self.available:
            new_available = set(self.available)
            new_available.remove(location)
            new_unavailable = dict(self.unavailable)
            new_unavailable[location] = player
            new_state = GomokuState(location, self, self.board_size, player, new_available,new_unavailable)
            successors.append(new_state)
        if player == 1:
            build_max_heap(successors)
        elif player == -1:
            build_min_heap(successors)
        return successors
    
    def evaluation(self):
        '''
        Given a GomokuState, return a value for this state. 
        Detail: we will consider the value for Max player(player 1) is positive
        while the value for Min player(player 2) is negetive. So the total value
        for given state is sum of this two values. Moreover, we will see that if
        the state value is positive, then Max player has more advantage, if it
        is negetive, then Min player has more advantage. 0 means both players
        have equal advantage.
        To evaluate state value, we will consider parent's value. Each action
        will only increase player's advantage, and decrease opponent's value, so
        we check 8 diagonals
        '''
        if location == 'START':
            return 0
        location = self.action
        score = self.parent.value
        #(me, empty, opponent)
        relation_tuple = (1,0,0)
        #first let's check horizontal line
        for i in range(-1,-5,-1):
            # Here we find a broken row, but the place is not occupied yet
            if (location[0]+i,location[1]) not in self.unavailable:
                relation_tuple[1] += 1
            elif self.unavailable[(location[0]+i,location[1])] == self.player:
                relation_tuple[0] += 1
                #find a 5 in row, but think about the value
                if relation_tuple[0] == 5:
                    return 100 * self.player
            # Here we find a opponent's go, damned
            else:
                relation_tuple[2] += 1
        for j in range(1, 5):
            # Here we find a broken row, but the place is not occupied yet
            if (location[0]+i,location[1]) not in self.unavailable:
                relation_tuple[1] += 1
            elif self.unavailable[(location[0]+i,location[1])] == self.player:
                relation_tuple[0] += 1
                #find a 5 in row, but think about the value
                if relation_tuple[0] == 5:
                    return 100 * self.player
            # Here we find a opponent's go, damned
            else:
                relation_tuple[2] += 1            
        return score
    



if __name__ == '__main__':
    #15*15
    l = list()
    for i in range(19):
        for j in range(19):
            l.append((i,j))
    a = GomokuState('Start', None, 15, 0, set(l),{(1,1):1,(3,4):-1})
    b = a.successors()
    a.display(a)