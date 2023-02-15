# пример придется собрать самому с видео
# часть первая https://www.youtube.com/watch?v=i9Q95I5cbyA
# часть вторая https://www.youtube.com/watch?v=CL-2D91k7F0
# github https://github.com/django-group/blackjack_intensive
from Black_Jack.example.bj_itvdn_youtube.src.const import *
from Black_Jack.example.bj_itvdn_youtube.src.deck import Deck

from Black_Jack.example.bj_itvdn_youtube.src.game import Game

if __name__ == "__main__":
    for suit in COLOR_SUITS:
        for rank in RANKS:
            print(f"{rank}{suit} Points:{int(rank) if rank.isdigit() else 11 if rank == 'ace' else 10}")
    # g = Game()
    # g.start_game()
    
