# Набросок змейки по проекту http://pythonicway.com/python-games/python-arcade/18-python-snake

from tkinter import *
from random import *

# создание окна
root = Tk()

# заголовок
root.title("PythonicWay Snake")

# ширина окна
WIDTH = 800

# высота окна
HEIGHT = 600

# размер сегмента змейки
SEG_SIZE = 20

# флаг отвечающий за состояние активности
IN_GAME = True

# создание экземпляра класса  Canvas. в дальнейше еще будет использоваться и залить все зеленым светом
GameField = Canvas(root, width=WIDTH, height=HEIGHT, bg="#003300")
GameField.grid()

# активация фокуса на
GameField.focus_set()


# класс сегмента из которого состоит змейка


class Segment(object):
    def __init__(self, x, y):
        self.instance = GameField.create_rectangle(x, y, x + SEG_SIZE, y + SEG_SIZE, fill="white")


# класс змейки которая состоит из сегментов класса Segment
# у неё будут методы: движения, изменения направления, добавления сегмента


class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        # список доступных направлений движения змейки
        self.mapping = {"Down": (0, 1), "Up": (0, -1), "Left": (-1, 0), "Right": (1, 0)}
        # изначально змейка движется вправо
        self.vektor = self.mapping["Right"]

    def move(self):
        """ двигает змейку в заданном направлении """

        # перебираем все сегменты кроме первого
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = GameField.coords(self.segments[index + 1].instance)
            # задать каждому сегменту координаты (позицию) сегмента стоящего за ним
            GameField.coords(segment, x1, y1, x2, y2)

        # получить координаты сегмента перед головой
        x1, y1, x2, y2 = GameField.coords(self.segments[-2].instance)

        # поместить голову в направлении указанном в векторе
        GameField.coords(self.segments[-1].instance,
                         x1 + self.vektor[0] * SEG_SIZE,
                         x2 + self.vektor[1] * SEG_SIZE,
                         y1 + self.vektor[0] * SEG_SIZE,
                         y2 + self.vektor[1] * SEG_SIZE)

    def change_direction(self, event):
        """ изменяет направление движения змейки """

        # event передаст символ нажатой клавмши
        # и если это клавиша в доступных направлениях
        # изменить направление движения
        if event.keysym in self.mapping:
            self.vektor = self.mapping[event.keysym]

    def add_segment(self):
        """ добавляет сегмент змейке """

        # определить последний сегмент в змейке
        last_segment = GameField.coords(self.segments[0].instance)

        # определить координаты куда поставить следующий сегмент
        x = last_segment[2] - SEG_SIZE
        y = last_segment[3] - SEG_SIZE

        # добавить змейке еще один сегмент в заданные координаты
        self.segments.insert(0, Segment(x, y))


def create_block():
    """ Создает блок в случайной позиции на карте """
    global BLOCK

    posx = SEG_SIZE * (random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE))
    posy = SEG_SIZE * (random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE))

    # блок это кружочек красного цвета
    BLOCK = GameField.create_oval(posx, posy,
                          posx + SEG_SIZE,
                          posy + SEG_SIZE,
                          fill="red")



# создать набор сегментов
segments = [Segment(SEG_SIZE, SEG_SIZE),
           Segment(SEG_SIZE*2, SEG_SIZE),
           Segment(SEG_SIZE*3, SEG_SIZE)]

# собственно змейка
snake = Snake(segments)
GameField.bind("<KeyPress>", snake.change_direction)

def main():
    global IN_GAME

    if IN_GAME:
        # Двигаем змейку
        snake.move()

        # Определяем координаты головы
        head_coords = GameField.coords(snake.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        # Столкновение с границами экрана
        if x1 < 0 or x2 > WIDTH or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False

        # Поедание яблок
        elif head_coords == GameField.coords(BLOCK):
            snake.add_segment()
            GameField.delete(BLOCK)
            GameField.create_block()

        # Самоедство
        else:
            # Проходим по всем сегментам змеи
            for index in range(len(snake.segments) - 1):
                if GameField.coords(snake.segments[index].instance) == head_coords:
                    IN_GAME = False

    # Если не в игре выводим сообщение о проигрыше
    else:
        GameField.create_text(WIDTH / 2, HEIGHT / 2,
                      text="GAME OVER!",
                      font="Arial 20",
                      fill="#ff0000")


# запуск окна -- ожидаемо последняя строка
root.mainloop()
