import tkinter as graph
from src.desk import *
from src.game import Game

#  есть интересные данные https://www.youtube.com/@user-cx2te1qr9f/videos
# koloada = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
# suits = ['♥', '♠', '♣', '♦']

def enough():
    pass


def take():
    pass


def main():
    print('Работет main')
    root = graph.Tk()
    root.geometry("300x140")
    
    text1 = graph.Label(root, text='Игра в Black Jack', fg="red")
    text1.place(x=100, y=0)
    
    text2 = graph.Label(root, text='У вас 0 очков', fg='blue')
    text2.place(x=110, y=30)
    
    but1 = graph.Button(root, width='15', text='Взять карту', command=take)
    but1.place(x=20, y=60)
    
    but2 = graph.Button(root, width='15', text='Хватит', command=enough)
    but2.place(x=160, y=60)
    
    text3 = graph.Label(root, text='Резкльтат игры', fg='red')
    text3.place(x=90, y=100)
    
    root.mainloop()


if __name__ == '__main__':
    g = Game()
    g.start_game()
