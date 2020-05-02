import sys
import numpy as np

from rlcard.games.simple_cribbage.card import RANKS, SUITS, RANK_TO_OFFSET, SUIT_TO_OFFSET
from rlcard.games.simple_cribbage.card import SimpleCribbageCard as Card

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

def decode_card_strs(plane):
    card_strs = []
    for rank_i, rank in enumerate(RANKS):
        for suit_i, suit in enumerate(SUITS):
            if plane[rank_i, suit_i] == 1:
                card_strs.append(rank + "-" + suit)
    return card_strs

def print_dqn_params(i, state_batch, legal_actions_batch, action_batch, reward_batch, next_state_batch, done_batch, q_values_next, target_batch, file=sys.stdout):
    legal_action_q_values_next = q_values_next[i][legal_actions_batch[i]]
    print(f"cards = {decode_card_strs(state_batch[i][0])}, table = {decode_card_strs(state_batch[i][1])}", file=file)
    print(f"legal_actions = {[INVERSE_ACTION_SPACE[a] for a in legal_actions_batch[i]]}, q_values_next = {legal_action_q_values_next}, action = {INVERSE_ACTION_SPACE[action_batch[i]]}", file=file)
    print(f"reward = {reward_batch[i]}, done = {done_batch[i]}, target = {target_batch[i]}, next cards = {decode_card_strs(next_state_batch[i][0])}, next table = {decode_card_strs(next_state_batch[i][1])}", file=file)