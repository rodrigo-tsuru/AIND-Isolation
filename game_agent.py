"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import logging
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    opponent = game.get_opponent(player)

    #return len(game.get_legal_moves(player)) - len(game.get_legal_moves(opponent))

    #improved_score?
    return float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(opponent)))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    opponent = game.get_opponent(player)

    #return len(game.get_legal_moves(player)) - len(game.get_legal_moves(opponent))

    return float(len(game.get_legal_moves(player)) - 2*len(game.get_legal_moves(opponent)))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    opponent = game.get_opponent(player)

    # put more weight on middle board moves
    center = (game.width/2,game.height/2)
    location = game.get_player_location(player)
    distance_from_center = math.hypot(center[0] - location[0],center[1] - location[1])
    weight = 1/math.exp(distance_from_center)


    #return len(game.get_legal_moves(player)) - len(game.get_legal_moves(opponent))
    return float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(opponent))) * weight


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        #self.logger.debug("time left: " + str(time_left))
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move = self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
#        if self.time_left() < self.TIMER_THRESHOLD:
#            raise SearchTimeout()

        maxv,maxm = self.max_value(game,depth)

        return maxm

    def min_value(self,game,depth):
        """ Return the utility value if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        # terminal tests
        if depth == 0:
            score = self.score(game,game.inactive_player)
            self.logger.debug(depth * ">" + " Score: " + str(score))
            return score,None

        if not bool(legal_moves):
            return game.utility(self),None

        # min value
        minv = float("inf")
        # min value move
        minm = legal_moves[0]

        self.logger.debug(depth * ">" + " MIN")
        for m in legal_moves:
            self.logger.debug("evaluating move: {0}".format(m))
            move_value,move_coord = self.max_value(game.forecast_move(m),depth-1)
            if move_value < minv:
                minv = move_value
                minm = m
        self.logger.debug(depth * "<" + " MIN: " + str(minv))
        return minv,minm


    def max_value(self,game,depth):
        """ Return the utility value if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # terminal test
        legal_moves = game.get_legal_moves()

        # terminal tests
        if depth == 0:
            score = self.score(game,game.active_player)
            self.logger.debug(depth * ">" + " Score: " + str(score))
            return score,None

        if not bool(legal_moves):
            return game.utility(self),None

        # max value
        maxv = float("-inf")
        # max value move
        maxm = legal_moves[0]

        self.logger.debug(depth * ">" + " MAX")
        for m in legal_moves:
            self.logger.debug("evaluating move: {0}".format(m))
            move_value,move_coord = self.min_value(game.forecast_move(m),depth-1)
            if move_value > maxv:
                maxv = move_value
                maxm = m

        self.logger.debug(depth * "<" + " MAX: " + str(maxv))
        return maxv,maxm


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1,-1)
        depth = 1
      
        try:

            while True:
                best_move = self.alphabeta(game.copy(),depth)
                depth+=1

        except SearchTimeout:
            self.logger.debug("Time out!")
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """


        maxv,maxm = self.max_value(game,depth)

        return maxm

    def min_value(self,game,depth,alpha=float("-inf"), beta=float("inf")):
        """ Return the utility value if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        self.logger.debug(" alpha: {0}. beta: {1}".format(alpha,beta))

        legal_moves = game.get_legal_moves()

        # terminal tests
        if depth == 0:
            score = self.score(game,game.inactive_player)
            self.logger.debug(" Score: " + str(score))
            return score,None

        if not bool(legal_moves):
            return game.utility(self),None

        # min value
        minv = float("inf")
        # min value move
        minm = legal_moves[0]

        self.logger.debug(depth * ">" + " MIN")
        for m in legal_moves:
            self.logger.debug(depth * ">" +" evaluating move: {0}".format(m))
            move_value,move_coord = self.max_value(game.forecast_move(m),depth-1,alpha,beta)
            if move_value < minv:
                minv = move_value
                minm = m

            if minv <= alpha:
                self.logger.debug(depth * ">" +" Pruning")
                return minv,minm
            
            beta = min(beta,minv)

        self.logger.debug(depth * "<" + " MIN: " + str(minv))
        return minv,minm


    def max_value(self,game,depth,alpha=float("-inf"), beta=float("inf")):
        """ Return the utility value if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        self.logger.debug(" alpha: {0}. beta: {1}".format(alpha,beta))

        # terminal test
        legal_moves = game.get_legal_moves()

        # terminal tests
        if depth == 0:
            score = self.score(game,game.active_player)
            self.logger.debug(" Score: " + str(score))
            return score,None

        if not bool(legal_moves):
            return game.utility(self),None

        # max value
        maxv = float("-inf")
        # max value move
        maxm = legal_moves[0]

        self.logger.debug(depth * ">" + " MAX")
        for m in legal_moves:
            self.logger.debug(depth * ">" +" evaluating move: {0}".format(m))
            move_value,move_coord = self.min_value(game.forecast_move(m),depth-1,alpha,beta)
            if move_value > maxv:
                maxv = move_value
                maxm = m

            if maxv >= beta:
                self.logger.debug(depth * ">" +" Pruning")
                return maxv,maxm

            alpha = max(alpha,maxv)

        self.logger.debug(depth * "<" + " MAX: " + str(maxv))
        return maxv,maxm

