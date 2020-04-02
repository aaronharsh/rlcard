import os
import json
import numpy as np
from collections import OrderedDict

import rlcard

from rlcard.games.simple_cribbage.card import SimpleCribbageCard as Card
from rlcard.games.simple_cribbage.card import RANKS, SUITS, RANK_PIPS, RANK_TO_OFFSET, SUIT_TO_OFFSET



ACTION_LIST = [r+'-'+s for r in RANKS for s in SUITS]
ACTION_SPACE = {c:i for (i,c) in enumerate(ACTION_LIST)}
INVERSE_ACTION_SPACE = {i:c for (i,c) in enumerate(ACTION_LIST)}


def init_deck():
    return [Card(r, s) for r in RANKS for s in SUITS]


def cards2list(cards):
    return [card.get_str() for card in cards]


def card_str_rank_suit(card_str):
    return card_str.split('-')


def encode_card_strs(plane, card_strs):
    plane[:] = np.zeros(plane.shape)
    for card_str in card_strs:
        (rank, suit) = card_str_rank_suit(card_str)
        plane[RANK_TO_OFFSET[rank], SUIT_TO_OFFSET[suit]] = 1
