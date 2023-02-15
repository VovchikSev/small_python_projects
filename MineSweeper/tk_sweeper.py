# https://adior.ru/index.php/robototekhnika/234-mines-python
"""
Попробовать реализовать, выгладит на картинках интересно.
Так же размечена интересно
"""
# Mines
# This is my version of the game, known as mines or Minesweeper.
#
# Created on June 25, 2021.
# Author: Diorditsa A.
# I thank Sergey Polozkov for checking the code for hidden errors.
#
# mines.py is distributed in the hope that it will be useful, but
# WITHOUT WARRANTY OF ANY KIND; not even an implied warranty
# MARKETABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See. See the GNU General Public License for more information.
# You can get a copy of the GNU General Public License
# by link http://www.gnu.org/licenses/

from tkinter import *
from random import choice

frm = [];
btn = []  # Списки с фреймами и кнопками
playArea = [];
nMoves = 0;
mrk = 40  # Игровое поле, счётчик ходов и маркеров


def play(n):  # n - номер нажатой кнопки
    global nMoves, mrk
    nMoves += 1
    if nMoves == 1:  # Если это первый ход игрока,
        tk.title('Achtung, ' + str(mrk) + ' Minen!')
        i = 0
        while i < 40:  # поставим мины,
            j = choice(range(0, 256))
            if j != n and playArea[j] != -1:
                playArea[j] = -1
                i += 1
        for i in range(0, 256):  # подсчитаем количесво мин вокруг каждой клетки
            if playArea[i] != -1:
                k = 0
                if i not in range(0, 256, 16):
                    if playArea[i - 1] == -1: k += 1  # слева
                    if i > 15:
                        if playArea[i - 17] == -1: k += 1  # слева сверху
                    if i < 240:
                        if playArea[i + 15] == -1: k += 1  # слева снизу
                if i not in range(-1, 256, 16):
                    if playArea[i + 1] == -1: k += 1  # справа
                    if i > 15:
                        if playArea[i - 15] == -1: k += 1  # справа сверху
                    if i < 240:
                        if playArea[i + 17] == -1: k += 1  # справа снизу
                if i > 15:
                    if playArea[i - 16] == -1: k += 1  # сверху
                if i < 240:
                    if playArea[i + 16] == -1: k += 1  # снизу
                playArea[i] = k

    btn[n].config(text=playArea[n], state=DISABLED)  # Отображаем игровую ситуацию
    if playArea[n] == 0:
        btn[n].config(text=' ', bg='#ccb')
    elif playArea[n] == -1:
        btn[n].config(text='\u2665')
        if nMoves <= (256 - 40):  # Если игрок ещё не выиграл, то проиграл
            tk.title('Your game is over.')
            nMoves = 256  # Если проиграл, то уже не выиграет
            chainReaction(0)  # Цепная реакция
    if nMoves == (256 - 40):  # Если все клетки открыты, это победа
        tk.title('You win!')
        winner(0)


def chainReaction(j):  # Цепная реакция
    for i in range(j, 256):
        if playArea[i] == -1 and btn[i].cget('text') == ' ':
            btn[i].config(text='\u2665')
            btn[i].flash()
            tk.bell()
            tk.after(50, chainReaction, i + 1)
            break


def winner(j):
    for i in range(j, 256):
        if playArea[i] == 0:
            btn[i].config(state=NORMAL, text='☺')
            btn[i].flash()
            tk.bell()
            btn[i].config(text=' ', state=DISABLED)
            tk.after(50, winner, i + 1)
            break


def marker(n):  # помечаем клетку под которой возможно скрывается мина.
    global mrk
    if (btn[n].cget('state')) != 'disabled':
        if btn[n].cget('text') == '\u2661':
            btn[n].config(text=' ')
            mrk += 1
        else:
            btn[n].config(text='\u2661')
            mrk -= 1
        tk.title('Achtung, ' + str(mrk) + ' Minen!')


def newGame():  # Чистим переменную nMoves, mrk и список playArea и кнопки
    global nMoves, btnBG, mrk
    nMoves = 0;
    mrk = 40
    for i in range(0, 256):
        playArea[i] = 0
        btn[i].config(text=' ', state=NORMAL, bg=btnBG)


tk = Tk()

for i in range(0, 16):  # Размещаем кнопки
    frm.append(Frame())
    frm[i].pack(expand=YES, fill=BOTH)
    for j in range(0, 16):
        btn.append(Button(frm[i], text=' ',
                          font=('mono', 16, 'bold'),
                          width=2, height=1,
                          command=lambda n=i * 16 + j: play(n)))
        btn[i * 16 + j].pack(side=LEFT, expand=NO, fill=Y)
        btn[i * 16 + j].bind('<Button-3>', lambda event, n=i * 16 + j: marker(n))
        playArea.append(0)  # Создаём элементы списка playArea
        tk.update()

Button(tk, text='New game', font=(16),  # Создаём кнопку "New game"
       command=newGame).pack(side=LEFT, expand=YES, fill=Y)

btnBG = btn[0].cget('bg')  # Запоминаем цвет кнопки по умолчанию

mainloop()