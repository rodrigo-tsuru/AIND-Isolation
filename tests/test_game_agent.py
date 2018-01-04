"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import logging
import logging.config

logging.config.fileConfig('logging.conf',disable_existing_loggers=False)

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    logger = logging.getLogger('IsolationTest')

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"

        logging.info("Creating empty game board...")
        self.game = isolation.Board(self.player1, self.player2)

    @unittest.skip
    def test_minimax(self):

        p1 = game_agent.MinimaxPlayer()
        p1.search_depth = 1

        p2 = game_agent.MinimaxPlayer()
        p2.search_depth = 1

        # Create a smaller board for testing
        self.game = isolation.Board(p1, p2, 9, 9)

        self.game._board_state =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 21]
        
        logging.info(self.game.to_string())

        # players take turns moving on the board, so player1 should be next to move
        assert(p1 == self.game.active_player)

        winner, history, outcome = self.game.play()
        logging.info("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        logging.info(self.game.to_string())
        logging.info("Move history:\n{!s}".format(history))

        # Check the first selected move
        expectedResults = [[2,4]]
        self.assertIn(history[0],expectedResults)


    def test_alphabeta(self):

        p1 = game_agent.AlphaBetaPlayer()
        p1.search_depth = 2

        p2 = game_agent.AlphaBetaPlayer()
        p2.search_depth = 2

        # Create a smaller board for testing
        self.game = isolation.Board(p1, p2, 9, 9)

        self.game._board_state =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 51, 69]
        
        logging.info(self.game.to_string())

        # players take turns moving on the board, so player1 should be next to move
        assert(p1 == self.game.active_player)

        winner, history, outcome = self.game.play()
        logging.info("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        logging.info(self.game.to_string())
        logging.info("Move history:\n{!s}".format(history))

        # Check the first selected move
        #expectedResults = [[2,4]]
        #self.assertIn(history[0],expectedResults)

if __name__ == '__main__':
    unittest.main()
