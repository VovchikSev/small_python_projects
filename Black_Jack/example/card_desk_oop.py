import random
from random import shuffle
import e

def RANKS(): return ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]


def SUITS(): return ["Clubs", "Diamonds", "Hearts", "Spades"]


class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.contents = []
        self.contents = [Card(rank, suit) for rank in RANKS() for suit in SUITS()]
        random.shuffle(self.contents)


# создается тестовая колода и перемешивается
d_test = Deck()
while d_test.contents:
    curr_card = d_test.contents.pop(0)
    print(f"Карта {curr_card}  осталось {len(d_test.contents)} карт")
