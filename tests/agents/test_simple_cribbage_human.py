import unittest

from rlcard.agents.simple_cribbage_human_agent import _print_state

class TestSimpleCribbageHuman(unittest.TestCase):

    def test_print_state(self):
        raw_state = {'table': ['A-C'], 'hand': ['5-H', '10-D'], 'legal_actions': ['5-H', '10-D']}
        action_record = []
        _print_state(raw_state, action_record)
