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

    def test_minimax(self):

        p1 = game_agent.MinimaxPlayer()
        p1.time_left = 300.0

        p2 = game_agent.MinimaxPlayer()
        p2.time_left = 300.0

        # Create a smaller board for testing
        self.game = isolation.Board(p1, p2, 7, 7)

        self.game.apply_move((0, 0))
        self.game.apply_move((0, 2))
        
        logging.info(self.game.to_string())

        # players take turns moving on the board, so player1 should be next to move
        assert(p1 == self.game.active_player)

        # get a list of the legal moves available to the active player
        logging.info("legal moves: {0}".format(self.game.get_legal_moves()))

        winner, history, outcome = self.game.play()

        if winner==self.game._player_1:
            logging.info("vencedor: player 1");
        else:
            logging.info("vencedor: player 2");
        logging.info("\nWinner: {}\nOutcome: {}".format("", outcome))
        logging.info(self.game.to_string())
        logging.info("Move history:\n{!s}".format(history))

        #v = p1.minimax(self.game,3)

        #self.assertEqual(v,1)

if __name__ == '__main__':
    unittest.main()
