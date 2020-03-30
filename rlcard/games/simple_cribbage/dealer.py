import random

from rlcard.games.simple_cribbage.utils import init_deck


class SimpleCribbageDealer(object):
    def __init__(self):
        self.deck = init_deck()
        self.shuffle()

    def shuffle(self):
        ''' Shuffle the deck
        '''
        random.shuffle(self.deck)

    def deal_cards(self, player, num):
        for _ in range(num):
            player.hand.append(self.deck.pop())
