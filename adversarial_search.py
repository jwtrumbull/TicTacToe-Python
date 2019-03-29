# -----------------------------------------------------------------------------
# Name:     adversarial_search
# Purpose:  Homework5 - Implement adversarial search algorithms
#
# Author:
#
# -----------------------------------------------------------------------------
"""
Adversarial search algorithms implementation

Your task for homework 5 is to implement:
1.  minimax
2.  alphabeta
3.  abdl (alpha beta depth limited)
"""
import random
import sys

def rand(game_state):
    """
    Generate a random move.
    :param game_state: GameState object
    :return:  a tuple representing the row column of the random move
    """
    found = False
    while not found:
        row = random.randint(0, game_state.size - 1)
        col = random.randint(0, game_state.size - 1)
        if game_state.available(row,col):
            found = True
    return row, col


def minimax(game_state):
    """
    Find the best move for our AI agent by applying the minimax algorithm
    (searching the entire tree from the current game state)
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    # Enter your code here and remove the raise statement below
    v = -1000
    for i in game_state.possible_moves():
        g = game_state.successor(i, 'AI')
        s = value(g, 'user')
        v = max(v, s)
        if v == s:
            m = i
    return m
def value(game_state, player):
    """
    Calculate the minimax value for any state under the given agent's control
    :param game_state: GameState object - state may be terminal or non-terminal
    :param player: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    if game_state.is_win('AI'):
        return 1
    if game_state.is_win('user'):
        return -1
    if game_state.is_tie():
        return 0
    if player is 'AI':
        return max_value(game_state)
    if player is 'user':
        return min_value(game_state)

def max_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent)
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    v = -1000
    for i in game_state.possible_moves():
        g = game_state.successor(i, 'AI')
        v = max(v,value(g, 'user'))
    return v

def min_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user)
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    v = 1000
    for i in game_state.possible_moves():
        g = game_state.successor(i, 'user')
        v = min(v, value(g, 'AI'))
    return v



def alphabeta(game_state):
    """
    Find the best move for our AI agent by applying the minimax algorithm
    with alpha beta pruning.
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    # Enter your code here and remove the raise statement below
    v = -1000
    alpha = -1000
    beta = 1000
    for i in game_state.possible_moves():
        g = game_state.successor(i, 'AI')
        s = abvalue(g, 'user', alpha, beta)
        v = max(v, s)
        if v == s:
            m = i

    return m


def abvalue(game_state, player, alpha, beta):
    """
    Calculate the minimax value for any state under the given agent's control
    using alpha beta pruning
    :param game_state: GameState object - state may be terminal or non-terminal
    :param player: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    if game_state.is_win('AI'):
        return 1
    if game_state.is_win('user'):
        return -1
    if game_state.is_tie():
        return 0
    if player is 'AI':
        return abmax_value(game_state, alpha, beta)
    if player is 'user':
        return abmin_value(game_state, alpha, beta)


def abmax_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent) using alpha beta pruning
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    v = -100
    for i in game_state.possible_moves():
        s = game_state.successor(i, 'AI')
        v = max(v, abvalue(s,'user',alpha,beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def abmin_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user) using alpha beta pruning
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    v = 1000
    for i in game_state.possible_moves():
        s = game_state.successor(i, 'user')
        v = min(v, abvalue(s, 'AI', alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def abdl(game_state, depth):
    """
    Find the best move for our AI agent by limiting the alpha beta search to
    the given depth and using the evaluation function game_state.eval()
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    # Enter your code here and remove the raise statement below
    v = -1000
    alpha = -1000
    beta = 1000
    for i in game_state.possible_moves():
        g = game_state.successor(i, 'AI')
        s = abvalue_dl(g, 'user', alpha, beta, depth)
        v = max(v, s)
        if v == s:
            m = i
    return m



def abvalue_dl(game_state, player, alpha, beta, depth):
    """
    Calculate the utility for any state under the given agent's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: GameState object - state may be terminal or non-terminal
    :param player: (string) 'user' or 'AI' - AI is max
    :return: (integer) utility of that state
    """
    # Enter your code here and remove the pass statement below
    if depth is 0:
        return game_state.eval()
    if game_state.is_win('AI'):
        return 1
    if game_state.is_win('user'):
        return -1
    if game_state.is_tie():
        return 0
    if player is 'AI':
        return abmax_value_dl(game_state, alpha, beta, depth-1)
    if player is 'user':
        return abmin_value_dl(game_state, alpha, beta, depth-1)


def abmax_value_dl(game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Max's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    # Enter your code here and remove the pass statement below
    v = -100
    for i in game_state.possible_moves():
        s = game_state.successor(i, 'AI')
        v = max(v, abvalue_dl(s, 'user', alpha, beta, depth))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def abmin_value_dl( game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Min's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    # Enter your code here and remove the pass statement below
    v = 1000
    for i in game_state.possible_moves():
        s = game_state.successor(i, 'user')
        v = min(v, abvalue_dl(s, 'AI', alpha, beta, depth))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

