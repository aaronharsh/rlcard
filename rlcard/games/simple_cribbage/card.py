RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = ['C', 'H', 'D', 'S']

RANK_TO_OFFSET = {r:i for (i,r) in enumerate(RANKS)}
SUIT_TO_OFFSET = {s:i for (i,s) in enumerate(SUITS)}

RANK_PIPS = {
    'A': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10
}

class SimpleCribbageCard(object):

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.str = self.get_str()


    def get_str(self):
        return self.rank + '-' + self.suit

    def pips(self):
        return RANK_PIPS[self.rank]

    @staticmethod
    def rank(card_str):
        return card_str.split('-')[0]


    @staticmethod
    def print_cards(cards):
        print(','.join(cards))
