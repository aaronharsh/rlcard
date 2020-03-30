import numpy as np

import rlcard
from rlcard.models.model import Model

class SimpleCribbageRuleAgentV1(object):
    ''' Simple Cribbage Rule agent version 1
    '''

    def __init__(self):
        self.use_raw = True


    def step(self, state):
        ''' Predict the action given raw state. Very naive -- just returns a
            random legal action

        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''

        legal_actions = state['raw_legal_actions']

        return np.random.choice(legal_actions)


    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []


class SimpleCribbageRuleModelV1(Model):
    ''' Simple Cribbage Rule Model version 1
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('simple-cribbage')

        rule_agent = SimpleCribbageRuleAgentV1()
        self.rule_agents = [rule_agent for _ in range(env.player_num)]


    @property
    def agents(self):
        ''' Get a list of agents for each position in the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.rule_agents


    @property
    def use_raw(self):
        ''' Indicate whether use raw state and action

        Returns:
            use_raw (boolean): True if using raw state and action
        '''
        return True
