"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None



def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_of_X, num_of_O = 0, 0
    for i in board:
        for j in i:
            if j == X:
                num_of_X += 1
            elif j == O:
                num_of_O += 1
    if num_of_O == num_of_X == 0:
        return X
    elif num_of_X > num_of_O:
        return O
    return X
    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions            


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not 0 <= action[0] <= 3 or not 0 <= action[1] <= 3:
        raise Exception("invalid action argument on result function")
    state = [row[:] for row in board]
    opponent = player(board)
    if state[action[0]][action[1]] != EMPTY:
        raise Exception("invalid action")
    state[action[0]][action[1]] = opponent
    return state

def winner(state):
    """
    Returns the winner of the game, if there is one.
    """
    # the vertical/ horizontal check
    for i in range(3):
        if state[i][0] == state[i][1] == state[i][2] and state[i][0]:
            return state[i][0]
        if state[0][i] == state[1][i] == state[2][i] and state[0][i]:
            return state[0][i]
    # the diagonal check
    if state[0][0] == state[1][1] == state[2][2] and state[1][1]:
        return state[1][1]
    if state[0][2] == state[1][1] == state[2][0] and state[1][1]:
        return state[1][1]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    return not any(EMPTY in row for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # You may assume utility will only be called on a board if terminal(board) is True.
    winner_player = winner(board)
    return 0 if winner_player is None else (1 if winner_player == X else -1)


def minimax(board):
    """
    Returns the optimal [board, score] for the current player on the board.
    """
    def h(board):
        if terminal(board):
            return (None, utility(board))
        
        if player(board) == X:
            best_score = -math.inf
            best_move = None
            for action in actions(board):
                _, score = h(result(board, action))
                if score > best_score:
                    best_score = score
                    best_move = action
            return (best_move, best_score)
        else:
            best_score = math.inf
            best_move = None
            for action in actions(board):
                _, score = h(result(board, action))
                if score < best_score:
                    best_score = score
                    best_move = action
            return (best_move, best_score)
    return h(board)[0]
