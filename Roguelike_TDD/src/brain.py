from abc import ABC, abstractclassmethod

from src.options import *


class Brain:
    def recognize(self, char):
        
        if char == TREE:
            return Tree()
        if char == STONE:
            return Stone()
        if char == LETTER:
            return Letter()
        if char == TREASURE:
            return Treasure()
        return Empty()


class KnowledgeAbout(ABC):
    @abstractclassmethod
    def message(self):
        pass
    
    @abstractclassmethod
    def can_do(self):
        return [DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT]
    
    @abstractclassmethod
    def do(self, user, map, action):
        pass
    
    # @abstractclassmethod
    def it_barier(self):
        return True


class Empty(KnowledgeAbout):
    def do(self, user, map, action):
        pass
    
    def message(self):
        return MESSAGE_EMPTY
    
    def can_do(self):
        return []
    
    def it_barier(self):
        return False


class Tree(KnowledgeAbout):
    def do(self, user, map, action):
        pass
    
    def message(self):
        return MESSAGE_TREE
    
    def can_do(self):
        return [HACK]


class Stone(KnowledgeAbout):
    def do(self, user, map, action):
        pass
    
    def message(self):
        return MESSAGE_STONE
    
    def can_do(self):
        return []


class Letter(KnowledgeAbout):
    def do(self, user, map, action):
        pass
    
    def message(self):
        return MESSAGE_LETTER
    
    def can_do(self):
        return [READ]


class Treasure(KnowledgeAbout):
    def do(self, user, map, action):
        pass
    
    def message(self):
        return MESSAGE_TREASURE
    
    def can_do(self):
        return [PICK_UP]
