from rlcard.games.simple_cribbage.card import SimpleCribbageCard as Card

class HumanAgent(object):
    ''' A human agent for Leduc Holdem. It can be used to play against trained models
    '''

    def __init__(self, action_num):
        ''' Initilize the human agent

        Args:
            action_num (int): the size of the ouput action space
        '''
        self.use_raw = True
        self.action_num = action_num

    @staticmethod
    def step(state):
        ''' Human agent will display the state and make decisions through interfaces

        Args:
            state (dict): A dictionary that represents the current state

        Returns:
            action (int): The action decided by human
        '''
        print(state['raw_obs'])
        _print_state(state['raw_obs'], state['action_record'])
        action = int(input('>> You choose action (integer): '))
        while action < 0 or action >= len(state['legal_actions']):
            print('Action illegel...')
            action = int(input('>> Re-choose action (integer): '))
        return state['raw_legal_actions'][action]

    def eval_step(self, state):
        ''' Predict the action given the curent state for evaluation. The same to step here.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        return self.step(state), []


def _print_state(state, action_record):
    ''' Print out the state of a given player

    Args:
        player (int): Player id
    '''
    print('\n=============== Your Hand ===============')
    Card.print_cards(state['hand'])
    print('')
    print('=============== Cards on Table ===============')
    Card.print_cards(state['table'])
    print('')
    print('======== Actions You Can Choose =========')
    actions = state['legal_actions']
    print(', '.join(["{}: {}".format(i, action) for (i, action) in enumerate(actions)]))
