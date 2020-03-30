import numpy as np

from rlcard.envs.env import Env
from rlcard import models
from rlcard.games.simple_cribbage.game import SimpleCribbageGame as Game
from rlcard.games.simple_cribbage.game import NUM_CARDS_DEALT, NUM_RANKS, NUM_SUITS, MAX_NUM_CARDS_ON_TABLE_BEFORE_DETERMINISTIC
from rlcard.games.simple_cribbage.utils import encode_cards
from rlcard.games.simple_cribbage.utils import ACTION_SPACE, ACTION_LIST

STATE_SHAPE = (
  2, # player, table
  NUM_RANKS,
  NUM_SUITS
)

class SimpleCribbageEnv(Env):

    def __init__(self, config):
        self.game = Game()
        super().__init__(config)

        self.state_shape = STATE_SHAPE

    def _load_model(self):
        ''' Load pretrained/rule model

        Returns:
            model (Model): A Model object
        '''
        return models.load('simple-cribbage-rule-v1')

    def _extract_state(self, state):
        obs = np.zeros(STATE_SHAPE, dtype=int)

        encode_cards(obs[0], state['hand'])
        encode_cards(obs[1], state['table'])

        legal_action_ids = self._get_legal_actions()
        extracted_state = {'obs': obs, 'legal_actions': legal_action_ids}
        if self.allow_raw_data:
            extracted_state['raw_obs'] = state
            extracted_state['raw_legal_actions'] = [a for a in state['legal_actions']]
        if self.record_action:
            extracted_state['action_record'] = self.action_recorder
        return extracted_state

    def get_payoffs(self):
        return self.game.get_payoffs()

    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        if action_id in legal_ids:
            return ACTION_LIST[action_id]
        else:
            return ACTION_LIST[np.random.choice(legal_ids)]

    def _get_legal_actions(self):
        legal_actions = self.game.get_legal_actions()
        legal_ids = [ACTION_SPACE[action] for action in legal_actions]
        return legal_ids
