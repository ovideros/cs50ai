"""
Tic Tac Toe Player
"""

import math
import copy

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
    # initialize counts
    x_count = 0
    o_count = 0
    # iterate through the board
    for i in range(3):
        for j in range(3):
            if (board[i][j] == X):
                x_count += 1
            if (board[i][j] == O):
                o_count += 1
    # initial state, X comes first
    if (x_count == 0 and o_count == 0):
        return X
    if (x_count > o_count):
        return O
    if (x_count == o_count):
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # stores all the actions
    available_actions = set()
    # iterate through the board
    for i in range(3):
        for j in range(3):
            if (board[i][j] == EMPTY):
                available_actions.append((i, j))
    return available_actions

def is_valid_action(board, action):
    i, j = action
    if (board[i][j] != EMPTY):
        raise ValueError("Action point is not empty.")
    if (i < 0 or i >= 3 or j < 0 or j >= 3):
        raise ValueError("Action index is out of bound.")

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # break down action into i, j
    i, j = action
    # cannot move
    is_valid_action(board, action)
    new_board = copy.deepcopy(board)
    # find player
    now_player = player(board)
    new_board[i][j] = now_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    tiles = []
    # rows
    for j in range(3):
        for i in range(3):
            tiles.append(board[i][j])
        if (judge_three(tiles)):
            return judge_three(tiles)
        tiles.clear()
    # columns
    for i in range(3):
        for j in range(3):
            tiles.append(board[i][j])
        if (judge_three(tiles)):
            return judge_three(tiles)
        tiles.clear()
    
    # diagonal
    for i in range(3):
        tiles.append(board[i][i])
    if (judge_three(tiles)):
        return judge_three(tiles)
    tiles.clear()
    # anti diagonal
    for i in range(3):
        tiles.append(board[i][2 - i])
    if (judge_three(tiles)):
        return judge_three(tiles)
    tiles.clear()
    return None


def judge_three(tiles):
    if (all([tile == X for tile in tiles])):
        return X
    if (all([tile == O for tile in tiles])):
        return O
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board)):
        return True
    is_full = True
    for i in range(3):
        for j in range(3):
            if (board[i][j] == EMPTY):
                is_full = False
    if (is_full):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if (winner(board) == X):
        return 1
    if (winner(board) == O):
        return -1
    return 0
    


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if (terminal(board)):
        return None
    now_player = player(board)
    best_action = ()
    if (now_player == X): # maximize the result
        highest_value = -float('inf')
        for action in actions(board):
            if (min_value(result(board, action)) > highest_value):
                highest_value = min_value(result(board, action))
                best_action = action
        return best_action
    else: # minimize the result
        lowest_value = float('inf')
        for action in actions(board):
            if (max_value(result(board, action)) < lowest_value):
                lowest_value = max_value(result(board, action))
                best_action = action
        return best_action
    
                                
def max_value(board):
    value = -float('inf')
    if (terminal(board)):
        return utility(board)
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value


def min_value(board):
    value = float('inf')
    if (terminal(board)):
        return utility(board)
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value
