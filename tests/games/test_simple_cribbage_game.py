import unittest
import numpy as np
from numpy.testing import assert_array_equal

from rlcard.games.simple_cribbage.card import SimpleCribbageCard as Card
from rlcard.games.simple_cribbage.game import SimpleCribbageGame as Game
from rlcard.games.simple_cribbage.player import SimpleCribbagePlayer as Player
from rlcard.games.simple_cribbage.utils import ACTION_LIST
from rlcard.games.simple_cribbage.utils import encode_card_strs, cards2list

class TestSimpleCribbageMethods(unittest.TestCase):

    def test_get_player_num(self):
        game = Game()
        num_player = game.get_player_num()
        self.assertEqual(num_player, 2)

    def test_get_action_num(self):
        game = Game()
        action_num = game.get_action_num()
        self.assertEqual(action_num, 16)

    def test_init_game(self):
        game = Game()
        state, _ = game.init_game()
        total_cards = list(state['hand'] + state['others_hand'])
        self.assertGreaterEqual(len(total_cards), 4)

    def test_get_player_id(self):
        game = Game()
        _, player_id = game.init_game()
        current = game.get_player_id()
        self.assertEqual(player_id, current)


    def test_get_legal_actions(self):
        game = Game()
        game.init_game()
        actions = game.get_legal_actions()
        for action in actions:
            self.assertIn(action, ACTION_LIST)

    def test_step(self):
        game = Game()
        game.init_game()
        game.players[0].hand = [Card('A', 'H'), Card('10', 'D')]
        game.players[1].hand = [Card('10', 'S'), Card('J', 'C')]

        self.assertEqual(game.round.current_player, 0)

        game.step('A-H')

        self.assertEqual(game.round.current_player, 1)
        self.assertEqual(cards2list(game.players[0].hand), cards2list([Card('10', 'D')]))
        self.assertEqual(game.round.count, 1)
        self.assertFalse(game.round.is_over)
        self.assertEqual(game.round.winner, None)

        game.step('10-S')

        self.assertEqual(game.round.current_player, 0)
        self.assertEqual(cards2list(game.players[1].hand), cards2list([Card('J', 'C')]))
        self.assertEqual(game.round.count, 11)
        self.assertFalse(game.round.is_over)
        self.assertEqual(game.round.winner, None)

        game.step('10-D')

        self.assertEqual(game.round.current_player, 1)
        self.assertEqual(cards2list(game.players[0].hand), [])
        self.assertEqual(game.round.count, 21)
        self.assertTrue(game.round.is_over)
        self.assertEqual(game.round.winner, [0])

    def test_step_back(self):
        game = Game(allow_step_back=True)
        _, player_id = game.init_game()
        action = np.random.choice(game.get_legal_actions())
        game.step(action)
        game.step_back()
        self.assertEqual(game.round.current_player, player_id)
        self.assertEqual(len(game.history), 0)
        success = game.step_back()
        self.assertEqual(success, False)

    def test_encode_card_strs(self):
        hand1 = ['A-D', '5-C', '5-S', '10-D', 'J-H']
        encoded_hand1 = np.zeros((4, 4), dtype=int)
        encode_card_strs(encoded_hand1, hand1)
        assert_array_equal(
            encoded_hand1,
            [[0, 0, 1, 0],
             [1, 0, 0, 1],
             [0, 0, 1, 0],
             [0, 1, 0, 0]])

    def test_player_get_player_id(self):
        player = Player(0)
        self.assertEqual(0, player.get_player_id())

if __name__ == '__main__':
    unittest.main()
