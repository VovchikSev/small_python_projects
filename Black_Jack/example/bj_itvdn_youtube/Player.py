import abc
from abc import ABC

from Deck import Deck


class AbstractPlayer(abc.ABC):
    def __int__(self, position):
        self.cards = []
        self.position = position
    
    @abc.abstractmethod
    def ask_card(self, deck):
        card = deck.get_card()
        self.cards.append(card)
        return True


class Player(AbstractPlayer):
    
    def ask_card(self, deck):
        pass


# ToDo: А дилер нужен как таковой?
# class Dealler(AbstractPlayer):
#     pass


class Bot(AbstractPlayer, ABC):
    def __int__(self, position):
        pass
