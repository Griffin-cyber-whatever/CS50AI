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
    if isinstance(board, Board):
        if board.player == X:
            return O
        return X
    raise Exception("incorrect board")


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    assert isinstance(board, Board)
    actions = []
    state = board.state
    for i in range(3):
        for j in range(3):
            if state[i][j] == EMPTY:
                actions.append((i, j))
    return actions            


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    assert isinstance(board, Board)
    print(action)
    state = [row[:] for row in board.state]
    opponent = player(board)
    if state[action[0]][action[1]] != EMPTY:
        raise Exception("invalid action")
    state[action[0]][action[1]] = opponent
    return Board(opponent, state, board, action)
        

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    assert isinstance(board, Board)
    state = board.state
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
    assert isinstance(board, Board)
    if winner(board):
        return True
    return not any(EMPTY in row for row in board.state)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # You may assume utility will only be called on a board if terminal(board) is True.
    assert isinstance(board, Board)
    winner_player = winner(board)
    return 0 if winner_player is None else (1 if winner_player == X else -1)


def minimax(board):
    """
    Returns the optimal [board, score] for the current player on the board.
    """
    assert isinstance(board, Board)
    
    if terminal(board):
        return (None, utility(board))
    
    if board.player == X:
        best_score = -math.inf
        best_move = None
        for action in actions(board):
            _, score = minimax(result(board, action))
            if score > best_score:
                best_score = score
                best_move = action
        return (best_move, best_score)
    else:
        best_score = math.inf
        best_move = None
        for action in actions(board):
            _, score = minimax(result(board, action))
            if score < best_score:
                best_score = score
                best_move = action
        return (best_move, best_score)


class Board:
    def __init__(self, player = X, state = initial_state(), parent = None, action = None):
        self.player = player
        self.state = state
        self.parent = parent
        self.action = action