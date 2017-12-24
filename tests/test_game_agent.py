"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"

        print("Creating empty game board...")
        self.game = isolation.Board(self.player1, self.player2)

    def test_minimax(self):

        p1 = game_agent.MinimaxPlayer()
        p1.time_left = 300.0

        p2 = game_agent.MinimaxPlayer()
        p2.time_left = 300.0

        # Create a smaller board for testing
        self.game = isolation.Board(p1, p2, 3, 3)

        self.game.apply_move((0, 0))
        self.game.apply_move((0, 2))
        
        print(self.game.to_string())

        # players take turns moving on the board, so player1 should be next to move
        assert(p1 == self.game.active_player)

        # get a list of the legal moves available to the active player
        print("legal moves: {0}".format(self.game.get_legal_moves()))

        winner, history, outcome = self.game.play()

        if winner==self.game._player_1:
            print("vencedor: player 1");
        else:
            print("vencedor: player 2");
        print("\nWinner: {}\nOutcome: {}".format("", outcome))
        print(self.game.to_string())
        print("Move history:\n{!s}".format(history))

        #v = p1.minimax(self.game,3)

        #self.assertEqual(v,1)

if __name__ == '__main__':
    unittest.main()
