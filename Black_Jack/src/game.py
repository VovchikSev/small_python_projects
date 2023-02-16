"""
Класс игры
интерфейс оконный и прочие
"""
import tkinter as graph


class Game:
    def __init__(self):
        self.win = None
        self.label_dealer_text = None
        self.label_user_text = None
        self.label_desk_text = None
        self._init_window()
    
    def _init_window(self):
        self.win = graph.Tk()
    
    def start_game(self):
        self.win.mainloop()
