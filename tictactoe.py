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
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    current_player = player(board)
    new_board = [row[:] for row in board]
    new_board[i][j] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(all(cell is not EMPTY for cell in row) for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    final_win = winner(board)
    if final_win == X:
        return 1
    elif final_win == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    I am using alpha beta-pruning
    """

    def max_func(board, alpha, beta):
        if terminal(board):
            return utility(board), None

        v = float("-inf")
        take_action_max = None

        for action in actions(board):
            minimum, _ = min_func(result(board, action), alpha, beta)
            if minimum > v:
                v = minimum
                take_action_max = action
            alpha = max(alpha, v)
            if alpha >= beta:
                break  # Beta Cut-off

        return v, take_action_max

    def min_func(board, alpha, beta):
        if terminal(board):
            return utility(board), None

        v = float("inf")
        take_action_min = None

        for action in actions(board):
            maximum, _ = max_func(result(board, action), alpha, beta)
            if maximum < v:
                v = maximum
                take_action_min = action
            beta = min(beta, v)
            if beta <= alpha:
                break  # Alpha Cut-Off

        return v, take_action_min

    if player(board) == X:
        return max_func(board, float("-inf"), float("inf"))[1]
    else:
        return min_func(board, float("-inf"), float("inf"))[1]
