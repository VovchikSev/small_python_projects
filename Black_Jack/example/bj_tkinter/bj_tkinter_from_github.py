# Оставить на разборку, начало интересное, но много непонятного ибо китай.
# хороший готовый набор карт

import tkinter as tk
import random as ra
import time
import tkinter.messagebox


class poke(object):
    __Type__ = 0
    __Number__ = 0

    def __init__(self, types, numbers):
        self.__Type__ = types
        self.__Number__ = numbers


# 初始桌面 Начальный рабочий стол, окно наверное имелось в виду.
win = tk.Tk()
win.geometry('800x600')
win.title('21点')  # 21 час.. придумать заголовок покрасивее
image_back = tk.PhotoImage(file='./images/rear.gif')
canvas = tk.Canvas(win, bg='green', width=800, height=600)
# 充当牌组显示一个牌的背面 Действуйте как колода для отображения обратной стороны карты
canvas.create_image(390, 250, image=image_back)
canvas.pack()
# 初始牌组 Начальная колода
types = [1, 2, 3, 4]  # масти
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]  # достоинства карт
# такой метод применен для работы с изображениями
# изображения имеют имена (номер масти)_(номер/достоинство карты).gif
player = []
computer = []
cards = []
image_pock = []
image_pockback = []
# p=numbers
point = 0
for t in types:
    for n in numbers:
        po = poke(t, n)
        cards.append(po)
# 随机打乱 Случайное разрушение:) перемешать колоду по нашему.
ra.shuffle(cards)


# 求和 просить мира... Создание чего? разобраться в контексте.
def countNum(l):
    count = 0
    for b in l:
        if b.__Number__ > 10:
            b.__Number__ = 10
        count = count + b.__Number__
    return count


# 抽牌 Вытягивать карты, наверное имелось в виду выбор карты.
def getpock():
    # 玩家抽牌 Игроки берут карты
    global point
    i = 0
    player.append(cards[point])
    global image_pock
    image_pock = [0] * len(player)
    point = point + 1
    for p_p in player:
        imagefile = './images/{0}-{1}.gif'.format(p_p.__Type__, p_p.__Number__)
        image_pock[i] = tk.PhotoImage(file=imagefile)
        canvas.create_image((300 + i * 20, 400), image=image_pock[i])
        canvas.pack()
        i = i + 1
    win.update()
    # 判断是否爆牌 Определите, является ли карта взрывоопасной...
    # Это чего, не победа или проигрыш по карте произошел
    count = countNum(player)
    if count >= 21:
        tk.messagebox.showinfo('提示', 'player牌炸了')
        win.destroy()
        return
    # 电脑判断其牌组是否应该抽牌 Компьютер определяет, следует ли брать карты из его колоды.
    # Наверное рассчитывает брать ему еще карту или нет?

    if 21 - countNum(computer) <= 5:  # да именно расчет брать карту, если на руках >= 16 не брать.
        stop()
        return

    # 电脑抽牌 Компьютерная графика
    i = 0
    computer.append(cards[point])
    global image_pockback
    image_pockback = [0] * len(computer)
    for c_p in computer:
        imagefile = './images/rear.gif'
        image_pockback[i] = tk.PhotoImage(file=imagefile)
        canvas.create_image((300 + i * 20, 100), image=image_pockback[i])
        canvas.pack()
        i = i + 1
    win.update()
    point = point + 1
    print(countNum(computer))
    # 判断是否爆牌 Определите, является ли карта взрывоопасной...
    count = countNum(computer)
    if count >= 21:
        tk.messagebox.showinfo('提示', '电脑牌炸了')  # "Подсказка", "Компьютерная карта взорвалась"
        win.destroy()


def stop():
    count_player = countNum(player)
    count_computer = countNum(computer)
    if count_computer > count_player:
        tk.messagebox.showinfo('提示', '电脑赢了')  # "Подсказка", "Компьютер выиграл"
        win.destroy()
    if count_computer < count_player:
        tk.messagebox.showinfo('提示', '你赢了')  # "Подсказка", "Ты выиграл"
        win.destroy()
    if count_computer == count_player:
        tk.messagebox.showinfo('提示', '平局')  # "Подсказать", "нарисовать"
        win.destroy()


# 放置按钮  Кнопка размещения
# image=tk.PhotoImage(file='./images/2-1.gif')
button = tk.Button(canvas, text='抽牌', width=10, command=getpock)  # Вытягивать карты
button.place(x=310, y=500, anchor='nw')
button1 = tk.Button(canvas, width=10, text='停牌', command=stop)  # Приостановление торговли
button1.place(x=410, y=500, anchor='nw')
win.mainloop()
