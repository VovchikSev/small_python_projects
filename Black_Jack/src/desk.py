"""
Класс колоды карт и сомой карты.

"""
from itertools import product
from random import shuffle

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['♥', '♠', '♣', '♦']


class Card:
    
    def __init__(self, suit, rank, points):
        self.suit = suit
        self.rank = rank
        self.picture = f'{self.rank} of {self.suit}'
        self.points = points
    
    def __str__(self):
        return self.picture


class Deck:
    
    def __init__(self):
        # переделать на гнерацию с
        self.cards: list[Card] = []
        self._generate_deck()
        shuffle(self.cards)
    
    def _generate_deck(self) -> list[Card]:
        cards = []
        # функцмя product создаеь список из двух аереданных ему
        for suit, rank in product(SUITS, RANKS):
            if rank == 'A':
                points = 11
            elif rank.isdigit():
                points = int(rank)
            else:
                points = 10
            c = Card(suit=suit, rank=rank, points=points)
            self.cards.append(c)
        # return cards
    
    def get_card(self):
        return self.cards.pop()
    
    def __len__(self):
        return len(self.cards)
