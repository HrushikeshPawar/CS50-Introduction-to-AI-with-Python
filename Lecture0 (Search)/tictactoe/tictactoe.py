"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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

    # Initialize the counter #
    cnt = 0

    # Count the empty boxes in the grid #
    for lst in board:
        cnt += lst.count(EMPTY)

    # Return the player #
    if (cnt % 2 == 0):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Create a set "moves" #
    moves = set()

    # Iteratively check every box #
    for i in range(3):
        for j in range(3):

            # Check if box is EMPTY #
            if (board[i][j] is None):

                # Add to the set #
                moves.add((i, j))

    # Check if set is empty i.e. terminal state #
    if terminal(board):
        return None

    # Else return all possible moves #
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check if the action is valid #
    if (board[action[0]][action[1]] is not None):
        raise Exception("Invalid Action !")
        return

    # Create a DeepCopy of the Board #
    boardcopy = deepcopy(board)

    # Get the Player #
    Player = player(boardcopy)

    # Make the move #
    boardcopy[action[0]][action[1]] = Player

    # Return the resulting board #
    return boardcopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check Rows #
    def checkRow(board):
        for row in board :
            # Check for X #
            if (row.count(X) == 3):
                return X

            # Check for O #
            elif (row.count(O) == 3):
                return O

        # no winner in rows #
        return None

    # Check Cols #
    def checkCols(board):
        for i in range(3):
            # Check for X #
            if(board[0][i] is X and board[1][i] is X and
                board[2][i] is X):
                return X

            # Check for O #
            if(board[0][i] == O and board[1][i] == O and
                board[2][i] == O):
                return O

        # No winner in Columns #
        return None

    # Check Diagonals #
    def checkDiags(board):
        # Check X for Left Diagonal #
        if(board[0][0] == X and board[1][1] == X and
            board[2][2] == X):
            return X

        # Check X for Right Diagonal #
        elif(board[2][0] == X and board[1][1] == X and
            board[0][2] == X):
            return X

        # Check O for Left Diagonal #
        elif(board[0][0] == O and board[1][1] == O and
            board[2][2] == O):
            return O

        # Check X for Right Diagonal #
        elif(board[2][0] == O and board[1][1] == O and
            board[0][2] == O):
            return O

        # No Winner in Diagonals #
        return None

    # Check for the winners #
    row_win = checkRow(board)
    col_win = checkCols(board)
    diag_win = checkDiags(board)

    # Return the Winner #
    if (row_win is not None):
        return row_win
    elif (col_win is not None):
        return col_win
    elif (diag_win is not None):
        return diag_win
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Check if we have a Winner  #
    Winner = winner(board)
    if (Winner is X or Winner is O):
        return True

    # Check if Board is completely filled #
    for row in board:
        if (None in row):
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # Get the winner #
    Winner = winner(board)

    # return the Winner #
    if (Winner is X):
        return 1
    elif (Winner is O):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Max-Value Function #
    def maxValue(board, alpha, beta):
        #check if the board is Terminal #
        if terminal(board):
            return utility(board)

        # Initialize the value #
        value = -2
        for act in actions(board):
            value = max(value, minValue(result(board, act), alpha, beta))
            alpha = max(alpha, value)

            # Prune - Beta cutoff #
            if (alpha >= beta):
                break

        # Return Max-Value #
        return value

    # Min-Value Function #
    def minValue(board, alpha, beta):
        #check if the board is Terminal #
        if terminal(board):
            return utility(board)

        # Initialize the value #
        value = 2
        for act in actions(board):
            value = min(value, maxValue(result(board, act), alpha, beta))
            beta = min(beta, value)

            # Prune - Alpha cutoff #
            if (beta <= alpha):
                break

        # Return Min-Value #
        return value

    # Set alpha beta to min and max utility #
    alpha = -1
    beta = 1

    # If Maximizing Player #
    if (player(board) is X):
        maxi = -5
        for act in actions(board):
            value = minValue(result(board, act), alpha, beta)
            if (value > maxi):
                maxi = value
                Action = act
    else:
        mini = 5
        for act in actions(board):
            value = maxValue(result(board, act), alpha, beta)
            if (value < mini):
                mini = value
                Action = act

    # Return Optimal Action #
    return Action
