from itertools import product
from random import shuffle

from Black_Jack.example.bj_itvdn_youtube.src.const import *


class Card:
    
    def __init__(self, suit, rank, picture, points):
        self.suit = suit
        self.rank = rank
        self.picture = picture
        self.points = points
    
    def __str__(self):
        message = self.picture + '\nPoints: ' + str(self.points)
        return message


class Deck:
    
    def __init__(self):
        # переделать на гнерацию с
        self.cards: list[Card] = self._generate_deck()
        shuffle(self.cards)
    
    def _generate_deck(self) -> list[Card]:
        cards = []
        # функцмя product создаеь список из двух аереданных ему
        for suit, rank in product(COLOR_SUITS, RANKS):
            if rank == 'ace':
                points = 11
            elif rank.isdigit():
                points = int(rank)
            else:
                points = 10
            picture = PRINTED.get(rank) # отказаться от переменной,
            c = Card(suit=suit, rank=rank, points=points, picture=picture)
            cards.append(c)
        return cards
    
    def get_card(self):
        return self.cards.pop()
    
    def __len__(self):
        return len(self.cards)
