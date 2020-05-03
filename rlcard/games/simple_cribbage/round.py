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
        player = players[self.current_player]
        (rank, suit) = action.split('-')

        player.hand = [card for card in player.hand if card.get_str() != action]

        self.count += RANK_PIPS[rank]

        score = 0
        if self.count == 15 or (self.table and Card.rank(self.table[-1]) == rank):
            score = 2
        elif self.count == 31:
            score = 2
        elif not self.get_legal_actions(players, 1 - self.current_player):
            score = 1

        if score > 0:
            player.score += score
            self.is_over = True
            self.winner = [self.current_player]

        self.table.append(action)

        self.current_player = 1 - self.current_player


    def get_legal_actions(self, players, player_id):
        cocount = 31 - self.count
        cards_under_31 = [c for c in players[player_id].hand if c.pips() <= cocount]
        return cards2list(cards_under_31)


    def get_state(self, players, player_id):
        ''' Get player's state

        Args:
            players: [SimpleCribbagePlayer]
            player_id: int (the id of the player)
        '''
        state = {}
        player = players[player_id]
        state['hand'] = cards2list(player.hand)
        state['others_hand'] = cards2list(players[1 - player_id].hand)
        state['table'] = self.table
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        return state
