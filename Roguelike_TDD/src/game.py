from src.map import Map
from src.options import *
from src.user import User

class GameOverException(Exception):
    pass

class Game:
    
    def __init__(self):
        self.map = Map()
        self.user = User("StartName")
        
    def generate_map(self, width, height, empty_char):
        self.map.generate(width, height, empty_char)
        
    def place_on_map(self, quantity, char):
        self.map.place(quantity, char)

    def run(self):
        self.generate_map(MAP_WIDTH, MAP_HEIGHT, EMPTY)
        self.place_on_map(MAX_TREES, TREE)
        self.place_on_map(MAX_STONES, STONE)
        self.place_on_map(MAX_LETTERS, LETTER)
        self.place_on_map(MAX_TREASURES, TREASURE)
        self.user.place_on(self.map)
        while True:
            self.turn()

    def turn(self):
        self.map.show()
        self.user.show_info(self.map)
        if self.is_over():
            raise GameOverException()


    def is_over(self):
        return  self.user.is_dead() or self.user.has(MAX_TREASURES, TREASURE)
    
