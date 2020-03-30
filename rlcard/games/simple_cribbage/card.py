RANKS = ['A', '5', '10', 'J']
SUITS = ['C', 'H', 'D', 'S']

RANK_TO_OFFSET = {r:i for (i,r) in enumerate(RANKS)}
SUIT_TO_OFFSET = {s:i for (i,s) in enumerate(SUITS)}

RANK_PIPS = {
    'A': 1,
    '5': 5,
    '10': 10,
    'J': 10
}

class SimpleCribbageCard(object):

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.str = self.get_str()


    def get_str(self):
        return self.rank + '-' + self.suit


    @staticmethod
    def rank(card_str):
        return card_str.split('-')[0]


    @staticmethod
    def print_cards(cards):
        print(','.join([c.get_str() for c in cards]))
