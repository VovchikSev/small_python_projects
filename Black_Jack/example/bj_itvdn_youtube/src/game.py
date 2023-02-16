from Black_Jack.example.bj_itvdn_youtube.src.player import *
from Black_Jack.example.bj_itvdn_youtube.src.const import MESSAGES
from Black_Jack.example.bj_itvdn_youtube.src.deck import Deck
import random


class Game:
    
    def __init__(self):
        self.players = []
        self.player = None
        # self.dealer = None
        self.all_players_count = 1
        self.deck = Deck()
    
    @staticmethod
    def _ask_starting(message):
        while True:
            choice = input(message)
            if choice == "n":
                return False
            elif choice == "y":
                return True
    
    def start_game(self):
        message = MESSAGES.get("ask_start")
        if not self._ask_starting(message=message):
            exit(1)
        
        bots_count = int(input("hello, write bots count "))
        self.all_players_count = bots_count + 1
        pos_list = [i for i in range(0, self.all_players_count)]
        random.shuffle(pos_list)
        for _ in range(bots_count):
            pos = pos_list.pop()
            b = Bot(pos)
            self.players.append(b)
            print(b, " is created")
        self.player = Player(position=bots_count + 1)
