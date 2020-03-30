import numpy as np

from rlcard.games.simple_cribbage.card import SimpleCribbageCard as Card, RANK_PIPS
from rlcard.games.simple_cribbage.utils import cards2list


class SimpleCribbageRound(object):

    def __init__(self, dealer, num_players):
        ''' Initialize the round class

        Args:
            dealer: SimpleCribbageDealer
            num_players: int (the number of players in game)
        '''
        self.dealer = dealer
        self.table = []
        self.current_player = 0
        self.num_players = num_players
        self.count = 0
        self.is_over = False
        self.winner = None


    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            players: [SimpleCribbagePlayer]
            action: str
        '''
        if action == 'draw':
            self._perform_draw_action(players)
            return None

        player = players[self.current_player]
        (rank, suit) = action.split('-')

        player.hand = [card for card in player.hand if card != action]

        self.table.append(action)
        self.count += RANK_PIPS(rank)

        score = 0
        if self.count == 15 || (self.table and Card.rank(self.table[-1]) == rank):
            score = 2
        elif not (players[0].hand or players[1].hand):
            score = 1

        if score > 0:
            player.score += score
            self.is_over = True
            self.winner = [self.current_player]


    def get_legal_actions(self, players, player_id):
        return players[player_id].hand


    def get_state(self, players, player_id):
        ''' Get player's state

        Args:
            players: [SimpleCribbagePlayer]
            player_id: int (the id of the player)
        '''
        state = {}
        player = players[player_id]
        state['hand'] = cards2list(player.hand)
        state['table'] = self.table
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        return state
