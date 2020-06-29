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
        cnt += lst.count("EMPTY")

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
            if (board[i][j] == "EMPTY"):

                # Add to the set #
                moves.add((i, j))

    # Check if set is empty i.e. terminal state #
    if moves == set():
        return None

    # Else return all possible moves #
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check if the action is valid #
    if (board[action[0]][action[1]] != "EMPTY"):
        raise Exception("Invalid Action !")
        return

    # Get the Player #
    player = player(board)

    # Create a DeepCopy of the Board #
    boardcopy = deepcopy(board)

    # Make the move #
    boardcopy[action[0]][action[1]] = player

    # Return the resulting board #
    return boardcopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check Rows #
    def checkRow(board, player):
        for i in range(3):
            if(board[i][0] == player and board[i][1] == player and
                board[i][2] == player): return player

    # Check Cols #
    def checkCols(board, player):
        for i in range(3):
            if(board[0][i] == player and board[1][i] == player and
                board[2][i] == player): return player

    # Check Diagonals #
    def checkDiags(board, player):
        if(board[0][0] == player and board[1][1] == player and
            board[2][2] == player): return player
        if(board[2][0] == player and board[1][1] == player and
            board[0][2] == player): return player

    # Check for X #
    checkRow(board, "X")
    checkCols(board, "X")
    checkDiags(board, "X")

    # Check for X #
    checkRow(board, "Y")
    checkCols(board, "Y")
    checkDiags(board, "Y")

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Check if we have a Winner  #
    Winner = winner(board)
    if (Winner == "X" or Winner == "O"):
        return True

    # Check if Board is completely filled #
    for lst in board:
        if ("EMPTY" in lst):
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # Get the winner #
    Winner = winner(board)

    # return the Winner #
    if (Winner == "X"):
        return 1
    elif (Winner == "O"):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Defining Maximizing Function #
    def alphabeta(board, alpha, beta, maximizingPlayer):
        # If Board is in Terminal State #
        if terminal(board):
            return None

        # Maximizing Player #
        if maximizingPlayer :
            value = -2

            # Check for every action possible #
            for act in actions(board):
                value = max(value, alphabeta(board, alpha, beta, False)[0])
                alpha = max(alpha, value)

                # Prunning #
                if (alpha >= beta):
                    break
                # Get the possibel action #
                px = act[0]
                py = act[1]
            return value, (px, py)

        # Minimizing Player #
        else
            value = 2

            # Check for every action possible #
            for act in actions(board):
                value = min(value, alphabeta(board, alpha, beta, TRUE)[0])
                beta = min(beta, value)

                # Prunning #
                if beta ≤ alpha then
                    break

                # Get the possibel action #
                px = act[0]
                py = act[1]

            return value, (px, py)

        # Optimal Move #
        return alphabeta(board = board, alpha = -5, beta = 5, False)[1]
